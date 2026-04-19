#!/usr/bin/env python3
"""
Fetch recent match results from football-data.org API and update DB.
Replaces CSV workflow for faster, more up-to-date results.
"""
import os
import sqlite3
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Load .env
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))
from config import API_KEY, DB_PATH

try:
    import requests
except ImportError:
    print("❌ requests library not found. Run: pip install requests")
    sys.exit(1)


# Competitions to fetch (use same codes as football-data.org)
COMPETITIONS = {
    "PL": "Premier League",
    "PD": "La Liga", 
    "SA": "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1",
    "CL": "Champions League",
}


class ResultsFetcher:
    def __init__(self, api_key: str):
        self.key = api_key
        self.base_url = "https://api.football-data.org/v4"
        self.session = requests.Session()
        self.session.headers.update({"X-Auth-Token": api_key})
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def get_recent_results(self, competition_code: str, days_back: int = 7) -> list:
        """Fetch finished matches from the past N days."""
        today = datetime.now(timezone.utc).date()
        date_from = (datetime.now(timezone.utc) - timedelta(days=days_back)).date()
        
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        params = {
            "dateFrom": date_from.isoformat(),
            "dateTo": today.isoformat(),
            "status": "FINISHED",
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=30)
            if resp.status_code == 429:
                print(f"  ⏳ Rate limited for {competition_code}")
                return []
            if resp.status_code == 403:
                print(f"  ❌ No access for {competition_code} (possible tier restriction)")
                return []
            resp.raise_for_status()
            return resp.json().get("matches", [])
        except Exception as e:
            print(f"  ❌ Error fetching {competition_code}: {e}")
            return []

    def upsert_match(self, conn: sqlite3.Connection, match: dict) -> bool:
        """Insert or update a match in the database."""
        cur = conn.cursor()
        
        mid = match.get("id")
        utc_date = match.get("utcDate", "")
        home = match.get("homeTeam", {}) or {}
        away = match.get("awayTeam", {}) or {}
        comp = match.get("competition", {}) or {}
        score = match.get("score", {}) or {}
        ft = score.get("fullTime", {}) or {}
        
        home_name = home.get("name") or "TBD"
        away_name = away.get("name") or "TBD"
        home_score = ft.get("home")
        away_score = ft.get("away")
        
        if home_score is None or away_score is None:
            return False
        
        # Determine winner
        if home_score > away_score:
            winner = "HOME_TEAM"
        elif home_score < away_score:
            winner = "AWAY_TEAM"
        else:
            winner = "DRAW"
        
        # Check if exists
        cur.execute("SELECT match_id FROM matches WHERE match_id = ?", (mid,))
        exists = cur.fetchone()
        
        if exists:
            # Update existing
            cur.execute("""
                UPDATE matches SET
                    status = 'FINISHED',
                    home_score = ?,
                    away_score = ?,
                    winner = ?,
                    last_updated = ?
                WHERE match_id = ?
            """, (home_score, away_score, winner, datetime.now(timezone.utc).isoformat(), mid))
            return False  # not new
        else:
            # Insert new
            cur.execute("""
                INSERT INTO matches (
                    match_id, competition_code, utc_date, status,
                    home_team_id, away_team_id, home_team_name, away_team_name,
                    home_score, away_score, winner, last_updated, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mid,
                comp.get("code", ""),
                utc_date,
                "FINISHED",
                home.get("id") or 0,
                away.get("id") or 0,
                home_name,
                away_name,
                home_score,
                away_score,
                winner,
                datetime.now(timezone.utc).isoformat(),
                json.dumps(match)
            ))
            return True  # new


def main():
    print(f"📊 Fetching recent results via API...")
    print(f"   API Key present: {'Yes' if API_KEY else 'No'}")
    
    if not API_KEY:
        print("❌ FOOTBALL_API_KEY not set")
        sys.exit(1)
    
    fetcher = ResultsFetcher(API_KEY)
    conn = sqlite3.connect(DB_PATH)
    total_new = 0
    total_updated = 0
    
    for comp_code, comp_name in COMPETITIONS.items():
        print(f"\n🔍 {comp_name} ({comp_code})...", end=" ", flush=True)
        matches = fetcher.get_recent_results(comp_code, days_back=7)
        
        if not matches:
            print("no data (rate limited or no matches)")
            continue
        
        new_count = 0
        upd_count = 0
        for m in matches:
            is_new = fetcher.upsert_match(conn, m)
            if is_new:
                new_count += 1
            else:
                upd_count += 1
        
        conn.commit()
        print(f"{len(matches)} matches, {new_count} new, {upd_count} updated")
        total_new += new_count
        total_updated += upd_count
    
    conn.close()
    
    print(f"\n✅ Done! {total_new} new matches, {total_updated} updated.")
    return total_new + total_updated


if __name__ == "__main__":
    main()
