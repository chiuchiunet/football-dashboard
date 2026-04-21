#!/usr/bin/env python3
"""
Daily Football Accuracy Report
Compares predictions vs actual results and outputs a structured report.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent / "football.db"


def get_accuracy_stats():
    conn = sqlite3.connect(DB_PATH)
    
    # Get all predicted + actual matches
    rows = conn.execute("""
        SELECT 
            p.match_id,
            p.home_win_prob,
            p.draw_prob,
            p.away_win_prob,
            p.expected_home_goals,
            p.expected_away_goals,
            p.over_2_5_prob,
            p.btts_yes_prob,
            m.home_score,
            m.away_score,
            m.winner,
            m.competition_code,
            m.home_team_name,
            m.away_team_name,
            p.home_win_prob + p.draw_prob + p.away_win_prob as prob_sum
        FROM predictions p
        JOIN matches m ON m.match_id = p.match_id
        WHERE m.status = 'FINISHED'
          AND m.home_score IS NOT NULL
          AND p.generated_at > '2026-04-01'
        ORDER BY m.utc_date DESC
        LIMIT 50
    """).fetchall()
    
    conn.close()
    
    if not rows:
        return None
    
    # Outcome accuracy
    correct_outcome = 0
    correct_score = 0
    correct_over_2_5 = 0
    correct_btts = 0
    total = len(rows)
    
    # Per-league
    league_stats = defaultdict(lambda: {"total": 0, "correct": 0, "home_correct": 0, "away_correct": 0, "draw_correct": 0})
    
    for row in rows:
        mid, home_prob, draw_prob, away_prob, exp_hg, exp_ag, over_prob, btts_prob, home_score, away_score, winner, comp, h_name, a_name, prob_sum = row
        
        # Actual result
        if home_score > away_score:
            actual = "HOME_TEAM"
        elif home_score < away_score:
            actual = "AWAY_TEAM"
        else:
            actual = "DRAW"
        
        # Predicted
        probs = [home_prob, draw_prob, away_prob]
        predicted = ["HOME_TEAM", "DRAW", "AWAY_TEAM"][probs.index(max(probs))]
        
        # Outcome
        if predicted == actual:
            correct_outcome += 1
            league_stats[comp]["correct"] += 1
        
        league_stats[comp]["total"] += 1
        
        if actual == "HOME_TEAM":
            league_stats[comp]["home_correct"] += 1
        elif actual == "AWAY_TEAM":
            league_stats[comp]["away_correct"] += 1
        else:
            league_stats[comp]["draw_correct"] += 1
        
        # Score
        pred_hg_rounded = round(exp_hg)
        pred_ag_rounded = round(exp_ag)
        if pred_hg_rounded == home_score and pred_ag_rounded == away_score:
            correct_score += 1
        
        # Over 2.5
        total_goals = home_score + away_score
        if (total_goals >= 3) == (over_prob > 0.5):
            correct_over_2_5 += 1
        
        # BTTS
        if (home_score > 0 and away_score > 0) == (btts_prob > 0.5):
            correct_btts += 1
    
    overall = {
        "total": total,
        "outcome_acc": correct_outcome / total * 100,
        "score_acc": correct_score / total * 100,
        "over_2_5_acc": correct_over_2_5 / total * 100,
        "btts_acc": correct_btts / total * 100,
    }
    
    league_breakdown = {}
    for comp, stats in league_stats.items():
        league_breakdown[comp] = {
            "total": stats["total"],
            "outcome_acc": stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0,
        }
    
    return overall, league_breakdown


if __name__ == "__main__":
    result = get_accuracy_stats()
    if result is None:
        print("No data")
    else:
        overall, leagues = result
        print(f"Overall (last 50 PL/CL matches since Apr 2026):")
        print(f"  Outcome: {overall['outcome_acc']:.1f}% ({overall['total']} matches)")
        print(f"  Exact Score: {overall['score_acc']:.1f}%")
        print(f"  Over 2.5: {overall['over_2_5_acc']:.1f}%")
        print(f"  BTTS: {overall['btts_acc']:.1f}%")
        print()
        for comp, stats in leagues.items():
            print(f"  {comp}: {stats['outcome_acc']:.1f}% ({stats['total']} matches)")
