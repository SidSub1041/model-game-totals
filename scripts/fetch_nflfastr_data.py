"""
NFL Betting Analysis - nflfastR Data Pipeline
Fetches real NFL data using nfl_data_py and exports to JSON for the dashboard.

Run locally with: python scripts/fetch_nflfastr_data.py

Requirements:
    pip install nfl_data_py pandas scikit-learn
"""

import json
import warnings
from datetime import datetime
from pathlib import Path

import nfl_data_py as nfl
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore")


# ============================================================================
# JSON ENCODER FOR NUMPY TYPES
# ============================================================================
class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def load_vegas_lines() -> list:
    """Load Vegas lines from the scraper-generated JSON file."""
    if VEGAS_LINES_FILE.exists():
        with open(VEGAS_LINES_FILE, "r") as f:
            data = json.load(f)
            games = data.get("games", [])
            # Convert from vegas_lines format to playoff_matchups format
            matchups = []
            for game in games:
                # Normalize team abbreviations (e.g., LAR -> LA, as used in nflfastR)
                home_team = normalize_team_abbr(game["home_team"])
                away_team = normalize_team_abbr(game["away_team"])
                
                matchup = {
                    "home_team": home_team,
                    "away_team": away_team,
                    "game_date": game.get("date", "")[:10] if game.get("date") else "2026-01-18",
                    "game_time": "TBD",
                    "vegas_total": game.get("over_under", 0),
                }
                matchups.append(matchup)
            return matchups
    return []


def normalize_team_abbr(abbr: str) -> str:
    """Convert standard team abbreviations to nflfastR format."""
    # nflfastR uses 'LA' for Rams and 'SD' for Chargers
    mapping = {
        "LAR": "LA",
        "LAC": "SD",
    }
    return mapping.get(abbr, abbr)


def denormalize_team_abbr(abbr: str) -> str:
    """Convert nflfastR format back to standard team abbreviations."""
    # Reverse mapping
    mapping = {
        "LA": "LAR",
        "SD": "LAC",
    }
    return mapping.get(abbr, abbr)


# ============================================================================
# CONFIGURATION
# ============================================================================
TRAINING_SEASONS = [2024]  # Historical seasons for training
OUTPUT_DIR = Path("public/data")
OUTPUT_FILE = OUTPUT_DIR / "nfl_analysis.json"
VEGAS_LINES_FILE = OUTPUT_DIR / "vegas_lines.json"

# Will be loaded from vegas_lines.json
PLAYOFF_MATCHUPS = []

# Team name mapping for display
TEAM_NAMES = {
    "ARI": "Cardinals", "ATL": "Falcons", "BAL": "Ravens", "BUF": "Bills",
    "CAR": "Panthers", "CHI": "Bears", "CIN": "Bengals", "CLE": "Browns",
    "DAL": "Cowboys", "DEN": "Broncos", "DET": "Lions", "GB": "Packers",
    "HOU": "Texans", "IND": "Colts", "JAX": "Jaguars", "KC": "Chiefs",
    "LAC": "Chargers", "LAR": "Rams", "LV": "Raiders", "MIA": "Dolphins",
    "MIN": "Vikings", "NE": "Patriots", "NO": "Saints", "NYG": "Giants",
    "NYJ": "Jets", "PHI": "Eagles", "PIT": "Steelers", "SF": "49ers",
    "SEA": "Seahawks", "TB": "Buccaneers", "TEN": "Titans", "WAS": "Commanders"
}


def fetch_pbp_data(seasons: list[int]) -> pd.DataFrame:
    """Fetch play-by-play data from nflfastR."""
    print(f"  Fetching play-by-play data for {seasons}...")
    try:
        pbp = nfl.import_pbp_data(seasons)
        print(f"  Loaded {len(pbp):,} plays")
        return pbp
    except Exception as e:
        # If we can't get all seasons, try without the most recent one
        if len(seasons) > 1:
            print(f"  Warning: Could not fetch data for all seasons. Trying {seasons[:-1]}...")
            pbp = nfl.import_pbp_data(seasons[:-1])
            print(f"  Loaded {len(pbp):,} plays from {seasons[:-1]}")
            return pbp
        else:
            raise


