#!/usr/bin/env python3
"""
Comprehensive Music Data Scraper
- Primary source: Kworb for reliable stream data
- Secondary: Enhanced metadata from track URLs
- Combines multiple data sources for complete music analytics
- Handles deduplication and data validation
"""

import requests
import csv
import time
import argparse
import re
import os
from urllib.parse import urljoin
import sys
from datetime import datetime

class ComprehensiveMusicScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def clean_text(self, text):
        """Remove HTML tags and clean text"""
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
        return ' '.join(text.split()).strip()
    
    def extract_spotify_track_id(self, html_content):
        """Extract Spotify track ID from HTML content"""
        spotify_pattern = r'https://open\.spotify\.com/track/([a-zA-Z0-9]{22})'
        match = re.search(spotify_pattern, html_content)
        return match.group(1) if match else None
    
    def extract_artist_id_from_url(self, url):
        """Extract artist ID from Kworb URL"""
        match = re.search(r'/artist/([^/_]+)', url)
        return match.group(1) if match else 'unknown_artist'
    
    def extract_last_update_date(self, html_content):
        """Extract the 'Last updated' date from kworb page"""
        # Look for "Last updated: YYYY/MM/DD" pattern
        patterns = [
            r'Last updated:\s*([0-9]{4}/[0-9]{2}/[0-9]{2})',
            r'last updated:\s*([0-9]{4}/[0-9]{2}/[0-9]{2})',
            r'Updated:\s*([0-9]{4}/[0-9]{2}/[0-9]{2})',
            r'updated:\s*([0-9]{4}/[0-9]{2}/[0-9]{2})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                # Convert from YYYY/MM/DD to YYYY-MM-DD format
                date_str = match.group(1).replace('/', '-')
                try:
                    # Validate the date format
                    from datetime import datetime
                    datetime.strptime(date_str, '%Y-%m-%d')
                    return date_str
                except ValueError:
                    continue
        
        # If no last update date found, return None
        return None

    def extract_artist_name(self, html_content):
        """Extract artist name from the page"""
        # Try multiple patterns to find artist name
        patterns = [
            r'<title[^>]*>([^<]+)(?:\s*-\s*[^<]*)?(?:\s*\|\s*kworb\.net)?</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'class=["\']artist[^"\']*["\'][^>]*>([^<]+)<',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                return self.clean_text(match.group(1))
        return 'Unknown Artist'
    
    def scrape_artist_songs_from_kworb(self, artist_url, max_songs=None):
        """Scrape artist songs from Kworb with enhanced data extraction"""
        print(f"🎵 Scraping: {artist_url}")
        
        try:
            response = self.session.get(artist_url, timeout=30)
            response.raise_for_status()
            html_content = response.text
            
            # Extract artist info and last update date
            artist_id = self.extract_artist_id_from_url(artist_url)
            artist_name = self.extract_artist_name(html_content)
            kworb_last_updated = self.extract_last_update_date(html_content)
            
            if kworb_last_updated:
                print(f"   📅 Kworb last updated: {kworb_last_updated}")
            else:
                print(f"   ⚠️  Could not find kworb last update date")
            
            # Find all song rows in the table
            song_pattern = r'<tr[^>]*>.*?</tr>'
            rows = re.findall(song_pattern, html_content, re.DOTALL)
            
            songs = []
            rank = 1
            
            for row in rows:
                # Skip header row
                if 'Total' in row or 'Song' in row or not re.search(r'\d+,\d+', row):
                    continue
                
                # Extract song data from the row, including kworb last update date
                song_data = self.extract_song_data_from_row(row, artist_name, artist_id, artist_url, rank, kworb_last_updated)
                
                if song_data:
                    songs.append(song_data)
                    rank += 1
                    
                    print(f"   ✅ {rank-1:2}. {song_data['song_title']} - {song_data['total_streams']:,} streams")
                    
                    if max_songs and len(songs) >= max_songs:
                        break
            
            print(f"   📊 Total songs scraped: {len(songs)}")
            return songs
            
        except requests.RequestException as e:
            print(f"   ❌ Error scraping {artist_url}: {e}")
            return []
    
    def extract_song_data_from_row(self, row_html, artist_name, artist_id, source_url, rank, kworb_last_updated=None):
        """Extract comprehensive song data from a table row"""
        try:
            # Extract song title (usually first link in the row)
            title_match = re.search(r'<a[^>]*>([^<]+)</a>', row_html)
            if not title_match:
                return None
            
            song_title = self.clean_text(title_match.group(1))
            
            # Extract Spotify track ID if present
            spotify_track_id = self.extract_spotify_track_id(row_html)
            
            # Extract total streams (looking for large numbers with commas)
            stream_patterns = [
                r'>([0-9,]+)</td>',  # Table cell with streams
                r'>([0-9]{3,}(?:,[0-9]{3})*)<',  # Any large number with commas
                r'streams?["\']?[^>]*>([0-9,]+)',  # Near "streams" text
            ]
            
            total_streams = 0
            for pattern in stream_patterns:
                matches = re.findall(pattern, row_html)
                for match in matches:
                    clean_number = match.replace(',', '')
                    if clean_number.isdigit() and int(clean_number) > 10000:  # Reasonable stream threshold
                        total_streams = int(clean_number)
                        break
                if total_streams > 0:
                    break
            
            # Extract daily streams (usually smaller numbers in the same row)
            daily_streams = 0
            daily_matches = re.findall(r'>([0-9,]+)<', row_html)
            for match in daily_matches:
                clean_number = match.replace(',', '')
                if clean_number.isdigit():
                    num = int(clean_number)
                    # Daily streams are typically much smaller than total streams
                    if 10 <= num <= 1000000 and num != total_streams:
                        daily_streams = num
                        break
            
            # Use kworb last update date as the primary date, scrape_date as reference
            primary_date = kworb_last_updated if kworb_last_updated else datetime.now().strftime('%Y-%m-%d')
            
            return {
                'artist_name': artist_name,
                'artist_id': artist_id,
                'rank': rank,
                'song_title': song_title,
                'spotify_track_id': spotify_track_id or '',
                'total_streams': total_streams,
                'daily_streams': daily_streams,
                'source_url': source_url,
                'data_date': primary_date,  # When kworb last updated this data
                'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # When we scraped it
                'data_source_updated': kworb_last_updated is not None
            }
            
        except Exception as e:
            print(f"   ⚠️  Error processing row: {e}")
            return None
    
    def enhance_data_with_spotify_metadata(self, songs_data):
        """Enhance song data with additional Spotify metadata where possible"""
        print("🔍 Enhancing data with Spotify metadata...")
        enhanced_songs = []
        
        for i, song in enumerate(songs_data):
            enhanced_song = song.copy()
            
            # If we have a Spotify track ID, we can add the full URL
            if song.get('spotify_track_id'):
                enhanced_song['spotify_url'] = f"https://open.spotify.com/track/{song['spotify_track_id']}"
            
            # Add data quality indicators
            enhanced_song['has_spotify_id'] = bool(song.get('spotify_track_id'))
            enhanced_song['data_confidence'] = 'high' if song.get('total_streams', 0) > 0 else 'medium'
            
            enhanced_songs.append(enhanced_song)
            
            if (i + 1) % 10 == 0:
                print(f"   📊 Enhanced {i+1}/{len(songs_data)} songs")
        
        return enhanced_songs
    
    def load_existing_data(self, filename):
        """Load existing data from CSV file to avoid duplicates"""
        existing_data = {}
        if not os.path.exists(filename):
            print(f"📄 No existing file found - will create new: {filename}")
            return existing_data
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Use combination of artist_id and spotify_track_id as unique key
                    key = f"{row.get('artist_id', '')}_{row.get('spotify_track_id', '')}"
                    existing_data[key] = row
            
            print(f"📂 Loaded {len(existing_data)} existing songs from {filename}")
            return existing_data
            
        except Exception as e:
            print(f"⚠️  Error reading existing file: {e}")
            return {}
    
    def filter_new_songs(self, songs_data, existing_data):
        """Filter out songs that already exist in the CSV"""
        if not existing_data:
            return songs_data, []
        
        new_songs = []
        duplicate_songs = []
        
        for song in songs_data:
            key = f"{song.get('artist_id', '')}_{song.get('spotify_track_id', '')}"
            if key in existing_data:
                duplicate_songs.append(song)
            else:
                new_songs.append(song)
        
        return new_songs, duplicate_songs
    
    def export_to_csv(self, songs_data, filename, mode='a'):
        """Export songs data to CSV file - always append new data"""
        if not songs_data:
            print("❌ No data to export")
            return False
        
        fieldnames = [
            'artist_name', 'artist_id', 'rank', 'song_title', 'spotify_track_id',
            'total_streams', 'daily_streams', 'source_url', 'data_date', 'scrape_date',
            'data_source_updated', 'spotify_url', 'has_spotify_id', 'data_confidence'
        ]
        
        # Add any extra fields that might be in the data
        extra_fields = set()
        for song in songs_data:
            extra_fields.update(song.keys())
        extra_fields -= set(fieldnames)
        fieldnames.extend(sorted(extra_fields))
        
        try:
            file_exists = os.path.exists(filename) and os.path.getsize(filename) > 0
            
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header only if file doesn't exist or is empty
                if not file_exists:
                    writer.writeheader()
                
                for song in songs_data:
                    # Ensure all fields are present
                    row = {field: song.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            print(f"✅ Added {len(songs_data)} songs to {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return False
    
    def show_summary(self, songs_data):
        """Show summary statistics of scraped data"""
        if not songs_data:
            return
        
        total_songs = len(songs_data)
        with_spotify_ids = sum(1 for song in songs_data if song.get('spotify_track_id'))
        total_streams = sum(song.get('total_streams', 0) for song in songs_data)
        
        print(f"\n📊 Scraping Summary:")
        print(f"   Total songs: {total_songs}")
        print(f"   Songs with Spotify IDs: {with_spotify_ids} ({with_spotify_ids/total_songs*100:.1f}%)")
        print(f"   Total combined streams: {total_streams:,}")
        
        # Show top songs
        sorted_songs = sorted([s for s in songs_data if s.get('total_streams', 0) > 0], 
                            key=lambda x: x.get('total_streams', 0), reverse=True)
        
        if sorted_songs:
            print(f"\n🔥 Top songs by streams:")
            for i, song in enumerate(sorted_songs[:5]):
                streams = song.get('total_streams', 0)
                has_id = "✅" if song.get('spotify_track_id') else "⚪"
                print(f"   {i+1}. {song.get('song_title', 'Unknown')} - {streams:,} streams {has_id}")

def main():
    parser = argparse.ArgumentParser(description='Comprehensive music data scraper (Kworb + enhanced metadata)')
    parser.add_argument('--artist-url', help='Kworb artist URL to scrape')
    parser.add_argument('--artist-urls', nargs='+', help='Multiple artist URLs')
    parser.add_argument('--output', '-o', default='../output/comprehensive_music_data.csv', help='Output CSV filename')
    parser.add_argument('--max-songs', type=int, help='Maximum songs per artist (for testing)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing file instead of appending (default: append)')
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    print("🎵 Comprehensive Music Data Scraper")
    print("=" * 60)
    
    scraper = ComprehensiveMusicScraper()
    
    # Get artist URLs
    artist_urls = []
    if args.artist_url:
        artist_urls = [args.artist_url]
    elif args.artist_urls:
        artist_urls = args.artist_urls
    else:
        print("❌ Please provide --artist-url or --artist-urls")
        print("\n💡 Example:")
        print("   python3 comprehensive_music_scraper.py --artist-url https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP_songs.html")
        sys.exit(1)
    
    all_songs = []
    
    # Scrape each artist
    for i, url in enumerate(artist_urls):
        if i > 0:
            print(f"\n⏸️  Waiting {args.delay} seconds before next artist...")
            time.sleep(args.delay)
        
        print(f"\n📂 Processing artist {i+1}/{len(artist_urls)}")
        songs = scraper.scrape_artist_songs_from_kworb(url, max_songs=args.max_songs)
        
        if songs:
            enhanced_songs = scraper.enhance_data_with_spotify_metadata(songs)
            all_songs.extend(enhanced_songs)
    
    if all_songs:
        # Export results (append by default, overwrite only if requested)
        export_mode = 'w' if args.overwrite else 'a'
        success = scraper.export_to_csv(all_songs, args.output, mode=export_mode)
        
        if success:
            # Also append to historical file
            historical_file = '/home/ecaps24/dev/ppop-insights/data/historical/comprehensive_streams.csv'
            scraper.export_to_csv(all_songs, historical_file, mode='a')
            scraper.show_summary(all_songs)
            print(f"\n✅ Scraping complete! Data saved to: {args.output}")
            print(f"✅ Historical data updated: {historical_file}")
        else:
            print("❌ Failed to export data")
            sys.exit(1)
    else:
        print("❌ No data was scraped")
        sys.exit(1)

if __name__ == "__main__":
    main()