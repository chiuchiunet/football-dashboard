#!/usr/bin/env python3
from math import exp, factorial
from datetime import date

TR = {
    'Argentina':(85,88,95),'France':(88,86,96),'Spain':(84,87,94),'Brazil':(87,82,93),
    'England':(82,85,92),'Germany':(83,83,91),'Portugal':(81,84,90),'Netherlands':(80,86,89),
    'Belgium':(78,80,85),'Croatia':(76,82,84),'Uruguay':(78,79,83),'Colombia':(77,78,82),
    'Italy':(74,85,83),'Mexico':(73,76,78),'USA':(72,77,77),'Denmark':(74,79,78),
    'Senegal':(75,76,77),'Morocco':(73,80,78),'Japan':(72,74,73),'Australia':(69,75,72),
    'Switzerland':(71,78,75),'Poland':(72,73,73),'Ukraine':(71,77,74),'Sweden':(70,76,73),
    'Austria':(70,75,72),'Chile':(70,72,71),'Nigeria':(71,70,70),'Serbia':(72,71,72),
    'Algeria':(68,72,68),'Ecuador':(69,73,70),'Ivory Coast':(70,68,69),'Egypt':(68,73,69),
    'Ghana':(68,69,67),'Paraguay':(69,68,68),'Peru':(68,71,69),'South Korea':(67,70,68),
    'Saudi Arabia':(65,68,64),'Qatar':(62,67,62),'Iran':(64,70,65),'Canada':(64,72,66),
    'Tunisia':(65,70,65),'Turkey':(66,68,66),'Scotland':(64,72,67),'Norway':(66,71,68),
    'Czechia':(65,70,66),'Bosnia & Herzegovina':(65,68,64),'New Zealand':(58,65,58),
    'Haiti':(55,62,54),'Panama':(58,67,58),'Jordan':(56,65,56),'Uzbekistan':(58,66,58),
    'Curacao':(55,62,54),'DR Congo':(58,62,58),'South Africa':(58,65,58),
    'Cape Verde':(58,65,58),'Bolivia':(58,65,58),
}

FE = {
    'AR':'\U0001f1e6\U0001f1f7','FR':'\U0001f1eb\U0001f1f7','ES':'\U0001f1ea\U0001f1f8',
    'BR':'\U0001f1e7\U0001f1f4','GB':'\U0001f3f4\U0001f1ec\U0001f1e7\U0001f1f8','DE':'\U0001f1e9\U0001f1ea',
    'PT':'\U0001f1f5\U0001f1f9','NL':'\U0001f1f3\U0001f1f1','BE':'\U0001f1e7\U0001f1ea',
    'HR':'\U0001f1ed\U0001f1f7','UY':'\U0001f1fa\U0001f1fe','CO':'\U0001f1e8\U0001f1f4',
    'IT':'\U0001f1ee\U0001f1f9','MX':'\U0001f1fa\U0001f1f2','US':'\U0001f1fa\U0001f1f8',
    'DK':'\U0001f1e9\U0001f1f0','SN':'\U0001f1f8\U0001f1f3','MA':'\U0001f1f2\U0001f1e6',
    'JP':'\U0001f1ef\U0001f1f5','AU':'\U0001f1e6\U0001f1fa','CH':'\U0001f1e8\U0001f1ed',
    'PL':'\U0001f1f5\U0001f1f1','UA':'\U0001f1fa\U0001f1e6','SE':'\U0001f1f8\U0001f1ea',
    'AT':'\U0001f1e6\U0001f1f9','CL':'\U0001f1e8\U0001f1f1','NG':'\U0001f1f3\U0001f1ec',
    'RS':'\U0001f1f7\U0001f1f8','DZ':'\U0001f1e9\U0001f1ff','EC':'\U0001f1ea\U0001f1e8',
    'CI':'\U0001f1e8\U0001f1ee','EG':'\U0001f1ea\U0001f1dc','GH':'\U0001f1ec\U0001f1ed',
    'PY':'\U0001f1f5\U0001f1fe','PE':'\U0001f1f5\U0001f1ea','KR':'\U0001f1f0\U0001f1f7',
    'SA':'\U0001f1f8\U0001f1e6','QA':'\U0001f1f6\U0001f1e6','IR':'\U0001f1ee\U0001f1f7',
    'CA':'\U0001f1e8\U0001f1e6','TN':'\U0001f1f9\U0001f1f3','TR':'\U0001f1f9\U0001f1f7',
    'SC':'\U0001f3f4\U0001f1ec\U0001f1e7\U0001f1f8','NO':'\U0001f1f3\U0001f1f4',
    'CZ':'\U0001f1e8\U0001f1ff','BA':'\U0001f1e7\U0001f1e6','NZ':'\U0001f1f3\U0001f1ff',
    'HT':'\U0001f1ed\U0001f1f9','PA':'\U0001f1f5\U0001f1e6','JO':'\U0001f1ef\U0001f1fe',
    'UZ':'\U0001f1fa\U0001f1ff','CW':'\U0001f1e8\U0001f1fc','CD':'\U0001f1e8\U0001f1e9',
    'ZA':'\U0001f1ff\U0001f1e6','CV':'\U0001f1e8\U0001f1fb','BO':'\U0001f1e7\U0001f1f4',
}

