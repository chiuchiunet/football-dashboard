#!/usr/bin/env python3
"""World Cup 2026 Dashboard Generator - Full 104 Matches + Recent Form"""
from datetime import date
import random, json

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
    'Iraq':'伊拉克',
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
    'South Africa':58,'Cape Verde':58,'Bolivia':58,'Ukraine':60,'Iraq':67,
}

E2C = {
    'AR':'🇦🇷','FR':'🇫🇷','ES':'🇪🇸','BR':'🇧🇷','GB':'🇬🇧','DE':'🇩🇪','PT':'🇵🇹',
    'NL':'🇳🇱','BE':'🇧🇪','HR':'🇭🇷','UY':'🇺🇾','CO':'🇨🇴','IT':'🇮🇹','MX':'🇲🇽',
    'US':'🇺🇸','DK':'🇩🇰','SN':'🇸🇳','MA':'🇲🇦','JP':'🇯🇵','AU':'🇦🇺','CH':'🇨🇭',
    'PL':'🇵🇱','SE':'🇸🇪','AT':'🇦🇹','DZ':'🇩🇿','EC':'🇪🇨','CI':'🇨🇮','EG':'🇪🇬',
    'GH':'🇬🇭','PY':'🇵🇾','KR':'🇰🇷','SA':'🇸🇦','QA':'🇶🇦','CA':'🇨🇦','TN':'🇹🇳',
    'TR':'🇹🇷','NO':'🇳🇴','CZ':'🇨🇿','BA':'🇧🇦','NZ':'🇳🇿','HT':'🇭🇹','PA':'🇵🇦',
    'JO':'🇯🇴','UZ':'🇺🇿','CW':'🇨🇼','CD':'🇨🇩','ZA':'🇿🇦','CV':'🇨🇻','BO':'🇧🇴',
    'UA':'🇺🇦','IQ':'🇮🇶',
}

def fl(t):
    m = {'Argentina':'AR','France':'FR','Spain':'ES','Brazil':'BR','England':'GB','Germany':'DE','Portugal':'PT','Netherlands':'NL','Belgium':'BE','Croatia':'HR','Uruguay':'UY','Colombia':'CO','Italy':'IT','Mexico':'MX','USA':'US','Denmark':'DK','Senegal':'SN','Morocco':'MA','Japan':'JP','Australia':'AU','Switzerland':'CH','Poland':'PL','Sweden':'SE','Austria':'AT','Algeria':'DZ','Ecuador':'EC','Ivory Coast':'CI','Egypt':'EG','Ghana':'GH','Paraguay':'PY','South Korea':'KR','Saudi Arabia':'SA','Qatar':'QA','Canada':'CA','Tunisia':'TN','Turkey':'TR','Scotland':'SC','Norway':'NO','Czechia':'CZ','Bosnia Herz':'BA','New Zealand':'NZ','Haiti':'HT','Panama':'PA','Jordan':'JO','Uzbekistan':'UZ','Curacao':'CW','DR Congo':'CD','South Africa':'ZA','Cape Verde':'CV','Bolivia':'BO','Ukraine':'UA','Iraq':'IQ'}
    return E2C.get(m.get(t,'🏴'),'🏴')

def cn(t): return CN.get(t, t)
def rt(t): return TR.get(t, 60)

GD = {
    'A':['Mexico','South Africa','South Korea','Czechia'],
    'B':['Canada','Bosnia Herz','Qatar','Switzerland'],
    'C':['Brazil','Morocco','Haiti','Scotland'],
    'D':['USA','Paraguay','Australia','Turkey'],
    'E':['Germany','Curacao','Ivory Coast','Ecuador'],
    'F':['Netherlands','Japan','Sweden','Tunisia'],
    'G':['Belgium','Egypt','Iran','New Zealand'],
    'H':['Spain','Cape Verde','Saudi Arabia','Uruguay'],
    'I':['France','Senegal','Iraq','Norway'],
    'J':['Argentina','Algeria','Austria','Jordan'],
    'K':['Portugal','DR Congo','Uzbekistan','Colombia'],
    'L':['England','Croatia','Ghana','Panama'],
}

