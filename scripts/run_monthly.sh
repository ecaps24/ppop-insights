#!/bin/bash
cd /home/ecaps24/dev/ppop-insights
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting monthly listeners scraper..."
python3 monthly_listeners_simple.py --both --output scheduled_monthly_listeners.csv
echo "$(date '+%Y-%m-%d %H:%M:%S') - Monthly listeners scraper completed."