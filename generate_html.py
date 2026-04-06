#!/usr/bin/env python3
"""Generate HTML dashboard for football predictions."""

from __future__ import annotations
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "football.db"

COLORS = {
    "primary": "#1a1a2e",
    "secondary": "#16213e",
    "accent": "#e94560",
    "accent2": "#0f3460",
    "text": "#eaeaea",
    "muted": "#a0a0a0",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "danger": "#f87171",
}

COMP_EMOJI = {
    "CL": "🏆", "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "PD": "🇪🇸", "SA": "🇮🇹",
    "BL1": "🇩🇪", "FL1": "🇫🇷", "EL": "🇪🇺", "EC": "🏆",
}


def get_predictions(days_ahead: int = 7) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.create_function("REGEXP", 2, lambda p, s: bool(__import__("re").search(p, s or "")))
    cursor = conn.execute("""
        SELECT m.match_id, m.utc_date, m.competition_code, m.home_team_name, m.away_team_name,
               m.home_team_id, m.away_team_id,
               p.home_win_prob, p.draw_prob, p.away_win_prob,
               p.over_2_5_prob, p.under_2_5_prob,
               p.btts_yes_prob, p.btts_no_prob,
               p.expected_home_goals, p.expected_away_goals,
               p.recommended_bets
        FROM matches m
        LEFT JOIN predictions p ON p.match_id = m.match_id
        WHERE m.status IN ('SCHEDULED', 'TIMED')
          AND datetime(m.utc_date) <= datetime('now', ?)
        ORDER BY datetime(m.utc_date) ASC
    """, [f"+{days_ahead} days"])
    
    rows = cursor.fetchall()
    conn.close()
    return rows


def color_bar(prob: float) -> str:
    if prob >= 0.5:
        return f"rgba(74, 222, 128, {prob:.2f})"
    elif prob >= 0.35:
        return f"rgba(251, 191, 36, {prob:.2f})"
    else:
        return f"rgba(248, 113, 113, {prob:.2f})"


def team_badge(home_name: str, away_name: str) -> str:
    return f"""
    <div class="team-badge">
        <div class="team-name">{home_name}</div>
        <div class="vs">vs</div>
        <div class="team-name">{away_name}</div>
    </div>"""


def prediction_card(row: dict) -> str:
    utc_date = row.get('utc_date', '')
    comp = row.get('competition_code', '')
    home = row.get('home_team_name', '')
    away = row.get('away_team_name', '')
    home_id = row.get('home_team_id', 0)
    away_id = row.get('away_team_id', 0)
    hwp = row.get('home_win_prob') or 0
    dp = row.get('draw_prob') or 0
    awp = row.get('away_win_prob') or 0
    ov = row.get('over_2_5_prob') or 0
    un = row.get('under_2_5_prob') or 0
    bts_yes = row.get('btts_yes_prob') or 0
    bts_no = row.get('btts_no_prob') or 0
    ehg = row.get('expected_home_goals') or 0
    eag = row.get('expected_away_goals') or 0
    bets = row.get('recommended_bets', '')
    
    # Format date
    dt = utc_date.replace("T", " ").replace("Z", "")[:16]
    emoji = COMP_EMOJI.get(comp, "⚽")
    
    # Determine favorite
    probs = {"主勝": hwp, "和": dp, "客勝": awp}
    fav = max(probs, key=probs.get)
    fav_prob = probs[fav]
    fav_color = "#4ade80" if fav_prob > 0.45 else "#fbbf24" if fav_prob > 0.35 else "#f87171"
    
    # Expected score
    score = f"{ehg:.1f} - {eag:.1f}"
    likely_score = f"{int(ehg+0.5)}-{int(eag+0.5)}"
    
    return f"""
    <div class="match-card">
        <div class="match-header">
            <span class="comp-badge">{emoji} {comp}</span>
            <span class="match-time">📅 {dt} UTC</span>
        </div>
        <div class="teams">
            <div class="team {home}">{home}</div>
            <div class="score-preview">⚽ {likely_score}</div>
            <div class="team {away}">{away}</div>
        </div>
        
        <div class="prob-grid">
            <div class="prob-bar-container">
                <div class="prob-label">主勝 {hwp*100:.0f}%</div>
                <div class="prob-bar">
                    <div class="prob-fill" style="width:{hwp*100:.0f}%; background:{color_bar(hwp)}"></div>
                </div>
            </div>
            <div class="prob-bar-container">
                <div class="prob-label">和 {dp*100:.0f}%</div>
                <div class="prob-bar">
                    <div class="prob-fill" style="width:{dp*100:.0f}%; background:{color_bar(dp)}"></div>
                </div>
            </div>
            <div class="prob-bar-container">
                <div class="prob-label">客勝 {awp*100:.0f}%</div>
                <div class="prob-bar">
                    <div class="prob-fill" style="width:{awp*100:.0f}%; background:{color_bar(awp)}"></div>
                </div>
            </div>
        </div>
        
        <div class="secondary-preds">
            <div class="sec-item">
                <span class="sec-label">大細 2.5</span>
                <span class="sec-val" style="color:{'#4ade80' if ov > 0.5 else '#f87171'}">大 {ov*100:.0f}%</span>
                <span class="sec-val" style="color:{'#4ade80' if un > 0.5 else '#f87171'}">細 {un*100:.0f}%</span>
            </div>
            <div class="sec-item">
                <span class="sec-label">BTTS</span>
                <span class="sec-val" style="color:{'#4ade80' if bts_yes > 0.5 else '#f87171'}">Yes {bts_yes*100:.0f}%</span>
                <span class="sec-val" style="color:{'#4ade80' if bts_no > 0.5 else '#f87171'}">No {bts_no*100:.0f}%</span>
            </div>
        </div>
        
        <div class="value-bets">
            💎 Value Bets: {bets or '暫無'}
        </div>
        
        <div class="fav-badge" style="background:{fav_color}20; border-left: 3px solid {fav_color}">
            最可能結果：<strong>{fav}</strong> ({fav_prob*100:.0f}%)
        </div>
    </div>
    """


