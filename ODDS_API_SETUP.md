# Getting Real Vegas Lines - The-Odds-API Setup

## Free API Setup (500 requests/month)

### Step 1: Sign Up
Visit https://the-odds-api.com and create a free account
- No credit card required
- 500 requests per month (plenty for daily updates)
- Real-time Vegas odds from multiple sportsbooks

### Step 2: Get Your API Key
1. Log in to your account
2. Go to the Dashboard
3. Copy your API key

### Step 3: Add to Your Project

Create a `.env` file in the project root:

```bash
# .env
THE_ODDS_API_KEY=your_api_key_here
```

### Step 4: Use the Script

```bash
# Fetch real Vegas lines from The-Odds-API
python3 scripts/fetch_via_odds_api.py

# Then run predictions
python3 scripts/fetch_nflfastr_data.py

# Or both at once
bash update_data.sh
```

## What You Get

✅ **Real-time Vegas odds** from DraftKings, FanDuel, etc.
✅ **Over/Under totals** for every game
✅ **Spreads** for every matchup
✅ **Updated multiple times per day**

## Data Available

- Live odds from 50+ sportsbooks
- Games for this weekend automatically detected
- Spreads, totals, moneylines
- Decimal and American odds formats

## API Limits

- Free tier: 500 requests/month (~16 per day)
- Easily enough for once-daily updates
- Upgrade to paid plan for more frequent updates

## Pricing

- **Free**: 500 requests/month
- **$9/month**: 5,000 requests
- **$99/month**: 100,000 requests

## Troubleshooting

**"No API key found"**
- Make sure `.env` file exists in project root
- Set `THE_ODDS_API_KEY=your_key_here`
- Restart the script

**"Invalid API key"**
- Double-check the key is copied correctly
- No extra spaces or quotes

**"Rate limit exceeded"**
- You've hit the 500 request/month limit
- Either wait for next month or upgrade plan

## Usage Flow

```
update_data.sh
    ↓
fetch_via_odds_api.py (if API key set)
    ↓
fetch_vegas_lines_advanced.py (fallback scraper)
    ↓
public/data/vegas_lines.json
    ↓
fetch_nflfastr_data.py
    ↓
public/data/nfl_analysis.json
    ↓
Dashboard displays real Vegas lines + predictions
```

This gives you the best of both worlds:
- **Primary**: Real API data when available
- **Fallback**: Web scraping if API fails
- **Always works**: Hardcoded data as last resort
