# Sistema de Triagem ODQ - Guia de Execução

## ✨ NOVA FUNCIONALIDADE: Filtro de Emails Não Lidos

O sistema agora processa **apenas emails não lidos**, melhorando significativamente a performance!

## Arquivos de Inicialização

O sistema possui diferentes arquivos .bat para inicializar os módulos:

### 🚀 iniciar_sistema.bat (RECOMENDADO)

Arquivo principal com menu interativo - v1.1

- Permite escolher entre os dois módulos disponíveis
- Verificação automática de dependências
- Interface amigável com menu
- Detecção e correção automática de problemas
- **NOVO:** Processa apenas emails não lidos

### 📋 Triagem GUI (Microsoft 365)

Módulo de triagem com filtro de emails não lidos

- Interface gráfica para triagem de currículos
- Integração com Microsoft 365
- Arquivo: `graph-app-python/triagem_gui.py`

### 🔍 iniciar_odq_recruta.bat

Executa diretamente o módulo ODQ Recruta

- Sistema principal de análise de currículos
- Configuração via arquivo .env
- Arquivo: `odq_recruta/app.py`

## Como Usar

### Primeira Execução

1. **Execute `iniciar_sistema.bat`** (duplo clique)
2. O sistema irá:
   - Verificar se o Python está instalado
   - Criar ambiente virtual (se necessário)
   - Instalar dependências automaticamente
   - Mostrar menu de opções

### Execuções Subsequentes

- Use `iniciar_sistema.bat` para ter o menu de escolha
- Ou execute diretamente o módulo desejado:
  - Opção 1 → Triagem GUI (apenas emails não lidos)
  - Opção 2 → ODQ Recruta

## Pré-requisitos

- **Python 3.10+** instalado no sistema
- Conexão com internet (para download de dependências)

## Configurações Necessárias

### Para Triagem GUI (Microsoft 365)

- Configure o arquivo `graph-app-python/parameters.json`
- Credenciais do Microsoft 365

### Para ODQ Recruta

- Configure o arquivo `odq_recruta/.env`
- O sistema copiará automaticamente de `env_example.txt` se necessário

## Solução de Problemas

### Erro: "Python não encontrado"

- Instale Python 3.10+ de <https://www.python.org/downloads/>
- Certifique-se de marcar "Add to PATH" durante a instalação

### Erro: "Falha ao instalar dependências"

- Verifique sua conexão com internet
- Execute como administrador se necessário

### Erro: "Arquivo não encontrado"

- Verifique se todos os arquivos estão na pasta correta
- Re-extraia o sistema se necessário

## Estrutura dos Módulos

```text
Sistema de Triagem ODQ/
├── iniciar_sistema.bat      ← ARQUIVO PRINCIPAL
├── iniciar_odq_recruta.bat  ← ODQ Recruta direto
├── graph-app-python/        ← Módulo Triagem GUI
│   └── triagem_gui.py
└── odq_recruta/             ← Módulo ODQ Recruta
    └── app.py
```

## Suporte

Em caso de dúvidas ou problemas:

1. Verifique este arquivo README
2. Consulte o arquivo `Guia_Instalacao.txt`
3. Entre em contato com o responsável pelo sistema

---

Sistema de Triagem ODQ - v1.1
