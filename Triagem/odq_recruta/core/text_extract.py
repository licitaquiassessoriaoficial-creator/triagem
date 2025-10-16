"""
Extração de texto de PDF, DOCX, DOC
"""
from pathlib import Path
from typing import Optional

def extract_text(path: Path) -> Optional[str]:
    ext = path.suffix.lower()
    if ext == ".pdf":
        try:
            from pdfminer.high_level import extract_text as pdf_extract
            return pdf_extract(str(path))
        except Exception:
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(path))
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            except Exception:
                return None
    elif ext == ".docx":
        try:
            from docx import Document
            doc = Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return None
    elif ext == ".doc":
        try:
            import docx2txt
            return docx2txt.process(str(path))  
        except Exception:
            return None
    return None
