#!/usr/bin/env python3
"""World Cup 2026 Dashboard Generator - Full 104 Matches + Recent Form + Real Results"""
from datetime import date, datetime
import random, json, os

# Load real match results (fetched from worldcup26.ir)
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'real_results.json')
try:
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        REAL_DATA = json.load(f)
    REAL_RESULTS = REAL_DATA.get('matches', {})
    FETCHED_AT = REAL_DATA.get('fetched_at', 'N/A')
except:
    REAL_RESULTS = {}
    FETCHED_AT = 'N/A'

def get_real_result(match_id):
    """Get actual result for a match ID (1-indexed from ALL_MATCHES)"""
    # match_id is 1-indexed position in ALL_MATCHES
    # worldcup26.ir uses string IDs like '1', '2', etc.
    return REAL_RESULTS.get(str(match_id), {})

def calc_real_standings():
    """Calculate group standings from REAL_RESULTS"""
    standings = {g: {} for g in 'ABCDEFGHIJKL'}
    
    for match_id, m in REAL_RESULTS.items():
        if not m.get('finished'): continue
        g = m.get('group', '')
        if g not in standings: continue
        
        home = m.get('home_team', '')
        away = m.get('away_team', '')
        hs = m.get('home_score', 0) or 0
        as_ = m.get('away_score', 0) or 0
        
        # Initialize if needed
        for t in [home, away]:
            if t not in standings[g]:
                standings[g][t] = {'pts': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'P': 0}
            standings[g][t]['P'] += 1  # Played
        
        # Update scores for home team
        if home in standings[g]:
            standings[g][home]['GF'] += hs
            standings[g][home]['GA'] += as_
            if hs > as_:
                standings[g][home]['pts'] += 3
                standings[g][home]['W'] += 1
            elif hs == as_:
                standings[g][home]['pts'] += 1
                standings[g][home]['D'] += 1
            else:
                standings[g][home]['L'] += 1
        
        # Update scores for away team
        if away in standings[g]:
            standings[g][away]['GF'] += as_
            standings[g][away]['GA'] += hs
            if as_ > hs:
                standings[g][away]['pts'] += 3
                standings[g][away]['W'] += 1
            elif as_ == hs:
                standings[g][away]['pts'] += 1
                standings[g][away]['D'] += 1
            else:
                standings[g][away]['L'] += 1
    
    return standings

REAL_STANDINGS = calc_real_standings()


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
    if m_num == 6 and 28 <= d_num <= 30: return 'R32'
    if m_num == 7 and d_num <= 3: return 'R32'
    if m_num == 7 and 4 <= d_num <= 7: return 'R16'
    if m_num == 7 and 9 <= d_num <= 11: return 'QF'
    if m_num == 7 and 14 <= d_num <= 15: return 'SF'
    if m_num == 7 and d_num == 18: return '3RD'
    return 'FNL'

def conf(h,a):
    d=abs(h-a)
    if d>=20: return 'high','🟢'
    if d>=10: return 'medium','🟡'
    return 'low','🔴'

KP={
    'France':'麥巴比','England':'哈利卡尼','Brazil':'尼馬','Germany':'湯馬斯穆勒',
    'Spain':'柏迪','Argentina':'美斯','Portugal':'C朗','Netherlands':'迪莊',
    'Belgium':'迪布尼','Croatia':'摩迪','Uruguay':'科斯塔','Colombia':'占美利斯',
    'Italy':'派路','Mexico':'Chicarito','USA':'達斯','Denmark':'艾歷臣',
    'Senegal':'沙迪文尼','Morocco':'夏約頓','Japan':'久保建英','Australia':'馬田',
    'Switzerland':'格列沙卡','Poland':'利雲','Sweden':'伊巴','Austria':'阿拉度',
    'Algeria':'馬列斯','Ecuador':'華倫西亞','Ivory Coast':'哈拿','Egypt':'沙拿',
    'Ghana':'奧巴美揚','Paraguay':'巴里奧斯','South Korea':'孫興慜',
    'Saudi Arabia':'達瓦沙利','Qatar':'阿費夫','Iran':'阿茲蒙',
    'Canada':'戴維斯','Tunisia':'卡斯里','Turkey':'杜辛',
    'Scotland':'阿當斯','Norway':'夏蘭特','Czechia':'舒希克',
    'Bosnia Herz':'比卡錫','New Zealand':'伍德',
}

def kp(team):
    if team not in KP: return ''
    return f"<span class='kp'>⭐ {KP[team]}</span>"

def mc_prob(g, n=3000):
    scores = {t: 0 for t in GD[g]}
    for _ in range(n):
        pts = {t: 0 for t in GD[g]}
        for i in range(4):
            for j in range(i+1, 4):
                h, a = GD[g][i], GD[g][j]
                hs, as_ = rt(h), rt(a)
                hp, dp, ap_ = prob(hs, as_)
                r = random.random() * 100
                if r < hp: pts[h] += 3
                elif r < hp + dp: pts[h] += 1; pts[a] += 1
                else: pts[a] += 3
        sorted_pts = sorted(pts.items(), key=lambda x: -x[1])
        for rank, (t, _) in enumerate(sorted_pts[:2]):
            scores[t] += 1
    return {t: round(scores[t]/n*100) for t in GD[g]}

# ---- Full tournament Monte Carlo (捧盃概率) ----


def resolve_r16():
    """Simulate R16 matchups based on group results. Returns dict of match_key -> winner."""
    winners = {}
    # Groups A-L: top 2 advance
    for g in 'ABCDEFGHIJKL':
        pts = {t: 0 for t in GD[g]}
        for i in range(4):
            for j in range(i+1, 4):
                h, a = GD[g][i], GD[g][j]
                hs, as_ = rt(h), rt(a)
                hp, dp, ap_ = prob(hs, as_)
                r = random.random() * 100
                if r < hp: pts[h] += 3
                elif r < hp + dp: pts[h] += 1; pts[a] += 1
                else: pts[a] += 3
        sorted_pts = sorted(pts.items(), key=lambda x: (-x[1], -rt(x[0])))
        winners[f'G{g}1'] = sorted_pts[0][0]
        winners[f'G{g}2'] = sorted_pts[1][0]
    
    # R16 bracket (M49-M56)
    r16_matches = [
        ('G1A1','G1A2'),('G1A3','G1A4'),  # M49: A1 vs A2, A3 vs A4  (invalid - fix)
    ]
    # Real bracket based on WC2026 structure:
    # M49: 1A vs 2B(C/D/E/F) depends on bracket
    # Simplified: pair group winners vs runners-up from adjacent groups
    r16_pairings = [
        ('G1A1','G2A2'),   # M49
        ('G3A1','G4A2'),   # M50
        ('G5A1','G6A2'),   # M51
        ('G7A1','G8A2'),   # M52
        ('G2A1','G1A2'),   # M53
        ('G4A1','G3A2'),   # M54
        ('G6A1','G5A2'),   # M55
        ('G8A1','G7A2'),   # M56
    ]
    results = {}
    for i, (h, a) in enumerate(r16_pairings):
        ht = winners.get(h, h)
        at = winners.get(a, a)
        if ht in TBD or at in TBD:
            results[f'M{49+i}'] = None
            continue
        hs, as_ = rt(ht), rt(at)
        hp, dp, ap_ = prob(hs, as_)
        r = random.random() * 100
        if r < hp: results[f'M{49+i}'] = ht
        elif r < hp + dp:
            results[f'M{49+i}'] = ht if random.random() < 0.5 else at
        else: results[f'M{49+i}'] = at
    return results

