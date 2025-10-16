"""
Exportação de aprovados para CSV e JSON
"""

import csv
import json
from pathlib import Path

from core.models import CandidateResult


def export_csv(aprovados: list[CandidateResult], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "email_id",
                "remetente",
                "assunto",
                "nome_arquivo",
                "hash",
                "score",
                "caminho_arquivo",
                "data_email",
            ]
        )
        for c in aprovados:
            a = c.attachment
            writer.writerow(
                [
                    a.email_id,
                    a.sender,
                    a.subject,
                    a.filename,
                    a.hash,
                    c.score,
                    str(a.path),
                    a.received_at,
                ]
            )


def export_json(aprovados: list[CandidateResult], path: Path):
    data = []
    for c in aprovados:
        a = c.attachment
        data.append(
            {
                "email_id": a.email_id,
                "remetente": a.sender,
                "assunto": a.subject,
                "nome_arquivo": a.filename,
                "hash": a.hash,
                "score": c.score,
                "caminho_arquivo": str(a.path),
                "data_email": a.received_at,
            }
        )
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
