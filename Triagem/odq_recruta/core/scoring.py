"""
Cálculo de score para currículos
"""
from typing import List, Dict
from core.models import JobSpec
import re
from rapidfuzz import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[\r\n\t]", " ", text)
    text = re.sub(r"[\p{P}\p{S}]", "", text)
    return text.split()

def compute_score(text: str, job: JobSpec) -> Dict:
    tokens = tokenize(text)
    req = sum(kw.lower() in tokens for kw in job.required_keywords)
    des = sum(kw.lower() in tokens for kw in (job.desired_keywords or []))
    req_score = req * 3
    des_score = des * 1
    # Semântico
    vectorizer = TfidfVectorizer().fit([job.description, text])
    tfidf = vectorizer.transform([job.description, text])
    sem_score = cosine_similarity(tfidf[0], tfidf[1])[0][0] * 2 * len(tokens)
    total = min(100, int(req_score + des_score + sem_score))
    return {
        "essenciais": req_score,
        "desejaveis": des_score,
        "semantico": int(sem_score),
        "score_total": total
    }

