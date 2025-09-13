import logging
import asyncio
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from resume_processor import ResumeProcessor
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Optimization Backend",
    description="A comprehensive backend system for optimizing resumes using AI and ATS best practices",
    version="1.0.0"
)

# Add CORS middleware for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize resume processor
resume_processor = ResumeProcessor()

# Pydantic models for request/response
class OptimizationResponse(BaseModel):
    success: bool
    optimized_resume: Optional[str] = None
    analysis: Optional[str] = None
    original_format: Optional[str] = None
    processing_steps: Optional[list] = None
    error: Optional[str] = None
    step: Optional[str] = None

class ProcessingInfo(BaseModel):
    supported_formats: list
    max_file_size_mb: float
    features: list
    processing_steps: list

class HealthCheck(BaseModel):
    status: str
    message: str
    version: str

@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint providing API information."""
    return HealthCheck(
        status="healthy",
        message="Resume Optimization Backend API is running",
        version="1.0.0"
    )

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    try:
        # Validate configuration
        Config.validate_config()
        return HealthCheck(
            status="healthy",
            message="All systems operational",
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )

@app.get("/info", response_model=ProcessingInfo)
async def get_processing_info():
    """Get information about processing capabilities."""
    return ProcessingInfo(**resume_processor.get_processing_info())

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_resume(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., description="Target job description"),
    include_analysis: bool = Form(False, description="Include detailed analysis in response")
):
    """
    Main endpoint for resume optimization.
    
    This endpoint accepts a resume file and job description, then processes
    the resume through the complete optimization pipeline.
    """
    try:
        logger.info(f"Received optimization request for file: {resume_file.filename}")
        
        # Read file content
        file_content = await resume_file.read()
        
        # Validate inputs
        is_valid, error_message = resume_processor.validate_inputs(
            file_content, resume_file.filename, job_description
        )
        
        if not is_valid:
            logger.warning(f"Input validation failed: {error_message}")
            return OptimizationResponse(
                success=False,
                error=error_message,
                step="validation"
            )
        
        # Process the resume
        result = await resume_processor.process_resume(
            file_content=file_content,
            filename=resume_file.filename,
            job_description=job_description,
            include_analysis=include_analysis
        )
        
        return OptimizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Unexpected error in optimize endpoint: {str(e)}")
        return OptimizationResponse(
            success=False,
            error=f"An unexpected error occurred: {str(e)}",
            step="unknown"
        )

@app.post("/analyze", response_model=OptimizationResponse)
async def analyze_resume(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., description="Target job description")
):
    """
    Endpoint for resume analysis only (without optimization).
    
    This endpoint provides detailed analysis of how well a resume
    matches a job description without performing optimization.
    """
    try:
        logger.info(f"Received analysis request for file: {resume_file.filename}")
        
        # Read file content
        file_content = await resume_file.read()
        
        # Validate inputs
        is_valid, error_message = resume_processor.validate_inputs(
            file_content, resume_file.filename, job_description
        )
        
        if not is_valid:
            logger.warning(f"Input validation failed: {error_message}")
            return OptimizationResponse(
                success=False,
                error=error_message,
                step="validation"
            )
        
        # Process with analysis only (no optimization)
        result = await resume_processor.process_resume(
            file_content=file_content,
            filename=resume_file.filename,
            job_description=job_description,
            include_analysis=True
        )
        
        # For analysis-only endpoint, don't return the optimized resume
        if result.get("success"):
            result["optimized_resume"] = None
        
        return OptimizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {str(e)}")
        return OptimizationResponse(
            success=False,
            error=f"An unexpected error occurred: {str(e)}",
            step="unknown"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with proper logging."""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions with proper logging."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )