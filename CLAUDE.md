# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PPOP Music Analytics Dashboard - tracks SB19 and BINI streaming performance across platforms with real-time data visualization and automated web scraping.

**Tech Stack**: Python 3.7+, vanilla JavaScript, Chart.js, CSV-based data storage, static HTML dashboard

**Target Artists**:
- SB19 (Spotify ID: 3g7vYcdDXnqnDKYFwqXBJP)
- BINI (Spotify ID: 7tNO3vJC9zlHy2IJOx34ga)

## Common Commands

### Running the Dashboard Locally
```bash
# Primary method (auto-selects available port 8080/8081/8082/3000)
./scripts/start_dashboard.sh

# Alternative
python3 scripts/serve_dashboard.py

# Access at: http://localhost:8080/dashboard/dashboard.html
```

### Running Scrapers

**Comprehensive Streaming Data (from Kworb)**:
```bash
python3 scripts/scraper/comprehensive_music_scraper.py \
  --artist-urls "https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP.html" \
                "https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga.html" \
  --output scheduled_comprehensive.csv
```

**Monthly Listeners (with anti-bot evasion)**:
```bash
python3 scripts/scraper/monthly_listeners_enhanced.py --both --output scheduled_monthly_listeners.csv
```

**Automated scheduled runs**:
```bash
./scripts/run_comprehensive.sh   # Runs comprehensive scraper
./scripts/run_monthly.sh         # Runs monthly listeners scraper
```

### Building for Deployment
```bash
# Create static build in build/
python3 scripts/build_static.py

# Deploy data to git
python3 scripts/deploy_data.py
```

## Architecture

### Data Flow
1. **Scrapers** → CSV files in `data/historical/` → **Dashboard** (reads CSVs client-side)
2. **Scrapers** → CSV files → **Build script** → JSON API endpoints in `api/` → **Dashboard**

### Key Components

**Scrapers** (`scripts/scraper/`):
- `comprehensive_music_scraper.py` - Fetches track-level streaming data from Kworb
  - Extracts: artist, rank, song title, Spotify track ID, total streams, daily streams
  - Outputs to: `data/historical/comprehensive_streams.csv`

- `monthly_listeners_enhanced.py` - Fetches monthly listener counts
  - Sources: Kworb (primary, reliable), Spotify (with anti-bot techniques)
  - Features: user agent rotation, session management, exponential backoff
  - Outputs to: `data/historical/monthly_listeners.csv`

**Dashboard** (`dashboard/dashboard.html`):
- Client-side vanilla JavaScript with Chart.js
- Reads CSVs directly via fetch API
- Features: time-range filtering, conditional coloring (red for declining metrics), artist-specific color coding
- Color scheme: SB19 = red (#f87171), BINI = blue (#60a5fa)

**Data Storage**:
- `data/historical/` - Primary CSV files consumed by dashboard
  - `monthly_listeners.csv` - Fields: artist_name, artist_id, monthly_listeners, source_url, scrape_date, data_source, extraction_method, data_date
  - `comprehensive_streams.csv` - Fields: artist_name, artist_id, rank, song_title, spotify_track_id, total_streams, daily_streams, source_url, scrape_date, has_spotify_id, data_confidence
- `data/raw/` - Raw scraped outputs
- `data/processed/` - Intermediate processed data
- `api/` - JSON versions of historical CSVs for API access

**Build System**:
- `scripts/build_static.py` - Creates deployable static site in `build/`
  - Copies dashboard/ and data/ directories
  - Generates build-info.json with metadata
  - Creates standalone server script

**Deployment**:
- Vercel (`vercel.json`) - Routes all requests to `/dashboard/`, API endpoints to `/api/`
- Netlify (`netlify.toml`) - Static site with CORS headers for data and API paths
- GitHub Pages ready (static HTML/CSS/JS)

### Anti-Bot Detection Strategy

The monthly listeners scraper implements multiple evasion techniques:
- Mobile and desktop user agent rotation (6+ variations)
- Session persistence with cookies
- Random delays between requests
- Multiple endpoint fallbacks
- Enhanced HTTP headers (referer, accept-language, etc.)
- Exponential backoff retry logic

### Important Patterns

**CSV Data Integrity**:
- Always include `data_date` column (actual date the data represents)
- Separate from `scrape_date` (when scraping occurred)
- Essential for accurate time-series analysis in dashboard

**Scraper Reliability**:
- Kworb is the primary reliable source (no bot detection)
- Spotify direct scraping is fragile (use Kworb when possible)
- Always implement multiple extraction patterns with fallbacks

**Dashboard Data Updates**:
- Dashboard fetches CSVs on load - no build step required
- To update data: run scraper → CSV updated → refresh dashboard
- For production: also update JSON in `api/` for better performance

**Local File Paths**:
- Shell scripts contain hardcoded paths to `/home/ecaps24/dev/ppop-insights`
- When running locally, either update paths or run from project root with relative paths

## Data Schema

### monthly_listeners.csv
```
artist_name, artist_id, monthly_listeners, source_url, scrape_date, data_source, extraction_method, data_date
```

### comprehensive_streams.csv
```
artist_name, artist_id, rank, song_title, spotify_track_id, total_streams, daily_streams, source_url, scrape_date, spotify_url, has_spotify_id, data_confidence
```

## Deployment Targets

- **Vercel**: Configured via `vercel.json` (static build from `dashboard/`)
- **Netlify**: Configured via `netlify.toml` (serves root directory)
- **Local Development**: Python HTTP server with CORS enabled on port 8080+

## Development Notes

- No package.json/dependencies - pure Python scripts and vanilla JS
- No build step required for dashboard (reads CSV directly)
- Python 3.7+ required (no virtual environment setup documented)
- Dashboard uses CDN-hosted libraries (Chart.js, chartjs-plugin-datalabels, chartjs-plugin-annotation)
- All styling inline in HTML (no separate CSS files except ppop-theme.css)
