#!/usr/bin/env python3
"""Fetch odds from OddsPapi - simplified version."""

from __future__ import annotations
import sqlite3
import json
import os
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path(__file__).resolve().parent / "football.db"
ODDSPAPI_KEY = os.environ.get("ODDSPAPI_KEY", "")

BOOKMAKER = "pinnacle"


def implied_prob(odds: float) -> float:
    if odds <= 1:
        return 1.0
    return 1.0 / odds


def api_get(url: str) -> dict:
    import urllib.request
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def fetch_tournaments() -> dict:
    """Fetch all tournaments, return dict of name->id."""
    url = f"https://api.oddspapi.io/v4/tournaments?sportId=10&apiKey={ODDSPAPI_KEY}"
    data = api_get(url)
    
    result = {}
    for t in data:
        name = t.get("tournamentName", "").lower()
        result[t["tournamentId"]] = t.get("tournamentName")
    return result


def fetch_fixtures_by_ids(tournament_ids: list[int], from_date: str, to_date: str) -> list:
    """Fetch fixtures for given tournaments."""
    ids = ",".join(str(tid) for tid in tournament_ids)
    url = f"https://api.oddspapi.io/v4/fixtures?sportId=10&tournamentIds={ids}&from={from_date}&to={to_date}&apiKey={ODDSPAPI_KEY}"
    data = api_get(url)
    return data if isinstance(data, list) else []


def store_odds(match_id: int, home_odds: float, draw_odds: float, away_odds: float) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            INSERT INTO bookmaker_odds (match_id, bookmaker, home_win_odds, draw_odds, away_win_odds, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(match_id) DO UPDATE SET
                bookmaker = excluded.bookmaker,
                home_win_odds = excluded.home_win_odds,
                draw_odds = excluded.draw_odds,
                away_win_odds = excluded.away_win_odds,
                updated_at = CURRENT_TIMESTAMP
        """, (match_id, BOOKMAKER, home_odds, draw_odds, away_odds))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error storing odds: {e}")
        return False


def calculate_value_bets(min_edge: float = 0.05) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT m.match_id, m.utc_date, m.competition_code,
               m.home_team_name, m.away_team_name,
               p.home_win_prob, p.draw_prob, p.away_win_prob,
               b.home_win_odds, b.draw_odds, b.away_win_odds,
               p.expected_home_goals, p.expected_away_goals
        FROM matches m
        JOIN predictions p ON p.match_id = m.match_id
        JOIN bookmaker_odds b ON b.match_id = m.match_id
        WHERE m.status IN ('SCHEDULED', 'TIMED')
          AND b.bookmaker = ?
    """, (BOOKMAKER,)).fetchall()
    conn.close()
    
    value_bets = []
    for row in rows:
        match_id, utc_date, comp, home, away, hwp, dp, awp, ho, do, ao, ehg, eag = row
        
        if not all([hwp, dp, awp, ho, do, ao]):
            continue
        
        ih, id_, ia = implied_prob(ho), implied_prob(do), implied_prob(ao)
        edges = {"Home": hwp - ih, "Draw": dp - id_, "Away": awp - ia}
        best = max(edges.items(), key=lambda x: x[1])
        
        if best[1] >= min_edge:
            value_bets.append({
                "match_id": match_id,
                "competition_code": comp,
                "home": home,
                "away": away,
                "utc_date": utc_date,
                "bet_type": best[0],
                "bet_odds": {"Home": ho, "Draw": do, "Away": ao}[best[0]],
                "model_prob": {"Home": hwp, "Draw": dp, "Away": awp}[best[0]],
                "implied_prob": {"Home": ih, "Draw": id_, "Away": ia}[best[0]],
                "edge": best[1],
                "expected_goals": f"{ehg:.1f}-{eag:.1f}",
            })
    
    return sorted(value_bets, key=lambda x: x["edge"], reverse=True)


def main():
    if not ODDSPAPI_KEY:
        print("❌ ODDSPAPI_KEY not set")
        return
    
    from_date = date.today().isoformat()
    to_date = (date.today() + timedelta(days=7)).isoformat()
    
    print("📊 Fetching tournaments to find target IDs...")
    tournaments = fetch_tournaments()
    
    # Find target tournament IDs by name search
    target_keywords = {
        "champions league": None,
        "premier league": None,
        "la liga": None,
        "serie a": None,
        "bundesliga": None,
        "ligue 1": None,
        "liga portugal": None,
    }
    
    for tid, name in tournaments.items():
        name_lower = name.lower()
        for keyword in target_keywords:
            if keyword in name_lower:
                target_keywords[keyword] = tid
    
    print("Found tournaments:")
    for kw, tid in target_keywords.items():
        print(f"  {kw}: {tid}")
    
    # Get target IDs
    target_ids = [tid for tid in target_keywords.values() if tid]
    if not target_ids:
        print("No target tournaments found!")
        return
    
    print(f"\n📅 Fetching fixtures for {len(target_ids)} tournaments...")
    fixtures = fetch_fixtures_by_ids(target_ids, from_date, to_date)
    print(f"Found {len(fixtures)} total fixtures")
    
    # Get our DB matches
    conn = sqlite3.connect(DB_PATH)
    db_matches = conn.execute("""
        SELECT match_id, utc_date, competition_code, home_team_name, away_team_name
        FROM matches
        WHERE status IN ('SCHEDULED', 'TIMED')
          AND datetime(utc_date) <= datetime('now', '+7 days')
    """).fetchall()
    conn.close()
    
    print(f"Our DB has {len(db_matches)} upcoming matches")
    
    # Create lookup by team name
    def normalize(name):
        return name.lower().replace(" fc", "").replace(".", "").replace(",", "")
    
    db_lookup = {}
    for m in db_matches:
        key = (normalize(m[3]), normalize(m[4]))
        db_lookup[key] = {"match_id": m[0], "utc_date": m[1], "comp": m[2]}
    
    # Match fixtures to DB matches
    odds_stored = 0
    for f in fixtures:
        p1 = normalize(f.get("participant1Name", ""))
        p2 = normalize(f.get("participant2Name", ""))
        key = (p1, p2)
        
        if key in db_lookup:
            db_match = db_lookup[key]
            # This fixture has odds embedded
            bo = f.get("bookmakerOdds", {})
            pinnacle = bo.get("pinnacle", {})
            markets = pinnacle.get("markets", {})
            moneyline = markets.get("101", markets.get("h2h", {}))
            
            try:
                outcomes = moneyline.get("outcomes", {})
                home_odds = float(outcomes.get("101", {}).get("price", 0))
                draw_odds = float(outcomes.get("102", {}).get("price", 0))
                away_odds = float(outcomes.get("103", {}).get("price", 0))
                
                if all([home_odds, draw_odds, away_odds]):
                    if store_odds(db_match["match_id"], home_odds, draw_odds, away_odds):
                        odds_stored += 1
                        print(f"  ✓ {f.get('participant1Name')} vs {f.get('participant2Name')}: {home_odds}-{draw_odds}-{away_odds}")
            except (KeyError, TypeError, ValueError):
                pass
    
    print(f"\n📊 Stored odds for {odds_stored} matches")
    
    # Calculate value bets
    if odds_stored > 0:
        value_bets = calculate_value_bets()
        print(f"\n💎 Found {len(value_bets)} value bets:")
        for vb in value_bets[:10]:
            print(f"  {vb['home']} vs {vb['away']} ({vb['competition_code']})")
            print(f"    Bet: {vb['bet_type']} @ {vb['bet_odds']} (Edge: {vb['edge']*100:.1f}%)")


if __name__ == "__main__":
    main()
