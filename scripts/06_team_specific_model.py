"""
Team-Specific Playoff Predictions
Uses existing team stats to make differentiated predictions for each matchup
"""

import json
import numpy as np
from datetime import datetime

print("=" * 80)
print("TEAM-SPECIFIC PLAYOFF PREDICTIONS")
print("=" * 80)

# Load existing data
print("\nLOADING TEAM DATA")
print("-" * 80)

with open('public/data/enhanced_analysis.json') as f:
    enhanced = json.load(f)
    team_stats = enhanced['team_stats']
    print(f"  ✓ Loaded stats for {len(team_stats)} teams")

with open('public/data/nfl_analysis.json') as f:
    games_data = json.load(f)
    print(f"  ✓ Loaded {len(games_data['games'])} playoff games")

# Step 2: Make team-specific predictions
print("\nGENERATING TEAM-SPECIFIC PREDICTIONS")
print("-" * 80)

def calculate_prediction(home_stats, away_stats, vegas_total):
    """
    Calculate predicted total and score distribution using team-specific stats
    Returns: (total, home_score, away_score)
    """
    # Extract EPA metrics (these are per-play, scale up)
    home_off_epa = home_stats.get('off_epa_per_play', 0)
    away_off_epa = away_stats.get('off_epa_per_play', 0)
    home_def_epa = home_stats.get('def_epa_per_play', 0)
    away_def_epa = away_stats.get('def_epa_per_play', 0)
    
    # Simple scoring formula based on EPA:
    # League average is ~23 points per team
    base_team_score = 23.0
    
    # Each 0.1 EPA per play ≈ 3-4 additional points
    # Each -0.1 DEF EPA per play ≈ 3-4 additional points (better defense = allow fewer points)
    epa_points_per_unit = 35.0
    
    # Calculate team-specific scoring
    home_score = base_team_score + (home_off_epa * epa_points_per_unit) - (home_def_epa * epa_points_per_unit * 0.5)
    away_score = base_team_score + (away_off_epa * epa_points_per_unit) - (away_def_epa * epa_points_per_unit * 0.5)
    
    # Clip to reasonable range
    home_score = np.clip(home_score, 10, 40)
    away_score = np.clip(away_score, 10, 40)
    
    pred_total = home_score + away_score
    
    return pred_total, home_score, away_score

predictions = []

for game in games_data['games']:
    home_abbr = game['homeAbbr']
    away_abbr = game['awayAbbr']
    vegas_total = game['vegasTotal']
    
    home_stats = team_stats.get(home_abbr, {})
    away_stats = team_stats.get(away_abbr, {})
    
    if not home_stats or not away_stats:
        print(f"  ⚠ Missing stats for {away_abbr} @ {home_abbr}")
        pred_total = vegas_total
        home_score = vegas_total / 2
        away_score = vegas_total / 2
    else:
        pred_total, home_score, away_score = calculate_prediction(home_stats, away_stats, vegas_total)
    
    prediction = {
        'game': f"{game['awayTeam']} @ {game['homeTeam']}",
        'away_team': away_abbr,
        'home_team': home_abbr,
        'vegas_total': vegas_total,
        'model_total': float(pred_total),
        'home_score': float(home_score),
        'away_score': float(away_score),
        'edge': float(pred_total - vegas_total),
        'recommendation': 'over' if pred_total > vegas_total + 2 else 'under' if pred_total < vegas_total - 2 else 'hold'
    }
    predictions.append(prediction)
    
    print(f"  {prediction['game']:<30} Model: {pred_total:>6.1f}  Vegas: {vegas_total:>6.1f}  Edge: {prediction['edge']:>+6.1f}")
    print(f"    Projected: {away_abbr} {away_score:.1f} @ {home_abbr} {home_score:.1f}")
    print(f"    Home ({home_abbr}): OFF_EPA={home_stats.get('off_epa_per_play', 0):+.4f}, Def EPA={home_stats.get('def_epa_per_play', 0):+.4f}")
    print(f"    Away ({away_abbr}): OFF_EPA={away_stats.get('off_epa_per_play', 0):+.4f}, Def EPA={away_stats.get('def_epa_per_play', 0):+.4f}")

# Step 3: Export to both files
print("\nEXPORTING RESULTS")
print("-" * 80)

output = {
    'generated_at': datetime.now().isoformat(),
    'model_type': 'Team-Specific EPA Predictions',
    'training_source': '2024 NFL Season (team-specific EPA and yards)',
    'predictions': predictions,
}

# Write to enhanced_model.json for reference
with open('public/data/enhanced_model.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"  ✓ Exported to public/data/enhanced_model.json")

# Also update nfl_analysis.json with new predictions
try:
    with open('public/data/nfl_analysis.json', 'r') as f:
        nfl_data = json.load(f)
    
    # Update each game with new model_total and edge
    for i, pred in enumerate(predictions):
        if i < len(nfl_data['games']):
            nfl_data['games'][i]['modelTotal'] = pred['model_total']
            nfl_data['games'][i]['homeScore'] = pred['home_score']
            nfl_data['games'][i]['awayScore'] = pred['away_score']
            nfl_data['games'][i]['edge'] = pred['edge']
            nfl_data['games'][i]['recommendation'] = pred['recommendation']
    
    with open('public/data/nfl_analysis.json', 'w') as f:
        json.dump(nfl_data, f, indent=2)
    
    print(f"  ✓ Updated public/data/nfl_analysis.json with new predictions")
except Exception as e:
    print(f"  ⚠ Failed to update nfl_analysis.json: {e}")

print("\n" + "=" * 80)
print("✓ TEAM-SPECIFIC PREDICTIONS COMPLETE")
print("=" * 80)
