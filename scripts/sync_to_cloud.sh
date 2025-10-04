#!/bin/bash
# Automated Cloud Sync Script
# Runs after data collection to update online dashboard

echo "🌐 Starting cloud data sync..."
echo "📅 $(date '+%Y-%m-%d %H:%M:%S')"

# Change to project directory
cd /home/ecaps24/dev/ppop-insights

# Create API endpoints from fresh data
echo "🔗 Creating JSON API endpoints..."
python3 scripts/deploy_data.py --api

# Build static dashboard with latest data
echo "🏗️  Building static dashboard..."
python3 scripts/build_static.py

# Option 1: Deploy to GitHub (if repo is set up)
if git remote get-url origin >/dev/null 2>&1; then
    echo "📤 Syncing to GitHub..."
    python3 scripts/deploy_data.py --github
fi

# Option 2: Upload to cloud storage (uncomment when configured)
# echo "☁️  Uploading to cloud storage..."
# aws s3 sync build/ s3://your-bucket-name/ --delete
# or
# gsutil -m rsync -r -d build/ gs://your-bucket-name/

# Option 3: Deploy to Vercel (if configured)
# cd build && vercel --prod --yes

# Option 4: Deploy to Netlify (now configured!)
echo "🌐 Deploying to Netlify..."
cd build && npx netlify-cli deploy --prod --dir . --site ppop-insights
cd ..

echo "✅ Cloud sync completed!"
echo "📊 Dashboard updated with latest data"
echo "🔗 API endpoints refreshed"
echo ""