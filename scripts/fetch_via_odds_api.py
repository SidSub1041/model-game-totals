"""
The-Odds-API Integration (Optional)
Get real Vegas lines with a free API key from https://the-odds-api.com

Setup:
1. Sign up at https://the-odds-api.com (free tier: 500 requests/month)
2. Get your API key from the dashboard
3. Create a .env file in the project root with:
   THE_ODDS_API_KEY=your_key_here
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path("public/data")
OUTPUT_FILE = OUTPUT_DIR / "vegas_lines.json"

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

# ESPN team IDs to abbreviations
ESPN_TO_ABBR = {
    "25": "ARI", "1": "ATL", "33": "BAL", "2": "BUF",
    "3": "CAR", "4": "CHI", "5": "CIN", "6": "CLE",
    "7": "DAL", "8": "DEN", "9": "DET", "10": "GB",
    "34": "HOU", "11": "IND", "30": "JAX", "12": "KC",
    "24": "LAC", "14": "LAR", "13": "LV", "15": "MIA",
    "16": "MIN", "17": "NE", "18": "NO", "19": "NYG",
    "20": "NYJ", "21": "PHI", "23": "PIT", "25": "SF",
    "26": "SEA", "27": "TB", "28": "TEN", "33": "WAS"
}


def get_api_key() -> str:
    """Get The-Odds-API key from environment or .env file."""
    # Try environment variable
    if "THE_ODDS_API_KEY" in os.environ:
        return os.environ["THE_ODDS_API_KEY"]
    
    # Try .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if line.startswith("THE_ODDS_API_KEY="):
                    return line.split("=", 1)[1].strip()
    
    return None


def decimal_to_american(decimal_odds: float) -> int:
    """Convert decimal odds to American odds."""
    if decimal_odds < 2:
        # Favorite: -100 / (decimal - 1)
        return int(-100 / (decimal_odds - 1))
    else:
        # Underdog: (decimal - 1) * 100
        return int((decimal_odds - 1) * 100)


def fetch_from_odds_api(api_key: str) -> list:
    """Fetch real-time Vegas odds from The-Odds-API."""
    print("  Fetching from The-Odds-API...")
    try:
        # Fetch totals odds
        url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
        params_totals = {
            "apiKey": api_key,
            "regions": "us",
            "markets": "totals",
            "oddsFormat": "decimal",
        }
        
        response_totals = requests.get(url, params=params_totals, timeout=10)
        response_totals.raise_for_status()
        events = response_totals.json()
        
        # Fetch moneyline odds separately (optional)
        params_ml = {
            "apiKey": api_key,
            "regions": "us",
            "markets": "moneyline",
            "oddsFormat": "decimal",
        }
        try:
            response_ml = requests.get(url, params=params_ml, timeout=10)
            response_ml.raise_for_status()
            events_ml = response_ml.json()
        except:
            # Moneyline might not be available on free tier
            print("    ℹ️  Moneyline odds not available (free tier limitation)")
            events_ml = []
        
        # Create a map of moneyline odds by game ID
        ml_map = {}
        if isinstance(events_ml, list):
            for event in events_ml:
                event_id = event.get("id")
                home_ml = None
                away_ml = None
                bookmakers = event.get("bookmakers", [])
                if bookmakers and len(bookmakers) > 0:
                    markets = bookmakers[0].get("markets", [])
                    for market in markets:
                        if market.get("key") == "moneyline":
                            outcomes = market.get("outcomes", [])
                            for outcome in outcomes:
                                decimal = outcome.get("price", 0)
                                if decimal > 0:
                                    american = decimal_to_american(float(decimal))
                                    if outcome.get("name") == "Home":
                                        home_ml = american
                                    elif outcome.get("name") == "Away":
                                        away_ml = american
                ml_map[event_id] = {"home": home_ml, "away": away_ml}
        
        # API returns a list directly
        if not isinstance(events, list):
            print(f"    ⚠️  Unexpected response format: {type(events)}")
            return []
        
        games = []
        
        for event in events:
            try:
                event_id = event.get("id")
                # Get home and away teams
                home_team = event.get("home_team", "")
                away_team = event.get("away_team", "")
                
                # Convert ESPN names to abbreviations
                home_abbr = convert_team_name(home_team)
                away_abbr = convert_team_name(away_team)
                
                # Get odds from first bookmaker
                over_under = None
                spread = None
                
                bookmakers = event.get("bookmakers", [])
                if bookmakers and isinstance(bookmakers, list) and len(bookmakers) > 0:
                    bookmaker = bookmakers[0]
                    if isinstance(bookmaker, dict):
                        markets = bookmaker.get("markets", [])
                        for market in markets:
                            if isinstance(market, dict):
                                if market.get("key") == "totals":
                                    outcomes = market.get("outcomes", [])
                                    if outcomes and isinstance(outcomes, list) and len(outcomes) > 0:
                                        # Get the Over line point value
                                        for outcome in outcomes:
                                            if isinstance(outcome, dict) and outcome.get("name") == "Over":
                                                over_under = float(outcome.get("point", 0))
                                                break
                
                # Get moneyline odds from the separate fetch
                home_moneyline = None
                away_moneyline = None
                if event_id in ml_map:
                    home_moneyline = ml_map[event_id]["home"]
                    away_moneyline = ml_map[event_id]["away"]
                
                game_date = event.get("commence_time", "").replace("Z", "+00:00")
                
                games.append({
                    "id": event_id,
                    "date": game_date,
                    "home_team": home_abbr,
                    "home_team_name": TEAM_NAMES.get(home_abbr, home_team),
                    "away_team": away_abbr,
                    "away_team_name": TEAM_NAMES.get(away_abbr, away_team),
                    "over_under": over_under,
                    "spread": spread,
                    "home_moneyline": home_moneyline,
                    "away_moneyline": away_moneyline,
                    "status": "Scheduled"
                })
            except Exception as e:
                print(f"      Warning: Could not parse event - {e}")
                continue
        
        if games:
            print(f"    ✅ Successfully fetched {len(games)} games from The-Odds-API")
            return games
        
    except Exception as e:
        print(f"    ❌ The-Odds-API error: {e}")
    
    return []


def convert_team_name(team_str: str) -> str:
    """Convert team name to abbreviation."""
    team_str = team_str.upper().strip()
    
    # Direct abbreviation match
    for abbr, name in TEAM_NAMES.items():
        if name.upper() == team_str or abbr == team_str:
            return abbr
    
    # Handle special cases
    special_cases = {
        "DENVER BRONCOS": "DEN",
        "BUFFALO BILLS": "BUF",
        "SAN FRANCISCO 49ERS": "SF",
        "SEATTLE SEAHAWKS": "SEA",
        "TEXANS": "HOU",
        "PATRIOTS": "NE",
        "LOS ANGELES RAMS": "LAR",
        "CHICAGO BEARS": "CHI",
        "SAN FRANCISCO": "SF",
        "LOS ANGELES": "LAR",
        "49ERS": "SF",
        "NINERS": "SF",
    }
    
    for key, abbr in special_cases.items():
        if key in team_str:
            return abbr
    
    # Partial match on team names
    for abbr, name in TEAM_NAMES.items():
        if name.upper() in team_str or team_str in name.upper():
            return abbr
    
    # Default: first 2-3 chars
    return team_str[:3]


def main():
    """Main execution."""
    print("\n" + "="*70)
    print("THE-ODDS-API INTEGRATION")
    print("="*70 + "\n")
    
    # Get API key
    api_key = get_api_key()
    
    if not api_key:
        print("⚠️  No API key found!")
        print("\nTo use The-Odds-API:")
        print("1. Sign up at: https://the-odds-api.com")
        print("2. Get your FREE API key (500 requests/month)")
        print("3. Create .env file with: THE_ODDS_API_KEY=your_key_here")
        print("4. Run this script again\n")
        return
    
    print("STEP 1: FETCHING LIVE VEGAS LINES")
    print("-" * 40)
    
    # Fetch from API
    games = fetch_from_odds_api(api_key)
    
    if not games:
        print("  Failed to fetch games. Check API key and rate limits.")
        return
    
    # Export to JSON
    print("\nSTEP 2: EXPORTING TO JSON")
    print("-" * 40)
    
    output_data = {
        "generatedAt": datetime.now().isoformat(),
        "source": "The-Odds-API",
        "gamesCount": len(games),
        "games": games
    }
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"  Exported to {OUTPUT_FILE}")
    print(f"  Total games: {len(games)}")
    
    # Print summary
    print("\n" + "="*70)
    print("LIVE VEGAS LINES")
    print("="*70)
    for game in games:
        print(f"  {game['away_team_name']} @ {game['home_team_name']}")
        if game.get('over_under'):
            print(f"    Over/Under: {game['over_under']}")
        if game.get('spread'):
            print(f"    Spread: {game['spread']}")


if __name__ == "__main__":
    main()
