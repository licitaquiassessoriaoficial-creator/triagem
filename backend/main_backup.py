"""
Sistema de Triagem de Currículos - Backend FastAPI
Autor: ODQ Sistemas
"""

import os
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Importar o sistema de triagem existente
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

try:
    from confidential_client_secret_sample import (
        extract_text_any, _has_exact_phrase,
        list_attachments, download_attachment, candidato_aprovado,
        save_bytes, safe_name
    )
    print("✅ Módulo confidential_client_secret_sample importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print(f"📁 Caminho pai: {parent_dir}")
    print("🔍 Arquivos no diretório pai:")
    try:
        files = os.listdir(parent_dir)
        for f in files:
            if f.endswith('.py'):
                print(f"   📄 {f}")
    except Exception as ex:
        print(f"   ❌ Erro ao listar: {ex}")
    sys.exit(1)

app = FastAPI(
    title="Sistema de Triagem ODQ",
    description="API para triagem automática de currículos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para Netlify e Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://triagem-odq.netlify.app",
        "https://system-triagem-odq.netlify.app",
        "*"  # Em produção, especificar domínios exatos
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic


class TriagemRequest(BaseModel):
    vaga_descricao: str
    palavras_chave: List[str]
    formacoes: List[str] = []
    palavras_negativas: List[str] = []
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None


def get_token_from_env(client_id, client_secret, authority, scope):
    """Função para obter token usando variáveis de ambiente"""
    try:
        from msal import ConfidentialClientApplication

        app = ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority
        )

        result = app.acquire_token_silent(scopes=scope, account=None)

        if not result:
            result = app.acquire_token_for_client(scopes=scope)

        if "access_token" in result:
            return result["access_token"]
        else:
            error_desc = result.get('error_description', 'Erro desconhecido')
            print(f"Erro ao obter token: {error_desc}")
            return None

    except Exception as e:
        print(f"Erro ao obter token: {str(e)}")
        return None


class TriagemEmailRequest(BaseModel):
    vaga_descricao: str
    palavras_chave: List[str]
    formacoes: List[str] = []
    palavras_negativas: List[str] = []
    usar_ocr: bool = True
    max_emails: int = 500


class TriagemResponse(BaseModel):
    success: bool
    message: str
    total_processados: int
    total_aprovados: int
    percentual_aprovacao: float
    arquivos_aprovados: List[dict]
    detalhes_usuarios: Optional[List[dict]] = []


class StatusResponse(BaseModel):
    status: str
    message: str
    timestamp: str


# Diretórios
UPLOAD_DIR = Path("../uploads")
APROVADOS_DIR = Path("../aprovados")
UPLOAD_DIR.mkdir(exist_ok=True)
APROVADOS_DIR.mkdir(exist_ok=True)

# Security
security = HTTPBearer()


def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verificação simples de token (implementar JWT em produção)"""
    expected_token = os.getenv("AUTH_TOKEN", "odq-triagem-2024")
    print(f"🔐 Token recebido: {credentials.credentials[:10]}...")
    print(f"🔐 Token esperado: {expected_token[:10]}...")
    
    if credentials.credentials != expected_token:
        print("❌ Token inválido!")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    print("✅ Token válido!")
    return credentials.credentials


@app.get("/", response_model=StatusResponse)
async def root():
    """Endpoint raiz - status da API"""
    print("📍 Endpoint root acessado")
    return StatusResponse(
        status="online",
        message="Sistema de Triagem ODQ - API funcionando v2.0",
        timestamp=datetime.now().isoformat()
    )


@app.get("/health")
async def health_check_simple():
    """Verificação de saúde da aplicação sem autenticação"""
    print("📍 Endpoint health acessado")
    return {
        "status": "healthy",
        "message": "Todos os sistemas funcionando normalmente",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/upload", response_model=dict)
async def upload_files(
    files: List[UploadFile] = File(...),
    token: str = Depends(verify_token)
):
    """Upload de múltiplos arquivos para triagem"""
    uploaded_files = []

    for file in files:
        if not file.filename:
            continue

        # Salvar arquivo temporariamente
        file_path = UPLOAD_DIR / file.filename
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        uploaded_files.append({
            "filename": file.filename,
            "size": len(content),
            "path": str(file_path)
        })

    return {
        "success": True,
        "message": f"{len(uploaded_files)} arquivos enviados com sucesso",
        "files": uploaded_files
    }


@app.post("/triagem", response_model=TriagemResponse)
async def executar_triagem(
    request: TriagemRequest,
    token: str = Depends(verify_token)
):
    """Executar triagem nos arquivos enviados"""
    try:
        # Listar arquivos no diretório de upload
        arquivos = list(UPLOAD_DIR.glob("*"))
        if not arquivos:
            raise HTTPException(
                status_code=400,
                detail="Nenhum arquivo encontrado para triagem"
            )

        total_processados = 0
        total_aprovados = 0
        aprovados_info = []

        # Processar cada arquivo
        for arquivo in arquivos:
            if arquivo.is_file():
                total_processados += 1

                # Extrair texto do arquivo
                with open(arquivo, "rb") as f:
                    data = f.read()

                texto, ocr_usado = extract_text_any(
                    arquivo.name,
                    "",
                    data
                )

                if not texto:
                    continue

                # Verificar critérios positivos
                palavras_positivas = ([request.vaga_descricao] +
                                      request.palavras_chave)
                pos_hit = any(
                    _has_exact_phrase(texto, palavra)
                    for palavra in palavras_positivas
                )

                # Verificar critérios negativos
                neg_hit = any(
                    _has_exact_phrase(texto, palavra)
                    for palavra in request.palavras_negativas
                ) if request.palavras_negativas else False

                # Verificar formações
                formacoes_encontradas = []
                if request.formacoes:
                    for formacao in request.formacoes:
                        if _has_exact_phrase(texto, formacao):
                            formacoes_encontradas.append(formacao)

                # Critério de aprovação
                aprovado = pos_hit and not neg_hit

                if aprovado:
                    total_aprovados += 1

                    # Mover para pasta de aprovados
                    arquivo_aprovado = APROVADOS_DIR / arquivo.name
                    arquivo.rename(arquivo_aprovado)

                    aprovados_info.append({
                        "arquivo": arquivo.name,
                        "formacoes_encontradas": formacoes_encontradas,
                        "tamanho_texto": len(texto),
                        "ocr_usado": ocr_usado
                    })

        # Limpar arquivos restantes
        for arquivo in UPLOAD_DIR.glob("*"):
            if arquivo.is_file():
                arquivo.unlink()

        percentual = (
            total_aprovados /
            total_processados *
            100) if total_processados > 0 else 0

        return TriagemResponse(
            success=True,
            message="Triagem concluída com sucesso",
            total_processados=total_processados,
            total_aprovados=total_aprovados,
            percentual_aprovacao=round(percentual, 2),
            arquivos_aprovados=aprovados_info
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante a triagem: {str(e)}"
        )


@app.get("/aprovados", response_model=dict)
async def listar_aprovados(token: str = Depends(verify_token)):
    """Listar arquivos aprovados"""
    arquivos = []

    for arquivo in APROVADOS_DIR.glob("*"):
        if arquivo.is_file():
            stat = arquivo.stat()
            data_mod = datetime.fromtimestamp(stat.st_mtime).isoformat()
            arquivos.append({
                "nome": arquivo.name,
                "tamanho": stat.st_size,
                "data_modificacao": data_mod
            })

    return {
        "success": True,
        "total": len(arquivos),
        "arquivos": arquivos
    }


@app.get("/aprovados/{filename}")
async def download_aprovado(
    filename: str,
    token: str = Depends(verify_token)
):
    """Download de arquivo aprovado"""
    arquivo_path = APROVADOS_DIR / filename

    if not arquivo_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado"
        )

    return FileResponse(
        path=arquivo_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.post("/triagem-email", response_model=TriagemResponse)
async def triagem_email_odq(
    request: TriagemEmailRequest,
    token: str = Depends(verify_token)
):
    """Triagem emails do domínio @odequadroservicos.com.br"""
    print("🚀 Iniciando triagem de emails...")
    print(f"📋 Vaga: {request.vaga_descricao}")
    print(f"🏷️ Palavras-chave: {request.palavras_chave}")
    print(f"📧 Max emails: {request.max_emails}")
    
    try:
        # Tentar carregar configuração do parameters.json primeiro
        config = {}
        config_loaded = False

        # Verificar no diretório atual e no pai
        for config_path in ["parameters.json", "../parameters.json"]:
            try:
                import json
                with open(config_path, "r") as f:
                    config = json.load(f)
                    print(f"Configuração carregada de {config_path}")
                    config_loaded = True
                    break
            except FileNotFoundError:
                continue

        if not config_loaded:
            print("parameters.json não encontrado, "
                  "usando apenas variáveis de ambiente")

        # Usar variáveis de ambiente se disponíveis,
        # senão usar config do arquivo
        client_id = os.getenv("CLIENT_ID") or config.get("client_id")
        client_secret = os.getenv("CLIENT_SECRET") or config.get("secret")
        authority = os.getenv("AUTHORITY") or config.get("authority")
        scope_env = os.getenv("SCOPE")
        if scope_env:
            scope = [scope_env]
        else:
            default_scope = ["https://graph.microsoft.com/.default"]
            scope = config.get("scope", default_scope)

        if not all([client_id, client_secret, authority]):
            return {"erro": "Configurações Microsoft Graph não encontradas"}

        # Obter token de autenticação
        auth_token = get_token_from_env(
            client_id, client_secret, authority, scope
        )

        if not auth_token:
            return {"erro": "Falha na autenticação Microsoft Graph"}

        print("🔍 PROCESSANDO EMAILS DO DOMÍNIO @odequadroservicos.com.br")
        print(f"📧 Máximo de emails por usuário: {request.max_emails}")

        # Lista para armazenar todos os emails de todo o domínio
        all_emails = []
        processed_users = []

        # Buscar lista de usuários do domínio @odequadroservicos.com.br
        users_endpoint = (
            "https://graph.microsoft.com/v1.0/users?"
            "$filter=endswith(userPrincipalName,'@odequadroservicos.com.br')"
            "&$top=100&$select=userPrincipalName,displayName"
        )

        headers = {"Authorization": f"Bearer {auth_token}"}

        # Buscar usuários do domínio
        import requests
        users_response = requests.get(users_endpoint, headers=headers)

        if users_response.status_code != 200:
            print(f"❌ Erro ao buscar usuários: {users_response.status_code}")
            return {
                "erro": f"Erro ao buscar usuários: "
                        f"{users_response.status_code}"
            }

        users_data = users_response.json()
        domain_users = users_data.get("value", [])

        print(f"👥 Encontrados {len(domain_users)} usuários no domínio")

        # Processar emails de cada usuário do domínio
        total_emails_found = 0

        for user in domain_users:
            user_email = user.get("userPrincipalName")
            display_name = user.get("displayName", "")

            if not user_email:
                continue

            print(f"📬 Processando: {display_name} ({user_email})")

            # Endpoint para emails deste usuário específico
            max_per_user = min(request.max_emails, 100)
            user_emails_endpoint = (
                f"https://graph.microsoft.com/v1.0/users/{user_email}"
                f"/messages?$top={max_per_user}"
            )

            try:
                user_emails_response = requests.get(
                    user_emails_endpoint, headers=headers
                )

                if user_emails_response.status_code == 200:
                    user_emails_data = user_emails_response.json()
                    user_emails = user_emails_data.get("value", [])

                    print(f"  ✅ {len(user_emails)} emails para {user_email}")

                    # Adicionar informação do usuário a cada email
                    for email in user_emails:
                        email["source_user"] = user_email
                        email["source_user_name"] = display_name

                    all_emails.extend(user_emails)
                    total_emails_found += len(user_emails)
                    processed_users.append({
                        "email": user_email,
                        "name": display_name,
                        "emails_count": len(user_emails)
                    })

                else:
                    status_code = user_emails_response.status_code
                    print(f"  ⚠️ Erro ao acessar emails de {user_email}: "
                          f"{status_code}")

            except Exception as e:
                print(f"  ❌ Erro ao processar {user_email}: {str(e)}")
                continue

        print(f"🎯 TOTAL DE EMAILS COLETADOS: {total_emails_found}")
        print(f"👥 USUÁRIOS PROCESSADOS: {len(processed_users)}")

        if not all_emails:
            return {
                "status": "nenhum_email_encontrado",
                "total_emails": 0,
                "usuarios_processados": len(processed_users),
                "detalhes_usuarios": processed_users
            }

        # Usar os emails já coletados de todo o domínio
        print(f"🔄 Processando triagem de {len(all_emails)} emails...")

        # Filtrar apenas emails com anexos
        emails_com_anexos = []
        for email in all_emails:
            if email.get("hasAttachments", False):
                emails_com_anexos.append(email)

        print(f"📎 Emails com anexos encontrados: {len(emails_com_anexos)}")

        if not emails_com_anexos:
            return TriagemResponse(
                success=True,
                message="Nenhum email com anexos encontrado no domínio",
                total_processados=0,
                total_aprovados=0,
                percentual_aprovacao=0.0,
                arquivos_aprovados=[],
                detalhes_usuarios=processed_users
            )

        total_anexos = 0
        total_aprovados = 0
        aprovados_info = []

        # Criar diretório temporário para anexos
        tmp_dir = Path(tempfile.mkdtemp(prefix="triagem_emails_"))

        # Processar emails
        for msg in emails_com_anexos[:request.max_emails]:
            msg_id = msg.get('id')
            if not msg.get('hasAttachments'):
                continue

            # Listar anexos do email - usar o email da origem
            user_email_source = msg.get("source_user")
            if not user_email_source:
                continue
            attachments = list_attachments(
                user_email_source, msg_id, auth_token
            )

            for att in attachments:
                if att.get('@odata.type') != '#microsoft.graph.fileAttachment':
                    continue

                # Baixar anexo
                fname, data, ctype = download_attachment(
                    user_email_source, msg_id, att['id'], auth_token
                )

                if not fname or not data:
                    continue

                total_anexos += 1

                # Salvar temporariamente
                safe_filename = safe_name(fname)
                temp_path = save_bytes(tmp_dir, safe_filename, data)

                # Extrair texto
                texto, ocr_usado = extract_text_any(
                    fname, ctype, data
                )

                if not texto:
                    continue

                # Aplicar critérios de triagem
                palavras_positivas = ([request.vaga_descricao] +
                                      request.palavras_chave)

                # Usar a função completa de candidato aprovado
                aprovado, formacoes_encontradas = candidato_aprovado(
                    texto,
                    palavras_positivas,
                    request.formacoes
                )

                # Verificar palavras negativas
                neg_hit = any(
                    _has_exact_phrase(texto, palavra)
                    for palavra in request.palavras_negativas
                ) if request.palavras_negativas else False

                # Decisão final
                if aprovado and not neg_hit:
                    total_aprovados += 1

                    # Mover para pasta de aprovados
                    arquivo_aprovado = APROVADOS_DIR / safe_filename
                    temp_path.rename(arquivo_aprovado)

                    aprovados_info.append({
                        "arquivo": safe_filename,
                        "email_assunto": msg.get('subject', 'Sem assunto'),
                        "email_data": msg.get('receivedDateTime', ''),
                        "email_origem": user_email_source,
                        "formacoes_encontradas": list(formacoes_encontradas),
                        "tamanho_texto": len(texto),
                        "ocr_usado": ocr_usado
                    })
                else:
                    # Remover arquivo não aprovado
                    temp_path.unlink(missing_ok=True)

        # Limpar diretório temporário
        shutil.rmtree(tmp_dir, ignore_errors=True)

        percentual = (
            total_aprovados /
            total_anexos *
            100) if total_anexos > 0 else 0

        return TriagemResponse(
            success=True,
            message=(f"Triagem de emails concluída: "
                     f"{len(emails_com_anexos)} emails processados"),
            total_processados=total_anexos,
            total_aprovados=total_aprovados,
            percentual_aprovacao=round(percentual, 2),
            arquivos_aprovados=aprovados_info,
            detalhes_usuarios=processed_users
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante triagem de emails: {str(e)}"
        )


@app.delete("/limpar")
async def limpar_diretorios(token: str = Depends(verify_token)):
    """Limpar diretórios de upload e aprovados"""
    # Limpar uploads
    for arquivo in UPLOAD_DIR.glob("*"):
        if arquivo.is_file():
            arquivo.unlink()

    # Limpar aprovados
    for arquivo in APROVADOS_DIR.glob("*"):
        if arquivo.is_file():
            arquivo.unlink()

    return {
        "success": True,
        "message": "Diretórios limpos com sucesso"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Voltar para porta 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Desabilitar reload para debug
    )