def mc_tournament(n=10000):
    """Run n full tournament simulations. Returns dict with stage advancement counts."""
    stage_counts = {t: {'GS':0,'R16':0,'QF':0,'SF':0,'FNL':0,'WIN':0} for t in sum(GD.values(), [])}
    
    for _ in range(n):
        # --- Group Stage ---
        group_standings = {}
        for g in 'ABCDEFGHIJKL':
            pts = {t: 0 for t in GD[g]}
            for i in range(4):
                for j in range(i+1, 4):
                    h, a = GD[g][i], GD[g][j]
                    hs, as_ = rt(h), rt(a)
                    hp, dp, ap_ = prob(hs, as_)
                    r = random.random() * 100
                    if r < hp: pts[h] += 3
                    elif r < hp + dp: pts[h] += 1; pts[a] += 1
                    else: pts[a] += 3
            sorted_pts = sorted(pts.items(), key=lambda x: (-x[1], -rt(x[0])))
            group_standings[g] = [t for t,_ in sorted_pts]
            for rank, t in enumerate(sorted_pts[:2]):
                stage_counts[t[0]]['GS'] += 1
                if rank == 0: stage_counts[t[0]]['R16'] += 1
        
        # --- R16 ---
        # Standard WC2026 bracket: A/B/C/D on one side, E/F/G/H on other
        # 1A vs 2B, 1C vs 2D, 1E vs 2F, 1G vs 2H, 1B vs 2A, 1D vs 2C, 1F vs 2E, 1H vs 2G
        r16_pairings = [
            (0, 1),   # M49: 1A vs 2B
            (2, 3),   # M50: 1C vs 2D
            (4, 5),   # M51: 1E vs 2F
            (6, 7),   # M52: 1G vs 2H
            (1, 0),   # M53: 1B vs 2A
            (3, 2),   # M54: 1D vs 2C
            (5, 4),   # M55: 1F vs 2E
            (7, 6),   # M56: 1H vs 2G
        ]
        group_order = list('ABCDEFGH')
        r16_winners = []
        for i, j in r16_pairings:
            ga, gb = group_order[i], group_order[j]
            ht = group_standings[ga][0]  # group winner
            at = group_standings[gb][1]   # runner-up
            if ht in TBD or at in TBD:
                r16_winners.append(None); continue
            hs, as_ = rt(ht), rt(at)
            hp, dp, ap_ = prob(hs, as_)
            r = random.random() * 100
            winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
            r16_winners.append(winner)
            stage_counts[winner]['QF'] += 1
        
        # --- QF ---
        qf_pairings = [(0,1),(2,3),(4,5),(6,7)]
        qf_winners = []
        for i, j in qf_pairings:
            ht = r16_winners[i]
            at = r16_winners[j]
            if not ht or not at:
                qf_winners.append(None); continue
            hs, as_ = rt(ht), rt(at)
            hp, dp, ap_ = prob(hs, as_)
            r = random.random() * 100
            winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
            qf_winners.append(winner)
            stage_counts[winner]['SF'] += 1
        
        # --- SF ---
        sf_pairings = [(0,1),(2,3)]
        sf_winners = []
        for i, j in sf_pairings:
            ht = qf_winners[i]
            at = qf_winners[j]
            if not ht or not at:
                sf_winners.append(None); continue
            hs, as_ = rt(ht), rt(at)
            hp, dp, ap_ = prob(hs, as_)
            r = random.random() * 100
            winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
            sf_winners.append(winner)
            stage_counts[winner]['FNL'] += 1
        
        # --- Final + 3rd ---
        for i, j in [(0,1)]:
            ht = sf_winners[i]
            at = sf_winners[j]
            if ht and at:
                hs, as_ = rt(ht), rt(at)
                hp, dp, ap_ = prob(hs, as_)
                r = random.random() * 100
                winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
                stage_counts[winner]['WIN'] += 1
    
    return {t: {s: round(c/n*100, 1) for s, c in counts.items()} for t, counts in stage_counts.items()}

R16=[('7月4日','W37','W38','13:00','Houston'),('7月4日','W41','W42','17:00','Philadelphia'),('7月5日','W39','W40','22:00','New York'),('7月5日','W43','W44','02:00','Mexico City'),('7月6日','W45','W46','15:00','Dallas'),('7月6日','W47','W48','20:00','Seattle'),('7月7日','W49','W50','04:00','Atlanta'),('7月7日','W51','W52','16:00','Vancouver')]
QF=[('7月9日','QF1-W','QF1-L','22:00','Boston'),('7月10日','QF2-W','QF2-L','15:00','Los Angeles'),('7月11日','QF3-W','QF3-L','17:00','Miami'),('7月11日','QF4-W','QF4-L','21:00','Kansas City')]
SF=[('7月14日','SF1-W','SF1-L','15:00','Dallas'),('7月15日','SF2-W','SF2-L','15:00','Atlanta')]
TD=[('7月18日','Semi1-L','Semi2-L','17:00','Miami')]
FN=[('7月19日','Final-W1','Final-W2','15:00','New York')]

def bm(d,h,a,et,city,lbl):
    hk=str(int(et.split(':')[0])+13).zfill(2)+':'+et.split(':')[1]
    nd=int(et.split(':')[0])+13>=24
    if nd: hk=str(int(et.split(':')[0])+13-24).zfill(2)+':'+et.split(':')[1]
    pl=' (+1)' if nd else ''
    if h in TBD or a in TBD: return "<div class='bmc tbd'><div class='bmtop'><span class='bmlbl'>"+lbl+"</span><span class='bmhk'> "+hk+" HK"+pl+"</span></div><div class='bmteams'><span class='bmtbd'>TBD</span></div></div>"
    hs,as_=rt(h),rt(a); hp,dp,ap_=prob(hs,as_); hsc,asc=score(hs,as_); cf,cfi=conf(hs,as_)
    return "<div class='bmc'><div class='bmtop'><span class='bmlbl'>"+lbl+"</span><span class='conf "+cf+"'>"+cfi+"</span><span class='bmhk'> "+hk+" HK"+pl+"</span></div><div class='bmteams'><div class='btm'>"+fl(h)+" "+cn(h)+" <span class='str'>"+str(hs)+"</span></div><div class='bscore'>"+str(hsc)+" - "+str(asc)+"</div><div class='btm'>"+fl(a)+" "+cn(a)+" <span class='str'>"+str(as_)+"</span></div></div><div class='bmbot'><div class='bmbbar'><div class='bmp' style='width:"+str(hp)+"%'><span>"+str(round(hp))+"%</span></div><div class='bmd' style='width:"+str(dp)+"%'><span>"+str(round(dp))+"%</span></div><div class='bma' style='width:"+str(ap_)+"%'><span>"+str(round(ap_))+"%</span></div></div></div></div>"

