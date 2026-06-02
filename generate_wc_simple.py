#!/usr/bin/env python3
"""World Cup 2026 Simple Dashboard Generator"""
from datetime import date

CN = {'Argentina':'阿根廷','France':'法國','Spain':'西班牙','Brazil':'巴西','England':'英格蘭','Germany':'德國','Portugal':'葡萄牙','Netherlands':'荷蘭','Belgium':'比利時','Croatia':'克羅地亞','Uruguay':'烏拉圭','Colombia':'哥倫比亞','Italy':'意大利','Mexico':'墨西哥','USA':'美國','Denmark':'丹麥','Senegal':'塞內加爾','Morocco':'摩洛哥','Japan':'日本','Australia':'澳洲','Switzerland':'瑞士','Poland':'波蘭','Sweden':'瑞典','Austria':'奧地利','Algeria':'阿爾及利亞','Ecuador':'厄瓜多爾','Ivory Coast':'象牙海岸','Egypt':'埃及','Ghana':'加納','Paraguay':'巴拉圭','South Korea':'南韓','Saudi Arabia':'沙特阿拉伯','Qatar':'卡塔爾','Iran':'伊朗','Canada':'加拿大','Tunisia':'突尼斯','Turkey':'土耳其','Scotland':'蘇格蘭','Norway':'挪威','Czechia':'捷克','Bosnia Herz':'波斯尼亞','New Zealand':'新西蘭','Haiti':'海地','Panama':'巴拿馬','Jordan':'約旦','Uzbekistan':'烏茲別克','Curacao':'庫拉索','DR Congo':'剛果','South Africa':'南非','Cape Verde':'佛得角','Bolivia':'玻利維亞'}
TR = {'Argentina':95,'France':96,'Spain':94,'Brazil':93,'England':92,'Germany':91,'Portugal':90,'Netherlands':89,'Belgium':85,'Croatia':84,'Uruguay':83,'Colombia':82,'Italy':83,'Mexico':78,'USA':77,'Denmark':78,'Senegal':77,'Morocco':78,'Japan':73,'Australia':72,'Switzerland':75,'Poland':73,'Sweden':73,'Austria':72,'Algeria':68,'Ecuador':70,'Ivory Coast':69,'Egypt':69,'Ghana':67,'Paraguay':68,'South Korea':68,'Saudi Arabia':64,'Qatar':62,'Iran':65,'Canada':66,'Tunisia':65,'Turkey':66,'Scotland':67,'Norway':68,'Czechia':66,'Bosnia Herz':64,'New Zealand':58,'Haiti':54,'Panama':58,'Jordan':56,'Uzbekistan':58,'Curacao':54,'DR Congo':58,'South Africa':58,'Cape Verde':58,'Bolivia':58}
F = {'AR':'🇦🇹','FR':'🇫🇷','ES':'🇪🇸','BR':'🇧🇷','GB':'🇬🇧','DE':'🇩🇪','PT':'🇵🇹','NL':'🇳🇱','BE':'🇧🇪','HR':'🇭🇷','UY':'🇺🇾','CO':'🇨🇴','IT':'🇮🇹','MX':'🇲🇽','US':'🇺🇸','DK':'🇩🇰','SN':'🇸🇳','MA':'🇲🇦','JP':'🇯🇵','AU':'🇦🇺','CH':'🇨🇭','PL':'🇵🇱','SE':'🇸🇪','AT':'🇦🇹','DZ':'🇩🇿','EC':'🇪🇨','CI':'🇨🇮','EG':'🇪🇬','GH':'🇬🇭','PY':'🇵🇾','KR':'🇰🇷','SA':'🇸🇦','QA':'🇶🇦','IR':'🇮🇷','CA':'🇨🇦','TN':'🇹🇳','TR':'🇹🇷','SC':'🏴󄒁','NO':'🇳🇴','CZ':'🇨🇿','BA':'🇧🇦','NZ':'🇳🇿','HT':'🇭🇹','PA':'🇵🇦','JO':'🇯🇴','UZ':'🇺🇿','CW':'🇨🇼','CD':'🇨🇩','ZA':'🇿🇦','CV':'🇨🇻','BO':'🇧🇴'}

def fl(t): return F.get(t, '🏴')
def cn(t): return CN.get(t, t)
def rt(t): return TR.get(t, 60)

# Groups
GD = {
    'A':['Mexico','South Africa','South Korea','Czechia'],
    'B':['Canada','Bosnia Herz','Qatar','Switzerland'],
    'C':['Brazil','Morocco','Haiti','Scotland'],
    'D':['USA','Paraguay','Australia','Turkey'],
    'E':['Germany','Curacao','Ivory Coast','Ecuador'],
    'F':['Netherlands','Japan','New Zealand','Scotland'],
    'G':['Belgium','Egypt','Iran','New Zealand'],
    'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],
    'I':['France','Senegal','Bolivia','Norway'],
    'J':['Argentina','Algeria','Austria','Jordan'],
    'K':['Portugal','DR Congo','Uzbekistan','Colombia'],
    'L':['England','Croatia','Ghana','Panama']
}

dl = (date(2026,6,11) - date.today()).days

# Generate groups HTML
gh = ''
for g in 'ABCDEFGHIJKL':
    rows = ''
    for t in GD[g]:
        rows += f'<tr><td>{fl(t)} {t}</td><td>{rt(t)}</td><td>{cn(t)}</td></tr>'
    gh += f'''<div class="gc"><div class="gh">組 {g}</div><table class="gt"><thead><tr><th>球隊</th><th>實力</th><th>中文</th></tr></thead><tbody>{rows}</tbody></table></div>'''

