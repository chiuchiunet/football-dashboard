with open('generate_html.py', 'r') as f:
    content = f.read()

func = '''

def get_recent_form_html(conn, team_id, is_home):
    cur = conn.cursor()
    if is_home:
        sc, oc, tc, venue = 'home_score', 'away_score', 'home_team_id', '主場'
    else:
        sc, oc, tc, venue = 'away_score', 'home_score', 'away_team_id', '作客'
    
    cur.execute(f"""
        SELECT m.%s, m.%s, t.name FROM matches m 
        JOIN teams t ON t.team_id = CASE WHEN m.home_team_id = ? THEN m.away_team_id ELSE m.home_team_id END
        WHERE m.%s = ? AND m.%s IS NOT NULL ORDER BY m.utc_date DESC LIMIT 5
    """ % (sc, oc, tc, sc), (team_id, team_id))
    
    rows = cur.fetchall()
    if not rows:
        return ""
    
    html = '<div style="margin-top:8px;padding-top:6px;border-top:1px dashed rgba(34,197,94,0.2);">'
    html += '<div style="font-size:0.7em;color:#166534;font-weight:600;margin-bottom:4px;">' + venue + ' - 近5場:</div>'
    html += '<div style="display:flex;gap:3px;flex-wrap:wrap;">'
    
    for gf, ga, opp in rows:
        r = 'W' if gf > ga else 'D' if gf == ga else 'L'
        bg = 'rgba(34,197,94,0.15)' if r == 'W' else 'rgba(245,158,11,0.15)' if r == 'D' else 'rgba(239,68,68,0.15)'
        col = '#15803d' if r == 'W' else '#b45309' if r == 'D' else '#dc2626'
        html += '<span style="font-size:0.65em;padding:2px 5px;border-radius:3px;background:%s;color:%s;font-weight:500;">%s<b>%s-%s</b></span>' % (bg, col, r, gf, ga)
    
    return html + '</div></div>'

'''

content = content.replace('if __name__', func + '\nif __name__')

with open('generate_html.py', 'w') as f:
    f.write(content)

print("Step 1 done: added function")
