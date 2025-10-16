@echo off
echo ========================================
echo    ODQ Recruta - Triagem de Curriculos
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.10+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se arquivo .env existe
if not exist ".env" (
    echo AVISO: Arquivo .env nao encontrado!
    echo Copiando env_example.txt para .env...
    copy "env_example.txt" ".env" >nul 2>&1
    if errorlevel 1 (
        echo ERRO: Nao foi possivel criar o arquivo .env
        pause
        exit /b 1
    )
    echo IMPORTANTE: Configure suas credenciais no arquivo .env antes de continuar!
    echo.
    pause
)

REM Executar o aplicativo
echo Iniciando ODQ Recruta...
python app.py

REM Se houver erro, pausar para mostrar a mensagem
if errorlevel 1 (
    echo.
    echo ERRO: O aplicativo falhou!
    pause
)



