from pydantic import BaseModel, Field
from typing import List, Optional


class MatchScoreResponse(BaseModel):
    score: float = Field(..., ge=0.0, le=100.0, description="Match score from 0 to 100")
    top_keywords: List[str] = Field(default_factory=list, description="Top weighted job keywords")
    skills_matched: List[str] = Field(default_factory=list, description="Technical skills found in resume that match job")
    years_experience: float = Field(default=0.0, ge=0.0, description="Estimated years of experience from resume")
    resume_char_count: int = Field(..., ge=0)
    job_char_count: int = Field(..., ge=0)
    method_used: str = Field(default="tfidf", description="Matching method: tfidf, bert+tfidf, or empty")
    explanation: Optional[str] = Field(None, description="Optional human-readable explanation")


class ConfigResponse(BaseModel):
    enable_gpt5: bool = Field(..., description="Whether GPT-5 features are enabled for all clients")