def gen_b():
    # Run one full bracket simulation to get real team names for gen_b() output
    # --- Group Stage ---
    group_standings = {}
    for g in 'ABCDEFGHIJKL':
        pts = {t: 0 for t in GD[g]}
        for i in range(4):
            for j in range(i+1, 4):
                h, a = GD[g][i], GD[g][j]
                hs, as_ = rt(h), rt(a)
                hp, dp, ap_ = prob(hs, as_)
                r = random.random() * 100
                if r < hp: pts[h] += 3
                elif r < hp + dp: pts[h] += 1; pts[a] += 1
                else: pts[a] += 3
        sorted_pts = sorted(pts.items(), key=lambda x: (-x[1], -rt(x[0])))
        group_standings[g] = [t for t,_ in sorted_pts]

    # --- R16 ---
    r16_pairings = [
        (0, 1),   # M49: 1A vs 2B
        (2, 3),   # M50: 1C vs 2D
        (4, 5),   # M51: 1E vs 2F
        (6, 7),   # M52: 1G vs 2H
        (1, 0),   # M53: 1B vs 2A
        (3, 2),   # M54: 1D vs 2C
        (5, 4),   # M55: 1F vs 2E
        (7, 6),   # M56: 1H vs 2G
    ]
    group_order = list('ABCDEFGH')
    r16_winners = []
    r16_teams = []
    for i, j in r16_pairings:
        ga, gb = group_order[i], group_order[j]
        ht = group_standings[ga][0]
        at = group_standings[gb][1]
        r16_teams.append((ht, at))
        hs, as_ = rt(ht), rt(at)
        hp, dp, ap_ = prob(hs, as_)
        r = random.random() * 100
        winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
        r16_winners.append(winner)

    # --- QF ---
    qf_pairings = [(0,1),(2,3),(4,5),(6,7)]
    qf_winners = []
    qf_teams = []
    for i, j in qf_pairings:
        ht = r16_winners[i]; at = r16_winners[j]
        qf_teams.append((ht, at))
        hs, as_ = rt(ht), rt(at)
        hp, dp, ap_ = prob(hs, as_)
        r = random.random() * 100
        winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
        qf_winners.append(winner)

    # --- SF ---
    sf_pairings = [(0,1),(2,3)]
    sf_winners = []
    sf_teams = []
    sf_losers = []
    for i, j in sf_pairings:
        ht = qf_winners[i]; at = qf_winners[j]
        sf_teams.append((ht, at))
        hs, as_ = rt(ht), rt(at)
        hp, dp, ap_ = prob(hs, as_)
        r = random.random() * 100
        winner = ht if r < hp else (at if r >= hp+dp else (ht if random.random()<0.5 else at))
        sf_winners.append(winner)
        sf_losers.append(at if winner == ht else ht)

    # --- Final + 3rd place ---
    fn_teams = [(sf_losers[0], sf_losers[1]), (sf_winners[0], sf_winners[1])]

    h='<div class="bracket"><div class="bround"><h3>16強</h3><div class="bgrid">'
    for i,m in enumerate(R16):
        ht, at = r16_teams[i] if i < len(r16_teams) else (m[1], m[2])
        h+=bm(m[0],ht,at,m[3],m[4],'M'+str(i+49))
    h+='</div></div><div class="bround"><h3>8強</h3><div class="bgrid">'
    for i,m in enumerate(QF):
        ht, at = qf_teams[i] if i < len(qf_teams) else (m[1], m[2])
        h+=bm(m[0],ht,at,m[3],m[4],'QF'+str(i+1))
    h+='</div></div><div class="bround"><h3>準決</h3><div class="bgrid">'
    for i,m in enumerate(SF):
        ht, at = sf_teams[i] if i < len(sf_teams) else (m[1], m[2])
        h+=bm(m[0],ht,at,m[3],m[4],'SF'+str(i+1))
    h+='</div></div><div class="bround finals"><h3>決賽</h3><div class="bgrid finals-grid">'
    for i, m in enumerate(TD):
        ht, at = fn_teams[i] if i < len(fn_teams) else (m[1], m[2])
        h+=bm(m[0],ht,at,m[3],m[4],'季軍')
    for i, m in enumerate(FN):
        ht, at = fn_teams[len(TD)+i] if len(TD)+i < len(fn_teams) else (m[1], m[2])
        h+=bm(m[0],ht,at,m[3],m[4],'決賽')
    h+='</div></div></div>'
    return h

SN={'GS':'分組','R32':'32強','R16':'16強','QF':'8強','SF':'準決','3RD':'季軍','FNL':'決賽'}
IC={'GS':'📅','R32':'🎯','R16':'⚡','QF':'🔥','SF':'🏆','3RD':'🥉','FNL':'🏆'}

# Trophy probability
print('Running 10000 tournament simulations for trophy probability...')
TROPHY = mc_tournament(10000)

# Group qualified 2nd place helpers for R16 lookup
def g2_str(g):
    """Get 2nd place team name from group g based on current ratings."""
    pts = {t: 0 for t in GD[g]}
    for i in range(4):
        for j in range(i+1, 4):
            h, a = GD[g][i], GD[g][j]
            hs, as_ = rt(h), rt(a)
            hp, dp, ap_ = prob(hs, as_)
            r = random.random() * 100
            if r < hp: pts[h] += 3
            elif r < hp + dp: pts[h] += 1; pts[a] += 1
            else: pts[a] += 3
    sorted_pts = sorted(pts.items(), key=lambda x: (-x[1], -rt(x[0])))
    return sorted_pts[1][0]

today=date.today().strftime('%Y-%m-%d')
days_to_go=max(0,(date(2026,6,11)-date.today()).days)

NEXT_DATE=datetime(2026,6,11,15,0)
now=datetime.now()
d2=NEXT_DATE-now
if d2.total_seconds()>0:
    cdown=f"{d2.days}日{d2.seconds//3600}時{(d2.seconds%3600)//60}分"
else:
    cdown="進行中！" 

mc_cache={}
for g in 'ABCDEFGHIJKL':
    mc_cache[g]=mc_prob(g,3000)

