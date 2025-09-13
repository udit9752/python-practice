#!/usr/bin/env python3
"""
Example client script demonstrating how to use the Resume Optimization Backend API.

This script shows how to:
1. Upload a resume file
2. Provide a job description
3. Get an optimized resume back
4. Handle API responses and errors

Usage:
    python3 example_client.py

Make sure the API server is running on http://localhost:8000
"""

import requests
import json
import os
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:8000"
SAMPLE_RESUME_PATH = "sample_resume.txt"
SAMPLE_JD_PATH = "sample_job_description.txt"

def check_api_health():
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✓ API is healthy and running")
            return True
        else:
            print(f"✗ API health check failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"✗ Cannot connect to API: {e}")
        print("Make sure the API server is running with: python3 main.py")
        return False

def get_api_info():
    """Get information about the API capabilities."""
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        if response.status_code == 200:
            info = response.json()
            print("\n=== API Information ===")
            print(f"Supported formats: {info['supported_formats']}")
            print(f"Max file size: {info['max_file_size_mb']}MB")
            print("Features:")
            for feature in info['features']:
                print(f"  • {feature}")
            return True
        else:
            print(f"✗ Failed to get API info: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"✗ Error getting API info: {e}")
        return False

def optimize_resume(resume_path, job_description, include_analysis=False):
    """
    Send resume and job description to the API for optimization.
    
    Args:
        resume_path: Path to the resume file
        job_description: Job description text
        include_analysis: Whether to include detailed analysis
        
    Returns:
        API response or None if failed
    """
    if not os.path.exists(resume_path):
        print(f"✗ Resume file not found: {resume_path}")
        return None
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {'resume_file': resume_file}
            data = {
                'job_description': job_description,
                'include_analysis': include_analysis
            }
            
            print(f"\n=== Optimizing Resume ===")
            print(f"Resume file: {resume_path}")
            print(f"Job description length: {len(job_description)} characters")
            print(f"Include analysis: {include_analysis}")
            print("Sending request to API...")
            
            response = requests.post(
                f"{API_BASE_URL}/optimize",
                files=files,
                data=data,
                timeout=60  # Allow up to 60 seconds for processing
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("✓ Resume optimization completed successfully!")
                    return result
                else:
                    print(f"✗ Optimization failed: {result.get('error', 'Unknown error')}")
                    print(f"Failed at step: {result.get('step', 'Unknown')}")
                    return None
            else:
                print(f"✗ API request failed with status: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    print(f"Response: {response.text}")
                return None
                
    except requests.RequestException as e:
        print(f"✗ Request error: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None

def analyze_resume_only(resume_path, job_description):
    """
    Send resume and job description to the API for analysis only.
    
    Args:
        resume_path: Path to the resume file
        job_description: Job description text
        
    Returns:
        API response or None if failed
    """
    if not os.path.exists(resume_path):
        print(f"✗ Resume file not found: {resume_path}")
        return None
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {'resume_file': resume_file}
            data = {'job_description': job_description}
            
            print(f"\n=== Analyzing Resume ===")
            print("Sending request for analysis...")
            
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                files=files,
                data=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("✓ Resume analysis completed successfully!")
                    return result
                else:
                    print(f"✗ Analysis failed: {result.get('error', 'Unknown error')}")
                    return None
            else:
                print(f"✗ API request failed with status: {response.status_code}")
                return None
                
    except requests.RequestException as e:
        print(f"✗ Request error: {e}")
        return None

def save_optimized_resume(optimized_content, output_path):
    """Save the optimized resume to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
        print(f"✓ Optimized resume saved to: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to save optimized resume: {e}")
        return False

def main():
    """Main function demonstrating the API usage."""
    print("Resume Optimization Backend - Example Client")
    print("=" * 50)
    
    # Check if API is running
    if not check_api_health():
        return 1
    
    # Get API information
    get_api_info()
    
    # Load job description
    if not os.path.exists(SAMPLE_JD_PATH):
        print(f"✗ Sample job description not found: {SAMPLE_JD_PATH}")
        return 1
    
    with open(SAMPLE_JD_PATH, 'r', encoding='utf-8') as f:
        job_description = f.read()
    
    # Example 1: Optimize resume with analysis
    print("\n" + "=" * 50)
    print("EXAMPLE 1: Full Resume Optimization with Analysis")
    print("=" * 50)
    
    result = optimize_resume(SAMPLE_RESUME_PATH, job_description, include_analysis=True)
    
    if result:
        print(f"\nProcessing steps completed:")
        for step in result.get('processing_steps', []):
            print(f"  ✓ {step}")
        
        print(f"\nOriginal format: {result.get('original_format', 'unknown')}")
        
        if result.get('analysis'):
            print(f"\n=== ANALYSIS ===")
            print(result['analysis'][:500] + "..." if len(result['analysis']) > 500 else result['analysis'])
        
        if result.get('optimized_resume'):
            print(f"\n=== OPTIMIZED RESUME (first 500 chars) ===")
            optimized = result['optimized_resume']
            print(optimized[:500] + "..." if len(optimized) > 500 else optimized)
            
            # Save the optimized resume
            output_path = "optimized_resume.txt"
            save_optimized_resume(optimized, output_path)
    
    # Example 2: Analysis only
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Resume Analysis Only")
    print("=" * 50)
    
    analysis_result = analyze_resume_only(SAMPLE_RESUME_PATH, job_description)
    
    if analysis_result and analysis_result.get('analysis'):
        print(f"\n=== ANALYSIS RESULTS ===")
        analysis = analysis_result['analysis']
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
    
    print("\n" + "=" * 50)
    print("✓ Example client completed successfully!")
    print("\nNext steps:")
    print("1. Check the generated 'optimized_resume.txt' file")
    print("2. Modify the sample files to test with your own content")
    print("3. Integrate the API calls into your own application")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    exit(main())