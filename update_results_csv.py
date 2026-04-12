#!/usr/bin/env python3
"""
更新賽果及預測準確度 - 使用 football-data.co.uk CSV
自動下載最新CSV，更新 match_results 表
"""
import sqlite3
import urllib.request
import re
from datetime import datetime

DB_PATH = '/home/ubuntu/.openclaw/workspace-football/football.db'

# football-data.co.uk league codes → DB competition codes
LEAGUE_MAP = {
    'E0': 'PL',    # Premier League
    'E1': 'EL1',   # Championship (England tier 2)
    'E2': 'EL2',   # League One (England tier 3)
    'E3': 'ELC',   # League Two (England tier 4)
    'EC':  None,   # Conference Premier - skip
    'SC0': 'SPL',  # Scottish Premiership
    'SC1': 'SL1',  # Scottish League One
    'SC2': 'SL2',  # Scottish League Two
    'SC3': 'SC3',  # Scottish Championship
    'D1': 'BL1',   # German Bundesliga
    'D2': 'BL2',   # German 2. Bundesliga
    'F1': 'FL1',   # French Ligue 1
    'F2': 'FL2',   # French Ligue 2
    'I1': 'SA',    # Italian Serie A
    'I2': 'SA2',   # Italian Serie B
    'N1': 'ERD',   # Dutch Eredivisie
    'P1': 'LIG',   # Portuguese Primeira Liga
    'SP1': 'PD',   # Spanish La Liga
    'SP2': 'SD',   # Spanish Segunda Division
    'T1': 'TR',    # Turkish Süper Lig
    'B1': 'BKC',   # Belgian Jupiler Pro League
    'CL': 'CL',    # Champions League
    'EL': 'EL',    # Europa League
    'ECL': 'ECL',  # Conference League
}

CSV_BASE = 'https://www.football-data.co.uk'

# New URL structure: mmz{season}/{year}/{code}.csv
# Latest season folder: 2526 (2025/26 season)
# Supported folders by season: 2526, 2425, 2324, 2223, 2122, etc.

# Map league codes to their country page for URL discovery
COUNTRY_PAGES = {
    'E0': 'englandm.php', 'E1': 'englandm.php', 'E2': 'englandm.php', 'E3': 'englandm.php', 'EC': 'englandm.php',
    'SC0': 'scotlandm.php', 'SC1': 'scotlandm.php', 'SC2': 'scotlandm.php', 'SC3': 'scotlandm.php',
    'D1': 'germanym.php', 'D2': 'germanym.php',
    'F1': 'francem.php', 'F2': 'francem.php',
    'I1': 'italym.php', 'I2': 'italym.php',
    'N1': 'netherlandsm.php',
    'P1': 'portugalm.php',
    'SP1': 'spainm.php', 'SP2': 'spainm.php',
    'T1': 'turkeym.php',
    'B1': 'belgiumm.php',
    'CL': 'europeanm.php', 'EL': 'europeanm.php', 'ECL': 'europeanm.php',
}

# Season folders to try (newest first)
SEASON_FOLDERS = ['2526', '2425', '2324', '2223', '2122']


def parse_score(score_str):
    """Parse '2-1' into (home, away)"""
    if not score_str or score_str.strip() == '':
        return None, None
    parts = score_str.strip().split('-')
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except:
        return None, None


def parse_date(date_str):
    """Parse '17/03/2026' into ISO format"""
    try:
        day, month, year = date_str.strip().split('/')
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    except:
        return None


def fetch_csv(league_code):
    """Download CSV for a league code"""
    # Try new mmz{season}/{year}/{code}.csv format first
    for season in SEASON_FOLDERS:
        url = f"{CSV_BASE}/mmz4281/{season}/{league_code}.csv"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode('utf-8', errors='replace')
                # Check if we got valid CSV content (not HTML/404)
                first_lines = content[:500].strip()
                if '<html' in first_lines[:100].lower() or '404' in first_lines[:100]:
                    continue
                if ',' not in first_lines:
                    continue
                print(f"  Success with: {url}")
                return content
        except Exception as e:
            continue
    
    # Fallback: try old mmz.csv pattern
    try:
        url = f"{CSV_BASE}/mmz.csv/{league_code}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
            first_lines = content[:500].strip()
            if '<html' in first_lines[:100].lower() or '404' in first_lines[:100]:
                print(f"  All URLs failed for {league_code}")
                return None
            print(f"  Success with fallback: {url}")
            return content
    except:
        pass
    
    print(f"  All URLs failed for {league_code}")
    return None


