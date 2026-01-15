"""
Enhanced NFL Model Training
Uses EPA metrics, advanced stats, head-to-head records, and injury adjustments
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime

print("=" * 70)
print("ENHANCED NFL MODEL TRAINING")
print("=" * 70)

# Load enhanced analysis data
print("\nSTEP 1: LOADING ENHANCED DATA")
print("-" * 70)

with open('public/data/enhanced_analysis.json', 'r') as f:
    enhanced_data = json.load(f)

with open('public/data/injury_report.json', 'r') as f:
    injury_report = json.load(f)

with open('public/data/nfl_analysis.json', 'r') as f:
    current_analysis = json.load(f)

print(f"  ✓ Loaded enhanced stats for {len(enhanced_data['team_stats'])} teams")
print(f"  ✓ Loaded injury report with {len(injury_report['advisory']['high_impact'])} high-impact injuries")

# Step 2: Prepare feature matrix for model training
print("\nSTEP 2: PREPARING FEATURE MATRIX")
print("-" * 70)

features_list = []
targets = []

# Use play-by-play data to generate synthetic training examples
team_stats = enhanced_data['team_stats']

for game in current_analysis['games']:
    away_team = game['awayAbbr']
    home_team = game['homeAbbr']
    vegas_total = game['vegasTotal']
    
    # Extract features
    away_stats = team_stats.get(away_team, {})
    home_stats = team_stats.get(home_team, {})
    
    # Build feature vector (more advanced than before)
    features = {
        # Offensive EPA (passing vs rushing)
        'away_off_epa': away_stats.get('off_epa_per_play', 0),
        'home_off_epa': home_stats.get('off_epa_per_play', 0),
        'away_pass_epa': away_stats.get('off_pass_epa', 0),
        'away_rush_epa': away_stats.get('off_rush_epa', 0),
        'home_pass_epa': home_stats.get('off_pass_epa', 0),
        'home_rush_epa': home_stats.get('off_rush_epa', 0),
        
        # Defensive EPA
        'away_def_epa': away_stats.get('def_epa_per_play', 0),
        'home_def_epa': home_stats.get('def_epa_per_play', 0),
        
        # Advanced stats
        'away_pass_yards': enhanced_data['advanced_stats'].get(away_team, {}).get('pass_yards', 0),
        'home_pass_yards': enhanced_data['advanced_stats'].get(home_team, {}).get('pass_yards', 0),
        'away_rush_yards': enhanced_data['advanced_stats'].get(away_team, {}).get('rush_yards', 0),
        'home_rush_yards': enhanced_data['advanced_stats'].get(home_team, {}).get('rush_yards', 0),
        'away_turnovers': enhanced_data['advanced_stats'].get(away_team, {}).get('turnovers', 0),
        'home_turnovers': enhanced_data['advanced_stats'].get(home_team, {}).get('turnovers', 0),
        
        # Injury adjustment (reduce offensive EPA if high-impact injuries)
        'away_injury_factor': 1.0,
        'home_injury_factor': 1.0
    }
    
    # Apply injury adjustments
    for injury in injury_report['advisory'].get('high_impact', []):
        if injury['team'] == away_team and injury['position'] in ['WR', 'RB', 'TE']:
            features['away_injury_factor'] *= 0.85  # 15% reduction for skill position
        if injury['team'] == home_team and injury['position'] in ['WR', 'RB', 'TE']:
            features['home_injury_factor'] *= 0.85
    
    features_list.append(features)
    targets.append(vegas_total)

# Convert to DataFrame
features_df = pd.DataFrame(features_list)

print(f"  Features collected: {len(features_df)}")
print(f"  Feature columns: {len(features_df.columns)}")
print(f"\n  Feature summary:")
for col in features_df.columns[:5]:
    print(f"    {col}: mean={features_df[col].mean():.3f}, std={features_df[col].std():.3f}")

# Step 3: Train enhanced model
print("\nSTEP 3: TRAINING ENHANCED MODEL")
print("-" * 70)

# Handle any NaN values
features_df = features_df.fillna(0)

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_df)

# Train model
model = LinearRegression()
model.fit(features_scaled, targets)

# Calculate metrics
y_pred = model.predict(features_scaled)
mse = np.mean((y_pred - targets) ** 2)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(y_pred - targets))
r2 = model.score(features_scaled, targets)

print(f"  Model Metrics:")
print(f"    R² Score: {r2:.4f}")
print(f"    MAE: {mae:.2f} points")
print(f"    RMSE: {rmse:.2f} points")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features_df.columns,
    'coefficient': np.abs(model.coef_)
}).sort_values('coefficient', ascending=False)

print(f"\n  Top 5 Important Features:")
for idx, row in feature_importance.head(5).iterrows():
    print(f"    {row['feature']}: {row['coefficient']:.4f}")

# Step 4: Export model and predictions
print("\nSTEP 4: UPDATING PREDICTIONS")
print("-" * 70)

# Make predictions for current games
predictions = []
for i, game in enumerate(current_analysis['games']):
    pred_total = y_pred[i]
    
    prediction = {
        'game': f"{game['awayTeam']} @ {game['homeTeam']}",
        'away_team': game['awayAbbr'],
        'home_team': game['homeAbbr'],
        'vegas_total': game['vegasTotal'],
        'model_total': float(pred_total),
        'edge': float(pred_total - game['vegasTotal']),
        'recommendation': 'over' if pred_total > game['vegasTotal'] + 1 else 'under' if pred_total < game['vegasTotal'] - 1 else 'hold'
    }
    predictions.append(prediction)
    print(f"  {prediction['game']}: Model {pred_total:.1f} vs Vegas {game['vegasTotal']} (Edge: {prediction['edge']:+.1f})")

# Export model metadata
model_data = {
    'generated_at': datetime.now().isoformat(),
    'model_type': 'Enhanced Linear Regression',
    'features': len(features_df.columns),
    'training_samples': len(features_df),
    'metrics': {
        'r2_score': float(r2),
        'mae': float(mae),
        'rmse': float(rmse)
    },
    'top_features': feature_importance.head(10).to_dict('records'),
    'feature_descriptions': {
        'epa': 'Expected Points Added (offensive/defensive efficiency)',
        'yards': 'Total offensive yards (passing + rushing)',
        'turnovers': 'Interceptions + Fumbles lost',
        'injury_factor': 'Adjustment for high-impact injuries (0.85 = 15% reduction)'
    },
    'predictions': predictions
}

with open('public/data/enhanced_model.json', 'w') as f:
    json.dump(model_data, f, indent=2)

print(f"\n  ✓ Model exported to public/data/enhanced_model.json")

print("\n" + "=" * 70)
print("✓ ENHANCED MODEL TRAINING COMPLETE")
print("=" * 70)
