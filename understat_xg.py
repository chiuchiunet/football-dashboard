#!/usr/bin/env python3
"""
Fetch xG data from Understat and integrate into football.db.
Pilot: EPL only (Premier League 2025-26 season).
"""
import sqlite3
import json
from pathlib import Path
from understatapi import UnderstatClient

DB_PATH = Path(__file__).resolve().parent / "football.db"

# Understat team name → football-data.org team name (EPL)
TEAM_MAPPING = {
    "Arsenal": "Arsenal FC",
    "Aston Villa": "Aston Villa FC",
    "Bournemouth": "AFC Bournemouth",
    "Brentford": "Brentford FC",
    "Brighton": "Brighton & Hove Albion FC",
    "Burnley": "Burnley FC",
    "Chelsea": "Chelsea FC",
    "Crystal Palace": "Crystal Palace FC",
    "Everton": "Everton FC",
    "Fulham": "Fulham FC",
    "Leeds": "Leeds United FC",
    "Liverpool": "Liverpool FC",
    "Manchester City": "Manchester City FC",
    "Manchester United": "Manchester United FC",
    "Newcastle United": "Newcastle United FC",
    "Nottingham Forest": "Nottingham Forest FC",
    "Sunderland": "Sunderland AFC",
    "Tottenham": "Tottenham Hotspur FC",
    "West Ham": "West Ham United FC",
    "Wolverhampton Wanderers": "Wolverhampton Wanderers FC",
}

LEAGUE_MAPPING = {
    "EPL": "PL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Bundesliga": "BL1",
    "Ligue 1": "FL1",
}


def fetch_understat_xg(league_code: str = "EPL", season: str = "2025") -> dict:
    """Fetch team xG stats from Understat."""
    understat = UnderstatClient()
    teams = understat.league(league=league_code).get_team_data(season=season)

    result = {}
    for team_id, data in teams.items():
        title = data["title"]
        history = data.get("history", [])

        total_xg = sum(float(m["xG"]) for m in history)
        total_xga = sum(float(m["xGA"]) for m in history)
        total_scored = sum(int(m["scored"]) for m in history)
        total_missed = sum(int(m["missed"]) for m in history)
        total_pts = sum(int(m["pts"]) for m in history)
        played = len(history)

        # Home/Away split
        home_matches = [m for m in history if m["h_a"] == "h"]
        away_matches = [m for m in history if m["h_a"] == "a"]

        home_xg = sum(float(m["xG"]) for m in home_matches)
        away_xg = sum(float(m["xG"]) for m in away_matches)
        home_xga = sum(float(m["xGA"]) for m in home_matches)
        away_xga = sum(float(m["xGA"]) for m in away_matches)

        result[title] = {
            "understat_id": team_id,
            "played": played,
            "xg": round(total_xg / played, 3) if played else 0,
            "xga": round(total_xga / played, 3) if played else 0,
            "npxg": round(sum(float(m["npxG"]) for m in history) / played, 3) if played else 0,
            "npxga": round(sum(float(m["npxGA"]) for m in history) / played, 3) if played else 0,
            "scored": total_scored,
            "missed": total_missed,
            "xpts": round(sum(float(m.get("xpts", 0)) for m in history), 1),
            "pts": total_pts,
            "home_xg": round(home_xg / len(home_matches), 3) if home_matches else 0,
            "away_xg": round(away_xg / len(away_matches), 3) if away_matches else 0,
            "home_xga": round(home_xga / len(home_matches), 3) if home_matches else 0,
            "away_xga": round(away_xga / len(away_matches), 3) if away_matches else 0,
        }
    return result


def create_xg_table():
    """Create understat_xg table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS understat_xg (
            team_name TEXT PRIMARY KEY,
            understat_id TEXT,
            played INTEGER,
            xg REAL,
            xga REAL,
            npxg REAL,
            npxga REAL,
            scored INTEGER,
            missed INTEGER,
            xpts REAL,
            pts INTEGER,
            home_xg REAL,
            away_xg REAL,
            home_xga REAL,
            away_xga REAL,
            league_code TEXT,
            season TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def upsert_xg_data(xg_data: dict, league_code: str, season: str = "2025"):
    """Insert or replace xG data into DB."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for understat_name, stats in xg_data.items():
        fd_name = TEAM_MAPPING.get(understat_name, understat_name)
        cur.execute("""
            INSERT OR REPLACE INTO understat_xg
            (team_name, understat_id, played, xg, xga, npxg, npxga, scored, missed, xpts, pts,
             home_xg, away_xg, home_xga, away_xga, league_code, season, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            fd_name, stats["understat_id"], stats["played"],
            stats["xg"], stats["xga"], stats["npxg"], stats["npxga"],
            stats["scored"], stats["missed"], stats["xpts"], stats["pts"],
            stats["home_xg"], stats["away_xg"], stats["home_xga"], stats["away_xga"],
            league_code, season
        ))
    conn.commit()
    conn.close()


def show_current_xg():
    """Show current xG data in DB."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute("SELECT team_name, played, xg, xga, pts FROM understat_xg WHERE league_code='PL' ORDER BY xg DESC").fetchall()
    print(f"{'Team':<30} {'M':>3} {'xG':>6} {'xGA':>6} {'Pts':>5}")
    print("-" * 55)
    for r in rows:
        print(f"{r[0]:<30} {r[1]:>3} {r[2]:>6.2f} {r[3]:>6.2f} {r[4]:>5}")
    conn.close()


if __name__ == "__main__":
    print("📊 Fetching EPL xG data from Understat...")
    xg_data = fetch_understat_xg("EPL", "2025")
    print(f"Fetched {len(xg_data)} teams")

    create_xg_table()
    upsert_xg_data(xg_data, "PL", "2025")
    print("✅ xG data saved to football.db\n")

    show_current_xg()