# Load recent form data
try:
    with open('recent_form.json', 'r') as f:
        RECENT_FORM = json.load(f)
except:
    RECENT_FORM = {}

def get_recent_form_html(team):
    """Generate recent form HTML for a team."""
    if team not in RECENT_FORM:
        return '<div class="rf"><span class="rfnil">無數據</span></div>'
    matches = RECENT_FORM[team][:3]  # Last 3 matches
    html = '<div class="rf">'
    for m in matches:
        date_str, home, score, away, venue, comp = m
        is_upcoming = score == 'v'
        if is_upcoming:
            result_class = 'rfup'
            result_text = 'vs'
        else:
            try:
                hs, as_ = map(int, score.split('-'))
                if home == team:
                    if hs > as_:
                        result_class = 'rfw'
                        result_text = f'W {score}'
                    elif hs < as_:
                        result_class = 'rfl'
                        result_text = f'L {score}'
                    else:
                        result_class = 'rfd'
                        result_text = f'D {score}'
                else:
                    if as_ > hs:
                        result_class = 'rfw'
                        result_text = f'W {score}'
                    elif as_ < hs:
                        result_class = 'rfl'
                        result_text = f'L {score}'
                    else:
                        result_class = 'rfd'
                        result_text = f'D {score}'
            except:
                result_class = 'rfup'
                result_text = score
        opp = away if home == team else home
        short_opp = opp[:8]
        html += f'<span class="{result_class}">{short_opp} {result_text}</span>'
    html += '</div>'
    return html

