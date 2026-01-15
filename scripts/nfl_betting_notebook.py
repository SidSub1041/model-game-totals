# %% [markdown]
# # NFL Betting Analysis - Game Totals Model
# 
# This notebook demonstrates the complete workflow for comparing your model's 
# projected game totals against Vegas lines to find betting edges.
# 
# **Workflow:**
# 1. Generate sample data (or load your own CSVs)
# 2. Build training features with pandas
# 3. Train a Linear Regression model
# 4. Project playoff matchups and compare to Vegas

# %%
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from pathlib import Path

# Create directories
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# %% [markdown]
# ## Step 1: Generate Sample Data
# 
# This creates realistic NFL team metrics and game results.
# Replace this with your actual data by loading your own CSVs.

# %%
np.random.seed(42)

teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"
]

# Team EPA metrics
team_epa_data = []
for team in teams:
    off_epa = np.random.normal(0, 0.12)
    def_epa = np.random.normal(0, 0.12)
    team_epa_data.append({
        "team": team,
        "off_epa_per_play": round(off_epa, 4),
        "def_epa_per_play": round(def_epa, 4),
        "off_pass_epa": round(off_epa + np.random.normal(0, 0.05), 4),
        "off_rush_epa": round(off_epa + np.random.normal(-0.05, 0.05), 4),
        "def_pass_epa": round(def_epa + np.random.normal(0, 0.05), 4),
        "def_rush_epa": round(def_epa + np.random.normal(-0.03, 0.05), 4)
    })
team_epa_df = pd.DataFrame(team_epa_data)

# Team points metrics
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

# Generate season games
games_data = []
game_id = 1
for week in range(1, 18):
    shuffled = teams.copy()
    np.random.shuffle(shuffled)
    for i in range(0, 32, 2):
        home_team, away_team = shuffled[i], shuffled[i + 1]
        home_epa = team_epa_df[team_epa_df["team"] == home_team]["off_epa_per_play"].values[0]
        away_epa = team_epa_df[team_epa_df["team"] == away_team]["off_epa_per_play"].values[0]
        home_def = team_epa_df[team_epa_df["team"] == home_team]["def_epa_per_play"].values[0]
        away_def = team_epa_df[team_epa_df["team"] == away_team]["def_epa_per_play"].values[0]
        
        home_score = max(0, int(24 + (home_epa - away_def) * 30 + np.random.normal(0, 7)))
        away_score = max(0, int(21 + (away_epa - home_def) * 30 + np.random.normal(0, 7)))
        
        games_data.append({
            "game_id": game_id, "week": week,
            "home_team": home_team, "away_team": away_team,
            "home_score": home_score, "away_score": away_score
        })
        game_id += 1

games_df = pd.DataFrame(games_data)

# Vegas lines for playoffs
top_teams = team_epa_df.nlargest(8, "off_epa_per_play")["team"].tolist()
vegas_df = pd.DataFrame([
    {"game_id": 1, "home_team": top_teams[0], "away_team": top_teams[7], "vegas_total": 47.5},
    {"game_id": 2, "home_team": top_teams[1], "away_team": top_teams[6], "vegas_total": 49.0},
    {"game_id": 3, "home_team": top_teams[2], "away_team": top_teams[5], "vegas_total": 45.5},
    {"game_id": 4, "home_team": top_teams[3], "away_team": top_teams[4], "vegas_total": 51.0},
])

print("Sample data generated!")
print(f"Teams: {len(team_epa_df)}, Games: {len(games_df)}, Playoff matchups: {len(vegas_df)}")

# %% [markdown]
# ## Step 2: Build Training Features with Pandas

# %%
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
game_features_df["home_matchup_edge"] = game_features_df["home_off_epa"] - game_features_df["away_def_epa"]
game_features_df["away_matchup_edge"] = game_features_df["away_off_epa"] - game_features_df["home_def_epa"]

print(f"Training data: {len(game_features_df)} games, {len(game_features_df.columns)} features")
game_features_df.head()

# %% [markdown]
# ## Step 3: Train the Model

# %%
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
print(f"R² Score: {r2_score(y, y_pred):.4f}")
print(f"Mean Absolute Error: {mean_absolute_error(y, y_pred):.2f} points")

# Feature importance
coef_df = pd.DataFrame({"feature": feature_columns, "coefficient": model.coef_})
coef_df = coef_df.reindex(coef_df["coefficient"].abs().sort_values(ascending=False).index)
print("\nTop Features:")
print(coef_df.head(8).to_string(index=False))

# %% [markdown]
# ## Step 4: Project Playoff Games vs Vegas

# %%
# Join home team EPA metrics
playoff_df = vegas_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "home_off_epa",
        "off_pass_epa": "home_off_pass_epa",
        "off_rush_epa": "home_off_rush_epa",
        "def_epa_per_play": "home_def_epa"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team EPA metrics
playoff_df = playoff_df.merge(
    team_epa_df.rename(columns={
        "off_epa_per_play": "away_off_epa",
        "off_pass_epa": "away_off_pass_epa",
        "off_rush_epa": "away_off_rush_epa",
        "def_epa_per_play": "away_def_epa"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join home team points metrics
playoff_df = playoff_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "home_points_per_play",
        "plays_per_game": "home_plays_per_game"
    }),
    left_on="home_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Join away team points metrics
playoff_df = playoff_df.merge(
    team_points_df.rename(columns={
        "points_per_play": "away_points_per_play",
        "plays_per_game": "away_plays_per_game"
    }),
    left_on="away_team",
    right_on="team",
    how="left"
).drop(columns=["team"])

# Compute derived features
playoff_df["off_epa_diff"] = playoff_df["home_off_epa"] - playoff_df["away_off_epa"]
playoff_df["def_epa_diff"] = playoff_df["home_def_epa"] - playoff_df["away_def_epa"]
playoff_df["home_matchup_edge"] = playoff_df["home_off_epa"] - playoff_df["away_def_epa"]
playoff_df["away_matchup_edge"] = playoff_df["away_off_epa"] - playoff_df["home_def_epa"]

X_future = playoff_df[feature_columns]

playoff_df["model_total"] = model.predict(X_future).round(1)
playoff_df["difference"] = (playoff_df["model_total"] - playoff_df["vegas_total"]).round(1)
playoff_df["signal"] = playoff_df["difference"].apply(
    lambda d: "OVER" if d > 2 else ("UNDER" if d < -2 else "NO EDGE")
)

# %% [markdown]
# ## Results: Model vs Vegas

# %%
print("=" * 65)
print("DIVISIONAL ROUND - MODEL vs VEGAS TOTALS")
print("=" * 65)
results = playoff_df[["home_team", "away_team", "model_total", "vegas_total", "difference", "signal"]]
print(results.to_string(index=False))
print("-" * 65)
print("Positive diff → lean OVER | Negative diff → lean UNDER")
print("|diff| > 2 points = potential edge")
