#!/usr/bin/env python3
"""
Simple HTTP Server for Music Dashboard
Serves the dashboard with CORS headers to access CSV files
"""

import http.server
import socketserver
import webbrowser
import os
from urllib.parse import urlparse

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def serve_dashboard(port=8000):
    """Start the dashboard server"""
    os.chdir('/home/ecaps24/dev/ppop-insights')
    
    with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
        print(f"🎵 Music Dashboard Server starting...")
        print(f"📊 Dashboard URL: http://localhost:{port}/dashboard/dashboard.html")
        print(f"🌐 Server running on port {port}")
        print(f"📁 Serving files from: {os.getcwd()}")
        print(f"💡 Press Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{port}/dashboard/dashboard.html')
            print(f"🚀 Opening dashboard in your default browser...")
        except:
            print(f"📝 Please manually open: http://localhost:{port}/dashboard/dashboard.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Dashboard server stopped.")

if __name__ == "__main__":
    serve_dashboard()