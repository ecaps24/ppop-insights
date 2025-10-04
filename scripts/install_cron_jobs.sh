#!/bin/bash
# Install Cron Jobs for Automated Scraping

echo "🕐 Setting up automated scraper scheduling..."

# Create the cron entries
CRON_FILE="/tmp/scraper_crons"

cat > $CRON_FILE << 'EOF'
# SB19 & BINI Music Data Scrapers - Auto-generated
# Monthly listeners scraper - runs daily at 8:00 AM
0 8 * * * /home/ecaps24/dev/ppop-insights/scripts/run_scheduled_scrapers.sh monthly >> /home/ecaps24/dev/ppop-insights/logs/monthly_listeners.log 2>&1

# Comprehensive songs/streams scraper - runs weekly on Sunday at 9:00 AM
0 9 * * 0 /home/ecaps24/dev/ppop-insights/scripts/run_scheduled_scrapers.sh comprehensive >> /home/ecaps24/dev/ppop-insights/logs/comprehensive.log 2>&1
EOF

# Install the cron jobs
echo "📅 Installing cron jobs..."
crontab -l 2>/dev/null | grep -v "SB19 & BINI Music Data Scrapers" > /tmp/existing_crons 2>/dev/null || touch /tmp/existing_crons
cat /tmp/existing_crons $CRON_FILE | crontab -

echo "✅ Cron jobs installed successfully!"
echo ""
echo "📊 Schedule Summary:"
echo "   • Monthly listeners: Daily at 8:00 AM"
echo "   • Songs/streams: Weekly on Sunday at 9:00 AM"
echo ""
echo "📂 Output files:"
echo "   • scheduled_monthly_listeners.csv"
echo "   • scheduled_comprehensive.csv"
echo ""
echo "📝 Log files:"
echo "   • logs/monthly_listeners.log"
echo "   • logs/comprehensive.log"
echo ""
echo "🔧 Manual commands:"
echo "   • Test monthly: ./run_scheduled_scrapers.sh monthly"
echo "   • Test comprehensive: ./run_scheduled_scrapers.sh comprehensive"
echo "   • View cron jobs: crontab -l"
echo "   • Edit cron jobs: crontab -e"

# Clean up temp files
rm -f $CRON_FILE /tmp/existing_crons