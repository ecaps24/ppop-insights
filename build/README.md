# PPOP Insights - Static Build

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

Built: 2025-09-06 08:30:01