TF = {
    'Argentina':'AR','France':'FR','Spain':'ES','Brazil':'BR','England':'GB','Germany':'DE',
    'Portugal':'PT','Netherlands':'NL','Belgium':'BE','Croatia':'HR','Uruguay':'UY','Colombia':'CO',
    'Italy':'IT','Mexico':'MX','USA':'US','Denmark':'DK','Senegal':'SN','Morocco':'MA',
    'Japan':'JP','Australia':'AU','Switzerland':'CH','Poland':'PL','Ukraine':'UA','Sweden':'SE',
    'Austria':'AT','Nigeria':'NG','Serbia':'RS','Algeria':'DZ','Ecuador':'EC',
    'Ivory Coast':'CI','Egypt':'EG','Ghana':'GH','Paraguay':'PY','Peru':'PE','South Korea':'KR',
    'Saudi Arabia':'SA','Qatar':'QA','Iran':'IR','Canada':'CA','Tunisia':'TN','Turkey':'TR',
    'Scotland':'SC','Norway':'NO','Czechia':'CZ','Bosnia & Herzegovina':'BA','New Zealand':'NZ',
    'Haiti':'HT','Panama':'PA','Jordan':'JO','Uzbekistan':'UZ','Curacao':'CW',
    'DR Congo':'CD','South Africa':'ZA','Cape Verde':'CV','Bolivia':'BO',
}

def fl(t): return FE.get(TF.get(t,''),'\U0001f3f4')

def pp(k, l):
    if l<=0: return 1.0 if k==0 else 0.0
    return (l**k)*exp(-l)/factorial(k)

def gs(n):
    for k,v in TR.items():
        if n.lower() in k.lower() or k.lower() in n.lower(): return v
    return (60,65,60)

def prd(h, a):
    ha,hd,_=gs(h); aa,ad,_=gs(a)
    hxg=max(0.3,min(3.5,1.35*(ha/75)*(ad/75)*1.12))
    axg=max(0.2,min(3.0,1.35*(aa/75)*(hd/75)))
    hw=dw=aw=0
    for hg in range(6):
        for ag in range(6):
            p=pp(hg,hxg)*pp(ag,axg)
            if hg>ag: hw+=p
            elif hg==ag: dw+=p
            else: aw+=p
    t=hw+dw+aw; hw,dw,aw=hw/t*100,dw/t*100,aw/t*100
    o25=sum(pp(hg,hxg)*pp(ag,axg) for hg in range(6) for ag in range(6) if hg+ag>2)*100
    b,bp=(0,0),0
    for hg in range(5):
        for ag in range(5):
            p=pp(hg,hxg)*pp(ag,axg)
            if p>bp: bp=p; b=(hg,ag)
    return {'hxg':round(hxg,2),'axg':round(axg,2),'hw':round(hw,1),'dw':round(dw,1),'aw':round(aw,1),'o25':round(o25,1),'score':'{}-{}'.format(b[0],b[1])}

