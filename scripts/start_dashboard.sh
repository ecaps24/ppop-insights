#!/bin/bash
cd /home/ecaps24/dev/kworb-scraper

echo "🎵 Starting Music Dashboard..."
echo "📊 Dashboard URL: http://localhost:8080/dashboard/dashboard.html"
echo "🌐 Server will run on port 8080"
echo "💡 Press Ctrl+C to stop the server"
echo ""

python3 -c "
import http.server
import socketserver
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

os.chdir('/home/ecaps24/dev/kworb-scraper')

# Try different ports
for port in [8080, 8081, 8082, 3000]:
    try:
        with socketserver.TCPServer(('', port), CORSRequestHandler) as httpd:
            print(f'✅ Dashboard server started on port {port}!')
            print(f'🚀 Open http://localhost:{port}/dashboard/dashboard.html in your browser')
            print('')
            httpd.serve_forever()
            break
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f'Port {port} in use, trying next...')
            continue
        else:
            print(f'Error: {e}')
            break
    except KeyboardInterrupt:
        print('\n🛑 Dashboard server stopped.')
        break
"
