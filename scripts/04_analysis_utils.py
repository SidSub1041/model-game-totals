"""
NFL Betting Analysis - Reusable Utility Functions
Wrap key steps into reusable functions for weekly/round updates.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import pickle
from pathlib import Path
from typing import Tuple, Dict, Any

# Default feature columns used by the model
DEFAULT_FEATURES = [
    "home_off_epa", "home_def_epa", "home_off_pass_epa", "home_off_rush_epa",
    "away_off_epa", "away_def_epa", "away_off_pass_epa", "away_off_rush_epa",
    "home_points_per_play", "away_points_per_play",
    "home_plays_per_game", "away_plays_per_game",
    "off_epa_diff", "def_epa_diff",
    "home_matchup_edge", "away_matchup_edge"
]


def build_training_data(
    data_dir: Path,
    season: int = 2025
) -> pd.DataFrame:
    """
    Load CSVs and build game_features table for a given season.
    
    Args:
        data_dir: Path to directory containing CSV files
        season: Season year
        
    Returns:
        DataFrame with all game features ready for modeling
    """
    # Load CSVs
    team_epa_df = pd.read_csv(data_dir / f"team_epa_{season}.csv")
    team_points_df = pd.read_csv(data_dir / f"team_points_{season}.csv")
    games_df = pd.read_csv(data_dir / f"games_{season}.csv")
    
    # Join home team EPA metrics
    result = games_df.merge(
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
    result = result.merge(
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
    result = result.merge(
        team_points_df.rename(columns={
            "points_per_play": "home_points_per_play",
            "plays_per_game": "home_plays_per_game"
        }),
        left_on="home_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Join away team points metrics
    result = result.merge(
        team_points_df.rename(columns={
            "points_per_play": "away_points_per_play",
            "plays_per_game": "away_plays_per_game"
        }),
        left_on="away_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Compute derived features
    result["total_points"] = result["home_score"] + result["away_score"]
    result["off_epa_diff"] = result["home_off_epa"] - result["away_off_epa"]
    result["def_epa_diff"] = result["home_def_epa"] - result["away_def_epa"]
    result["ppp_diff"] = result["home_points_per_play"] - result["away_points_per_play"]
    result["home_matchup_edge"] = result["home_off_epa"] - result["away_def_epa"]
    result["away_matchup_edge"] = result["away_off_epa"] - result["home_def_epa"]
    
    return result.sort_values(["week", "game_id"]).reset_index(drop=True)


def fit_total_model(
    training_df: pd.DataFrame,
    feature_columns: list = None
) -> Tuple[LinearRegression, Dict[str, Any]]:
    """
    Fit a linear regression model for game totals.
    
    Args:
        training_df: DataFrame with game features and total_points
        feature_columns: List of feature column names (uses defaults if None)
        
    Returns:
        Tuple of (fitted model, metrics dict)
    """
    if feature_columns is None:
        feature_columns = DEFAULT_FEATURES
    
    X = training_df[feature_columns]
    y = training_df["total_points"]
    
    model = LinearRegression()
    model.fit(X, y)
    
    y_pred = model.predict(X)
    metrics = {
        "r2_score": r2_score(y, y_pred),
        "mae": mean_absolute_error(y, y_pred),
        "feature_columns": feature_columns
    }
    
    return model, metrics


def project_week(
    model: LinearRegression,
    upcoming_games_df: pd.DataFrame,
    team_epa_df: pd.DataFrame,
    team_points_df: pd.DataFrame,
    vegas_lines_df: pd.DataFrame,
    feature_columns: list = None,
    edge_threshold: float = 2.0
) -> pd.DataFrame:
    """
    Build features for upcoming games and output model vs Vegas totals.
    
    Args:
        model: Trained LinearRegression model
        upcoming_games_df: DataFrame with home_team, away_team columns
        team_epa_df: Team EPA metrics
        team_points_df: Team points per play metrics
        vegas_lines_df: Vegas lines with home_team, away_team, vegas_total
        feature_columns: List of feature column names
        edge_threshold: Minimum point difference to flag as edge
        
    Returns:
        DataFrame with projections and betting signals
    """
    if feature_columns is None:
        feature_columns = DEFAULT_FEATURES
    
    # Merge upcoming games with vegas lines
    games_with_lines = upcoming_games_df.merge(
        vegas_lines_df[["home_team", "away_team", "vegas_total"]],
        on=["home_team", "away_team"],
        how="left"
    )
    
    # Join home team EPA metrics
    result = games_with_lines.merge(
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
    result = result.merge(
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
    result = result.merge(
        team_points_df.rename(columns={
            "points_per_play": "home_points_per_play",
            "plays_per_game": "home_plays_per_game"
        }),
        left_on="home_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Join away team points metrics
    result = result.merge(
        team_points_df.rename(columns={
            "points_per_play": "away_points_per_play",
            "plays_per_game": "away_plays_per_game"
        }),
        left_on="away_team",
        right_on="team",
        how="left"
    ).drop(columns=["team"])
    
    # Compute derived features
    result["off_epa_diff"] = result["home_off_epa"] - result["away_off_epa"]
    result["def_epa_diff"] = result["home_def_epa"] - result["away_def_epa"]
    result["ppp_diff"] = result["home_points_per_play"] - result["away_points_per_play"]
    result["home_matchup_edge"] = result["home_off_epa"] - result["away_def_epa"]
    result["away_matchup_edge"] = result["away_off_epa"] - result["home_def_epa"]
    
    # Predict
    X = result[feature_columns]
    result["model_total"] = model.predict(X)
    result["difference"] = result["model_total"] - result["vegas_total"]
    
    # Signal
    def get_signal(diff):
        if diff > edge_threshold:
            return "OVER"
        elif diff < -edge_threshold:
            return "UNDER"
        return "NO EDGE"
    
    result["signal"] = result["difference"].apply(get_signal)
    
    return result[["home_team", "away_team", "model_total", "vegas_total", "difference", "signal"]]


def save_model(model: LinearRegression, metrics: dict, path: Path):
    """Save model and metadata to pickle file."""
    data = {"model": model, **metrics}
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_model(path: Path) -> Tuple[LinearRegression, dict]:
    """Load model and metadata from pickle file."""
    with open(path, "rb") as f:
        data = pickle.load(f)
    model = data.pop("model")
    return model, data