MT = [
    ('Mexico','South Africa','2026-06-11','A','Estadio Azteca','Mexico City'),
    ('South Korea','Czechia','2026-06-11','A','Estadio Akron','Zapopan'),
    ('Canada','Bosnia & Herzegovina','2026-06-12','B','BMO Field','Toronto'),
    ('USA','Paraguay','2026-06-12','D','SoFi Stadium','Los Angeles'),
    ('Qatar','Switzerland','2026-06-13','B','Levi\'s Stadium','Santa Clara'),
    ('Brazil','Morocco','2026-06-13','C','MetLife Stadium','East Rutherford'),
    ('Haiti','Scotland','2026-06-13','C','Gillette Stadium','Foxborough'),
    ('Australia','Turkey','2026-06-14','D','BC Place','Vancouver'),
    ('Germany','Curacao','2026-06-14','E','NRG Stadium','Houston'),
    ('Netherlands','Japan','2026-06-14','F','AT&T Stadium','Arlington'),
    ('Ivory Coast','Ecuador','2026-06-14','E','Lincoln Financial Field','Philadelphia'),
    ('Sweden','Tunisia','2026-06-14','F','Estadio BBVA','Monterrey'),
    ('Spain','Cape Verde','2026-06-15','H','Mercedes-Benz Stadium','Atlanta'),
    ('Belgium','Egypt','2026-06-15','G','Lumen Field','Seattle'),
    ('Saudi Arabia','Uruguay','2026-06-15','H','Hard Rock Stadium','Miami Gardens'),
    ('Iran','New Zealand','2026-06-15','G','SoFi Stadium','Los Angeles'),
    ('France','Senegal','2026-06-16','I','MetLife Stadium','East Rutherford'),
    ('Bolivia','Norway','2026-06-16','I','Gillette Stadium','Foxborough'),
    ('Argentina','Algeria','2026-06-16','J','Arrowhead Stadium','Kansas City'),
    ('Austria','Jordan','2026-06-17','J','Levi\'s Stadium','Santa Clara'),
    ('Portugal','DR Congo','2026-06-17','K','NRG Stadium','Houston'),
    ('England','Croatia','2026-06-17','L','AT&T Stadium','Arlington'),
    ('Ghana','Panama','2026-06-17','L','BMO Field','Toronto'),
    ('Uzbekistan','Colombia','2026-06-17','K','Estadio Azteca','Mexico City'),
    ('Czechia','South Africa','2026-06-18','A','Mercedes-Benz Stadium','Atlanta'),
    ('Switzerland','Bosnia & Herzegovina','2026-06-18','B','SoFi Stadium','Los Angeles'),
    ('Canada','Qatar','2026-06-18','B','BC Place','Vancouver'),
    ('Mexico','South Korea','2026-06-18','A','Estadio Akron','Zapopan'),
    ('USA','Australia','2026-06-19','D','Lumen Field','Seattle'),
    ('Scotland','Morocco','2026-06-19','C','Gillette Stadium','Foxborough'),
    ('Brazil','Haiti','2026-06-19','C','Lincoln Financial Field','Philadelphia'),
    ('Turkey','Paraguay','2026-06-19','D','Levi\'s Stadium','Santa Clara'),
    ('Netherlands','Sweden','2026-06-20','F','NRG Stadium','Houston'),
    ('Germany','Ivory Coast','2026-06-20','E','BMO Field','Toronto'),
    ('Ecuador','Curacao','2026-06-20','E','Arrowhead Stadium','Kansas City'),
    ('Tunisia','Japan','2026-06-21','F','Estadio BBVA','Monterrey'),
    ('Spain','Saudi Arabia','2026-06-21','H','Mercedes-Benz Stadium','Atlanta'),
    ('Belgium','Iran','2026-06-21','G','SoFi Stadium','Los Angeles'),
    ('Uruguay','Cape Verde','2026-06-21','H','Hard Rock Stadium','Miami Gardens'),
    ('New Zealand','Egypt','2026-06-21','G','BC Place','Vancouver'),
    ('Argentina','Austria','2026-06-22','J','AT&T Stadium','Arlington'),
    ('France','Bolivia','2026-06-22','I','Lincoln Financial Field','Philadelphia'),
    ('Norway','Senegal','2026-06-22','I','MetLife Stadium','East Rutherford'),
    ('Jordan','Algeria','2026-06-22','J','Levi\'s Stadium','Santa Clara'),
    ('Portugal','Uzbekistan','2026-06-23','K','NRG Stadium','Houston'),
    ('England','Ghana','2026-06-23','L','Gillette Stadium','Foxborough'),
    ('Panama','Croatia','2026-06-23','L','BMO Field','Toronto'),
    ('Colombia','DR Congo','2026-06-23','K','Estadio Akron','Zapopan'),
    ('Switzerland','Canada','2026-06-24','B','BC Place','Vancouver'),
    ('Bosnia & Herzegovina','Qatar','2026-06-24','B','Lumen Field','Seattle'),
    ('Scotland','Brazil','2026-06-24','C','Hard Rock Stadium','Miami Gardens'),
    ('Morocco','Haiti','2026-06-24','C','Mercedes-Benz Stadium','Atlanta'),
    ('Czechia','Mexico','2026-06-24','A','Estadio Azteca','Mexico City'),
    ('South Africa','South Korea','2026-06-24','A','Estadio BBVA','Monterrey'),
    ('Curacao','Ivory Coast','2026-06-25','E','Lincoln Financial Field','Philadelphia'),
    ('Ecuador','Germany','2026-06-25','E','MetLife Stadium','East Rutherford'),
    ('Japan','Sweden','2026-06-25','F','AT&T Stadium','Arlington'),
    ('Tunisia','Netherlands','2026-06-25','F','Arrowhead Stadium','Kansas City'),
    ('Turkey','USA','2026-06-25','D','SoFi Stadium','Los Angeles'),
    ('Paraguay','Australia','2026-06-25','D','Levi\'s Stadium','Santa Clara'),
    ('Norway','France','2026-06-26','I','Gillette Stadium','Foxborough'),
    ('Senegal','Bolivia','2026-06-26','I','BMO Field','Toronto'),
    ('Cape Verde','Saudi Arabia','2026-06-26','H','NRG Stadium','Houston'),
    ('Uruguay','Spain','2026-06-26','H','Estadio Akron','Zapopan'),
    ('Egypt','Iran','2026-06-26','G','Lumen Field','Seattle'),
    ('New Zealand','Belgium','2026-06-26','G','BC Place','Vancouver'),
    ('Panama','England','2026-06-27','L','MetLife Stadium','East Rutherford'),
    ('Croatia','Ghana','2026-06-27','L','Lincoln Financial Field','Philadelphia'),
    ('Colombia','Portugal','2026-06-27','K','Hard Rock Stadium','Miami Gardens'),
    ('DR Congo','Uzbekistan','2026-06-27','K','Mercedes-Benz Stadium','Atlanta'),
    ('Algeria','Austria','2026-06-27','J','Arrowhead Stadium','Kansas City'),
    ('Jordan','Argentina','2026-06-27','J','AT&T Stadium','Arlington'),
]

