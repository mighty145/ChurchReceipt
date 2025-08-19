
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
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    run_minimal_server()
