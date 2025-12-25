import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .schemas import MatchScoreResponse, ConfigResponse
from .services.text_extraction import extract_text_from_file
from .services.ml_logic import compute_match_score

app = FastAPI(title="Resume Match Backend")

# Configure CORS for local Next.js dev
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/score", response_model=MatchScoreResponse)
async def score_resume(
    resume: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_description: str = Form(..., description="Job description text"),
    use_bert: bool = Query(False, description="Enable BERT semantic similarity (slower)"),
):
    """Accepts a resume file (PDF/DOCX) and job description, returns a detailed match score.

    Supports:
    - PDF files via pdfplumber
    - DOCX (Word) files via python-docx
    - TF-IDF + optional BERT semantic similarity
    """
    # Validate file type
    filename = resume.filename or ""
    filename_lower = filename.lower()
    if not (filename_lower.endswith('.pdf') or filename_lower.endswith('.docx')):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    resume_bytes = await resume.read()

    # Basic size limit (10 MB)
    MAX_FILE_BYTES = 10 * 1024 * 1024
    if len(resume_bytes) > MAX_FILE_BYTES:
        raise HTTPException(status_code=400, detail="File exceeds 10 MB size limit")

    # For PDF, ensure it starts with PDF signature
    if filename_lower.endswith('.pdf') and not resume_bytes.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Invalid PDF file content")

    # Validate job description
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description must not be empty")

    # Extract text from file
    resume_text, file_type = extract_text_from_file(resume_bytes, filename)

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail=f"Could not extract text from {file_type.upper()} file. Ensure file is not corrupted."
        )

    # Compute match score
    score, top_keywords, skills_matched, years_exp, method = compute_match_score(
        resume_text,
        job_description,
        use_bert=use_bert,
        top_k=10,
    )

    return MatchScoreResponse(
        score=score,
        top_keywords=top_keywords,
        skills_matched=skills_matched,
        years_experience=years_exp,
        resume_char_count=len(resume_text),
        job_char_count=len(job_description),
        method_used=method,
        explanation=f"Score computed using {method} method. Skills matched: {len(skills_matched)}.",
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/config", response_model=ConfigResponse)
async def config():
    """Return simple runtime config for clients (e.g., feature flags)."""
    enable_gpt5_env = os.environ.get("ENABLE_GPT5", "true").lower()
    enable_gpt5 = enable_gpt5_env in ("1", "true", "yes", "on")
    return ConfigResponse(enable_gpt5=enable_gpt5)
