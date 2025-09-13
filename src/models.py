"""
Pydantic models for the Resume Optimization API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class OptimizationStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PROCESSING = "processing"

class OptimizationRequest(BaseModel):
    """Request model for resume optimization"""
    resume_content: str = Field(..., description="Original resume content")
    job_description: str = Field(..., description="Job description text")
    
class OptimizationResponse(BaseModel):
    """Response model for resume optimization"""
    original_resume: str = Field(..., description="Original resume content")
    optimized_resume: str = Field(..., description="Optimized resume content")
    job_description: str = Field(..., description="Job description used for optimization")
    status: OptimizationStatus = Field(..., description="Processing status")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ResumeAnalysis(BaseModel):
    """Model for resume analysis results"""
    skills_match: float = Field(..., description="Skills match percentage")
    experience_match: float = Field(..., description="Experience match percentage")
    keyword_density: Dict[str, float] = Field(..., description="Keyword density analysis")
    ats_score: float = Field(..., description="ATS compatibility score")
    suggestions: list = Field(..., description="Optimization suggestions")

class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    file_name: str = Field(..., description="Uploaded file name")
    file_type: str = Field(..., description="File type/extension")
    content: str = Field(..., description="Extracted content")
    status: OptimizationStatus = Field(..., description="Processing status")