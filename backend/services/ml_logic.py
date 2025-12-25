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
    """Estimate years of experience from resume text (heuristic).
    
    Attempts to extract experience in the following order:
    1. Explicit "X years of experience" statements
    2. Job tenure calculations from date ranges
    3. Professional role level inference (fallback only)
    """
    text_lower = text.lower()
    
    # Priority 1: Look for explicit experience patterns like "X years", "X+ years", etc.
    explicit_patterns = [
        r'(\d+)\+?\s+years?\s+(?:of\s+)?(?:professional\s+)?experience',
        r'total\s+experience:?\s*(\d+)\+?\s+years?',
        r'experience:?\s*(\d+)\+?\s+years?',
    ]
    
    years = []
    for pattern in explicit_patterns:
        matches = re.findall(pattern, text_lower)
        years.extend([int(m) for m in matches if m.isdigit()])
    
    if years:
        # Return average if multiple values found, capped at 50 years
        avg_years = sum(years) / len(years)
        return min(float(avg_years), 50.0)
    
    # Priority 2: Try to calculate from date ranges in work history
    # Look for patterns like "Jan 2020 - Dec 2023" or "2020 - 2023"
    date_patterns = [
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.?\s*(\d{4})\s*[-–]\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\.?\s*(\d{4})',
        r'(\d{4})\s*[-–]\s*(?:present|current|now|ongoing)',
    ]
    
    total_duration = 0.0
    for pattern in date_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            if isinstance(match, tuple):
                if len(match) == 2:
                    try:
                        start_year = int(match[0])
                        # Handle "present" case
                        if match[1] in ('present', 'current', 'now', 'ongoing'):
                            end_year = 2025  # Current year
                        else:
                            end_year = int(match[1])
                        
                        if start_year <= end_year:
                            duration = end_year - start_year
                            if 0 <= duration <= 50:  # Sanity check
                                total_duration += duration
                    except (ValueError, IndexError):
                        pass
            else:
                try:
                    year = int(match)
                    # If we find "2020 - present" type pattern
                    if year <= 2025:
                        total_duration += (2025 - year)
                except (ValueError, TypeError):
                    pass
    
    if total_duration > 0:
        # Average duration across jobs found
        job_count = len(re.findall(r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).*?\d{4}|(?:job|position|role|worked|employed)', text_lower))
        if job_count > 0:
            return min(float(total_duration / max(1, job_count)), 50.0)
        return min(float(total_duration), 50.0)
    
    # Priority 3: Estimate from job level keywords (conservative estimates)
    # Only use this if no explicit data is found
    if any(word in text_lower for word in ['principal', 'director', 'vp ', 'vice president']):
        return 15.0
    elif any(word in text_lower for word in ['senior', 'lead', 'architect', 'staff']):
        return 7.0
    elif any(word in text_lower for word in ['mid-level', 'mid level', 'intermediate', 'specialist']):
        return 4.0
    elif any(word in text_lower for word in ['junior', 'entry', 'graduate', 'intern', 'trainee']):
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

