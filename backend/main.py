"""
Sistema de Triagem de Currículos - Backend Mínimo
Este é um backend mínimo para deploy que redireciona para o frontend.
O sistema funciona principalmente no modo offline/frontend.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema Triagem ODQ",
    description="Backend mínimo - Sistema funciona no frontend",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Redireciona para o frontend"""
    return {"message": "Sistema Triagem ODQ - Backend Ativo", "status": "online", "mode": "minimal"}

@app.get("/health")
async def health_check():
    """Health check para Railway"""
    return {"status": "healthy", "service": "triagem-backend-minimal"}

@app.get("/status")
async def status():
    """Status do sistema"""
    return {
        "backend": "minimal",
        "frontend": "full-featured",
        "mode": "production",
        "recommendation": "Use frontend em localhost:3000 para funcionalidade completa"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)