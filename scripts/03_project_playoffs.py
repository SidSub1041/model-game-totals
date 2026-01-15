"""
NFL Betting Analysis - Playoff Projections
Compares model predictions against Vegas lines to find betting edges.
"""

import pandas as pd
import pickle
from pathlib import Path

data_dir = Path("data")
models_dir = Path("models")

# ============================================================================
# Load the trained model
# ============================================================================
print("Loading trained model...")
with open(models_dir / "total_points_model.pkl", "rb") as f:
    model_data = pickle.load(f)

model = model_data["model"]
feature_columns = model_data["feature_columns"]
print(f"  ✓ Model loaded (R²: {model_data['r2_score']:.4f}, MAE: {model_data['mae']:.2f})")

# ============================================================================
# E. Build features for divisional round matchups
# ============================================================================
print("\nLoading team metrics and Vegas lines...")

team_epa_df = pd.read_csv(data_dir / "team_epa_2025.csv")
team_points_df = pd.read_csv(data_dir / "team_points_2025.csv")
vegas_df = pd.read_csv(data_dir / "vegas_lines_divisional.csv")

print(f"  ✓ Loaded {len(vegas_df)} divisional round matchups")

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

# ============================================================================
# F. Compare model projections vs Vegas totals
# ============================================================================
print("\nGenerating model projections...")

# Extract features for prediction
X_future = playoff_features_df[feature_columns]

# Predict totals
playoff_features_df["model_total"] = model.predict(X_future)
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
# Display Results
# ============================================================================
print("\n" + "=" * 70)
print("DIVISIONAL ROUND - MODEL vs VEGAS TOTALS")
print("=" * 70)

results = playoff_features_df[["home_team", "away_team", "model_total", "vegas_total", "difference", "signal"]]
results = results.copy()
results["model_total"] = results["model_total"].round(1)
results["difference"] = results["difference"].round(1)

print(results.to_string(index=False))

print("\n" + "-" * 70)
print("INTERPRETATION:")
print("  Positive difference → Model projects HIGHER than Vegas (lean OVER)")
print("  Negative difference → Model projects LOWER than Vegas (lean UNDER)")
print("  |difference| > 2 points = potential betting edge")
print("-" * 70)

# Save results
results.to_csv(data_dir / "projections_divisional.csv", index=False)
print(f"\n✓ Projections saved to {data_dir / 'projections_divisional.csv'}")