ALL_MATCHES = [
    ('6月11日','Mexico','South Africa','15:00','Mexico City'),
    ('6月11日','South Korea','Czechia','22:00','Guadalajara'),
    ('6月12日','Canada','Bosnia Herz','15:00','Toronto'),
    ('6月12日','USA','Paraguay','21:00','Los Angeles'),
    ('6月13日','Qatar','Switzerland','15:00','San Francisco'),
    ('6月13日','Brazil','Morocco','18:00','New York'),
    ('6月13日','Haiti','Scotland','21:00','Boston'),
    ('6月13日','Australia','Turkey','12:00','Vancouver'),
    ('6月14日','Germany','Curacao','13:00','Houston'),
    ('6月14日','Ivory Coast','Ecuador','19:00','Philadelphia'),
    ('6月14日','Netherlands','Japan','16:00','Dallas'),
    ('6月14日','Sweden','Tunisia','22:00','Monterrey'),
    ('6月15日','Spain','Cape Verde','12:00','Atlanta'),
    ('6月15日','Belgium','Egypt','15:00','Seattle'),
    ('6月15日','Saudi Arabia','Uruguay','18:00','Miami'),
    ('6月15日','Iran','New Zealand','21:00','Los Angeles'),
    ('6月16日','France','Senegal','15:00','New York'),
    ('6月16日','Iraq','Norway','18:00','Boston'),
    ('6月16日','Argentina','Algeria','03:00','Kansas City'),
    ('6月16日','Austria','Jordan','12:00','San Francisco'),
    ('6月17日','Portugal','DR Congo','13:00','Houston'),
    ('6月17日','Uzbekistan','Colombia','22:00','Mexico City'),
    ('6月17日','England','Croatia','16:00','Dallas'),
    ('6月17日','Ghana','Panama','19:00','Toronto'),
    ('6月18日','Czechia','South Africa','18:00','Atlanta'),
    ('6月18日','Mexico','South Korea','03:00','Guadalajara'),
    ('6月18日','Switzerland','Bosnia Herz','21:00','Los Angeles'),
    ('6月18日','Canada','Qatar','00:00','Vancouver'),
    ('6月19日','Scotland','Morocco','02:00','Boston'),
    ('6月19日','Brazil','Haiti','03:00','Philadelphia'),
    ('6月19日','USA','Australia','21:00','Seattle'),
    ('6月19日','Turkey','Paraguay','12:00','San Francisco'),
    ('6月20日','Germany','Ivory Coast','22:00','Toronto'),
    ('6月20日','Ecuador','Curacao','04:00','Kansas City'),
    ('6月20日','Netherlands','Sweden','13:00','Houston'),
    ('6月20日','Tunisia','Japan','12:00','Monterrey'),
    ('6月21日','Spain','Saudi Arabia','12:00','Atlanta'),
    ('6月21日','Uruguay','Cape Verde','18:00','Miami'),
    ('6月21日','Belgium','Iran','21:00','Los Angeles'),
    ('6月21日','New Zealand','Egypt','03:00','Vancouver'),
    ('6月22日','France','Iraq','13:00','Philadelphia'),
    ('6月22日','Norway','Senegal','20:00','New York'),
    ('6月22日','Argentina','Austria','13:00','Dallas'),
    ('6月22日','Jordan','Algeria','11:00','San Francisco'),
    ('6月23日','Portugal','Uzbekistan','13:00','Houston'),
    ('6月23日','Colombia','DR Congo','22:00','Guadalajara'),
    ('6月23日','England','Ghana','22:00','Boston'),
    ('6月23日','Panama','Croatia','03:00','Toronto'),
    ('6月24日','Mexico','Czechia','03:00','Mexico City'),
    ('6月24日','South Korea','South Africa','03:00','Monterrey'),
    ('6月24日','Switzerland','Canada','21:00','Vancouver'),
    ('6月24日','Bosnia Herz','Qatar','03:00','Seattle'),
    ('6月24日','Scotland','Brazil','02:00','Miami'),
    ('6月24日','Morocco','Haiti','02:00','Atlanta'),
    ('6月25日','Ecuador','Germany','22:00','New York'),
    ('6月25日','Curacao','Ivory Coast','22:00','Philadelphia'),
    ('6月25日','Japan','Sweden','03:00','Dallas'),
    ('6月25日','Tunisia','Netherlands','03:00','Kansas City'),
    ('6月25日','Turkey','USA','06:00','Los Angeles'),
    ('6月25日','Paraguay','Australia','06:00','San Francisco'),
    ('6月26日','Egypt','Iran','03:00','Seattle'),
    ('6月26日','New Zealand','Belgium','03:00','Vancouver'),
    ('6月26日','Cape Verde','Saudi Arabia','02:00','Houston'),
    ('6月26日','Uruguay','Spain','02:00','Guadalajara'),
    ('6月26日','Norway','France','21:00','Boston'),
    ('6月26日','Senegal','Iraq','21:00','Toronto'),
    ('6月27日','Algeria','Austria','06:00','Kansas City'),
    ('6月27日','Jordan','Argentina','06:00','Dallas'),
    ('6月27日','Colombia','Portugal','03:30','Miami'),
    ('6月27日','DR Congo','Uzbekistan','03:30','Atlanta'),
    ('6月27日','Panama','England','01:00','New York'),
    ('6月27日','Croatia','Ghana','01:00','Philadelphia'),
    ('6月28日','Runner-up A','Runner-up B','15:00','Los Angeles'),
    ('6月29日','Winner C','Runner-up F','13:00','Houston'),
    ('6月29日','Winner E','3rd A/B/C/D','18:30','Boston'),
    ('6月29日','Winner F','Runner-up C','21:00','Monterrey'),
    ('6月30日','Runner-up E','Runner-up I','13:00','Dallas'),
    ('6月30日','Winner I','3rd C/D/F/G/H','17:00','New York'),
    ('6月30日','Winner A','3rd C/E/F/H/I','03:00','Mexico City'),
    ('7月1日','Winner L','3rd E/H/I/J/K','18:00','Atlanta'),
    ('7月1日','Winner G','3rd A/E/H/I/J','22:00','Seattle'),
    ('7月1日','Winner D','3rd B/E/F/I/J','02:00','San Francisco'),
    ('7月2日','Winner H','Runner-up J','21:00','Los Angeles'),
    ('7月2日','Runner-up K','Runner-up L','03:00','Toronto'),
    ('7月2日','Winner B','3rd E/F/G/I/J','11:00','Vancouver'),
    ('7月3日','Runner-up D','Runner-up G','14:00','Dallas'),
    ('7月3日','Winner J','Runner-up H','18:00','Miami'),
    ('7月3日','Winner K','3rd D/E/I/J/L','21:30','Kansas City'),
    ('7月4日','W37','W38','13:00','Houston'),
    ('7月4日','W41','W42','17:00','Philadelphia'),
    ('7月5日','W39','W40','22:00','New York'),
    ('7月5日','W43','W44','02:00','Mexico City'),
    ('7月6日','W45','W46','15:00','Dallas'),
    ('7月6日','W47','W48','20:00','Seattle'),
    ('7月7日','W49','W50','04:00','Atlanta'),
    ('7月7日','W51','W52','16:00','Vancouver'),
    ('7月9日','QF1-W','QF1-L','22:00','Boston'),
    ('7月10日','QF2-W','QF2-L','15:00','Los Angeles'),
    ('7月11日','QF3-W','QF3-L','17:00','Miami'),
    ('7月11日','QF4-W','QF4-L','21:00','Kansas City'),
    ('7月14日','SF1-W','SF1-L','15:00','Dallas'),
    ('7月15日','SF2-W','SF2-L','15:00','Atlanta'),
    ('7月18日','Semi1-L','Semi2-L','17:00','Miami'),
    ('7月19日','Final-W1','Final-W2','15:00','New York'),
]

