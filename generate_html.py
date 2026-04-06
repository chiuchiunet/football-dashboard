#!/usr/bin/env python3
"""Generate HTML dashboard for football predictions - Enhanced Version."""

from __future__ import annotations
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

DB_PATH = Path(__file__).resolve().parent / "football.db"

# Modern color palette
COLORS = {
    "bg_primary": "#0f0f1a",
    "bg_card": "#1a1a2e",
    "bg_card_hover": "#222240",
    "accent_pink": "#ff6b9d",
    "accent_blue": "#4ecdc4",
    "accent_yellow": "#ffe66d",
    "accent_purple": "#a855f7",
    "text_primary": "#ffffff",
    "text_secondary": "#a0a0b0",
    "text_muted": "#6b6b80",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "gradient_header": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "gradient_featured": "linear-gradient(135deg, rgba(255,107,157,0.15) 0%, rgba(78,205,196,0.1) 100%)",
    "gradient_card": "linear-gradient(180deg, #1a1a2e 0%, #151528 100%)",
}

# 中文隊名映射
TEAM_NAMES_CN = {
    "Real Madrid CF": "皇家馬德里",
    "FC Bayern München": "拜仁慕尼黑",
    "Arsenal FC": "阿仙奴",
    "Liverpool FC": "利物浦",
    "Paris Saint-Germain FC": "巴黎聖日耳門",
    "FC Barcelona": "巴塞隆拿",
    "Club Atlético de Madrid": "馬德里體育會",
    "Sporting Clube de Portugal": "士砵亭",
    "Manchester City": "曼城",
    "Manchester United": "曼聯",
    "Chelsea FC": "車路士",
    "Tottenham Hotspur FC": "熱刺",
    "Inter Milan": "國際米蘭",
    "AC Milan": "AC米蘭",
    "Juventus FC": "祖雲達斯",
    "Borussia Dortmund": "多蒙特",
    "RB Leipzig": "RB萊比錫",
    "Bayern Munich": "拜仁慕尼黑",
    "Sporting CP": "士砵亭",
    "PSG": "巴黎聖日耳門",
    "Barça": "巴塞隆拿",
    "Atleti": "馬德里體育會",
    "Leverkusen": "利華古遜",
    "Newcastle United": "紐卡素",
    "Atalanta": "阿特蘭大",
    "Benfica": "賓菲加",
    "Celtic": "些路迪",
    "Feyenoord": "飛燕諾",
    "West Ham United FC": "韋斯咸",
    "Aston Villa": "阿士東維拉",
    "Brighton Hove Albion FC": "白禮頓",
    "Wolverhampton Wanderers FC": "狼隊",
    "Crystal Palace": "水晶宮",
    "Fulham FC": "富咸",
    "Brentford FC": "賓福特",
    "AFC Bournemouth": "般尼茅夫",
    "Everton FC": "愛華頓",
    "Nottingham Forest": "諾定咸森林",
    "Burnley FC": "般尼",
    "Sunderland AFC": "新特蘭",
    "Tottenham Hotspur": "熱刺",
    "Brighton & Hove Albion FC": "白禮頓",
    "Wolverhampton Wanderers": "狼隊",
    "Manchester City FC": "曼城",
    "Liverpool FC": "利物浦",
    "West Ham United": "韋斯咸",
    "Brighton": "白禮頓",
}

# 聯賽中文名
COMP_NAMES_CN = {
    "CL": "🏆 歐聯",
    "EL": "🌍 歐霸",
    "EC": "🏆 歐超杯",
    "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英超",
    "PD": "🇪🇸 西甲",
    "SA": "🇮🇹 意甲",
    "BL1": "🇩🇪 德甲",
    "FL1": "🇫🇷 法甲",
    "PO": "🇵🇹 葡超",
    "NL": "🇳🇱 荷甲",
}

# 聯賽漸變色
COMP_GRADIENTS = {
    "CL": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "EL": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
    "PL": "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)",
    "PD": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
    "SA": "linear-gradient(135deg, #22c55e 0%, #15803d 100%)",
    "BL1": "linear-gradient(135deg, #f59e0b 0%, #ca8a04 100%)",
    "FL1": "linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)",
    "PO": "linear-gradient(135deg, #dc2626 0%, #991b1b 100%)",
    "NL": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
}


