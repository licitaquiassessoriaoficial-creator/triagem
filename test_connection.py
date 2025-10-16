"""
Teste de Conexão com Microsoft Graph API
Verifica se as credenciais estão funcionando corretamente
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao Python path
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

# Carregar variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv(root_dir / '.env')

import requests
import msal


def test_graph_connection():
    """Testa a conexão com Microsoft Graph API"""
    
    # Configurações do Azure AD
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET") 
    tenant_id = os.getenv("AZURE_TENANT_ID")
    user_email = os.getenv("AZURE_USER_EMAIL")
    
    print("🔍 Testando configuração do Microsoft Graph...")
    print(f"Client ID: {client_id[:8]}..." if client_id else "❌ CLIENT_ID não encontrado")
    print(f"Tenant ID: {tenant_id[:8]}..." if tenant_id else "❌ TENANT_ID não encontrado") 
    print(f"User Email: {user_email}" if user_email else "❌ USER_EMAIL não encontrado")
    print(f"Client Secret: {'✅ Configurado' if client_secret else '❌ Não encontrado'}")
    
    if not all([client_id, client_secret, tenant_id, user_email]):
        print("\n❌ Credenciais incompletas! Verifique o arquivo .env")
        return False
    
    try:
        # Criar cliente MSAL
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=client_id,
            client_credential=client_secret,
            authority=authority
        )
        
        # Obter token
        print("\n🔐 Obtendo token de acesso...")
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_silent(scopes, account=None)
        
        if not result:
            result = app.acquire_token_for_client(scopes=scopes)
        
        if "access_token" not in result:
            print(f"❌ Erro ao obter token: {result.get('error_description', 'Erro desconhecido')}")
            return False
            
        token = result["access_token"]
        print("✅ Token obtido com sucesso!")
        
        # Testar endpoint do Graph
        print(f"\n📧 Testando acesso ao email: {user_email}")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Testar endpoint de mensagens
        url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
        params = {"$top": 5, "$select": "subject,from,receivedDateTime"}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get("value", [])
            print(f"✅ Conexão bem-sucedida! Encontradas {len(messages)} mensagens")
            
            if messages:
                print("\n📬 Últimas mensagens:")
                for i, msg in enumerate(messages[:3], 1):
                    subject = msg.get("subject", "Sem assunto")
                    sender = msg.get("from", {}).get("emailAddress", {}).get("address", "Desconhecido")
                    date = msg.get("receivedDateTime", "Data desconhecida")
                    print(f"  {i}. {subject[:50]}... (de: {sender})")
            
            return True
            
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Sistema de Triagem ODQ - Teste de Conectividade")
    print("=" * 50)
    
    success = test_graph_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCESSO! As credenciais estão funcionando corretamente.")
        print("✅ O sistema pode ler emails da conta configurada.")
    else:
        print("❌ FALHA! Verifique as credenciais no arquivo .env")
        print("📝 Consulte CONFIGURACAO_SEGURA.md para instruções.")
    
    print("\n🔗 Repository: https://github.com/licitaquiassessoriaoficial-creator/triagem.git")