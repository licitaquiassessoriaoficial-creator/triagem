#!/bin/bash

# Script para configurar URL da API após deploy
# Usage: ./configure-api.sh https://sua-url-railway.railway.app

if [ -z "$1" ]; then
    echo "❌ Erro: URL da API não fornecida"
    echo "📖 Uso: ./configure-api.sh https://sua-url-railway.railway.app"
    exit 1
fi

API_URL=$1
SCRIPT_FILE="frontend/script.js"

echo "🔧 Configurando URL da API..."
echo "📡 URL: $API_URL"

# Fazer backup
cp "$SCRIPT_FILE" "$SCRIPT_FILE.backup"

# Substituir URL
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|const API_BASE_URL = '.*';|const API_BASE_URL = '$API_URL';|g" "$SCRIPT_FILE"
else
    # Linux/Windows
    sed -i "s|const API_BASE_URL = '.*';|const API_BASE_URL = '$API_URL';|g" "$SCRIPT_FILE"
fi

echo "✅ URL da API configurada com sucesso!"
echo "🔍 Verifique o arquivo: $SCRIPT_FILE"
echo ""
echo "📋 Próximos passos:"
echo "1. Faça commit das alterações"
echo "2. Push para o repositório"
echo "3. Netlify fará deploy automático"