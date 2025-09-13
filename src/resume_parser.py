"""
Resume Parser Module
Handles parsing of different resume file formats (PDF, DOCX, TXT)
"""

import io
import re
from typing import Union
import PyPDF2
from docx import Document
from fastapi import UploadFile

class ResumeParser:
    """Parser for different resume file formats"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'txt']
    
    async def parse_file(self, file: UploadFile, file_extension: str) -> str:
        """
        Parse resume file based on its extension
        
        Args:
            file: Uploaded file object
            file_extension: File extension (pdf, docx, txt)
            
        Returns:
            Extracted text content
        """
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Read file content
        content = await file.read()
        
        if file_extension == 'pdf':
            return self._parse_pdf(content)
        elif file_extension == 'docx':
            return self._parse_docx(content)
        elif file_extension == 'txt':
            return self._parse_txt(content)
    
    def _parse_pdf(self, content: bytes) -> str:
        """Parse PDF file content"""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return self._clean_text(text)
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, content: bytes) -> str:
        """Parse DOCX file content"""
        try:
            doc_file = io.BytesIO(content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self._clean_text(text)
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
    
    def _parse_txt(self, content: bytes) -> str:
        """Parse TXT file content"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    text = content.decode(encoding)
                    return self._clean_text(text)
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            text = content.decode('utf-8', errors='replace')
            return self._clean_text(text)
        except Exception as e:
            raise ValueError(f"Error parsing TXT: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\/\\]', '', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_sections(self, resume_text: str) -> dict:
        """
        Extract different sections from resume text
        
        Args:
            resume_text: Clean resume text
            
        Returns:
            Dictionary with extracted sections
        """
        sections = {
            'contact_info': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': '',
            'certifications': ''
        }
        
        # Common section headers
        section_patterns = {
            'contact_info': r'(?i)(contact|personal|info)',
            'summary': r'(?i)(summary|profile|objective|about)',
            'experience': r'(?i)(experience|work\s+history|employment|career)',
            'education': r'(?i)(education|academic|qualification)',
            'skills': r'(?i)(skills|technical\s+skills|competencies)',
            'projects': r'(?i)(projects|portfolio|work\s+samples)',
            'certifications': r'(?i)(certifications|certificates|licenses)'
        }
        
        lines = resume_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line):
                    current_section = section
                    sections[section] = line + '\n'
                    break
            else:
                # Add line to current section
                if current_section:
                    sections[current_section] += line + '\n'
        
        # Clean up sections
        for section in sections:
            sections[section] = sections[section].strip()
        
        return sections