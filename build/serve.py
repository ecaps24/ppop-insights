#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    port = 8080
    try:
        with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
            print(f"🚀 Static dashboard server running on http://localhost:{port}")
            print(f"📊 Open http://localhost:{port}/dashboard/dashboard.html")
            try:
                webbrowser.open(f'http://localhost:{port}/dashboard/dashboard.html')
            except:
                pass
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
