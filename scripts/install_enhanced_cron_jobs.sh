#!/bin/bash

# Enhanced Cron Jobs Installation with Email Notifications
# Installs scheduled scrapers with comprehensive logging and email alerts

SCRIPT_DIR="/home/ecaps24/dev/ppop-insights/scripts"
LOG_DIR="/home/ecaps24/dev/ppop-insights/logs"

echo "🕐 Setting up enhanced automated scraper scheduling..."
echo "📧 Email notifications will be sent to: edwin.f.capidos@gmail.com"
echo ""

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Remove old cron jobs for PPOP Insights
echo "🧹 Cleaning up old cron jobs..."
crontab -l 2>/dev/null | grep -v "ppop-insights" | grep -v "SB19 & BINI" | crontab - 2>/dev/null || true

# Create new enhanced cron jobs
echo "📅 Installing enhanced cron jobs..."

# Create temporary crontab file
TEMP_CRON=$(mktemp)

# Add existing non-PPOP cron jobs
crontab -l 2>/dev/null | grep -v "ppop-insights" | grep -v "SB19 & BINI" > "$TEMP_CRON" 2>/dev/null || true

# Add enhanced PPOP Insights cron jobs
cat >> "$TEMP_CRON" << 'EOF'

# PPOP Insights - Enhanced Scrapers with Email Notifications
# Generated automatically - do not edit manually

# Monthly listeners scraper - runs daily at 8:00 AM
0 8 * * * /home/ecaps24/dev/ppop-insights/scripts/run_scheduled_scrapers_enhanced.sh monthly >> /home/ecaps24/dev/ppop-insights/logs/cron_monthly.log 2>&1

# Comprehensive streams scraper - runs weekly on Sunday at 9:00 AM  
0 9 * * 0 /home/ecaps24/dev/ppop-insights/scripts/run_scheduled_scrapers_enhanced.sh comprehensive >> /home/ecaps24/dev/ppop-insights/logs/cron_comprehensive.log 2>&1

# Cloud sync after data collection - runs daily at 8:30 AM
30 8 * * * /home/ecaps24/dev/ppop-insights/scripts/sync_to_cloud.sh >> /home/ecaps24/dev/ppop-insights/logs/cloud_sync.log 2>&1

EOF

# Install the new crontab
crontab "$TEMP_CRON"
rm -f "$TEMP_CRON"

echo "✅ Enhanced cron jobs installed successfully!"
echo ""
echo "📊 Enhanced Schedule Summary:"
echo "   • Monthly listeners: Daily at 8:00 AM (with email alerts)"
echo "   • Comprehensive streams: Weekly on Sunday at 9:00 AM (with email alerts)"
echo "   • Cloud sync: Daily at 8:30 AM"
echo ""
echo "📧 Email Features:"
echo "   • Detailed success/failure reports"
echo "   • Performance statistics"
echo "   • Error details and troubleshooting"
echo "   • Sent to: edwin.f.capidos@gmail.com"
echo ""
echo "📂 Enhanced Log Files:"
echo "   • Daily timestamped logs: $LOG_DIR/[scraper]_YYYYMMDD.log"
echo "   • Cron execution logs: $LOG_DIR/cron_[scraper].log"
echo "   • Statistics JSON: $LOG_DIR/[scraper]_stats.json"
echo ""
echo "🔧 Manual Commands:"
echo "   • Test enhanced monthly: $SCRIPT_DIR/run_scheduled_scrapers_enhanced.sh monthly"
echo "   • Test enhanced comprehensive: $SCRIPT_DIR/run_scheduled_scrapers_enhanced.sh comprehensive"
echo "   • Test both: $SCRIPT_DIR/run_scheduled_scrapers_enhanced.sh both"
echo "   • Setup email: $SCRIPT_DIR/setup_email.sh"
echo "   • View cron jobs: crontab -l"
echo ""

# Check if email is configured
if [ -z "$GMAIL_USER" ] || [ -z "$GMAIL_APP_PASSWORD" ]; then
    echo "⚠️  EMAIL SETUP REQUIRED"
    echo "   Email notifications are not yet configured."
    echo "   Run the following command to set up email alerts:"
    echo "   $SCRIPT_DIR/setup_email.sh"
    echo ""
else
    echo "✅ Email notifications are configured and ready!"
    echo "   Gmail User: $GMAIL_USER"
    echo "   Recipient: edwin.f.capidos@gmail.com"
    echo ""
fi

echo "🚀 Enhanced automation is now active!"
echo "   Next monthly run: Today at 8:00 AM"
echo "   Next comprehensive run: Next Sunday at 9:00 AM"