TBD = set(['Runner-up A','Runner-up B','Winner C','Runner-up F','Winner E','3rd A/B/C/D','Winner F','Runner-up E','Runner-up I','Winner I','3rd C/D/F/G/H','Winner A','3rd C/E/F/H/I','Winner L','3rd E/H/I/J/K','Winner G','3rd A/E/H/I/J','Winner D','3rd B/E/F/I/J','Winner H','Runner-up J','Runner-up K','Runner-up L','Winner B','3rd E/F/G/I/J','Runner-up D','Runner-up G','Winner J','Runner-up H','Winner K','3rd D/E/I/J/L','W37','W38','W41','W42','W39','W40','W43','W44','W45','W46','W47','W48','W49','W50','W51','W52','SF1-W','SF1-L','SF2-W','SF2-L','QF1-W','QF1-L','QF2-W','QF2-L','QF3-W','QF3-L','QF4-W','QF4-L','Semi1-W','Semi1-L','Semi2-W','Semi2-L','Semi1-L','Semi2-L','Final-W1','Final-W2'])

def et_to_hk(et):
    h,m=map(int,et.split(':'))
    h+=13
    if h>=24: h-=24; return f"{h:02}:{m:02}",True
    return f"{h:02}:{m:02}",False

def prob(h,a):
    d=h-a
    hp=max(0,45+d*0.6); ap=max(0,45-d*0.6); dp=max(0,100-hp-ap)
    if dp<5: dp=5
    if hp>90: hp=90+(hp-90)*0.3
    if ap>90: ap=90+(ap-90)*0.3
    t=hp+dp+ap
    return hp/t*100,dp/t*100,ap/t*100

def xg(h,a):
    b=(h+a)/200
    return round(b*(h/75)*1.8,1),round(b*(a/75)*1.6,1)

def score(h,a):
    lh=(h/75)*1.5*(0.8+random.random()*0.5)
    la=(a/75)*1.1*(0.8+random.random()*0.5)
    return max(0,int(lh)),max(0,int(la))

def stage_of(day):
    # Extract month and day properly
    parts = day.replace('月', '-').replace('日', '').split('-')
    m_num = int(parts[0])
    d_num = int(parts[1])
    if m_num == 6 and d_num <= 27: return 'GS'
    if m_num == 7 and d_num <= 3: return 'R32'
    if m_num == 7 and 4 <= d_num <= 7: return 'R16'
    if m_num == 7 and 9 <= d_num <= 11: return 'QF'
    if m_num == 7 and 14 <= d_num <= 15: return 'SF'
    if m_num == 7 and d_num == 18: return '3RD'
    return 'FNL'

