"""
Resume Optimizer Module
Orchestrates the resume optimization process using Gemini API
"""

from typing import Dict, Any, Tuple
import re
from .gemini_client import GeminiClient
from .resume_parser import ResumeParser

class ResumeOptimizer:
    """Main optimizer class that coordinates resume optimization"""
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize the optimizer
        
        Args:
            gemini_client: Configured Gemini client instance
        """
        self.gemini_client = gemini_client
        self.resume_parser = ResumeParser()
    
    async def optimize_resume(self, resume_content: str, job_description: str) -> str:
        """
        Complete resume optimization pipeline
        
        Args:
            resume_content: Original resume content
            job_description: Job description text
            
        Returns:
            Optimized resume content
        """
        try:
            # Step 1: Analyze resume-JD match
            analysis = await self.gemini_client.analyze_resume_jd_match(resume_content, job_description)
            
            # Step 2: Optimize content based on analysis
            optimized_content = await self.gemini_client.optimize_resume_content(
                resume_content, job_description, analysis
            )
            
            # Step 3: Ensure ATS-friendly formatting
            ats_optimized = await self.gemini_client.generate_ats_friendly_format(optimized_content)
            
            # Step 4: Final cleanup and validation
            final_resume = self._finalize_resume(ats_optimized, analysis)
            
            return final_resume
            
        except Exception as e:
            raise Exception(f"Resume optimization failed: {str(e)}")
    
    def _finalize_resume(self, optimized_content: str, analysis: Dict[str, Any]) -> str:
        """
        Final cleanup and validation of optimized resume
        
        Args:
            optimized_content: Optimized resume content
            analysis: Analysis results
            
        Returns:
            Finalized resume content
        """
        # Extract sections for better organization
        sections = self.resume_parser.extract_sections(optimized_content)
        
        # Reorganize sections in a logical order
        final_sections = self._reorganize_sections(sections)
        
        # Apply final formatting
        final_resume = self._apply_final_formatting(final_sections)
        
        # Validate ATS compatibility
        self._validate_ats_compatibility(final_resume)
        
        return final_resume
    
    def _reorganize_sections(self, sections: Dict[str, str]) -> Dict[str, str]:
        """
        Reorganize resume sections in optimal order
        
        Args:
            sections: Dictionary of resume sections
            
        Returns:
            Reorganized sections
        """
        # Define optimal section order
        section_order = [
            'contact_info',
            'summary',
            'experience',
            'education',
            'skills',
            'projects',
            'certifications'
        ]
        
        reorganized = {}
        for section in section_order:
            if sections.get(section):
                reorganized[section] = sections[section]
        
        return reorganized
    
    def _apply_final_formatting(self, sections: Dict[str, str]) -> str:
        """
        Apply final formatting to resume sections
        
        Args:
            sections: Organized resume sections
            
        Returns:
            Formatted resume content
        """
        formatted_resume = ""
        
        # Section headers mapping
        section_headers = {
            'contact_info': 'CONTACT INFORMATION',
            'summary': 'PROFESSIONAL SUMMARY',
            'experience': 'PROFESSIONAL EXPERIENCE',
            'education': 'EDUCATION',
            'skills': 'TECHNICAL SKILLS',
            'projects': 'PROJECTS',
            'certifications': 'CERTIFICATIONS'
        }
        
        for section_key, section_content in sections.items():
            if section_content.strip():
                header = section_headers.get(section_key, section_key.upper().replace('_', ' '))
                formatted_resume += f"\n{header}\n"
                formatted_resume += "=" * len(header) + "\n\n"
                formatted_resume += self._format_section_content(section_content, section_key)
                formatted_resume += "\n"
        
        return formatted_resume.strip()
    
    def _format_section_content(self, content: str, section_type: str) -> str:
        """
        Format content based on section type
        
        Args:
            content: Section content
            section_type: Type of section
            
        Returns:
            Formatted section content
        """
        if section_type == 'experience':
            return self._format_experience_section(content)
        elif section_type == 'skills':
            return self._format_skills_section(content)
        elif section_type == 'education':
            return self._format_education_section(content)
        else:
            return self._format_general_section(content)
    
    def _format_experience_section(self, content: str) -> str:
        """Format experience section with proper structure"""
        lines = content.split('\n')
        formatted = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line contains job title/company pattern
            if re.match(r'^[A-Z][^a-z]*$', line) or 'at ' in line.lower():
                formatted += f"\n{line}\n"
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                formatted += f"  {line}\n"
            else:
                formatted += f"{line}\n"
        
        return formatted
    
    def _format_skills_section(self, content: str) -> str:
        """Format skills section as comma-separated list"""
        # Extract skills and format as list
        skills = re.findall(r'\b[A-Za-z][A-Za-z\s&/]+[A-Za-z]\b', content)
        if skills:
            return ', '.join(skills[:20])  # Limit to 20 skills
        return content
    
    def _format_education_section(self, content: str) -> str:
        """Format education section"""
        return content  # Keep as is for now
    
    def _format_general_section(self, content: str) -> str:
        """Format general sections"""
        return content
    
    def _validate_ats_compatibility(self, resume_content: str) -> None:
        """
        Validate ATS compatibility of the resume
        
        Args:
            resume_content: Resume content to validate
            
        Raises:
            Exception: If resume is not ATS-compatible
        """
        # Check for common ATS issues
        issues = []
        
        # Check for excessive special characters
        special_char_count = len(re.findall(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\/\\]', resume_content))
        if special_char_count > len(resume_content) * 0.05:  # More than 5% special chars
            issues.append("Too many special characters")
        
        # Check for proper section headers
        section_headers = ['CONTACT', 'SUMMARY', 'EXPERIENCE', 'EDUCATION', 'SKILLS']
        found_headers = sum(1 for header in section_headers if header in resume_content.upper())
        if found_headers < 3:
            issues.append("Missing essential section headers")
        
        # Check for reasonable length
        if len(resume_content) < 500:
            issues.append("Resume too short")
        elif len(resume_content) > 5000:
            issues.append("Resume too long")
        
        if issues:
            # Log issues but don't fail - just warn
            print(f"ATS compatibility warnings: {', '.join(issues)}")
    
    def get_optimization_metadata(self, original: str, optimized: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate metadata about the optimization process
        
        Args:
            original: Original resume content
            optimized: Optimized resume content
            analysis: Analysis results
            
        Returns:
            Metadata dictionary
        """
        return {
            "original_length": len(original),
            "optimized_length": len(optimized),
            "length_change": len(optimized) - len(original),
            "skills_match": analysis.get("skills_match_percentage", 0),
            "experience_match": analysis.get("experience_match_percentage", 0),
            "ats_score": analysis.get("ats_score", 0),
            "keywords_added": len(analysis.get("keyword_density", {}).get("missing_keywords", [])),
            "suggestions_applied": len(analysis.get("suggestions", []))
        }