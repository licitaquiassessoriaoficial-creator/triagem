"""
Testes para core.text_extract.extract_text (mock)
"""
from core.text_extract import extract_text
from pathlib import Path

def test_extract_pdf(monkeypatch):
    def fake_pdf_extract(path):
        return "conteudo pdf"
    monkeypatch.setattr("pdfminer.high_level.extract_text", fake_pdf_extract)
    assert extract_text(Path("arquivo.pdf")) == "conteudo pdf"

def test_extract_docx(monkeypatch):
    class FakeDoc:
        paragraphs = [type("p", (), {"text": "conteudo docx"})()]
    monkeypatch.setattr("docx.Document", lambda path: FakeDoc())
    assert extract_text(Path("arquivo.docx")) == "conteudo docx"

