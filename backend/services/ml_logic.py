import re
from typing import List, Tuple
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download NLTK resources if needed (idempotent)
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)

stemmer = PorterStemmer()


def _preprocess_text(text: str, use_stemming: bool = True) -> str:
    """Preprocess text: lowercase, remove punctuation, tokenize, stem, remove stopwords."""
    text = (text or "").lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Tokenize on whitespace and punctuation
    tokens = re.findall(r'\b[a-z0-9]+\b', text)
    
    if use_stemming:
        stop_words = set(stopwords.words("english"))
        tokens = [stemmer.stem(t) for t in tokens if t not in stop_words]
    
    return " ".join(tokens)


def _detect_skills(text: str) -> List[str]:
    """Detect common technical skills in text (heuristic-based)."""
    text_lower = text.lower()
    
    # Common tech skills (expandable)
    tech_skills = {
        "python": r"\bpython\b",
        "java": r"\bjava\b",
        "javascript": r"\bjavascript\b|js(?:\s|$)",
        "typescript": r"\btypescript\b",
        "react": r"\breact\b",
        "fastapi": r"\bfastapi\b",
        "django": r"\bdjango\b",
        "sql": r"\bsql\b",
        "mongodb": r"\bmongodb\b",
        "aws": r"\baws\b",
        "docker": r"\bdocker\b",
        "kubernetes": r"\bkubernetes\b|k8s",
        "git": r"\bgit\b",
        "machine learning": r"\bmachine\s+learning\b|ml(?:\s|$)",
        "deep learning": r"\bdeep\s+learning\b",
        "nlp": r"\bnlp\b|natural\s+language\s+processing",
        "bert": r"\bbert\b",
        "tensorflow": r"\btensorflow\b",
        "pytorch": r"\bpytorch\b",
        "scikit-learn": r"\bscikit.learn\b|sklearn",
        "rest api": r"\brest\b|restful\b",
        "gcp": r"\bgcp\b|google\s+cloud",
    }
    
    detected = []
    for skill, pattern in tech_skills.items():
        if re.search(pattern, text_lower):
            detected.append(skill)
    
    return detected


def _detect_experience(text: str) -> float:
    """Estimate years of experience from resume text (heuristic)."""
    text_lower = text.lower()
    
    # Look for experience patterns like "X years", "X+ years", etc.
    patterns = [
        r'(\d+)\+?\s+years?\s+(?:of\s+)?experience',
        r'(?:experience|worked).*?(\d+)\+?\s+years?',
        r'(\d+)\+?\s+years?\s+(?:in|with)',
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        years.extend([int(m) for m in matches if m.isdigit()])
    
    if years:
        return float(max(years))  # Return highest mentioned experience
    
    # If no explicit years found, estimate from job titles/keywords
    if any(word in text_lower for word in ['senior', 'lead', 'principal', 'staff']):
        return 8.0
    elif any(word in text_lower for word in ['mid', 'intermediate']):
        return 4.0
    elif any(word in text_lower for word in ['junior', 'entry', 'graduate']):
        return 1.0
    
    return 0.0


def compute_match_score(
    resume_text: str,
    job_text: str,
    use_bert: bool = False,
    top_k: int = 10,
) -> Tuple[float, List[str], List[str], float, str]:
    """Compute match score using TF-IDF + optional BERT.

    Returns:
        (score_0_to_100, top_keywords, skills_matched, years_experience, method_used)
    """
    resume_clean = _preprocess_text(resume_text)
    job_clean = _preprocess_text(job_text)

    if not resume_clean or not job_clean:
        return 0.0, [], [], 0.0, "empty"

    # TF-IDF baseline
    vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
    tfidf = vectorizer.fit_transform([resume_clean, job_clean])
    tfidf_score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])

    # Optional BERT semantic similarity
    final_score = tfidf_score
    method = "tfidf"
    
    if use_bert:
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
            
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            
            # Encode and compute similarity
            resume_encoded = tokenizer(resume_text, return_tensors="pt", truncation=True)
            job_encoded = tokenizer(job_text, return_tensors="pt", truncation=True)
            
            with torch.no_grad():
                resume_emb = model(**resume_encoded).pooler_output
                job_emb = model(**job_encoded).pooler_output
            
            bert_score = float(cosine_similarity(resume_emb.numpy(), job_emb.numpy())[0][0])
            
            # Weighted combo: 60% BERT + 40% TF-IDF
            final_score = 0.6 * bert_score + 0.4 * tfidf_score
            method = "bert+tfidf"
        except Exception:
            # Fallback to TF-IDF if BERT fails
            pass

    # Convert to 0-100 scale
    score = float(round(final_score * 100.0, 2))

    # Extract top job keywords
    feature_names = vectorizer.get_feature_names_out()
    job_vec = tfidf.toarray()[1]
    indices = job_vec.argsort()[::-1]
    top_indices = [i for i in indices[:top_k] if job_vec[i] > 0]
    top_keywords = [feature_names[i] for i in top_indices]

    # Detect skills
    skills = _detect_skills(resume_text)
    job_skills = set(_detect_skills(job_text))
    skills_matched = [s for s in skills if s in job_skills]

    # Estimate experience
    years_experience = _detect_experience(resume_text)

    return score, top_keywords, skills_matched, years_experience, method

