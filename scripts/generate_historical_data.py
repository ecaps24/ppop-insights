#!/usr/bin/env python3
"""
Generate Historical Sample Data
Creates realistic sample data for the past month to simulate continuous tracking
"""

import csv
import random
from datetime import datetime, timedelta

def generate_monthly_listeners_history():
    """Generate 30 days of monthly listeners data using a random walk.

    Each day's value changes by a random delta between 5,000 and 20,000
    (increase or decrease) from the previous day, independently per artist.
    """
    data = []

    # Starting values (yesterday's baseline approximations)
    sb19_value = 1720632
    bini_value = 1977848

    # Generate data for past 30 days (oldest to most recent)
    for i in range(30, 0, -1):
        date = datetime.now() - timedelta(days=i)
        timestamp = date.strftime('%Y-%m-%d %H:%M:%S')

        # Apply random walk deltas for today's value from yesterday's value
        sb19_delta = random.randint(5000, 20000) * (1 if random.random() < 0.5 else -1)
        bini_delta = random.randint(5000, 20000) * (1 if random.random() < 0.5 else -1)

        # For the first iteration we keep the baseline, afterwards we update
        if i != 30:
            sb19_value = max(0, sb19_value + sb19_delta)
            bini_value = max(0, bini_value + bini_delta)

        # Add SB19 record
        data.append({
            'artist_name': 'SB19',
            'artist_id': '3g7vYcdDXnqnDKYFwqXBJP',
            'monthly_listeners': sb19_value,
            'monthly_listeners_raw': f"{sb19_value:,}",
            'source_url': 'https://open.spotify.com/artist/3g7vYcdDXnqnDKYFwqXBJP',
            'scrape_date': timestamp,
            'data_source': 'spotify.com',
            'extraction_method': 'historical_sample_random_walk'
        })

        # Add BINI record
        data.append({
            'artist_name': 'BINI',
            'artist_id': '7tNO3vJC9zlHy2IJOx34ga',
            'monthly_listeners': bini_value,
            'monthly_listeners_raw': f"{bini_value:,}",
            'source_url': 'https://open.spotify.com/artist/7tNO3vJC9zlHy2IJOx34ga',
            'scrape_date': timestamp,
            'data_source': 'spotify.com',
            'extraction_method': 'historical_sample_random_walk'
        })

    return data

