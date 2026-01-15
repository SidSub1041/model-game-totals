# NFL Betting Analysis - Game Totals Model

Compare your model's projected game totals against Vegas lines to find betting edges.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Option A: Use Real nflfastR Data (Recommended)**
   ```bash
   python fetch_nflfastr_data.py  # Fetches real NFL data, exports to JSON
   ```
   This fetches play-by-play data from nflfastR, calculates EPA metrics, trains the model, and exports projections to `public/data/nfl_analysis.json` for the dashboard.

3. **Option B: Use Sample Data**
   ```bash
   python nfl_betting_complete.py  # All-in-one with generated sample data
   ```

## Full Pipeline (nflfastR + Dashboard)

1. Run the Python script to fetch real data:
   ```bash
   python scripts/fetch_nflfastr_data.py
   ```

2. Start the Next.js dashboard:
   ```bash
   npm run dev
   ```

3. View projections at `http://localhost:3000`

## Files

| File | Description |
|------|-------------|
| `fetch_nflfastr_data.py` | **NEW** - Fetches real nflfastR data, exports JSON for dashboard |
| `nfl_betting_complete.py` | All-in-one script with sample data (no file dependencies) |
| `01_generate_sample_data.py` | Generates realistic NFL sample data |
| `02_build_model.py` | Loads CSVs, builds features, trains model |
| `03_project_playoffs.py` | Projects playoff totals and compares to Vegas |
| `04_analysis_utils.py` | Reusable functions for weekly updates |

## nflfastR Data Pipeline

The `fetch_nflfastr_data.py` script:
1. Fetches play-by-play data from nflfastR via `nfl_data_py`
2. Calculates team EPA metrics (offensive/defensive, pass/rush)
3. Calculates scoring metrics (PPG, plays per game)
4. Trains a linear regression model on game totals
5. Projects playoff matchups vs Vegas lines
6. Exports everything to JSON for the dashboard

### Configuring Playoff Matchups

Edit the `PLAYOFF_MATCHUPS` list in `fetch_nflfastr_data.py`:

```python
PLAYOFF_MATCHUPS = [
    {"home_team": "KC", "away_team": "HOU", "game_date": "2025-01-18", "game_time": "4:30 PM ET", "vegas_total": 48.5},
    # Add more matchups...
]
```

## Dashboard Features

- Game cards showing matchup, date/time, and projections
- EPA metrics (offensive/defensive) for each team
- Model vs Vegas comparison with edge calculation
- Recommendation badges (OVER/UNDER/HOLD)
- Model performance metrics (R², MAE, RMSE)

## Weekly Updates

1. Update `PLAYOFF_MATCHUPS` in `fetch_nflfastr_data.py` with fresh Vegas lines
2. Rerun `python scripts/fetch_nflfastr_data.py`
3. Refresh the dashboard to see updated projections

## Output Example

```
DIVISIONAL ROUND - MODEL vs VEGAS TOTALS
=============================================
home_team away_team  model_total  vegas_total  edge   signal
       KC       HOU         51.2         48.5   2.7     OVER
      PHI       LAR         42.1         44.0  -1.9     HOLD
      BUF       BAL         52.8         51.5   1.3     HOLD
      DET       WAS         58.3         55.5   2.8     OVER
```

Interpretation:
- **Positive edge**: Model projects higher than Vegas (lean OVER)
- **Negative edge**: Model projects lower than Vegas (lean UNDER)
- **|edge| > 2 points**: Potential betting edge (OVER/UNDER recommendation)
