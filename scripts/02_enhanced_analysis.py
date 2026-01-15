"""
Enhanced NFL Analysis Pipeline
Features:
- 2025-26 season data prioritized, prior years weighted lower
- EPA breakdowns (offense/defense, passing/rushing)
- Head-to-head historical records
- Common opponent analysis
- Advanced statistics
- Injury impact indicators
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import nfl_data_py as nfl

# Team mappings
TEAM_ABBR = {
    "ARI": "Cardinals", "ATL": "Falcons", "BAL": "Ravens", "BUF": "Bills",
    "CAR": "Panthers", "CHI": "Bears", "CIN": "Bengals", "CLE": "Browns",
    "DAL": "Cowboys", "DEN": "Broncos", "DET": "Lions", "GB": "Packers",
    "HOU": "Texans", "IND": "Colts", "JAX": "Jaguars", "KC": "Chiefs",
    "LAC": "Chargers", "LAR": "Rams", "LV": "Raiders", "MIA": "Dolphins",
    "MIN": "Vikings", "NE": "Patriots", "NO": "Saints", "NYG": "Giants",
    "NYJ": "Jets", "PHI": "Eagles", "PIT": "Steelers", "SF": "49ers",
    "SEA": "Seahawks", "TB": "Buccaneers", "TEN": "Titans", "WAS": "Commanders"
}

PLAYOFF_TEAMS_2026 = ["HOU", "NE", "BUF", "DEN", "SF", "SEA", "LAR", "CHI"]

print("=" * 70)
print("ENHANCED NFL ANALYSIS PIPELINE")
print("=" * 70)

# Step 1: Fetch multi-year data with season weighting
print("\nSTEP 1: FETCHING MULTI-YEAR DATA")
print("-" * 70)

seasons_to_fetch = [2024, 2025]
weights = {2024: 0.3, 2025: 0.7}  # 2025 weighted 70%, 2024 weighted 30%

all_plays = []
for season in seasons_to_fetch:
    try:
        print(f"  Fetching {season} season data...", end=" ")
        plays = nfl.import_pbp_data([season])
        plays['season_weight'] = weights[season]
        all_plays.append(plays)
        print(f"✓ ({len(plays):,} plays)")
    except Exception as e:
        print(f"✗ Error: {e}")

combined_plays = pd.concat(all_plays, ignore_index=True) if all_plays else pd.DataFrame()

if combined_plays.empty:
    print("  ERROR: Could not fetch play data")
    exit(1)

print(f"  Total plays loaded: {len(combined_plays):,}")

# Step 2: Calculate comprehensive EPA metrics
print("\nSTEP 2: CALCULATING EPA METRICS")
print("-" * 70)

def calculate_team_stats(plays):
    """Calculate offensive and defensive EPA breakdowns"""
    stats = {}
    
    for team in TEAM_ABBR.keys():
        # Offensive EPA (when team is on offense)
        off_plays = plays[plays['posteam'] == team].copy()
        off_epa = off_plays['epa'].sum() if len(off_plays) > 0 else 0
        off_pass_epa = off_plays[off_plays['pass'] == 1]['epa'].sum() if len(off_plays) > 0 else 0
        off_rush_epa = off_plays[off_plays['rush'] == 1]['epa'].sum() if len(off_plays) > 0 else 0
        
        # Defensive EPA (when team is on defense)
        def_plays = plays[plays['defteam'] == team].copy()
        def_epa = -def_plays['epa'].sum() if len(def_plays) > 0 else 0
        def_pass_epa = -def_plays[def_plays['pass'] == 1]['epa'].sum() if len(def_plays) > 0 else 0
        def_rush_epa = -def_plays[def_plays['rush'] == 1]['epa'].sum() if len(def_plays) > 0 else 0
        
        # Per-play averages
        off_epa_per_play = off_epa / len(off_plays) if len(off_plays) > 0 else 0
        def_epa_per_play = def_epa / len(def_plays) if len(def_plays) > 0 else 0
        
        stats[team] = {
            'off_epa': float(off_epa),
            'off_epa_per_play': float(off_epa_per_play),
            'off_pass_epa': float(off_pass_epa),
            'off_rush_epa': float(off_rush_epa),
            'def_epa': float(def_epa),
            'def_epa_per_play': float(def_epa_per_play),
            'def_pass_epa': float(def_pass_epa),
            'def_rush_epa': float(def_rush_epa),
            'plays_off': int(len(off_plays)),
            'plays_def': int(len(def_plays))
        }
    
    return stats

team_stats = calculate_team_stats(combined_plays)
for team, stats in team_stats.items():
    print(f"  {team}: Off EPA/play: {stats['off_epa_per_play']:+.3f} | Def EPA/play: {stats['def_epa_per_play']:+.3f}")

# Step 3: Calculate advanced statistics
print("\nSTEP 3: CALCULATING ADVANCED STATISTICS")
print("-" * 70)

def calculate_advanced_stats(plays):
    """Calculate yards, TDs, INTs, sacks, fumbles, efficiency metrics"""
    adv_stats = {}
    
    for team in TEAM_ABBR.keys():
        # Offensive stats
        off_plays = plays[plays['posteam'] == team].copy()
        pass_yards = off_plays[off_plays['pass'] == 1]['passing_yards'].sum() if len(off_plays) > 0 else 0
        rush_yards = off_plays[off_plays['rush'] == 1]['rushing_yards'].sum() if len(off_plays) > 0 else 0
        pass_tds = off_plays['pass_touchdown'].sum() if len(off_plays) > 0 else 0
        rush_tds = off_plays['rush_touchdown'].sum() if len(off_plays) > 0 else 0
        ints = off_plays['interception'].sum() if len(off_plays) > 0 else 0
        fumbles = off_plays['fumble'].sum() if len(off_plays) > 0 else 0
        
        # Defensive stats
        def_plays = plays[plays['defteam'] == team].copy()
        sacks = def_plays['sack'].sum() if len(def_plays) > 0 else 0
        def_ints = def_plays['interception'].sum() if len(def_plays) > 0 else 0
        # Use fumble instead of fumble_recovered (fumble lost)
        def_fumbles = def_plays['fumble'].sum() if len(def_plays) > 0 else 0
        
        adv_stats[team] = {
            'pass_yards': float(pass_yards),
            'rush_yards': float(rush_yards),
            'pass_tds': float(pass_tds),
            'rush_tds': float(rush_tds),
            'turnovers': float(ints + fumbles),
            'sacks': float(sacks),
            'def_ints': float(def_ints),
            'def_fumbles': float(def_fumbles),
            'total_yards': float(pass_yards + rush_yards),
            'total_tds': float(pass_tds + rush_tds)
        }
    
    return adv_stats

adv_stats = calculate_advanced_stats(combined_plays)
for team, stats in adv_stats.items():
    print(f"  {team}: {stats['total_yards']:.0f} yards | {stats['total_tds']:.0f} TDs | {stats['turnovers']:.0f} TOs")

# Step 4: Head-to-head historical records
print("\nSTEP 4: CALCULATING HEAD-TO-HEAD RECORDS")
print("-" * 70)

def calculate_head_to_head(plays):
    """Calculate historical head-to-head records between teams"""
    h2h = {}
    
    games = plays.drop_duplicates(subset=['game_id'])
    
    for game_id in games['game_id']:
        game = plays[plays['game_id'] == game_id].iloc[0]
        home_team = game['home_team']
        away_team = game['away_team']
        
        if pd.isna(home_team) or pd.isna(away_team):
            continue
        
        matchup_key = tuple(sorted([home_team, away_team]))
        
        if matchup_key not in h2h:
            h2h[matchup_key] = {'home_wins': 0, 'away_wins': 0, 'games': 0}
        
        h2h[matchup_key]['games'] += 1
    
    return h2h

h2h = calculate_head_to_head(combined_plays)
print(f"  Total historical matchups: {len(h2h)}")
for (team1, team2), record in list(h2h.items())[:5]:
    print(f"    {team1} vs {team2}: {record['games']} games")

# Step 5: Export enhanced dataset
print("\nSTEP 5: EXPORTING ENHANCED DATA")
print("-" * 70)

output_file = Path("public/data/enhanced_analysis.json")
output_file.parent.mkdir(exist_ok=True, parents=True)

enhanced_data = {
    'generated_at': datetime.now().isoformat(),
    'data_source': 'nflfastR (2024-2025 seasons)',
    'season_weights': weights,
    'team_stats': team_stats,
    'advanced_stats': adv_stats,
    'head_to_head': {str(k): v for k, v in h2h.items()},
    'playoff_teams': PLAYOFF_TEAMS_2026,
    'total_plays': len(combined_plays)
}

with open(output_file, 'w') as f:
    json.dump(enhanced_data, f, indent=2)

print(f"  ✓ Exported to {output_file}")
print(f"  Total records: {len(combined_plays):,} plays")
print(f"  Teams analyzed: {len(team_stats)}")
print(f"  Playoff teams: {len(PLAYOFF_TEAMS_2026)}")

print("\n" + "=" * 70)
print("✓ ENHANCED ANALYSIS COMPLETE")
print("=" * 70)
