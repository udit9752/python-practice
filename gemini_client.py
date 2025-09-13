import logging
import google.generativeai as genai
from typing import Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Google Gemini Flash API."""
    
    def __init__(self):
        """Initialize Gemini client with API key and configuration."""
        Config.validate_config()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        self.generation_config = Config.GENERATION_CONFIG
    
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description using Gemini.
        
        Args:
            resume_text: Extracted resume content
            job_description: Job description text
            
        Returns:
            Dictionary containing analysis results
        """
        prompt = self._create_analysis_prompt(resume_text, job_description)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "analysis": response.text,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            return {
                "analysis": None,
                "success": False,
                "error": str(e)
            }
    
    def optimize_resume(self, resume_text: str, job_description: str, analysis: str = None) -> Dict[str, Any]:
        """
        Optimize resume content for ATS and job alignment using Gemini.
        
        Args:
            resume_text: Original resume content
            job_description: Target job description
            analysis: Previous analysis results (optional)
            
        Returns:
            Dictionary containing optimized resume
        """
        prompt = self._create_optimization_prompt(resume_text, job_description, analysis)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return {
                "optimized_resume": response.text,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error optimizing resume: {str(e)}")
            return {
                "optimized_resume": None,
                "success": False,
                "error": str(e)
            }
    
    def _create_analysis_prompt(self, resume_text: str, job_description: str) -> str:
        """Create prompt for resume analysis."""
        return f"""
You are an expert resume analyst and ATS optimization specialist. Analyze the following resume against the provided job description.

RESUME CONTENT:
{resume_text}

JOB DESCRIPTION:
{job_description}

Please provide a comprehensive analysis including:

1. **Keyword Alignment**: Compare resume keywords with job description requirements
2. **Skills Gap Analysis**: Identify missing skills or qualifications
3. **Experience Relevance**: Evaluate how well experience matches job requirements
4. **ATS Compatibility Issues**: Identify potential ATS parsing problems
5. **Formatting Issues**: Note any formatting that might hurt ATS readability
6. **Improvement Recommendations**: Specific suggestions for optimization

Format your response in clear sections with actionable insights.
        """
    
    def _create_optimization_prompt(self, resume_text: str, job_description: str, analysis: str = None) -> str:
        """Create prompt for resume optimization."""
        analysis_section = f"\n\nPREVIOUS ANALYSIS:\n{analysis}\n" if analysis else ""
        
        return f"""
You are an expert resume optimizer specializing in ATS-friendly resume creation. Your task is to optimize the following resume to better align with the job description while maintaining ATS compatibility.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
{analysis_section}

OPTIMIZATION REQUIREMENTS:
1. **ATS Optimization**: Ensure the resume is fully ATS-compatible with:
   - Clear, simple formatting
   - Standard section headers (Experience, Education, Skills, etc.)
   - No complex formatting, tables, or graphics
   - Consistent date formats
   - Proper use of keywords from job description

2. **Content Optimization**:
   - Incorporate relevant keywords from job description naturally
   - Highlight relevant experience and achievements
   - Quantify accomplishments where possible
   - Align skills section with job requirements
   - Improve action verbs and impact statements

3. **Structure Optimization**:
   - Use standard resume sections
   - Maintain logical flow and hierarchy
   - Ensure consistent formatting throughout
   - Keep bullet points concise and impactful

4. **Keyword Integration**:
   - Naturally integrate job-specific keywords
   - Match technical skills and requirements
   - Use industry-standard terminology
   - Maintain keyword density without stuffing

Please provide the complete optimized resume with improved content, better keyword alignment, and full ATS compatibility. Maintain the person's actual experience and qualifications while presenting them in the most effective way for this specific job.

Return only the optimized resume content without any additional commentary or explanations.
        """