#!/usr/bin/env python3
"""
Check finished matches and compare predictions vs actual results.
Sends comparison report via WhatsApp.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "football.db"


def get_unreported_results():
    """Get finished matches that haven't been sent to user yet."""
    conn = sqlite3.connect(DB_PATH)
    
    # Get matches that are finished and have predictions but no result sent
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
            p.recommended_bets,
            m.home_score,
            m.away_score,
            m.winner,
            m.competition_code,
            m.home_team_name,
            m.away_team_name,
            m.utc_date,
            p.generated_at,
            'NO_REPORT' as report_sent_flag
        FROM predictions p
        JOIN matches m ON m.match_id = p.match_id
        WHERE m.status = 'FINISHED'
          AND m.home_score IS NOT NULL
          AND p.generated_at > '2026-04-01'
          AND p.match_id IN (
              SELECT match_id FROM predictions 
              GROUP BY match_id 
              HAVING COUNT(*) = 1
          )
        ORDER BY m.utc_date DESC
        LIMIT 20
    """).fetchall()
    
    conn.close()
    return rows


def format_result_message(rows):
    """Format comparison message."""
    if not rows:
        return None
        
    blocks = []
    blocks.append("📊 **賽後預測 vs 實際結果**\n")
    blocks.append(f"比對最近 {len(rows)} 場比賽：\n")
    
    for row in rows:
        (match_id, home_prob, draw_prob, away_prob, 
         exp_hg, exp_ag, over_prob, btts_prob,
         recommended, home_score, away_score, winner,
         comp, home_name, away_name, utc_date, generated_at, _) = row
        
        # Predicted outcome
        probs = [home_prob, draw_prob, away_prob]
        prob_labels = ["主勝", "和", "客勝"]
        predicted_label = prob_labels[probs.index(max(probs))]
        predicted_confidence = max(probs) * 100
        
        # Actual outcome
        if home_score > away_score:
            actual_label = "主勝"
        elif home_score < away_score:
            actual_label = "客勝"
        else:
            actual_label = "和"
        
        # Check if prediction was correct
        predicted_outcome = ["HOME_TEAM", "DRAW", "AWAY_TEAM"][probs.index(max(probs))]
        if home_score > away_score:
            actual_outcome = "HOME_TEAM"
        elif home_score < away_score:
            actual_outcome = "AWAY_TEAM"
        else:
            actual_outcome = "DRAW"
        
        hit_status = "✅" if predicted_outcome == actual_outcome else "❌"
        
        # Format kickoff time
        kickoff = utc_date.replace('T', ' ').replace('Z', '')[:16] if utc_date else 'N/A'
        
        # Score prediction
        pred_hg_rounded = round(exp_hg)
        pred_ag_rounded = round(exp_ag)
        
        blocks.append(f"{hit_status} **{home_name} vs {away_name}**")
        blocks.append(f"   比分：{home_score} - {away_score}")
        blocks.append(f"   預測：{predicted_label} ({predicted_confidence:.0f}%) → 實際：{actual_label}")
        blocks.append(f"   預測入球：{pred_hg_rounded}-{pred_ag_rounded} | 實際：{home_score}-{away_score}")
        if over_prob > 0.5:
            over_actual = "大" if (home_score + away_score) >= 3 else "細"
            over_pred = "大" if over_prob > 0.5 else "細"
            blocks.append(f"   大細：預測{over_pred} → 實際{over_actual}")
        blocks.append("")
    
    return "\n".join(blocks)


def main():
    rows = get_unreported_results()
    
    if not rows:
        print("NO_REPLY")
        return
    
    message = format_result_message(rows)
    print(message)


if __name__ == "__main__":
    main()