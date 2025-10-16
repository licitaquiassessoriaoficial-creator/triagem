#!/bin/bash

# 🚀 Script de Setup Automatizado - Sistema de Triagem ODQ Web

set -e

echo "🚀 Iniciando setup do Sistema de Triagem ODQ Web..."
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está no diretório correto
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    log_error "Execute este script no diretório triagem-web/"
    exit 1
fi

log_info "Verificando pré-requisitos..."

# Verificar Node.js
if ! command -v node &> /dev/null; then
    log_error "Node.js não encontrado. Instale Node.js 18+ antes de continuar."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    log_error "Node.js versão 18+ é necessária. Versão atual: $(node -v)"
    exit 1
fi

log_success "Node.js $(node -v) encontrado"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 não encontrado. Instale Python 3.9+ antes de continuar."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
log_success "Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    log_error "pip3 não encontrado. Instale pip antes de continuar."
    exit 1
fi

log_success "pip3 encontrado"

echo ""
echo "🛠️  Configurando Backend..."
echo "=========================="

cd backend

# Criar ambiente virtual
log_info "Criando ambiente virtual Python..."
python3 -m venv venv

# Ativar ambiente virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    log_success "Ambiente virtual ativado (Linux/Mac)"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    log_success "Ambiente virtual ativado (Windows)"
else
    log_error "Não foi possível ativar o ambiente virtual"
    exit 1
fi

# Instalar dependências
log_info "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

log_success "Dependências Python instaladas"

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    log_info "Criando arquivo .env..."
    cat > .env << EOL
# Configurações de desenvolvimento
ENVIRONMENT=development
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Banco de dados local (substitua pela URL do Railway em produção)
DATABASE_URL=postgresql://postgres:password@localhost:5432/triagem_odq

# Gmail (opcional - preencha se necessário)
GMAIL_USERNAME=
GMAIL_APP_PASSWORD=

# Microsoft 365 (opcional - preencha se necessário)
MS_CLIENT_ID=
MS_CLIENT_SECRET=
MS_TENANT_ID=
MS_REDIRECT_URI=http://localhost:8000/auth/callback

# Configurações de upload
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=pdf,doc,docx,txt

# Redis (opcional)
REDIS_URL=redis://localhost:6379

# Debug
DB_ECHO=false
EOL
    log_success "Arquivo .env criado. EDITE o arquivo com suas configurações!"
    log_warning "Abra backend/.env e configure suas credenciais antes de continuar"
else
    log_info "Arquivo .env já existe"
fi

cd ..

echo ""
echo "🌐 Configurando Frontend..."
echo "=========================="

cd frontend

# Instalar dependências
log_info "Instalando dependências Node.js..."
npm install

log_success "Dependências Node.js instaladas"

# Criar arquivo .env.local se não existir
if [ ! -f ".env.local" ]; then
    log_info "Criando arquivo .env.local..."
    cat > .env.local << EOL
# Configurações de desenvolvimento
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_APP_NAME=Sistema de Triagem ODQ
NEXT_PUBLIC_ENVIRONMENT=development
EOL
    log_success "Arquivo .env.local criado"
else
    log_info "Arquivo .env.local já existe"
fi

cd ..

echo ""
echo "✅ Setup Concluído!"
echo "=================="

log_success "Backend configurado em: ./backend/"
log_success "Frontend configurado em: ./frontend/"

echo ""
echo "🚀 Próximos Passos:"
echo "==================="
echo "1. Configure suas credenciais em backend/.env"
echo "2. Configure um banco PostgreSQL (local ou Railway)"
echo "3. Execute os comandos abaixo para iniciar:"
echo ""
echo "   # Terminal 1 - Backend"
echo "   cd backend"
echo "   source venv/bin/activate  # ou venv\\Scripts\\activate no Windows"
echo "   uvicorn main:app --reload"
echo ""
echo "   # Terminal 2 - Frontend"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Acesse http://localhost:3000 no navegador"
echo ""

echo "📚 Para deploy em produção:"
echo "============================"
echo "• Backend: Siga instruções em README.md seção 'Deploy do Backend (Railway)'"
echo "• Frontend: Siga instruções em README.md seção 'Deploy do Frontend (Netlify)'"
echo ""

log_success "Setup automatizado concluído! 🎉"