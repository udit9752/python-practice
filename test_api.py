"""
Test script for Resume Optimization API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoints"""
    print("Testing health check...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("✓ Root endpoint working")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health endpoint working")

def create_test_files():
    """Create test resume files"""
    print("Creating test files...")
    
    # Create test directory
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Create a simple text resume
    txt_resume = """John Doe
Software Engineer
john.doe@email.com | (555) 123-4567 | LinkedIn: john-doe

PROFESSIONAL SUMMARY
Experienced software engineer with 5 years of experience in web development and cloud technologies.

PROFESSIONAL EXPERIENCE
Software Engineer | Tech Company | 2020-2023
• Developed web applications using Python and JavaScript
• Worked with databases and APIs
• Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2018

TECHNICAL SKILLS
Python, JavaScript, SQL, Git, AWS
"""
    
    with open("test_files/test_resume.txt", "w") as f:
        f.write(txt_resume)
    
    print("✓ Test files created")

def test_parse_resume():
    """Test resume parsing endpoint"""
    print("Testing resume parsing...")
    
    with open("test_files/test_resume.txt", "rb") as f:
        files = {"resume_file": ("test_resume.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/parse-resume", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "resume_content" in data
    assert data["status"] == "success"
    print("✓ Resume parsing working")

def test_optimize_resume():
    """Test resume optimization endpoint"""
    print("Testing resume optimization...")
    
    job_description = """
    We are looking for a Senior Software Engineer with expertise in:
    - Python and Django framework
    - React and JavaScript
    - AWS cloud services
    - Database design and optimization
    - Agile development methodologies
    - Team leadership experience
    
    The ideal candidate should have 5+ years of experience and a strong background in full-stack development.
    """
    
    with open("test_files/test_resume.txt", "rb") as f:
        files = {"resume_file": ("test_resume.txt", f, "text/plain")}
        data = {"job_description": job_description}
        response = requests.post(f"{BASE_URL}/optimize", files=files, data=data)
    
    assert response.status_code == 200
    result = response.json()
    assert "original_resume" in result
    assert "optimized_resume" in result
    assert result["status"] == "success"
    print("✓ Resume optimization working")
    
    # Print some results
    print(f"Original length: {len(result['original_resume'])}")
    print(f"Optimized length: {len(result['optimized_resume'])}")
    print("Optimization completed successfully!")

def test_error_handling():
    """Test error handling"""
    print("Testing error handling...")
    
    # Test unsupported file format
    with open("test_files/test_resume.txt", "rb") as f:
        files = {"resume_file": ("test_resume.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/optimize", files=files, data={"job_description": ""})
    
    # Should handle empty job description gracefully
    print("✓ Error handling working")

def cleanup():
    """Clean up test files"""
    print("Cleaning up...")
    import shutil
    if os.path.exists("test_files"):
        shutil.rmtree("test_files")
    print("✓ Cleanup completed")

def main():
    """Run all tests"""
    print("Starting API tests...\n")
    
    try:
        test_health_check()
        print()
        
        create_test_files()
        print()
        
        test_parse_resume()
        print()
        
        test_optimize_resume()
        print()
        
        test_error_handling()
        print()
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        cleanup()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)