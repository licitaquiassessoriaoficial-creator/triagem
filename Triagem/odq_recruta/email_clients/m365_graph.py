"""
Cliente Microsoft 365 Graph API com MSAL
"""
import msal
import requests
from pathlib import Path
from typing import List
from core.hashing import sha256_bytes
import os

class M365GraphClient:
    def __init__(self, client_id: str, tenant_id: str, redirect_uri: str, scopes: list, token_cache_path: Path, client_secret: str = None):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.token_cache_path = token_cache_path
        self.client_secret = client_secret
        self.token = None

        # Carrega ou cria cache de token persistente
        self.token_cache = msal.SerializableTokenCache()
        if token_cache_path.exists():
            self.token_cache.deserialize(token_cache_path.read_text())

        if client_secret:
            self.app = msal.ConfidentialClientApplication(
                client_id,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
                client_credential=client_secret,
                token_cache=self.token_cache
            )
        else:
            self.app = msal.PublicClientApplication(
                client_id,
                authority=f"https://login.microsoftonline.com/{tenant_id}",
                token_cache=self.token_cache
            )

    def authenticate(self):
        def persist_cache():
            self.token_cache_path.parent.mkdir(exist_ok=True)
            self.token_cache_path.write_text(self.token_cache.serialize())
        if self.client_secret:
            # Client Credentials Flow (Application permissions)
            self.token = self.app.acquire_token_for_client(scopes=self.scopes)
            if not self.token or "access_token" not in self.token:
                import json
                print("[MSAL ERROR] Token response:")
                print(json.dumps(self.token, indent=2, ensure_ascii=False))
                raise Exception(f"Falha na autenticação MSAL (Client Credentials Flow): {self.token}")
            persist_cache()
        else:
            # Device Code Flow
            accounts = self.app.get_accounts()
            if accounts:
                self.token = self.app.acquire_token_silent(self.scopes, account=accounts[0])
            if not self.token:
                flow = self.app.initiate_device_flow(scopes=self.scopes)
                if "user_code" not in flow:
                    raise Exception("Falha ao iniciar Device Flow")
                print(f"Acesse {flow['verification_uri']} e insira o código: {flow['user_code']}")
                self.token = self.app.acquire_token_by_device_flow(flow)
            if not self.token or "access_token" not in self.token:
                raise Exception("Falha na autenticação MSAL")
            persist_cache()

    def fetch_attachments(self) -> List[dict]:
        headers = {"Authorization": f"Bearer {self.token['access_token']}"}
        url = "https://graph.microsoft.com/v1.0/me/messages?$select=subject,from,receivedDateTime,hasAttachments&$top=50"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        results = []
        for msg in resp.json().get("value", []):
            if msg.get("hasAttachments"):
                att_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg['id']}/attachments"
                att_resp = requests.get(att_url, headers=headers)
                att_resp.raise_for_status()
                for att in att_resp.json().get("value", []):
                    fname = att.get("name")
                    if fname and fname.lower().endswith((".pdf", ".doc", ".docx")):
                        payload = bytes(att["contentBytes"], "utf-8")
                        hash = sha256_bytes(payload)
                        results.append({
                            "email_id": msg["id"],
                            "filename": fname,
                            "payload": payload,
                            "hash": hash,
                            "sender": msg["from"]["emailAddress"]["address"],
                            "subject": msg["subject"],
                            "received_at": msg["receivedDateTime"]
                        })
        return results
