#!/usr/bin/env python3
"""Add recent form display to generate_html.py"""

with open('generate_html.py', 'r') as f:
    content = f.read()

# 1. Add recent form SQL function before main()
sql_func = '''

def get_recent_form_html(conn, team_id, is_home):
    """Generate HTML for recent form"""
    cur = conn.cursor()
    if is_home:
        sc, oc, tc = 'home_score', 'away_score', 'home_team_id'
        venue = '主場'
    else:
        sc, oc, tc = 'away_score', 'home_score', 'away_team_id'
        venue = '作客'
    
    cur.execute(f"""
        SELECT m.{sc}, m.{oc}, t.name
        FROM matches m JOIN teams t ON t.team_id = 
            CASE WHEN m.home_team_id = ? THEN m.away_team_id ELSE m.home_team_id END
        WHERE m.{tc} = ? AND m.{sc} IS NOT NULL
        ORDER BY m.utc_date DESC LIMIT 5
    """, (team_id, team_id))
    
    matches = cur.fetchall()
    if not matches:
        return ""
    
    html = f'<div style="margin-top:8px;padding-top:6px;border-top:1px dashed rgba(34,197,94,0.2);">'
    html += f'<div style="font-size:0.7em;color:#166534;font-weight:600;margin-bottom:4px;">{venue} - 近5場:</div>'
    html += '<div style="display:flex;gap:3px;flex-wrap:wrap;">'
    
    for gf, ga, opp in matches:
        r = 'W' if gf > ga else 'D' if gf == ga else 'L'
        opp_s = opp[:10]
        bg = 'rgba(34,197,94,0.15)' if r == 'W' else 'rgba(245,158,11,0.15)' if r == 'D' else 'rgba(239,68,68,0.15)'
        col = '#15803d' if r == 'W' else '#b45309' if r == 'D' else '#dc2626'
        html += f'<span style="font-size:0.65em;padding:2px 5px;border-radius:3px;background:{bg};color:{col};font-weight:500;">{r}<b>{gf}-{ga}</b></span>'
    
    html += '</div></div>'
    return html

'''

content = content.replace('if __name__', sql_func + '\nif __name__')

# 2. Modify SQL to add home_id, away_id to SELECT
content = content.replace(
    'p.recommended_bets\n        FROM matches m',
    'p.recommended_bets,\n               m.home_team_id, m.away_team_id\n        FROM matches m'
)

# 3. Modify tuple unpacking to include home_id, away_id
content = content.replace(
    'eag, hhp, dhp, ahp, ehg2, ea2, bets) = row',
    'eag, hhp, dhp, ahp, ehg2, ea2, bets, home_id, away_id) = row'
)

# 4. Modify return to fetch and pass recent form - prediction_card_from_tuple
old_return = '''    return _build_card(utc_date, comp, home, away, hwp, dp, awp, ov, un, bts_yes, bts_no, ehg, ea, hhp, dhp, ahp, ehg2, ea2, bets, home_id, away_id)'''

new_return = '''    conn = sqlite3.connect(DB_PATH)
    home_recent = get_recent_form_html(conn, home_id, True)
    away_recent = get_recent_form_html(conn, away_id, False)
    conn.close()
    return _build_card(utc_date, comp, home, away, hwp, dp, awp, ov, un, bts_yes, bts_no, ehg, ea, hhp, dhp, ahp, ehg2, ea2, bets, home_id, away_id, home_recent, away_recent)'''

content = content.replace(old_return, new_return)

# 5. Modify _build_card signature to accept home_recent and away_recent
content = content.replace(
    'home_id: int = 0, away_id: int = 0) -> str:',
    'home_id: int = 0, away_id: int = 0, home_recent: str = "", away_recent: str = "") -> str:'
)

# 6. Add recent form HTML after h2h_section in the card
content = content.replace(
    '{h2h_section}\n        \n        {\'<div class="value-bets">',
    '{h2h_section}\n        {home_recent}\n        {away_recent}\n        {\'<div class="value-bets">'
)

with open('generate_html.py', 'w') as f:
    f.write(content)

print("Done!")
