# Configuração de Ambiente para Sistema de Triagem ODQ

## Variáveis de Ambiente Necessárias

### Para Microsoft Graph API (Office 365):
```bash
# Windows (PowerShell)
$env:AZURE_CLIENT_ID="seu-client-id-aqui"
$env:AZURE_CLIENT_SECRET="seu-client-secret-aqui" 
$env:AZURE_TENANT_ID="seu-tenant-id-aqui"

# Linux/Mac
export AZURE_CLIENT_ID="seu-client-id-aqui"
export AZURE_CLIENT_SECRET="seu-client-secret-aqui"
export AZURE_TENANT_ID="seu-tenant-id-aqui"
```

### Para Banco de Dados PostgreSQL:
```bash
# Windows (PowerShell)
$env:DATABASE_URL="postgresql://user:password@localhost:5432/triagem_odq"

# Linux/Mac  
export DATABASE_URL="postgresql://user:password@localhost:5432/triagem_odq"
```

### Para Gmail IMAP:
```bash
# Windows (PowerShell)
$env:GMAIL_USER="seu-email@gmail.com"
$env:GMAIL_PASSWORD="sua-senha-de-app"

# Linux/Mac
export GMAIL_USER="seu-email@gmail.com" 
export GMAIL_PASSWORD="sua-senha-de-app"
```

## Como Configurar:

1. **Copie o arquivo `.env.example` para `.env`**
2. **Preencha suas credenciais reais no arquivo `.env`**
3. **O arquivo `.env` será ignorado pelo Git (já está no .gitignore)**

## Segurança:
- ✅ Credenciais ficam em variáveis de ambiente
- ✅ Arquivo `.env` não vai para o GitHub
- ✅ Sistema funciona normalmente
- ✅ Deploy seguro garantido