def get_team_name_cn(name: str) -> str:
    return TEAM_NAMES_CN.get(name, name)


def get_comp_cn(code: str) -> str:
    return COMP_NAMES_CN.get(code, f"⚽ {code}")


def get_comp_gradient(code: str) -> str:
    return COMP_GRADIENTS.get(code, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")


def color_by_prob(prob: float) -> str:
    if prob >= 0.5:
        return "#22c55e"
    elif prob >= 0.35:
        return "#f59e0b"
    else:
        return "#ef4444"


def get_predictions(days_ahead: int = 7) -> list:
    conn = sqlite3.connect(DB_PATH)
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
        ORDER BY m.competition_code, datetime(m.utc_date) ASC
    """, [f"+{days_ahead} days"])
    rows = cursor.fetchall()
    conn.close()
    return rows


def format_match_time(utc_date: str) -> tuple:
    if not utc_date:
        return "TBD", "", "TBD"
    try:
        dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
        hkt = dt.astimezone(timezone(timedelta(hours=8)))
        now_utc = datetime.now(timezone.utc)
        today_hkt = now_utc.astimezone(timezone(timedelta(hours=8))).date()
        match_date = hkt.date()
        
        time_str = hkt.strftime("%H:%M")
        if match_date == today_hkt:
            label = "今日"
        elif match_date == today_hkt + timedelta(days=1):
            label = "明日"
        else:
            label = hkt.strftime("%m/%d")
        
        return time_str, label, hkt.strftime("%Y-%m-%d %H:%M")
    except:
        return utc_date[:16] if utc_date else "TBD", "", utc_date[:16] if utc_date else "TBD"


def prediction_card(row) -> str:
    if isinstance(row, dict):
        (match_id, utc_date, comp, home, away, home_id, away_id,
         hwp, dp, awp, ov, un, bts_yes, bts_no,
         ehg, eag, bets) = (
            row.get('match_id'), row.get('utc_date'), row.get('competition_code'),
            row.get('home_team_name'), row.get('away_team_name'),
            row.get('home_team_id'), row.get('away_team_id'),
            row.get('home_win_prob'), row.get('draw_prob'), row.get('away_win_prob'),
            row.get('over_2_5_prob'), row.get('under_2_5_prob'),
            row.get('btts_yes_prob'), row.get('btts_no_prob'),
            row.get('expected_home_goals'), row.get('expected_away_goals'),
            row.get('recommended_bets')
        )
    elif isinstance(row, (tuple, list)):
        (match_id, utc_date, comp, home, away, home_id, away_id,
         hwp, dp, awp, ov, un, bts_yes, bts_no,
         ehg, eag, bets) = row
    
    hwp = hwp or 0
    dp = dp or 0
    awp = awp or 0
    ov = ov or 0
    un = un or 0
    bts_yes = bts_yes or 0
    bts_no = bts_no or 0
    ehg = ehg or 0
    eag = eag or 0
    
    home_cn = get_team_name_cn(home)
    away_cn = get_team_name_cn(away)
    comp_cn = get_comp_cn(comp)
    comp_gradient = get_comp_gradient(comp)
    
    time_str, date_label, full_time = format_match_time(utc_date)
    
    # 預測總入球 (scale down for display since model produces high values)
    total_goals = min((ehg or 0) + (eag or 0), 6.0)
    total_goals_str = f"{total_goals:.1f}"
    
    probs = {"主勝": hwp, "和": dp, "客勝": awp}
    fav = max(probs, key=probs.get)
    fav_prob = probs[fav]
    fav_color = color_by_prob(fav_prob)
    
    likely_score = f"{int(ehg+0.5)}-{int(eag+0.5)}"
    
    has_value = bool(bets and bets.strip())
    
    return f"""
    <div class="match-card {'has-value' if has_value else ''}">
        <div class="match-header">
            <div class="comp-badge" style="background: {comp_gradient}">{comp_cn}</div>
            <div class="match-datetime">
                <span class="date-label">{date_label}</span>
                <span class="time">{time_str}</span>
            </div>
        </div>
        
        <div class="teams-section">
            <div class="team home">
                <div class="team-name">{home_cn}</div>
                <div class="team-en">{home}</div>
            </div>
            <div class="score-center">
                <div class="predicted-score">{likely_score}</div>
                <div class="total-goals">預測 {total_goals_str} 球</div>
            </div>
            <div class="team away">
                <div class="team-name">{away_cn}</div>
                <div class="team-en">{away}</div>
            </div>
        </div>
        
        <div class="prob-grid">
            <div class="prob-item">
                <div class="prob-header">
                    <span class="prob-market">主勝</span>
                    <span class="prob-value" style="color: {color_by_prob(hwp)}">{hwp*100:.0f}%</span>
                </div>
                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{hwp*100:.0f}%; background: {color_by_prob(hwp)}"></div></div>
            </div>
            <div class="prob-item">
                <div class="prob-header">
                    <span class="prob-market">和</span>
                    <span class="prob-value" style="color: {color_by_prob(dp)}">{dp*100:.0f}%</span>
                </div>
                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{dp*100:.0f}%; background: {color_by_prob(dp)}"></div></div>
            </div>
            <div class="prob-item">
                <div class="prob-header">
                    <span class="prob-market">客勝</span>
                    <span class="prob-value" style="color: {color_by_prob(awp)}">{awp*100:.0f}%</span>
                </div>
                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{awp*100:.0f}%; background: {color_by_prob(awp)}"></div></div>
            </div>
        </div>
        
        <div class="extra-stats">
            <div class="stat-item">
                <span class="stat-label">大細 2.5</span>
                <span class="stat-value" style="color: {'#22c55e' if ov > 0.5 else '#ef4444'}">{total_goals_str}球 → 大 {ov*100:.0f}%</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">BTTS</span>
                <span class="stat-value" style="color: {'#22c55e' if bts_yes > 0.5 else '#ef4444'}">Yes {bts_yes*100:.0f}%</span>
            </div>
        </div>
        
        {'<div class="value-bets">💎 Value Bet: ' + bets + '</div>' if has_value else ''}
        
        <div class="fav-result" style="border-left: 3px solid {fav_color}">
            <span>最可能：<strong>{fav}</strong> {fav_prob*100:.0f}%</span>
        </div>
    </div>"""


def group_by_competition(rows) -> dict:
    groups = {}
    for row in rows:
        if isinstance(row, dict):
            comp = row.get('competition_code', 'OTHER')
        elif isinstance(row, (tuple, list)) and len(row) > 2:
            comp = row[2]
        else:
            comp = 'OTHER'
        if comp not in groups:
            groups[comp] = []
        groups[comp].append(row)
    return groups


def generate_html(predictions, title: str = "⚽ 足球預測報告") -> str:
    if hasattr(predictions, 'to_dict'):
        rows = predictions.to_dict(orient='records')
    elif predictions and isinstance(predictions[0], dict):
        rows = predictions
    elif predictions and isinstance(predictions[0], (tuple, list)):
        rows = predictions
    else:
        rows = list(predictions) if predictions else []
    
    groups = group_by_competition(rows)
    
    comp_sections = []
    for comp_code, comp_rows in sorted(groups.items(), key=lambda x: x[0]):
        comp_cn = get_comp_cn(comp_code)
        comp_gradient = get_comp_gradient(comp_code)
        cards = "\n".join(prediction_card(row) for row in comp_rows)
        comp_sections.append(f"""
        <div class="comp-group">
            <div class="comp-header" style="background: {comp_gradient}">
                <span class="comp-name">{comp_cn}</span>
                <span class="comp-count">{len(comp_rows)} 場</span>
            </div>
            <div class="comp-matches">{cards}</div>
        </div>
        """)
    
    comp_html = "\n".join(comp_sections)
    
    # Featured - only show if there are value bets
    def get_recommended_bets(r):
        if isinstance(r, dict):
            return r.get('recommended_bets', '')
        elif isinstance(r, (tuple, list)) and len(r) > 16:
            return r[16] or ''
        return ''
    
    featured_rows = [r for r in rows if get_recommended_bets(r) and str(get_recommended_bets(r)).strip()]
    featured_html = ""
    if featured_rows:
        featured_cards = "\n".join(prediction_card(row) for row in featured_rows)
        featured_html = f"""
        <div class="featured-section">
            <div class="featured-header">
                <span>💎 精選重心場次</span>
                <span class="count">{len(featured_rows)} 場</span>
            </div>
            <div class="featured-grid">{featured_cards}</div>
        </div>
        """
    
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: {COLORS['bg_primary']};
            color: {COLORS['text_primary']};
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{ max-width: 1000px; margin: 0 auto; }}
        
        .header {{
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 40px;
            background: {COLORS['gradient_header']};
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        }}
        
        .header h1 {{
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .header p {{
            color: rgba(255,255,255,0.85);
            font-size: 1em;
        }}
        
        .featured-section {{
            background: {COLORS['gradient_featured']};
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,107,157,0.3);
        }}
        
        .featured-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            color: {COLORS['accent_pink']};
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .featured-header .count {{
            font-size: 0.85em;
            color: {COLORS['text_secondary']};
        }}
        
        .comp-group {{ margin-bottom: 30px; }}
        
        .comp-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            border-radius: 12px;
            margin-bottom: 15px;
            color: white;
            font-weight: 600;
        }}
        
        .comp-name {{ font-size: 1.1em; }}
        .comp-count {{ font-size: 0.85em; opacity: 0.9; }}
        
        .match-card {{
            background: {COLORS['bg_card']};
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.08);
            transition: all 0.25s ease;
        }}
        
        .match-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
            background: {COLORS['bg_card_hover']};
        }}
        
        .match-card.has-value {{
            border-color: rgba(255, 230, 109, 0.4);
            background: linear-gradient(135deg, rgba(255,230,109,0.08) 0%, rgba(255,107,157,0.05) 100%);
        }}
        
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .comp-badge {{
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
            color: white;
        }}
        
        .match-datetime {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}
        
        .date-label {{
            background: rgba(255,255,255,0.15);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8em;
        }}
        
        .time {{
            color: {COLORS['text_secondary']};
            font-size: 0.9em;
        }}
        
        .teams-section {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            background: rgba(0,0,0,0.25);
            border-radius: 12px;
            margin-bottom: 15px;
        }}
        
        .team {{ flex: 1; text-align: center; }}
        
        .team-name {{
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .team-en {{
            font-size: 0.75em;
            color: {COLORS['text_muted']};
        }}
        
        .score-center {{
            text-align: center;
            padding: 0 20px;
        }}
        
        .predicted-score {{
            font-size: 2em;
            font-weight: 700;
            background: linear-gradient(135deg, #ff6b9d, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .total-goals {{
            font-size: 0.8em;
            color: {COLORS['accent_yellow']};
            margin-top: 2px;
        }}
        
        .prob-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 12px;
        }}
        
        .prob-item {{}}
        
        .prob-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }}
        
        .prob-market {{
            font-size: 0.85em;
            color: {COLORS['text_secondary']};
        }}
        
        .prob-value {{
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .prob-bar-bg {{
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .prob-bar-fill {{
            height: 100%;
            border-radius: 3px;
            transition: width 0.6s ease;
        }}
        
        .extra-stats {{
            display: flex;
            gap: 15px;
            padding: 10px 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 12px;
        }}
        
        .stat-item {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}
        
        .stat-label {{
            font-size: 0.8em;
            color: {COLORS['text_muted']};
        }}
        
        .stat-value {{
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .value-bets {{
            font-size: 0.9em;
            color: {COLORS['accent_yellow']};
            padding: 8px 12px;
            background: rgba(255,230,109,0.1);
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        
        .fav-result {{
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            background: rgba(255,255,255,0.05);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: {COLORS['text_muted']};
            font-size: 0.8em;
        }}
        
        .footer a {{ color: {COLORS['accent_blue']}; text-decoration: none; }}
        
        .no-data {{
            text-align: center;
            padding: 60px;
            color: {COLORS['text_secondary']};
        }}
        
        @media (max-width: 600px) {{
            .teams-section {{ flex-direction: column; gap: 10px; }}
            .score-center {{ order: -1; }}
            .team {{ display: flex; gap: 10px; align-items: center; }}
            .team-en {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚽ 足球預測報告</h1>
            <p>Football Predictions | Powered by Hanni 🐰</p>
        </div>
        
        {featured_html}
        
        <div class="all-matches">
            {comp_html if comp_html else '<div class="no-data">⚠️ 暫時冇可用預測數據</div>'}
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
    output = Path(__file__).resolve().parent / "web" / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"✅ Dashboard written to: {output}")
    print(f"📊 Total matches: {len(predictions)}")


if __name__ == "__main__":
    main()
