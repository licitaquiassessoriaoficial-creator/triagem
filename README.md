# Triagem de Currículos - Microsoft 365

Sistema de triagem automatizada de currículos através de emails do Microsoft 365.

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8+
- Conta Microsoft 365 configurada
- Dependências instaladas: `pip install -r requirements.txt`

### Configuração
1. Configure o arquivo `parameters.json` com suas credenciais do Azure AD
2. Configure o arquivo `.env` com seu email (use `.env.example` como base)

### Execução
Execute a interface gráfica:
```bash
python triagem_gui.py
```

## 📋 Funcionalidades
- ✅ Conexão com Microsoft 365 via Graph API
- ✅ Busca automatizada de emails com anexos
- ✅ Extração de texto de PDFs e DOCs
- ✅ Filtros por palavras-chave e formação
- ✅ Filtros por data
- ✅ Interface gráfica intuitiva
- ✅ Pasta automática para aprovados

## 📁 Estrutura
- `triagem_gui.py` - Interface principal
- `confidential_client_secret_sample.py` - Motor de triagem
- `parameters.json` - Configurações do Azure AD
- `.env` - Variáveis de ambiente
- `aprovados/` - Pasta com currículos aprovados

## 🔧 Configuração Segura
Consulte `CONFIGURACAO_SEGURA.md` para instruções detalhadas de configuração.