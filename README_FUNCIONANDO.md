# Sistema de Triagem ODQ - Funcionando ✅

## Status Atual

- ✅ **Frontend**: Funcionando perfeitamente
- ✅ **Sistema de Triagem**: Modo simulação ativo
- ✅ **Interface**: Totalmente funcional
- ⚠️ **Backend**: Em modo simulação (demonstração)

## Como Usar o Sistema

### Opção 1: Execução Automática (Recomendada)

1. Execute o arquivo `iniciar_sistema.bat`
2. O sistema abrirá automaticamente no navegador
3. Acesse: <http://localhost:3000>

### Opção 2: Execução Manual

1. Abra o PowerShell no diretório do projeto
2. Execute:

   ```powershell
   cd frontend
   python -m http.server 3000
   ```

3. Abra <http://localhost:3000> no navegador

## Funcionalidades Disponíveis

### ✅ Triagem de Currículos (Simulação)

- Preencha os campos do formulário:
  - **Descrição da Vaga**: Ex: "Desenvolvedor Python"
  - **Palavras-chave**: Ex: "Python, Desenvolvimento, Software"
  - **Formações**: Ex: "Engenharia, Ciência da Computação"
  - **Palavras Negativas**: Ex: "Estagiário, Trainee"
- Clique em "Executar Triagem"
- O sistema simulará:
  - Conexão com Microsoft Graph
  - Processamento de emails
  - Análise de currículos com OCR
  - Aplicação de critérios de triagem
  - Geração de relatório de aprovados

### ✅ Logs em Tempo Real

- Acompanhe todo o processo na seção "Log de Execução"
- Logs detalhados de cada etapa
- Indicadores visuais de progresso

### ✅ Resultados Detalhados

- Lista de currículos aprovados
- Formações encontradas
- Taxa de aprovação
- Informações dos candidatos

## Arquivos Importantes

```text
triagem/
├── iniciar_sistema.bat          # Script de inicialização
├── frontend/
│   ├── index.html              # Interface principal
│   ├── script.js               # Lógica da aplicação
│   └── styles.css              # Estilos
├── backend/
│   ├── main.py                 # Servidor principal
│   └── requirements.txt        # Dependências
├── confidential_client_secret_sample.py  # Sistema de triagem
├── parameters.json             # Configurações Microsoft Graph
└── aprovados/                  # Diretório de currículos aprovados
```

## Configuração Real (Produção)

Para usar o sistema com dados reais do Microsoft Graph:

1. Configure as credenciais no `parameters.json`:

   ```json
   {
     "client_id": "seu-client-id",
     "authority": "https://login.microsoftonline.com/seu-tenant-id",
     "secret": "seu-client-secret",
     "scope": ["https://graph.microsoft.com/.default"]
   }
   ```

2. Execute o backend real:

   ```powershell
   cd backend
   python main.py
   ```

## Modo de Funcionamento

### Modo Simulação (Atual)

- ✅ Demonstra todas as funcionalidades
- ✅ Interface totalmente funcional
- ✅ Resultados simulados realistas
- ✅ Não requer configuração Microsoft Graph

### Modo Produção

- 🔗 Conecta ao Microsoft Graph real
- 📧 Processa emails reais do domínio
- 📄 Analisa currículos reais com OCR
- 💾 Salva aprovados em arquivos

## Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, FastAPI, Uvicorn
- **Triagem**: PyPDF2, python-docx, Tesseract OCR
- **Microsoft Graph**: MSAL, Requests
- **Servidor**: HTTP Server (Python)

## Demonstração das Funcionalidades

O sistema atual demonstra:

1. **Interface Profissional**: Design limpo e intuitivo
2. **Formulário Completo**: Todos os campos necessários
3. **Validação**: Verificação de dados de entrada
4. **Processamento Visual**: Barra de progresso e logs
5. **Resultados Detalhados**: Relatório completo
6. **Responsividade**: Funciona em diferentes tamanhos de tela

## Próximos Passos

Para ativar o modo produção:

1. Configurar credenciais Microsoft Graph
2. Testar conexão com emails reais
3. Validar OCR com documentos reais
4. Deploy em servidor de produção

---

**Sistema de Triagem ODQ** - Versão 2.0  
© 2024 ODQ Sistemas - Funcionando ✅