gh=[]
for g in 'ABCDEFGHIJKL':
    qps=mc_cache[g]
    ts=GD[g]
    rows=[]
    for t in sorted(ts,key=lambda x:-rt(x)):
        # Get real standings if available
        rs = REAL_STANDINGS.get(g, {}).get(t, {})
        p = rs.get('P', 0)
        w = rs.get('W', 0)
        d = rs.get('D', 0)
        l = rs.get('L', 0)
        pts = rs.get('pts', 0)
        if p == 0:
            p_str = w_str = d_str = l_str = pts_str = "—"
        else:
            p_str = str(p)
            w_str = str(w)
            d_str = str(d)
            l_str = str(l)
            pts_str = str(pts)
        rows.append(f"<tr><td>{fl(t)} {cn(t)}</td><td style='text-align:center;font-size:0.65rem;'>{rt(t)}</td><td style='text-align:center;font-size:0.65rem;'>{p_str}</td><td style='text-align:center;font-size:0.65rem;'>{w_str}</td><td style='text-align:center;font-size:0.65rem;'>{d_str}</td><td style='text-align:center;font-size:0.65rem;'>{l_str}</td><td style='text-align:right;'><span style='font-weight:700;color:#FFD700;'>{pts_str}</span></td><td style='text-align:center;font-size:0.55rem;color:#888;'>{qps.get(t,'-')}</td></tr>")
    gh.append(f"<div class='gc'><div class='gh'>組 {g}</div><table class='gt'><thead><tr><th>球隊</th><th style='text-align:center'>實力</th><th style='text-align:center'>賽</th><th style='text-align:center'>勝</th><th style='text-align:center'>和</th><th style='text-align:center'>負</th><th style='text-align:right'>分</th><th style='text-align:center'>出線%</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>")

chan_map={'Mexico City':'Now618','Guadalajara':'Now 618','Toronto':'Now638','Los Angeles':'Now 638','San Francisco':'Now 638','New York':'Now638','Boston':'Now 638','Vancouver':'Now638','Houston':'Now 638','Philadelphia':'Now 638','Dallas':'Now 638','Monterrey':'Now 638','Atlanta':'Now 638','Seattle':'Now 638','Miami':'Now 638','Kansas City':'Now 638'}

# --- Accuracy tracking ---
acc_correct = 0   # exact score
acc_winner = 0   # correct winner/draw
acc_total = 0    # total finished matches

mm=[]
cur=''
for idx, m in enumerate(ALL_MATCHES):
    day,h,a,et,city=m
    hk,nd=et_to_hk(et)
    plus=' (+1)' if nd else ''
    st=stage_of(day)
    lbl=SN[st]
    icon=IC[st]
    if day!=cur:
        mm.append(f"<div class='md' data-stage='{st}'>{icon} {day} <span style='font-size:0.65rem;color:#888;margin-left:6px;'>({lbl})</span></div>")
        cur=day
    if h in TBD or a in TBD:
        mm.append(f"<div class='mc' data-stage='{st}' data-home='{h}' data-away='{a}'><div class='mhd'><span class='mcomp'>{lbl} </span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span></div><div class='mbody' style='justify-content:center;'><span style='color:#888;font-size:0.75rem;'>⚠️ 待定 - 分組賽後揭曉</span></div></div>")
    else:
        hs,as_=rt(h),rt(a)
        hp,dp,ap_=prob(hs,as_)
        xh,xa=xg(hs,as_)
        hsc,asc=score(hs,as_)
        cf_cls,cf_icon=conf(hs,as_)
        chan=chan_map.get(city,'Now TV')
        rf_h = get_recent_form_html(h)
        rf_a = get_recent_form_html(a)
        
        # Check for real result
        match_id = str(idx + 1)
        real = REAL_RESULTS.get(match_id, {})
        real_finished = real.get('finished', False)
        real_hs = real.get('home_score')
        real_as = real.get('away_score')
        
        # Build comparison HTML
        comparison_html = ''
        if real_finished and real_hs is not None and real_as is not None:
            acc_total += 1
            # Exact score?
            if real_hs == hsc and real_as == asc:
                acc_correct += 1
                acc_winner += 1
                badge = '<span class="pred-badge correct">✅ 完全估中！</span>'
                badge_cls = 'mc-correct'
            elif (real_hs > real_as) == (hsc > asc) or real_hs == hsc and real_as == asc:
                # Same winner (or both draw)
                acc_winner += 1
                badge = '<span class="pred-badge partial">🟡 估中勝方</span>'
                badge_cls = 'mc-partial'
            else:
                badge = '<span class="pred-badge wrong">❌ 估錯</span>'
                badge_cls = 'mc-wrong'
            comparison_html = f"""<div class='cmp'><div class='cmp-pred'><span class='cmpl'>預測</span><span class='cmpv'>{hsc}-{asc}</span></div><div class='cmp-arrow'>→</div><div class='cmp-real'><span class='cmpl'>實際</span><span class='cmpv'>{real_hs}-{real_as}</span></div><div class='cmp-badge'>{badge}</div></div>"""
            card_cls = f"mc {badge_cls}"
        else:
            card_cls = 'mc'
        
        mm.append(f"""<div class='{card_cls}' data-stage='{st}' data-home='{h}' data-away='{a}'><div class='mhd'><span class='mcomp'>{lbl} </span><span class='conf {cf_cls}'>{cf_icon}</span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span><span class='mchan'>📺 {chan}</span></div><div class='mbody'><div class='mteam'>{fl(h)} {cn(h)}<span class='str'>{hs}</span>{kp(h)}<div class='mr'>{rf_h}</div></div><div class='mscore'>{hsc}⚽{asc}</div><div class='mteam'>{fl(a)} {cn(a)}<span class='str'>{as_}</span>{kp(a)}<div class='mr'>{rf_a}</div></div>{comparison_html}<div class='mfoot'><div class='mbar'><div class='mp' style='width:{hp:.0f}%'><span>H{hp:.0f}%</span></div><div class='mpd' style='width:{dp:.0f}%'><span>D{dp:.0f}%</span></div><div class='mpa' style='width:{ap_:.0f}%'><span>A{ap_:.0f}%</span></div></div><div class='mxg'>xG {xh}-{xa} | O{int(xh+xa+0.5)} | ⚽{int(xh+xa+0.5)}球</div></div></div>""")

all_t=[]
for ts in GD.values(): all_t.extend(ts)
all_t.sort(key=lambda t:-rt(t))
sd=''.join([f"<div class='sb'><span class='sl'>{rt(t)}</span><div class='sb2'><div class='sbf' style='width:{rt(t)}%'></div></div><span class='sn'>{fl(t)}</span><span style='font-size:0.6rem;color:#aaa;margin-left:4px;'>{cn(t)}</span></div>" for t in all_t])

# Trophy standings - sort by WIN%
trophy_sorted = sorted(TROPHY.items(), key=lambda x: -x[1]['WIN'])

