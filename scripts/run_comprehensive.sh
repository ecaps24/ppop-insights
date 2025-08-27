#!/bin/bash
cd /home/ecaps24/dev/ppop-insights
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting comprehensive scraper..."
python3 comprehensive_music_scraper.py --artist-urls "https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP_songs.html" "https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga_songs.html" --output scheduled_comprehensive.csv
echo "$(date '+%Y-%m-%d %H:%M:%S') - Comprehensive scraper completed."