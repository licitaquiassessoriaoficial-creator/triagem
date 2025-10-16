"""
API Principal do Sistema de Triagem ODQ
FastAPI backend para deploy no Railway
"""

import os
from typing import List

from database import engine, get_db
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import Base
from schemas import (
    CandidateResultResponse,
    TriagemJobCreate,
    TriagemJobResponse,
)
from services.auth_service import AuthService
from services.triagem_service import TriagemService
from sqlalchemy.orm import Session

# Criar tabelas
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Triagem ODQ API",
    description="API para triagem automatizada de currículos",
    version="2.0.0",
)


# CORS para permitir requests do frontend Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://triagem-odq.netlify.app",  # Domínio Netlify
        "http://localhost:3000",  # Dev local
        "http://localhost:3001",  # Dev local alternativo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Autenticação
security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Middleware de autenticação"""
    return await auth_service.verify_token(credentials.credentials)


@app.get("/")
async def root():
    """Health check"""
    return {"message": "Sistema de Triagem ODQ API", "status": "online"}


@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "2.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


@app.post("/auth/login")
async def login(credentials: dict):
    """Login de usuário"""
    try:
        token = await auth_service.authenticate(
            credentials.get("email"), credentials.get("password")
        )
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/triagem/jobs", response_model=TriagemJobResponse)
async def create_triagem_job(
    job_data: TriagemJobCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Criar nova triagem"""
    triagem_service = TriagemService(db)
    # Criar job na base de dados
    job = await triagem_service.create_job(job_data, current_user["id"])
    # Iniciar processamento em background
    background_tasks.add_task(
        triagem_service.process_triagem, job.id, job_data
    )
    return job


@app.get("/triagem/jobs", response_model=List[TriagemJobResponse])
async def get_user_jobs(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Listar triagens do usuário"""
    triagem_service = TriagemService(db)
    return await triagem_service.get_user_jobs(current_user["id"])


@app.get("/triagem/jobs/{job_id}", response_model=TriagemJobResponse)
async def get_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obter detalhes de uma triagem"""
    triagem_service = TriagemService(db)
    job = await triagem_service.get_job(job_id, current_user["id"])
    if not job:
        raise HTTPException(status_code=404, detail="Triagem não encontrada")
    return job


@app.get(
    "/triagem/jobs/{job_id}/results",
    response_model=List[CandidateResultResponse],
)
async def get_job_results(
    job_id: int,
    approved_only: bool = False,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obter resultados de uma triagem"""
    triagem_service = TriagemService(db)
    return await triagem_service.get_job_results(
        job_id, current_user["id"], approved_only
    )


@app.post("/triagem/jobs/{job_id}/stop")
async def stop_job(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Parar uma triagem em execução"""
    triagem_service = TriagemService(db)
    success = await triagem_service.stop_job(job_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=400, detail="Não foi possível parar a triagem"
        )
    return {"message": "Triagem parada com sucesso"}


@app.get("/triagem/jobs/{job_id}/status")
async def get_job_status(
    job_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Obter status de uma triagem"""
    triagem_service = TriagemService(db)
    job = await triagem_service.get_job(job_id, current_user["id"])
    if not job:
        raise HTTPException(status_code=404, detail="Triagem não encontrada")
    return {
        "status": job.status,
        "progress": job.progress,
        "total_candidates": job.total_candidates,
        "processed_candidates": job.processed_candidates,
    }


@app.post("/triagem/jobs/{job_id}/export/{format}")
async def export_results(
    job_id: int,
    format: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Exportar resultados da triagem"""
    if format not in ["csv", "json", "xlsx"]:
        raise HTTPException(status_code=400, detail="Formato não suportado")
    triagem_service = TriagemService(db)
    file_content = await triagem_service.export_results(
        job_id, current_user["id"], format
    )
    media_types = {
        "csv": "text/csv",
        "json": "application/json",
        "xlsx": "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet",
    }
    return {
        "filename": f"triagem_{job_id}.{format}",
        "content": file_content,
        "media_type": media_types[format],
    }


# Import opcional para desenvolvimento
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