SN={'GS':'分組','R32':'32強','R16':'16強','QF':'8強','SF':'準決','3RD':'季軍','FNL':'決賽'}
IC={'GS':'📅','R32':'🎯','R16':'⚡','QF':'🔥','SF':'🏆','3RD':'🥉','FNL':'🏆'}

today=date.today().strftime('%Y-%m-%d')
days_to_go=max(0,(date(2026,6,11)-date.today()).days)

gh=[]
for g in 'ABCDEFGHIJKL':
    ts=GD[g]
    rows=[]
    for t in sorted(ts,key=lambda x:-rt(x)):
        rf_html = get_recent_form_html(t)
        rows.append(f"<tr><td>{fl(t)} {cn(t)}</td><td style='text-align:center;font-size:0.7rem;'>{rt(t)}</td><td style='text-align:right;color:#4ade80;font-size:0.7rem;'>—</td><td style='width:100.0%;background:rgba(74,222,128,0.1);height:8px;'></td></tr><tr><td colspan='4' style='padding:2px 6px;border-bottom:1px solid #1a1a2e;'>{rf_html}</td></tr>")
    gh.append(f"<div class='gc'><div class='gh'>組 {g}</div><table class='gt'><thead><tr><th>球隊</th><th style='text-align:center'>實力</th><th style='text-align:right'>出線%</th><th></th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>")

mm=[]
cur=''
for m in ALL_MATCHES:
    day,h,a,et,city=m
    hk,nd=et_to_hk(et)
    plus=' (+1)' if nd else ''
    st=stage_of(day)
    lbl=SN[st]
    icon=IC[st]
    if day!=cur:
        mm.append(f"<div class='md'>{icon} {day} <span style='font-size:0.65rem;color:#888;margin-left:6px;'>({lbl})</span></div>")
        cur=day
    if h in TBD or a in TBD:
        mm.append(f"<div class='mc'><div class='mhd'><span class='mcomp'>{lbl} </span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span></div><div class='mbody' style='justify-content:center;'><span style='color:#888;font-size:0.75rem;'>⚠️ 待定 - 分組賽後揭曉</span></div></div>")
    else:
        hs,as_=rt(h),rt(a)
        hp,dp,ap_=prob(hs,as_)
        xh,xa=xg(hs,as_)
        hsc,asc=score(hs,as_)
        rf_h = get_recent_form_html(h)
        rf_a = get_recent_form_html(a)
        mm.append(f"<div class='mc'><div class='mhd'><span class='mcomp'>{lbl} </span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span></div><div class='mbody'><div class='mteam'>{fl(h)} {cn(h)}<span class='str'>{hs}</span><div class='mr'>{rf_h}</div></div><div class='mscore'>{hsc}⚽{asc}</div><div class='mteam'>{fl(a)} {cn(a)}<span class='str'>{as_}</span><div class='mr'>{rf_a}</div></div></div><div class='mfoot'><div class='mbar'><div class='mp' style='width:{hp:.0f}%'><span>H{hp:.0f}%</span></div><div class='mpd' style='width:{dp:.0f}%'><span>D{dp:.0f}%</span></div><div class='mpa' style='width:{ap_:.0f}%'><span>A{ap_:.0f}%</span></div></div><div class='mxg'>xG {xh}-{xa} | O{int(xh+xa+0.5)}</div></div></div>")

all_t=[]
for ts in GD.values(): all_t.extend(ts)
all_t.sort(key=lambda t:-rt(t))
sd=''.join([f"<div class='sb'><span class='sl'>{rt(t)}</span><div class='sb2'><div class='sbf' style='width:{rt(t)}%'></div></div><span class='sn'>{fl(t)}</span><span style='font-size:0.6rem;color:#aaa;margin-left:4px;'>{cn(t)}</span></div>" for t in all_t])

gs_c=72; r32_c=16; r16_c=8; qf_c=4; sf_c=2; f_c=2

