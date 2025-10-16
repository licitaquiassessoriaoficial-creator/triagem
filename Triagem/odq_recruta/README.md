# ODQ Recruta

Aplicativo desktop para triagem de currículos via Gmail e Microsoft 365.

## Pré-requisitos
- Python 3.10+
- App Password do Gmail
- App registrado no Azure AD (Microsoft 365)

## Configuração
1. Crie um App Password no Gmail: [Instruções](https://support.google.com/accounts/answer/185833)
2. Registre o app no Azure AD:
   - Copie o Client ID, Tenant ID, Redirect URI
   - Permissão: Mail.Read (delegada)
3. Preencha o arquivo `.env` conforme `.env.example`

## Instalação
```bash
pip install -r requirements.txt
```

## Execução
```bash
python app.py
```

## Limitações conhecidas
- Arquivos .doc (legado) dependem de textract (opcional)
- Busca irrestrita, pode ser lenta em caixas grandes

## Critérios de aceitação
- Busca e download de anexos PDF/DOC/DOCX no Gmail/M365
- Logs em tempo real na GUI e arquivo
- Processamento paralelo (download/análise)
- Deduplicação por hash com cache
- Score 0–100 com pesos e match semântico
- Aprovação por threshold
- Salva aprovados em pasta vaga/data
- Exporta aprovados.csv e aprovados.json
- Testes passando (pytest)
- README com instruções
