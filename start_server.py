#!/usr/bin/env python3
"""
Startup script for the Resume Optimization Backend System.
"""

import os
import sys
import uvicorn
from config import Config

def check_requirements():
    """Check if all requirements are met before starting."""
    print("Checking system requirements...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found. Please create one with your GEMINI_API_KEY")
        print("   You can copy .env.example to .env and add your API key")
    
    # Check API key
    try:
        Config.validate_config()
        print("✓ Configuration validated successfully")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("   Please set your GEMINI_API_KEY in the .env file")
        return False
    
    # Check if required modules can be imported
    try:
        import fastapi
        import google.generativeai
        import PyPDF2
        import docx
        print("✓ All required packages are installed")
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main startup function."""
    print("Resume Optimization Backend System")
    print("=" * 40)
    
    if not check_requirements():
        print("\n❌ System requirements not met. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting the server...")
    print("   API will be available at: http://localhost:8000")
    print("   API documentation at: http://localhost:8000/docs")
    print("   Health check at: http://localhost:8000/health")
    print("\n   Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()