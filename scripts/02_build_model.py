"""
NFL Betting Analysis - Model Training
Loads CSVs, builds training features with pandas, and fits a regression model.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import pickle
from pathlib import Path

data_dir = Path("data")
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

# ============================================================================
# B. Load CSVs
# ============================================================================
print("Loading CSV files...")

team_epa_df = pd.read_csv(data_dir / "team_epa_2025.csv")
team_points_df = pd.read_csv(data_dir / "team_points_2025.csv")
games_df = pd.read_csv(data_dir / "games_2025.csv")

print(f"  ✓ Loaded {len(team_epa_df)} teams with EPA metrics")
print(f"  ✓ Loaded {len(team_points_df)} teams with points metrics")
print(f"  ✓ Loaded {len(games_df)} games from 2025 season")

# ============================================================================
# C. Build training table with pandas (replaces DuckDB SQL)
# ============================================================================
print("\nBuilding training features with pandas...")

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

# Sort by week and game_id
game_features_df = game_features_df.sort_values(["week", "game_id"]).reset_index(drop=True)

print(f"  ✓ Built training table with {len(game_features_df)} games and {len(game_features_df.columns)} features")

# Save training data for reference
game_features_df.to_csv(data_dir / "game_features_2025.csv", index=False)

# ============================================================================
# D. Fit regression model for game totals
# ============================================================================
print("\nTraining Linear Regression model...")

# Define features for the model
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

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Evaluate
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)

print(f"  ✓ Model trained successfully")
print(f"  R² Score: {r2:.4f}")
print(f"  Mean Absolute Error: {mae:.2f} points")

# Display feature importances
print("\n  Feature Coefficients:")
coef_df = pd.DataFrame({
    "feature": feature_columns,
    "coefficient": model.coef_
}).sort_values("coefficient", key=abs, ascending=False)

for _, row in coef_df.head(8).iterrows():
    print(f"    {row['feature']}: {row['coefficient']:.3f}")

# Save the model
model_data = {
    "model": model,
    "feature_columns": feature_columns,
    "r2_score": r2,
    "mae": mae
}
with open(models_dir / "total_points_model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print(f"\n✓ Model saved to {models_dir / 'total_points_model.pkl'}")
print("\nNext step: Run 03_project_playoffs.py to compare model vs Vegas lines")
