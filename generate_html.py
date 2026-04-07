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
    "home_color": "#22c55e",
    "draw_color": "#f59e0b", 
    "away_color": "#ef4444",
}

# 中文隊名映射
TEAM_NAMES_CN = {
    "Real Madrid CF": "皇家馬德里",
    "FC Bayern Munchen": "拜仁慕尼黑",
    "Arsenal FC": "阿仙奴",
    "Liverpool FC": "利物浦",
    "Paris Saint-Germain FC": "巴黎聖日耳門",
    "FC Barcelona": "巴塞隆拿",
    "Club Atletico de Madrid": "馬德里體育會",
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
    "Barca": "巴塞隆拿",
    "Atleti": "馬德里體育會",
    "Leverkusen": "利華古遜",
    "Newcastle United": "紐卡素",
    "Atalanta": "阿特蘭大",
    "Benfica": "賓菲加",
    "Tottenham Hotspur": "熱刺",
    "Manchester City FC": "曼城",
    "Manchester United FC": "曼聯",
    "Liverpool FC": "利物浦",
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


# Cache for team Chinese names from DB
_TEAM_CN_CACHE = None


def _load_team_cn_cache():
    """Load Chinese team names from database."""
    global _TEAM_CN_CACHE
    if _TEAM_CN_CACHE is None:
        _TEAM_CN_CACHE = {}
        try:
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute("SELECT name, name_cn FROM teams WHERE name_cn IS NOT NULL").fetchall()
            for name, name_cn in rows:
                _TEAM_CN_CACHE[name] = name_cn
            conn.close()
        except:
            pass
    return _TEAM_CN_CACHE


def get_team_name_cn(name: str) -> str:
    cache = _load_team_cn_cache()
    if name in cache:
        return cache[name]
    return TEAM_NAMES_CN.get(name, name)


_H2H_CACHE = None


def _get_h2h_record(home_id: int, away_id: int) -> dict:
    """由 Football-Data.co.uk historical 賽果計指定主客對賽記錄。"""
    global _H2H_CACHE
    if _H2H_CACHE is None:
        _H2H_CACHE = {}
        try:
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute('''
                SELECT home_team_id, away_team_id, home_goals, away_goals
                FROM h2h_historical
                WHERE home_team_id IS NOT NULL
                  AND away_team_id IS NOT NULL
                  AND home_goals IS NOT NULL
                  AND away_goals IS NOT NULL
            ''').fetchall()
            for home_team_id, away_team_id, home_goals, away_goals in rows:
                # UI 要用當前主隊視角，所以同一場賽果要寫入兩個方向。
                for team_id, opponent_id, goals_for, goals_against in (
                    (home_team_id, away_team_id, home_goals, away_goals),
                    (away_team_id, home_team_id, away_goals, home_goals),
                ):
                    record = _H2H_CACHE.setdefault(
                        (team_id, opponent_id),
                        {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'gf': 0, 'ga': 0},
                    )
                    record['played'] += 1
                    record['gf'] += goals_for
                    record['ga'] += goals_against
                    if goals_for > goals_against:
                        record['wins'] += 1
                    elif goals_for == goals_against:
                        record['draws'] += 1
                    else:
                        record['losses'] += 1
            conn.close()
        except:
            pass
    return _H2H_CACHE.get((home_id, away_id), None)


def get_comp_cn(code: str) -> str:
    return COMP_NAMES_CN.get(code, f"⚽ {code}")


def get_comp_gradient(code: str) -> str:
    return COMP_GRADIENTS.get(code, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")


def get_predictions(days_ahead: int = 7) -> list:
    """Fetch predictions directly from database as tuples."""
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
        JOIN predictions p ON p.match_id = m.match_id
        AND p.prediction_id = (
            SELECT MAX(p2.prediction_id) 
            FROM predictions p2 
            WHERE p2.match_id = m.match_id
        )
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
        
        full_date = hkt.strftime("%Y/%m/%d %H:%M")
        return time_str, label, full_date
    except:
        return utc_date[:16] if utc_date else "TBD", "", utc_date[:16] if utc_date else "TBD"


def prediction_card_from_dict(row: dict) -> str:
    """Build card from dict (DataFrame row)."""
    utc_date = row.get('utc_date') or row.get('kickoff_hk', '')
    match_id = row.get('match_id')
    comp = row.get('competition_code')
    home = row.get('home_team_name')
    away = row.get('away_team_name')
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
    bets = row.get('recommended_bets') or ""
    
    return _build_card(utc_date, comp, home, away, hwp, dp, awp, ov, un, bts_yes, bts_no, ehg, eag, bets)


def prediction_card_from_tuple(row: tuple) -> str:
    """Build card from tuple (DB row)."""
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
    bets = bets or ""
    home_id = home_id or 0
    away_id = away_id or 0
    
    return _build_card(utc_date, comp, home, away, hwp, dp, awp, ov, un, bts_yes, bts_no, ehg, eag, bets, home_id, away_id)


def _build_card(utc_date: str, comp: str, home: str, away: str, hwp: float, dp: float, awp: float, 
                 ov: float, un: float, bts_yes: float, bts_no: float, ehg: float, eag: float, bets: str,
                 home_id: int = 0, away_id: int = 0) -> str:
    """Common card building logic."""
    home_cn = get_team_name_cn(home)
    away_cn = get_team_name_cn(away)
    comp_cn = get_comp_cn(comp)
    comp_gradient = get_comp_gradient(comp)
    
    time_str, date_label, full_date = format_match_time(utc_date)
    
    total_goals = min((ehg or 0) + (eag or 0), 6.0)
    total_goals_str = f"{total_goals:.1f}"
    
    probs = {"主勝": hwp, "和": dp, "客勝": awp}
    fav = max(probs, key=probs.get)
    fav_prob = probs[fav]
    
    max_prob = max(hwp, dp, awp)
    is_confident = max_prob > 0.50
    conf_level = "高信心" if max_prob > 0.55 else "中信心" if max_prob > 0.45 else "一般"
    conf_color = "#22c55e" if max_prob > 0.55 else "#f59e0b" if max_prob > 0.45 else "#6b6b80"
    
    if hwp >= dp and hwp >= awp:
        primary_color = COLORS["home_color"]
    elif awp >= dp:
        primary_color = COLORS["away_color"]
    else:
        primary_color = COLORS["draw_color"]
    
    # H2H section
    h2h_section = ""
    if home_id and away_id:
        h2h = _get_h2h_record(home_id, away_id)
        if h2h and h2h.get('played', 0) > 0:
            w, d, l = h2h['wins'], h2h['draws'], h2h['losses']
            gf, ga = h2h['gf'], h2h['ga']
            h2h_section = f"""
        <div class="h2h-container">
            <div class="h2h-header">📊 對賽記錄</div>
            <div class="h2h-stats">
                <span class="h2h-wins">勝 {w}</span>
                <span class="h2h-draws">和 {d}</span>
                <span class="h2h-losses">負 {l}</span>
                <span class="h2h-goals">{gf}-{ga}</span>
            </div>
            <div class="h2h-matches">{h2h['played']} 場</div>
        </div>"""
    
    return f"""
    <div class="match-card">
        <div class="match-header">
            <div class="comp-badge" style="background: {comp_gradient}">{comp_cn}</div>
            <div class="match-datetime">
                <span class="date-label">{date_label} {time_str}</span>
            </div>
        </div>
        
        <div class="teams-section">
            <div class="team home">
                <div class="team-name">{home_cn}</div>
                <div class="team-en">{home}</div>
            </div>
            <div class="score-center">
                <div class="predicted-score">{int(ehg+0.5)}-{int(eag+0.5)}</div>
                <div class="total-goals">預測 {total_goals_str} 球</div>
            </div>
            <div class="team away">
                <div class="team-name">{away_cn}</div>
                <div class="team-en">{away}</div>
            </div>
        </div>
        
        <!-- Stacked Bar for Win/Draw/Win probabilities -->
        <div class="stacked-bar-section">
            <div class="stacked-bar">
                <div class="bar-segment bar-home" style="width:{hwp*100/max(hwp+dp+awp, 0.001):.0f}%"></div>
                <div class="bar-segment bar-draw" style="width:{dp*100/max(hwp+dp+awp, 0.001):.0f}%"></div>
                <div class="bar-segment bar-away" style="width:{awp*100/max(hwp+dp+awp, 0.001):.0f}%"></div>
            </div>
            <div class="stacked-bar-labels">
                <span class="label-home">主勝 {hwp*100:.0f}%</span>
                <span class="label-draw">和 {dp*100:.0f}%</span>
                <span class="label-away">客勝 {awp*100:.0f}%</span>
            </div>
        </div>
        
        <!-- Stats container -->
        <div class="stats-container">
            <div class="stat-row">
                <span class="stat-label">大細 2.5</span>
                <div class="stat-bars">
                    <div class="mini-bar"><div class="mini-fill green" style="width:{ov*100:.0f}%"></div></div>
                    <span class="stat-val">大 {ov*100:.0f}%</span>
                </div>
            </div>
            <div class="stat-row">
                <span class="stat-label">BTTS</span>
                <div class="stat-bars">
                    <div class="mini-bar"><div class="mini-fill pink" style="width:{bts_yes*100:.0f}%"></div></div>
                    <span class="stat-val">Yes {bts_yes*100:.0f}%</span>
                </div>
            </div>
        </div>
        
        {h2h_section}
        
        {'<div class="value-bets">⭐ 模型高信心揀選</div>' if is_confident else ''}
        
        <div class="fav-result">
            <div class="fav-main" style="border-left: 4px solid {primary_color}">
                <span>最可能：<strong>{fav}</strong> {fav_prob*100:.0f}%</span>
            </div>
            <span class="conf-badge" style="background:{conf_color}20; color:{conf_color}">{conf_level}</span>
        </div>
    </div>"""


def group_by_competition(rows) -> dict:
    groups = {}
    for row in rows:
        if isinstance(row, dict):
            comp = row.get('competition_code', 'OTHER')
        else:
            comp = row[2] if len(row) > 2 else 'OTHER'
        if comp not in groups:
            groups[comp] = []
        groups[comp].append(row)
    return groups


def prediction_card(row) -> str:
    """Generic prediction card builder."""
    if isinstance(row, dict):
        return prediction_card_from_dict(row)
    else:
        return prediction_card_from_tuple(row)


def generate_html(predictions, title: str = "⚽ 足球預測報告") -> str:
    # Handle both DataFrame and tuple list
    if hasattr(predictions, 'to_dict'):
        rows = predictions.to_dict(orient='records')
    else:
        rows = predictions
    
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
    
    # Featured - model confidence based picks (>50% probability)
    def get_max_prob(r):
        if isinstance(r, dict):
            return max(r.get('home_win_prob') or 0, r.get('draw_prob') or 0, r.get('away_win_prob') or 0)
        return max(r[7] or 0, r[8] or 0, r[9] or 0)
    
    featured_rows = [r for r in rows if get_max_prob(r) > 0.50]
    featured_html = ""
    if featured_rows:
        featured_cards = "\n".join(prediction_card(row) for row in featured_rows)
        featured_html = f"""
        <div class="featured-section">
            <div class="featured-header">
                <span>⭐ 精選信心場次</span>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            background: linear-gradient(135deg, rgba(255,107,157,0.15) 0%, rgba(78,205,196,0.1) 100%);
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
            flex-direction: column;
            align-items: flex-end;
            gap: 2px;
        }}
        
        .date-label {{
            background: rgba(255,255,255,0.15);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 600;
            color: white;
        }}
        
        .date-full {{
            font-size: 0.75em;
            color: {COLORS['text_secondary']};
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
        
        /* Stacked Bar Section */
        .stacked-bar-section {{
            margin-bottom: 15px;
        }}
        
        .stacked-bar {{
            display: flex;
            height: 32px;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 8px;
            background: rgba(255,255,255,0.06);
        }}
        
        .bar-segment {{
            height: 100%;
            transition: width 0.6s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 0;
        }}
        
        .bar-home {{
            background: #3a3a4a;
            border-radius: 16px 0 0 16px;
        }}
        
        .bar-draw {{
            background: #4a4a5a;
        }}
        
        .bar-away {{
            background: linear-gradient(135deg, #38BDF8 0%, #7dd3fc 100%);
            border-radius: 0 16px 16px 0;
        }}
        
        .stacked-bar-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
            font-weight: 700;
        }}
        
        .label-home {{ color: #6b6b80; }}
        .label-draw {{ color: #8b8b9b; }}
        .label-away {{ color: #7dd3fc; font-weight: 700; }}
        
        /* Stats Container */
        .stats-container {{
            background: rgba(0,0,0,0.25);
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }}
        
        /* H2H Container */
        .h2h-container {{
            background: rgba(56,189,248,0.08);
            border: 1px solid rgba(56,189,248,0.2);
            border-radius: 10px;
            padding: 12px 14px;
            margin-bottom: 12px;
        }}
        
        .h2h-header {{
            font-size: 0.8em;
            color: #7dd3fc;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .h2h-stats {{
            display: flex;
            gap: 12px;
            margin-bottom: 4px;
        }}
        
        .h2h-stats span {{
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .h2h-wins {{ color: #22c55e; }}
        .h2h-draws {{ color: #f59e0b; }}
        .h2h-losses {{ color: #ef4444; }}
        .h2h-goals {{ color: #7dd3fc; }}
        
        .h2h-matches {{
            font-size: 0.75em;
            color: #6b6b80;
        }}
        
        .stat-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }}
        
        .stat-row:last-child {{ margin-bottom: 0; }}
        
        .stat-label {{
            width: 60px;
            font-size: 0.85em;
            color: {COLORS['text_secondary']};
        }}
        
        .stat-bars {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .mini-bar {{
            width: 80px;
            height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
        }}
        
        .mini-fill {{
            height: 100%;
            border-radius: 3px;
        }}
        
        .mini-fill.green {{
            background: linear-gradient(90deg, #22c55e, #4ade80);
        }}
        
        .mini-fill.pink {{
            background: linear-gradient(90deg, #ff6b9d, #ff8fab);
        }}
        
        .stat-val {{
            font-size: 0.85em;
            font-weight: 600;
            color: {COLORS['text_primary']};
            min-width: 70px;
        }}
        
        .value-bets {{
            font-size: 0.9em;
            color: {COLORS['accent_yellow']};
            padding: 8px 12px;
            background: rgba(255,230,109,0.1);
            border-radius: 8px;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        
        .fav-result {{
            padding: 12px 14px;
            border-radius: 10px;
            font-size: 1em;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(125, 211, 252, 0.08) 100%);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}
        
        .fav-main {{
            padding-left: 12px;
            font-weight: 700;
        }}
        
        .fav-main span {{ 
            color: {COLORS['text_secondary']};
            font-size: 0.95em;
        }}
        
        .fav-main strong {{ 
            color: #38BDF8; 
            font-weight: 800;
            font-size: 1.2em;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
        }}
        
        .conf-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
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
            .stacked-bar-labels {{ flex-wrap: wrap; gap: 5px; }}
            .stacked-bar-labels span {{ font-size: 0.8em; }}
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
