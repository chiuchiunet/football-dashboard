#!/usr/bin/env python3
"""
World Cup 2026 Dashboard Generator
Repurpose the football workspace for the World Cup
"""

from pathlib import Path
from datetime import datetime

# =============================================================================
# WORLD CUP 2026 DATA
# =============================================================================

GROUPS = {
    "A": [
        {"team": "🇲🇽 Mexico", "seed": "Host"},
        {"team": "🇿🇦 South Africa", "seed": ""},
        {"team": "🇰🇷 South Korea", "seed": ""},
        {"team": "🇨🇿 Czechia", "seed": "UEFA Playoff D"},
    ],
    "B": [
        {"team": "🇨🇦 Canada", "seed": "Host"},
        {"team": "🇧🇦 Bosnia & Herzegovina", "seed": "UEFA Playoff A"},
        {"team": "🇶🇦 Qatar", "seed": ""},
        {"team": "🇨🇭 Switzerland", "seed": ""},
    ],
    "C": [
        {"team": "🇧🇷 Brazil", "seed": ""},
        {"team": "🇲🇦 Morocco", "seed": ""},
        {"team": "🇭🇹 Haiti", "seed": ""},
        {"team": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland", "seed": ""},
    ],
    "D": [
        {"team": "🇺🇸 USA", "seed": "Host"},
        {"team": "🇵🇾 Paraguay", "seed": ""},
        {"team": "🇦🇺 Australia", "seed": ""},
        {"team": "🇹🇷 Türkiye", "seed": "UEFA Playoff C"},
    ],
    "E": [
        {"team": "🇩🇪 Germany", "seed": ""},
        {"team": "🇨🇼 Curaçao", "seed": ""},
        {"team": "🇨🇮 Ivory Coast", "seed": ""},
        {"team": "🇪🇨 Ecuador", "seed": ""},
    ],
    "F": [
        {"team": "🇳🇱 Netherlands", "seed": ""},
        {"team": "🇯🇵 Japan", "seed": ""},
        {"team": "🇺🇦 Ukraine", "seed": "UEFA Playoff B"},
        {"team": "🇹🇳 Tunisia", "seed": ""},
    ],
    "G": [
        {"team": "🇧🇪 Belgium", "seed": ""},
        {"team": "🇪🇬 Egypt", "seed": ""},
        {"team": "🇮🇷 Iran", "seed": ""},
        {"team": "🇳🇿 New Zealand", "seed": ""},
    ],
    "H": [
        {"team": "🇪🇸 Spain", "seed": ""},
        {"team": "🇨🇻 Cape Verde", "seed": ""},
        {"team": "🇸🇦 Saudi Arabia", "seed": ""},
        {"team": "🇺🇾 Uruguay", "seed": ""},
    ],
    "I": [
        {"team": "🇫🇷 France", "seed": "Defending Champion"},
        {"team": "🇸🇳 Senegal", "seed": ""},
        {"team": "🇧🇴 Bolivia", "seed": "Intercontinental Playoff 2"},
        {"team": "🇳🇴 Norway", "seed": ""},
    ],
    "J": [
        {"team": "🇦🇷 Argentina", "seed": "Defending Champion"},
        {"team": "🇩🇿 Algeria", "seed": ""},
        {"team": "🇦🇹 Austria", "seed": ""},
        {"team": "🇯🇴 Jordan", "seed": ""},
    ],
    "K": [
        {"team": "🇵🇹 Portugal", "seed": ""},
        {"team": "🇨🇩 DR Congo", "seed": "Intercontinental Playoff 1"},
        {"team": "🇺🇿 Uzbekistan", "seed": ""},
        {"team": "🇨🇴 Colombia", "seed": ""},
    ],
    "L": [
        {"team": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "seed": ""},
        {"team": "🇭🇷 Croatia", "seed": ""},
        {"team": "🇬🇭 Ghana", "seed": ""},
        {"team": "🇵🇦 Panama", "seed": ""},
    ],
}

MATCHES = [
    {"date": "2026-06-11", "time_et": "15:00", "group": "A", "home": "Mexico", "away": "South Africa", "venue": "Estadio Azteca, Mexico City", "hk": "03:00+1"},
    {"date": "2026-06-11", "time_et": "22:00", "group": "A", "home": "South Korea", "away": "Czechia", "venue": "Estadio Akron, Zapopan", "hk": "10:00+1"},
    {"date": "2026-06-12", "time_et": "15:00", "group": "B", "home": "Canada", "away": "Bosnia & Herzegovina", "venue": "BMO Field, Toronto", "hk": "03:00+1"},
    {"date": "2026-06-12", "time_et": "21:00", "group": "D", "home": "USA", "away": "Paraguay", "venue": "SoFi Stadium, Inglewood", "hk": "09:00+1"},
    {"date": "2026-06-13", "time_et": "15:00", "group": "B", "home": "Qatar", "away": "Switzerland", "venue": "Levi's Stadium, Santa Clara", "hk": "03:00+1"},
    {"date": "2026-06-13", "time_et": "18:00", "group": "C", "home": "Brazil", "away": "Morocco", "venue": "MetLife Stadium, East Rutherford", "hk": "06:00+1"},
    {"date": "2026-06-13", "time_et": "21:00", "group": "C", "home": "Haiti", "away": "Scotland", "venue": "Gillette Stadium, Foxborough", "hk": "09:00+1"},
    {"date": "2026-06-14", "time_et": "00:00", "group": "D", "home": "Australia", "away": "Türkiye", "venue": "BC Place, Vancouver", "hk": "12:00"},
    {"date": "2026-06-14", "time_et": "13:00", "group": "E", "home": "Germany", "away": "Curaçao", "venue": "NRG Stadium, Houston", "hk": "01:00+1"},
    {"date": "2026-06-14", "time_et": "16:00", "group": "F", "home": "Netherlands", "away": "Japan", "venue": "AT&T Stadium, Arlington", "hk": "04:00+1"},
    {"date": "2026-06-14", "time_et": "19:00", "group": "E", "home": "Ivory Coast", "away": "Ecuador", "venue": "Lincoln Financial Field, Philadelphia", "hk": "07:00+1"},
    {"date": "2026-06-14", "time_et": "22:00", "group": "F", "home": "Sweden", "away": "Tunisia", "venue": "Estadio BBVA, Monterrey", "hk": "10:00+1"},
    {"date": "2026-06-15", "time_et": "12:00", "group": "H", "home": "Spain", "away": "Cape Verde", "venue": "Mercedes-Benz Stadium, Atlanta", "hk": "00:00+1"},
    {"date": "2026-06-15", "time_et": "15:00", "group": "G", "home": "Belgium", "away": "Egypt", "venue": "Lumen Field, Seattle", "hk": "03:00+1"},
    {"date": "2026-06-15", "time_et": "18:00", "group": "H", "home": "Saudi Arabia", "away": "Uruguay", "venue": "Hard Rock Stadium, Miami Gardens", "hk": "06:00+1"},
    {"date": "2026-06-15", "time_et": "21:00", "group": "G", "home": "Iran", "away": "New Zealand", "venue": "SoFi Stadium, Inglewood", "hk": "09:00+1"},
    {"date": "2026-06-16", "time_et": "15:00", "group": "I", "home": "France", "away": "Senegal", "venue": "MetLife Stadium, East Rutherford", "hk": "03:00+1"},
    {"date": "2026-06-16", "time_et": "18:00", "group": "I", "home": "Bolivia", "away": "Norway", "venue": "Gillette Stadium, Foxborough", "hk": "06:00+1"},
    {"date": "2026-06-16", "time_et": "21:00", "group": "J", "home": "Argentina", "away": "Algeria", "venue": "Arrowhead Stadium, Kansas City", "hk": "09:00+1"},
    {"date": "2026-06-17", "time_et": "00:00", "group": "J", "home": "Austria", "away": "Jordan", "venue": "Levi's Stadium, Santa Clara", "hk": "12:00"},
    {"date": "2026-06-17", "time_et": "13:00", "group": "K", "home": "Portugal", "away": "DR Congo", "venue": "NRG Stadium, Houston", "hk": "01:00+1"},
    {"date": "2026-06-17", "time_et": "16:00", "group": "L", "home": "England", "away": "Croatia", "venue": "AT&T Stadium, Arlington", "hk": "04:00+1"},
    {"date": "2026-06-17", "time_et": "19:00", "group": "L", "home": "Ghana", "away": "Panama", "venue": "BMO Field, Toronto", "hk": "07:00+1"},
    {"date": "2026-06-17", "time_et": "22:00", "group": "K", "home": "Uzbekistan", "away": "Colombia", "venue": "Estadio Azteca, Mexico City", "hk": "10:00+1"},
    {"date": "2026-06-18", "time_et": "12:00", "group": "A", "home": "Czechia", "away": "South Africa", "venue": "Mercedes-Benz Stadium, Atlanta", "hk": "00:00+1"},
    {"date": "2026-06-18", "time_et": "15:00", "group": "B", "home": "Switzerland", "away": "Bosnia & Herzegovina", "venue": "SoFi Stadium, Inglewood", "hk": "03:00+1"},
    {"date": "2026-06-18", "time_et": "18:00", "group": "B", "home": "Canada", "away": "Qatar", "venue": "BC Place, Vancouver", "hk": "06:00+1"},
    {"date": "2026-06-18", "time_et": "21:00", "group": "A", "home": "Mexico", "away": "South Korea", "venue": "Estadio Akron, Zapopan", "hk": "09:00+1"},
    {"date": "2026-06-19", "time_et": "15:00", "group": "D", "home": "USA", "away": "Australia", "venue": "Lumen Field, Seattle", "hk": "03:00+1"},
    {"date": "2026-06-19", "time_et": "18:00", "group": "C", "home": "Scotland", "away": "Morocco", "venue": "Gillette Stadium, Foxborough", "hk": "06:00+1"},
    {"date": "2026-06-19", "time_et": "20:30", "group": "C", "home": "Brazil", "away": "Haiti", "venue": "Lincoln Financial Field, Philadelphia", "hk": "08:30+1"},
    {"date": "2026-06-19", "time_et": "23:00", "group": "D", "home": "Türkiye", "away": "Paraguay", "venue": "Levi's Stadium, Santa Clara", "hk": "11:00+1"},
    {"date": "2026-06-20", "time_et": "13:00", "group": "F", "home": "Netherlands", "away": "Sweden", "venue": "NRG Stadium, Houston", "hk": "01:00+1"},
    {"date": "2026-06-20", "time_et": "16:00", "group": "E", "home": "Germany", "away": "Ivory Coast", "venue": "BMO Field, Toronto", "hk": "04:00+1"},
    {"date": "2026-06-20", "time_et": "20:00", "group": "E", "home": "Ecuador", "away": "Curaçao", "venue": "Arrowhead Stadium, Kansas City", "hk": "08:00+1"},
    {"date": "2026-06-21", "time_et": "00:00", "group": "F", "home": "Tunisia", "away": "Japan", "venue": "Estadio BBVA, Monterrey", "hk": "12:00"},
    {"date": "2026-06-21", "time_et": "12:00", "group": "H", "home": "Spain", "away": "Saudi Arabia", "venue": "Mercedes-Benz Stadium, Atlanta", "hk": "00:00+1"},
    {"date": "2026-06-21", "time_et": "15:00", "group": "G", "home": "Belgium", "away": "Iran", "venue": "SoFi Stadium, Inglewood", "hk": "03:00+1"},
    {"date": "2026-06-21", "time_et": "18:00", "group": "H", "home": "Uruguay", "away": "Cape Verde", "venue": "Hard Rock Stadium, Miami Gardens", "hk": "06:00+1"},
    {"date": "2026-06-21", "time_et": "21:00", "group": "G", "home": "New Zealand", "away": "Egypt", "venue": "BC Place, Vancouver", "hk": "09:00+1"},
    {"date": "2026-06-22", "time_et": "13:00", "group": "J", "home": "Argentina", "away": "Austria", "venue": "AT&T Stadium, Arlington", "hk": "01:00+1"},
    {"date": "2026-06-22", "time_et": "17:00", "group": "I", "home": "France", "away": "Bolivia", "venue": "Lincoln Financial Field, Philadelphia", "hk": "05:00+1"},
    {"date": "2026-06-22", "time_et": "20:00", "group": "I", "home": "Norway", "away": "Senegal", "venue": "MetLife Stadium, East Rutherford", "hk": "08:00+1"},
    {"date": "2026-06-22", "time_et": "23:00", "group": "J", "home": "Jordan", "away": "Algeria", "venue": "Levi's Stadium, Santa Clara", "hk": "11:00+1"},
    {"date": "2026-06-23", "time_et": "13:00", "group": "K", "home": "Portugal", "away": "Uzbekistan", "venue": "NRG Stadium, Houston", "hk": "01:00+1"},
    {"date": "2026-06-23", "time_et": "16:00", "group": "L", "home": "England", "away": "Ghana", "venue": "Gillette Stadium, Foxborough", "hk": "04:00+1"},
    {"date": "2026-06-23", "time_et": "19:00", "group": "L", "home": "Panama", "away": "Croatia", "venue": "BMO Field, Toronto", "hk": "07:00+1"},
    {"date": "2026-06-23", "time_et": "22:00", "group": "K", "home": "Colombia", "away": "DR Congo", "venue": "Estadio Akron, Zapopan", "hk": "10:00+1"},
    {"date": "2026-06-24", "time_et": "15:00", "group": "B", "home": "Switzerland", "away": "Canada", "venue": "BC Place, Vancouver", "hk": "03:00+1"},
    {"date": "2026-06-24", "time_et": "15:00", "group": "B", "home": "Bosnia & Herzegovina", "away": "Qatar", "venue": "Lumen Field, Seattle", "hk": "03:00+1"},
    {"date": "2026-06-24", "time_et": "18:00", "group": "C", "home": "Scotland", "away": "Brazil", "venue": "Hard Rock Stadium, Miami Gardens", "hk": "06:00+1"},
    {"date": "2026-06-24", "time_et": "18:00", "group": "C", "home": "Morocco", "away": "Haiti", "venue": "Mercedes-Benz Stadium, Atlanta", "hk": "06:00+1"},
    {"date": "2026-06-24", "time_et": "21:00", "group": "A", "home": "Czechia", "away": "Mexico", "venue": "Estadio Azteca, Mexico City", "hk": "09:00+1"},
    {"date": "2026-06-24", "time_et": "21:00", "group": "A", "home": "South Africa", "away": "South Korea", "venue": "Estadio BBVA, Monterrey", "hk": "09:00+1"},
    {"date": "2026-06-25", "time_et": "16:00", "group": "E", "home": "Curaçao", "away": "Ivory Coast", "venue": "Lincoln Financial Field, Philadelphia", "hk": "04:00+1"},
    {"date": "2026-06-25", "time_et": "16:00", "group": "E", "home": "Ecuador", "away": "Germany", "venue": "MetLife Stadium, East Rutherford", "hk": "04:00+1"},
    {"date": "2026-06-25", "time_et": "19:00", "group": "F", "home": "Japan", "away": "Sweden", "venue": "AT&T Stadium, Arlington", "hk": "07:00+1"},
    {"date": "2026-06-25", "time_et": "19:00", "group": "F", "home": "Tunisia", "away": "Netherlands", "venue": "Arrowhead Stadium, Kansas City", "hk": "07:00+1"},
    {"date": "2026-06-25", "time_et": "22:00", "group": "D", "home": "Türkiye", "away": "USA", "venue": "SoFi Stadium, Inglewood", "hk": "10:00+1"},
    {"date": "2026-06-25", "time_et": "22:00", "group": "D", "home": "Paraguay", "away": "Australia", "venue": "Levi's Stadium, Santa Clara", "hk": "10:00+1"},
    {"date": "2026-06-26", "time_et": "15:00", "group": "I", "home": "Norway", "away": "France", "venue": "Gillette Stadium, Foxborough", "hk": "03:00+1"},
    {"date": "2026-06-26", "time_et": "15:00", "group": "I", "home": "Senegal", "away": "Bolivia", "venue": "BMO Field, Toronto", "hk": "03:00+1"},
    {"date": "2026-06-26", "time_et": "20:00", "group": "H", "home": "Cape Verde", "away": "Saudi Arabia", "venue": "NRG Stadium, Houston", "hk": "08:00+1"},
    {"date": "2026-06-26", "time_et": "20:00", "group": "H", "home": "Uruguay", "away": "Spain", "venue": "Estadio Akron, Zapopan", "hk": "08:00+1"},
    {"date": "2026-06-26", "time_et": "23:00", "group": "G", "home": "Egypt", "away": "Iran", "venue": "Lumen Field, Seattle", "hk": "11:00+1"},
    {"date": "2026-06-26", "time_et": "23:00", "group": "G", "home": "New Zealand", "away": "Belgium", "venue": "BC Place, Vancouver", "hk": "11:00+1"},
    {"date": "2026-06-27", "time_et": "17:00", "group": "L", "home": "Panama", "away": "England", "venue": "MetLife Stadium, East Rutherford", "hk": "05:00+1"},
    {"date": "2026-06-27", "time_et": "17:00", "group": "L", "home": "Croatia", "away": "Ghana", "venue": "Lincoln Financial Field, Philadelphia", "hk": "05:00+1"},
    {"date": "2026-06-27", "time_et": "19:30", "group": "K", "home": "Colombia", "away": "Portugal", "venue": "Hard Rock Stadium, Miami Gardens", "hk": "07:30+1"},
    {"date": "2026-06-27", "time_et": "19:30", "group": "K", "home": "DR Congo", "away": "Uzbekistan", "venue": "Mercedes-Benz Stadium, Atlanta", "hk": "07:30+1"},
    {"date": "2026-06-27", "time_et": "22:00", "group": "J", "home": "Algeria", "away": "Austria", "venue": "Arrowhead Stadium, Kansas City", "hk": "10:00+1"},
    {"date": "2026-06-27", "time_et": "22:00", "group": "J", "home": "Jordan", "away": "Argentina", "venue": "AT&T Stadium, Arlington", "hk": "10:00+1"},
]

VENUES = {
    "Estadio Azteca, Mexico City": "🇲🇽 Mexico City",
    "Estadio Akron, Zapopan": "🇲🇽 Zapopan (GDL)",
    "BMO Field, Toronto": "🇨🇦 Toronto",
    "SoFi Stadium, Inglewood": "🇺🇸 Los Angeles",
    "Levi's Stadium, Santa Clara": "🇺🇸 San Francisco",
    "MetLife Stadium, East Rutherford": "🇺🇸 New York",
    "Gillette Stadium, Foxborough": "🇺🇸 Boston",
    "NRG Stadium, Houston": "🇺🇸 Houston",
    "AT&T Stadium, Arlington": "🇺🇸 Dallas",
    "Lumen Field, Seattle": "🇺🇸 Seattle",
    "Lincoln Financial Field, Philadelphia": "🇺🇸 Philadelphia",
    "Estadio BBVA, Monterrey": "🇲🇽 Monterrey",
    "Mercedes-Benz Stadium, Atlanta": "🇺🇸 Atlanta",
    "Hard Rock Stadium, Miami Gardens": "🇺🇸 Miami",
    "BC Place, Vancouver": "🇨🇦 Vancouver",
    "Arrowhead Stadium, Kansas City": "🇺🇸 Kansas City",
}

def generate_html():
    today = datetime.now().strftime("%Y-%m-%d")
    now_hk = datetime.now().strftime("%Y-%m-%d %H:%M") + " HKT"
    
    # Groups HTML
    groups_html = ""
    for letter in "ABCDEFGHIJKL":
        teams = GROUPS[letter]
        groups_html += f'''<div class="group-card" id="group-{letter}">
            <div class="group-header">🏆 Group {letter}</div>
            <table class="group-table"><thead><tr><th>球隊</th><th>特色</th></tr></thead><tbody>'''
        for t in teams:
            groups_html += f'''<tr><td class="team-name">{t['team']}</td><td class="team-seed">{t['seed'] if t['seed'] else '—'}</td></tr>'''
        groups_html += '''</tbody></table></div>'''
    
    # Matches HTML
    matches_html = ""
    current_date = None
    date_num = 0
    months_cn = ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
    
    for match in MATCHES:
        m_date = match['date']
        if m_date != current_date:
            date_num += 1
            current_date = m_date
            month = int(m_date.split('-')[1])
            day = int(m_date.split('-')[2])
            date_display = f"{months_cn[month-1]}{day}日"
            matches_html += f'''<div class="date-header" id="day-{date_num}"><span class="date-badge">Day {date_num}</span><span class="date-full">{date_display}</span></div>'''
        
        venue_short = VENUES.get(match['venue'], match['venue'])
        matches_html += f'''<div class="match-card">
            <div class="match-group">Group {match['group']}</div>
            <div class="match-teams"><span class="team">{match['home']}</span><span class="vs">vs</span><span class="team">{match['away']}</span></div>
            <div class="match-meta"><span class="match-time">🕐 {match['time_et']} ET → {match['hk']} HK</span><span class="match-venue">📍 {venue_short}</span></div>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 世界盃 2026 Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@300;400;500;600;700&family=Noto+Serif+HK:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0a0a0f;
            --card-bg: #16161d;
            --card-border: #2a2a3a;
            --gold: #FFD700;
            --text: #f0f0f5;
            --text-muted: #8888a0;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Noto Sans HK', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
        
        .hero {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border: 1px solid var(--gold);
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,215,0,0.05) 0%, transparent 50%);
            animation: pulse 4s ease-in-out infinite;
        }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} }}
        .hero h1 {{ font-family: 'Noto Serif HK', serif; font-size: 2.5rem; color: var(--gold); margin-bottom: 8px; }}
        .hero .subtitle {{ color: var(--text-muted); font-size: 1rem; }}
        .hero .countdown {{ margin-top: 20px; display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; }}
        .hero .countdown-item {{ text-align: center; }}
        .hero .countdown-num {{ font-size: 2rem; font-weight: 700; color: var(--gold); }}
        .hero .countdown-label {{ font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; }}
        
        .section-header {{ font-family: 'Noto Serif HK', serif; font-size: 1.4rem; color: var(--gold); margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--card-border); }}
        
        .groups-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-bottom: 32px; }}
        .group-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; overflow: hidden; transition: border-color 0.2s; }}
        .group-card:hover {{ border-color: var(--gold); }}
        .group-header {{ background: linear-gradient(90deg, #2a2a3a, #1a1a2e); padding: 10px 14px; font-weight: 600; font-size: 1rem; }}
        .group-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .group-table th {{ text-align: left; padding: 6px 10px; color: var(--text-muted); font-weight: 500; border-bottom: 1px solid var(--card-border); }}
        .group-table td {{ padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.03); }}
        .team-name {{ font-weight: 500; }}
        .team-seed {{ color: var(--text-muted); font-size: 0.75rem; }}
        
        .stats-row {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
        .stat-card {{ flex: 1; min-width: 140px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 16px; text-align: center; }}
        .stat-card .stat-num {{ font-size: 1.8rem; font-weight: 700; color: var(--gold); }}
        .stat-card .stat-label {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 4px; }}
        
        .date-header {{ background: linear-gradient(90deg, var(--card-bg), #1a1a2e); border-left: 3px solid var(--gold); padding: 10px 16px; margin: 20px 0 12px; border-radius: 0 8px 8px 0; display: flex; align-items: center; gap: 12px; }}
        .date-badge {{ background: var(--gold); color: #000; font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; }}
        .date-full {{ font-weight: 600; font-size: 1rem; }}
        
        .match-card {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; transition: border-color 0.2s; }}
        .match-card:hover {{ border-color: var(--gold); }}
        .match-group {{ font-size: 0.7rem; background: rgba(255,215,0,0.1); color: var(--gold); padding: 2px 8px; border-radius: 4px; white-space: nowrap; }}
        .match-teams {{ flex: 1; display: flex; align-items: center; gap: 8px; font-weight: 500; font-size: 0.95rem; }}
        .match-teams .team {{ flex: 1; }}
        .match-teams .vs {{ color: var(--text-muted); font-size: 0.8rem; flex: 0 0 auto; }}
        .match-meta {{ display: flex; gap: 12px; font-size: 0.78rem; color: var(--text-muted); }}
        
        .footer {{ text-align: center; padding: 32px 0; color: var(--text-muted); font-size: 0.8rem; border-top: 1px solid var(--card-border); margin-top: 40px; }}
        
        @media (max-width: 600px) {{ .hero h1 {{ font-size: 1.8rem; }} .groups-grid {{ grid-template-columns: 1fr; }} .match-meta {{ flex-direction: column; gap: 4px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>🏆 世界盃 2026</h1>
            <p class="subtitle">北美聯合主辦 · 48隊 · 104場比賽 · 6月11日-7月19日</p>
            <div class="countdown" id="countdown">
                <div class="countdown-item"><div class="countdown-num" id="cd-days">—</div>
