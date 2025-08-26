#!/usr/bin/env python3
"""
Mobile-First Monthly Listeners Scraper
- Mimics mobile browser behavior
- Uses mobile user agents
- Implements additional evasion techniques
"""

import requests
import csv
import time
import argparse
import re
import os
import sys
import random
from datetime import datetime
import urllib.parse

class MobileListenersScraper:
    def __init__(self):
        self.session = requests.Session()
        self.mobile_user_agents = [
            # iPhone Safari
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            # Android Chrome
            'Mozilla/5.0 (Linux; Android 14; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            # iPad Safari
            'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
            # Samsung Internet
            'Mozilla/5.0 (Linux; Android 14; SAMSUNG SM-G996U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36',
        ]
        self.setup_mobile_session()
    
    def setup_mobile_session(self):
        """Setup session to mimic mobile browser"""
        mobile_headers = {
            'User-Agent': random.choice(self.mobile_user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'Viewport-Width': '360',
            'dnt': '1',
        }
        
        self.session.headers.update(mobile_headers)
        
        # Set mobile-specific cookies
        self.session.cookies.update({
            'sp_t': ''.join(random.choices('abcdef0123456789', k=32)),
            '_gcl_au': '1.1.123456789.1234567890'
        })
    
    def try_different_endpoints(self, artist_id):
        """Try different Spotify endpoints that might be less protected"""
        endpoints = [
            f"https://open.spotify.com/artist/{artist_id}",
            f"https://open.spotify.com/artist/{artist_id}?si=abc123",
            f"https://open.spotify.com/intl-en/artist/{artist_id}",
            f"https://open.spotify.com/embed/artist/{artist_id}",
        ]
        
        for endpoint in endpoints:
            print(f"   🔄 Trying endpoint: {endpoint}")
            try:
                # Reset headers for each attempt
                self.setup_mobile_session()
                
                # Add referer for some attempts
                if random.random() > 0.5:
                    self.session.headers['Referer'] = 'https://www.google.com/search?q=spotify+artist'
                
                response = self.session.get(endpoint, timeout=30)
                response.raise_for_status()
                
                # Check if we got actual content
                if 'Spotify – Web Player' not in response.text and len(response.text) > 1000:
                    print(f"   ✅ Success with endpoint: {endpoint}")
                    return response.text, endpoint
                else:
                    print(f"   ❌ Got web player redirect")
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                print(f"   ❌ Failed: {str(e)[:50]}")
                time.sleep(random.uniform(1, 3))
        
        return None, None
    
    def extract_from_page_source(self, html_content):
        """Extract data from various parts of the page"""
        data = {'monthly_listeners': 0, 'artist_name': 'Unknown Artist'}
        
        # Try to extract artist name
        name_patterns = [
            r'<h1[^>]*>([^<]+)</h1>',
            r'<title[^>]*>([^<|]+)(?:\s*\|\s*Spotify)?</title>',
            r'"name"\s*:\s*"([^"]+)"',
            r'artist["\']?\s*:\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name and 'Spotify' not in name and len(name) > 1:
                    data['artist_name'] = name
                    break
        
        # Try to extract monthly listeners
        listener_patterns = [
            # Exact numbers
            r'([0-9]{1,3}(?:,[0-9]{3})+)\s*monthly\s+listeners',
            # Abbreviated numbers
            r'([0-9.]+[MK])\s*monthly\s+listeners',
            # In JSON or data attributes
            r'"monthly_listeners["\']?\s*:\s*["\']?([0-9,]+)',
            # In meta descriptions
            r'Artist\s*·\s*([0-9.]+[MK]?)\s*monthly\s+listeners',
            # Alternative formats
            r'listeners["\']?\s*:\s*["\']?([0-9,]+)',
        ]
        
        for pattern in listener_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    if 'M' in match:
                        number = float(match.replace('M', '')) * 1000000
                        data['monthly_listeners'] = int(number)
                        return data
                    elif 'K' in match:
                        number = float(match.replace('K', '')) * 1000
                        data['monthly_listeners'] = int(number)
                        return data
                    else:
                        number = int(match.replace(',', ''))
                        if 1000 <= number <= 50000000:  # Reasonable range
                            data['monthly_listeners'] = number
                            return data
                except ValueError:
                    continue
        
        return data
    
    def scrape_artist(self, artist_url):
        """Scrape single artist with multiple strategies"""
        print(f"🎵 Mobile scraping: {artist_url}")
        
        # Extract artist ID
        artist_id_match = re.search(r'/artist/([a-zA-Z0-9]{22})', artist_url)
        if not artist_id_match:
            return self.create_error_result(artist_url, "Invalid artist URL")
        
        artist_id = artist_id_match.group(1)
        
        # Try different approaches
        html_content, final_url = self.try_different_endpoints(artist_id)
        
        if not html_content:
            return self.create_error_result(artist_url, "All endpoints failed")
        
        # Extract data
        data = self.extract_from_page_source(html_content)
        
        result = {
            'artist_name': data['artist_name'],
            'artist_id': artist_id,
            'monthly_listeners': data['monthly_listeners'],
            'source_url': final_url or artist_url,
            'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': 'spotify.com',
            'extraction_method': 'mobile_scraper' if data['monthly_listeners'] > 0 else 'mobile_failed'
        }
        
        status = "✅" if result['monthly_listeners'] > 0 else "❌"
        print(f"   {status} {result['artist_name']}: {result['monthly_listeners']:,} monthly listeners")
        
        return result
    
    def create_error_result(self, artist_url, error_msg):
        """Create error result structure"""
        return {
            'artist_name': 'Error',
            'artist_id': 'unknown',
            'monthly_listeners': 0,
            'source_url': artist_url,
            'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': 'spotify.com',
            'extraction_method': 'error',
            'error': error_msg
        }
    
    def scrape_multiple_artists(self, artist_urls, delay=5):
        """Scrape multiple artists with delays"""
        results = []
        
        for i, url in enumerate(artist_urls):
            print(f"\n📊 Progress: {i+1}/{len(artist_urls)}")
            result = self.scrape_artist(url)
            results.append(result)
            
            if i < len(artist_urls) - 1:
                delay_time = delay + random.uniform(-1, 3)
                delay_time = max(3.0, delay_time)
                print(f"   ⏸️  Waiting {delay_time:.1f} seconds...")
                time.sleep(delay_time)
        
        return results
    
    def export_to_csv(self, data, filename):
        """Export results to CSV"""
        if not data:
            print("❌ No data to export")
            return False
        
        fieldnames = [
            'artist_name', 'artist_id', 'monthly_listeners',
            'source_url', 'scrape_date', 'data_source', 'extraction_method'
        ]
        
        # Add extra fields
        extra_fields = set()
        for item in data:
            extra_fields.update(item.keys())
        extra_fields -= set(fieldnames)
        fieldnames.extend(sorted(extra_fields))
        
        try:
            file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
            
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                for item in data:
                    row = {field: item.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            print(f"✅ Added {len(data)} records to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Mobile-first monthly listeners scraper')
    parser.add_argument('--sb19', action='store_true', help='Scrape SB19')
    parser.add_argument('--bini', action='store_true', help='Scrape BINI')
    parser.add_argument('--both', action='store_true', help='Scrape both SB19 and BINI')
    parser.add_argument('--output', '-o', default='mobile_monthly_listeners.csv', help='Output CSV file')
    parser.add_argument('--delay', type=int, default=6, help='Base delay between requests')
    
    args = parser.parse_args()
    
    print("📱 Mobile Monthly Listeners Scraper")
    print("=" * 50)
    print("🛡️  Using mobile browser simulation")
    
    scraper = MobileListenersScraper()
    
    # Determine URLs
    urls = []
    if args.both or (args.sb19 and args.bini):
        urls = [
            "https://open.spotify.com/artist/3g7vYcdDXnqnDKYFwqXBJP",  # SB19
            "https://open.spotify.com/artist/7tNO3vJC9zlHy2IJOx34ga"   # BINI
        ]
    elif args.sb19:
        urls = ["https://open.spotify.com/artist/3g7vYcdDXnqnDKYFwqXBJP"]
    elif args.bini:
        urls = ["https://open.spotify.com/artist/7tNO3vJC9zlHy2IJOx34ga"]
    else:
        print("❌ Please specify --sb19, --bini, or --both")
        sys.exit(1)
    
    # Scrape
    results = scraper.scrape_multiple_artists(urls, delay=args.delay)
    
    if results:
        scraper.export_to_csv(results, args.output)
        # Also append to historical file
        historical_file = '/home/ecaps24/dev/kworb-scraper/data/historical/monthly_listeners.csv'
        scraper.export_to_csv(results, historical_file)
        
        # Show summary
        total = len(results)
        successful = sum(1 for r in results if r.get('monthly_listeners', 0) > 0)
        print(f"\n📊 Summary: {successful}/{total} successful ({(successful/total)*100:.1f}%)")
        
        for result in results:
            if result.get('monthly_listeners', 0) > 0:
                print(f"   🎵 {result['artist_name']}: {result['monthly_listeners']:,}")
        
        print(f"\n✅ Complete! Data saved to: {args.output}")
    else:
        print("❌ No results")

if __name__ == "__main__":
    main()