CSS="""*{margin:0;padding:0;box-sizing:border-box;}body{font-family:"Noto Sans HK",sans-serif;background:#080810;color:#f0f0f5;padding:12px;}.wrap{max-width:1200px;margin:0 auto;}.hero{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #FFD700;border-radius:14px;padding:22px;text-align:center;margin-bottom:16px;}.hero h1{font-size:1.8rem;color:#FFD700;margin-bottom:4px;}.hero p{color:#8888a0;font-size:0.75rem;margin-top:4px;}.cd{margin-top:12px;display:flex;justify-content:center;gap:14px;flex-wrap:wrap;}.cdi{text-align:center;}.cdn{font-size:1.3rem;font-weight:700;color:#FFD700;}.cdl{font-size:0.5rem;color:#8888a0;text-transform:uppercase;}.stats{display:flex;gap:6px;margin-bottom:16px;}.sc{flex:1;background:#16161d;border:1px solid #2a2a3a;border-radius:8px;padding:8px;text-align:center;}.sc:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(255,215,0,0.15);}.scn{font-size:1rem;font-weight:700;color:#FFD700;}.scl{font-size:0.5rem;color:#8888a0;}.tab-nav{display:flex;gap:4px;margin-bottom:14px;flex-wrap:wrap;}.tab{background:#16161d;border:1px solid #2a2a3a;color:#f0f0f5;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:0.75rem;transition:all 0.2s;}.tab:hover{background:#2a2a3a;border-color:#FFD700;}.tab.active{background:#FFD700;color:#000;font-weight:700;}.content{display:none;}.content.show{display:block;}h2{font-size:0.9rem;color:#FFD700;margin:18px 0 8px;border-bottom:1px solid #2a2a3a;padding-bottom:4px;}.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px;margin-bottom:20px;}.gc{background:#16161d;border:1px solid #2a2a3a;border-radius:10px;overflow:hidden;}.gc:hover{border-color:#FFD700;transform:translateY(-2px);}.gh{background:linear-gradient(90deg,#2a2a3a,#1a1a2e);padding:6px 10px;font-weight:700;font-size:0.75rem;color:#FFD700;}.gt{width:100%;border-collapse:collapse;font-size:0.62rem;}.gt th{text-align:left;padding:4px 6px;color:#8888a0;border-bottom:1px solid #2a2a3a;}.gt td{padding:4px 6px;border-bottom:1px solid #1a1a2e;}.str{color:#888;font-size:0.7em;margin-left:3px;}.rf{display:flex;gap:3px;margin-top:3px;flex-wrap:wrap;}.rf span{font-size:0.55rem;padding:1px 4px;border-radius:3px;font-weight:600;}.rfw{background:rgba(74,222,128,0.3);color:#4ade80;}.rfl{background:rgba(248,113,113,0.3);color:#f87171;}.rfd{background:rgba(148,148,160,0.3);color:#888;}.rfup{background:rgba(255,215,0,0.2);color:#FFD700;}.rfnil{font-size:0.55rem;color:#555;}.mr{margin-top:4px;}.mteam{line-height:1.3;}.ml{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.md{background:#FFD700;color:#000;font-size:0.7rem;font-weight:700;padding:5px 12px;border-radius:5px;margin:14px 0 6px;}.mc{background:#16161d;border:1px solid #2a2a3a;border-radius:10px;overflow:hidden;transition:all 0.2s;}.mc:hover{border-color:#FFD700;transform:translateY(-1px);}.mhd{display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:#1a1a2e;border-bottom:1px solid #2a2a3a;gap:6px;flex-wrap:wrap;}.mcomp{font-size:0.65rem;font-weight:700;color:#FFD700;}.mhkt{font-size:0.6rem;color:#FFD700;}.mvenue{font-size:0.6rem;color:#8888a0;}.mbody{display:flex;align-items:center;padding:12px;gap:10px;flex-wrap:wrap;}.mteam{flex:1;font-size:0.85rem;font-weight:600;min-width:80px;}.mscore{font-size:1.4rem;font-weight:700;color:#FFD700;padding:0 12px;white-space:nowrap;}.mfoot{padding:6px 10px;border-top:1px solid #2a2a3a;}.mbar{display:flex;height:20px;border-radius:4px;overflow:hidden;gap:2px;margin-bottom:4px;}.mp{background:rgba(74,222,128,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpd{background:rgba(148,148,160,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpa{background:rgba(248,113,113,0.6);display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mxg{font-size:0.58rem;color:#8888a0;}.sd{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:20px;}.sb{display:flex;align-items:center;gap:6px;}.sl{font-size:0.65rem;color:#8888a0;width:32px;text-align:right;}.sb2{flex:1;height:16px;background:#1a1a2e;border-radius:3px;overflow:hidden;}.sbf{height:100%;background:linear-gradient(90deg,#FFD700,#e94560);border-radius:3px;}.sn{font-size:0.65rem;color:#FFD700;font-weight:700;width:16px;}.ft{text-align:center;padding:16px 0;color:#8888a0;font-size:0.6rem;border-top:1px solid #2a2a3a;margin-top:20px;}@media(max-width:600px){.hero{padding:14px}.hero h1{font-size:1.4rem}.tab{padding:6px 10px;font-size:0.7rem}.mscore{font-size:1.1rem}.mteam{font-size:0.75rem}.gg{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}}"""

