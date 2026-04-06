#!/usr/bin/env python3
"""Generate HTML dashboard for football predictions - Enhanced Version."""

from __future__ import annotations
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

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
    "Viktoria Plzeň": "比爾森勝利",
    "Red Bull Salzburg": "薩爾斯堡紅牛",
    "GNK Dinamo Zagreb": "薩格勒布戴拿模",
    "Lille OSC": "里昂",
    "Stuttgart": "史特加",
    "Girona": "切爾達",
    "Villarreal": "維拉利爾",
    "Real Sociedad": "皇家蘇斯達",
    "Athletic Bilbao": "畢爾包",
    "Getafe": "基達菲",
    "Osasuna": "奧沙蘇拿",
    "Valencia": "華倫西亞",
    "Real Betis": "貝迪斯",
    "Sevilla": "西維爾",
    "Udinese": "烏甸尼斯",
    "Como 1907": "科木",
    "Lecce": "萊切",
    "Napoli": "拿玻里",
    "Genoa": "熱拿亞",
    "Frosinone": "費辛隆",
    "Cagliari": "卡利亞里",
    "Sassuolo": "莎索羅",
    "Torino": "拖連奴",
    "Empoli": "恩波利",
    "Monaco": "摩納哥",
    "Marseille": "馬賽",
    "Rennes": "雷恩",
    "Nice": "尼斯",
    "Lens": "朗斯",
    "Lyon": "里昂",
    "Brest": "布雷斯斯特",
    "Leipzig": "萊比錫",
    "Eintracht Frankfurt": "法蘭克福",
    "Wolfsburg": "沃爾夫斯堡",
    "Mönchengladbach": "慕遜加柏",
    "Freiburg": "弗賴堡",
    "Hoffenheim": "賀芬咸",
    "Bayer Leverkusen": "利華古遜",
    "West Ham United": "韋斯咸",
    "Aston Villa": "阿士東維拉",
    "Brighton Hove Albion": "白禮頓",
    "Wolverhampton Wanderers": "狼隊",
    "Crystal Palace": "水晶宮",
    "Fulham": "富咸",
    "Brentford": "賓福特",
    "Bournemouth": "般尼茅夫",
    "Everton": "愛華頓",
    "Nottingham Forest": "諾定咸森林",
    "Burnley": "般尼",
    "Luton Town": "洛達咸",
    "Sheffield United": "錫菲聯",
    "Leicester City": "李斯特城",
    "West Brom": "西布朗",
    "Norwich City": "諾域治",
    "Swansea City": "史雲斯",
    "Middlesbrough": "米杜域",
    "Coventry City": "高雲地利",
    "Sunderland": "新特蘭",
    "Hull City": "侯城",
    "Stoke City": "史篤城",
    "Derby County": "打比郡",
    "Reading": "雷丁",
    "Birmingham City": "伯明翰",
    "Blackburn Rovers": "布力般流浪",
    "AFC Bournemouth": "般尼茅夫",
    "Norwich": "諾域治",
    "Swansea": "史雲斯",
    "Bristol City": "布里斯托城",
    "Huddersfield Town": "哈特斯菲爾德",
    "Preston North End": "普雷斯頓",
    "Stoke": "史篤城",
    "Derby": "打比郡",
    "Birmingham": "伯明翰",
    "Blackburn": "布力般流浪",
    "Cardiff City": "卡迪夫城",
    "Derby County": "打比郡",
    "Sheffield Wednesday": "錫周三",
    "Middlesbrough": "米杜域",
    "Coventry": "高雲地利",
    "Luton": "洛達咸",
    "Burnley": "般尼",
    "Sunderland": "新特蘭",
    "Portsmouth": "樸茨茅夫",
    "Peterborough United": "彼德堡",
    "Bristol Rovers": "布里斯托流浪",
    "Ipswich Town": "葉士域治",
    "Oxford United": "牛津聯",
    "Cambridge United": "劍橋聯",
    "Moreirense": "摩里維斯",
    "Famalicao": "法馬利卡奧",
    "Casa Pia": "卡斯皮亞",
    "Gil Vicente": "基維辛迪",
    "Arouca": "阿魯卡",
    "Porto": "波圖",
    "Braga": "布拉加",
    "Vizela": "維塞拉",
    "Estrela Amadora": "埃斯特雷拉",
    "Santa Clara": "辛達卡拉",
    "Boavista": "博阿維斯塔",
    "Rio Ave": "里奧艾維",
    "Farense": "法倫斯",
    "Maritimo": "馬爾莫",
    "Tondela": "通德拉",
    "Paços de Ferreira": "帕科斯",
    "B SAD": "B SAD",
    "Nasional": "拿薩爾",
    "Arsenal": "阿仙奴",
    "Liverpool": "利物浦",
    "Man City": "曼城",
    "Man United": "曼聯",
    "Tottenham": "熱刺",
    "Chelsea": "車路士",
    "Newcastle": "紐卡素",
    "Brighton": "白禮頓",
    "Wolves": "狼隊",
}

