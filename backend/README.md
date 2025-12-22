# Resume Match Backend (FastAPI)

A FastAPI backend that accepts resume files (PDF or DOCX) and job descriptions, extracts clean text, matches skills, and returns a detailed 0-100 match score using TF-IDF and optional BERT semantic similarity.

## Features

- **Multi-format support**: Extract text from PDF (via pdfplumber) and DOCX (via python-docx)
- **Clean text extraction**: Normalization and preprocessing with NLTK
- **Skill detection**: Identifies technical skills in resume matching job keywords
- **Experience estimation**: Extracts years of experience from resume text
- **TF-IDF matching**: Fast cosine similarity baseline (default)
- **Optional BERT**: Semantic similarity with transformer models (60% BERT + 40% TF-IDF weighted combo)
- **CORS enabled**: Works with local Next.js frontend

## Endpoints

- `POST /score`: Multipart form with `resume` (file: PDF/DOCX) and `job_description` (string). Optional query param `use_bert=true` for semantic matching.
  - Returns: `score`, `top_keywords`, `skills_matched`, `years_experience`, `method_used`, and explanation.
- `GET /health`: Basic health check.
- `GET /config`: Returns `{ "enable_gpt5": true|false }` from `ENABLE_GPT5` env var.

## Run locally

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Start server

```bash
# Basic (TF-IDF only)
uvicorn backend.main:app --reload --port 8000

# Or set ENABLE_GPT5 flag (Windows PowerShell)
$env:ENABLE_GPT5 = "true"
uvicorn backend.main:app --reload --port 8000
```

## Example requests

### TF-IDF matching (fast)
```bash
curl -X POST \
  -F "resume=@resume.pdf;type=application/pdf" \
  -F "job_description=We need a Python FastAPI developer with ML experience." \
  http://localhost:8000/score
```

### BERT semantic matching (slower, more accurate)
```bash
curl -X POST \
  -F "resume=@resume.pdf;type=application/pdf" \
  -F "job_description=We need a Python FastAPI developer with ML experience." \
  "http://localhost:8000/score?use_bert=true"
```

### DOCX file
```bash
curl -X POST \
  -F "resume=@resume.docx;type=application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -F "job_description=Python developer job description..." \
  http://localhost:8000/score
```

## Response example

```json
{
  "score": 78.5,
  "top_keywords": ["python", "fastapi", "machine", "learning", "sql", "docker"],
  "skills_matched": ["python", "fastapi", "sql"],
  "years_experience": 5.0,
  "resume_char_count": 3421,
  "job_char_count": 541,
  "method_used": "bert+tfidf",
  "explanation": "Score computed using bert+tfidf method. Skills matched: 3."
}
```

## Tech stack

- **Extraction**: pdfplumber (PDF), python-docx (DOCX)
- **Preprocessing**: NLTK (tokenization, stemming, stopwords)
- **Matching**: scikit-learn (TF-IDF), transformers (BERT)
- **ML**: PyTorch for BERT embeddings

## Notes

- TF-IDF is fast and works well for keyword matching.
- BERT (`use_bert=true`) provides semantic understanding but requires GPU or is slower on CPU.
- Skill detection is rule-based; expand `_detect_skills()` with more keywords as needed.
- Experience detection uses regex patterns and keyword heuristics; may vary by resume format.

- Validations: only PDF files are accepted, max size 10 MB, non-empty job description required.
