"""
Leitura e validação de variáveis de ambiente (.env)
"""

import os
from pathlib import Path

from dotenv import load_dotenv

GMAIL_ENV_VARS = ["GMAIL_USERNAME", "GMAIL_APP_PASSWORD"]
M365_ENV_VARS = [
    "MS_CLIENT_ID",
    "MS_TENANT_ID",
    "MS_REDIRECT_URI",
    "MS_SCOPES",
]


def load_and_validate_env(
    env_path: Path = Path(".env"),
    use_gmail: bool = False,
    use_m365: bool = False,
) -> dict:
    load_dotenv(env_path)
    required_vars = []
    if use_gmail:
        required_vars += GMAIL_ENV_VARS
    if use_m365:
        required_vars += M365_ENV_VARS
    config = {var: os.getenv(var) for var in required_vars}
    missing = [k for k, v in config.items() if not v]
    if missing:
        raise ValueError(f"Variáveis ausentes no .env: {', '.join(missing)}")
    # Adiciona todas as variáveis (mesmo as não obrigatórias) para uso
    # posterior
    config.update(
        {
            var: os.getenv(var)
            for var in set(GMAIL_ENV_VARS + M365_ENV_VARS)
            if var not in config
        }
    )
    return config
