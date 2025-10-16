"""
Testes para core.scoring.compute_score
"""

from core.models import JobSpec
from core.scoring import compute_score


def test_score_essenciais():
    job = JobSpec("Dev", "Python dev", ["python"], [], 70)
    text = "Python, SQL, API"
    result = compute_score(text, job)
    assert result["essenciais"] >= 3
    assert result["score_total"] >= 3


def test_score_desejaveis():
    job = JobSpec("Dev", "Python dev", [], ["sql"], 70)
    text = "Python, SQL, API"
    result = compute_score(text, job)
    assert result["desejaveis"] >= 1


def test_score_semantico():
    job = JobSpec("Dev", "Python developer", ["python"], [], 70)
    text = "Python developer with experience"
    result = compute_score(text, job)
    assert result["semantico"] >= 0
