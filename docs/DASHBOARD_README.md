# 🎵 SB19 vs BINI Dashboard

A beautiful web dashboard for comparing monthly listeners between SB19 and BINI music groups.

## 🚀 Quick Start

```bash
# Start the dashboard server
./start_dashboard.sh

# Or manually:
python3 serve_dashboard.py
```

Then open http://localhost:8080/dashboard.html in your browser.

## 📊 Features

### Real-time Stats
- **Current Monthly Listeners** - Latest numbers for both groups
- **Growth Trends** - 7-day average growth percentages  
- **Leader Status** - Who's ahead and by how much
- **Combined Total** - Total monthly listeners across both groups

### Interactive Charts
- **Trend Line Chart** - 30-day historical view showing growth patterns
- **Comparison Bar Chart** - Current listener counts side by side
- **Responsive Design** - Works on desktop and mobile devices

### Data Table
- **Recent History** - Last 10 days of data with daily comparisons
- **Daily Differences** - Exact gaps between the groups
- **Leader Tracking** - Which group led on each day

## 📁 Data Sources

The dashboard automatically loads data from:
- `historical_monthly_listeners.csv` - Historical data (past 30 days)
- `scheduled_monthly_listeners.csv` - Real-time scraped data
- Fallback sample data if CSV files aren't accessible

## 🎨 Design Features

### Visual Elements
- **Gradient Background** - Modern purple/blue gradient
- **Glass Morphism** - Frosted glass effect on cards
- **Color Coding** - SB19 (Red), BINI (Blue)
- **Responsive Layout** - Grid system adapts to screen size

### Interactive Elements
- **Hover Effects** - Chart tooltips with detailed info
- **Growth Indicators** - Color-coded positive/negative growth
- **Real-time Updates** - Refreshes automatically with new data
- **Mobile Friendly** - Touch-optimized for mobile devices

## 📈 Key Insights Displayed

Based on current data trends:
- **BINI Leading**: ~1.98M vs SB19's ~1.72M monthly listeners
- **Growth Patterns**: BINI showing faster growth trajectory
- **Historical Context**: 30-day trend analysis
- **Competitive Dynamics**: Daily leadership changes tracked

## 🔧 Technical Details

### Dependencies
- **Chart.js** - Interactive charts and graphs
- **Python HTTP Server** - Simple local web server with CORS
- **Vanilla JavaScript** - No framework dependencies
- **CSS Grid/Flexbox** - Modern responsive layout

### Server Configuration
- **Port**: 8080 (configurable)
- **CORS Enabled**: Allows CSV file access
- **Auto-refresh**: Data updates automatically
- **Error Handling**: Graceful fallbacks for missing data

## 🚀 Usage Examples

### Starting the Server
```bash
# Simple start
./start_dashboard.sh

# Custom port (edit script)
python3 -c "..." # with port=8081
```

### Accessing the Dashboard
- **Local**: http://localhost:8080/dashboard.html
- **Network**: http://[your-ip]:8080/dashboard.html

### Stopping the Server
Press `Ctrl+C` in the terminal running the server.

## 📊 Data Format Expected

The dashboard expects CSV files with these columns:

**Monthly Listeners CSV:**
```csv
artist_name,artist_id,monthly_listeners,scrape_date,data_source
SB19,3g7vYcdDXnqnDKYFwqXBJP,1720632,2025-08-24 08:00:00,spotify.com
BINI,7tNO3vJC9zlHy2IJOx34ga,1977848,2025-08-24 08:00:00,spotify.com
```

## 🎯 Future Enhancements

- **Stream Counts Integration** - Add song streaming data
- **Export Features** - Download charts as images/PDF
- **Alert System** - Notifications for significant changes
- **Historical Analysis** - Deeper trend analytics
- **Social Media Integration** - Connect with social metrics

## 🛠️ Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using port 8080
lsof -i :8080

# Use different port in start_dashboard.sh
```

**CSV Files Not Loading:**
- Ensure files exist in the same directory as dashboard.html
- Check CORS headers in server configuration
- Verify CSV format matches expected columns

**Charts Not Displaying:**
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Verify data format in CSV files

## 📝 Notes

- Dashboard updates automatically when new data is scraped
- Historical data provides context for current trends
- Responsive design works on all device sizes
- All processing happens client-side for fast performance