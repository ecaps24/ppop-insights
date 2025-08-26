# Historical Sample Data

## 📊 Overview
This directory contains generated historical sample data covering the past 30 days for SB19 and BINI music analytics.

## 📁 Files Created

### `historical_monthly_listeners.csv`
- **Records**: 60 (30 days × 2 artists)
- **Frequency**: Daily data points
- **Time Range**: July 25, 2025 to August 23, 2025
- **Data Points**: Monthly listener counts with realistic daily variations

### `historical_comprehensive_data.csv`  
- **Records**: 40 (4 weeks × 10 songs)
- **Frequency**: Weekly data points
- **Time Range**: Past 4 weeks
- **Data Points**: Top 5 songs per artist with stream counts

## 📈 Data Characteristics

### Monthly Listeners Trends
- **SB19**: Started around 1.71M, gradual growth to 1.72M
- **BINI**: Started around 1.97M, faster growth trend
- **Variations**: Realistic daily fluctuations (±2K to ±12K)
- **Growth Pattern**: BINI showing faster growth rate

### Stream Count Evolution
- **SB19 Top Song (MAPA)**: ~78.3M to ~78.9M streams
- **BINI Top Song (Pantropiko)**: ~190.6M to ~191.2M streams
- **Growth Rate**: BINI songs showing higher daily stream increases

## 🎯 Key Insights from Sample Data

### Competition Status
1. **BINI** is leading in monthly listeners (1.98M vs 1.72M)
2. **BINI** dominates stream counts (Pantropiko: 191M vs MAPA: 79M)
3. **BINI** shows faster growth trajectory
4. **Top 3 songs globally** are all BINI tracks

### Realistic Patterns Included
- Daily variations in monthly listeners
- Weekly growth in stream counts  
- Seasonal fluctuations
- Realistic growth rates based on current performance

## 🚀 Usage

### Combining with Real Data
```bash
# Merge historical with current scheduled data
cat historical_monthly_listeners.csv > combined_monthly_data.csv
tail -n +2 scheduled_monthly_listeners.csv >> combined_monthly_data.csv
```

### Analysis Examples
- Track monthly listener growth trends
- Compare stream count evolution
- Identify breakthrough moments
- Monitor competitive dynamics

## ⚠️ Important Notes

1. **Sample Data**: This is realistic but simulated data
2. **Baseline**: Use as historical context for real tracking
3. **Growth Trends**: Based on current performance patterns
4. **Date Format**: Standard YYYY-MM-DD HH:MM:SS format
5. **Continuity**: Designed to seamlessly connect with live scraped data

## 🔄 Next Steps

Your automated scrapers will continue from current real values:
- **SB19**: 1,720,632 monthly listeners (exact)
- **BINI**: 1,977,848 monthly listeners (exact)

The historical data provides context for understanding growth patterns and competitive dynamics over the past month.