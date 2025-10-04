#!/usr/bin/env python3
"""
Deploy Data to Remote Sources
Automatically uploads fresh data to GitHub, S3, or other cloud storage
"""

import os
import subprocess
import json
from datetime import datetime
import argparse

class DataDeployer:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def deploy_to_github(self, repo_url=None):
        """Deploy data files to GitHub repository"""
        print("🚀 Deploying data to GitHub...")
        
        # Check if we're in a git repo
        try:
            subprocess.run(['git', 'status'], check=True, capture_output=True)
            in_git_repo = True
        except:
            in_git_repo = False
            
        if not in_git_repo:
            print("❌ Not in a git repository. Initialize with:")
            print("   git init")
            print("   git remote add origin <your-repo-url>")
            return False
        
        # Add data files
        data_files = [
            'data/historical/monthly_listeners.csv',
            'data/historical/comprehensive_streams.csv',
            'data/processed/',
            'dashboard/'
        ]
        
        for file in data_files:
            if os.path.exists(file):
                subprocess.run(['git', 'add', file])
        
        # Commit changes
        commit_message = f"📊 Data update {self.timestamp}"
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
            print(f"✅ Data pushed to GitHub!")
            return True
        except subprocess.CalledProcessError:
            print("❌ No changes to commit or push failed")
            return False
    
    def create_data_api(self):
        """Create a simple JSON API endpoint from CSV data"""
        print("🔗 Creating data API endpoints...")
        
        api_dir = "api"
        if not os.path.exists(api_dir):
            os.makedirs(api_dir)
        
        # Convert CSV to JSON for API consumption
        import csv
        
        # Monthly listeners API
        monthly_data = []
        csv_file = 'data/historical/monthly_listeners.csv'
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                monthly_data = list(reader)
        
        api_response = {
            "status": "success",
            "last_updated": datetime.now().isoformat(),
            "data": monthly_data,
            "total_records": len(monthly_data)
        }
        
        with open(os.path.join(api_dir, 'monthly-listeners.json'), 'w') as f:
            json.dump(api_response, f, indent=2)
        
        # Comprehensive streams API
        streams_data = []
        csv_file = 'data/historical/comprehensive_streams.csv'
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                streams_data = list(reader)
        
        api_response = {
            "status": "success", 
            "last_updated": datetime.now().isoformat(),
            "data": streams_data,
            "total_records": len(streams_data)
        }
        
        with open(os.path.join(api_dir, 'comprehensive-streams.json'), 'w') as f:
            json.dump(api_response, f, indent=2)
        
        print(f"✅ API files created in /{api_dir}/")
        return True
    
    def create_deployment_config(self):
        """Create configuration files for various platforms"""
        print("⚙️  Creating deployment configurations...")
        
        # Vercel configuration
        vercel_config = {
            "version": 2,
            "name": "ppop-insights",
            "builds": [
                {
                    "src": "dashboard/**",
                    "use": "@vercel/static"
                }
            ],
            "routes": [
                {
                    "src": "/api/(.*)",
                    "dest": "/api/$1"
                },
                {
                    "src": "/(.*)",
                    "dest": "/dashboard/$1"
                }
            ]
        }
        
        with open('vercel.json', 'w') as f:
            json.dump(vercel_config, f, indent=2)
        
        # Netlify configuration  
        netlify_config = """[build]
  publish = "."
  command = "echo 'Static site ready'"

[[headers]]
  for = "/data/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Content-Type = "application/json"
"""
        
        with open('netlify.toml', 'w') as f:
            f.write(netlify_config)
        
        print("✅ Deployment configs created (vercel.json, netlify.toml)")

def main():
    parser = argparse.ArgumentParser(description='Deploy PPOP Insights data')
    parser.add_argument('--github', action='store_true', help='Deploy to GitHub')
    parser.add_argument('--api', action='store_true', help='Create JSON API files')
    parser.add_argument('--config', action='store_true', help='Create deployment configs')
    parser.add_argument('--all', action='store_true', help='Run all deployment tasks')
    
    args = parser.parse_args()
    
    deployer = DataDeployer()
    
    if args.all:
        deployer.create_data_api()
        deployer.create_deployment_config() 
        deployer.deploy_to_github()
    else:
        if args.api:
            deployer.create_data_api()
        if args.config:
            deployer.create_deployment_config()
        if args.github:
            deployer.deploy_to_github()
    
    if not any([args.github, args.api, args.config, args.all]):
        print("Usage: python3 deploy_data.py [--github] [--api] [--config] [--all]")

if __name__ == "__main__":
    main()