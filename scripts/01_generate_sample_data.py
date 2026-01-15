"""
NFL Betting Analysis - Sample Data Generator
Run this script first to create the CSV files needed for the analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set seed for reproducibility
np.random.seed(42)

# Create data directory
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# NFL Teams
teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"
]

# Generate team_epa_2025.csv - EPA metrics for each team
print("Generating team_epa_2025.csv...")
team_epa_data = []
for team in teams:
    # Generate realistic EPA values (typically between -0.3 and 0.3)
    off_epa = np.random.normal(0, 0.12)
    def_epa = np.random.normal(0, 0.12)  # Lower is better for defense
    off_pass_epa = off_epa + np.random.normal(0, 0.05)
    off_rush_epa = off_epa + np.random.normal(-0.05, 0.05)
    def_pass_epa = def_epa + np.random.normal(0, 0.05)
    def_rush_epa = def_epa + np.random.normal(-0.03, 0.05)
    
    team_epa_data.append({
        "team": team,
        "off_epa_per_play": round(off_epa, 4),
        "def_epa_per_play": round(def_epa, 4),
        "off_pass_epa": round(off_pass_epa, 4),
        "off_rush_epa": round(off_rush_epa, 4),
        "def_pass_epa": round(def_pass_epa, 4),
        "def_rush_epa": round(def_rush_epa, 4)
    })

team_epa_df = pd.DataFrame(team_epa_data)
team_epa_df.to_csv(data_dir / "team_epa_2025.csv", index=False)
print(f"  Created: {data_dir / 'team_epa_2025.csv'}")

# Generate team_points_2025.csv - Points per play metrics
print("Generating team_points_2025.csv...")
team_points_data = []
for team in teams:
    # Points per play typically 0.3-0.5, home advantage ~0.02-0.05
    base_ppp = np.random.normal(0.38, 0.05)
    home_bonus = np.random.uniform(0.02, 0.05)
    
    team_points_data.append({
        "team": team,
        "points_per_play": round(base_ppp, 4),
        "points_per_play_home": round(base_ppp + home_bonus, 4),
        "points_per_play_away": round(base_ppp - home_bonus * 0.5, 4),
        "plays_per_game": round(np.random.normal(62, 4), 1)
    })

team_points_df = pd.DataFrame(team_points_data)
team_points_df.to_csv(data_dir / "team_points_2025.csv", index=False)
print(f"  Created: {data_dir / 'team_points_2025.csv'}")

# Generate games_2025.csv - Regular season games with scores
print("Generating games_2025.csv...")
games_data = []
game_id = 1

# Generate 17 weeks of games (simplified - not full NFL schedule)
for week in range(1, 18):
    # Shuffle teams for matchups each week
    shuffled = teams.copy()
    np.random.shuffle(shuffled)
    
    # Create 16 games per week
    for i in range(0, 32, 2):
        home_team = shuffled[i]
        away_team = shuffled[i + 1]
        
        # Get team metrics to influence scores
        home_epa = team_epa_df[team_epa_df["team"] == home_team]["off_epa_per_play"].values[0]
        away_epa = team_epa_df[team_epa_df["team"] == away_team]["off_epa_per_play"].values[0]
        home_def = team_epa_df[team_epa_df["team"] == home_team]["def_epa_per_play"].values[0]
        away_def = team_epa_df[team_epa_df["team"] == away_team]["def_epa_per_play"].values[0]
        
        # Generate scores based on EPA (roughly 20-35 points typical)
        home_base = 24 + (home_epa - away_def) * 30 + np.random.normal(0, 7)
        away_base = 21 + (away_epa - home_def) * 30 + np.random.normal(0, 7)
        
        home_score = max(0, int(round(home_base)))
        away_score = max(0, int(round(away_base)))
        
        games_data.append({
            "game_id": game_id,
            "week": week,
            "date": f"2025-{9 + (week - 1) // 4:02d}-{((week - 1) % 4) * 7 + 8:02d}",
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score
        })
        game_id += 1

games_df = pd.DataFrame(games_data)
games_df.to_csv(data_dir / "games_2025.csv", index=False)
print(f"  Created: {data_dir / 'games_2025.csv'}")

# Generate vegas_lines_divisional.csv - Playoff matchups with Vegas totals
print("Generating vegas_lines_divisional.csv...")

# Pick top teams by offensive EPA for playoffs (simplified)
top_teams = team_epa_df.nlargest(8, "off_epa_per_play")["team"].tolist()

# Create 4 divisional round matchups
vegas_data = [
    {"game_id": 1, "home_team": top_teams[0], "away_team": top_teams[7], "vegas_total": 47.5},
    {"game_id": 2, "home_team": top_teams[1], "away_team": top_teams[6], "vegas_total": 49.0},
    {"game_id": 3, "home_team": top_teams[2], "away_team": top_teams[5], "vegas_total": 45.5},
    {"game_id": 4, "home_team": top_teams[3], "away_team": top_teams[4], "vegas_total": 51.0},
]

vegas_df = pd.DataFrame(vegas_data)
vegas_df.to_csv(data_dir / "vegas_lines_divisional.csv", index=False)
print(f"  Created: {data_dir / 'vegas_lines_divisional.csv'}")

print("\n✓ All sample data files created in ./data/")
print("\nNext step: Run 02_build_model.py to train the game totals model")
