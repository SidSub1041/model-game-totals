"""
Download NFL Team Logos from ESPN/NFL CDN
Saves logos to public/images/team-logos/
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse

# Create output directory
OUTPUT_DIR = Path("public/images/team-logos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NFL team logos from StatsBomb API (publicly available)
TEAM_LOGOS = {
    "ARI": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "ATL": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "BAL": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "BUF": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "CAR": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "CHI": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "CIN": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "CLE": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "DAL": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "DEN": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "DET": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "GB": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "HOU": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "IND": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "JAX": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "KC": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "LAC": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "LAR": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "LV": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "MIA": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "MIN": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "NE": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "NO": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "NYG": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "NYJ": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "PHI": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "PIT": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "SEA": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "SF": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "TB": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "TEN": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
    "WAS": "https://raw.githubusercontent.com/statsbomb/statsbomb-data/master/data/Teams.json",
}

print("\n" + "="*70)
print("DOWNLOADING NFL TEAM LOGOS")
print("="*70 + "\n")

success_count = 0
failed_count = 0

for team_abbr, url in TEAM_LOGOS.items():
    try:
        print(f"  Downloading {team_abbr}...", end=" ")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get file extension from URL
        parsed_url = urlparse(url)
        file_ext = os.path.splitext(parsed_url.path)[1] or ".png"
        
        # Save file
        file_path = OUTPUT_DIR / f"{team_abbr}{file_ext}"
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ ({len(response.content)} bytes)")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        failed_count += 1

print("\n" + "="*70)
print(f"DOWNLOAD COMPLETE: {success_count} successful, {failed_count} failed")
print("="*70 + "\n")

print(f"Team logos saved to: {OUTPUT_DIR.resolve()}\n")

# Generate TypeScript code for team-logos.ts
print("To use these logos, update lib/team-logos.ts with:")
print("-" * 70)
print("""
export const teamLogos: Record<string, { logo: string; color: string }> = {
""")

for team_abbr in sorted(TEAM_LOGOS.keys()):
    print(f'  "{team_abbr}": {{ logo: "/images/team-logos/{team_abbr}.png", color: "..." }},')

print("}")
print("-" * 70)
