import logging
from typing import Dict, Any, Tuple
from file_parser import FileParser
from gemini_client import GeminiClient
from ats_optimizer import ATSOptimizer

logger = logging.getLogger(__name__)

class ResumeProcessor:
    """Core resume processing pipeline that orchestrates the entire optimization workflow."""
    
    def __init__(self):
        """Initialize the resume processor with required components."""
        self.file_parser = FileParser()
        self.gemini_client = GeminiClient()
        self.ats_optimizer = ATSOptimizer()
    
    async def process_resume(
        self, 
        file_content: bytes, 
        filename: str, 
        job_description: str,
        include_analysis: bool = False
    ) -> Dict[str, Any]:
        """
        Complete resume processing pipeline.
        
        Args:
            file_content: Raw file content as bytes
            filename: Name of the uploaded file
            job_description: Target job description
            include_analysis: Whether to include detailed analysis in response
            
        Returns:
            Dictionary containing processing results
        """
        try:
            # Step 1: Parse the resume file
            logger.info(f"Starting resume processing for file: {filename}")
            resume_text, file_format = self.file_parser.parse_file(file_content, filename)
            
            # Validate resume content
            if not self.file_parser.validate_content(resume_text):
                return {
                    "success": False,
                    "error": "The uploaded file does not appear to contain valid resume content",
                    "step": "validation"
                }
            
            logger.info("Resume file parsed successfully")
            
            # Step 2: Analyze resume against job description (optional detailed analysis)
            analysis_result = None
            if include_analysis:
                logger.info("Performing detailed resume analysis")
                analysis_result = self.gemini_client.analyze_resume(resume_text, job_description)
                
                if not analysis_result["success"]:
                    return {
                        "success": False,
                        "error": f"Resume analysis failed: {analysis_result.get('error', 'Unknown error')}",
                        "step": "analysis"
                    }
            
            # Step 3: Optimize resume using Gemini
            logger.info("Optimizing resume with Gemini AI")
            optimization_result = self.gemini_client.optimize_resume(
                resume_text, 
                job_description, 
                analysis_result["analysis"] if analysis_result else None
            )
            
            if not optimization_result["success"]:
                return {
                    "success": False,
                    "error": f"Resume optimization failed: {optimization_result.get('error', 'Unknown error')}",
                    "step": "optimization"
                }
            
            # Step 4: Apply ATS-specific optimizations
            logger.info("Applying ATS-specific optimizations")
            ats_optimized_resume = self.ats_optimizer.optimize_for_ats(
                optimization_result["optimized_resume"]
            )
            
            # Step 5: Prepare final response
            response = {
                "success": True,
                "original_format": file_format,
                "optimized_resume": ats_optimized_resume,
                "processing_steps": [
                    "File parsing completed",
                    "Content validation passed",
                    "AI optimization completed",
                    "ATS formatting applied"
                ]
            }
            
            # Include analysis if requested
            if include_analysis and analysis_result:
                response["analysis"] = analysis_result["analysis"]
                response["processing_steps"].insert(-2, "Detailed analysis completed")
            
            logger.info("Resume processing completed successfully")
            return response
            
        except ValueError as e:
            # Handle validation errors (file format, size, etc.)
            logger.error(f"Validation error during resume processing: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "step": "validation"
            }
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error during resume processing: {str(e)}")
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}",
                "step": "unknown"
            }
    
    def get_processing_info(self) -> Dict[str, Any]:
        """
        Get information about the processing capabilities.
        
        Returns:
            Dictionary with processing information
        """
        return {
            "supported_formats": self.file_parser.supported_formats,
            "max_file_size_mb": self.file_parser.max_file_size / (1024 * 1024),
            "features": [
                "Multi-format resume parsing (PDF, DOCX, TXT)",
                "AI-powered resume optimization",
                "ATS compatibility enhancement",
                "Job description alignment",
                "Keyword optimization",
                "Format standardization"
            ],
            "processing_steps": [
                "File format validation and parsing",
                "Resume content validation",
                "Optional detailed analysis",
                "AI-powered optimization",
                "ATS formatting enhancement"
            ]
        }
    
    def validate_inputs(self, file_content: bytes, filename: str, job_description: str) -> Tuple[bool, str]:
        """
        Validate inputs before processing.
        
        Args:
            file_content: File content to validate
            filename: Filename to validate
            job_description: Job description to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file content exists
        if not file_content:
            return False, "No file content provided"
        
        # Check filename
        if not filename:
            return False, "No filename provided"
        
        # Check job description
        if not job_description or len(job_description.strip()) < 50:
            return False, "Job description must be at least 50 characters long"
        
        # Check file extension
        file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
        if file_extension not in self.file_parser.supported_formats:
            return False, f"Unsupported file format: {file_extension}"
        
        return True, ""