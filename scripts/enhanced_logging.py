#!/usr/bin/env python3
"""
Enhanced Logging System for PPOP Insights Scrapers
Provides detailed logging with timestamps, status tracking, and email notifications
"""

import os
import sys
import logging
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

class ScraperLogger:
    def __init__(self, script_name, log_dir="/home/ecaps24/dev/ppop-insights/logs"):
        self.script_name = script_name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file path
        self.log_file = self.log_dir / f"{script_name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(script_name)
        
        # Email settings
        self.email_recipient = "edwin.f.capidos@gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Stats tracking
        self.stats = {
            'start_time': datetime.now().isoformat(),
            'status': 'started',
            'errors': [],
            'success_count': 0,
            'total_count': 0
        }
    
    def log_start(self, message="Script started"):
        """Log script start"""
        self.logger.info(f"🚀 {message}")
        self.logger.info(f"📝 Log file: {self.log_file}")
        
    def log_success(self, message):
        """Log successful operation"""
        self.logger.info(f"✅ {message}")
        self.stats['success_count'] += 1
        
    def log_error(self, message, error=None):
        """Log error with details"""
        error_msg = f"❌ {message}"
        if error:
            error_msg += f" - {str(error)}"
        self.logger.error(error_msg)
        self.stats['errors'].append({
            'message': message,
            'error': str(error) if error else None,
            'timestamp': datetime.now().isoformat()
        })
        
    def log_info(self, message):
        """Log general information"""
        self.logger.info(f"ℹ️  {message}")
        
    def log_warning(self, message):
        """Log warning"""
        self.logger.warning(f"⚠️  {message}")
        
    def set_total_count(self, count):
        """Set total expected operations"""
        self.stats['total_count'] = count
        
    def log_finish(self, message="Script completed"):
        """Log script completion and send email"""
        end_time = datetime.now()
        self.stats['end_time'] = end_time.isoformat()
        self.stats['duration'] = str(end_time - datetime.fromisoformat(self.stats['start_time']))
        
        if self.stats['errors']:
            self.stats['status'] = 'completed_with_errors'
            self.logger.warning(f"⚠️  {message} with {len(self.stats['errors'])} errors")
        else:
            self.stats['status'] = 'completed_successfully'
            self.logger.info(f"🎉 {message} successfully")
            
        # Log summary
        self.logger.info(f"📊 Summary: {self.stats['success_count']}/{self.stats['total_count']} successful")
        self.logger.info(f"⏱️  Duration: {self.stats['duration']}")
        
        # Save stats to JSON
        stats_file = self.log_dir / f"{self.script_name}_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
            
        # Send email notification
        self.send_email_notification()
        
    def send_email_notification(self):
        """Send email notification with log summary"""
        try:
            # Check if we have email credentials in environment
            gmail_user = os.environ.get('GMAIL_USER')
            gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
            
            if not gmail_user or not gmail_password:
                self.logger.warning("📧 Email credentials not found in environment variables")
                self.logger.info("📧 To enable email notifications, set GMAIL_USER and GMAIL_APP_PASSWORD")
                return
                
            # Create email content
            subject = f"PPOP Insights - {self.script_name.title()} Report"
            
            # Determine status emoji and color
            if self.stats['status'] == 'completed_successfully':
                status_emoji = "✅"
                status_text = "SUCCESS"
            elif self.stats['status'] == 'completed_with_errors':
                status_emoji = "⚠️"
                status_text = "COMPLETED WITH ERRORS"
            else:
                status_emoji = "❌"
                status_text = "FAILED"
                
            # Build email body
            body = f"""
PPOP Insights Automation Report
===============================

Script: {self.script_name.title()}
Status: {status_emoji} {status_text}
Duration: {self.stats.get('duration', 'Unknown')}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 SUMMARY
----------
Success Count: {self.stats['success_count']}
Total Operations: {self.stats['total_count']}
Success Rate: {(self.stats['success_count']/max(1, self.stats['total_count'])*100):.1f}%

"""
            
            # Add error details if any
            if self.stats['errors']:
                body += f"\n❌ ERRORS ({len(self.stats['errors'])})\n"
                body += "-" * 20 + "\n"
                for i, error in enumerate(self.stats['errors'], 1):
                    body += f"{i}. {error['message']}\n"
                    if error['error']:
                        body += f"   Details: {error['error']}\n"
                    body += f"   Time: {error['timestamp']}\n\n"
            
            # Add log file info
            body += f"\n📝 LOG FILE\n"
            body += f"Location: {self.log_file}\n"
            body += f"Size: {self.log_file.stat().st_size if self.log_file.exists() else 0} bytes\n"
            
            body += f"\n--\nPPOP Insights Automation System\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Create and send email
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = self.email_recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"📧 Email notification sent to {self.email_recipient}")
            
        except Exception as e:
            self.logger.error(f"📧 Failed to send email notification: {str(e)}")
            self.logger.info("📧 Email setup instructions:")
            self.logger.info("   1. Enable 2-factor authentication on Gmail")
            self.logger.info("   2. Generate app password: https://myaccount.google.com/apppasswords")
            self.logger.info("   3. Set environment variables:")
            self.logger.info("      export GMAIL_USER='your-email@gmail.com'")
            self.logger.info("      export GMAIL_APP_PASSWORD='your-app-password'")

if __name__ == "__main__":
    # Test the logging system
    logger = ScraperLogger("test_logger")
    logger.log_start("Testing enhanced logging system")
    logger.set_total_count(3)
    
    logger.log_info("Processing item 1...")
    logger.log_success("Item 1 completed")
    
    logger.log_info("Processing item 2...")
    logger.log_success("Item 2 completed")
    
    logger.log_info("Processing item 3...")
    logger.log_error("Item 3 failed", Exception("Test error"))
    
    logger.log_finish("Test completed")