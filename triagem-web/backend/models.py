"""
Modelos SQLAlchemy para o banco PostgreSQL no Railway
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    Float, JSON, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
Base = declarative_base()
class JobStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"
class EmailProvider(enum.Enum):
    GMAIL = "gmail"
    M365 = "m365"
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    # Relacionamentos
    triagem_jobs = relationship("TriagemJob", back_populates="user")
class TriagemJob(Base):
    __tablename__ = "triagem_jobs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING)
    progress = Column(Float, default=0.0)
    # Configurações de email
    email_provider = Column(SQLEnum(EmailProvider), nullable=False)
    email_config = Column(JSON)  # Credenciais e configurações
    # Configurações de triagem
    job_description = Column(Text, nullable=False)
    required_skills = Column(JSON)  # Lista de habilidades obrigatórias
    optional_skills = Column(JSON)  # Lista de habilidades opcionais
    min_experience = Column(Integer, default=0)
    max_experience = Column(Integer)
    required_formations = Column(JSON)  # Lista de formações obrigatórias
    languages = Column(JSON)  # Idiomas requeridos
    # Configurações de pontuação
    skill_weight = Column(Float, default=0.4)  # Peso das habilidades
    experience_weight = Column(Float, default=0.3)  # Peso da experiência
    formation_weight = Column(Float, default=0.2)  # Peso da formação
    language_weight = Column(Float, default=0.1)  # Peso dos idiomas
    # Metadados de execução
    total_candidates = Column(Integer, default=0)
    processed_candidates = Column(Integer, default=0)
    approved_candidates = Column(Integer, default=0)
    execution_log = Column(JSON)  # Log de execução
    error_message = Column(Text)
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    # Relacionamentos
    user = relationship("User", back_populates="triagem_jobs")
    candidates = relationship("CandidateResult", back_populates="job")
class CandidateResult(Base):
    __tablename__ = "candidate_results"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("triagem_jobs.id"), nullable=False)
    # Dados do candidato
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    linkedin = Column(String(500))
    # Análise do currículo
    resume_text = Column(Text)
    resume_filename = Column(String(255))
    resume_hash = Column(String(64))  # Hash MD5 para evitar duplicatas
    # Pontuação detalhada
    skill_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    formation_score = Column(Float, default=0.0)
    language_score = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    # Detalhamento da análise
    found_skills = Column(JSON)  # Habilidades encontradas
    experience_years = Column(Integer)
    found_formations = Column(JSON)  # Formações encontradas
    found_languages = Column(JSON)  # Idiomas encontrados
    # Status
    is_approved = Column(Boolean, default=False)
    manual_review = Column(Boolean, default=False)
    review_notes = Column(Text)
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    # Relacionamentos
    job = relationship("TriagemJob", back_populates="candidates")
class EmailAccount(Base):
    __tablename__ = "email_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    provider = Column(SQLEnum(EmailProvider), nullable=False)
    email_address = Column(String(255), nullable=False)
    # Configurações específicas por provedor
    config = Column(JSON, nullable=False)  # Credenciais e configurações
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime(timezone=True))
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

