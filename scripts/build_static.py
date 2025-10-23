#!/usr/bin/env python3
"""
Build Static Dashboard
Creates a deployable version of the dashboard with embedded data
"""

import os
import shutil
import json
from datetime import datetime

def create_static_build():
    """Create static build directory with dashboard and data"""
    
    build_dir = "build"
    
    # Clean and create build directory
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    print("🏗️  Building static dashboard...")
    
    # Copy dashboard files
    shutil.copytree("dashboard", os.path.join(build_dir, "dashboard"))
    
    # Copy data files
    shutil.copytree("data", os.path.join(build_dir, "data"))
    
    # Create build info
    build_info = {
        "build_time": datetime.now().isoformat(),
        "build_type": "static",
        "data_files": {
            "monthly_listeners": "data/historical/monthly_listeners.csv",
            "comprehensive_streams": "data/historical/comprehensive_streams.csv"
        }
    }
    
    with open(os.path.join(build_dir, "build-info.json"), 'w') as f:
        json.dump(build_info, f, indent=2)
    
    # Create simple server script for local testing
    server_script = '''#!/usr/bin/env python3
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
        print("\\n🛑 Server stopped")
'''
    
    with open(os.path.join(build_dir, "serve.py"), 'w') as f:
        f.write(server_script)
    
    os.chmod(os.path.join(build_dir, "serve.py"), 0o755)
    
    # Create deployment README
    readme_content = """# PPOP Insights - Static Build

This is a static build of your PPOP Insights dashboard.

## Local Testing
```bash
python3 serve.py
```

## Deploy to Hosting Platforms

### Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Follow prompts

### Netlify
1. Drag and drop this folder to netlify.com
2. Or use Netlify CLI: `netlify deploy --prod --dir .`

### GitHub Pages
1. Push this build folder to a GitHub repo
2. Enable Pages in repo settings
3. Point to main branch

## Files Included
- `/dashboard/` - Dashboard HTML/CSS/JS
- `/data/` - All CSV data files
- `build-info.json` - Build metadata
- `serve.py` - Local test server

Built: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(os.path.join(build_dir, "README.md"), 'w') as f:
        f.write(readme_content)
    
    # Get directory size
    total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(build_dir)
                    for filename in filenames)
    
    size_mb = total_size / (1024 * 1024)
    
    print(f"✅ Static build complete!")
    print(f"📁 Location: {os.path.abspath(build_dir)}")
    print(f"📊 Size: {size_mb:.1f}MB")
    print(f"🚀 Test locally: cd {build_dir} && python3 serve.py")
    
    return build_dir

if __name__ == "__main__":
    create_static_build()