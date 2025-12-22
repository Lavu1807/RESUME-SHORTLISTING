import re
from io import BytesIO
from typing import Optional

import pdfplumber
from docx import Document


def _clean_text(text: str) -> str:
    """Normalize whitespace, remove extra newlines, preserve structure."""
    if not text:
        return ""
    # Replace multiple newlines with single space
    text = re.sub(r'\n\s*\n', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF using pdfplumber for better quality than pdfminer.

    Args:
        pdf_bytes: Raw PDF file bytes

    Returns:
        Cleaned extracted text, or empty string if extraction fails.
    """
    try:
        with BytesIO(pdf_bytes) as bio:
            with pdfplumber.open(bio) as pdf:
                text_parts = []
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    if page_text:
                        text_parts.append(page_text)
                full_text = "\n".join(text_parts)
                return _clean_text(full_text)
    except Exception:
        # Fallback to silent failure; in production, log this
        return ""


def extract_text_from_docx(docx_bytes: bytes) -> str:
    """Extract text from DOCX (MS Word) files.

    Args:
        docx_bytes: Raw DOCX file bytes

    Returns:
        Cleaned extracted text, or empty string if extraction fails.
    """
    try:
        with BytesIO(docx_bytes) as bio:
            doc = Document(bio)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            full_text = "\n".join(paragraphs)
            return _clean_text(full_text)
    except Exception:
        return ""


def extract_text_from_file(file_bytes: bytes, filename: str) -> tuple[str, str]:
    """Dispatch extraction based on file extension.

    Args:
        file_bytes: Raw file bytes
        filename: Filename to infer format

    Returns:
        Tuple of (extracted_text, file_type)
    """
    filename_lower = filename.lower()

    if filename_lower.endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
        return text, "pdf"
    elif filename_lower.endswith('.docx'):
        text = extract_text_from_docx(file_bytes)
        return text, "docx"
    else:
        # Fallback: try PDF first, then DOCX
        text = extract_text_from_pdf(file_bytes)
        if text:
            return text, "pdf"
        text = extract_text_from_docx(file_bytes)
        if text:
            return text, "docx"
        return "", "unknown"