RE = {
    'Mexico City':'\U0001f1fa\U0001f1f2','Zapopan':'\U0001f1fa\U0001f1f2','Toronto':'\U0001f1e8\U0001f1e6',
    'Vancouver':'\U0001f1e8\U0001f1e6','Los Angeles':'\U0001f1fa\U0001f1f8','Santa Clara':'\U0001f1fa\U0001f1f8',
    'East Rutherford':'\U0001f1fa\U0001f1f8','Foxborough':'\U0001f1fa\U0001f1f8','Houston':'\U0001f1fa\U0001f1f8',
    'Arlington':'\U0001f1fa\U0001f1f8','Seattle':'\U0001f1fa\U0001f1f8','Philadelphia':'\U0001f1fa\U0001f1f8',
    'Atlanta':'\U0001f1fa\U0001f1f8','Miami Gardens':'\U0001f1fa\U0001f1f8','Kansas City':'\U0001f1fa\U0001f1f8',
    'Monterrey':'\U0001f1fa\U0001f1f2',
}

GD = {
    'A':['Mexico','South Africa','South Korea','Czechia'],
    'B':['Canada','Bosnia & Herzegovina','Qatar','Switzerland'],
    'C':['Brazil','Morocco','Haiti','Scotland'],
    'D':['USA','Paraguay','Australia','Turkey'],
    'E':['Germany','Curacao','Ivory Coast','Ecuador'],
    'F':['Netherlands','Japan','Ukraine','Tunisia'],
    'G':['Belgium','Egypt','Iran','New Zealand'],
    'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],
    'I':['France','Senegal','Bolivia','Norway'],
    'J':['Argentina','Algeria','Austria','Jordan'],
    'K':['Portugal','DR Congo','Uzbekistan','Colombia'],
    'L':['England','Croatia','Ghana','Panama'],
}