html=f"""<!DOCTYPE html>
<html lang='zh-HK'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width,initial-scale=1.0'>
<title>🏆 FIFA 世界盃 2026 - 104場完整賽程</title>
<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+HK:wght@300;400;500;600;700&display=swap' rel='stylesheet'>
<style>{CSS}</style>
</head>
<body>
<div class='wrap'>
<div class='hero'>
<h1>🏆 FIFA 世界盃 2026</h1>
<p>6月11日 - 7月19日 | 美國 🇺🇸 / 加拿大 🇨🇦 / 墨西哥 🇲🇽</p>
<div class='cd'>
<div class='cdi'><div class='cdn'>{days_to_go}</div><div class='cdl'>Days</div></div>
<div class='cdi'><div class='cdn'>48</div><div class='cdl'>Teams</div></div>
<div class='cdi'><div class='cdn'>104</div><div class='cdl'>Matches</div></div>
<div class='cdi'><div class='cdn'>16</div><div class='cdl'>Cities</div></div>
</div>
</div>
<div class='stats'>
<div class='sc'><div class='scn'>{gs_c}</div><div class='scl'>分組</div></div>
<div class='sc'><div class='scn'>{r32_c}</div><div class='scl'>32強</div></div>
<div class='sc'><div class='scn'>{r16_c}</div><div class='scl'>16強</div></div>
<div class='sc'><div class='scn'>{qf_c}</div><div class='scl'>8強</div></div>
<div class='sc'><div class='scn'>{sf_c+f_c}</div><div class='scl'>決賽</div></div>
</div>
<div class='tab-nav'>
<button class='tab active' onclick="showTab('groups')">📊 48隊 + 實力</button>
<button class='tab' onclick="showTab('schedule')">📅 104場賽程</button>
<button class='tab' onclick="showTab('strength')">📈 實力分佈</button>
</div>
<div id='groups' class='content show'>
<h2>📊 12個小組 · 48支球隊</h2>
<div class='gg'>{''.join(gh)}</div>
</div>
<div id='schedule' class='content'>
<h2>📅 完整104場賽程 · 含預測比分 / xG / HK時間</h2>
<div class='ml'>{''.join(mm)}</div>
</div>
<div id='strength' class='content'>
<h2>📈 實力分佈（48支球隊）</h2>
<div class='sd'>{sd}</div>
</div>
<div class='ft'>Updated: {today} | Generated by Hanni 🐰</div>
</div>
<script>function showTab(tab){{document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.content').forEach(c=>c.classList.remove('show'));document.querySelectorAll('.tab').forEach(t=>{{if(t.getAttribute('onclick').includes(tab))t.classList.add('active');}});document.getElementById(tab).classList.add('show');}}</script>
</body>
</html>"""

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"OK! Generated 104 matches HTML")
print(f"File size: {len(html)} bytes")
print(f"Match count: {len(ALL_MATCHES)}")