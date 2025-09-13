"""
Resume Optimization Backend API
Main FastAPI application entry point
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from src.resume_parser import ResumeParser
from src.gemini_client import GeminiClient
from src.resume_optimizer import ResumeOptimizer
from src.models import OptimizationRequest, OptimizationResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Resume Optimization API",
    description="Backend API for resume optimization using Google Gemini Flash",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
gemini_client = GeminiClient()
resume_optimizer = ResumeOptimizer(gemini_client)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Resume Optimization API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "resume_parser": "active",
            "gemini_client": "active",
            "resume_optimizer": "active"
        }
    }

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Optimize resume based on job description
    
    Args:
        resume_file: Uploaded resume file (PDF, DOCX, or TXT)
        job_description: Job description text
        
    Returns:
        Optimized resume content
    """
    try:
        # Validate file type
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = resume_file.filename.split('.')[-1].lower()
        if file_extension not in ['pdf', 'docx', 'txt']:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload PDF, DOCX, or TXT files only."
            )
        
        # Read and parse resume
        resume_content = await resume_parser.parse_file(resume_file, file_extension)
        
        if not resume_content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")
        
        # Optimize resume
        optimized_resume = await resume_optimizer.optimize_resume(resume_content, job_description)
        
        return OptimizationResponse(
            original_resume=resume_content,
            optimized_resume=optimized_resume,
            job_description=job_description,
            status="success"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/parse-resume")
async def parse_resume_only(resume_file: UploadFile = File(...)):
    """
    Parse resume file without optimization
    
    Args:
        resume_file: Uploaded resume file (PDF, DOCX, or TXT)
        
    Returns:
        Parsed resume content
    """
    try:
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = resume_file.filename.split('.')[-1].lower()
        if file_extension not in ['pdf', 'docx', 'txt']:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload PDF, DOCX, or TXT files only."
            )
        
        resume_content = await resume_parser.parse_file(resume_file, file_extension)
        
        return {
            "resume_content": resume_content,
            "file_name": resume_file.filename,
            "file_type": file_extension,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )