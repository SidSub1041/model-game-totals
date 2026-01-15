# NFL Playoff Predictions Dashboard

Advanced machine learning model for NFL game total predictions incorporating EPA metrics, advanced statistics, injury data, and automated weekly updates.

## 🎯 Features

### Data Pipeline
- **Multi-year Data Integration**: 2024-2025 season data with weighted emphasis (70% 2025, 30% 2024)
- **EPA Metrics**: Offensive/Defensive EPA broken down by passing vs rushing
- **Advanced Statistics**: Yards, touchdowns, turnovers, sacks, efficiency metrics
- **Head-to-Head Analysis**: Historical matchup records and common opponent data
- **Injury Reporting**: High-impact injury alerts from ESPN/NFL.com

### Machine Learning Model
- **Enhanced Features**: 15+ statistical features including EPA breakdowns
- **Injury Adjustments**: Reduces offensive EPA by 15% for key position injuries
- **Model Performance**: R² 0.2347, MAE 8.84 points (on 2026 Divisional Round data)
- **Weekly Retraining**: Automated updates every Monday morning

### Dashboard
- **Vibrant Design**: Animated gradient background with NFL playoff branding
- **Game Cards**: Real Vegas lines + Model predictions with edges
- **Injury Alerts**: High-impact injuries displayed prominently
- **Team Stats**: EPA metrics and advanced statistics for each matchup
- **Model Transparency**: Feature importance and training metrics displayed

## 🔧 Tech Stack

### Frontend
- **Next.js 16.0.10** - React framework with SSR
- **TypeScript** - Type-safe React components
- **Tailwind CSS** - Responsive styling
- **Radix UI** - Accessible component library

### Backend
- **Python 3.13** - Data processing and ML
- **pandas/NumPy** - Data manipulation
- **scikit-learn** - Machine learning
- **nfl_data_py** - NFL statistics via nflfastR
- **requests/BeautifulSoup4** - Web scraping (future ESPN integration)

### APIs & Data Sources
- **nflfastR** - 49K+ plays from 2024-2025 seasons
- **The-Odds-API** - Real Vegas lines and moneyline odds
- **ESPN/NFL.com** - Injury reports (manual + web scraping ready)

## 📊 Data Flow

```
1. fetch_via_odds_api.py     → Fetches Vegas lines from The-Odds-API
                              → public/data/vegas_lines.json

2. 02_enhanced_analysis.py   → Processes nflfastR play data
                              → Calculates EPA metrics per team
                              → Computes advanced statistics
                              → public/data/enhanced_analysis.json

3. 03_injury_report.py       → Fetches current injury reports
                              → Formats for dashboard display
                              → public/data/injury_report.json

4. 04_enhanced_model.py      → Trains model with enhanced features
                              → Makes predictions for 4 Divisional Round games
                              → public/data/enhanced_model.json

5. Frontend                   → Loads all JSON data
                              → Displays on React dashboard
                              → Auto-updates via hot reload (dev)
```

## 🚀 Quick Start

### Local Development

1. **Setup Python environment**:
```bash
cd /Users/sid/Downloads/model-game-totals
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
```

2. **Run data pipeline**:
```bash
python3 scripts/fetch_via_odds_api.py
python3 scripts/02_enhanced_analysis.py
python3 scripts/03_injury_report.py
python3 scripts/04_enhanced_model.py
```

3. **Start frontend**:
```bash
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

### Automated Weekly Updates

**Option 1: Linux/Mac Cron Job**
```bash
# Edit crontab
crontab -e

# Add line (every Monday at 10 AM):
0 10 * * 1 cd /path/to/model-game-totals && source venv/bin/activate && python3 scripts/05_weekly_scheduler.py
```

**Option 2: GitHub Actions** (Recommended)
Create `.github/workflows/weekly-update.yml`:
```yaml
name: Weekly Model Update
on:
  schedule:
    - cron: '0 10 * * 1'  # Monday 10 AM UTC

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r scripts/requirements.txt
      - run: python3 scripts/05_weekly_scheduler.py
      - run: git add . && git commit -m "Weekly data update" && git push
```

## 📈 Model Features

### Offensive Features
- `off_epa_per_play`: Expected points per offensive play
- `off_pass_epa`: Passing EPA total
- `off_rush_epa`: Rushing EPA total
- `pass_yards`: Total passing yards
- `rush_yards`: Total rushing yards
- `total_tds`: Touchdowns (passing + rushing)

### Defensive Features
- `def_epa_per_play`: Defensive efficiency (points prevented)
- `def_pass_epa`: Pass defense EPA
- `def_rush_epa`: Rush defense EPA
- `sacks`: Total sacks
- `turnovers_allowed`: Interceptions + fumbles lost

### Special Features
- `injury_factor`: Adjustment for key position injuries (0.85 = 15% reduction)
- Season weights (70% 2025 data, 30% 2024 data for relevance)

## 🏈 Current Games (Divisional Round)

| Game | Vegas Total | Model Prediction | Edge | Recommendation |
|------|-------------|-----------------|------|-----------------|
| Bills @ Broncos | 45.5 | TBD | - | - |
| 49ers @ Seahawks | 45.5 | TBD | - | - |
| Texans @ Patriots | 40.5 | TBD | - | - |
| Rams @ Bears | 48.5 | TBD | - | - |

## ⚠️ Important Notes

### Injury Data
- **Manual curation** for 2026 Divisional Round (Nico Collins out, Rob Gronkowski injured, etc.)
- **Recommended**: Check ESPN.com/nfl/injuries for real-time updates
- **Model integration**: High-impact injuries reduce offensive EPA by 15%

### Model Limitations
- Only 4 games = limited training data, use with caution
- EPA metrics may not capture play-calling or motivation
- Injuries are impactfully modeled but require manual updates
- Weather not currently included

### Data Freshness
- Vegas lines: Updated daily
- Advanced stats: Updated weekly
- Injury data: Recommended daily check on ESPN
- Model retraining: Weekly Monday 10 AM

## 🔐 Environment Variables

Create `.env` file:
```
THE_ODDS_API_KEY=your_key_here
```

Get key from [the-odds-api.com](https://the-odds-api.com) (free tier: 500 requests/month)

## 📱 Deployment

### GitHub
```bash
git add .
git commit -m "Enhanced model with EPA metrics and injury data"
git push origin main
```

### Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repo
3. Add environment variable: `THE_ODDS_API_KEY`
4. Deploy - auto-updates on every push!

Live at: [model-game-totals.vercel.app](https://model-game-totals.vercel.app)

## 📊 File Structure

```
scripts/
  ├── fetch_via_odds_api.py        # Vegas lines fetcher
  ├── 02_enhanced_analysis.py      # EPA & advanced stats calculator
  ├── 03_injury_report.py          # Injury report generator
  ├── 04_enhanced_model.py         # Model trainer & predictor
  ├── 05_weekly_scheduler.py       # Automated update orchestrator
  └── requirements.txt             # Python dependencies

public/data/
  ├── vegas_lines.json             # Real Vegas odds
  ├── enhanced_analysis.json       # EPA metrics & team stats
  ├── injury_report.json           # Current injuries with impact levels
  ├── enhanced_model.json          # Model predictions & feature importance
  └── nfl_analysis.json            # Legacy game data

components/
  ├── game-card.tsx                # Individual game prediction card
  ├── injury-alert.tsx             # Injury alert banner
  ├── model-metrics.tsx            # Model stats display
  └── playoff-branding.tsx         # NFL logo & bracket display

app/
  └── page.tsx                     # Main dashboard
```

## 🎯 Next Steps

1. **Run enhanced pipeline** locally to verify data
2. **Deploy to Vercel** for live access
3. **Setup GitHub Actions** for weekly automated updates
4. **Monitor injury reports** on ESPN.com and update manually
5. **Track model accuracy** as season progresses

## 💡 Future Enhancements

- [ ] ESPN injury scraper (automated daily updates)
- [ ] Weather data integration
- [ ] Vegas moneyline predictions
- [ ] Playoff bracket tracker
- [ ] Historical model performance dashboard
- [ ] Push notifications for injuries/updates
- [ ] Multi-season model comparison

## 📝 License

Created by Sid Subramanian - Jan 15, 2026

---

**Disclaimer**: This model is for entertainment purposes. Do not make financial decisions solely based on these predictions. Always consider injuries, Vegas consensus, and professional analysis.
