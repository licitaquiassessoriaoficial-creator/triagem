"""
Configuração segura para Microsoft Graph API
Use variáveis de ambiente para manter os segredos seguros
"""

import os

# Configurações do Azure AD
AZURE_CONFIG = {
    "client_id": os.getenv("AZURE_CLIENT_ID", "your-client-id-here"),
    "client_secret": os.getenv(
        "AZURE_CLIENT_SECRET", "your-client-secret-here"
    ),
    "tenant_id": os.getenv("AZURE_TENANT_ID", "your-tenant-id-here"),
    "redirect_uri": os.getenv(
        "AZURE_REDIRECT_URI", "http://localhost:8080/callback"
    ),
}


def get_azure_config():
    """Retorna configuração do Azure com validação"""
    if not all(
        [
            AZURE_CONFIG["client_id"] != "your-client-id-here",
            AZURE_CONFIG["client_secret"] != "your-client-secret-here",
            AZURE_CONFIG["tenant_id"] != "your-tenant-id-here",
        ]
    ):
        raise ValueError(
            "Configure as variáveis de ambiente AZURE_CLIENT_ID, "
            "AZURE_CLIENT_SECRET e AZURE_TENANT_ID"
        )
    return AZURE_CONFIG