def calculate_team_epa(pbp: pd.DataFrame) -> pd.DataFrame:
    """Calculate EPA metrics per team from play-by-play data."""
    print("  Calculating team EPA metrics...")
    
    # Filter to relevant plays (passes and rushes, excluding special teams)
    plays = pbp[
        (pbp["play_type"].isin(["pass", "run"])) &
        (pbp["epa"].notna()) &
        (pbp["posteam"].notna())
    ].copy()
    
    # Offensive EPA by team
    off_epa = plays.groupby("posteam").agg(
        off_epa_per_play=("epa", "mean"),
        off_plays=("epa", "count")
    ).reset_index().rename(columns={"posteam": "team"})
    
    # Offensive EPA by play type
    pass_plays = plays[plays["play_type"] == "pass"]
    rush_plays = plays[plays["play_type"] == "run"]
    
    off_pass_epa = pass_plays.groupby("posteam").agg(
        off_pass_epa=("epa", "mean")
    ).reset_index().rename(columns={"posteam": "team"})
    
    off_rush_epa = rush_plays.groupby("posteam").agg(
        off_rush_epa=("epa", "mean")
    ).reset_index().rename(columns={"posteam": "team"})
    
    # Defensive EPA by team (EPA allowed)
    def_epa = plays.groupby("defteam").agg(
        def_epa_per_play=("epa", "mean"),
        def_plays=("epa", "count")
    ).reset_index().rename(columns={"defteam": "team"})
    
    def_pass_epa = pass_plays.groupby("defteam").agg(
        def_pass_epa=("epa", "mean")
    ).reset_index().rename(columns={"defteam": "team"})
    
    def_rush_epa = rush_plays.groupby("defteam").agg(
        def_rush_epa=("epa", "mean")
    ).reset_index().rename(columns={"defteam": "team"})
    
    # Merge all EPA metrics
    team_epa = off_epa.merge(off_pass_epa, on="team", how="left")
    team_epa = team_epa.merge(off_rush_epa, on="team", how="left")
    team_epa = team_epa.merge(def_epa, on="team", how="left")
    team_epa = team_epa.merge(def_pass_epa, on="team", how="left")
    team_epa = team_epa.merge(def_rush_epa, on="team", how="left")
    
    print(f"  Calculated EPA for {len(team_epa)} teams")
    return team_epa


def calculate_team_scoring(pbp: pd.DataFrame) -> pd.DataFrame:
    """Calculate scoring metrics per team."""
    print("  Calculating team scoring metrics...")
    
    # Get game-level scoring
    games = pbp.groupby(["game_id", "home_team", "away_team"]).agg(
        home_score=("home_score", "max"),
        away_score=("away_score", "max")
    ).reset_index()
    
    # Home team stats
    home_stats = games.groupby("home_team").agg(
        home_ppg=("home_score", "mean"),
        home_games=("game_id", "count")
    ).reset_index().rename(columns={"home_team": "team"})
    
    # Away team stats
    away_stats = games.groupby("away_team").agg(
        away_ppg=("away_score", "mean"),
        away_games=("game_id", "count")
    ).reset_index().rename(columns={"away_team": "team"})
    
    # Merge
    team_scoring = home_stats.merge(away_stats, on="team", how="outer")
    team_scoring["ppg"] = (
        (team_scoring["home_ppg"] * team_scoring["home_games"] +
         team_scoring["away_ppg"] * team_scoring["away_games"]) /
        (team_scoring["home_games"] + team_scoring["away_games"])
    )
    
    # Calculate plays per game
    plays = pbp[(pbp["play_type"].isin(["pass", "run"])) & (pbp["posteam"].notna())]
    plays_per_game = plays.groupby(["game_id", "posteam"]).size().reset_index(name="plays")
    avg_plays = plays_per_game.groupby("posteam")["plays"].mean().reset_index()
    avg_plays.columns = ["team", "plays_per_game"]
    
    team_scoring = team_scoring.merge(avg_plays, on="team", how="left")
    team_scoring["points_per_play"] = team_scoring["ppg"] / team_scoring["plays_per_game"]
    
    print(f"  Calculated scoring for {len(team_scoring)} teams")
    return team_scoring