MN=['','1\u6708','2\u6708','3\u6708','4\u6708','5\u6708','6\u6708','7\u6708','8\u6708','9\u6708','10\u6708','11\u6708','12\u6708']

dl = (date(2026,6,11)-date.today()).days

gh=''
for l in 'ABCDEFGHIJKL':
    rows=''.join('<tr><td>{} {}</td><td class="s">{}</td></tr>'.format(fl(t),t,TR.get(t,(0,0,60))[2]) for t in GD[l])
    gh+='<div class="gc"><div class="gh">\u5206\u7ec4 {}</div><table class="gt"><thead><tr><th>\u7403\u961f</th><th>\u7b49\u7d1a</th></tr></thead><tbody>{}</tbody></table></div>'.format(l,rows)

mh=''
cd=None; dn=0
for home,away,d,g,venue,city in MT:
    if d!=cd:
        dn+=1; cd=d
        mo=int(d.split('-')[1]); day=int(d.split('-')[2])
        mh+='<div class="dh" id="d{}"><span class="db">Day {}</span><span class="df">{}{}\u65e5</span></div>'.format(dn,dn,MN[mo],day)
    p=prd(home,away)
    rg=RE.get(city,'')
    mh+='''<div class="mc" data-group="{}" data-day="{}" data-home="{}" data-away="{}">
<span class="mg">G{}</span>
<div class="mtc"><span class="tn">{} {}</span><span class="vs">vs</span><span class="tn">{} {}</span></div>
<div class="pred"><div class="prow">
<span class="pl">{:.1f}%</span><div class="bar" style="width:{:.0f}px;background:#4CAF50;"></div>
<span class="pl">{:.1f}%</span><div class="bar" style="width:{:.0f}px;background:#9E9E9E;"></div>
<span class="pl">{:.1f}%</span><div class="bar" style="width:{:.0f}px;background:#E91E63;"></div>
</div><div class="mr"><span class="sc">\u983b\u6e2c:{}</span><span class="o25">O2.5:{:.0f}%</span><span class="xg">xG {:.2f}-{:.2f}</span></div></div>
<div class="loc">\U0001f550 {}<br>\U0001f4cd {} {}</div>
</div>'''.format(g,dn,home,away,g,fl(home),home,fl(away),away,p['hw'],p['hw']*0.55,p['dw'],p['dw']*0.55,p['aw'],p['aw']*0.55,p['score'],p['o25'],p['hxg'],p['axg'],venue,rg,city)

