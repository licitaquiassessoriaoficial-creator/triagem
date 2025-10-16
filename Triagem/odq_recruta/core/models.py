"""
Dataclasses principais: Attachment, CandidateResult, JobSpec
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

@dataclass
class Attachment:
    email_id: str
    sender: str
    subject: str
    filename: str
    hash: str
    path: Path
    received_at: str

@dataclass
class CandidateResult:
    attachment: Attachment
    score: int
    approved: bool
    extracted_text: Optional[str] = None

@dataclass
class JobSpec:
    title: str
    description: str
    required_keywords: List[str]
    desired_keywords: Optional[List[str]]
    threshold: int