# Build trophy HTML - top 16 with full stage breakdown
trophy_rows = []
for rank, (t, stages) in enumerate(trophy_sorted[:16]):
    win_p = stages['WIN']
    final_p = stages['FNL']
    sf_p = stages['SF']
    qf_p = stages['QF']
    r16_p = stages['R16']
    gs_p = stages['GS']
    bar = f"""<div class='tpbar'><div class='tpw' style='width:{win_p*3:.0f}%'></div><div class='tpf' style='width:{(final_p-win_p)*3:.0f}%'></div><div class='tps' style='width:{(sf_p-final_p)*3:.0f}%'></div><div class='tpq' style='width:{(qf_p-sf_p)*3:.0f}%'></div><div class='tpr' style='width:{(r16_p-qf_p)*3:.0f}%'></div></div>"""
    trophy_rows.append(f"""<tr>
        <td style='text-align:center;font-weight:700;color:#FFD700;'>{rank+1}</td>
        <td>{fl(t)} {cn(t)}</td>
        <td style='text-align:center;font-size:0.7rem;'>{rt(t)}</td>
        <td style='text-align:center;'><span class='tpc tw'>{win_p:.1f}%</span></td>
        <td style='text-align:center;'><span class='tpc tf'>{final_p:.1f}%</span></td>
        <td style='text-align:center;'><span class='tpc ts'>{sf_p:.1f}%</span></td>
        <td style='text-align:center;'><span class='tpc tq'>{qf_p:.1f}%</span></td>
        <td style='text-align:center;'><span class='tpc tr'>{r16_p:.1f}%</span></td>
        <td>{bar}</td>
    </tr>""")

trophy_table_html = ''.join(trophy_rows)

# Build medal table (top 8 by WIN%)
medal = []
for rank, (t, stages) in enumerate(trophy_sorted[:8]):
    win_p = stages['WIN']
    medal.append(f"""<div class='medal-card {'gold' if rank==0 else 'silver' if rank==1 else 'bronze'}'>
        <div class='mrank'>{'🥇' if rank==0 else '🥈' if rank==1 else '🥉'}</div>
        <div class='mflag'>{fl(t)}</div>
        <div class='mname'>{cn(t)}</div>
        <div class='mwin'>{win_p:.1f}%</div>
        <div class='msf'>{stages['FNL']:.1f}%</div>
    </div>""")
medal_html = ''.join(medal)

# Accuracy stats HTML
if acc_total > 0:
    exact_pct = acc_correct / acc_total * 100
    winner_pct = acc_winner / acc_total * 100
    acc_html = f"""<div class='acc-stats'>
    <div class='acc-item'>
        <div class='acc-val'>{acc_correct}/{acc_total}</div>
        <div class='acc-label'>✅ 完全估中</div>
        <div class='acc-pct'>{exact_pct:.0f}%</div>
    </div>
    <div class='acc-item'>
        <div class='acc-val'>{acc_winner}/{acc_total}</div>
        <div class='acc-label'>🟡 估中勝方</div>
        <div class='acc-pct'>{winner_pct:.0f}%</div>
    </div>
    <div class='acc-note'>📊 預測 vs 實際 · 數據更新: {FETCHED_AT[:16]}</div>
</div>"""
else:
    acc_html = "<div class='acc-stats'><div class='acc-note'>📊 世界盃 6月11日開始 · 預測即將揭曉！</div></div>"

gs_c=72; r32_c=16; r16_c=8; qf_c=4; sf_c=2; f_c=2

