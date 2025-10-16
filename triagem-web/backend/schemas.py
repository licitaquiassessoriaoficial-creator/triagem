"""
Schemas Pydantic para validação de dados da API
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"
class EmailProvider(str, Enum):
    GMAIL = "gmail"
    M365 = "m365"
# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
class UserCreate(UserBase):
    password: str
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True
# Email Account Schemas
class EmailAccountBase(BaseModel):
    name: str
    provider: EmailProvider
    email_address: EmailStr
class EmailAccountCreate(EmailAccountBase):
    config: Dict[str, Any]
class EmailAccountResponse(EmailAccountBase):
    id: int
    user_id: int
    is_active: bool
    last_sync: Optional[datetime]
    created_at: datetime
    class Config:
        orm_mode = True
# Triagem Job Schemas
class TriagemJobBase(BaseModel):
    name: str
    description: Optional[str]
    job_description: str
    required_skills: List[str] = []
    optional_skills: List[str] = []
    min_experience: int = 0
    max_experience: Optional[int]
    required_formations: List[str] = []
    languages: List[str] = []
class TriagemJobCreate(TriagemJobBase):
    email_provider: EmailProvider
    email_config: Dict[str, Any]
    skill_weight: float = 0.4
    experience_weight: float = 0.3
    formation_weight: float = 0.2
    language_weight: float = 0.1
class TriagemJobUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[JobStatus]
class TriagemJobResponse(TriagemJobBase):
    id: int
    user_id: int
    status: JobStatus
    progress: float
    email_provider: EmailProvider
    total_candidates: int
    processed_candidates: int
    approved_candidates: int
    skill_weight: float
    experience_weight: float
    formation_weight: float
    language_weight: float
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    class Config:
        orm_mode = True
# Candidate Result Schemas
class CandidateResultBase(BaseModel):
    name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    linkedin: Optional[str]
class CandidateResultCreate(CandidateResultBase):
    resume_text: str
    resume_filename: str
    resume_hash: str
class CandidateResultUpdate(BaseModel):
    is_approved: Optional[bool]
    manual_review: Optional[bool]
    review_notes: Optional[str]
class CandidateResultResponse(CandidateResultBase):
    id: int
    job_id: int
    resume_filename: Optional[str]
    skill_score: float
    experience_score: float
    formation_score: float
    language_score: float
    total_score: float
    found_skills: List[str] = []
    experience_years: Optional[int]
    found_formations: List[str] = []
    found_languages: List[str] = []
    is_approved: bool
    manual_review: bool
    review_notes: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True
# Authentication Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
# API Response Schemas
class MessageResponse(BaseModel):
    message: str
class ErrorResponse(BaseModel):
    detail: str
# Export Schemas
class ExportRequest(BaseModel):
    format: str
    approved_only: bool = False
class ExportResponse(BaseModel):
    filename: str
    content: str
    media_type: str
# Statistics Schemas
class JobStatistics(BaseModel):
    total_jobs: int
    completed_jobs: int
    running_jobs: int
    failed_jobs: int
    total_candidates: int
    approved_candidates: int
    avg_score: float
class DashboardData(BaseModel):
    recent_jobs: List[TriagemJobResponse]
    statistics: JobStatistics
    top_skills: List[Dict[str, Any]]
    score_distribution: List[Dict[str, Any]]
# WebSocket Schemas
class WSMessage(BaseModel):
    type: str
    data: Dict[str, Any]
class JobProgressUpdate(BaseModel):
    job_id: int
    status: JobStatus
    progress: float
    processed_candidates: int
    total_candidates: int
    message: Optional[str]

