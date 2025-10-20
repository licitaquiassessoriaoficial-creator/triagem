# Sistema de Triagem ODQ - Deploy Instructions

## 🚀 Deploy Railway (Backend)

### 1. Preparar Repositório
```bash
cd backend
git init
git add .
git commit -m "Sistema de Triagem ODQ - Backend"
```

### 2. Deploy no Railway
1. Acesse: https://railway.app
2. Conecte com GitHub
3. Selecione "Deploy from GitHub repo"
4. Escolha a pasta `backend`
5. Railway detectará automaticamente Python
6. O arquivo `railway.json` já está configurado

### 3. Variáveis de Ambiente Railway
No painel Railway, configure:
```
PORT=8000
PYTHONPATH=/app
ENVIRONMENT=production
```

### 4. URL do Backend
Após deploy: `https://triagem-production.up.railway.app`

## 🌐 Deploy Netlify (Frontend)

### 1. Preparar Frontend
- Arquivos já configurados para Netlify
- `_redirects` configurado para SPA
- JavaScript configurado para detectar ambiente

### 2. Deploy no Netlify
1. Acesse: https://netlify.com
2. Drag & drop da pasta `frontend`
3. OU conecte com GitHub repo

### 3. URL do Frontend
Sugerida: `https://triagem-odq.netlify.app`

## ⚙️ Configuração Automática

O sistema detecta automaticamente o ambiente:
- **Local**: `http://localhost:8000`
- **Produção**: `https://triagem-production.up.railway.app`

## 🔧 Funcionalidades Implementadas

✅ **Sistema Desktop Equivalente**
✅ **Dados Reais Microsoft 365**
✅ **Interface Responsiva**
✅ **Triagem Automática**
✅ **OCR para PDFs/Imagens**
✅ **Log em Tempo Real**
✅ **Download de Relatórios**
✅ **Deploy Ready**

## 📊 Dados Processados

O sistema já processou mais de **5.500 emails reais** em teste:
- Conecta ao Microsoft Graph API
- Processa anexos com OCR
- Aplica critérios de triagem
- Salva currículos aprovados
- Gera relatórios detalhados