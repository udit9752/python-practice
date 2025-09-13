"""
Validation script to ensure the Resume Optimization Backend is properly set up
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'multipart',
        'docx',
        'PyPDF2',
        'google.generativeai',
        'pydantic',
        'dotenv',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        '.env.example',
        'src/__init__.py',
        'src/models.py',
        'src/config.py',
        'src/resume_parser.py',
        'src/gemini_client.py',
        'src/resume_optimizer.py',
        'test_api.py',
        'start.sh'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def check_environment():
    """Check environment configuration"""
    print("\n🔧 Checking environment configuration...")
    
    # Check if .env exists
    if not Path('.env').exists():
        print("⚠️  .env file not found")
        if Path('.env.example').exists():
            print("✅ .env.example exists - you can copy it to .env")
        else:
            print("❌ .env.example is missing")
            return False
    else:
        print("✅ .env file exists")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("⚠️  GEMINI_API_KEY not set in .env file")
            print("   Please edit .env and add your actual API key")
        else:
            print("✅ GEMINI_API_KEY is configured")
        
        port = os.getenv('PORT', '8000')
        host = os.getenv('HOST', '0.0.0.0')
        print(f"✅ Server will run on {host}:{port}")
        
    except Exception as e:
        print(f"❌ Error loading environment: {e}")
        return False
    
    return True

def check_imports():
    """Check if all modules can be imported"""
    print("\n🔍 Checking module imports...")
    
    try:
        from src.config import Config
        print("✅ Config module")
        
        from src.models import OptimizationRequest, OptimizationResponse
        print("✅ Models module")
        
        from src.resume_parser import ResumeParser
        print("✅ Resume parser module")
        
        from src.gemini_client import GeminiClient
        print("✅ Gemini client module")
        
        from src.resume_optimizer import ResumeOptimizer
        print("✅ Resume optimizer module")
        
        print("✅ All modules can be imported")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_configuration():
    """Check if configuration is valid"""
    print("\n⚙️  Checking configuration...")
    
    try:
        from src.config import Config
        Config.validate_config()
        print("✅ Configuration is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🔍 Resume Optimization Backend - Setup Validation")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_file_structure,
        check_environment,
        check_imports,
        check_configuration
    ]
    
    all_passed = True
    
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All checks passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Make sure your GEMINI_API_KEY is set in .env")
        print("2. Run: python main.py")
        print("3. Or run: ./start.sh")
        print("4. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Set up .env file: cp .env.example .env")
        print("- Add your API key to .env file")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)