js='''let cf='all';function sf(g){cf=g;document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('active'));document.querySelector('[data-filter="'+g+'"]').classList.add('active');fm();}function fm(){var q=document.getElementById('si').value.toLowerCase();document.querySelectorAll('.mc').forEach(c=>{var g=c.dataset.group;var h=c.dataset.home.toLowerCase();var a=c.dataset.away.toLowerCase();var show=(cf==='all'||g===cf)&&(!q||h.includes(q)||a.includes(q));c.classList.toggle('hid',!show);});}'''

html='<!DOCTYPE html><html lang="zh-HK"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>World Cup 2026 | Predictions + Schedule</title><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@300;400;500;600;700&family=Noto+Serif+HK:wght@400;500;600;700&display=swap" rel="stylesheet"><style>:root{--bg:#0a0a0f;--c:#16161d;--b:#2a2a3a;--g:#FFD700;--t:#f0f0f5;--m:#8888a0;}*{margin:0;padding:0;box-sizing:border-box;}body{font-family:"Noto Sans HK",sans-serif;background:var(--bg);color:var(--t);min-height:100vh;}.w{max-width:1100px;margin:0 auto;padding:20px;}.hero{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);border:1px solid var(--g);border-radius:16px;padding:36px;text-align:center;margin-bottom:24px;}.hero h1{font-family:"Noto Serif HK",serif;font-size:2.4rem;color:var(--g);margin-bottom:8px;}.hero p{color:var(--m);font-size:0.95rem;}.cd{margin-top:16px;display:flex;justify-content:center;gap:28px;flex-wrap:wrap;}.cdi{text-align:center;}.cdn{font-size:1.8rem;font-weight:700;color:var(--g);}.cdl{font-size:0.68rem;color:var(--m);text-transform:uppercase;}.filters{display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap;align-items:center;}.fbtn{background:var(--c);border:1px solid var(--b);color:var(--t);padding:7px 14px;border-radius:8px;cursor:pointer;font-size:0.82rem;font-family:inherit;transition:all .2s;}.fbtn:hover,.fbtn.active{border-color:var(--g);color:var(--g);}.fbtn.active{background:rgba(255,215,0,0.12);}.sbar{background:var(--c);border:1px solid var(--b);color:var(--t);padding:7px 12px;border-radius:8px;font-size:0.82rem;font-family:inherit;width:180px;}.sbar::placeholder{color:var(--m);}.stats{display:flex;gap:12px;margin-bottom:24px;}.sc{flex:1;background:var(--c);border:1px solid var(--b);border-radius:10px;padding:12px;text-align:center;}.scn{font-size:1.5rem;font-weight:700;color:var(--g);}.scl{font-size:0.72rem;color:var(--m);margin-top:3px;}h2{font-family:"Noto Serif HK",serif;font-size:1.2rem;color:var(--g);margin:24px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--b);}.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(185px,1fr));gap:12px;margin-bottom:28px;}.gc{background:var(--c);border:1px solid var(--b);border-radius:10px;overflow:hidden;transition:border-color .2s;}.gc:hover{border-color:var(--g);}.gh{background:linear-gradient(90deg,#2a2a3a,#1a1a2e);padding:8px 12px;font-weight:600;font-size:0.88rem;}.gt{width:100%;border-collapse:collapse;font-size:0.76rem;}.gt th{text-align:left;padding:5px 8px;color:var(--m);font-weight:500;border-bottom:1px solid var(--b);}.gt td{padding:6px 8px;border-bottom:1px solid rgba(255,255,255,0.04);}.gt td.s{color:var(--m);font-size:0.68rem;text-align:right;}.dh{background:linear-gradient(90deg,var(--c),#1a1a2e);border-left:3px solid var(--g);padding:8px 14px;margin:18px 0 10px;border-radius:0 6px 6px 0;display:flex;align-items:center;gap:10px;}.db{background:var(--g);color:#000;font-size:0.65rem;font-weight:700;padding:2px 7px;border-radius:4px;}.df{font-weight:600;font-size:0.92rem;}.mc{background:var(--c);border:1px solid var(--b);border-radius:10px;padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;transition:border-color .2s;}.mc:hover{border-color:var(--g);}.mc.hid{display:none;}.mg{font-size:0.65rem;background:rgba(255,215,0,0.12);color:var(--g);padding:2px 7px;border-radius:4px;white-space:nowrap;}.mtc{display:flex;align-items:center;gap:8px;flex:1;min-width:180px;}.tn{font-weight:500;font-size:0.88rem;}.vs{color:var(--m);font-size:0.72rem;}.pred{flex:1;min-width:160px;}.prow{display:flex;align-items:center;gap:3px;margin-bottom:4px;}.pl{font-size:0.62rem;width:34px;text-align:center;color:var(--m);}.bar{height:6px;border-radius:3px;min-width:3px;max-width:55px;}.mr{display:flex;gap:10px;}.sc,.o25,.xg{font-size:0.62rem;color:var(--m);}.loc{font-size:0.68rem;color:var(--m);text-align:right;line-height:1.5;min-width:120px;}.ft{text-align:center;padding:24px 0;color:var(--m);font-size:0.72rem;border-top:1px solid var(--b);margin-top:32px;}@media(max-width:600px){.hero h1{font-size:1.7rem;}.gg{grid-template-columns:1fr;}.mc{flex-direction:column;align-items:flex-start;}.mtc,.pred,.loc{width:100%;}.loc{text-align:left;}.sbar{width:100%;}}}</style></head><body><div class="w"><div class="hero"><h1>World Cup 2026</h1><p>48 Teams | 104 Matches | Jun 11 - Jul 19 | North America</p><div class="cd"><div class="cdi"><div class="cdn">'+str(dl)+'</div><div class="cdl">Days to Kick-off</div></div><div class="cdi"><div class="cdn">48</div><div class="cdl">Teams</div></div><div class="cdi"><div class="cdn">72</div><div class="cdl">Group Matches</div></div><div class="cdi"><div class="cdn">12</div><div class="cdl">Groups</div></div></div></div><div class="filters"><button class="fbtn active" data-filter="all" onclick="sf(\'all\')">All</button><button class="fbtn" data-filter="A" onclick="sf(\'A\')">A</button><button class="fbtn" data-filter="B" onclick="sf(\'B\')">B</button><button class="fbtn" data-filter="C" onclick="sf(\'C\')">C</button><button class="fbtn" data-filter="D" onclick="sf(\'D\')">D</button><button class="fbtn" data-filter="E" onclick="sf(\'E\')">E</button><button class="fbtn" data-filter="F" onclick="sf(\'F\')">F</button><button class="fbtn" data-filter="G" onclick="sf(\'G\')">G</button><button class="fbtn" data-filter="H" onclick="sf(\'H\')">H</button><button class="fbtn" data-filter="I" onclick="sf(\'I\')">I</button><button class="fbtn" data-filter="J" onclick="sf(\'J\')">J</button><button class="fbtn" data-filter="K" onclick="sf(\'K\')">K</button><button class="fbtn" data-filter="L" onclick="sf(\'L\')">L</button><input type="text" class="sbar" id="si" placeholder="Search team or match..." oninput="fm()"></div><div class="stats"><div class="sc"><div class="scn">3</div><div class="scl">Host Nations</div></div><div class="sc"><div class="scn">48</div><div class="scl">Teams</div></div><div class="sc"><div class="scn">72</div><div class="scl">Group Matches</div></div><div class="sc"><div class="scn">32</div><div class="scl">Knockout Teams</div></div></div><h2>Groups</h2><div class="gg">'+gh+'</div><h2>Schedule + Predictions</h2>'+mh+'<div class="ft">Powered by Hanni | Poisson Model</div></div><script>'+js+'</script></body></html>'

with open('/home/ubuntu/.openclaw/workspace-football/web/index.html','w',encoding='utf-8') as f:
    f.write(html)
print('Done! Size: {} chars'.format(len(html)))
