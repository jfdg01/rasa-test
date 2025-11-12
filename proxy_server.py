#!/usr/bin/env python3
"""
Simple proxy server to forward requests from web server to Rasa API.
This allows the HTML to use the same origin for all requests.
"""
import http.server
import socketserver
import urllib.request
import urllib.parse
import json
from http.server import BaseHTTPRequestHandler

RASA_API_URL = "http://localhost:5005"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests - proxy to Rasa"""
        if self.path.startswith('/webhooks/rest/webhook'):
            # This shouldn't happen for GET, but handle it
            self.send_error(405, "Method Not Allowed")
            return
        
        # Serve static files
        self.serve_static()
    
    def do_POST(self):
        """Handle POST requests - proxy to Rasa API"""
        if self.path.startswith('/webhooks/rest/webhook'):
            try:
                # Read request body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                
                # Forward to Rasa API
                req = urllib.request.Request(
                    f"{RASA_API_URL}{self.path}",
                    data=body,
                    headers={
                        'Content-Type': self.headers.get('Content-Type', 'application/json'),
                        'Content-Length': str(content_length)
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()
                    
                    # Send response back to client
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', str(len(response_data)))
                    self.end_headers()
                    self.wfile.write(response_data)
                    
            except Exception as e:
                self.send_error(500, f"Proxy Error: {str(e)}")
        else:
            self.send_error(404, "Not Found")
    
    def serve_static(self):
        """Serve static files using Python's http.server"""
        import os
        import mimetypes
        
        # Remove query string
        path = urllib.parse.urlparse(self.path).path
        
        # Default to game_ui.html for root
        if path == '/':
            path = '/game_ui.html'
        
        # Security: prevent directory traversal
        if '..' in path:
            self.send_error(403, "Forbidden")
            return
        
        # Get file path
        file_path = os.path.join('.', path.lstrip('/'))
        
        if os.path.isfile(file_path):
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            # Read and serve file
            with open(file_path, 'rb') as f:
                content = f.read()
                
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "File Not Found")
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def run(port=8080):
    """Run the proxy server"""
    with socketserver.TCPServer(("", port), ProxyHandler) as httpd:
        print(f"Proxy server running on port {port}")
        print(f"Proxying Rasa API requests to {RASA_API_URL}")
        httpd.serve_forever()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(port)

