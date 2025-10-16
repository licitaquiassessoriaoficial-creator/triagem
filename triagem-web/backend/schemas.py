"""
Schemas Pydantic para validação de dados da API
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class EmailProvider(str, Enum):
    GMAIL = "gmail"
    M365 = "m365"


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TriagemJobCreate(BaseModel):
    name: str
    description: Optional[str] = None
    email_account_id: int
    folder_name: str = "INBOX"
    required_skills: List[str] = []
    optional_skills: List[str] = []
    min_experience: int = 0
    max_experience: Optional[int] = None
    required_formations: List[str] = []
    languages: List[str] = []
    skill_weight: float = 0.4
    experience_weight: float = 0.3
    formation_weight: float = 0.2
    language_weight: float = 0.1


class TriagemJobResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    folder_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateResultResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    total_score: float
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True
