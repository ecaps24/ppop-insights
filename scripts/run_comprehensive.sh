#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting comprehensive streams scraper (Kworb only)..."
python3 scripts/scraper/comprehensive_music_scraper.py --artist-urls "https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP.html" "https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga.html" --output scheduled_comprehensive.csv
echo "$(date '+%Y-%m-%d %H:%M:%S') - Comprehensive streams scraper completed."