def get_game_results(pbp: pd.DataFrame) -> pd.DataFrame:
    """Extract game results from play-by-play data."""
    print("  Extracting game results...")
    
    games = pbp.groupby(["game_id", "week", "home_team", "away_team"]).agg(
        home_score=("home_score", "max"),
        away_score=("away_score", "max")
    ).reset_index()
    
    games["total_points"] = games["home_score"] + games["away_score"]
    
    # Filter to regular season (weeks 1-18)
    games = games[games["week"] <= 18].copy()
    
    print(f"  Found {len(games)} regular season games")
    return games


def build_training_data(
    games: pd.DataFrame,
    team_epa: pd.DataFrame,
    team_scoring: pd.DataFrame
) -> pd.DataFrame:
    """Build training dataset with features."""
    print("  Building training features...")
    
    # Join home team EPA
    df = games.merge(
        team_epa.rename(columns={
            "off_epa_per_play": "home_off_epa",
            "off_pass_epa": "home_off_pass_epa",
            "off_rush_epa": "home_off_rush_epa",
            "def_epa_per_play": "home_def_epa",
            "def_pass_epa": "home_def_pass_epa",
            "def_rush_epa": "home_def_rush_epa"
        })[["team", "home_off_epa", "home_off_pass_epa", "home_off_rush_epa",
            "home_def_epa", "home_def_pass_epa", "home_def_rush_epa"]],
        left_on="home_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Join away team EPA
    df = df.merge(
        team_epa.rename(columns={
            "off_epa_per_play": "away_off_epa",
            "off_pass_epa": "away_off_pass_epa",
            "off_rush_epa": "away_off_rush_epa",
            "def_epa_per_play": "away_def_epa",
            "def_pass_epa": "away_def_pass_epa",
            "def_rush_epa": "away_def_rush_epa"
        })[["team", "away_off_epa", "away_off_pass_epa", "away_off_rush_epa",
            "away_def_epa", "away_def_pass_epa", "away_def_rush_epa"]],
        left_on="away_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Join home team scoring
    df = df.merge(
        team_scoring.rename(columns={
            "ppg": "home_ppg",
            "home_ppg": "home_ppg_at_home",
            "away_ppg": "home_ppg_on_road",
            "plays_per_game": "home_plays_per_game",
            "points_per_play": "home_points_per_play"
        })[["team", "home_ppg", "home_ppg_at_home", "home_plays_per_game", "home_points_per_play"]],
        left_on="home_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Join away team scoring
    df = df.merge(
        team_scoring.rename(columns={
            "ppg": "away_ppg",
            "home_ppg": "away_ppg_at_home",
            "away_ppg": "away_ppg_on_road",
            "plays_per_game": "away_plays_per_game",
            "points_per_play": "away_points_per_play"
        })[["team", "away_ppg", "away_ppg_on_road", "away_plays_per_game", "away_points_per_play"]],
        left_on="away_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Derived features
    df["off_epa_diff"] = df["home_off_epa"] - df["away_off_epa"]
    df["def_epa_diff"] = df["home_def_epa"] - df["away_def_epa"]
    df["home_matchup_edge"] = df["home_off_epa"] - df["away_def_epa"]
    df["away_matchup_edge"] = df["away_off_epa"] - df["home_def_epa"]
    
    # Drop rows with missing features
    df = df.dropna()
    
    print(f"  Built training data: {len(df)} games x {len(df.columns)} columns")
    return df


def train_model(train_df: pd.DataFrame) -> tuple:
    """Train linear regression model."""
    print("  Training model...")
    
    feature_cols = [
        "home_off_epa", "home_def_epa", "home_off_pass_epa", "home_off_rush_epa",
        "away_off_epa", "away_def_epa", "away_off_pass_epa", "away_off_rush_epa",
        "home_ppg", "away_ppg",
        "home_plays_per_game", "away_plays_per_game",
        "off_epa_diff", "def_epa_diff",
        "home_matchup_edge", "away_matchup_edge"
    ]
    
    X = train_df[feature_cols]
    y = train_df["total_points"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    y_pred = model.predict(X)
    metrics = {
        "r2_score": round(r2_score(y, y_pred), 4),
        "mae": round(mean_absolute_error(y, y_pred), 2),
        "rmse": round(np.sqrt(mean_squared_error(y, y_pred)), 2),
        "training_samples": len(train_df)
    }
    
    print(f"  Model R²: {metrics['r2_score']}, MAE: {metrics['mae']}")
    return model, feature_cols, metrics


def project_games(
    matchups: list[dict],
    model,
    feature_cols: list[str],
    team_epa: pd.DataFrame,
    team_scoring: pd.DataFrame
) -> list[dict]:
    """Generate projections for playoff matchups."""
    print("  Projecting playoff games...")
    
    projections = []
    
    for matchup in matchups:
        home = matchup["home_team"]
        away = matchup["away_team"]
        
        # Get team stats
        home_epa = team_epa[team_epa["team"] == home].iloc[0] if len(team_epa[team_epa["team"] == home]) > 0 else None
        away_epa = team_epa[team_epa["team"] == away].iloc[0] if len(team_epa[team_epa["team"] == away]) > 0 else None
        home_scoring = team_scoring[team_scoring["team"] == home].iloc[0] if len(team_scoring[team_scoring["team"] == home]) > 0 else None
        away_scoring = team_scoring[team_scoring["team"] == away].iloc[0] if len(team_scoring[team_scoring["team"] == away]) > 0 else None
        
        if home_epa is None or away_epa is None or home_scoring is None or away_scoring is None:
            print(f"  Warning: Missing data for {home} vs {away}")
            continue
        
        # Build feature vector
        features = {
            "home_off_epa": home_epa["off_epa_per_play"],
            "home_def_epa": home_epa["def_epa_per_play"],
            "home_off_pass_epa": home_epa["off_pass_epa"],
            "home_off_rush_epa": home_epa["off_rush_epa"],
            "away_off_epa": away_epa["off_epa_per_play"],
            "away_def_epa": away_epa["def_epa_per_play"],
            "away_off_pass_epa": away_epa["off_pass_epa"],
            "away_off_rush_epa": away_epa["off_rush_epa"],
            "home_ppg": home_scoring["ppg"],
            "away_ppg": away_scoring["ppg"],
            "home_plays_per_game": home_scoring["plays_per_game"],
            "away_plays_per_game": away_scoring["plays_per_game"],
            "off_epa_diff": home_epa["off_epa_per_play"] - away_epa["off_epa_per_play"],
            "def_epa_diff": home_epa["def_epa_per_play"] - away_epa["def_epa_per_play"],
            "home_matchup_edge": home_epa["off_epa_per_play"] - away_epa["def_epa_per_play"],
            "away_matchup_edge": away_epa["off_epa_per_play"] - home_epa["def_epa_per_play"],
        }
        
        X = pd.DataFrame([features])[feature_cols]
        model_total = model.predict(X)[0]
        
        vegas_total = matchup["vegas_total"]
        edge = model_total - vegas_total
        
        # Determine recommendation
        if edge > 2:
            recommendation = "over"
        elif edge < -2:
            recommendation = "under"
        else:
            recommendation = "hold"
        
        # Estimate individual team scores (simplified)
        home_pct = home_scoring["ppg"] / (home_scoring["ppg"] + away_scoring["ppg"])
        home_score = model_total * home_pct
        away_score = model_total * (1 - home_pct)
        
        projections.append({
            "homeTeam": TEAM_NAMES.get(home, home),
            "awayTeam": TEAM_NAMES.get(away, away),
            "homeAbbr": denormalize_team_abbr(home),
            "awayAbbr": denormalize_team_abbr(away),
            "gameDate": datetime.strptime(matchup["game_date"], "%Y-%m-%d").strftime("%a, %b %d"),
            "gameTime": matchup["game_time"],
            "vegasTotal": vegas_total,
            "modelTotal": round(model_total, 1),
            "homeScore": round(home_score, 1),
            "awayScore": round(away_score, 1),
            "edge": round(edge, 1),
            "recommendation": recommendation,
            # EPA details for display
            "homeOffEpa": round(home_epa["off_epa_per_play"], 3),
            "homeDefEpa": round(home_epa["def_epa_per_play"], 3),
            "awayOffEpa": round(away_epa["off_epa_per_play"], 3),
            "awayDefEpa": round(away_epa["def_epa_per_play"], 3),
        })
    
    print(f"  Generated {len(projections)} projections")
    return projections


def calculate_summary_stats(projections: list[dict]) -> dict:
    """Calculate summary statistics."""
    edges = [p["edge"] for p in projections]
    return {
        "gamesAnalyzed": len(projections),
        "avgEdge": round(np.mean(np.abs(edges)), 1),
        "overPicks": sum(1 for p in projections if p["recommendation"] == "over"),
        "underPicks": sum(1 for p in projections if p["recommendation"] == "under"),
        "holdPicks": sum(1 for p in projections if p["recommendation"] == "hold"),
        "avgModelTotal": round(np.mean([p["modelTotal"] for p in projections]), 1),
        "avgVegasTotal": round(np.mean([p["vegasTotal"] for p in projections]), 1),
    }


def main():
    """Main pipeline function."""
    print("=" * 70)
    print("NFL BETTING ANALYSIS - nflfastR DATA PIPELINE")
    print("=" * 70)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load Vegas lines for this weekend
    global PLAYOFF_MATCHUPS
    PLAYOFF_MATCHUPS = load_vegas_lines()
    if not PLAYOFF_MATCHUPS:
        print("\nWARNING: No Vegas lines found. Run fetch_vegas_lines.py first!")
        return
    
    # Step 1: Fetch play-by-play data
    print("\nSTEP 1: FETCHING DATA")
    print("-" * 40)
    pbp = fetch_pbp_data(TRAINING_SEASONS)
    
    # Step 2: Calculate team metrics
    print("\nSTEP 2: CALCULATING TEAM METRICS")
    print("-" * 40)
    team_epa = calculate_team_epa(pbp)
    team_scoring = calculate_team_scoring(pbp)
    
    # Step 3: Get game results and build training data
    print("\nSTEP 3: BUILDING TRAINING DATA")
    print("-" * 40)
    games = get_game_results(pbp)
    train_df = build_training_data(games, team_epa, team_scoring)
    
    # Step 4: Train model
    print("\nSTEP 4: TRAINING MODEL")
    print("-" * 40)
    model, feature_cols, model_metrics = train_model(train_df)
    
    # Step 5: Generate projections
    print("\nSTEP 5: GENERATING PROJECTIONS")
    print("-" * 40)
    projections = project_games(PLAYOFF_MATCHUPS, model, feature_cols, team_epa, team_scoring)
    
    # Step 6: Calculate summary stats
    summary_stats = calculate_summary_stats(projections)
    
    # Step 7: Export to JSON
    print("\nSTEP 6: EXPORTING TO JSON")
    print("-" * 40)
    output_data = {
        "generatedAt": datetime.now().isoformat(),
        "trainingSeasons": TRAINING_SEASONS,
        "playoffWeekend": "Divisional Round - January 18-19, 2026",
        "modelMetrics": model_metrics,
        "summaryStats": summary_stats,
        "games": projections,
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=2, cls=NumpyEncoder)
    
    print(f"  Exported to {OUTPUT_FILE}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    print(f"  Training Seasons: {TRAINING_SEASONS}")
    print(f"  Playoff Weekend: Divisional Round - January 18-19, 2026")
    print(f"  Model R²: {model_metrics['r2_score']}")
    print(f"  Model MAE: {model_metrics['mae']} points")
    print(f"  Games projected: {len(projections)}")
    print(f"  Over picks: {summary_stats['overPicks']}")
    print(f"  Under picks: {summary_stats['underPicks']}")
    print(f"\n  Dashboard data saved to: {OUTPUT_FILE}")
    print("  Run `npm run dev` to view the dashboard")


if __name__ == "__main__":
    main()
