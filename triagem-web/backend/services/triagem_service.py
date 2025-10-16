"""
Serviço principal para processamento de triagem de currículos
"""
import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import (
    TriagemJob, CandidateResult, JobStatus,
    EmailProvider
)
from schemas import TriagemJobCreate
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class TriagemService:
    """
    Serviço principal para gerenciamento de triagens
    """
    def __init__(self, db: Session):
        self.db = db
    async def create_job(
        self,
        job_data: TriagemJobCreate,
        user_id: int
    ) -> TriagemJob:
        """
        Criar nova triagem
        """
        job = TriagemJob(
            user_id=user_id,
            name=job_data.name,
            description=job_data.description,
            email_provider=job_data.email_provider,
            email_config=job_data.email_config,
            job_description=job_data.job_description,
            required_skills=job_data.required_skills,
            optional_skills=job_data.optional_skills,
            min_experience=job_data.min_experience,
            max_experience=job_data.max_experience,
            required_formations=job_data.required_formations,
            languages=job_data.languages,
            skill_weight=job_data.skill_weight,
            experience_weight=job_data.experience_weight,
            formation_weight=job_data.formation_weight,
            language_weight=job_data.language_weight,
            status=JobStatus.PENDING
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        logger.info(f"Nova triagem criada: {job.id} - {job.name}")
        return job
    async def get_user_jobs(self, user_id: int) -> List[TriagemJob]:
        """
        Listar todas as triagens do usuário
        """
        return self.db.query(TriagemJob).filter(
            TriagemJob.user_id == user_id
        ).order_by(TriagemJob.created_at.desc()).all()
    async def get_job(self, job_id: int, user_id: int) -> Optional[TriagemJob]:
        """
        Obter triagem específica do usuário
        """
        return self.db.query(TriagemJob).filter(
            and_(
                TriagemJob.id == job_id,
                TriagemJob.user_id == user_id
            )
        ).first()
    async def get_job_results(
        self,
        job_id: int,
        user_id: int,
        approved_only: bool = False
    ) -> List[CandidateResult]:
        """
        Obter resultados de uma triagem
        """
        # Verificar se o job pertence ao usuário
        job = await self.get_job(job_id, user_id)
        if not job:
            return []
        query = self.db.query(CandidateResult).filter(
            CandidateResult.job_id == job_id
        )
        if approved_only:
            query = query.filter(CandidateResult.is_approved is True)
        return query.order_by(
            CandidateResult.total_score.desc()
        ).all()
    async def stop_job(self, job_id: int, user_id: int) -> bool:
        """
        Parar execução de uma triagem
        """
        job = await self.get_job(job_id, user_id)
        if not job:
            return False
        if job.status == JobStatus.RUNNING:
            job.status = JobStatus.STOPPED
            job.completed_at = datetime.utcnow()
            self.db.commit()
            logger.info(f"Triagem {job_id} parada pelo usuário")
            return True
        return False
    async def process_triagem(
        self,
        job_id: int,
        job_data: TriagemJobCreate
    ):
        """
        Processar triagem em background
        """
        job = self.db.query(TriagemJob).filter(
            TriagemJob.id == job_id
        ).first()
        if not job:
            logger.error(f"Job {job_id} não encontrado")
            return
        try:
            # Atualizar status para running
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            self.db.commit()
            logger.info(f"Iniciando processamento da triagem {job_id}")
            # 1. Conectar ao email e baixar currículos
            candidates = await self._fetch_candidates(job)
            # 2. Processar cada candidato
            await self._process_candidates(job, candidates)
            # 3. Finalizar job
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.progress = 100.0
            self.db.commit()
            logger.info(f"Triagem {job_id} concluída com sucesso")
        except Exception as e:
            logger.error(f"Erro na triagem {job_id}: {str(e)}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()
    async def _fetch_candidates(self, job: TriagemJob) -> List[Dict]:
        """
        Buscar candidatos via email
        """
        candidates = []
        try:
            if job.email_provider == EmailProvider.GMAIL:
                candidates = await self._fetch_gmail_candidates(job)
            elif job.email_provider == EmailProvider.M365:
                candidates = await self._fetch_m365_candidates(job)
            job.total_candidates = len(candidates)
            self.db.commit()
            logger.info(f"Encontrados {len(candidates)} candidatos")
            return candidates
        except Exception as e:
            logger.error(f"Erro ao buscar candidatos: {str(e)}")
            raise
    async def _fetch_gmail_candidates(self, job: TriagemJob) -> List[Dict]:
        """
        Buscar candidatos via Gmail IMAP
        """
        # Implementação simulada - seria integrada com o código original
        await asyncio.sleep(2)  # Simular tempo de processamento
        return [
            {
                "name": "João Silva",
                "email": "joao@email.com",
                "resume_text": "Experiência em Python, Django...",
                "resume_filename": "joao_cv.pdf"
            },
            {
                "name": "Maria Santos",
                "email": "maria@email.com",
                "resume_text": "Desenvolvedora Full Stack...",
                "resume_filename": "maria_cv.pdf"
            }
        ]
    async def _fetch_m365_candidates(self, job: TriagemJob) -> List[Dict]:
        """
        Buscar candidatos via Microsoft 365 Graph API
        """
        # Implementação simulada - seria integrada com o código original
        await asyncio.sleep(2)  # Simular tempo de processamento
        return [
            {
                "name": "Pedro Costa",
                "email": "pedro@email.com",
                "resume_text": "Especialista em React, Node.js...",
                "resume_filename": "pedro_cv.pdf"
            }
        ]
    async def _process_candidates(
        self,
        job: TriagemJob,
        candidates: List[Dict]
    ):
        """
        Processar lista de candidatos
        """
        total = len(candidates)
        processed = 0
        for candidate_data in candidates:
            try:
                # Verificar se já foi processado (hash do resume)
                resume_hash = hashlib.md5(
                    candidate_data["resume_text"].encode()
                ).hexdigest()
                existing = self.db.query(CandidateResult).filter(
                    and_(
                        CandidateResult.job_id == job.id,
                        CandidateResult.resume_hash == resume_hash
                    )
                ).first()
                if existing:
                    logger.info(
                        f"Candidato já processado: {candidate_data['email']}"
                    )
                    continue
                # Análise do currículo
                analysis = await self._analyze_resume(
                    candidate_data["resume_text"],
                    job
                )
                # Criar resultado
                result = CandidateResult(
                    job_id=job.id,
                    name=candidate_data.get("name"),
                    email=candidate_data["email"],
                    resume_text=candidate_data["resume_text"],
                    resume_filename=candidate_data.get("resume_filename"),
                    resume_hash=resume_hash,
                    skill_score=analysis["skill_score"],
                    experience_score=analysis["experience_score"],
                    formation_score=analysis["formation_score"],
                    language_score=analysis["language_score"],
                    total_score=analysis["total_score"],
                    found_skills=analysis["found_skills"],
                    experience_years=analysis["experience_years"],
                    found_formations=analysis["found_formations"],
                    found_languages=analysis["found_languages"],
                    is_approved=analysis["total_score"] >= 70.0
                )
                self.db.add(result)
                processed += 1
                # Atualizar progresso
                job.processed_candidates = processed
                job.progress = (processed / total) * 100
                if result.is_approved:
                    job.approved_candidates += 1
                self.db.commit()
                logger.info(
                    f"Candidato processado: {candidate_data['email']} - "
                    f"Score: {analysis['total_score']:.1f}"
                )
                # Pausa para não sobrecarregar
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(
                    f"Erro ao processar candidato "
                    f"{candidate_data.get('email')}: {str(e)}"
                )
                continue
    async def _analyze_resume(
        self,
        resume_text: str,
        job: TriagemJob
    ) -> Dict[str, Any]:
        """
        Analisar currículo e calcular pontuação
        """
        # Implementação básica de análise
        resume_lower = resume_text.lower()
        # Análise de habilidades
        found_skills = []
        for skill in job.required_skills + job.optional_skills:
            if skill.lower() in resume_lower:
                found_skills.append(skill)
        if job.required_skills:
            skill_score = (len(found_skills) / len(job.required_skills)) * 100
        else:
            skill_score = 0
        # Análise de experiência (simulada)
        experience_years = self._extract_experience_years(resume_text)
        min_exp = max(job.min_experience, 1)
        exp_score = min((experience_years / min_exp) * 100, 100)
        # Análise de formação
        found_formations = []
        formation_score = 50.0  # Score padrão
        # Análise de idiomas
        found_languages = []
        language_score = 50.0  # Score padrão
        # Calcular score total ponderado
        total_score = (
            skill_score * job.skill_weight +
            exp_score * job.experience_weight +
            formation_score * job.formation_weight +
            language_score * job.language_weight
        )
        return {
            "skill_score": skill_score,
            "experience_score": exp_score,
            "formation_score": formation_score,
            "language_score": language_score,
            "total_score": total_score,
            "found_skills": found_skills,
            "experience_years": experience_years,
            "found_formations": found_formations,
            "found_languages": found_languages
        }
    def _extract_experience_years(self, resume_text: str) -> int:
        """
        Extrair anos de experiência do currículo (implementação básica)
        """
        import re
        # Buscar por padrões como "5 anos", "3 years", etc.
        patterns = [
            r'(\d+)\s*anos?\s*de\s*experiência',
            r'(\d+)\s*years?\s*of\s*experience',
            r'experiência.*?(\d+)\s*anos?',
            r'experience.*?(\d+)\s*years?'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, resume_text.lower())
            if matches:
                return max([int(match) for match in matches])
        return 1  # Experiência mínima padrão
    async def export_results(
        self,
        job_id: int,
        user_id: int,
        format: str
    ) -> str:
        """
        Exportar resultados da triagem
        """
        results = await self.get_job_results(job_id, user_id)
        if format == "json":
            return json.dumps([
                {
                    "name": r.name,
                    "email": r.email,
                    "total_score": r.total_score,
                    "is_approved": r.is_approved,
                    "found_skills": r.found_skills
                }
                for r in results
            ], indent=2)
        elif format == "csv":
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            # Headers
            writer.writerow([
                "Nome", "Email", "Score Total", "Aprovado",
                "Habilidades Encontradas"
            ])
            # Data
            for r in results:
                writer.writerow([
                    r.name or "",
                    r.email,
                    f"{r.total_score:.1f}",
                    "Sim" if r.is_approved else "Não",
                    ", ".join(r.found_skills)
                ])
            return output.getvalue()
        else:
            raise ValueError(f"Formato não suportado: {format}")

