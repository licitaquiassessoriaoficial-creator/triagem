"""
Cliente IMAP para Gmail com App Password
"""

import email
import imaplib
from pathlib import Path
from typing import List

from core.hashing import sha256_bytes


class GmailIMAPClient:
    def __init__(self, username: str, app_password: str):
        self.username = username
        self.app_password = app_password
        self.conn = None

    def connect(self):
        self.conn = imaplib.IMAP4_SSL("imap.gmail.com")
        self.conn.login(self.username, self.app_password)

    def fetch_attachments(self) -> List[dict]:
        self.conn.select("INBOX")
        typ, data = self.conn.search(None, "ALL")
        ids = data[0].split()
        results = []
        for eid in ids:
            typ, msg_data = self.conn.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                filename = part.get_filename()
                if filename and filename.lower().endswith(
                    (".pdf", ".doc", ".docx")
                ):
                    payload = part.get_payload(decode=True)
                    hash = sha256_bytes(payload)
                    results.append(
                        {
                            "email_id": eid.decode(),
                            "filename": filename,
                            "payload": payload,
                            "hash": hash,
                            "sender": msg.get("From"),
                            "subject": msg.get("Subject"),
                            "received_at": msg.get("Date"),
                        }
                    )
        return results
