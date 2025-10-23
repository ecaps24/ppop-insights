#!/bin/bash

# Email Setup Script for PPOP Insights
# Sets up Gmail credentials for automated email notifications

echo "📧 PPOP Insights Email Setup"
echo "============================"
echo ""
echo "This script will help you set up email notifications for your scrapers."
echo "You'll receive automated reports sent to: edwin.f.capidos@gmail.com"
echo ""

# Check if credentials already exist
if [ -n "$GMAIL_USER" ] && [ -n "$GMAIL_APP_PASSWORD" ]; then
    echo "✅ Email credentials are already configured!"
    echo "   Gmail User: $GMAIL_USER"
    echo "   App Password: [HIDDEN]"
    echo ""
    read -p "Do you want to update the credentials? (y/N): " update
    if [[ ! $update =~ ^[Yy]$ ]]; then
        echo "Email setup cancelled."
        exit 0
    fi
fi

echo "📋 Setup Instructions:"
echo "1. You'll need a Gmail account with 2-factor authentication enabled"
echo "2. Generate an App Password (not your regular Gmail password)"
echo "3. Visit: https://myaccount.google.com/apppasswords"
echo ""

# Get Gmail credentials
read -p "Enter your Gmail address: " gmail_user
echo "Enter your Gmail App Password (16 characters, no spaces):"
read -s gmail_password
echo ""

# Validate inputs
if [ -z "$gmail_user" ] || [ -z "$gmail_password" ]; then
    echo "❌ Error: Both email and password are required!"
    exit 1
fi

# Check password format (should be 16 characters for app password)
if [ ${#gmail_password} -ne 16 ]; then
    echo "⚠️  Warning: App passwords are typically 16 characters long."
    echo "   Make sure you're using an App Password, not your regular Gmail password."
    echo ""
fi

# Create environment file
ENV_FILE="/home/ecaps24/dev/ppop-insights/.env"
echo "# Email Configuration for PPOP Insights" > "$ENV_FILE"
echo "GMAIL_USER=\"$gmail_user\"" >> "$ENV_FILE"
echo "GMAIL_APP_PASSWORD=\"$gmail_password\"" >> "$ENV_FILE"
chmod 600 "$ENV_FILE"

# Add to bashrc for persistent environment variables
BASHRC_FILE="$HOME/.bashrc"
if ! grep -q "PPOP Insights Email Config" "$BASHRC_FILE"; then
    echo "" >> "$BASHRC_FILE"
    echo "# PPOP Insights Email Config" >> "$BASHRC_FILE"
    echo "export GMAIL_USER=\"$gmail_user\"" >> "$BASHRC_FILE"
    echo "export GMAIL_APP_PASSWORD=\"$gmail_password\"" >> "$BASHRC_FILE"
fi

# Export for current session
export GMAIL_USER="$gmail_user"
export GMAIL_APP_PASSWORD="$gmail_password"

echo "✅ Email credentials saved successfully!"
echo ""
echo "📁 Configuration saved to:"
echo "   • $ENV_FILE (for scripts)"
echo "   • $BASHRC_FILE (for persistent environment)"
echo ""

# Test email functionality
echo "🧪 Testing email functionality..."
python3 - << EOF
import sys
sys.path.append('/home/ecaps24/dev/ppop-insights/scripts')
from enhanced_logging import ScraperLogger

logger = ScraperLogger("email_test")
logger.log_start("Testing email setup")
logger.log_success("Email credentials configured")
logger.log_info("Test email will be sent to: edwin.f.capidos@gmail.com")
logger.set_total_count(1)
logger.log_finish("Email test completed")
EOF

echo ""
echo "📧 Test complete! Check edwin.f.capidos@gmail.com for the test email."
echo ""
echo "🔧 To manually test anytime, run:"
echo "   python3 /home/ecaps24/dev/ppop-insights/scripts/enhanced_logging.py"
echo ""
echo "✅ Email notifications are now active for all automated scrapers!"