import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ATSOptimizer:
    """Handles ATS-specific optimizations and formatting for resumes."""
    
    def __init__(self):
        """Initialize ATS optimizer with formatting rules."""
        self.ats_section_headers = {
            'contact': ['Contact Information', 'Contact Details', 'Personal Information'],
            'summary': ['Professional Summary', 'Summary', 'Profile', 'Objective'],
            'experience': ['Work Experience', 'Professional Experience', 'Employment History', 'Experience'],
            'education': ['Education', 'Educational Background', 'Academic Background'],
            'skills': ['Skills', 'Technical Skills', 'Core Competencies', 'Key Skills'],
            'projects': ['Projects', 'Key Projects', 'Notable Projects'],
            'certifications': ['Certifications', 'Certificates', 'Professional Certifications'],
            'achievements': ['Achievements', 'Awards', 'Accomplishments']
        }
    
    def optimize_for_ats(self, resume_text: str) -> str:
        """
        Apply comprehensive ATS optimizations to resume text.
        
        Args:
            resume_text: The resume text to optimize
            
        Returns:
            ATS-optimized resume text
        """
        try:
            # Step 1: Clean and normalize text
            optimized_text = self._clean_text(resume_text)
            
            # Step 2: Standardize section headers
            optimized_text = self._standardize_section_headers(optimized_text)
            
            # Step 3: Format dates consistently
            optimized_text = self._standardize_dates(optimized_text)
            
            # Step 4: Clean up bullet points and formatting
            optimized_text = self._optimize_bullet_points(optimized_text)
            
            # Step 5: Remove problematic characters and formatting
            optimized_text = self._remove_problematic_formatting(optimized_text)
            
            # Step 6: Ensure proper line spacing and structure
            optimized_text = self._optimize_spacing(optimized_text)
            
            logger.info("ATS optimization completed successfully")
            return optimized_text
            
        except Exception as e:
            logger.error(f"Error during ATS optimization: {str(e)}")
            # Return original text if optimization fails
            return resume_text
    
    def _clean_text(self, text: str) -> str:
        """Remove unnecessary characters and normalize whitespace."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that can cause ATS issues
        problematic_chars = ['•', '◦', '▪', '▫', '■', '□', '★', '☆']
        for char in problematic_chars:
            text = text.replace(char, '•')
        
        # Normalize line breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        return text.strip()
    
    def _standardize_section_headers(self, text: str) -> str:
        """Standardize section headers to ATS-friendly formats."""
        lines = text.split('\n')
        standardized_lines = []
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                standardized_lines.append(line)
                continue
            
            # Check if line might be a section header
            if self._is_potential_header(line_clean):
                standardized_header = self._get_standard_header(line_clean)
                if standardized_header:
                    standardized_lines.append(standardized_header.upper())
                else:
                    standardized_lines.append(line)
            else:
                standardized_lines.append(line)
        
        return '\n'.join(standardized_lines)
    
    def _is_potential_header(self, line: str) -> bool:
        """Check if a line might be a section header."""
        # Headers are typically short, may be in caps, and don't contain common resume content
        if len(line) > 50:
            return False
        
        # Check for common header patterns
        header_patterns = [
            r'^[A-Z\s]+$',  # All caps
            r'^[A-Z][a-z\s]+$',  # Title case
            r'^\w+(\s+\w+)*:?$'  # Simple word patterns
        ]
        
        return any(re.match(pattern, line) for pattern in header_patterns)
    
    def _get_standard_header(self, line: str) -> str:
        """Get standardized header for a given line."""
        line_lower = line.lower().strip(':')
        
        # Map to standard headers
        header_mapping = {
            'contact': 'CONTACT INFORMATION',
            'summary': 'PROFESSIONAL SUMMARY',
            'experience': 'WORK EXPERIENCE',
            'education': 'EDUCATION',
            'skills': 'SKILLS',
            'projects': 'PROJECTS',
            'certifications': 'CERTIFICATIONS',
            'achievements': 'ACHIEVEMENTS'
        }
        
        for category, standard_header in header_mapping.items():
            if any(keyword in line_lower for keyword in [category] + 
                   [h.lower() for h in self.ats_section_headers.get(category, [])]):
                return standard_header
        
        return None
    
    def _standardize_dates(self, text: str) -> str:
        """Standardize date formats throughout the resume."""
        # Common date patterns and their standardized formats
        date_patterns = [
            (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', r'\3-\1-\2'),  # MM/DD/YYYY to YYYY-MM-DD
            (r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b', r'\1-\2-\3'),  # Keep YYYY-MM-DD
            (r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})\b', r'\1 \2'),  # Month YYYY
            (r'\b(\d{1,2})/(\d{4})\b', r'\2-\1'),  # MM/YYYY to YYYY-MM
        ]
        
        for pattern, replacement in date_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _optimize_bullet_points(self, text: str) -> str:
        """Optimize bullet points for ATS readability."""
        lines = text.split('\n')
        optimized_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            
            # Handle bullet points
            if stripped_line.startswith(('•', '-', '*', '◦', '▪')):
                # Standardize to simple bullet
                content = re.sub(r'^[•\-*◦▪]\s*', '', stripped_line)
                optimized_lines.append(f"• {content}")
            elif re.match(r'^\d+\.\s', stripped_line):
                # Keep numbered lists as is
                optimized_lines.append(line)
            else:
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _remove_problematic_formatting(self, text: str) -> str:
        """Remove formatting that can cause ATS parsing issues."""
        # Remove tabs and replace with spaces
        text = text.replace('\t', '    ')
        
        # Remove excessive punctuation
        text = re.sub(r'[^\w\s\-.,()@:/•\n]', '', text)
        
        # Clean up multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        return text
    
    def _optimize_spacing(self, text: str) -> str:
        """Optimize spacing and line breaks for ATS parsing."""
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Ensure sections are properly separated
        lines = text.split('\n')
        optimized_lines = []
        
        for i, line in enumerate(lines):
            optimized_lines.append(line)
            
            # Add spacing after section headers
            if (line.strip() and 
                line.strip().isupper() and 
                len(line.strip()) < 50 and
                i < len(lines) - 1 and
                lines[i + 1].strip()):
                optimized_lines.append('')
        
        return '\n'.join(optimized_lines).strip()
    
    def validate_ats_compliance(self, text: str) -> Dict[str, bool]:
        """
        Validate ATS compliance of the resume text.
        
        Args:
            text: Resume text to validate
            
        Returns:
            Dictionary with compliance checks
        """
        checks = {
            'has_standard_sections': self._has_standard_sections(text),
            'proper_formatting': self._has_proper_formatting(text),
            'no_problematic_chars': self._has_no_problematic_chars(text),
            'consistent_dates': self._has_consistent_dates(text),
            'appropriate_length': len(text.split()) >= 100  # At least 100 words
        }
        
        return checks
    
    def _has_standard_sections(self, text: str) -> bool:
        """Check if resume has standard ATS-friendly sections."""
        required_sections = ['experience', 'education', 'skills']
        text_lower = text.lower()
        
        found_sections = 0
        for section in required_sections:
            if any(keyword in text_lower for keyword in [section] + 
                   [h.lower() for h in self.ats_section_headers.get(section, [])]):
                found_sections += 1
        
        return found_sections >= 2  # At least 2 of 3 required sections
    
    def _has_proper_formatting(self, text: str) -> bool:
        """Check for proper formatting structure."""
        lines = text.split('\n')
        
        # Check for reasonable line count
        if len(lines) < 10:
            return False
        
        # Check for section headers (uppercase lines)
        header_count = sum(1 for line in lines if line.strip() and line.strip().isupper() and len(line.strip()) < 50)
        
        return header_count >= 2
    
    def _has_no_problematic_chars(self, text: str) -> bool:
        """Check for characters that might cause ATS issues."""
        problematic_patterns = [
            r'[^\w\s\-.,()@:/•\n]',  # Special characters
            r'\t',  # Tabs
            r'  {3,}'  # Excessive spaces
        ]
        
        return not any(re.search(pattern, text) for pattern in problematic_patterns)
    
    def _has_consistent_dates(self, text: str) -> bool:
        """Check for consistent date formatting."""
        # This is a simplified check - in practice, you might want more sophisticated validation
        date_formats = [
            r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
            r'\d{4}-\d{1,2}',  # YYYY-MM
            r'[A-Za-z]{3}\s+\d{4}',  # Mon YYYY
        ]
        
        dates_found = []
        for pattern in date_formats:
            dates_found.extend(re.findall(pattern, text))
        
        return len(dates_found) > 0  # At least some dates found