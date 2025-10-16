# 🚀 Sistema de Triagem ODQ - Deploy Web

## 📋 Visão Geral

Sistema completo de triagem de currículos modernizado para deploy em nuvem:

- **Frontend**: Next.js + TypeScript → Netlify
- **Backend**: FastAPI + Python → Railway  
- **Banco**: PostgreSQL → Railway
- **Cache**: Redis → Railway (opcional)

## 🏗️ Arquitetura do Sistema

```mermaid
graph TB
    A[Usuário] --> B[Frontend Next.js - Netlify]
    B --> C[API FastAPI - Railway]
    C --> D[PostgreSQL - Railway]
    C --> E[Redis Cache - Railway]
    C --> F[Gmail API]
    C --> G[Microsoft 365 API]
    
    H[WebSocket] --> B
    C --> H
```

## 📁 Estrutura do Projeto

```
triagem-web/
├── backend/                 # API FastAPI
│   ├── main.py             # Aplicação principal
│   ├── models.py           # Modelos SQLAlchemy
│   ├── schemas.py          # Schemas Pydantic
│   ├── database.py         # Configuração DB
│   ├── requirements.txt    # Dependências Python
│   ├── Dockerfile         # Container para Railway
│   ├── railway.toml       # Config Railway
│   └── services/          # Serviços da aplicação
│       ├── triagem_service.py
│       ├── email_service.py
│       ├── auth_service.py
│       └── scoring_service.py
│
└── frontend/               # Interface Next.js
    ├── src/
    │   ├── pages/         # Páginas da aplicação
    │   ├── components/    # Componentes React
    │   ├── hooks/         # Custom hooks
    │   └── services/      # Serviços API
    ├── package.json       # Dependências Node
    ├── next.config.js     # Config Next.js
    ├── tailwind.config.js # Config Tailwind
    └── netlify.toml       # Config Netlify
```

## 🚀 Deploy do Backend (Railway)

### 1. Preparar o Projeto

```bash
cd triagem-web/backend
```

### 2. Configurar Railway

