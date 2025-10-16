"""
Janela principal Tkinter, componentes, binding, logs
"""
import tkinter as tk
from tkinter import filedialog, scrolledtext
import queue
import threading
from core.logging_setup import setup_logging

class MainWindow:
    def update_counters(self, emails=0, lidos=0, aprovados=0, rejeitados=0):
        self.lbl_emails.config(text=f"E-mails processados: {emails}")
        self.lbl_lidos.config(text=f"Currículos lidos: {lidos}")
        self.lbl_aprovados.config(text=f"Aprovados: {aprovados}")
        self.lbl_rejeitados.config(text=f"Rejeitados: {rejeitados}")
        total = lidos if lidos > 0 else 1
        progresso = int((aprovados + rejeitados) / total * 100)
        self.progress.set(progresso)
    def __init__(self, root):
        self.root = root
        self.root.title("ODQ Recruta")
        self.log_queue = queue.Queue()
        self.logger = setup_logging()

        # Frame principal
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Descrição da vaga
        tk.Label(frame, text="Descrição da vaga:").grid(row=0, column=0, sticky="w")
        self.txt_descricao = tk.Text(frame, height=4, width=60)
        self.txt_descricao.grid(row=0, column=1, columnspan=3, pady=5)

        # Palavras-chave
        tk.Label(frame, text="Palavras-chave (essenciais, separadas por vírgula):").grid(row=1, column=0, sticky="w")
        self.entry_keywords = tk.Entry(frame, width=50)
        self.entry_keywords.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Desejáveis (opcional, vírgula):").grid(row=1, column=2, sticky="w")
        self.entry_desired = tk.Entry(frame, width=30)
        self.entry_desired.grid(row=1, column=3, pady=5)

        # Threshold
        tk.Label(frame, text="Threshold (0-100):").grid(row=2, column=0, sticky="w")
        self.entry_threshold = tk.Entry(frame, width=10)
        self.entry_threshold.grid(row=2, column=1, sticky="w", pady=5)

        # Pasta de saída
        tk.Label(frame, text="Pasta de saída:").grid(row=2, column=2, sticky="w")
        self.entry_outdir = tk.Entry(frame, width=30)
        self.entry_outdir.grid(row=2, column=3, pady=5)
        self.btn_outdir = tk.Button(frame, text="Selecionar", command=self.select_outdir)
        self.btn_outdir.grid(row=2, column=4, padx=5)

        # Checkboxes
        self.var_gmail = tk.BooleanVar()
        self.var_m365 = tk.BooleanVar()
        tk.Checkbutton(frame, text="Usar Gmail", variable=self.var_gmail).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(frame, text="Usar Microsoft 365", variable=self.var_m365).grid(row=3, column=1, sticky="w")

        # Botões
        self.btn_iniciar = tk.Button(frame, text="Iniciar", width=12, command=self.on_iniciar)
        self.btn_iniciar.grid(row=4, column=0, pady=10)
        self.btn_parar = tk.Button(frame, text="Parar", width=12)
        self.btn_parar.grid(row=4, column=1, pady=10)
        self.btn_exportar = tk.Button(frame, text="Exportar Relatório", width=18)
        self.btn_exportar.grid(row=4, column=2, pady=10)
        self.btn_abrir = tk.Button(frame, text="Abrir Pasta", width=12)
        self.btn_abrir.grid(row=4, column=3, pady=10)

        # Barra de progresso
        self.progress = tk.DoubleVar()
        self.progressbar = tk.Scale(frame, variable=self.progress, orient="horizontal", length=400, from_=0, to=100, showvalue=0)
        self.progressbar.grid(row=5, column=0, columnspan=4, pady=10)

        # Contadores
        self.lbl_emails = tk.Label(frame, text="E-mails processados: 0")
        self.lbl_emails.grid(row=6, column=0, sticky="w")
        self.lbl_lidos = tk.Label(frame, text="Currículos lidos: 0")
        self.lbl_lidos.grid(row=6, column=1, sticky="w")
        self.lbl_aprovados = tk.Label(frame, text="Aprovados: 0")
        self.lbl_aprovados.grid(row=6, column=2, sticky="w")
        self.lbl_rejeitados = tk.Label(frame, text="Rejeitados: 0")
        self.lbl_rejeitados.grid(row=6, column=3, sticky="w")

        # Janela de logs
        tk.Label(frame, text="Logs:").grid(row=7, column=0, sticky="nw")
        self.txt_logs = scrolledtext.ScrolledText(frame, height=10, width=100, state="disabled")
        self.txt_logs.grid(row=7, column=1, columnspan=4, pady=10)

    def select_outdir(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.entry_outdir.delete(0, tk.END)
            self.entry_outdir.insert(0, dirname)

    def update_logs(self, msg):
        self.txt_logs.config(state="normal")
        self.txt_logs.insert(tk.END, msg + "\n")
        self.txt_logs.see(tk.END)
        self.txt_logs.config(state="disabled")

    def poll_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.update_logs(msg)
        self.root.after(500, self.poll_log_queue)

    def on_iniciar(self):
        self.update_logs("[TESTE] Botão Iniciar clicado!")
        # Validação dos campos
        descricao = self.txt_descricao.get("1.0", tk.END).strip()
        keywords = self.entry_keywords.get().strip()
        desired = self.entry_desired.get().strip()
        threshold = self.entry_threshold.get().strip()
        outdir = self.entry_outdir.get().strip()
        use_gmail = self.var_gmail.get()
        use_m365 = self.var_m365.get()

        if not descricao:
            self.update_logs("[ERRO] Descrição da vaga obrigatória.")
            return
        if not keywords:
            self.update_logs("[ERRO] Palavras-chave obrigatórias.")
            return
        try:
            threshold_val = int(threshold)
            if not (0 <= threshold_val <= 100):
                raise ValueError
        except Exception:
            self.update_logs("[ERRO] Threshold deve ser um número entre 0 e 100.")
            return
        if not outdir:
            self.update_logs("[ERRO] Selecione a pasta de saída.")
            return
        if not (use_gmail or use_m365):
            self.update_logs("[ERRO] Selecione ao menos uma conta de e-mail.")
            return

        self.update_logs("[INFO] Iniciando pipeline...")
        # Iniciar pipeline real em thread separada
        import threading
        threading.Thread(target=self.start_pipeline, daemon=True).start()

    def start_pipeline(self):
        # Contadores locais
        emails_count = 0
        lidos_count = 0
        aprovados_count = 0
        rejeitados_count = 0
        try:
            from workers.pipeline import Pipeline
            from core.models import JobSpec
            from pathlib import Path

            descricao = self.txt_descricao.get("1.0", tk.END).strip()
            keywords = [k.strip() for k in self.entry_keywords.get().split(",") if k.strip()]
            desired = [k.strip() for k in self.entry_desired.get().split(",") if k.strip()]
            threshold = int(self.entry_threshold.get().strip())
            outdir = Path(self.entry_outdir.get().strip())
            use_gmail = self.var_gmail.get()
            use_m365 = self.var_m365.get()

            job = JobSpec(
                title="",
                description=descricao,
                required_keywords=keywords,
                desired_keywords=desired,
                threshold=threshold
            )

            pipeline = Pipeline(
                job=job,
                out_dir=outdir,
                use_gmail=use_gmail,
                use_m365=use_m365,
                log_queue=self.log_queue
            )

            self.update_logs("[INFO] Pipeline iniciado!")
            # Executa pipeline e atualiza contadores
            def run_and_update():
                # Busca de emails e anexos
                attachments = []
                if use_gmail:
                    self.update_logs("[INFO] Buscando anexos no Gmail...")
                if use_m365:
                    self.update_logs("[INFO] Buscando anexos no Microsoft 365...")
                # Chama pipeline.run() (já atualiza log_queue)
                pipeline.run()
                # Atualiza contadores finais
                emails_count = len(pipeline.aprovados)
                lidos_count = len(pipeline.aprovados)
                aprovados_count = sum(1 for c in pipeline.aprovados if c.approved)
                rejeitados_count = lidos_count - aprovados_count
                self.update_counters(emails=emails_count, lidos=lidos_count, aprovados=aprovados_count, rejeitados=rejeitados_count)
                self.update_logs("[INFO] Pipeline finalizado!")
            run_and_update()
        except Exception as e:
            import traceback
            self.update_logs(f"[ERRO] {e}\n{traceback.format_exc()}")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    app.poll_log_queue()
    root.mainloop()