# 聯賽中文名
COMP_NAMES_CN = {
    "CL": "🏆 歐聯",
    "EL": "🌍 歐霸",
    "EC": "🏆 歐洲超級杯",
    "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英超",
    "PD": "🇪🇸 西甲",
    "SA": "🇮🇹 意甲",
    "BL1": "🇩🇪 德甲",
    "FL1": "🇫🇷 法甲",
    "PO": "🇵🇹 葡超",
    "NL": "🇳🇱 荷甲",
    "BEC": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英冠",
    "LAL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英甲",
}

# 聯賽 emoji 背景色
COMP_COLORS = {
    "CL": "#1a237e",
    "EL": "#0d47a1",
    "PL": "#b71c1c",
    "PD": "#e65100",
    "SA": "#1b5e20",
    "BL1": "#f57f17",
    "FL1": "#0d47a1",
    "PO": "#c62828",
    "NL": "#ff6f00",
    "BEC": "#4a148c",
    "LAL": "#880e4f",
}


def get_team_name_cn(name: str) -> str:
    """取得中文隊名，否則返回原文"""
    return TEAM_NAMES_CN.get(name, name)


def get_comp_cn(code: str) -> str:
    """取得聯賽中文名"""
    return COMP_NAMES_CN.get(code, f"⚽ {code}")


def color_bar(prob: float) -> str:
    if prob >= 0.5:
        return f"rgba(74, 222, 128, {prob:.2f})"
    elif prob >= 0.35:
        return f"rgba(251, 191, 36, {prob:.2f})"
    else:
        return f"rgba(248, 113, 113, {prob:.2f})"


def get_predictions(days_ahead: int = 7, featured_only: bool = False) -> list[dict]:
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


def format_match_time(utc_date: str) -> tuple[str, str, str]:
    """Format datetime and return time label"""
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


def prediction_card(row, show_comp: bool = True) -> str:
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
    else:
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
    comp_color = COMP_COLORS.get(comp, "#1a1a2e")
    
    time_str, date_label, full_time = format_match_time(utc_date)
    
    probs = {"主勝": hwp, "和": dp, "客勝": awp}
    fav = max(probs, key=probs.get)
    fav_prob = probs[fav]
    fav_color = "#4ade80" if fav_prob > 0.45 else "#fbbf24" if fav_prob > 0.35 else "#f87171"
    
    likely_score = f"{int(ehg+0.5)}-{int(eag+0.5)}"
    
    comp_badge = f'<span class="comp-badge" style="background:{comp_color}">{comp_cn}</span>' if show_comp else ""
    date_badge = f'<span class="date-badge">{date_label} {time_str}</span>' if date_label else ""
    
    has_value = bool(bets and bets.strip())
    
    return f"""
    <div class="match-card {'has-value' if has_value else ''}">
        <div class="match-header">
            {comp_badge}
            {date_badge}
        </div>
        <div class="teams">
            <div class="team">
                <div class="team-name">{home_cn}</div>
                <div class="team-name-en">{home}</div>
            </div>
            <div class="score-preview">
                <div class="score">{likely_score}</div>
                <div class="vs-label">預測</div>
            </div>
            <div class="team">
                <div class="team-name">{away_cn}</div>
                <div class="team-name-en">{away}</div>
            </div>
        </div>
        
        <div class="prob-section">
            <div class="prob-row">
                <span class="prob-label">主勝</span>
                <div class="prob-bar"><div class="prob-fill" style="width:{hwp*100:.0f}%; background:{color_bar(hwp)}"></div></div>
                <span class="prob-val">{hwp*100:.0f}%</span>
            </div>
            <div class="prob-row">
                <span class="prob-label">和</span>
                <div class="prob-bar"><div class="prob-fill" style="width:{dp*100:.0f}%; background:{color_bar(dp)}"></div></div>
                <span class="prob-val">{dp*100:.0f}%</span>
            </div>
            <div class="prob-row">
                <span class="prob-label">客勝</span>
                <div class="prob-bar"><div class="prob-fill" style="width:{awp*100:.0f}%; background:{color_bar(awp)}"></div></div>
                <span class="prob-val">{awp*100:.0f}%</span>
            </div>
        </div>
        
        <div class="extra-section">
            <div class="extra-item">
                <span class="extra-label">大細</span>
                <span class="extra-val {'green' if ov > 0.5 else 'red'}">大 {ov*100:.0f}%</span>
                <span class="extra-val {'green' if un > 0.5 else 'red'}">細 {un*100:.0f}%</span>
            </div>
            <div class="extra-item">
                <span class="extra-label">BTTS</span>
                <span class="extra-val {'green' if bts_yes > 0.5 else 'red'}">Yes {bts_yes*100:.0f}%</span>
                <span class="extra-val {'green' if bts_no > 0.5 else 'red'}">No {bts_no*100:.0f}%</span>
            </div>
        </div>
        
        {'<div class="value-bets">💎 Value Bet: ' + bets + '</div>' if has_value else ''}
        
        <div class="fav-mark" style="border-left-color:{fav_color}">
            <span>最可能：<strong>{fav}</strong> ({fav_prob*100:.0f}%)</span>
        </div>
    </div>"""