def update_from_csv(conn):
    cur = conn.cursor()
    
    # Get all league codes we track
    cur.execute('SELECT DISTINCT competition_code FROM matches')
    db_leagues = [row[0] for row in cur.fetchall()]
    
    # Build reverse map: league code → football-data.co.uk code
    fdco_codes = {v: k for k, v in LEAGUE_MAP.items() if v}
    
    # Add manual codes that are in DB but not in LEAGUE_MAP
    extra_codes = {
        'PL': 'E0',
        'BL1': 'DED',
        'FL1': 'F1',
        'SA': 'I1',
        'PD': 'SP1',
    }
    fdco_codes.update({k: v for k, v in extra_codes.items() if k in db_leagues})
    
    updated = 0
    
    for comp_code, fdco_code in fdco_codes.items():
        if not fdco_code:
            continue
            
        print(f"Fetching {comp_code} ({fdco_code})...")
        csv_content = fetch_csv(fdco_code)
        if not csv_content:
            continue
        
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            continue
        
        header = lines[0].split(',')
        
        # Find column indices
        def col_idx(name):
            try:
                return header.index(name)
            except ValueError:
                return -1
        
        div_idx = col_idx('Div')
        date_idx = col_idx('Date')
        hometeam_idx = col_idx('HomeTeam')
        awayteam_idx = col_idx('AwayTeam')
        # New CSV uses FTHG, FTAG, FTR instead of FT
        fthg_idx = col_idx('FTHG')
        ftag_idx = col_idx('FTAG')
        ftr_idx = col_idx('FTR')
        
        if any(x == -1 for x in [date_idx, hometeam_idx, awayteam_idx, ftr_idx]):
            print(f"  Missing columns in {fdco_code}, skipping")
            continue
        
        for line in lines[1:]:
            cols = line.split(',')
            if len(cols) <= max(date_idx, hometeam_idx, awayteam_idx, ftr_idx):
                continue
            
            date_str = cols[date_idx].strip('"')
            home_team = cols[hometeam_idx].strip('"')
            away_team = cols[awayteam_idx].strip('"')
            ftr = cols[ftr_idx].strip('"')
            
            # Get scores if available
            home_score = int(cols[fthg_idx].strip('"')) if fthg_idx >= 0 and cols[fthg_idx].strip('"').isdigit() else None
            away_score = int(cols[ftag_idx].strip('"')) if ftag_idx >= 0 and cols[ftag_idx].strip('"').isdigit() else None
            
            if not date_str or not home_team or not away_team:
                continue
            
            date_iso = parse_date(date_str)
            
            if date_iso is None:
                continue
            
            # actual result comes from FTR column
            actual = ftr if ftr in ('H', 'D', 'A') else None
            if actual is None:
                continue
            
            # Find match in DB by date + team names
            cur.execute('''
                SELECT match_id, home_team_name, away_team_name, status
                FROM matches
                WHERE utc_date LIKE ? || '%'
                  AND (home_team_name LIKE ? || '%' OR away_team_name LIKE ? || '%')
                  AND competition_code = ?
                LIMIT 1
            ''', (date_iso, home_team[:10], away_team[:10], comp_code))
            
            row = cur.fetchone()
            if not row:
                # Try fuzzy name matching
                cur.execute('''
                    SELECT match_id, home_team_name, away_team_name, status
                    FROM matches
                    WHERE utc_date LIKE ? || '%'
                      AND competition_code = ?
                    LIMIT 10
                ''', (date_iso, comp_code))
                candidates = cur.fetchall()
                
                match_id = None
                for cand in candidates:
                    _, db_home, db_away, _ = cand
                    if (home_team[:6].lower() in db_home[:20].lower() or 
                        db_home[:6].lower() in home_team[:20].lower()) and \
                       (away_team[:6].lower() in db_away[:20].lower() or
                        db_away[:6].lower() in away_team[:20].lower()):
                        match_id = cand[0]
                        break
            else:
                match_id = row[0]
            
            if not match_id:
                continue
            
            # Calculate actual result
            if home_score > away_score:
                actual = 'H'
            elif home_score == away_score:
                actual = 'D'
            else:
                actual = 'A'
            
            # Update match status and scores
            cur.execute('''
                UPDATE matches 
                SET status = 'FINISHED',
                    home_score = ?,
                    away_score = ?,
                    last_updated = datetime('now')
                WHERE match_id = ?
                  AND status != 'FINISHED'
            ''', (home_score, away_score, match_id))
            
            if cur.rowcount > 0:
                # Get prediction
                cur.execute('''
                    SELECT home_win_prob, draw_prob, away_win_prob
                    FROM predictions
                    WHERE match_id = ?
                    ORDER BY prediction_id DESC LIMIT 1
                ''', (match_id,))
                pred_row = cur.fetchone()
                
                if pred_row:
                    hwp, dp, ap = pred_row
                    probs = {'H': hwp or 0.33, 'D': dp or 0.33, 'A': ap or 0.34}
                    pred = max(probs, key=probs.get)
                    correct = 1 if actual == pred else 0
                    
                    cur.execute('''
                        INSERT OR REPLACE INTO match_results 
                        (match_id, actual_home_score, actual_away_score, actual_result,
                         prediction_correct_outcome, confidence_when_predicted, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                    ''', (match_id, home_score, away_score, actual, correct, probs[pred]))
                
                print(f"  ✓ {home_team[:15]} vs {away_team[:15]}: {home_score}-{away_score} ({actual})")
                updated += 1
    
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
          AND mr.updated_at > datetime('now', '-1 day')
        GROUP BY m.competition_code
    ''')
    conn.commit()
    
    return updated


if __name__ == '__main__':
    print(f"Fetching match results from football-data.co.uk...")
    print(f"DB: {DB_PATH}")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    n = update_from_csv(conn)
    conn.close()
    
    print(f"\n✓ Updated {n} matches")
