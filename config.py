import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the resume optimization system."""
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = ["pdf", "docx", "txt"]
    
    # Gemini model configuration
    GEMINI_MODEL = "gemini-1.5-flash"
    GENERATION_CONFIG = {
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 4000,
    }
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True