1. Acesse [railway.app](https://railway.app)
2. Conecte sua conta GitHub
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório do projeto
5. Configure o diretório raiz: `triagem-web/backend`

### 3. Adicionar PostgreSQL

1. No dashboard do Railway, clique em "New"
2. Selecione "Database" → "PostgreSQL"
3. O Railway criará automaticamente a variável `DATABASE_URL`

### 4. Configurar Variáveis de Ambiente

No Railway, adicione estas variáveis:

```env
# Banco de dados (criado automaticamente)
DATABASE_URL=postgresql://user:pass@host:port/db

# Configurações da aplicação
ENVIRONMENT=production
SECRET_KEY=sua-chave-secreta-super-forte-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Gmail (opcional)
GMAIL_USERNAME=seu-email@gmail.com
GMAIL_APP_PASSWORD=sua-senha-de-app

# Microsoft 365 (opcional)
MS_CLIENT_ID=seu-client-id
MS_CLIENT_SECRET=seu-client-secret
MS_TENANT_ID=seu-tenant-id
MS_REDIRECT_URI=https://seu-dominio.railway.app/auth/callback

# Configurações de upload/storage
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=pdf,doc,docx,txt

# Redis (opcional - para performance)
REDIS_URL=redis://localhost:6379
```

### 5. Deploy Automático

O Railway detectará o `Dockerfile` e fará o deploy automaticamente.

### 6. Configurar Domínio

1. No dashboard, vá em "Settings" → "Domains"
2. Clique em "Generate Domain" para obter URL gratuita
3. Ou configure domínio customizado

## 🌐 Deploy do Frontend (Netlify)

### 1. Preparar o Projeto

```bash
cd triagem-web/frontend
npm install
```

### 2. Configurar Netlify

1. Acesse [netlify.com](https://netlify.com)
2. Conecte sua conta GitHub
3. Clique em "New site from Git"
4. Selecione o repositório
5. Configure:
   - **Base directory**: `triagem-web/frontend`
   - **Build command**: `npm run build && npm run export`
   - **Publish directory**: `out`

### 3. Configurar Variáveis de Ambiente

No Netlify, adicione estas variáveis em "Site settings" → "Environment variables":

```env
# URL da API (substitua pela URL do Railway)
NEXT_PUBLIC_API_URL=https://seu-projeto.railway.app
NEXT_PUBLIC_WS_URL=wss://seu-projeto.railway.app/ws

# Configurações opcionais
NEXT_PUBLIC_APP_NAME=Sistema de Triagem ODQ
NEXT_PUBLIC_ENVIRONMENT=production
```

### 4. Deploy Automático

O Netlify fará deploy automático a cada push no GitHub.

### 5. Configurar Domínio

1. Em "Site settings" → "Domain management"
2. Configure domínio customizado se necessário
3. Netlify fornece HTTPS automático

## 🔧 Configuração Local para Desenvolvimento

### Backend Local

```bash
# Navegar para backend
cd triagem-web/backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis (criar .env)
cp .env.example .env
# Editar .env com suas configurações

# Executar migrações
alembic upgrade head

# Iniciar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Local

```bash
# Navegar para frontend
cd triagem-web/frontend

# Instalar dependências
npm install

# Configurar variáveis (criar .env.local)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws" >> .env.local

# Iniciar desenvolvimento
npm run dev
```

## 📊 Monitoramento e Logs

### Railway (Backend)

- **Logs**: Disponíveis no dashboard do Railway
- **Métricas**: CPU, RAM, latência automáticas
- **Alerts**: Configurar notificações por email

### Netlify (Frontend)

- **Deploy logs**: Histórico de builds
- **Analytics**: Tráfego e performance
- **Forms**: Captura de contatos (se necessário)

## 🔒 Segurança

### Configurações Implementadas

✅ **CORS configurado** para permitir apenas domínios específicos  
✅ **Headers de segurança** (XSS, CSRF, etc.)  
✅ **Autenticação JWT** com refresh tokens  
✅ **Validação de entrada** com Pydantic  
✅ **Sanitização de dados** antes do banco  
✅ **Rate limiting** para prevenir abuso  

### Configurações Adicionais Recomendadas

- **Firewall**: Configurar no Railway se necessário
- **Backup**: Backup automático do PostgreSQL
- **SSL**: Incluído automaticamente no Railway/Netlify
- **Secrets**: Usar Railway/Netlify secrets para credenciais

## 📈 Performance e Escalabilidade

### Otimizações Implementadas

- **Cache Redis** para emails processados
- **Processamento assíncrono** com background tasks
- **Paginação** em todas as listagens
- **Lazy loading** no frontend
- **CDN** automático do Netlify

### Monitoramento

```python
# Métricas disponíveis via /metrics endpoint
from prometheus_client import Counter, Histogram

email_processed = Counter('emails_processed_total')
response_time = Histogram('response_time_seconds')
```

## 🎯 Próximos Passos

### Imediatos
1. ✅ Fazer deploy do backend no Railway
2. ✅ Fazer deploy do frontend no Netlify
3. ✅ Configurar variáveis de ambiente
4. ✅ Testar conexão entre frontend/backend

### Curto Prazo (1-2 semanas)
- [ ] Implementar autenticação completa
- [ ] Adicionar testes automatizados
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Implementar sistema de logs estruturados

### Médio Prazo (1 mês)
- [ ] Adicionar Redis para cache
- [ ] Implementar notificações por email
- [ ] Dashboard de métricas avançado
- [ ] Sistema de backup automático

## 🆘 Troubleshooting

### Problemas Comuns

**1. Backend não inicia**
```bash
# Verificar logs no Railway
railway logs

# Verificar variáveis de ambiente
railway variables
```

**2. Frontend não conecta na API**
```bash
# Verificar URL da API
echo $NEXT_PUBLIC_API_URL

# Testar conexão
curl https://sua-api.railway.app/health
```

**3. Banco não conecta**
```bash
# Verificar DATABASE_URL
railway run python -c "import os; print(os.getenv('DATABASE_URL'))"
```

**4. Build falha**
```bash
# Limpar cache e rebuildar
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 📞 Suporte

Para dúvidas ou problemas:

1. **Documentação**: Consulte este arquivo
2. **Logs**: Verifique logs no Railway/Netlify
3. **Issues**: Criar issue no repositório GitHub
4. **Email**: Contatar equipe de desenvolvimento

---

**Sistema de Triagem ODQ v2.0** - Modernizado para a nuvem! 🚀