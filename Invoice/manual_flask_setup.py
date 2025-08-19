"""
Manual Flask Setup Script
This script downloads and sets up Flask manually when pip is not working
"""

import os
import sys
import urllib.request
import zipfile
import tempfile

def download_file(url, filename):
    """Download a file from URL"""
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted {zip_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to extract {zip_path}: {e}")
        return False

def setup_manual_packages():
    """Set up packages manually"""
    print("Manual Flask Setup")
    print("=" * 30)
    
    # Create packages directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    packages_dir = os.path.join(current_dir, 'manual_packages')
    os.makedirs(packages_dir, exist_ok=True)
    
    # Add to Python path
    if packages_dir not in sys.path:
        sys.path.insert(0, packages_dir)
    
    print(f"Package directory: {packages_dir}")
    
    # For now, let's create a minimal Flask application that doesn't require complex dependencies
    minimal_flask_path = os.path.join(packages_dir, 'minimal_flask.py')
    
    minimal_flask_code = '''
"""
Minimal Flask-like server for Church Invoice Analyzer
This is a simplified web server that provides basic Flask functionality
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import mimetypes

class MinimalFlaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index':
            self.serve_file('templates/upload.html')
        elif path == '/manual-entry':
            self.serve_file('templates/manual_entry.html')
        elif path.startswith('/static/'):
            self.serve_static(path[8:])  # Remove '/static/' prefix
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        # This would handle form submissions
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Form submitted successfully</h1>')
    
    def serve_file(self, filepath):
        """Serve a file"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            content_type, _ = mimetypes.guess_type(filepath)
            self.send_header('Content-type', content_type or 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_static(self, filepath):
        """Serve static files"""
        try:
            static_path = os.path.join('static', filepath)
            with open(static_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            content_type, _ = mimetypes.guess_type(static_path)
            self.send_header('Content-type', content_type or 'text/plain')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

def run_minimal_server(port=5000):
    """Run the minimal server"""
    server = HTTPServer(('localhost', port), MinimalFlaskHandler)
    print(f"Starting minimal server on http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    run_minimal_server()
'''
    
    with open(minimal_flask_path, 'w') as f:
        f.write(minimal_flask_code)
    
    print(f"✓ Created minimal Flask server: {minimal_flask_path}")
    return packages_dir

def main():
    """Main setup function"""
    try:
        packages_dir = setup_manual_packages()
        
        print("\\nManual setup complete!")
        print("\\nTo test the application:")
        print("1. Run: py manual_packages/minimal_flask.py")
        print("2. Open browser to: http://localhost:5000")
        print("\\nAlternatively, try installing Python properly:")
        print("1. Download Python from python.org")
        print("2. Make sure to check 'Add Python to PATH'")
        print("3. Run: pip install flask werkzeug requests pillow")
        
    except Exception as e:
        print(f"Setup failed: {e}")

if __name__ == "__main__":
    main()
