#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting enhanced monthly listeners scraper (Spotify + Kworb only)..."
python3 scripts/scraper/monthly_listeners_enhanced.py --both --output scheduled_monthly_listeners.csv
echo "$(date '+%Y-%m-%d %H:%M:%S') - Monthly listeners scraper completed."