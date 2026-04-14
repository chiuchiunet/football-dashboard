#!/usr/bin/env python3
"""Fetch upcoming fixtures from football-data.org API and store in DB."""

import json
import sys
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import API_KEY, API_BASE_URL, DEFAULT_COMPETITIONS, DB_PATH

try:
    import requests
except ImportError:
    print("❌ requests library not found. Run: pip install requests")
    sys.exit(1)


class FixturesFetcher:
    def __init__(self, api_key: str, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-Auth-Token": api_key})
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})

    def get_fixtures(self, competition_code: str, days_ahead: int = 14) -> list:
        """Fetch upcoming fixtures for a competition."""
        today = datetime.now(timezone.utc).date()
        date_to = (datetime.now(timezone.utc) + timedelta(days=days_ahead)).date()
        
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        params = {
            "dateFrom": today.isoformat(),
            "dateTo": date_to.isoformat(),
            "status": "SCHEDULED",
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=30)
            if resp.status_code == 429:
                print(f"  ⏳ Rate limited, waiting 60s...")
                import time
                time.sleep(60)
                resp = self.session.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json().get("matches", [])
        except Exception as e:
            print(f"  ❌ Error fetching {competition_code}: {e}")
            return []

    def upsert_match(self, conn: sqlite3.Connection, match: dict) -> bool:
        """Insert or update a match in the database."""
        cur = conn.cursor()
        
        utc_date = match.get("utcDate", "")
        home = match.get("homeTeam", {}) or {}
        away = match.get("awayTeam", {}) or {}
        home_name = home.get("name") or "TBD"
        away_name = away.get("name") or "TBD"
        
        # Check if already exists
        cur.execute("SELECT match_id FROM matches WHERE utc_date = ? AND home_team_name = ? AND away_team_name = ?",
                    (utc_date, home_name, away_name))
        existing = cur.fetchone()
        
        if existing:
            return False  # Already exists
        
        # Insert new fixture
        cur.execute("""
            INSERT INTO matches (
                competition_code, utc_date, status, stage, matchday,
                home_team_id, away_team_id, home_team_name, away_team_name,
                home_score, away_score, winner, last_updated, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            match.get("competition", {}).get("code", ""),
            utc_date,
            match.get("status", "SCHEDULED"),
            match.get("stage", ""),
            match.get("matchday", None),
            home.get("id") or 0,
            away.get("id") or 0,
            home_name,
            away_name,
            None, None, None,
            datetime.now(timezone.utc).isoformat(),
            json.dumps(match)
        ))
        return True


def main():
    print("📅 Fetching upcoming fixtures from football-data.org API...")
    
    if not API_KEY:
        print("❌ FOOTBALL_API_KEY not set in .env")
        sys.exit(1)
    
    fetcher = FixturesFetcher(API_KEY, API_BASE_URL)
    
    conn = sqlite3.Connection(DB_PATH)
    total_added = 0
    
    for comp in DEFAULT_COMPETITIONS:
        print(f"\n🔍 {comp}...", end=" ", flush=True)
        fixtures = fetcher.get_fixtures(comp, days_ahead=14)
        
        if not fixtures:
            print("no upcoming matches")
            continue
        
        added = 0
        for fx in fixtures:
            if fetcher.upsert_match(conn, fx):
                added += 1
        
        conn.commit()
        print(f"{len(fixtures)} fixtures found, {added} new")
        total_added += added
    
    conn.close()
    
    print(f"\n✅ Done! {total_added} new fixtures added.")


if __name__ == "__main__":
    main()
