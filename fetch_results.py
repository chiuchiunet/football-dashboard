#!/usr/bin/env python3
"""Fetch real World Cup 2026 match results from worldcup26.ir"""
import requests, json, os, sys
from datetime import datetime

API_BASE = "https://worldcup26.ir"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(DATA_DIR, "real_results.json")

def fetch_results():
    """Fetch all match results from worldcup26.ir"""
    r = requests.get(f"{API_BASE}/get/games", timeout=60)
    r.raise_for_status()
    games = r.json()["games"]

    # Fetch teams for name mapping
    r2 = requests.get(f"{API_BASE}/get/teams", timeout=60)
    teams_data = r2.json() if isinstance(r2.json(), list) else r2.json().get("teams", [])
    team_map = {t["id"]: t["name_en"] for t in teams_data}
    
    results = {}
    for g in games:
        match_id = g["id"]
        finished = g.get("finished", "FALSE").upper() == "TRUE"
        
        # Build match info
        match_info = {
            "id": match_id,
            "group": g.get("group", ""),
            "type": g.get("type", ""),
            "date": g.get("local_date", ""),
            "finished": finished,
            "time_elapsed": g.get("time_elapsed", ""),
        }
        
        # Determine home/away teams
        if g["home_team_id"] == "0":
            # Knockout stage - TBD
            match_info["home_team"] = g.get("home_team_label", "TBD")
            match_info["away_team"] = g.get("away_team_label", "TBD")
        else:
            match_info["home_team"] = team_map.get(g["home_team_id"], g.get("home_team_name_en", "?"))
            match_info["away_team"] = team_map.get(g["away_team_id"], g.get("away_team_name_en", "?"))
        
        # Scores
        if finished:
            match_info["home_score"] = int(g.get("home_score") or 0)
            match_info["away_score"] = int(g.get("away_score") or 0)
        else:
            match_info["home_score"] = None
            match_info["away_score"] = None
        
        results[match_id] = match_info
    
    return results

def save_results(results):
    """Save results to JSON file"""
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(),
            "matches": results
        }, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(results)} matches to {RESULTS_FILE}")

def load_results():
    """Load cached results"""
    if not os.path.exists(RESULTS_FILE):
        return None
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["matches"]

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching World Cup 2026 results...")
    try:
        results = fetch_results()
        save_results(results)
        
        # Summary
        finished = sum(1 for m in results.values() if m["finished"])
        print(f"Total: {len(results)} matches | Finished: {finished}")
        
        # Show finished matches
        print("\n=== Finished Matches ===")
        for m in sorted(results.values(), key=lambda x: x["date"]):
            if m["finished"]:
                print(f"  {m['date'][:10]} | {m['home_team']} {m['home_score']}-{m['away_score']} {m['away_team']}")
        
        return 0
    except Exception as e:
        # API 唔穩定 (e.g. 502 Bad Gateway) — 唔好 crash cron
        # 用舊 cache 嘅 real_results.json 繼續行 gen_wc.py
        print(f"⚠️  Fetch failed: {e}")
        print(f"⚠️  Will use cached {os.path.basename(RESULTS_FILE)} (if exists)")
        cached = load_results()
        if cached:
            finished = sum(1 for m in cached.values() if m.get("finished"))
            print(f"📦 Cached: {len(cached)} matches | Finished: {finished}")
            return 0
        # 連 cache 都冇，先 exit 1
        print("❌ No cached data available")
        return 1

if __name__ == "__main__":
    sys.exit(main())