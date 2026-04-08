#!/usr/bin/env python3
"""
更新賽果及預測準確度
自動 fetch 最新賽果，更新 match_results 表
"""
import sqlite3
import urllib.request
import json
from datetime import datetime, timedelta

DB_PATH = '/home/ubuntu/.openclaw/workspace-football/football.db'
API_KEY = '40da067a02msh8a2e6e63f76p10d4ejsn17f40b6bef41'  # Need to get from DB

def get_api_key():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT api_key FROM api_keys WHERE source = 'football-data.org' LIMIT 1")
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def update_finished_matches():
    api_key = get_api_key()
    if not api_key:
        print("No API key found")
        return 0
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get TIMED matches that may now be finished
    cur.execute('''
        SELECT DISTINCT m.match_id, m.home_team_id, m.away_team_id, m.utc_date, 
               m.home_team_name, m.away_team_name
        FROM matches m
        WHERE m.status IN ('TIMED', 'SCHEDULED', 'IN_PLAY', 'PAUSED', 'FINISHED')
    ''')
    matches = cur.fetchall()
    
    updated = 0
    
    for mid, home_id, away_id, utc_date, home_name, away_name in matches:
        # Fetch this match from API
        url = f"https://api.football-data.org/v4/matches/{mid}"
        req = urllib.request.Request(url, headers={'X-Auth-Token': api_key})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                match_data = data.get('match', {})
                
                status = match_data.get('status', '')
                score = match_data.get('score', {})
                
                if score and status == 'FINISHED':
                    ft = score.get('fullTime', {})
                    home_score = ft.get('home', None)
                    away_score = ft.get('away', None)
                    
                    if home_score is not None and away_score is not None:
                        # Update matches table
                        cur.execute('''
                            UPDATE matches 
                            SET status = 'FINISHED',
                                home_score = ?,
                                away_score = ?,
                                last_updated = datetime('now')
                            WHERE match_id = ?
                        ''', (home_score, away_score, mid))
                        
                        # Calculate actual result
                        if home_score > away_score:
                            actual = 'H'
                        elif home_score == away_score:
                            actual = 'D'
                        else:
                            actual = 'A'
                        
                        # Get prediction and calculate accuracy
                        cur.execute('''
                            SELECT home_win_prob, draw_prob, away_win_prob
                            FROM predictions
                            WHERE match_id = ?
                            ORDER BY prediction_id DESC LIMIT 1
                        ''', (mid,))
                        pred_row = cur.fetchone()
                        
                        if pred_row:
                            hwp, dp, ap = pred_row
                            probs = {'H': hwp or 0.33, 'D': dp or 0.33, 'A': ap or 0.34}
                            pred = max(probs, key=probs.get)
                            correct = 1 if actual == pred else 0
                            
                            # Insert/update match_results
                            cur.execute('''
                                INSERT OR REPLACE INTO match_results 
                                (match_id, actual_home_score, actual_away_score, actual_result,
                                 prediction_correct_outcome, confidence_when_predicted, updated_at)
                                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                            ''', (mid, home_score, away_score, actual, correct, probs[pred]))
                            
                            print(f"  {home_name[:15]} vs {away_name[:15]}: {home_score}-{away_score} ({actual}) - {'✓' if correct else '✗'}")
                            updated += 1
                            
        except Exception as e:
            # Match not found or error, skip
            pass
    
    conn.commit()
    
    # Update accuracy history
    cur.execute('''
        INSERT INTO accuracy_history (date, competition_code, total_predictions, 
                                     correct_outcome, correct_score, avg_confidence)
        SELECT 
            DATE('now') as date,
            m.competition_code,
            COUNT(*) as total,
            SUM(mr.prediction_correct_outcome) as correct,
            0 as correct_score,
            AVG(mr.confidence_when_predicted) as avg_conf
        FROM match_results mr
        JOIN matches m ON mr.match_id = m.match_id
        WHERE m.competition_code IS NOT NULL
        GROUP BY m.competition_code
    ''')
    conn.commit()
    
    conn.close()
    return updated

if __name__ == '__main__':
    print("Fetching latest match results...")
    n = update_finished_matches()
    print(f"\nUpdated {n} matches")
