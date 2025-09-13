"""
Configuration module for Resume Optimization API
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = ["pdf", "docx", "txt"]
    
    # Gemini API Configuration
    GEMINI_MODEL: str = "gemini-1.5-flash"
    MAX_TOKENS: int = 8192
    TEMPERATURE: float = 0.7
    
    # Resume Processing Configuration
    MIN_RESUME_LENGTH: int = 100
    MAX_RESUME_LENGTH: int = 10000
    MIN_JD_LENGTH: int = 50
    MAX_JD_LENGTH: int = 5000
    
    # ATS Configuration
    MAX_SPECIAL_CHARS_RATIO: float = 0.05
    MIN_SECTION_HEADERS: int = 3
    REQUIRED_SECTIONS: list = ["CONTACT", "EXPERIENCE", "EDUCATION"]
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate configuration
        
        Returns:
            True if configuration is valid
        """
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError("PORT must be between 1 and 65535")
        
        return True
    
    @classmethod
    def get_upload_config(cls) -> dict:
        """
        Get file upload configuration
        
        Returns:
            Upload configuration dictionary
        """
        return {
            "max_file_size": cls.MAX_FILE_SIZE,
            "allowed_extensions": cls.ALLOWED_EXTENSIONS,
            "min_resume_length": cls.MIN_RESUME_LENGTH,
            "max_resume_length": cls.MAX_RESUME_LENGTH
        }