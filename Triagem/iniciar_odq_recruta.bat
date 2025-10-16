@echo off
title ODQ Recruta - Sistema de Triagem
color 0B
cls

echo ========================================
echo    ODQ Recruta - Sistema de Triagem
echo ========================================
echo.

REM Mudar para o diretório do script
cd /d "%~dp0"

REM Verificar se Python está instalado
echo [INFO] Verificando instalacao do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.10+ antes de continuar.
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verificar se o ambiente virtual existe
if not exist ".venv" (
    echo [AVISO] Ambiente virtual nao encontrado!
    echo [INFO] Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo [INFO] Ambiente virtual criado com sucesso!
    echo.
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Verificar e instalar dependências se necessário
echo [INFO] Verificando dependencias...
pip show msal >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando dependencias do sistema principal...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias principais!
        pause
        exit /b 1
    )
)

REM Instalar dependências específicas do ODQ Recruta
echo [INFO] Verificando dependencias do ODQ Recruta...
cd odq_recruta
pip show python-dotenv >nul 2>&1
if errorlevel 1 (
    echo [INFO] Instalando dependencias do ODQ Recruta...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias do ODQ Recruta!
        pause
        exit /b 1
    )
)

REM Verificar arquivo .env
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    if exist "env_example.txt" (
        echo [INFO] Copiando env_example.txt para .env...
        copy "env_example.txt" ".env" >nul 2>&1
        echo.
        echo [IMPORTANTE] Configure suas credenciais no arquivo .env antes de continuar!
        echo Pressione qualquer tecla apos configurar...
        pause
    ) else (
        echo [ERRO] Arquivo env_example.txt nao encontrado!
        echo Crie um arquivo .env com as configuracoes necessarias.
        pause
        exit /b 1
    )
)

REM Verificar se o arquivo existe
if not exist "app.py" (
    echo [ERRO] Arquivo app.py nao encontrado!
    pause
    exit /b 1
)

echo [INFO] Iniciando ODQ Recruta...
echo.
python app.py

REM Se houver erro, pausar para mostrar a mensagem
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o ODQ Recruta!
    pause
)

cd ..