html = f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>FIFA 世界盃 2026 | 預測 + 賽程</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0a0a0f;--c:#16161d;--b:#2a2a3a;--g:#FFD700;--t:#f0f0f5;--m:#8888a0;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:"Noto Sans HK",sans-serif;background:var(--bg);color:var(--t);padding:16px;}}
.wrap{{max-width:1100px;margin:0 auto;}}
.hero{{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid var(--g);border-radius:14px;padding:24px;text-align:center;margin-bottom:18px;}}
.hero h1{{font-size:1.8rem;color:var(--g);margin-bottom:6px;}}
.cd{{margin-top:10px;display:flex;justify-content:center;gap:16px;}}
.cdi{{text-align:center;}}
.cdn{{font-size:1.3rem;font-weight:700;color:var(--g);}}
.cdl{{font-size:0.55rem;color:var(--m);text-transform:uppercase;}}
.stats{{display:flex;gap:8px;margin-bottom:16px;}}
.sc{{flex:1;background:var(--c);border:1px solid var(--b);border-radius:8px;padding:8px;text-align:center;}}
.scn{{font-size:1rem;font-weight:700;color:var(--g);}}
.scl{{font-size:0.55rem;color:var(--m);}}
.filters{{display:flex;gap:5px;margin-bottom:16px;flex-wrap:wrap;}}
.fbtn{{background:var(--c);border:1px solid var(--b);color:var(--t);padding:5px 10px;border-radius:5px;cursor:pointer;font-size:0.7rem;}}
.fbtn:hover,.fbtn.active{{border-color:var(--g);color:var(--g);}}
h2{{font-size:0.9rem;color:var(--g);margin:16px 0 8px;border-bottom:1px solid var(--b);padding-bottom:4px;}}
.gg{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;margin-bottom:20px;}}
.gc{{background:var(--c);border:1px solid var(--b);border-radius:8px;overflow:hidden;}}
.gc:hover{{border-color:var(--g);}}
.gh{{background:linear-gradient(90deg,#2a2a3a,#1a1a2e);padding:5px 10px;font-weight:600;font-size:0.75rem;}}
.gt{{width:100%;border-collapse:collapse;font-size:0.65rem;}}
.gt th{{text-align:left;padding:3px 6px;color:var(--m);border-bottom:1px solid var(--b);}}
.gt td{{padding:4px 6px;border-bottom:1px solid rgba(255,255,255,0.04);}}
.gt td:nth-child(2){{color:var(--m);text-align:right;font-size:0.6rem;}}
.gt td:nth-child(3){{color:var(--m);font-size:0.6rem;}}
.legend{{background:var(--c);border:1px solid var(--b);border-radius:10px;padding:14px;margin:18px 0;}}
.legend h3{{font-size:0.9rem;color:var(--g);margin-bottom:10px;}}
.li{{display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:0.75rem;}}
.dot{{width:10px;height:10px;border-radius:50%;}}
.info{{width:16px;height:16px;background:var(--g);color:#000;border-radius:50%;font-size:0.55rem;display:flex;align-items:center;justify-content:center;font-weight:700;}}
.ft{{text-align:center;padding:18px 0;color:var(--m);font-size:0.65rem;border-top:1px solid var(--b);margin-top:24px;}}
@media(max-width:600px){{.gg{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>
<div class="wrap">
<div class="hero">
<h1>🏆 FIFA 世界盃 2026</h1>
<p>2026年6月11日 - 7月19日 | 美國 / 加拿大 / 墨西哥</p>
<div class="cd">
<div class="cdi"><div class="cdn">{dl}</div><div class="cdl">Days to Kickoff</div></div>
<div class="cdi"><div class="cdn">48</div><div class="cdl">Teams</div></div>
<div class="cdi"><div class="cdn">72</div><div class="cdl">Matches</div></div>
<div class="cdi"><div class="cdn">12</div><div class="cdl">Groups</div></div>
</div>
</div>
<div class="stats">
<div class="sc"><div class="scn">104</div><div class="scl">Total Matches</div></div>
<div class="sc"><div class="scn">3</div><div class="scl">Teams/Adv</div></div>
<div class="sc"><div class="scn">8</div><div class="scl">Knockout</div></div>
</div>
<div class="filters">
<button class="fbtn active" onclick="filterGroup('all')">全部</button>
{' '.join([f'<button class="fbtn" data-g="{g}" onclick="filterGroup(\'{g}\')">{g}</button>' for g in 'ABCDEFGHIJKL'])}
</div>
<h2>參賽球隊</h2>
<div class="gg">{gh}</div>
<div class="legend">
<h3>預測解釋</h3>
<div class="li"><span class="dot" style="background:#4CAF50;"></span><span><b>實力值</b> = 基于 FIFA 排名同近期表現</span></div>
<div class="li"><span class="info">i</span><span><b>xG</b> = 預期入球數，根據攻防強度計算</span></div>
<div class="li"><span class="info">i</span><span><b>O2.5</b> = 兩隊合計超過2.5球概率</span></div>
<div class="li"><span class="info">i</span><span><b>信心度</b>: 高(差&gt;25%) 中(12-25%) 低(&lt;12%)</span></div>
</div>
<div class="ft">Data from World Cup 2026 Fixtures | Updated: {date.today()}</div>
</div>
<script>
function filterGroup(g){{
document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('active'));
if(g=='all'){{document.querySelector('.fbtn').classList.add('active');}}
else{{document.querySelector('[data-g="'+g+'"]').classList.add('active');}}
}}
</script>
</body>
</html>'''

with open('web/index.html', 'w') as f:
    f.write(html)
print('✓ World Cup Dashboard generated!')