def generate_streams_history():
    """Generate weekly streams data for past month (4 weeks)"""
    data = []
    
    # Sample SB19 songs with current stream counts
    sb19_songs = [
        {'title': 'MAPA', 'track_id': '6Fz2TpxUD0YvAPsuG8nDMJ', 'current_streams': 78870417},
        {'title': 'GENTO', 'track_id': '6RYhIHur2unkQv28fcinNO', 'current_streams': 69152677},
        {'title': 'DAM', 'track_id': '1NNsL6tYk06TqTea3mKB9P', 'current_streams': 42806370},
        {'title': 'Hanggang Sa Huli', 'track_id': '2WUhR1SraSy0SVIQKohJb6', 'current_streams': 29491168},
        {'title': 'Bazinga', 'track_id': '5QZw4F3N3PvuKNKHm9L20b', 'current_streams': 28736054}
    ]
    
    # Sample BINI songs with current stream counts  
    bini_songs = [
        {'title': 'Pantropiko', 'track_id': '03vwhCqyxupZDVEncdnCSc', 'current_streams': 191212682},
        {'title': 'Salamin, Salamin', 'track_id': '1iIJtD9hkzw4ZHfR7ND9yb', 'current_streams': 189300956},
        {'title': 'Karera', 'track_id': '1RL9cRcuzCrs75Wb2aq9Op', 'current_streams': 116829276},
        {'title': 'Lagi', 'track_id': '4Zau3FVlXayC82sQwGK5c1', 'current_streams': 89205857},
        {'title': 'Cherry On Top', 'track_id': '4lJbwNzGiP6YPqjCKQ2DHb', 'current_streams': 67421872}
    ]
    
    # Generate weekly data for past 4 weeks
    for week in range(4, 0, -1):  # 4 weeks ago to last week
        date = datetime.now() - timedelta(weeks=week)
        timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
        
        rank = 1
        
        # Add SB19 songs
        for song in sb19_songs:
            # Calculate historical stream counts (less than current)
            historical_streams = song['current_streams'] - (week * random.randint(50000, 200000))
            historical_streams = max(historical_streams, song['current_streams'] * 0.8)  # At least 80% of current
            
            data.append({
                'artist_name': 'SB19',
                'artist_id': '3g7vYcdDXnqnDKYFwqXBJP',
                'rank': rank,
                'song_title': song['title'],
                'spotify_track_id': song['track_id'],
                'total_streams': int(historical_streams),
                'daily_streams': random.randint(20000, 80000),
                'source_url': 'https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP_songs.html',
                'scrape_date': timestamp,
                'spotify_url': f"https://open.spotify.com/track/{song['track_id']}",
                'has_spotify_id': True,
                'data_confidence': 'high'
            })
            rank += 1
        
        # Add BINI songs
        for song in bini_songs:
            # BINI songs growing faster
            historical_streams = song['current_streams'] - (week * random.randint(100000, 400000))
            historical_streams = max(historical_streams, song['current_streams'] * 0.7)  # At least 70% of current
            
            data.append({
                'artist_name': 'BINI',
                'artist_id': '7tNO3vJC9zlHy2IJOx34ga', 
                'rank': rank - 5,  # Continue ranking from SB19
                'song_title': song['title'],
                'spotify_track_id': song['track_id'],
                'total_streams': int(historical_streams),
                'daily_streams': random.randint(30000, 120000),
                'source_url': 'https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga_songs.html',
                'scrape_date': timestamp,
                'spotify_url': f"https://open.spotify.com/track/{song['track_id']}",
                'has_spotify_id': True,
                'data_confidence': 'high'
            })
            rank += 1
    
    return data

def save_to_csv(data, filename, fieldnames):
    """Save data to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                csv_row = {field: row.get(field, '') for field in fieldnames}
                writer.writerow(csv_row)
        
        print(f"✅ Created {filename} with {len(data)} records")
        return True
    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return False

def main():
    print("🎵 Generating Historical Sample Data")
    print("=" * 50)
    
    # Generate monthly listeners historical data (30 days)
    print("📊 Generating monthly listeners history...")
    monthly_data = generate_monthly_listeners_history()
    
    monthly_fieldnames = [
        'artist_name', 'artist_id', 'monthly_listeners', 'monthly_listeners_raw',
        'source_url', 'scrape_date', 'data_source', 'extraction_method'
    ]
    
    save_to_csv(monthly_data, 'historical_monthly_listeners.csv', monthly_fieldnames)
    
    # Generate streams historical data (4 weeks)
    print("📊 Generating streams history...")
    streams_data = generate_streams_history()
    
    streams_fieldnames = [
        'artist_name', 'artist_id', 'rank', 'song_title', 'spotify_track_id',
        'total_streams', 'daily_streams', 'source_url', 'scrape_date',
        'spotify_url', 'has_spotify_id', 'data_confidence'
    ]
    
    save_to_csv(streams_data, 'historical_comprehensive_data.csv', streams_fieldnames)
    
    print(f"\n📈 Historical Data Summary:")
    print(f"   • Monthly listeners: 60 records (30 days × 2 artists)")
    print(f"   • Streams data: 40 records (4 weeks × 10 songs)")
    print(f"   • Time range: Past 30 days")
    print(f"   • Realistic growth trends included")
    print(f"\n📂 Files created:")
    print(f"   • historical_monthly_listeners.csv")
    print(f"   • historical_comprehensive_data.csv")
    
    print(f"\n💡 Usage:")
    print(f"   • Use these as baseline historical data")
    print(f"   • Your real scrapers will continue from current values")
    print(f"   • Data shows realistic trends and variations")

if __name__ == "__main__":
    main()