CSS="""*{margin:0;padding:0;box-sizing:border-box;}body{font-family:"Noto Sans HK",sans-serif;background:linear-gradient(160deg,#080812 0%,#0d0d1a 50%,#080812 100%);color:#f5f5f7;padding:12px;min-height:100vh;}.wrap{max-width:1200px;margin:0 auto;}.hero{background:linear-gradient(135deg,rgba(26,26,46,0.95),rgba(22,33,62,0.9));border:1px solid rgba(255,215,0,0.3);border-radius:18px;padding:24px;text-align:center;margin-bottom:16px;backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.05);position:relative;overflow:hidden;}.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at center,rgba(255,215,0,0.06) 0%,transparent 60%);pointer-events:none;}.hero h1{font-size:1.9rem;background:linear-gradient(135deg,#FFD700,#FF8C00,#FFD700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:4px;font-weight:800;letter-spacing:-0.5px;}.hero p{color:#9ca3af;font-size:0.78rem;margin-top:4px;}.cd{margin-top:14px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;}.cdi{text-align:center;padding:8px 16px;background:rgba(255,215,0,0.05);border-radius:12px;border:1px solid rgba(255,215,0,0.1);}.cdn{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}.cdl{font-size:0.5rem;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;}.ctd{font-size:0.6rem;color:#FF8C00;margin-top:4px;}.stats{display:flex;gap:6px;margin-bottom:16px;}.sc{flex:1;background:rgba(22,22,29,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:10px;text-align:center;cursor:pointer;backdrop-filter:blur(10px);transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}.sc:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(255,215,0,0.15);border-color:rgba(255,215,0,0.3);}.scn{font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}.scl{font-size:0.5rem;color:#9ca3af;}.tab-nav{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;}.tab{background:rgba(22,22,29,0.6);border:1px solid rgba(255,255,255,0.06);color:#9ca3af;padding:10px 16px;border-radius:50px;cursor:pointer;font-size:0.75rem;transition:all 0.3s;backdrop-filter:blur(10px);}.tab:hover{background:rgba(255,215,0,0.1);border-color:rgba(255,215,0,0.3);color:#FFD700;}.tab.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-weight:700;box-shadow:0 4px 16px rgba(255,215,0,0.3);}.content{display:none;}.content.show{display:block;}h2{font-size:0.95rem;color:#FFD700;margin:20px 0 10px;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:6px;font-weight:600;}.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin-bottom:20px;}.gc{background:rgba(22,22,29,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:14px;overflow:hidden;backdrop-filter:blur(10px);transition:all 0.3s;}.gc:hover{border-color:rgba(255,215,0,0.4);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3);}.gh{background:linear-gradient(90deg,rgba(42,42,58,0.9),rgba(26,26,46,0.9));padding:8px 12px;font-weight:700;font-size:0.75rem;color:#FFD700;border-bottom:1px solid rgba(255,255,255,0.04);}.gt{width:100%;border-collapse:collapse;font-size:0.62rem;}.gt th{text-align:left;padding:5px 8px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,0.04);font-weight:500;}.gt td{padding:5px 8px;border-bottom:1px solid rgba(255,255,255,0.02);}.str{color:#9ca3af;font-size:0.7em;margin-left:4px;}.rf{display:flex;gap:3px;margin-top:4px;flex-wrap:wrap;}.rf span{font-size:0.55rem;padding:2px 5px;border-radius:4px;font-weight:600;}.rfw{background:rgba(34,197,94,0.25);color:#22c55e;border:1px solid rgba(34,197,94,0.3);}.rfl{background:rgba(239,68,68,0.25);color:#ef4444;border:1px solid rgba(239,68,68,0.3);}.rfd{background:rgba(148,148,160,0.2);color:#9ca3af;}.rfup{background:rgba(255,215,0,0.15);color:#FFD700;}.rfnil{font-size:0.55rem;color:#555;}.mr{margin-top:4px;}.mteam{line-height:1.4;}.ml{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.md{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-size:0.72rem;font-weight:700;padding:6px 14px;border-radius:8px;margin:16px 0 8px;box-shadow:0 4px 12px rgba(255,215,0,0.2);}.md.hidden,.mc.hidden{display:none;}.mc{background:rgba(22,22,29,0.75);border:1px solid rgba(255,255,255,0.06);border-radius:14px;overflow:hidden;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);backdrop-filter:blur(12px);}.mc:hover{border-color:rgba(255,215,0,0.4);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3),0 0 20px rgba(255,215,0,0.08);}.mc.fav{border-color:rgba(255,215,0,0.5);box-shadow:0 0 20px rgba(255,215,0,0.2);}.mhd{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:rgba(26,26,46,0.6);border-bottom:1px solid rgba(255,255,255,0.04);gap:8px;flex-wrap:wrap;}.mcomp{font-size:0.65rem;font-weight:700;color:#FFD700;}.conf{font-size:0.6rem;padding:2px 8px;border-radius:50px;font-weight:600;margin-right:6px;}.conf.high{background:rgba(34,197,94,0.2);color:#22c55e;border:1px solid rgba(34,197,94,0.3);}.conf.medium{background:rgba(234,179,8,0.2);color:#eab308;border:1px solid rgba(234,179,8,0.3);}.conf.low{background:rgba(239,68,68,0.2);color:#ef4444;border:1px solid rgba(239,68,68,0.3);}.mhkt{font-size:0.6rem;color:#FF8C00;}.mvenue{font-size:0.6rem;color:#9ca3af;}.mbody{display:flex;align-items:center;padding:14px;gap:12px;flex-wrap:wrap;}.mteam{flex:1;font-size:0.88rem;font-weight:600;min-width:80px;}.mscore{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;padding:0 14px;white-space:nowrap;}.mfoot{padding:8px 12px;border-top:1px solid rgba(255,255,255,0.04);}.mbar{display:flex;height:22px;border-radius:6px;overflow:hidden;gap:2px;margin-bottom:4px;}.mp{background:linear-gradient(90deg,rgba(34,197,94,0.7),rgba(34,197,94,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpd{background:linear-gradient(90deg,rgba(148,148,160,0.7),rgba(148,148,160,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpa{background:linear-gradient(90deg,rgba(239,68,68,0.7),rgba(239,68,68,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mxg{font-size:0.58rem;color:#9ca3af;}.sd{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:20px;}.sb{display:flex;align-items:center;gap:6px;}.sl{font-size:0.65rem;color:#9ca3af;width:32px;text-align:right;}.sb2{flex:1;height:16px;background:rgba(26,26,46,0.8);border-radius:4px;overflow:hidden;}.sbf{height:100%;background:linear-gradient(90deg,#FFD700,#FF6B35,#FF4500);border-radius:4px;}.sn{font-size:0.65rem;color:#FFD700;font-weight:700;width:16px;}.ft{text-align:center;padding:20px 0;color:#9ca3af;font-size:0.6rem;border-top:1px solid rgba(255,255,255,0.04);margin-top:20px;}.sch-bar{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;align-items:center;}.sf-btn{background:rgba(22,22,29,0.6);border:1px solid rgba(255,255,255,0.06);color:#9ca3af;padding:6px 12px;border-radius:50px;cursor:pointer;font-size:0.7rem;transition:all 0.3s;backdrop-filter:blur(10px);}.sf-btn:hover{border-color:rgba(255,215,0,0.3);color:#FFD700;}.sf-btn.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-weight:700;box-shadow:0 4px 12px rgba(255,215,0,0.2);}.fav-filter.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;}.fav-filter{background:rgba(22,22,29,0.6);border:1px solid rgba(255,215,0,0.4);color:#FFD700;}.kp{font-size:0.55rem;color:#FF8C00;display:block;margin-top:3px;font-weight:500;}
.mr{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.medal-row{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;}.medal-card{flex:1;min-width:100px;background:rgba(22,22,29,0.8);border-radius:14px;padding:14px;text-align:center;border:1px solid rgba(255,255,255,0.06);transition:all 0.3s;}.medal-card.gold{border-color:rgba(255,215,0,0.5);background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(22,22,29,0.8));}.medal-card.silver{border-color:rgba(192,192,192,0.4);}.medal-card.bronze{border-color:rgba(205,127,50,0.4);}.medal-card:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.3);}.mrank{font-size:1.5rem;margin-bottom:6px;}.mflag{font-size:1.8rem;margin-bottom:4px;}.mname{font-size:0.72rem;font-weight:600;color:#f5f5f7;margin-bottom:6px;}.mwin{font-size:1.1rem;font-weight:800;color:#FFD700;}.msf{font-size:0.65rem;color:#9ca3af;}.trophy-legend{display:flex;gap:14px;margin-bottom:14px;flex-wrap:wrap;align-items:center;}.tpc{font-size:0.65rem;padding:2px 8px;border-radius:50px;font-weight:600;}.tw{background:rgba(255,215,0,0.2);color:#FFD700;}.tf{background:rgba(148,163,184,0.2);color:#c0c0c0;}.ts{background:rgba(239,68,68,0.2);color:#ef4444;}.tq{background:rgba(234,179,8,0.2);color:#eab308;}.tr{background:rgba(34,197,94,0.2);color:#22c55e;}.ttbl{width:100%;border-collapse:collapse;font-size:0.65rem;}.ttbl th{text-align:left;padding:8px 10px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,0.08);font-weight:500;}.ttbl td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,0.03);}.ttbl tr:hover td{background:rgba(255,215,0,0.05);}.tpbar{display:flex;height:10px;border-radius:5px;overflow:hidden;gap:1px;}.tpw{background:linear-gradient(90deg,#FFD700,#FF8C00);}.tpf{background:rgba(192,192,192,0.6);}.tps{background:rgba(239,68,68,0.6);}.tpq{background:rgba(234,179,8,0.6);}.tpr{background:rgba(34,197,94,0.6);}.mchan{font-size:0.55rem;color:#9ca3af;margin-left:6px;}.bracket{margin-top:10px;}.bround{margin-bottom:20px;}.bround h3{font-size:0.85rem;color:#FFD700;margin:0 0 10px;padding:6px 12px;background:rgba(255,215,0,0.1);border-radius:8px;border-left:3px solid #FFD700;}.bgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;}.bgrid.finals-grid{grid-template-columns:repeat(2,1fr);max-width:500px;}.bmc{background:rgba(22,22,29,0.8);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:12px;transition:all 0.3s;}.bmc:hover{border-color:rgba(255,215,0,0.4);box-shadow:0 4px 16px rgba(0,0,0,0.2);}.bmc.tbd{opacity:0.5;}.bmtop{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.04);}.bmlbl{font-size:0.7rem;font-weight:700;color:#FFD700;}.bmhk{font-size:0.6rem;color:#9ca3af;}.bmteams{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;}.btm{flex:1;font-size:0.8rem;font-weight:600;}.bscore{font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;padding:0 8px;white-space:nowrap;}.bmtbd{color:#666;font-size:0.8rem;}.bmbbar{display:flex;height:18px;border-radius:4px;overflow:hidden;gap:1px;}.bmp{flex:0 0 auto;background:linear-gradient(90deg,rgba(34,197,94,0.8),rgba(34,197,94,0.6));display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}.bmd{flex:0 0 auto;background:rgba(148,148,160,0.6);display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}.bma{flex:0 0 auto;background:linear-gradient(90deg,rgba(239,68,68,0.8),rgba(239,68,68,0.6));display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}
.bnav{display:none;position:fixed;bottom:0;left:0;right:0;background:rgba(13,13,26,0.95);backdrop-filter:blur(20px);border-top:1px solid rgba(255,215,0,0.2);padding:8px 0;padding-bottom:max(8px,env(safe-area-inset-bottom));z-index:1000;box-shadow:0 -4px 20px rgba(0,0,0,0.3);}.bni{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;background:none;border:none;color:#9ca3af;cursor:pointer;padding:4px 8px;transition:all 0.2s;}.bni.active{color:#FFD700;}.bni:hover{color:#FFD700;}.bne{font-size:1.3rem;}.bnl{font-size:0.55rem;font-weight:500;}
@media(max-width:600px){.bnav{display:flex;}.wrap{padding-bottom:70px;}}

/* Accuracy stats */
.acc-stats{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;justify-content:center;align-items:center;}
.acc-item{text-align:center;padding:6px 14px;background:rgba(22,22,29,0.7);border-radius:10px;border:1px solid rgba(255,255,255,0.06);}
.acc-val{font-size:1rem;font-weight:800;color:#FFD700;}
.acc-label{font-size:0.5rem;color:#9ca3af;margin-top:2px;}
.acc-pct{font-size:0.6rem;color:#22c55e;margin-top:2px;}
.acc-note{font-size:0.58rem;color:#888;padding:6px 10px;}

/* Prediction vs Actual comparison */
.cmp{display:flex;align-items:center;gap:8px;padding:6px 12px;background:rgba(0,0,0,0.3);border-radius:8px;margin:0 12px 8px;font-size:0.72rem;flex-wrap:wrap;}
.cmp-pred,.cmp-real{display:flex;flex-direction:column;align-items:center;gap:1px;}
.cmpl{font-size:0.5rem;color:#9ca3af;text-transform:uppercase;letter-spacing:0.5px;}
.cmpv{font-weight:800;font-size:1rem;}
.cmp-pred .cmpv{color:#FFD700;}
.cmp-real .cmpv{color:#22c55e;}
.cmp-arrow{color:#888;font-size:1.1rem;}
.cmp-badge{font-size:0.6rem;padding:2px 8px;border-radius:50px;margin-left:auto;}
.pred-badge{padding:2px 8px;border-radius:50px;font-size:0.6rem;font-weight:600;}
.correct{background:rgba(34,197,94,0.2);color:#22c55e;}
.partial{background:rgba(234,179,8,0.2);color:#eab308;}
.wrong{background:rgba(239,68,68,0.2);color:#ef4444;}

/* Match card states */
.mc-correct{border-color:rgba(34,197,94,0.4) !important;}
.mc-partial{border-color:rgba(234,179,8,0.3) !important;}
.mc-wrong{border-color:rgba(239,68,68,0.3) !important;}
.mc-correct:hover{border-color:rgba(34,197,94,0.6) !important;}
.mc-partial:hover{border-color:rgba(234,179,8,0.5) !important;}
.mc-wrong:hover{border-color:rgba(239,68,68,0.5) !important;}"""

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
<div class='cdi'><div class='cdn'>{cdown}</div><div class='ctd'>距離開幕</div></div>
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
{acc_html}
<div class='tab-nav'>
<button class='tab active' onclick="showTab('groups')">📊 48隊 + 實力</button>
<button class='tab' onclick="showTab('schedule')">📅 104場賽程</button>
<button class='tab' onclick="showTab('strength')">📈 實力分佈</button>
<button class='tab' onclick="showTab('bracket')">🏆 淘汰賽</button>
<button class='tab' onclick="showTab('trophy')">🏅 捧盃概率</button>
</div>
<div id='groups' class='content show'>
<h2>📊 12個小組 · 48支球隊</h2>
<div class='gg'>{''.join(gh)}</div>
</div>
<div id='schedule' class='content'>
<h2>📅 完整104場賽程 · 含預測比分 / xG / HK時間</h2>
<div class="sch-bar">
<select id="teamSearch" onchange="searchTeam(this.value)" style="background:#16161d;border:1px solid #2a2a3a;color:#f0f0f5;padding:6px 10px;border-radius:8px;font-size:0.75rem;flex:1;max-width:200px;appearance:auto;">
<option value="">🔍 搜索球隊...</option>
<option value='France'>🇫🇷 法國</option><option value='Argentina'>🇦🇷 阿根廷</option><option value='Spain'>🇪🇸 西班牙</option><option value='Brazil'>🇧🇷 巴西</option><option value='England'>🇬🇧 英格蘭</option><option value='Germany'>🇩🇪 德國</option><option value='Portugal'>🇵🇹 葡萄牙</option><option value='Netherlands'>🇳🇱 荷蘭</option><option value='Belgium'>🇧🇪 比利時</option><option value='Croatia'>🇭🇷 克羅地亞</option><option value='Uruguay'>🇺🇾 烏拉圭</option><option value='Colombia'>🇨🇴 哥倫比亞</option><option value='Mexico'>🇲🇽 墨西哥</option><option value='Morocco'>🇲🇦 摩洛哥</option><option value='USA'>🇺🇸 美國</option><option value='Senegal'>🇸🇳 塞內加爾</option><option value='Switzerland'>🇨🇭 瑞士</option><option value='Japan'>🇯🇵 日本</option><option value='Sweden'>🇸🇪 瑞典</option><option value='Austria'>🇦🇹 奧地利</option><option value='Australia'>🇦🇺 澳洲</option><option value='Ecuador'>🇪🇨 厄瓜多爾</option><option value='Ivory Coast'>🇨🇮 象牙海岸</option><option value='Egypt'>🇪🇬 埃及</option><option value='South Korea'>🇰🇷 南韓</option><option value='Algeria'>🇩🇿 阿爾及利亞</option><option value='Paraguay'>🇵🇾 巴拉圭</option><option value='Norway'>🇳🇴 挪威</option><option value='Ghana'>🇬🇭 加納</option><option value='Scotland'>🏴 蘇格蘭</option><option value='Iraq'>🇮🇶 伊拉克</option><option value='Turkey'>🇹🇷 土耳其</option><option value='Canada'>🇨🇦 加拿大</option><option value='Czechia'>🇨🇿 捷克</option><option value='Tunisia'>🇹🇳 突尼斯</option><option value='Iran'>🏴 伊朗</option><option value='Bosnia Herz'>🇧🇦 波斯尼亞</option><option value='Saudi Arabia'>🇸🇦 沙特阿拉伯</option><option value='Qatar'>🇶🇦 卡塔爾</option><option value='Uzbekistan'>🇺🇿 烏茲別克</option><option value='New Zealand'>🇳🇿 新西蘭</option><option value='Cape Verde'>🇨🇻 佛得角</option><option value='Panama'>🇵🇦 巴拿馬</option><option value='South Africa'>🇿🇦 南非</option><option value='DR Congo'>🇨🇩 剛果</option><option value='Jordan'>🇯🇴 約旦</option><option value='Curacao'>🇨🇼 庫拉索</option><option value='Haiti'>🇭🇹 海地</option>
</select>
<button class="sf-btn active" onclick="filterStage('all',this)">全部</button>
<button class="sf-btn" onclick="filterStage('GS',this)">📅 分組</button>
<button class="sf-btn" onclick="filterStage('R32',this)">🎯 32強</button>
<button class="sf-btn" onclick="filterStage('R16',this)">⚡ 16強</button>
<button class="sf-btn" onclick="filterStage('QF',this)">🔥 8強</button>
<button class="sf-btn" onclick="filterStage('SF',this)">🏆 決賽</button>
<button class="sf-btn fav-filter" onclick="toggleFavFilter(this)" style="margin-left:auto;">⭐ 我的最愛</button>
</div>
<div class='ml'>{''.join(mm)}</div>
</div>
<div id='bracket' class='content'>
<h2>🏆 淘汰賽 · 16強至決賽</h2>
{gen_b()}
</div>

