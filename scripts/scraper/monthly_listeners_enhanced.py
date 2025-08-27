#!/usr/bin/env python3
"""
Enhanced Monthly Listeners Scraper with Anti-Bot Detection Evasion
- Multiple user agents rotation
- Random delays and request patterns
- Session persistence
- Enhanced header manipulation
- Multiple extraction strategies
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
import json

class EnhancedMonthlyListenersScraper:
    def __init__(self):
        self.sessions = []
        self.current_session_idx = 0
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
        ]
        self.setup_sessions()
    
    def setup_sessions(self):
        """Create multiple sessions with different configurations"""
        for i in range(3):
            session = requests.Session()
            
            # Rotate user agents
            user_agent = random.choice(self.user_agents)
            
            # Enhanced headers to mimic real browser
            headers = {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            
            # Add some randomization to headers
            if random.random() > 0.5:
                headers['Referer'] = random.choice([
                    'https://www.google.com/',
                    'https://open.spotify.com/',
                    'https://www.spotify.com/',
                ])
            
            session.headers.update(headers)
            self.sessions.append(session)
    
    def get_session(self):
        """Get next session in rotation"""
        session = self.sessions[self.current_session_idx]
        self.current_session_idx = (self.current_session_idx + 1) % len(self.sessions)
        return session
    
    def human_delay(self, base_delay=2):
        """Simulate human-like delays"""
        delay = base_delay + random.uniform(-0.5, 2.0)
        delay = max(1.0, delay)  # Minimum 1 second delay
        time.sleep(delay)
    
    def make_request(self, url, max_retries=3):
        """Make request with retries and different strategies"""
        for attempt in range(max_retries):
            try:
                session = self.get_session()
                
                # Add some randomization to the request
                if attempt > 0:
                    self.human_delay(3 + attempt)
                
                # Try different approaches based on attempt
                if attempt == 0:
                    # Normal request
                    response = session.get(url, timeout=30)
                elif attempt == 1:
                    # Request with different headers
                    session.headers.update({
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                    })
                    response = session.get(url, timeout=30)
                else:
                    # Last attempt with minimal headers
                    minimal_session = requests.Session()
                    minimal_session.headers.update({
                        'User-Agent': random.choice(self.user_agents)
                    })
                    response = minimal_session.get(url, timeout=30)
                
                response.raise_for_status()
                
                # Check if we got the actual page (not a redirect to web player)
                if 'Spotify – Web Player' in response.text:
                    print(f"   ⚠️  Got web player redirect on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return None
                
                return response
                
            except Exception as e:
                print(f"   ❌ Request failed (attempt {attempt + 1}): {str(e)[:100]}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    backoff = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff)
                else:
                    return None
        
        return None
    
    def extract_monthly_listeners(self, html_content, artist_url):
        """Enhanced extraction with multiple strategies"""
        
        # Extract artist ID and basic info
        artist_id_match = re.search(r'/artist/([a-zA-Z0-9]{22})', artist_url)
        artist_id = artist_id_match.group(1) if artist_id_match else 'unknown'
        
        # Strategy 1: Extract artist name from title
        artist_name = 'Unknown Artist'
        title_patterns = [
            r'<title[^>]*>([^<|]+)(?:\s*\|\s*Spotify)?</title>',
            r'<title[^>]*>([^<]+)</title>',
        ]
        
        for pattern in title_patterns:
            title_match = re.search(pattern, html_content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                if title and title != 'Spotify – Web Player' and 'Spotify' not in title:
                    artist_name = title
                    break
                elif ' | Spotify' in title:
                    artist_name = title.replace(' | Spotify', '').strip()
                    if artist_name and artist_name != 'Spotify':
                        break
        
        # Strategy 2: Multiple patterns for monthly listeners
        monthly_listeners = 0
        source = 'not_found'
        
        extraction_strategies = [
            # Pattern 1: data-testid approach
            (r'data-testid="monthly-listeners-label">([0-9,]+)\s*monthly\s+listeners', 'testid_exact'),
            # Pattern 2: Meta description approach
            (r'Artist\s*·\s*([0-9.]+(?:[MKB])?)\s*monthly\s+listeners', 'meta_description'),
            # Pattern 3: JSON-LD structured data
            (r'"description":\s*"[^"]*([0-9,]+)\s*monthly\s+listeners[^"]*"', 'json_ld'),
            # Pattern 4: Generic monthly listeners
            (r'([0-9]{1,3}(?:,[0-9]{3})*)\s*monthly\s+listeners', 'generic_exact'),
            # Pattern 5: Abbreviated format (1.7M monthly listeners)
            (r'([0-9.]+[MKB])\s*monthly\s+listeners', 'abbreviated'),
            # Pattern 6: In content or aria-labels
            (r'aria-label="[^"]*([0-9,]+)[^"]*monthly\s+listeners', 'aria_label'),
            # Pattern 7: In script tags or data attributes
            (r'monthly[_-]?listeners["\']?\s*:\s*["\']?([0-9,]+)', 'data_attribute'),
        ]
        
        for pattern, source_type in extraction_strategies:
            if monthly_listeners > 0:
                break
                
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    if source_type == 'meta_description' or source_type == 'abbreviated':
                        # Handle abbreviated numbers (1.7M, 800K, etc.)
                        if match.endswith('M'):
                            base_value = float(match[:-1])
                            monthly_listeners = int(base_value * 1000000)
                            source = source_type
                            break
                        elif match.endswith('K'):
                            base_value = float(match[:-1])
                            monthly_listeners = int(base_value * 1000)
                            source = source_type
                            break
                        elif match.endswith('B'):
                            base_value = float(match[:-1])
                            monthly_listeners = int(base_value * 1000000000)
                            source = source_type
                            break
                    else:
                        # Handle exact numbers
                        clean_number = match.replace(',', '')
                        if clean_number.isdigit():
                            monthly_listeners = int(clean_number)
                            source = source_type
                            break
                except ValueError:
                    continue
        
        return {
            'artist_name': artist_name,
            'artist_id': artist_id,
            'monthly_listeners': monthly_listeners,
            'source_url': artist_url,
            'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': 'spotify.com',
            'extraction_method': source
        }
    
    def get_exact_monthly_listeners(self, artist_url):
        """Enhanced monthly listeners extraction with anti-bot techniques"""
        print(f"🎵 Getting exact monthly listeners: {artist_url}")
        
        # Make request with anti-bot evasion
        response = self.make_request(artist_url)
        
        if not response:
            return {
                'artist_name': 'Error',
                'artist_id': 'unknown',
                'monthly_listeners': 0,
                'source_url': artist_url,
                'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source': 'spotify.com',
                'extraction_method': 'request_failed'
            }
        
        # Extract data from response
        result = self.extract_monthly_listeners(response.text, artist_url)
        
        print(f"   ✅ {result['artist_name']}: {result['monthly_listeners']:,} monthly listeners [{result['extraction_method']}]")
        return result
    
    def scrape_multiple_artists(self, artist_urls, delay=3):
        """Scrape multiple artists with enhanced anti-bot techniques"""
        results = []
        
        for i, url in enumerate(artist_urls):
            print(f"\n📊 Progress: {i+1}/{len(artist_urls)}")
            result = self.get_exact_monthly_listeners(url)
            results.append(result)
            
            if i < len(artist_urls) - 1:
                delay_time = delay + random.uniform(-1, 2)
                delay_time = max(2.0, delay_time)
                print(f"   ⏸️  Waiting {delay_time:.1f} seconds...")
                self.human_delay(delay_time)
        
        return results
    
    def export_to_csv(self, data, filename):
        """Export data to CSV with enhanced error handling"""
        if not data:
            print("❌ No data to export")
            return False
        
        fieldnames = [
            'artist_name', 'artist_id', 'monthly_listeners',
            'source_url', 'scrape_date', 'data_source', 'extraction_method'
        ]
        
        # Add extra fields if they exist
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
    
    def show_summary(self, data):
        """Show enhanced results summary"""
        if not data:
            return
        
        total = len(data)
        with_data = sum(1 for d in data if d.get('monthly_listeners', 0) > 0)
        success_rate = (with_data / total) * 100 if total > 0 else 0
        
        print(f"\n📊 Results Summary:")
        print(f"   Artists processed: {total}")
        print(f"   With monthly listeners: {with_data}")
        print(f"   Success rate: {success_rate:.1f}%")
        
        # Show extraction methods used
        methods = {}
        for d in data:
            method = d.get('extraction_method', 'unknown')
            methods[method] = methods.get(method, 0) + 1
        
        print(f"\n🔧 Extraction methods:")
        for method, count in sorted(methods.items()):
            print(f"   {method}: {count}")
        
        # Show by listeners
        valid_data = sorted([d for d in data if d.get('monthly_listeners', 0) > 0], 
                          key=lambda x: x.get('monthly_listeners', 0), reverse=True)
        
        if valid_data:
            print(f"\n🔥 Monthly listeners ranking:")
            for i, artist in enumerate(valid_data):
                listeners = artist.get('monthly_listeners', 0)
                name = artist.get('artist_name', 'Unknown')
                method = artist.get('extraction_method', 'unknown')
                print(f"   {i+1}. {name}: {listeners:,} [{method}]")

def main():
    parser = argparse.ArgumentParser(description='Enhanced monthly listeners scraper with anti-bot evasion')
    parser.add_argument('--sb19', action='store_true', help='Scrape SB19')
    parser.add_argument('--bini', action='store_true', help='Scrape BINI')
    parser.add_argument('--both', action='store_true', help='Scrape both SB19 and BINI')
    parser.add_argument('--artist-url', help='Custom Spotify artist URL')
    parser.add_argument('--output', '-o', default='enhanced_monthly_listeners.csv', help='Output CSV file')
    parser.add_argument('--delay', type=int, default=4, help='Base delay between requests (seconds)')
    
    args = parser.parse_args()
    
    print("🎵 Enhanced Monthly Listeners Scraper")
    print("=" * 60)
    print("🛡️  Using anti-bot detection evasion techniques")
    
    scraper = EnhancedMonthlyListenersScraper()
    
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
    elif args.artist_url:
        urls = [args.artist_url]
    else:
        print("❌ Please specify --sb19, --bini, --both, or --artist-url")
        print("Examples:")
        print("  python3 monthly_listeners_enhanced.py --both")
        print("  python3 monthly_listeners_enhanced.py --sb19")
        sys.exit(1)
    
    # Scrape with enhanced techniques
    results = scraper.scrape_multiple_artists(urls, delay=args.delay)
    
    if results:
        scraper.export_to_csv(results, args.output)
        # Also append to historical file
        historical_file = '/home/ecaps24/dev/ppop-insights/data/historical/monthly_listeners.csv'
        scraper.export_to_csv(results, historical_file)
        scraper.show_summary(results)
        print(f"\n✅ Complete! Data saved to: {args.output}")
        print(f"✅ Historical data updated: {historical_file}")
    else:
        print("❌ No results")

if __name__ == "__main__":
    main()