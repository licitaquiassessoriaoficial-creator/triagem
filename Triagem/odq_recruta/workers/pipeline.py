"""
Pipeline principal: busca, download, extração, score, salvamento
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import List
from core.hashing import sha256_bytes, load_hash_cache, save_hash_cache
from core.text_extract import extract_text
from core.scoring import compute_score
from core.models import CandidateResult, JobSpec, Attachment
from core.exporters import export_csv, export_json
import queue
import threading
import time

class Pipeline:
    def __init__(self, job: JobSpec, out_dir: Path, use_gmail: bool, use_m365: bool, log_queue: queue.Queue):
        self.job = job
        self.out_dir = out_dir
        self.use_gmail = use_gmail
        self.use_m365 = use_m365
        self.log_queue = log_queue
        self.stop_event = threading.Event()
        self.hash_cache = load_hash_cache()
        self.aprovados: List[CandidateResult] = []

    def run(self):
        self.log_queue.put("[INFO] Iniciando busca de emails...")
        attachments = []
        # Gmail
        if self.use_gmail:
            try:
                from core.config import load_and_validate_env
                from email_clients.gmail_imap import GmailIMAPClient
                env = load_and_validate_env(use_gmail=True, use_m365=False)
                gmail = GmailIMAPClient(env["GMAIL_USERNAME"], env["GMAIL_APP_PASSWORD"])
                gmail.connect()
                self.log_queue.put("[INFO] Buscando anexos no Gmail...")
                attachments += gmail.fetch_attachments()
            except Exception as e:
                self.log_queue.put(f"[ERRO] Gmail: {e}")
        # M365
        if self.use_m365:
            from core.config import load_and_validate_env
            from email_clients.m365_graph import M365GraphClient
            env = load_and_validate_env(use_gmail=False, use_m365=True)
            scopes = env["MS_SCOPES"].split(",") if "," in env["MS_SCOPES"] else [env["MS_SCOPES"]]
            client_secret = env.get("MS_CLIENT_SECRET")
            token_cache_path = Path(".odq_cache/msal_token.json")
            m365 = M365GraphClient(
                env["MS_CLIENT_ID"], env["MS_TENANT_ID"], env["MS_REDIRECT_URI"], scopes, token_cache_path, client_secret
            )
            try:
                m365.authenticate()
            except Exception as e:
                import traceback
                self.log_queue.put(f"[ERRO] M365: {e}\n{traceback.format_exc()}")
                return
            self.log_queue.put("[INFO] Buscando anexos no Microsoft 365...")
            attachments += m365.fetch_attachments()

        self.log_queue.put(f"[INFO] Total de anexos encontrados: {len(attachments)}")
        # Deduplicação
        new_attachments = [a for a in attachments if a["hash"] not in self.hash_cache]
        self.log_queue.put(f"[INFO] Anexos novos após deduplicação: {len(new_attachments)}")
        # Download e salvar temporário
        temp_dir = Path(".odq_temp")
        temp_dir.mkdir(exist_ok=True)
        for att in new_attachments:
            temp_path = temp_dir / att["hash"]
            with open(temp_path, "wb") as f:
                f.write(att["payload"])
            att["path"] = temp_path

        # Extração + análise paralela
        self.log_queue.put("[INFO] Extraindo texto e calculando score...")
        from core.text_extract import extract_text
        from core.scoring import compute_score
        from core.models import Attachment, CandidateResult
        aprovados = []
        def process_attachment(att):
            texto = extract_text(att["path"])
            score_dict = compute_score(texto or "", self.job)
            score = score_dict["score_total"]
            approved = score >= self.job.threshold
            attachment = Attachment(
                email_id=att["email_id"], sender=att["sender"], subject=att["subject"],
                filename=att["filename"], hash=att["hash"], path=att["path"], received_at=att["received_at"]
            )
            result = CandidateResult(attachment=attachment, score=score, approved=approved, extracted_text=texto)
            return result

        with ProcessPoolExecutor() as proc_pool:
            results = list(proc_pool.map(process_attachment, new_attachments))

        # Salvar aprovados
        self.log_queue.put("[INFO] Salvando currículos aprovados...")
        from datetime import datetime
        slug = self.job.title or "vaga"
        data_str = datetime.now().strftime("%Y-%m-%d")
        saida_dir = self.out_dir / slug / data_str
        saida_dir.mkdir(parents=True, exist_ok=True)
        for res in results:
            if res.approved:
                # Renomear arquivo: score_nome_original.ext
                ext = Path(res.attachment.filename).suffix
                nome = f"{res.score}_{res.attachment.filename}"
                dest_path = saida_dir / nome
                Path(res.attachment.path).rename(dest_path)
                res.attachment.path = dest_path
                aprovados.append(res)
                self.hash_cache.add(res.attachment.hash)

        self.aprovados = aprovados
        self.log_queue.put(f"[INFO] Total aprovados: {len(aprovados)}")
        save_hash_cache(self.hash_cache)
        # Exportar relatório
        from core.exporters import export_csv, export_json
        export_csv(self.aprovados, self.out_dir / "aprovados.csv")
        export_json(self.aprovados, self.out_dir / "aprovados.json")
        self.log_queue.put("[INFO] Relatórios exportados!")

    def stop(self):
        self.stop_event.set()
