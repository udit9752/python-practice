#!/usr/bin/env python3
"""
Simple HTTP server to serve the Resume Optimizer frontend.

This script serves the frontend files and handles the development setup.
"""

import os
import sys
import http.server
import socketserver
import webbrowser
import threading
import time
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS headers."""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        frontend_dir = Path(__file__).parent / "frontend"
        os.chdir(frontend_dir)
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests."""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def check_backend_status():
    """Check if the backend API is running."""
    import urllib.request
    import json
    
    try:
        with urllib.request.urlopen('http://localhost:8000/health', timeout=5) as response:
            data = json.loads(response.read())
            return data.get('status') == 'healthy'
    except:
        return False

def start_server(port=8080):
    """Start the frontend server."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if frontend files exist
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    required_files = ['index.html', 'styles.css', 'script.js']
    missing_files = [f for f in required_files if not (frontend_dir / f).exists()]
    
    if missing_files:
        print(f"❌ Missing frontend files: {', '.join(missing_files)}")
        return False
    
    print("🎨 Resume Optimizer Frontend Server")
    print("=" * 40)
    
    # Check backend status
    backend_status = check_backend_status()
    if backend_status:
        print("✅ Backend API is running and healthy")
    else:
        print("⚠️  Backend API is not running!")
        print("   Please start the backend server first:")
        print("   python3 start_server.py")
        print()
    
    try:
        # Create server
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Frontend server starting on port {port}")
            print(f"📱 Frontend URL: http://localhost:{port}")
            print(f"🔗 Backend API: http://localhost:8000")
            print()
            print("📋 Features available:")
            print("   • Resume file upload (PDF, DOCX, TXT)")
            print("   • Job description input")
            print("   • AI-powered optimization")
            print("   • ATS compatibility analysis")
            print("   • Download optimized resume")
            print()
            print("Press Ctrl+C to stop the server")
            print("=" * 40)
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{port}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")
        return True
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print(f"   Try a different port: python3 frontend_server.py --port 8081")
        else:
            print(f"❌ Error starting server: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Resume Optimizer Frontend Server')
    parser.add_argument('--port', type=int, default=8080, 
                       help='Port to serve the frontend (default: 8080)')
    parser.add_argument('--no-browser', action='store_true',
                       help='Don\'t automatically open browser')
    
    args = parser.parse_args()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return 1
    
    success = start_server(args.port)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())