import requests
import os
from datetime import datetime, timezone

# Free API from football-data.org (requires free API key set as FOOTBALL_DATA_API_KEY env var)
FOOTBALL_DATA_BASE_URL = "https://api.football-data.org/v4"

# Leagues available on free tier
LEAGUES = {
    "PL":  "🏴󠁧󠁢󠁥󠁮󠁧󠁿 English Premier League",
    "PD":  "🇪🇸 Spanish La Liga",
    "BL1": "🇩🇪 German Bundesliga",
    "SA":  "🇮🇹 Italian Serie A",
    "FL1": "🇫🇷 French Ligue 1",
    "CL":  "🏆 UEFA Champions League",
}


def _get_headers():
    api_key = os.getenv("FOOTBALL_DATA_API_KEY", "")
    return {"X-Auth-Token": api_key}


def _fetch_todays_matches():
    """Fetch all matches scheduled for today across tracked leagues."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    matches = []
    headers = _get_headers()

    for competition_code in LEAGUES:
        try:
            url = f"{FOOTBALL_DATA_BASE_URL}/competitions/{competition_code}/matches"
            params = {"dateFrom": today, "dateTo": today, "status": "SCHEDULED,TIMED"}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for match in data.get("matches", []):
                    matches.append({
                        "competition": LEAGUES[competition_code],
                        "competition_code": competition_code,
                        "home_team": match["homeTeam"]["name"],
                        "away_team": match["awayTeam"]["name"],
                        "utc_date": match.get("utcDate", ""),
                        "matchday": match.get("matchday"),
                        "home_id": match["homeTeam"].get("id"),
                        "away_id": match["awayTeam"].get("id"),
                        "match_id": match.get("id"),
                    })
        except Exception as e:
            print(f"⚠️  Could not fetch matches for {competition_code}: {e}")

    return matches


def _fetch_standings(competition_code):
    """Fetch current standings for a competition and return a dict of {team_id: position}."""
    headers = _get_headers()
    try:
        url = f"{FOOTBALL_DATA_BASE_URL}/competitions/{competition_code}/standings"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {}
        data = response.json()
        standings = {}
        for standing_group in data.get("standings", []):
            if standing_group.get("type") == "TOTAL":
                for entry in standing_group.get("table", []):
                    team_id = entry["team"]["id"]
                    standings[team_id] = {
                        "position": entry["position"],
                        "won": entry.get("won", 0),
                        "draw": entry.get("draw", 0),
                        "lost": entry.get("lost", 0),
                        "points": entry.get("points", 0),
                        "goals_for": entry.get("goalsFor", 0),
                        "goals_against": entry.get("goalsAgainst", 0),
                        "played": entry.get("playedGames", 0),
                    }
        return standings
    except Exception:
        return {}


def _predict_outcome(home_stats, away_stats):
    """
    Simple heuristic prediction based on standings.
    Returns a tuple: (prediction_label, confidence_pct, reasoning)
    """
    # Home advantage base boost
    HOME_ADVANTAGE = 5  # extra points equivalent

    if not home_stats and not away_stats:
        return "Draw / Uncertain", 40, "No standings data available; result is unpredictable."

    if not home_stats or not away_stats:
        return "Draw / Uncertain", 40, "Incomplete data for one team."

    home_points = home_stats["points"] + HOME_ADVANTAGE
    away_points = away_stats["points"]

    home_position = home_stats["position"]
    away_position = away_stats["position"]

    home_played = home_stats["played"] or 1
    away_played = away_stats["played"] or 1

    # Points per game (normalised)
    home_ppg = home_points / home_played
    away_ppg = away_points / away_played

    diff = home_ppg - away_ppg

    if diff > 0.4:
        label = "Home Win"
        confidence = min(75, 50 + int(diff * 30))
        reason = (
            f"Home side sit {away_position - home_position} places higher in the table "
            f"and enjoy home advantage."
        )
    elif diff < -0.4:
        label = "Away Win"
        confidence = min(75, 50 + int(abs(diff) * 30))
        reason = (
            f"Away side sit {home_position - away_position} places higher in the table "
            f"despite the travel disadvantage."
        )
    else:
        label = "Draw"
        confidence = 40
        reason = "Both sides are evenly matched; a draw is the most likely outcome."

    return label, confidence, reason


def get_football_predictions():
    """
    Fetch today's matches and return a list of prediction dicts.

    Each dict has:
        competition, home_team, away_team, kickoff, prediction, confidence, reasoning
    """
    print("⚽ Fetching today's football fixtures...")
    matches = _fetch_todays_matches()

    if not matches:
        print("📭 No matches scheduled today across tracked leagues.")
        return []

    print(f"📋 Found {len(matches)} match(es) today. Generating predictions...")

    # Cache standings per competition to avoid redundant API calls
    standings_cache = {}
    predictions = []

    for match in matches:
        comp_code = match["competition_code"]
        if comp_code not in standings_cache:
            standings_cache[comp_code] = _fetch_standings(comp_code)

        standings = standings_cache[comp_code]
        home_stats = standings.get(match["home_id"])
        away_stats = standings.get(match["away_id"])

        prediction, confidence, reasoning = _predict_outcome(home_stats, away_stats)

        # Format kickoff time
        kickoff = match["utc_date"]
        try:
            dt = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))
            kickoff_fmt = dt.strftime("%H:%M UTC")
        except Exception:
            kickoff_fmt = kickoff

        predictions.append({
            "competition": match["competition"],
            "home_team": match["home_team"],
            "away_team": match["away_team"],
            "kickoff": kickoff_fmt,
            "prediction": prediction,
            "confidence": confidence,
            "reasoning": reasoning,
        })

    return predictions
