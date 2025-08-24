#!/bin/bash
# Scheduled Scrapers Runner Script
# This script runs both scrapers with proper logging

# Set working directory
cd /home/ecaps24/dev/kworb-scraper

# Function to log with timestamp
log_with_timestamp() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Run Monthly Listeners Scraper
run_monthly_listeners() {
    log_with_timestamp "Starting monthly listeners scraper..."
    python3 monthly_listeners_simple.py --both --output scheduled_monthly_listeners.csv
    log_with_timestamp "Monthly listeners scraper completed."
}

# Run Comprehensive Songs/Streams Scraper
run_comprehensive_scraper() {
    log_with_timestamp "Starting comprehensive songs/streams scraper..."
    python3 comprehensive_music_scraper.py \
        --artist-urls \
        "https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP_songs.html" \
        "https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga_songs.html" \
        --output scheduled_comprehensive.csv
    log_with_timestamp "Comprehensive scraper completed."
}

# Check command line argument
case "$1" in
    "monthly")
        run_monthly_listeners
        ;;
    "comprehensive")
        run_comprehensive_scraper
        ;;
    "both")
        run_monthly_listeners
        echo ""
        run_comprehensive_scraper
        ;;
    *)
        echo "Usage: $0 {monthly|comprehensive|both}"
        exit 1
        ;;
esac