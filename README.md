# 🎵 PPOP Music Analytics Dashboard

A comprehensive music streaming analytics tool for tracking SB19 and BINI performance across platforms, featuring real-time data visualization and automated scraping with anti-bot detection evasion.

## ✨ Features

### 📊 Interactive Dashboard
- **Real-time streaming analytics** with comprehensive visualization
- **Monthly listeners tracking** with trend analysis  
- **Time-range filtering** for focused data analysis
- **Conditional chart coloring** - red indicators for declining metrics
- **Artist-specific color coding** for easy identification
- **Responsive design** with custom PPOP theme

### 🤖 Advanced Scrapers
- **Comprehensive streaming data** from Kworb.net
- **Monthly listeners tracking** from Spotify with anti-bot evasion
- **Mobile browser simulation** to bypass detection systems
- **Multiple extraction strategies** with fallback methods
- **Automated data collection** with configurable scheduling

### 🛡️ Anti-Bot Detection Features
- Mobile user agent rotation
- Dynamic header manipulation  
- Session management with cookies
- Request timing randomization
- Multiple endpoint testing
- Exponential backoff retry logic

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser

### Installation
```bash
git clone https://github.com/yourusername/kworb-scraper.git
cd kworb-scraper
```

### Running the Dashboard
```bash
# Start the dashboard server
./scripts/start_dashboard.sh

# Or use Python directly
python3 scripts/serve_dashboard.py
```

Visit `http://localhost:8000/dashboard/dashboard.html`

### Running the Scrapers

**Comprehensive Streaming Data:**
```bash
python3 scripts/scraper/comprehensive_music_scraper.py --artist-urls \
    "https://kworb.net/spotify/artist/3g7vYcdDXnqnDKYFwqXBJP_songs.html" \
    "https://kworb.net/spotify/artist/7tNO3vJC9zlHy2IJOx34ga_songs.html" \
    --output latest_streams.csv
```

**Monthly Listeners (Mobile Anti-Bot):**
```bash
python3 scripts/scraper/mobile_listeners_scraper.py --both --output latest_listeners.csv
```

## 📁 Project Structure

```
kworb-scraper/
├── dashboard/
│   ├── dashboard.html          # Main analytics dashboard
│   ├── ppop-theme.css         # Custom styling
│   └── theme-example.html     # Theme preview
├── scripts/
│   ├── scraper/
│   │   ├── comprehensive_music_scraper.py    # Kworb streaming data
│   │   ├── mobile_listeners_scraper.py       # Anti-bot Spotify scraper  
│   │   ├── monthly_listeners_enhanced.py     # Advanced techniques
│   │   └── monthly_listeners_simple.py       # Basic scraper
│   ├── serve_dashboard.py     # Dashboard server
│   ├── start_dashboard.sh     # Launch script
│   └── run_*.sh              # Automation scripts
├── data/
│   ├── historical/           # Long-term data storage
│   ├── processed/           # Cleaned datasets
│   └── raw/                # Original scraped data
└── docs/                   # Documentation
```

## 📈 Dashboard Features

### Monthly Listeners Chart
- **Bar chart**: Current monthly listener counts
- **Line chart**: Period-over-period changes  
- **Red indicators**: Declining listener counts
- **Time filtering**: Last 7 days, Month-to-date, All time

### Streaming Analytics  
- **Top tracks ranking** by total streams
- **Artist comparison** with color coding
- **Interactive tooltips** with detailed metrics
- **Responsive time-range filtering**

### Data Management
- **Automatic updates** from multiple scraper runs
- **Historical data preservation** 
- **CSV export capabilities**
- **Real-time chart updates**

## 🎯 Supported Artists

- **SB19** (3g7vYcdDXnqnDKYFwqXBJP)
- **BINI** (7tNO3vJC9zlHy2IJOx34ga)

*Easily extensible to support additional artists*

## ⚙️ Configuration

### Scraper Settings
- **Delay timing**: Configurable request intervals
- **User agent rotation**: Multiple mobile browsers
- **Retry logic**: Exponential backoff
- **Output formats**: CSV with customizable fields

### Dashboard Customization
- **Color schemes**: Artist-specific palettes
- **Chart types**: Bar, line, combined views
- **Time ranges**: Flexible date filtering
- **Update frequency**: Real-time data refresh

## 🔧 Technical Details

### Anti-Bot Techniques
1. **Mobile Browser Simulation**
   - iPhone/Android user agents
   - Mobile-specific headers
   - Viewport and device characteristics

2. **Request Patterns**
   - Human-like timing delays
   - Session persistence
   - Cookie management
   - Referer rotation

3. **Endpoint Diversity**
   - Multiple Spotify URLs
   - Embed endpoint testing
   - International variants
   - Fallback strategies

### Data Processing
- **Real-time parsing** of HTML content
- **Multiple extraction patterns** for robustness
- **Data validation** and error handling
- **Historical trend calculation**

## 📊 Sample Data

Latest metrics (as of recent scraping):
- **SB19**: 1,724,972 monthly listeners
- **BINI**: 1,963,675 monthly listeners  
- **Combined streams**: 1.9B+ across 97 tracked songs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes with descriptive messages
4. Push to your fork
5. Create a Pull Request

## ⚠️ Ethical Usage

This tool is designed for:
- ✅ Analytics and research purposes
- ✅ Fan community insights  
- ✅ Educational data science projects
- ✅ Personal music trend tracking

Please respect:
- 🚫 Website terms of service
- 🚫 Rate limiting and server resources
- 🚫 Commercial data reselling
- 🚫 Malicious usage

## 📄 License

This project is provided as-is for educational and analytical purposes. Please ensure compliance with all applicable terms of service when using web scraping functionality.

## 🎵 About PPOP

Supporting the growing Filipino pop music scene through data-driven insights and community analytics.

---

**🤖 Built with Claude Code**

*Empowering music analytics through intelligent automation*