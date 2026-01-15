# NFL Betting Analysis Dashboard - Data Fetching Guide

## Overview
This project uses **web scraping** instead of paid APIs to fetch live Vegas lines and NFL data for the dashboard.

## Scripts

### 1. `fetch_vegas_lines_advanced.py` (PRIMARY - RECOMMENDED)
**Automatically fetches real Vegas lines from multiple sources**

```bash
python3 scripts/fetch_vegas_lines_advanced.py
```

**Features:**
- ✅ Automatically identifies this weekend's NFL games
- ✅ Scrapes Vegas odds from ESPN, Reddit, Covers.com
- ✅ Extracts over/under and spread data
- ✅ Falls back to hardcoded games if scraping fails
- ✅ No manual input required
- Outputs to: `public/data/vegas_lines.json`

**How it works:**
1. Fetches NFL schedule from ESPN
2. Tries multiple betting data sources:
   - ESPN Betting Lines
   - Reddit r/sportsbook
   - Sports betting aggregators
3. Merges schedule with odds
4. Falls back to hardcoded data if scraping fails

---

### 2. `fetch_vegas_lines_scraper.py` (FALLBACK)
**Simpler web scraper with hardcoded fallback games**

```bash
python3 scripts/fetch_vegas_lines_scraper.py
```

**Features:**
- Falls back to hardcoded Divisional Round games
- Outputs to: `public/data/vegas_lines.json`

---

### 2. `fetch_nflfastr_data.py` (SECONDARY)
**Trains model on historical NFL data and generates predictions**

```bash
python3 scripts/fetch_nflfastr_data.py
```

**Features:**
- Fetches 2024 NFL play-by-play data from nflfastR
- Calculates team EPA metrics
- Trains prediction model on 272 regular season games
- Reads Vegas lines from `vegas_lines.json`
- Generates predictions for weekend games
- Outputs to: `public/data/nfl_analysis.json`

---

## Complete Workflow

To update the dashboard with current data:

```bash
# Automatic - scrapes real Vegas lines automatically
bash update_data.sh

# Or manual - run scripts individually
python3 scripts/fetch_vegas_lines_advanced.py  # Get Vegas lines
python3 scripts/fetch_nflfastr_data.py         # Generate predictions

# View the dashboard
npm run dev
# Open http://localhost:3000
```

**What happens automatically:**
✅ Identifies this weekend's NFL games
✅ Fetches Vegas over/under and spreads
✅ Trains model on 2024 NFL data
✅ Generates predictions vs Vegas
✅ Outputs to JSON files

---

## Data Flow

```
fetch_vegas_lines_scraper.py
        ↓
   public/data/vegas_lines.json (Vegas odds for this weekend)
        ↓
fetch_nflfastr_data.py
        ↓
   public/data/nfl_analysis.json (Model predictions + Vegas lines)
        ↓
   Dashboard (http://localhost:3000)
```

---

## Why Web Scraping?

❌ **Paid APIs** - Most reliable sources (The-Odds-API, SportsData.io) have paywalls
❌ **Free APIs** - Limited data, rate-limited, often outdated
✅ **Web Scraping** - Free, real-time data from public websites

---

## Limitations & Future Improvements

1. **Anti-scraping measures** - Some sites may block requests
   - Solution: Use rotating proxies or headless browser (Selenium)

2. **HTML structure changes** - Website updates break selectors
   - Solution: Implement fallback selectors and alerts

3. **Rate limiting** - Too many requests get blocked
   - Solution: Add delays between requests (already implemented)

---

## Requirements

- Python 3.9+
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast HTML/XML processing
- `requests` - HTTP requests
- `nfl_data_py` - NFL historical data
- `pandas`, `numpy`, `scikit-learn` - Data processing

Install all:
```bash
pip3 install -r scripts/requirements.txt beautifulsoup4 lxml
```

---

## Manual Vegas Lines Update

If scraping fails, manually update `public/data/vegas_lines.json`:

```json
{
  "generatedAt": "2026-01-14T...",
  "gamesCount": 4,
  "games": [
    {
      "id": "1",
      "date": "2026-01-18T15:00Z",
      "home_team": "KC",
      "home_team_name": "Chiefs",
      "away_team": "HOU",
      "away_team_name": "Texans",
      "over_under": 44.5,
      "spread": -6.5,
      "status": "Scheduled"
    }
    // ... more games
  ]
}
```

---

## Troubleshooting

**"Web scraping unsuccessful, using hardcoded games"**
- All scrapers failed - check internet connection
- ESPN/Bleacher Report may be blocking requests
- Solution: Use hardcoded data or add API key to `fetch_vegas_lines.py`

**"No Vegas lines found"**
- Make sure `fetch_vegas_lines_scraper.py` ran successfully first
- Check `public/data/vegas_lines.json` exists

**"Games projected: 0"**
- Vegas lines file is empty
- Run `fetch_vegas_lines_scraper.py` first
- Manually update games in `public/data/vegas_lines.json`

---

## Next Steps

To make this production-ready:

1. **Add error handling** - Email alerts on scraping failures
2. **Database** - Store historical Vegas lines and results
3. **Cron job** - Automate scripts to run before market open
4. **Dashboard** - Display prediction confidence and accuracy over time
5. **Paid API** - Consider The-Odds-API free tier (500 requests/month) for reliability
