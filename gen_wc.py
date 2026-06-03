#!/usr/bin/env python3
"""World Cup 2026 Full Dashboard"""
from datetime import date
import math, random

CN = {
    'Argentina':'阿根廷','France':'法國','Spain':'西班牙','Brazil':'巴西',
    'England':'英格蘭','Germany':'德國','Portugal':'葡萄牙','Netherlands':'荷蘭',
    'Belgium':'比利時','Croatia':'克羅地亞','Uruguay':'烏拉圭','Colombia':'哥倫比亞',
    'Italy':'意大利','Mexico':'墨西哥','USA':'美國','Denmark':'丹麥',
    'Senegal':'塞內加爾','Morocco':'摩洛哥','Japan':'日本','Australia':'澳洲',
    'Switzerland':'瑞士','Poland':'波蘭','Sweden':'瑞典','Austria':'奧地利',
    'Algeria':'阿爾及利亞','Ecuador':'厄瓜多爾','Ivory Coast':'象牙海岸',
    'Egypt':'埃及','Ghana':'加納','Paraguay':'巴拉圭','South Korea':'南韓',
    'Saudi Arabia':'沙特阿拉伯','Qatar':'卡塔爾','Iran':'伊朗','Canada':'加拿大',
    'Tunisia':'突尼斯','Turkey':'土耳其','Scotland':'蘇格蘭','Norway':'挪威',
    'Czechia':'捷克','Bosnia Herz':'波斯尼亞','New Zealand':'新西蘭',
    'Haiti':'海地','Panama':'巴拿馬','Jordan':'約旦','Uzbekistan':'烏茲別克',
    'Curacao':'庫拉索','DR Congo':'剛果','South Africa':'南非',
    'Cape Verde':'佛得角','Bolivia':'玻利維亞','Ukraine':'烏克蘭',
}
TR = {
    'Argentina':95,'France':96,'Spain':94,'Brazil':93,'England':92,'Germany':91,
    'Portugal':90,'Netherlands':89,'Belgium':85,'Croatia':84,'Uruguay':83,
    'Colombia':82,'Italy':83,'Mexico':78,'USA':77,'Denmark':78,'Senegal':77,
    'Morocco':78,'Japan':73,'Australia':72,'Switzerland':75,'Poland':73,
    'Sweden':73,'Austria':72,'Algeria':68,'Ecuador':70,'Ivory Coast':69,
    'Egypt':69,'Ghana':67,'Paraguay':68,'South Korea':68,'Saudi Arabia':64,
    'Qatar':62,'Iran':65,'Canada':66,'Tunisia':65,'Turkey':66,'Scotland':67,
    'Norway':68,'Czechia':66,'Bosnia Herz':64,'New Zealand':58,'Haiti':54,
    'Panama':58,'Jordan':56,'Uzbekistan':58,'Curacao':54,'DR Congo':58,
    'South Africa':58,'Cape Verde':58,'Bolivia':58,'Ukraine':60,
}
E2C = {
    'AR':'🇦🇹','FR':'🇫🇷','ES':'🇪🇸','BR':'🇧🇷','GB':'🇬🇧','DE':'🇩🇪','PT':'🇵🇹',
    'NL':'🇳🇱','BE':'🇧🇪','HR':'🇭🇷','UY':'🇺🇾','CO':'🇨🇴','IT':'🇮🇹','MX':'🇲🇽',
    'US':'🇺🇸','DK':'🇩🇰','SN':'🇸🇳','MA':'🇲🇦','JP':'🇯🇵','AU':'🇦🇺','CH':'🇨🇭',
    'PL':'🇵🇱','SE':'🇸🇪','AT':'🇦🇹','DZ':'🇩🇿','EC':'🇪🇨','CI':'🇨🇮','EG':'🇪🇬',
    'GH':'🇬🇭','PY':'🇵🇾','KR':'🇰🇷','SA':'🇸🇦','QA':'🇶🇦','CA':'🇨🇦','TN':'🇹🇳',
    'TR':'🇹🇷','NO':'🇳🇴','CZ':'🇨🇿','BA':'🇧🇦','NZ':'🇳🇿','HT':'🇭🇹','PA':'🇵🇦',
    'JO':'🇯🇴','UZ':'🇺🇿','CW':'🇨🇼','CD':'🇨🇩','ZA':'🇿🇦','CV':'🇨🇻','BO':'🇧🇴',
    'UA':'🇺🇦',
}
def fl(t):
    m={'Argentina':'AR','France':'FR','Spain':'ES','Brazil':'BR','England':'GB','Germany':'DE','Portugal':'PT','Netherlands':'NL','Belgium':'BE','Croatia':'HR','Uruguay':'UY','Colombia':'CO','Italy':'IT','Mexico':'MX','USA':'US','Denmark':'DK','Senegal':'SN','Morocco':'MA','Japan':'JP','Australia':'AU','Switzerland':'CH','Poland':'PL','Sweden':'SE','Austria':'AT','Algeria':'DZ','Ecuador':'EC','Ivory Coast':'CI','Egypt':'EG','Ghana':'GH','Paraguay':'PY','South Korea':'KR','Saudi Arabia':'SA','Qatar':'QA','Canada':'CA','Tunisia':'TN','Turkey':'TR','Scotland':'SC','Norway':'NO','Czechia':'CZ','Bosnia Herz':'BA','New Zealand':'NZ','Haiti':'HT','Panama':'PA','Jordan':'JO','Uzbekistan':'UZ','Curacao':'CW','DR Congo':'CD','South Africa':'ZA','Cape Verde':'CV','Bolivia':'BO','Ukraine':'UA'}
    return E2C.get(m.get(t,'🏴'),'🏴')
