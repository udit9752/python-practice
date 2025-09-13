"""
Google Gemini Flash API Client
Handles communication with Google's Gemini API for resume optimization
"""

import os
import google.generativeai as genai
from typing import Optional, Dict, Any
import json
import re

class GeminiClient:
    """Client for Google Gemini Flash API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google Gemini API key. If not provided, will use environment variable
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_resume_jd_match(self, resume_content: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze how well the resume matches the job description
        
        Args:
            resume_content: Resume text content
            job_description: Job description text
            
        Returns:
            Analysis results including match scores and suggestions
        """
        prompt = f"""
        Analyze the following resume against the job description and provide a detailed analysis.
        
        RESUME:
        {resume_content}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please provide a JSON response with the following structure:
        {{
            "skills_match_percentage": <number between 0-100>,
            "experience_match_percentage": <number between 0-100>,
            "keyword_density": {{
                "required_keywords": <list of keywords from JD>,
                "missing_keywords": <list of missing important keywords>,
                "keyword_frequency": <dict of keyword frequencies in resume>
            }},
            "ats_score": <number between 0-100>,
            "strengths": <list of resume strengths>,
            "weaknesses": <list of areas for improvement>,
            "suggestions": <list of specific optimization suggestions>
        }}
        
        Focus on:
        1. Technical skills alignment
        2. Experience relevance
        3. Keyword optimization for ATS
        4. Format and structure improvements
        5. Quantifiable achievements
        """
        
        try:
            response = await self._generate_content(prompt)
            return self._parse_json_response(response)
        except Exception as e:
            raise Exception(f"Error analyzing resume-JD match: {str(e)}")
    
    async def optimize_resume_content(self, resume_content: str, job_description: str, analysis: Dict[str, Any]) -> str:
        """
        Optimize resume content based on analysis and job description
        
        Args:
            resume_content: Original resume content
            job_description: Job description text
            analysis: Analysis results from analyze_resume_jd_match
            
        Returns:
            Optimized resume content
        """
        prompt = f"""
        Optimize the following resume to better match the job description while maintaining ATS compatibility.
        
        ORIGINAL RESUME:
        {resume_content}
        
        JOB DESCRIPTION:
        {job_description}
        
        ANALYSIS RESULTS:
        {json.dumps(analysis, indent=2)}
        
        Please provide an optimized version of the resume that:
        1. Incorporates missing keywords naturally
        2. Highlights relevant experience and skills
        3. Uses action verbs and quantifiable achievements
        4. Maintains clear, ATS-friendly formatting
        5. Preserves the original structure but improves content
        6. Ensures all sections are well-organized and professional
        
        Return ONLY the optimized resume content, no additional commentary.
        """
        
        try:
            optimized_resume = await self._generate_content(prompt)
            return self._clean_optimized_content(optimized_resume)
        except Exception as e:
            raise Exception(f"Error optimizing resume: {str(e)}")
    
    async def generate_ats_friendly_format(self, resume_content: str) -> str:
        """
        Format resume content to be ATS-friendly
        
        Args:
            resume_content: Resume content to format
            
        Returns:
            ATS-friendly formatted resume
        """
        prompt = f"""
        Format the following resume content to be ATS (Applicant Tracking System) friendly.
        
        RESUME CONTENT:
        {resume_content}
        
        Please ensure:
        1. Use standard section headers (Contact, Summary, Experience, Education, Skills)
        2. Use bullet points for lists
        3. Include relevant keywords naturally
        4. Use consistent formatting throughout
        5. Avoid graphics, tables, or complex formatting
        6. Use standard fonts and clear structure
        7. Include quantifiable achievements where possible
        
        Return ONLY the formatted resume content.
        """
        
        try:
            formatted_resume = await self._generate_content(prompt)
            return self._clean_optimized_content(formatted_resume)
        except Exception as e:
            raise Exception(f"Error formatting resume for ATS: {str(e)}")
    
    async def _generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini API
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            Generated content
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON response from Gemini API
        
        Args:
            response: Raw response text
            
        Returns:
            Parsed JSON as dictionary
        """
        try:
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # If no JSON found, return a default structure
                return {
                    "skills_match_percentage": 0,
                    "experience_match_percentage": 0,
                    "keyword_density": {
                        "required_keywords": [],
                        "missing_keywords": [],
                        "keyword_frequency": {}
                    },
                    "ats_score": 0,
                    "strengths": [],
                    "weaknesses": [],
                    "suggestions": []
                }
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON response: {str(e)}")
    
    def _clean_optimized_content(self, content: str) -> str:
        """
        Clean and format optimized resume content
        
        Args:
            content: Raw optimized content
            
        Returns:
            Cleaned resume content
        """
        if not content:
            return ""
        
        # Remove any markdown formatting that might interfere
        content = re.sub(r'```[a-zA-Z]*\n?', '', content)
        content = re.sub(r'```', '', content)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Ensure proper line breaks
        content = content.strip()
        
        return content