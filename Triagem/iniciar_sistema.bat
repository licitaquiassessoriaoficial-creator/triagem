@echo off
title Sistema de Triagem ODQ
color 0A
cls

echo ========================================
echo    Sistema de Triagem ODQ - v1.1
echo    [NOVO] Filtra apenas emails nao lidos
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
    echo [INFO] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Menu de escolha
:MENU
cls
echo ========================================
echo    Sistema de Triagem ODQ - v1.1
echo    [NOVO] Filtra apenas emails nao lidos
echo ========================================
echo.
echo Escolha o modulo para executar:
echo.
echo [1] Triagem GUI (Microsoft 365) - EMAILS NAO LIDOS
echo [2] ODQ Recruta (Sistema Principal)
echo [3] Sair
echo.
set /p choice="Digite sua opcao (1-3): "

if "%choice%"=="1" goto TRIAGEM_GUI
if "%choice%"=="2" goto ODQ_RECRUTA
if "%choice%"=="3" goto EXIT
echo [ERRO] Opcao invalida! Tente novamente.
timeout /t 2 >nul
goto MENU

:TRIAGEM_GUI
cls
echo ========================================
echo    Iniciando Triagem GUI...
echo    Processando apenas EMAILS NAO LIDOS
echo ========================================
echo.
if not exist "graph-app-python\triagem_gui.py" (
    echo [ERRO] Arquivo triagem_gui.py nao encontrado!
    pause
    goto MENU
)
echo [INFO] Executando Triagem GUI...
python graph-app-python\triagem_gui.py
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o Triagem GUI!
    pause
)
goto MENU

:ODQ_RECRUTA
cls
echo ========================================
echo    Iniciando ODQ Recruta...
echo ========================================
echo.
if not exist "odq_recruta\app.py" (
    echo [ERRO] Arquivo app.py nao encontrado!
    pause
    goto MENU
)

REM Verificar arquivo .env para ODQ Recruta
cd odq_recruta
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    if exist "env_example.txt" (
        echo [INFO] Copiando env_example.txt para .env...
        copy "env_example.txt" ".env" >nul 2>&1
        echo [IMPORTANTE] Configure suas credenciais no arquivo .env!
        echo.
        pause
    ) else (
        echo [ERRO] Arquivo env_example.txt nao encontrado!
        pause
        cd ..
        goto MENU
    )
)

echo [INFO] Executando ODQ Recruta...
python app.py
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o ODQ Recruta!
    pause
)
cd ..
goto MENU

:EXIT
echo.
echo [INFO] Encerrando sistema...
timeout /t 1 >nul
exit /b 0