def generate_html(predictions, title: str = "⚽ 足球預測報告") -> str:
    # Accept both DataFrame and list of tuples/dicts
    if hasattr(predictions, 'to_dict'):
        rows = predictions.to_dict(orient='records')
    else:
        rows = predictions
    
    cards_html = "\n".join(prediction_card(row) for row in rows)
    
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: {COLORS['text']};
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #e94560, #fbbf24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header p {{
            color: {COLORS['muted']};
            font-size: 0.95em;
        }}
        
        .match-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .match-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(233, 69, 96, 0.2);
        }}
        
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .comp-badge {{
            background: {COLORS['accent']};
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
        }}
        
        .match-time {{
            color: {COLORS['muted']};
            font-size: 0.85em;
        }}
        
        .teams {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
        }}
        
        .team {{
            font-size: 1.1em;
            font-weight: 600;
            flex: 1;
            text-align: center;
        }}
        
        .team:first-child {{ text-align: left; }}
        .team:last-child {{ text-align: right; }}
        
        .vs {{
            color: {COLORS['muted']};
            font-size: 0.8em;
            padding: 0 15px;
        }}
        
        .score-preview {{
            font-size: 1.2em;
            color: {COLORS['accent']};
            font-weight: 700;
        }}
        
        .prob-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .prob-bar-container {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .prob-label {{
            width: 70px;
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .prob-bar {{
            flex: 1;
            height: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            overflow: hidden;
        }}
        
        .prob-fill {{
            height: 100%;
            border-radius: 5px;
            transition: width 0.5s ease;
        }}
        
        .secondary-preds {{
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            padding: 10px;
            background: rgba(0,0,0,0.15);
            border-radius: 10px;
        }}
        
        .sec-item {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .sec-label {{
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .sec-val {{
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .value-bets {{
            font-size: 0.9em;
            color: {COLORS['warning']};
            margin-bottom: 12px;
            padding: 8px 12px;
            background: rgba(251,191,36,0.1);
            border-radius: 8px;
        }}
        
        .fav-badge {{
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: {COLORS['muted']};
            font-size: 0.8em;
        }}
        
        .no-data {{
            text-align: center;
            padding: 60px;
            color: {COLORS['muted']};
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ 足球預測報告</h1>
            <p>Football Match Predictions | Poisson Model</p>
        </div>
        
        <div class="matches">
            {cards_html if cards_html else '<div class="no-data">⚠️ 暫時冇可用預測數據</div>'}
        </div>
        
        <div class="footer">
            <p>Generated by Hanni 🐰 | Data: football-data.org</p>
            <p>⚠️ 僅供參考，不構成投注建議</p>
        </div>
    </div>
</body>
</html>"""


def main():
    predictions = get_predictions(days_ahead=7)
    html = generate_html(predictions)
    output = Path(__file__).resolve().parent / "predictions.html"
    output.write_text(html, encoding="utf-8")
    print(f"✅ Dashboard written to: {output}")
    print(f"📊 Total matches: {len(predictions)}")


if __name__ == "__main__":
    main()
