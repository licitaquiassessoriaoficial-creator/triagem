# 🚀 Script de Setup Automatizado - Sistema de Triagem ODQ Web (Windows)

param(
    [switch]$SkipChecks = $false
)

Write-Host "🚀 Iniciando setup do Sistema de Triagem ODQ Web..." -ForegroundColor Blue
Write-Host "==================================================" -ForegroundColor Blue
Write-Host ""

# Funções auxiliares
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)  
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Verificar se está no diretório correto
if (-not (Test-Path "README.md") -or -not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Error "Execute este script no diretório triagem-web\"
    exit 1
}

if (-not $SkipChecks) {
    Write-Info "Verificando pré-requisitos..."

    # Verificar Node.js
    try {
        $nodeVersion = node --version
        Write-Success "Node.js $nodeVersion encontrado"
    }
    catch {
        Write-Error "Node.js não encontrado. Instale Node.js 18+ antes de continuar."
        Write-Host "Download: https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }

    # Verificar Python
    try {
        $pythonVersion = python --version
        Write-Success "$pythonVersion encontrado"
    }
    catch {
        Write-Error "Python não encontrado. Instale Python 3.9+ antes de continuar."
        Write-Host "Download: https://python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }

    # Verificar pip
    try {
        pip --version | Out-Null
        Write-Success "pip encontrado"
    }
    catch {
        Write-Error "pip não encontrado. Reinstale Python com pip incluído."
        exit 1
    }
}

Write-Host ""
Write-Host "🛠️  Configurando Backend..." -ForegroundColor Blue  
Write-Host "==========================" -ForegroundColor Blue

Set-Location backend

# Criar ambiente virtual
Write-Info "Criando ambiente virtual Python..."
python -m venv venv

# Ativar ambiente virtual
Write-Info "Ativando ambiente virtual..."
if (Test-Path "venv\Scripts\activate.ps1") {
    & "venv\Scripts\activate.ps1"
    Write-Success "Ambiente virtual ativado"
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1" 
    Write-Success "Ambiente virtual ativado"
} else {
    Write-Error "Não foi possível ativar o ambiente virtual"
    exit 1
}

# Instalar dependências
Write-Info "Instalando dependências Python..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Success "Dependências Python instaladas"

# Criar arquivo .env se não existir
if (-not (Test-Path ".env")) {
    Write-Info "Criando arquivo .env..."
    
    # Gerar chave secreta
    $secretKey = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString()))
    
    $envContent = @"
# Configurações de desenvolvimento
ENVIRONMENT=development
SECRET_KEY=$secretKey
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
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-Success "Arquivo .env criado. EDITE o arquivo com suas configurações!"
    Write-Warning "Abra backend\.env e configure suas credenciais antes de continuar"
} else {
    Write-Info "Arquivo .env já existe"
}

Set-Location ..

Write-Host ""
Write-Host "🌐 Configurando Frontend..." -ForegroundColor Blue
Write-Host "==========================" -ForegroundColor Blue

Set-Location frontend

# Instalar dependências
Write-Info "Instalando dependências Node.js..."
npm install

Write-Success "Dependências Node.js instaladas"

# Criar arquivo .env.local se não existir
if (-not (Test-Path ".env.local")) {
    Write-Info "Criando arquivo .env.local..."
    
    $envLocalContent = @"
# Configurações de desenvolvimento
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_APP_NAME=Sistema de Triagem ODQ
NEXT_PUBLIC_ENVIRONMENT=development
"@
    
    $envLocalContent | Out-File -FilePath ".env.local" -Encoding UTF8
    Write-Success "Arquivo .env.local criado"
} else {
    Write-Info "Arquivo .env.local já existe"
}

Set-Location ..

Write-Host ""
Write-Host "✅ Setup Concluído!" -ForegroundColor Green
Write-Host "==================" -ForegroundColor Green

Write-Success "Backend configurado em: .\backend\"
Write-Success "Frontend configurado em: .\frontend\"

Write-Host ""
Write-Host "🚀 Próximos Passos:" -ForegroundColor Blue
Write-Host "==================="
Write-Host "1. Configure suas credenciais em backend\.env"
Write-Host "2. Configure um banco PostgreSQL (local ou Railway)"
Write-Host "3. Execute os comandos abaixo para iniciar:"
Write-Host ""
Write-Host "   # Terminal 1 - Backend (PowerShell)" -ForegroundColor Yellow
Write-Host "   cd backend"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   uvicorn main:app --reload"
Write-Host ""
Write-Host "   # Terminal 2 - Frontend" -ForegroundColor Yellow
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "4. Acesse http://localhost:3000 no navegador"
Write-Host ""

Write-Host "📚 Para deploy em produção:" -ForegroundColor Blue
Write-Host "============================"
Write-Host "• Backend: Siga instruções em README.md seção 'Deploy do Backend (Railway)'"
Write-Host "• Frontend: Siga instruções em README.md seção 'Deploy do Frontend (Netlify)'"
Write-Host ""

Write-Success "Setup automatizado concluído! 🎉"

# Perguntar se quer abrir os arquivos de configuração
$openConfigs = Read-Host "Deseja abrir os arquivos de configuração agora? (y/N)"
if ($openConfigs -eq "y" -or $openConfigs -eq "Y") {
    if (Test-Path "backend\.env") {
        notepad "backend\.env"
    }
    if (Test-Path "frontend\.env.local") {
        notepad "frontend\.env.local"
    }
}