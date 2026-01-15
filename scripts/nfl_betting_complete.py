"""
NFL Betting Analysis - Complete All-in-One Script
This script generates sample data, trains the model, and outputs projections
all in a single execution. No file persistence required between runs.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# ============================================================================
# A. GENERATE SAMPLE DATA (in-memory)
# ============================================================================
print("=" * 70)
print("STEP 1: GENERATING SAMPLE DATA")
print("=" * 70)

np.random.seed(42)

# NFL Teams
teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"
]

# Generate team_epa data
print("  Generating team EPA metrics...")
team_epa_data = []
for team in teams:
    off_epa = np.random.normal(0, 0.12)
    def_epa = np.random.normal(0, 0.12)
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

# Generate team_points data
print("  Generating team points metrics...")
team_points_data = []
for team in teams:
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

# Generate games data
print("  Generating regular season games...")
games_data = []
game_id = 1

for week in range(1, 18):
    shuffled = teams.copy()
    np.random.shuffle(shuffled)
    
    for i in range(0, 32, 2):
        home_team = shuffled[i]
        away_team = shuffled[i + 1]
        
        home_epa = team_epa_df[team_epa_df["team"] == home_team]["off_epa_per_play"].values[0]
        away_epa = team_epa_df[team_epa_df["team"] == away_team]["off_epa_per_play"].values[0]
        home_def = team_epa_df[team_epa_df["team"] == home_team]["def_epa_per_play"].values[0]
        away_def = team_epa_df[team_epa_df["team"] == away_team]["def_epa_per_play"].values[0]
        
        home_base = 24 + (home_epa - away_def) * 30 + np.random.normal(0, 7)
        away_base = 21 + (away_epa - home_def) * 30 + np.random.normal(0, 7)
        
        home_score = max(0, int(round(home_base)))
        away_score = max(0, int(round(away_base)))
        
        games_data.append({
            "game_id": game_id,
            "week": week,
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score
        })
        game_id += 1

games_df = pd.DataFrame(games_data)

# Generate Vegas lines for divisional round
print("  Generating Vegas lines for divisional round...")
top_teams = team_epa_df.nlargest(8, "off_epa_per_play")["team"].tolist()

vegas_data = [
    {"game_id": 1, "home_team": top_teams[0], "away_team": top_teams[7], "vegas_total": 47.5},
    {"game_id": 2, "home_team": top_teams[1], "away_team": top_teams[6], "vegas_total": 49.0},
    {"game_id": 3, "home_team": top_teams[2], "away_team": top_teams[5], "vegas_total": 45.5},
    {"game_id": 4, "home_team": top_teams[3], "away_team": top_teams[4], "vegas_total": 51.0},
]

vegas_df = pd.DataFrame(vegas_data)

print(f"  Generated {len(team_epa_df)} teams, {len(games_df)} games, {len(vegas_df)} playoff matchups")

# ============================================================================
# B. BUILD TRAINING TABLE
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: BUILDING TRAINING FEATURES")
print("=" * 70)

# Join home team EPA metrics
game_features_df = games_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "home_off_epa",
        "off_pass_epa": "home_off_pass_epa",
        "off_rush_epa": "home_off_rush_epa",
        "def_epa_per_play": "home_def_epa",
        "def_pass_epa": "home_def_pass_epa",
        "def_rush_epa": "home_def_rush_epa"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team EPA metrics
game_features_df = game_features_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "away_off_epa",
        "off_pass_epa": "away_off_pass_epa",
        "off_rush_epa": "away_off_rush_epa",
        "def_epa_per_play": "away_def_epa",
        "def_pass_epa": "away_def_pass_epa",
        "def_rush_epa": "away_def_rush_epa"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join home team points metrics
game_features_df = game_features_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "home_points_per_play",
        "points_per_play_home": "home_ppp_at_home",
        "points_per_play_away": "home_ppp_on_road",
        "plays_per_game": "home_plays_per_game"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team points metrics
game_features_df = game_features_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "away_points_per_play",
        "points_per_play_home": "away_ppp_at_home",
        "points_per_play_away": "away_ppp_on_road",
        "plays_per_game": "away_plays_per_game"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Compute derived features
game_features_df["total_points"] = game_features_df["home_score"] + game_features_df["away_score"]
game_features_df["off_epa_diff"] = game_features_df["home_off_epa"] - game_features_df["away_off_epa"]
game_features_df["def_epa_diff"] = game_features_df["home_def_epa"] - game_features_df["away_def_epa"]
game_features_df["ppp_diff"] = game_features_df["home_points_per_play"] - game_features_df["away_points_per_play"]
game_features_df["home_matchup_edge"] = game_features_df["home_off_epa"] - game_features_df["away_def_epa"]
game_features_df["away_matchup_edge"] = game_features_df["away_off_epa"] - game_features_df["home_def_epa"]

print(f"  Built training table: {len(game_features_df)} games x {len(game_features_df.columns)} features")

# ============================================================================
# C. TRAIN MODEL
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: TRAINING LINEAR REGRESSION MODEL")
print("=" * 70)

feature_columns = [
    "home_off_epa", "home_def_epa", "home_off_pass_epa", "home_off_rush_epa",
    "away_off_epa", "away_def_epa", "away_off_pass_epa", "away_off_rush_epa",
    "home_points_per_play", "away_points_per_play",
    "home_plays_per_game", "away_plays_per_game",
    "off_epa_diff", "def_epa_diff",
    "home_matchup_edge", "away_matchup_edge"
]

X = game_features_df[feature_columns]
y = game_features_df["total_points"]

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)

print(f"  Model trained successfully")
print(f"  R-squared: {r2:.4f}")
print(f"  Mean Absolute Error: {mae:.2f} points")

print("\n  Top Feature Coefficients:")
coef_df = pd.DataFrame({
    "feature": feature_columns,
    "coefficient": model.coef_
}).sort_values("coefficient", key=abs, ascending=False)

for _, row in coef_df.head(6).iterrows():
    print(f"    {row['feature']}: {row['coefficient']:.3f}")

# ============================================================================
# D. BUILD PLAYOFF FEATURES & PROJECT
# ============================================================================
print("\n" + "=" * 70)
print("STEP 4: PROJECTING DIVISIONAL ROUND TOTALS")
print("=" * 70)

# Join home team EPA metrics
playoff_features_df = vegas_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "home_off_epa",
        "off_pass_epa": "home_off_pass_epa",
        "off_rush_epa": "home_off_rush_epa",
        "def_epa_per_play": "home_def_epa",
        "def_pass_epa": "home_def_pass_epa",
        "def_rush_epa": "home_def_rush_epa"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team EPA metrics
playoff_features_df = playoff_features_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "away_off_epa",
        "off_pass_epa": "away_off_pass_epa",
        "off_rush_epa": "away_off_rush_epa",
        "def_epa_per_play": "away_def_epa",
        "def_pass_epa": "away_def_pass_epa",
        "def_rush_epa": "away_def_rush_epa"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join home team points metrics
playoff_features_df = playoff_features_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "home_points_per_play",
        "points_per_play_home": "home_ppp_at_home",
        "points_per_play_away": "home_ppp_on_road",
        "plays_per_game": "home_plays_per_game"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team points metrics
playoff_features_df = playoff_features_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "away_points_per_play",
        "points_per_play_home": "away_ppp_at_home",
        "points_per_play_away": "away_ppp_on_road",
        "plays_per_game": "away_plays_per_game"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Compute derived features
playoff_features_df["off_epa_diff"] = playoff_features_df["home_off_epa"] - playoff_features_df["away_off_epa"]
playoff_features_df["def_epa_diff"] = playoff_features_df["home_def_epa"] - playoff_features_df["away_def_epa"]
playoff_features_df["ppp_diff"] = playoff_features_df["home_points_per_play"] - playoff_features_df["away_points_per_play"]
playoff_features_df["home_matchup_edge"] = playoff_features_df["home_off_epa"] - playoff_features_df["away_def_epa"]
playoff_features_df["away_matchup_edge"] = playoff_features_df["away_off_epa"] - playoff_features_df["home_def_epa"]

# Predict totals
X_playoff = playoff_features_df[feature_columns]
playoff_features_df["model_total"] = model.predict(X_playoff)
playoff_features_df["difference"] = playoff_features_df["model_total"] - playoff_features_df["vegas_total"]

# Determine betting signal
def get_signal(diff):
    if diff > 2:
        return "OVER"
    elif diff < -2:
        return "UNDER"
    else:
        return "NO EDGE"

playoff_features_df["signal"] = playoff_features_df["difference"].apply(get_signal)

# ============================================================================
# E. DISPLAY FINAL RESULTS
# ============================================================================
print("\n" + "=" * 70)
print("DIVISIONAL ROUND - MODEL vs VEGAS TOTALS")
print("=" * 70)

results = playoff_features_df[["home_team", "away_team", "model_total", "vegas_total", "difference", "signal"]].copy()
results["model_total"] = results["model_total"].round(1)
results["difference"] = results["difference"].round(1)

print("\n" + results.to_string(index=False))

print("\n" + "-" * 70)
print("INTERPRETATION:")
print("  Positive difference -> Model projects HIGHER than Vegas (lean OVER)")
print("  Negative difference -> Model projects LOWER than Vegas (lean UNDER)")
print("  |difference| > 2 points = potential betting edge")
print("-" * 70)

# Summary stats
print("\n" + "=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)
print(f"  Average model total: {results['model_total'].mean():.1f}")
print(f"  Average Vegas total: {results['vegas_total'].mean():.1f}")
print(f"  Average difference:  {results['difference'].mean():.1f}")
print(f"  Games with OVER signal:  {len(results[results['signal'] == 'OVER'])}")
print(f"  Games with UNDER signal: {len(results[results['signal'] == 'UNDER'])}")
print(f"  Games with no edge:      {len(results[results['signal'] == 'NO EDGE'])}")