def group_by_competition(rows: list[dict]) -> dict[str, list[dict]]:
    """按聯賽分組"""
    groups = {}
    for row in rows:
        if isinstance(row, dict):
            comp = row.get('competition_code', 'OTHER')
        else:
            comp = row[2]  # tuple format
        if comp not in groups:
            groups[comp] = []
        groups[comp].append(row)
    return groups


def generate_html(predictions, title: str = "⚽ 足球預測報告") -> str:
    if hasattr(predictions, 'to_dict'):
        rows = predictions.to_dict(orient='records')
    else:
        rows = predictions
    
    # 分組
    groups = group_by_competition(rows)
    
    # 構建每個聯賽的 HTML
    comp_sections = []
    for comp_code, comp_rows in sorted(groups.items()):
        comp_cn = get_comp_cn(comp_code)
        comp_color = COMP_COLORS.get(comp_code, "#1a1a2e")
        cards = "\n".join(prediction_card(row) for row in comp_rows)
        comp_sections.append(f"""
        <div class="comp-group">
            <div class="comp-header" style="border-left-color:{comp_color}">
                <span class="comp-title">{comp_cn}</span>
                <span class="comp-count">{len(comp_rows)} 場賽事</span>
            </div>
            <div class="comp-matches">{cards}</div>
        </div>
        """)
    
    comp_html = "\n".join(comp_sections)
    
    # Featured section - value bets
    featured_rows = [r for r in rows if (r.get('recommended_bets') if isinstance(r, dict) else r[-1]) and str(r.get('recommended_bets') if isinstance(r, dict) else r[-1]).strip()]
    featured_html = ""
    if featured_rows:
        featured_cards = "\n".join(prediction_card(row) for row in featured_rows)
        featured_html = f"""
        <div class="featured-section">
            <div class="featured-header">
                <span class="featured-title">💎 精選重心場次</span>
                <span class="featured-count">{len(featured_rows)} 場</span>
            </div>
            <div class="featured-matches">{featured_cards}</div>
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
        
        .featured-section {{
            background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(233,69,96,0.1));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(251,191,36,0.3);
        }}
        
        .featured-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(251,191,36,0.2);
        }}
        
        .featured-title {{
            font-size: 1.2em;
            font-weight: 700;
            color: {COLORS['warning']};
        }}
        
        .featured-count {{
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .comp-group {{
            margin-bottom: 30px;
        }}
        
        .comp-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            margin-bottom: 15px;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            border-left: 4px solid;
        }}
        
        .comp-title {{
            font-size: 1.1em;
            font-weight: 600;
        }}
        
        .comp-count {{
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .match-card {{
            background: rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .match-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(233, 69, 96, 0.15);
        }}
        
        .match-card.has-value {{
            border-color: rgba(251, 191, 36, 0.3);
            background: rgba(251, 191, 36, 0.05);
        }}
        
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .comp-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8em;
            color: white;
        }}
        
        .date-badge {{
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .teams {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding: 12px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }}
        
        .team {{
            flex: 1;
            text-align: center;
        }}
        
        .team-name {{
            font-size: 1.05em;
            font-weight: 600;
            margin-bottom: 3px;
        }}
        
        .team-name-en {{
            font-size: 0.75em;
            color: {COLORS['muted']};
        }}
        
        .score-preview {{
            text-align: center;
            padding: 0 15px;
        }}
        
        .score {{
            font-size: 1.4em;
            font-weight: 700;
            color: {COLORS['accent']};
        }}
        
        .vs-label {{
            font-size: 0.7em;
            color: {COLORS['muted']};
        }}
        
        .prob-section {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 12px;
        }}
        
        .prob-row {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .prob-label {{
            width: 45px;
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .prob-bar {{
            flex: 1;
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .prob-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        
        .prob-val {{
            width: 40px;
            text-align: right;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .extra-section {{
            display: flex;
            gap: 20px;
            padding: 10px;
            background: rgba(0,0,0,0.15);
            border-radius: 8px;
            margin-bottom: 12px;
        }}
        
        .extra-item {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .extra-label {{
            font-size: 0.85em;
            color: {COLORS['muted']};
        }}
        
        .extra-val {{
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .extra-val.green {{ color: {COLORS['success']}; }}
        .extra-val.red {{ color: {COLORS['danger']}; }}
        
        .value-bets {{
            font-size: 0.9em;
            color: {COLORS['warning']};
            margin-bottom: 10px;
            padding: 8px 12px;
            background: rgba(251,191,36,0.12);
            border-radius: 8px;
        }}
        
        .fav-mark {{
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            border-left: 3px solid;
            background: rgba(255,255,255,0.05);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: {COLORS['muted']};
            font-size: 0.8em;
        }}
        
        .footer a {{
            color: {COLORS['accent']};
            text-decoration: none;
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
            <p>Football Predictions | Poisson Model | Powered by Hanni 🐰</p>
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