<div id='trophy' class='content'>
<h2>🏅 捧盃概率 · 16強預測（10,000次模擬）</h2>
<div class='medal-row'>{medal_html}</div>
<div class='trophy-legend'>
<span><span class='tpc tw'>🏆 捧盃</span></span>
<span><span class='tpc tf'>🥚 入決賽</span></span>
<span><span class='tpc ts'>🔥 入準決</span></span>
<span><span class='tpc tq'>⚡ 入8強</span></span>
<span><span class='tpc tr'>🎯 入16強</span></span>
</div>
<table class='ttbl'>
<thead><tr><th style='width:30px;'>#</th><th>球隊</th><th style='width:40px;'>實力</th><th>🏆捧盃</th><th>🥚決賽</th><th>🔥準決</th><th>⚡8強</th><th>🎯16強</th><th style='width:200px;'>晉級線</th></tr></thead>
<tbody>{trophy_table_html}</tbody>
</table>
</div>

<div id='strength' class='content'>
<h2>📈 實力分佈（48支球隊）</h2>
<div class='sd'>{sd}</div>
</div>
<div class='ft'>Updated: {today} | Generated by Hanni 🐰</div>
</div>
<script>

function showTab(tab){{
  var ts=document.querySelectorAll(".tab");
  for(var i=0;i<ts.length;i++)ts[i].classList.remove("active");
  var cs=document.querySelectorAll(".content");
  for(var i=0;i<cs.length;i++)cs[i].classList.remove("show");
  var target = document.getElementById(tab);
  if(target) target.classList.add("show");
  document.getElementById(tab).classList.add("show");
}}
function filterStage(stage,btn){{
  var bs=document.querySelectorAll(".sf-btn");
  for(var i=0;i<bs.length;i++)bs[i].classList.remove("active");
  btn.classList.add("active");
  var ds=document.querySelectorAll(".md");
  for(var i=0;i<ds.length;i++){{
    var s=ds[i].getAttribute("data-stage")||"";
    ds[i].classList.toggle("hidden",stage!="all"&&s!=stage);
  }}
  var cs=document.querySelectorAll(".mc");
  for(var i=0;i<cs.length;i++){{
    var s=cs[i].getAttribute("data-stage")||"";
    cs[i].classList.toggle("hidden",stage!="all"&&s!=stage);
  }}
}}
function searchTeam(team){{
  var cs=document.querySelectorAll(".mc");
  if(!team){{
    for(var i=0;i<cs.length;i++)cs[i].classList.remove("hidden");
    var ds=document.querySelectorAll(".md");
    for(var i=0;i<ds.length;i++)ds[i].classList.remove("hidden");
    return;
  }}
  for(var i=0;i<cs.length;i++){{
    var h=cs[i].getAttribute("data-home")||"";
    var a=cs[i].getAttribute("data-away")||"";
    cs[i].classList.toggle("hidden",h!=team&&a!=team);
  }}
  var ds=document.querySelectorAll(".md");
  for(var i=0;i<ds.length;i++){{
    var nxt=ds[i].nextElementSibling;
    var vis=false;
    while(nxt&&!nxt.classList.contains("md")){{
      if(nxt.classList.contains("mc")&&!nxt.classList.contains("hidden")){{vis=true;break;}}
      nxt=nxt.nextElementSibling;
    }}
    ds[i].classList.toggle("hidden",!vis);
  }}
}}
function toggleFavFilter(btn){{
  btn.classList.toggle("active");
  var act=btn.classList.contains("active");
  var favs=JSON.parse(localStorage.getItem("wc_favs")||"[]");
  var cs=document.querySelectorAll(".mc");
  if(!act){{
    for(var i=0;i<cs.length;i++)cs[i].classList.remove("hidden","fav");
    return;
  }}
  for(var i=0;i<cs.length;i++){{
    var h=cs[i].getAttribute("data-home")||"";
    var a=cs[i].getAttribute("data-away")||"";
    cs[i].classList.toggle("hidden",favs.indexOf(h)<0&&favs.indexOf(a)<0);
  }}
}}
function toggleFav(team,btn){{
  var favs=JSON.parse(localStorage.getItem("wc_favs")||"[]");
  var idx=favs.indexOf(team);
  if(idx>-1){{favs.splice(idx,1);btn.textContent="☆";btn.style.color="#888";}}
  else{{favs.push(team);btn.textContent="★";btn.style.color="#FFD700";}}
  localStorage.setItem("wc_favs",JSON.stringify(favs));
}}
function initFavs(){{
  var cs=document.querySelectorAll(".mc[data-home]");
  var favs=JSON.parse(localStorage.getItem("wc_favs")||"[]");
  for(var i=0;i<cs.length;i++){{
    if(cs[i].classList.contains("tbd"))continue;
    var h=cs[i].getAttribute("data-home");
    var isFav=favs.indexOf(h)>-1;
    var mhd=cs[i].querySelector(".mhd");
    if(mhd&&!cs[i].querySelector(".favbtn")){{
      var btn=document.createElement("span");
      btn.className="favbtn";
      btn.style.cssText="cursor:pointer;font-size:0.8rem;margin-left:4px;";
      btn.textContent=isFav?"★":"☆";
      btn.style.color=isFav?"#FFD700":"#888";
      btn.onclick=function(e){{e.stopPropagation();toggleFav(h,this);}};
      mhd.appendChild(btn);
    }}
  }}
}}
initFavs();

</script>
</body>
</html>"""

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"OK! Generated 104 matches HTML")
print(f"File size: {len(html)} bytes")
print(f"Match count: {len(ALL_MATCHES)}")