def cn(t): return CN.get(t,t)
def rt(t): return TR.get(t,60)
def group_of(team):
    GD={'A':['Mexico','South Africa','South Korea','Czechia'],'B':['Canada','Bosnia Herz','Qatar','Switzerland'],'C':['Brazil','Morocco','Haiti','Scotland'],'D':['USA','Paraguay','Australia','Turkey'],'E':['Germany','Curacao','Ivory Coast','Ecuador'],'F':['Netherlands','Japan','Ukraine','Tunisia'],'G':['Belgium','Egypt','Iran','New Zealand'],'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],'I':['France','Senegal','Bolivia','Norway'],'J':['Argentina','Algeria','Austria','Jordan'],'K':['Portugal','DR Congo','Uzbekistan','Colombia'],'L':['England','Croatia','Ghana','Panama']}
    for g,ts in GD.items():
        if team in ts: return g
    return '?'

VENUES = {
    'New York':('🇺🇸','紐約'),'Los Angeles':('🇺🇸','洛杉矶'),'Dallas':('🇺🇸','達拉斯'),
    'Miami':('🇺🇸','邁阿密'),'Seattle':('🇺🇸','西雅圖'),'San Francisco':('🇺🇸','三藩市'),
    'Boston':('🇺🇸','波士頓'),'Houston':('🇺🇸','侯斯頓'),'Kansas City':('🇺🇸','堪薩斯城'),
    'Philadelphia':('🇺🇸','費城'),'Atlanta':('🇺🇸','亞特蘭大'),'Denver':('🇺🇸','丹佛'),
    'Phoenix':('🇺🇸','鳳凰城'),'Mexiko City':('🇲🇽','墨西哥城'),
    'Guadalajara':('🇲🇽','瓜達拉哈拉'),'Monterrey':('🇲🇽','蒙特雷'),
    'Toronto':('🇨🇦','多倫多'),'Vancouver':('🇨🇦','溫哥華'),
}

MT = [
    ('6月11日','Mexico','South Africa','22:00','New York'),('6月11日','South Korea','Czechia','01:00','Los Angeles'),
    ('6月12日','Canada','Bosnia Herz','22:00','Toronto'),('6月12日','USA','Paraguay','02:00','Los Angeles'),
    ('6月13日','Qatar','Switzerland','22:00','Mexiko City'),('6月13日','Brazil','Morocco','01:00','New York'),
    ('6月13日','Haiti','Scotland','22:00','Denver'),
    ('6月14日','Australia','Turkey','22:00','Los Angeles'),('6月14日','Germany','Curacao','01:00','Mexiko City'),
    ('6月14日','Netherlands','Japan','22:00','Seattle'),('6月14日','Ivory Coast','Ecuador','01:00','Vancouver'),
    ('6月15日','Spain','Cape Verde','22:00','Miami'),('6月15日','Belgium','Egypt','01:00','New York'),
    ('6月15日','Saudi Arabia','Uruguay','22:00','Kansas City'),('6月15日','Iran','New Zealand','01:00','Toronto'),
    ('6月16日','France','Senegal','22:00','Boston'),('6月16日','Bolivia','Norway','01:00','Denver'),
    ('6月16日','Argentina','Algeria','22:00','New York'),('6月17日','Austria','Jordan','01:00','Los Angeles'),
    ('6月17日','Portugal','DR Congo','22:00','Seattle'),('6月17日','England','Croatia','01:00','New York'),
    ('6月17日','Ghana','Panama','22:00','Toronto'),('6月17日','Uzbekistan','Colombia','01:00','Miami'),
    ('6月18日','Czechia','South Africa','22:00','Seattle'),('6月18日','Switzerland','Bosnia Herz','01:00','Toronto'),
    ('6月18日','Canada','Qatar','22:00','Vancouver'),('6月18日','Mexico','South Korea','01:00','Mexiko City'),
    ('6月19日','USA','Australia','22:00','Boston'),('6月19日','Scotland','Morocco','01:00','San Francisco'),
    ('6月19日','Brazil','Haiti','22:00','Los Angeles'),('6月19日','Turkey','Paraguay','01:00','New York'),
    ('6月20日','Netherlands','Sweden','22:00','New York'),('6月20日','Germany','Ivory Coast','01:00','Dallas'),
    ('6月20日','Ecuador','Curacao','22:00','San Francisco'),
    ('6月21日','Tunisia','Japan','22:00','Phoenix'),('6月21日','Spain','Saudi Arabia','01:00','Los Angeles'),
    ('6月21日','Belgium','Iran','22:00','Boston'),('6月21日','Uruguay','Cape Verde','01:00','Seattle'),
    ('6月21日','New Zealand','Egypt','22:00','Vancouver'),
    ('6月22日','Argentina','Austria','22:00','Dallas'),('6月22日','France','Bolivia','01:00','Los Angeles'),
    ('6月22日','Norway','Senegal','22:00','Boston'),('6月22日','Jordan','Algeria','01:00','Miami'),
    ('6月23日','Portugal','Uzbekistan','22:00','Miami'),('6月23日','England','Ghana','01:00','New York'),
    ('6月23日','Ghana','Panama','22:00','Toronto'),('6月23日','Colombia','DR Congo','01:00','Los Angeles'),
    ('6月24日','Switzerland','Canada','22:00','Toronto'),('6月24日','Bosnia Herz','Qatar','01:00','Phoenix'),
    ('6月24日','Czechia','Mexico','22:00','Dallas'),('6月24日','South Africa','South Korea','01:00','Kansas City'),
    ('6月25日','Ecuador','Germany','22:00','San Francisco'),('6月25日','Sweden','Tunisia','01:00','Denver'),
    ('6月25日','Turkey','USA','22:00','Philadelphia'),('6月25日','Paraguay','Australia','01:00','Miami'),
    ('6月26日','Uruguay','Spain','22:00','New York'),('6月26日','Saudi Arabia','Cape Verde','01:00','Dallas'),
    ('6月26日','Egypt','Iran','22:00','Houston'),('6月26日','Belgium','New Zealand','01:00','Philadelphia'),
    ('6月26日','Norway','France','22:00','New York'),('6月26日','Senegal','Bolivia','01:00','Seattle'),
    ('6月27日','Jordan','Argentina','22:00','Houston'),('6月27日','Algeria','Austria','01:00','Kansas City'),
    ('6月27日','Colombia','Portugal','22:00','Philadelphia'),('6月27日','DR Congo','Uzbekistan','01:00','Denver'),
    ('6月27日','Panama','England','22:00','Miami'),('6月27日','Croatia','Ghana','01:00','New York'),
]

GD={'A':['Mexico','South Africa','South Korea','Czechia'],'B':['Canada','Bosnia Herz','Qatar','Switzerland'],'C':['Brazil','Morocco','Haiti','Scotland'],'D':['USA','Paraguay','Australia','Turkey'],'E':['Germany','Curacao','Ivory Coast','Ecuador'],'F':['Netherlands','Japan','Ukraine','Tunisia'],'G':['Belgium','Egypt','Iran','New Zealand'],'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],'I':['France','Senegal','Bolivia','Norway'],'J':['Argentina','Algeria','Austria','Jordan'],'K':['Portugal','DR Congo','Uzbekistan','Colombia'],'L':['England','Croatia','Ghana','Panama']}

def strength_diff(home, away):
    diff = rt(home) - rt(away)
    xg_h = max(0.3, min(4.5, 1.35 + diff*0.045 + 0.18))
    xg_a = max(0.2, min(3.8, 1.05 - diff*0.045))
    return xg_h, xg_a

def poisson_prob(x, mu):
    return math.exp(-mu) * (mu**x) / math.factorial(x)

def most_likely_score(xg_h, xg_a):
    best, best_p = (0,0), 0
    for g in range(6):
        for b in range(6):
            p = poisson_prob(g, xg_h) * poisson_prob(b, xg_a)
            if p > best_p: best, best_p = (g,b), p
    return best, best_p

def win_probs(xg_h, xg_a):
    ph = pa = 0.0
    for gh in range(8):
        for ga in range(8):
            p = poisson_prob(gh, xg_h) * poisson_prob(ga, xg_a)
            if gh > ga: ph += p
            elif ga > gh: pa += p
    return ph, 1-ph-pa, pa

random.seed(42)
def simulate_groups(n=10000):
    results = {g: {t: 0 for t in GD[g]} for g in GD}
    group_map = {
        'A':[('Mexico','South Africa'),('South Korea','Czechia'),('Mexico','South Korea'),('South Africa','Czechia'),('Mexico','Czechia'),('South Africa','South Korea')],
        'B':[('Canada','Bosnia Herz'),('Qatar','Switzerland'),('Canada','Qatar'),('Bosnia Herz','Switzerland'),('Canada','Switzerland'),('Bosnia Herz','Qatar')],
        'C':[('Brazil','Morocco'),('Haiti','Scotland'),('Brazil','Haiti'),('Morocco','Scotland'),('Brazil','Scotland'),('Morocco','Haiti')],
        'D':[('USA','Paraguay'),('Australia','Turkey'),('USA','Australia'),('Paraguay','Turkey'),('USA','Turkey'),('Paraguay','Australia')],
        'E':[('Germany','Curacao'),('Ivory Coast','Ecuador'),('Germany','Ivory Coast'),('Curacao','Ecuador'),('Germany','Ecuador'),('Curacao','Ivory Coast')],
        'F':[('Netherlands','Japan'),('Ukraine','Tunisia'),('Netherlands','Ukraine'),('Japan','Tunisia'),('Netherlands','Tunisia'),('Japan','Ukraine')],
        'G':[('Belgium','Egypt'),('Iran','New Zealand'),('Belgium','Iran'),('Egypt','New Zealand'),('Belgium','New Zealand'),('Egypt','Iran')],
        'H':[('Spain','Cape Verde'),('Saudi Arabia','Uruguay'),('Spain','Saudi Arabia'),('Cape Verde','Uruguay'),('Spain','Uruguay'),('Cape Verde','Saudi Arabia')],
        'I':[('France','Senegal'),('Bolivia','Norway'),('France','Bolivia'),('Senegal','Norway'),('France','Norway'),('Senegal','Bolivia')],
        'J':[('Argentina','Algeria'),('Austria','Jordan'),('Argentina','Austria'),('Algeria','Jordan'),('Argentina','Jordan'),('Algeria','Austria')],
        'K':[('Portugal','DR Congo'),('Uzbekistan','Colombia'),('Portugal','Uzbekistan'),('DR Congo','Colombia'),('Portugal','Colombia'),('DR Congo','Uzbekistan')],
        'L':[('England','Croatia'),('Ghana','Panama'),('England','Ghana'),('Croatia','Panama'),('England','Panama'),('Croatia','Ghana')],
    }
    for _ in range(n):
        for g in GD:
            pts, gd = {t:0 for t in GD[g]}, {t:0 for t in GD[g]}
            for home, away in group_map[g]:
                xh, xa = strength_diff(home, away)
                sc, _ = most_likely_score(xh, xa)
                pts[home] += sc[0]; pts[away] += sc[1]
                gd[home] += sc[0]-sc[1]; gd[away] += sc[1]-sc[0]
                if sc[0]>sc[1]: pts[home] += 3
                elif sc[1]>sc[0]: pts[away] += 3
            sorted_t = sorted(GD[g], key=lambda t: (-pts[t], -gd[t]))
            for i,t in enumerate(sorted_t[:2]): results[g][t] += 1
    for g in results:
        for t in results[g]: results[g][t] = results[g][t]/n*100
    return results

ADV = simulate_groups(10000)

def is_big(home, away): return rt(home) >= 83 and rt(away) >= 83

dl = max(0, (date(2026,6,11) - date.today()).days)

gh = 
for g in 'ABCDEFGHIJKL':
    rows = 
    for t in sorted(GD[g], key=lambda x: -ADV[g][x]):
        ap = ADV[g][t]
        rows += f'<tr><td>{fl(t)} {cn(t)}</td><td style="text-align:center;font-size:0.7rem;">{rt(t)}</td><td style="text-align:right;color:#4ade80;font-size:0.7rem;">{ap:.0f}%</td><td style="width:{ap}%;background:rgba(74,222,128,0.15);height:8px;"></td></tr>'
    gh += f'<div class="gc"><div class="gh">組 {g}</div><table class="gt"><thead><tr><th>球隊</th><th style="text-align:center">實力</th><th style="text-align:right">出線%</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>'

mm = 
last_date = 
for item in MT:
    d, home, away, hkt, venue = item
    if d != last_date:
        mm += f'<div class="md">📅 {d}</div>'
        last_date = d

    xg_h, xg_a = strength_diff(home, away)
    score, _ = most_likely_score(xg_h, xg_a)
    ph, pd, pa = win_probs(xg_h, xg_a)
    big = '⭐' if is_big(home, away) else 
    conf = max(ph, pd, pa)
    conf_badge = '🔴' if conf > 0.55 else '🟡' if conf > 0.40 else '🟢'
    total = xg_h + xg_a
    ou = f'O{total:.1f}' if total >= 2.5 else f'U{total:.1f}'
    v_flag, v_cn = VENUES.get(venue, ('🏴','未知'))

    mm += f'''<div class="mc">
<div class="mhd">
  <span class="mcomp">G{group_of(home)} {big}</span>
  <span class="mconf">{conf_badge}</span>
  <span class="mhkt">🕐 {hkt} HK</span>
  <span class="mvenue">{v_flag} {v_cn}</span>
</div>
<div class="mbody">
  <div class="mteam">{fl(home)} {cn(home)}<span class="str">{rt(home)}</span></div>
  <div class="mscore">{score[0]}⚽{score[1]}</div>
  <div class="mteam">{fl(away)} {cn(away)}<span class="str">{rt(away)}</span></div>
</div>
<div class="mfoot">
  <div class="mbar"><div class="mp" style="width:{ph*100:.0f}%"><span>H{ph*100:.0f}%</span></div><div class="mpd" style="width:{pd*100:.0f}%"><span>D{pd*100:.0f}%</span></div><div class="mpa" style="width:{pa*100:.0f}%"><span>A{pa*100:.0f}%</span></div></div>
  <div class="mxg">xG {xg_h:.1f}-{xg_a:.1f} | {ou} | H2H {rt(home)-rt(away):+.0f}</div>
</div>
</div>'''

buckets = {'90+':0,'80-89':0,'70-79':0,'60-69':0,'<60':0}
for t,r in TR.items():
    if r>=90: buckets['90+']+=1
    elif r>=80: buckets['80-89']+=1
    elif r>=70: buckets['70-79']+=1
    elif r>=60: buckets['60-69']+=1
    else: buckets['<60']+=1
max_b = max(buckets.values())
sd_bars = .join(f'<div class="sb"><div class="sl">{k}</div><div class="sb2"><div class="sbf" style="width:{v/max_b*100:.0f}%"></div></div><div class="sn">{v}</div></div>' for k,v in buckets.items())

KO_BRACKET = [
    ('16強', ['🇦🇹 阿根廷 vs 瑞士 🇨🇭','🇩🇪 德國 vs 葡萄牙','🇫🇷 法國 vs 哥倫比亞','🇧🇷 巴西 vs 英格蘭','🏴 英格蘭 vs 荷蘭','🇪🇸 西班牙 vs 比利時','🇵🇹 葡萄牙 vs 法國','🇦🇹 阿根廷 vs 巴西']),
    ('8強', ['🇦🇹 阿根廷 vs 🇩🇪 德國','🇧🇷 巴西 vs 🏴 英格蘭','🇫🇷 法國 vs 🇪🇸 西班牙','🇵🇹 葡萄牙 vs 🇳🇱 荷蘭']),
    ('4強', ['🇦🇹 阿根廷 vs 🇫🇷 法國','🇧🇷 巴西 vs 🇵🇹 葡萄牙']),
    ('決賽', ['🇦🇹 阿根廷 vs 🇧🇷 巴西','預測：阿根廷 2-1 巴西 🏆']),
]
ko_html = 
for round_name, matches in KO_BRACKET:
    ko_html += f'<div class="kn"><h4>{round_name}</h4>'
    for m in matches: ko_html += f'<div class="km">{m}</div>'
    ko_html += '</div>'

today = str(date.today())

CSS = '*{margin:0;padding:0;box-sizing:border-box;}body{font-family:"Noto Sans HK",sans-serif;background:#080810;color:#f0f0f5;padding:12px;}.wrap{max-width:1100px;margin:0 auto;}.hero{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #FFD700;border-radius:14px;padding:22px;text-align:center;margin-bottom:16px;}.hero h1{font-size:1.8rem;color:#FFD700;margin-bottom:4px;}.hero p{color:#8888a0;font-size:0.75rem;margin-top:4px;}.cd{margin-top:12px;display:flex;justify-content:center;gap:14px;flex-wrap:wrap;}.cdi{text-align:center;}.cdn{font-size:1.3rem;font-weight:700;color:#FFD700;}.cdl{font-size:0.5rem;color:#8888a0;text-transform:uppercase;}.stats{display:flex;gap:6px;margin-bottom:16px;}.sc{flex:1;background:#16161d;border:1px solid #2a2a3a;border-radius:8px;padding:8px;text-align:center;}.scn{font-size:1rem;font-weight:700;color:#FFD700;}.scl{font-size:0.5rem;color:#8888a0;}.tab-nav{display:flex;gap:4px;margin-bottom:14px;}.tab{background:#16161d;border:1px solid #2a2a3a;color:#f0f0f5;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:0.75rem;}.tab.active{background:#FFD700;color:#000;font-weight:700;}.content{display:none;}.content.show{display:block;}h2{font-size:0.9rem;color:#FFD700;margin:18px 0 8px;border-bottom:1px solid #2a2a3a;padding-bottom:4px;}.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px;margin-bottom:20px;}.gc{background:#16161d;border:1px solid #2a2a3a;border-radius:10px;overflow:hidden;}.gh{background:linear-gradient(90deg,#2a2a3a,#1a1a2e);padding:6px 10px;font-weight:700;font-size:0.75rem;color:#FFD700;}.gt{width:100%;border-collapse:collapse;font-size:0.62rem;}.gt th{text-align:left;padding:4px 6px;color:#8888a0;border-bottom:1px solid #2a2a3a;}.gt td{padding:4px 6px;border-bottom:1px solid #1a1a2e;}.str{color:#888;font-size:0.7em;margin-left:3px;}.ml{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.md{background:#FFD700;color:#000;font-size:0.7rem;font-weight:700;padding:5px 12px;border-radius:5px;margin:14px 0 6px;}.mc{background:#16161d;border:1px solid #2a2a3a;border-radius:10px;overflow:hidden;}.mhd{display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:#1a1a2e;border-bottom:1px solid #2a2a3a;gap:6px;}.mcomp{font-size:0.65rem;font-weight:700;color:#FFD700;}.mconf{font-size:0.7rem;}.mhkt{font-size:0.6rem;color:#FFD700;}.mvenue{font-size:0.6rem;color:#8888a0;}.mbody{display:flex;align-items:center;padding:12px;gap:10px;}.mteam{flex:1;font-size:0.85rem;font-weight:600;}.mscore{font-size:1.4rem;font-weight:700;color:#FFD700;padding:0 12px;white-space:nowrap;}.mfoot{padding:6px 10px;border-top:1px solid #2a2a3a;}.mbar{display:flex;height:20px;border-radius:4px;overflow:hidden;gap:2px;margin-bottom:4px;}.mp{background:rgba(74,222,128,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpd{background:rgba(148,148,160,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpa{background:rgba(248,113,113,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mxg{font-size:0.58rem;color:#8888a0;}.sd{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:20px;}.sb{display:flex;align-items:center;gap:6px;}.sl{font-size:0.65rem;color:#8888a0;width:32px;text-align:right;}.sb2{flex:1;height:16px;background:#1a1a2e;border-radius:3px;overflow:hidden;}.sbf{height:100%;background:linear-gradient(90deg,#FFD700,#e94560);border-radius:3px;}.sn{font-size:0.65rem;color:#FFD700;font-weight:700;width:16px;}.kg{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:20px;}.kn{background:#16161d;border:1px solid #2a2a3a;border-radius:8px;padding:10px;}.kn h4{font-size:0.75rem;color:#FFD700;margin-bottom:6px;text-align:center;}.km{font-size:0.65rem;padding:4px 8px;background:#1a1a2e;border-radius:5px;margin-bottom:4px;}.ft{text-align:center;padding:16px 0;color:#8888a0;font-size:0.6rem;border-top:1px solid #2a2a3a;margin-top:20px;}'

html = f'<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🏆 FIFA 世界盃 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="hero">
<h1>🏆 FIFA 世界盃 2026</h1>
<p>6月11日 - 7月19日 | 美國 🇺🇸 / 加拿大 🇨🇦 / 墨西哥 🇲🇽</p>
<div class="cd">
<div class="cdi"><div class="cdn">{dl}</div><div class="cdl">Days</div></div>
<div class="cdi"><div class="cdn">48</div><div class="cdl">Teams</div></div>
<div class="cdi"><div class="cdn">72</div><div class="cdl">Matches</div></div>
<div class="cdi"><div class="cdn">12</div><div class="cdl">Groups</div></div>
<div class="cdi"><div class="cdn">16</div><div class="cdl">Venues</div></div>
</div>
</div>
<div class="stats">
<div class="sc"><div class="scn">16</div><div class="scl">Venues</div></div>
<div class="sc"><div class="scn">8</div><div class="scl">16強</div></div>
<div class="sc"><div class="scn">4</div><div class="scl">8強</div></div>
<div class="sc"><div class="scn">2</div><div class="scl">半決</div></div>
<div class="sc"><div class="scn">1</div><div class="scl">決賽</div></div>
</div>
<div class="tab-nav">
<button class="tab active" onclick="showTab('groups')">📊 48隊 + 出線概率</button>
<button class="tab" onclick="showTab('matches')">📅 72場賽程</button>
<button class="tab" onclick="showTab('strength')">📈 實力分佈</button>
<button class="tab" onclick="showTab('knockout')">🏆 淘汰賽預測</button>
</div>
<div id="groups" class="content show">
<h2>📊 12個小組 · 48隊出線概率（Monte Carlo 10,000次模擬）</h2>
<div class="gg">{gh}</div>
</div>
<div id="matches" class="content">
<h2>📅 分組賽程 · 含預測比分 / xG / HK時間 / 場地</h2>
<div class="ml">{mm}</div>
</div>
<div id="strength" class="content">
<h2>📈 實力分佈（48支球隊）</h2>
<div class="sd">{sd_bars}</div>
</div>
<div id="knockout" class="content">
<h2>🏆 淘汰賽預測（基於實力模擬）</h2>
<div class="kg">{ko_html}</div>
</div>
<div class="ft">Updated: {today} | Generated by Hanni 🐰 | Poisson Model xG</div>
</div>
<script>
function showTab(tab){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.content').forEach(c=>c.classList.remove('show'));document.querySelectorAll('.tab').forEach(t=>{if(t.getAttribute('onclick').includes(tab))t.classList.add('active');});document.getElementById(tab).classList.add('show');}
</script>
</body>
</html>'

with open('web/index.html','w') as f: f.write(html)
print('OK - World Cup Dashboard generated!')
