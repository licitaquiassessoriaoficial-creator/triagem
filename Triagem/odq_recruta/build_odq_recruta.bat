@echo off
REM Script para gerar o executável ODQ_Recruta
pip install pyinstaller
pyinstaller --onefile --windowed --name "ODQ_Recruta" app.py

REM Copiar .env e pasta odq_recruta para dist
xcopy .env dist /Y
xcopy odq_recruta dist\odq_recruta /E /I /Y

echo Build finalizado! O executável está em dist\ODQ_Recruta.exe
pause
