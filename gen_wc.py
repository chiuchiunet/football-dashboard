#!/usr/bin/env python3
"""World Cup 2026 Dashboard Generator - Full 104 Matches + Recent Form"""
from datetime import date, datetime
import random, json
import os
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_results.json")
try:
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        REAL_DATA = json.load(f)
    REAL_RESULTS = REAL_DATA.get("matches", {})
except:
    REAL_RESULTS = {}

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

# US timezones (DST June): ET=UTC-4, CT=UTC-5, MT=UTC-6, PT=UTC-7
# HK is UTC+8
TZ_OFFSET = {
    'New York': 12, 'Miami': 12,  # ET
    'Houston': 13, 'Dallas': 13, 'Kansas City': 13, 'Monterrey': 13, 'Guadalajara': 13, 'Mexico City': 13,  # CT
    'Seattle': 15, 'Los Angeles': 15, 'Vancouver': 15,  # PT
    'Philadelphia': 12, 'Boston': 12, 'Atlanta': 12,  # ET
    'Toronto': 12,  # ET (加拿大東部)
}

def et_to_hk(et, city):
    h, m = map(int, et.split(':'))
    offset = TZ_OFFSET.get(city, 13)
    h += offset
    if h >= 24: h -= 24; return f"{h:02}:{m:02}", True
    return f"{h:02}:{m:02}", False

def local_to_hk_from_api(date_str, city):
    """Convert API local_date (venue local time) to HKT.
    API date_str format: 'MM/DD/YYYY HH:MM' (no timezone)
    Treat as venue local time per city timezone offset.
    Returns (hk_str, is_next_day) or (None, False) on error.
    """
    from datetime import datetime, timedelta
    if not date_str or date_str == 'TBD':
        return None, False
    try:
        dt = datetime.strptime(date_str, '%m/%d/%Y %H:%M')
    except (ValueError, TypeError):
        return date_str, False
    h, m = dt.hour, dt.minute
    offset = TZ_OFFSET.get(city, 13)
    new_h = h + offset
    new_date = dt.date()
    is_next = False
    while new_h >= 24:
        new_h -= 24
        new_date += timedelta(days=1)
        is_next = True
    return f"{new_date.strftime('%m/%d')} {new_h:02}:{m:02}", is_next

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
    if m_num == 6 and d_num >= 28: return 'R32'
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
    R32=[('6月28日','Runner-up A','Runner-up B','15:00','Los Angeles'),('6月29日','Winner C','Runner-up F','13:00','Houston'),('6月29日','Winner E','3rd A/B/C/D','18:30','Boston'),('6月29日','Winner F','Runner-up C','21:00','Monterrey'),('6月30日','Runner-up E','Runner-up I','13:00','Dallas'),('6月30日','Winner I','3rd C/D/F/G/H','17:00','New York'),('6月30日','Winner A','3rd C/E/F/H/I','03:00','Mexico City'),('7月1日','Winner L','3rd E/H/I/J/K','18:00','Atlanta'),('7月1日','Winner G','3rd A/E/H/I/J','22:00','Seattle'),('7月1日','Winner D','3rd B/E/F/I/J','02:00','San Francisco'),('7月2日','Winner H','Runner-up J','21:00','Los Angeles'),('7月2日','Runner-up K','Runner-up L','03:00','Toronto'),('7月2日','Winner B','3rd E/F/G/I/J','11:00','Vancouver'),('7月3日','Runner-up D','Runner-up G','14:00','Dallas'),('7月3日','Winner J','Runner-up H','18:00','Miami'),('7月3日','Winner K','3rd D/E/I/J/L','21:30','Kansas City')]
    h='<div class="bracket"><div class="bround"><h3>32強</h3><div class="bgrid">'
    for i,m in enumerate(R32): h+=bm(m[0],m[1],m[2],m[3],m[4],'M'+str(i+73))
    h+='</div></div><div class="bround"><h3>16強</h3><div class="bgrid">'
    for i,m in enumerate(R16): h+=bm(m[0],m[1],m[2],m[3],m[4],'M'+str(i+49))
    h+='</div></div><div class="bround"><h3>8強</h3><div class="bgrid">'
    for i,m in enumerate(QF): h+=bm(m[0],m[1],m[2],m[3],m[4],'QF'+str(i+1))
    h+='</div></div><div class="bround"><h3>準決</h3><div class="bgrid">'
    for i,m in enumerate(SF): h+=bm(m[0],m[1],m[2],m[3],m[4],'SF'+str(i+1))
    h+='</div></div><div class="bround finals"><h3>決賽</h3><div class="bgrid finals-grid">'
    for m in TD: h+=bm(m[0],m[1],m[2],m[3],m[4],'季軍')
    for m in FN: h+=bm(m[0],m[1],m[2],m[3],m[4],'決賽')
    h+='</div></div></div>'
    return h

SN={'GS':'分組','R32':'32強','R16':'16強','QF':'8強','SF':'準決','3RD':'季軍','FNL':'決賽'}
IC={'GS':'📅','R32':'🎯','R16':'⚡','QF':'🔥','SF':'🏆','3RD':'🥉','FNL':'🏆'}

# Trophy probability
import sys
print('Running 10000 tournament simulations for trophy probability...', file=sys.stderr)
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

# Team name mapping: JSON name -> gen_wc.py name
TEAM_MAP = {
    'Czech Republic': 'Czechia',
    'Bosnia and Herzegovina': 'Bosnia Herz',
    'United States': 'USA',
    'Curaçao': 'Curacao',
    'Democratic Republic of the Congo': 'DR Congo',
}

# Calculate standings from REAL_RESULTS
def calc_standings():
    standings = {}  # team -> {'played':P, 'won':W, 'drawn':D, 'lost':L, 'points':Pts, 'gd':GD, 'gf':GF}
    for g in 'ABCDEFGHIJKL':
        for t in GD[g]:
            standings[t] = {'played':0, 'won':0, 'drawn':0, 'lost':0, 'points':0, 'gd':0, 'gf':0}
    
    for mid, m in REAL_RESULTS.items():
        home = m.get('home_team', '')
        away = m.get('away_team', '')
        hs = m.get('home_score')
        as_ = m.get('away_score')
        if hs is None or as_ is None:
            continue
        # Map team names
        home = TEAM_MAP.get(home, home)
        away = TEAM_MAP.get(away, away)
        if home not in standings or away not in standings:
            continue
        
        # Update played
        standings[home]['played'] += 1
        standings[away]['played'] += 1
        # Goals
        standings[home]['gf'] += hs
        standings[away]['gf'] += as_
        standings[home]['gd'] += (hs - as_)
        standings[away]['gd'] += (as_ - hs)
        
        if hs > as_:
            standings[home]['won'] += 1
            standings[home]['points'] += 3
            standings[away]['lost'] += 1
        elif hs < as_:
            standings[away]['won'] += 1
            standings[away]['points'] += 3
            standings[home]['lost'] += 1
        else:
            standings[home]['drawn'] += 1
            standings[away]['drawn'] += 1
            standings[home]['points'] += 1
            standings[away]['points'] += 1
    
    return standings

STANDINGS = calc_standings()

# Resolve group stage → R32 placeholders
# After all GS matches, compute group winners, runners-up, and best 8 3rd-place teams
def get_group_ranking():
    """Compute WC2026 group ranking: top 2 + best 8 3rds advance to R32.
    Returns (winner, runner_up, third, best_3rd_groups)
    - winner[g]: 1st in group g
    - runner_up[g]: 2nd in group g
    - third[g]: 3rd in group g
    - best_3rd_groups: list of 8 group letters whose 3rd-place teams advance
    Tiebreak order: points → goal diff → goals for
    """
    winner = {}
    runner_up = {}
    third = {}
    third_ranked = []  # [(group_letter, team, pts, gd, gf)]
    
    for g in 'ABCDEFGHIJKL':
        ranked = sorted(
            GD[g],
            key=lambda t: (-STANDINGS.get(t, {}).get('points', 0),
                           -STANDINGS.get(t, {}).get('gd', 0),
                           -STANDINGS.get(t, {}).get('gf', 0))
        )
        winner[g] = ranked[0]
        runner_up[g] = ranked[1]
        third[g] = ranked[2]
        st = STANDINGS.get(ranked[2], {})
        third_ranked.append((g, ranked[2], st.get('points', 0), st.get('gd', 0), st.get('gf', 0)))
    
    # Sort 3rds by points → GD → GF, take top 8
    third_ranked.sort(key=lambda x: (-x[2], -x[3], -x[4]))
    best_3rd_groups = [g for g, _, _, _, _ in third_ranked[:8]]
    
    return winner, runner_up, third, best_3rd_groups

WINNER_G, RUNNER_UP_G, THIRD_G, BEST_3RD_GROUPS = get_group_ranking()

def resolve_tbd(name):
    """Resolve WC2026 R32 placeholder to actual team name.
    Handles:
      - 'Winner X' → 1st place in group X
      - 'Runner-up X' → 2nd place in group X
      - '3rd X/Y/Z/...' → best 3rd-place team from qualifying groups (each 3rd used at most once)
      - 'W37'/'SF1-W'/etc → leave as-is (later rounds)
    Uses module-level USED_3RD_GROUPS set to track which 3rd-place groups have been assigned.
    """
    global USED_3RD_GROUPS
    if not name or not isinstance(name, str):
        return name
    if name.startswith('Winner '):
        g = name.split(' ', 1)[1]
        if g in WINNER_G:
            return WINNER_G[g]
        return name
    if name.startswith('Runner-up '):
        g = name.split(' ', 1)[1]
        if g in RUNNER_UP_G:
            return RUNNER_UP_G[g]
        return name
    if name.startswith('3rd '):
        groups = name.split(' ', 1)[1].split('/')
        # FIFA bracket rule: pick first group whose 3rd-place team advanced
        # AND hasn't been used in an earlier R32 match yet
        for g in groups:
            if g in BEST_3RD_GROUPS and g not in USED_3RD_GROUPS:
                USED_3RD_GROUPS.add(g)
                return THIRD_G[g]
        # Fallback: first qualifying (may duplicate if all eligible already used)
        for g in groups:
            if g in BEST_3RD_GROUPS:
                return THIRD_G[g]
        return name
    return name

USED_3RD_GROUPS = set()  # Track which 3rd-place groups have been assigned to R32 matches

# Build team-pair lookup for real results (API id order ≠ ALL_MATCHES order)
RESULTS_BY_TEAM_PAIR = {}
for mid, m in REAL_RESULTS.items():
    home = TEAM_MAP.get(m.get('home_team', ''), m.get('home_team', ''))
    away = TEAM_MAP.get(m.get('away_team', ''), m.get('away_team', ''))
    if home and away:
        RESULTS_BY_TEAM_PAIR[(home, away)] = m

gh=[]
for g in 'ABCDEFGHIJKL':
    qps=mc_cache[g]
    ts=GD[g]
    rows=[]
    for t in sorted(ts,key=lambda x:-rt(x)):
        st = STANDINGS.get(t, {'played':'-', 'won':'-', 'drawn':'-', 'lost':'-', 'points':'-'})
        p = st.get('played', '-')
        w = st.get('won', '-')
        d = st.get('drawn', '-')
        l = st.get('lost', '-')
        pts = st.get('points', '-')
        # Use gray color if no results yet
        pg = '#888' if p == '-' else '#fff'
        rows.append(f"<tr><td>{fl(t)} {cn(t)}</td><td style='text-align:center;font-size:0.65rem;'>{rt(t)}</td><td style='text-align:center;font-size:0.65rem;color:{pg}'>{p}</td><td style='text-align:center;font-size:0.65rem;color:{pg}'>{w}</td><td style='text-align:center;font-size:0.65rem;color:{pg}'>{d}</td><td style='text-align:center;font-size:0.65rem;color:{pg}'>{l}</td><td style='text-align:right;'><span style='font-weight:700;color:#FFD700;'>{pts}</span></td><td style='text-align:center;font-size:0.55rem;color:#888;'>{qps.get(t,'-')}</td></tr>")
    gh.append(f"<div class='gc'><div class='gh'>組 {g}</div><table class='gt'><thead><tr><th>球隊</th><th style='text-align:center'>實力</th><th style='text-align:center'>賽</th><th style='text-align:center'>勝</th><th style='text-align:center'>和</th><th style='text-align:center'>負</th><th style='text-align:right'>分</th><th style='text-align:center'>出線%</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>")

chan_map={'Mexico City':'Now618','Guadalajara':'Now 618','Toronto':'Now638','Los Angeles':'Now 638','San Francisco':'Now 638','New York':'Now638','Boston':'Now 638','Vancouver':'Now638','Houston':'Now 638','Philadelphia':'Now 638','Dallas':'Now 638','Monterrey':'Now 638','Atlanta':'Now 638','Seattle':'Now 638','Miami':'Now 638','Kansas City':'Now 638'}
acc_correct = 0
acc_winner = 0
acc_total = 0
mm=[]
cur=''
# Load official schedule cache (ET times from sportsbrackets.net → UTC/HKT)
# This is the SINGLE SOURCE OF TRUTH for group stage kickoff times.
OFFICIAL_SCHEDULE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'official_schedule_utc.json')
OFFICIAL_SCHEDULE = {}  # key: (home, away) → {date_hkt, time_hkt, date_et, time_et, ...}
try:
    if os.path.exists(OFFICIAL_SCHEDULE_FILE):
        with open(OFFICIAL_SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            _os_data = json.load(f)
        for _m in _os_data:
            OFFICIAL_SCHEDULE[(_m['home'], _m['away'])] = _m
            OFFICIAL_SCHEDULE[(_m['away'], _m['home'])] = _m  # reverse lookup
        print(f"Loaded {len(_os_data)} official schedule entries from {OFFICIAL_SCHEDULE_FILE}", file=sys.stderr)
    else:
        print(f"⚠️  Official schedule file not found: {OFFICIAL_SCHEDULE_FILE}", file=sys.stderr)
except Exception as _e:
    print(f"⚠️  Failed to load official schedule: {_e}", file=sys.stderr)

for idx, m in enumerate(ALL_MATCHES):
    day,h,a,et,city=m
    # PRIORITY 1: Use official schedule cache (FIFA-accurate ET times → HKT)
    official = OFFICIAL_SCHEDULE.get((h, a))
    if official:
        hk = official['time_hkt']
        hk_date = official['date_hkt']
        nd = hk_date != '2026-' + day.replace('月', '-').zfill(2) and not hk_date.endswith(day.split('月')[1].zfill(2)) if '月' in day else False
        # Simpler: compare month-day only
        try:
            cur_md = day.replace('月', '-').zfill(5)  # "6月17日" → "06-17"
            nd = hk_date[5:] != cur_md
        except Exception:
            nd = False
    else:
        hk, nd = et_to_hk(et, city)
    # PRIORITY 2 (legacy): worldcup26.ir local_date fallback
    real_for_time = RESULTS_BY_TEAM_PAIR.get((h, a), {}) or RESULTS_BY_TEAM_PAIR.get((a, h), {})
    api_date = real_for_time.get('date', '') if isinstance(real_for_time, dict) else ''
    if not official and api_date:
        api_hk, api_nd = local_to_hk_from_api(api_date, city)
        if api_hk:
            hk, nd = api_hk, api_nd
    plus=' (+1)' if nd else ''
    # Build ISO-like string for live banner JS to compute next match
    if official:
        hkt_iso = official['date_hkt'] + 'T' + official['time_hkt'] + ':00'
    else:
        # fallback: use current HKT date + hk time (less reliable for cross-day)
        try:
            from datetime import datetime, timedelta
            cur_md = day.replace('月', '-').zfill(5)  # '6月17日' → '06-17'
            year = 2026
            month, day_num = cur_md.split('-')
            # If nd (next day) bump by 1
            base_dt = datetime(int(year), int(month), int(day_num))
            if nd:
                base_dt += timedelta(days=1)
            hkt_iso = base_dt.strftime('%Y-%m-%d') + 'T' + hk + ':00'
        except Exception:
            hkt_iso = ''
    # Resolve R32 placeholders to actual teams from group standings
    h = resolve_tbd(h)
    a = resolve_tbd(a)
    st=stage_of(day)
    lbl=SN[st]
    icon=IC[st]
    if day!=cur:
        mm.append(f"<div class='md' data-stage='{st}'>{icon} {day} <span style='font-size:0.65rem;color:#888;margin-left:6px;'>({lbl})</span></div>")
        cur=day
    if h in TBD or a in TBD:
        # Check real result via team-pair lookup
        real = RESULTS_BY_TEAM_PAIR.get((h, a), {})
        real_finished = real.get('finished', False)
        real_hs = real.get('home_score')
        real_as = real.get('away_score')
        comparison_badge = ''
        if real_finished and real_hs is not None and real_as is not None:
            acc_total += 1
            if real_hs == hsc and real_as == asc:
                acc_correct += 1
                acc_winner += 1
                comparison_badge = f'<span style="margin-left:6px;color:#22c55e;" title="預測正確">✅ {real_hs}-{real_as}</span>'
            elif (real_hs > real_as) == (hsc > asc) or (real_hs == hsc and real_as == asc):
                acc_winner += 1
                comparison_badge = f'<span style="margin-left:6px;color:#eab308;" title="估中勝方">🟡 {real_hs}-{real_as}</span>'
            else:
                comparison_badge = f'<span style="margin-left:6px;color:#ef4444;">❌ {real_hs}-{real_as}</span>'
        mm.append(f"<div class='mc' data-stage='{st}'  data-home='{h}' data-away='{a}' data-hkt-iso=''><div class='mhd'><span class='mcomp'>{lbl} </span><span class='conf {cf_cls}'>{cf_icon}</span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span><span class='mchan'>📺 {chan}</span></div><div class='mbody' style='justify-content:center;'><span style='color:#888;font-size:0.75rem;'>⚠️ 待定 - 分組賽後揭曉</span></div></div>")
    else:
        hs,as_=rt(h),rt(a)
        hp,dp,ap_=prob(hs,as_)
        xh,xa=xg(hs,as_)
        hsc,asc=score(hs,as_)
        cf_cls,cf_icon=conf(hs,as_)
        chan=chan_map.get(city,'Now TV')
        rf_h = get_recent_form_html(h)
        rf_a = get_recent_form_html(a)
        # Check real result via team-pair lookup
        real = RESULTS_BY_TEAM_PAIR.get((h, a), {})
        real_finished = real.get('finished', False)
        real_hs = real.get('home_score')
        real_as = real.get('away_score')
        comparison_badge = ''
        if real_finished and real_hs is not None and real_as is not None:
            acc_total += 1
            if real_hs == hsc and real_as == asc:
                acc_correct += 1
                acc_winner += 1
                comparison_badge = f'<span style="margin-left:6px;color:#22c55e;" title="預測正確">✅ {real_hs}-{real_as}</span>'
            elif (real_hs > real_as) == (hsc > asc) or (real_hs == hsc and real_as == asc):
                acc_winner += 1
                comparison_badge = f'<span style="margin-left:6px;color:#eab308;" title="估中勝方">🟡 {real_hs}-{real_as}</span>'
            else:
                comparison_badge = f'<span style="margin-left:6px;color:#ef4444;">❌ {real_hs}-{real_as}</span>'
        mm.append(f"<div class='mc' data-stage='{st}'  data-home='{h}' data-away='{a}' data-hkt-iso='{hkt_iso}'><div class='mhd'><span class='mcomp'>{lbl} </span><span class='conf {cf_cls}'>{cf_icon}</span><span class='mhkt'>🕐 {hk} HK{plus}</span><span class='mvenue'>🏟️ {city}</span><span class='mchan'>📺 {chan}</span></div><div class='mbody'><div class='mteam'>{fl(h)} {cn(h)}<span class='str'>{hs}</span>{kp(h)}<div class='mr'>{rf_h}</div></div><div class='mscore'>{hsc}⚽{asc}{comparison_badge}</div><div class='mteam'>{fl(a)} {cn(a)}<span class='str'>{as_}</span>{kp(a)}<div class='mr'>{rf_a}</div></div></div><div class='mfoot'><div class='mbar'><div class='mp' style='width:{hp:.0f}%'><span>H{hp:.0f}%</span></div><div class='mpd' style='width:{dp:.0f}%'><span>D{dp:.0f}%</span></div><div class='mpa' style='width:{ap_:.0f}%'><span>A{ap_:.0f}%</span></div></div><div class='mxg'>xG {xh}-{xa} | O{int(xh+xa+0.5)} | ⚽{int(xh+xa+0.5)}球</div></div></div>")

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

gs_c=72; r32_c=16; r16_c=8; qf_c=4; sf_c=2; f_c=2

CSS="""*{margin:0;padding:0;box-sizing:border-box;}body{font-family:"Noto Sans HK",sans-serif;background:linear-gradient(160deg,#080812 0%,#0d0d1a 50%,#080812 100%);color:#f5f5f7;padding:12px;min-height:100vh;}.wrap{max-width:1200px;margin:0 auto;}.hero{background:linear-gradient(135deg,rgba(26,26,46,0.95),rgba(22,33,62,0.9));border:1px solid rgba(255,215,0,0.3);border-radius:18px;padding:24px;text-align:center;margin-bottom:16px;backdrop-filter:blur(20px);box-shadow:0 8px 32px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.05);position:relative;overflow:hidden;}.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at center,rgba(255,215,0,0.06) 0%,transparent 60%);pointer-events:none;}.hero h1{font-size:1.9rem;background:linear-gradient(135deg,#FFD700,#FF8C00,#FFD700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:4px;font-weight:800;letter-spacing:-0.5px;}.hero p{color:#9ca3af;font-size:0.78rem;margin-top:4px;}.cd{margin-top:14px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap;}.cdi{text-align:center;padding:8px 16px;background:rgba(255,215,0,0.05);border-radius:12px;border:1px solid rgba(255,215,0,0.1);}.cdn{font-size:1.4rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}.cdl{font-size:0.5rem;color:#9ca3af;text-transform:uppercase;letter-spacing:1px;}.ctd{font-size:0.6rem;color:#FF8C00;margin-top:4px;}.stats{display:flex;gap:6px;margin-bottom:16px;}.sc{flex:1;background:rgba(22,22,29,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:10px;text-align:center;cursor:pointer;backdrop-filter:blur(10px);transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}.sc:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(255,215,0,0.15);border-color:rgba(255,215,0,0.3);}.scn{font-size:1.1rem;font-weight:700;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}.scl{font-size:0.5rem;color:#9ca3af;}.tab-nav{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;}.tab{background:rgba(22,22,29,0.6);border:1px solid rgba(255,255,255,0.06);color:#9ca3af;padding:10px 16px;border-radius:50px;cursor:pointer;font-size:0.75rem;transition:all 0.3s;backdrop-filter:blur(10px);}.tab:hover{background:rgba(255,215,0,0.1);border-color:rgba(255,215,0,0.3);color:#FFD700;}.tab.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-weight:700;box-shadow:0 4px 16px rgba(255,215,0,0.3);}.content{display:none;}.content.show{display:block;}h2{font-size:0.95rem;color:#FFD700;margin:20px 0 10px;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:6px;font-weight:600;}.gg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin-bottom:20px;}.gc{background:rgba(22,22,29,0.7);border:1px solid rgba(255,255,255,0.06);border-radius:14px;overflow:hidden;backdrop-filter:blur(10px);transition:all 0.3s;}.gc:hover{border-color:rgba(255,215,0,0.4);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3);}.gh{background:linear-gradient(90deg,rgba(42,42,58,0.9),rgba(26,26,46,0.9));padding:8px 12px;font-weight:700;font-size:0.75rem;color:#FFD700;border-bottom:1px solid rgba(255,255,255,0.04);}.gt{width:100%;border-collapse:collapse;font-size:0.62rem;}.gt th{text-align:left;padding:5px 8px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,0.04);font-weight:500;}.gt td{padding:5px 8px;border-bottom:1px solid rgba(255,255,255,0.02);}.str{color:#9ca3af;font-size:0.7em;margin-left:4px;}.rf{display:flex;gap:3px;margin-top:4px;flex-wrap:wrap;}.rf span{font-size:0.55rem;padding:2px 5px;border-radius:4px;font-weight:600;}.rfw{background:rgba(34,197,94,0.25);color:#22c55e;border:1px solid rgba(34,197,94,0.3);}.rfl{background:rgba(239,68,68,0.25);color:#ef4444;border:1px solid rgba(239,68,68,0.3);}.rfd{background:rgba(148,148,160,0.2);color:#9ca3af;}.rfup{background:rgba(255,215,0,0.15);color:#FFD700;}.rfnil{font-size:0.55rem;color:#555;}.mr{margin-top:4px;}.mteam{line-height:1.4;}.ml{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.md{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-size:0.72rem;font-weight:700;padding:6px 14px;border-radius:8px;margin:16px 0 8px;box-shadow:0 4px 12px rgba(255,215,0,0.2);}.md.hidden,.mc.hidden{display:none;}.mc{background:rgba(22,22,29,0.75);border:1px solid rgba(255,255,255,0.06);border-radius:14px;overflow:hidden;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);backdrop-filter:blur(12px);}.mc:hover{border-color:rgba(255,215,0,0.4);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3),0 0 20px rgba(255,215,0,0.08);}.mc.fav{border-color:rgba(255,215,0,0.5);box-shadow:0 0 20px rgba(255,215,0,0.2);}.mhd{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:rgba(26,26,46,0.6);border-bottom:1px solid rgba(255,255,255,0.04);gap:8px;flex-wrap:wrap;}.mcomp{font-size:0.65rem;font-weight:700;color:#FFD700;}.conf{font-size:0.6rem;padding:2px 8px;border-radius:50px;font-weight:600;margin-right:6px;}.conf.high{background:rgba(34,197,94,0.2);color:#22c55e;border:1px solid rgba(34,197,94,0.3);}.conf.medium{background:rgba(234,179,8,0.2);color:#eab308;border:1px solid rgba(234,179,8,0.3);}.conf.low{background:rgba(239,68,68,0.2);color:#ef4444;border:1px solid rgba(239,68,68,0.3);}.mhkt{font-size:0.6rem;color:#FF8C00;}.mvenue{font-size:0.6rem;color:#9ca3af;}.mbody{display:flex;align-items:center;padding:14px;gap:12px;flex-wrap:wrap;}.mteam{flex:1;font-size:0.88rem;font-weight:600;min-width:80px;}.mscore{display:flex;align-items:center;font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;padding:0 14px;white-space:nowrap;}.mfoot{padding:8px 12px;border-top:1px solid rgba(255,255,255,0.04);}.mbar{display:flex;height:22px;border-radius:6px;overflow:hidden;gap:2px;margin-bottom:4px;}.mp{background:linear-gradient(90deg,rgba(34,197,94,0.7),rgba(34,197,94,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpd{background:linear-gradient(90deg,rgba(148,148,160,0.7),rgba(148,148,160,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mpa{background:linear-gradient(90deg,rgba(239,68,68,0.7),rgba(239,68,68,0.5));display:flex;align-items:center;justify-content:center;font-size:0.55rem;color:#fff;font-weight:600;min-width:24px;overflow:hidden;}.mxg{font-size:0.58rem;color:#9ca3af;}.sd{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:8px;margin-bottom:20px;}.sb{display:flex;align-items:center;gap:6px;}.sl{font-size:0.65rem;color:#9ca3af;width:32px;text-align:right;}.sb2{flex:1;height:16px;background:rgba(26,26,46,0.8);border-radius:4px;overflow:hidden;}.sbf{height:100%;background:linear-gradient(90deg,#FFD700,#FF6B35,#FF4500);border-radius:4px;}.sn{font-size:0.65rem;color:#FFD700;font-weight:700;width:16px;}.ft{text-align:center;padding:20px 0;color:#9ca3af;font-size:0.6rem;border-top:1px solid rgba(255,255,255,0.04);margin-top:20px;}.sch-bar{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;align-items:center;}.sf-btn{background:rgba(22,22,29,0.6);border:1px solid rgba(255,255,255,0.06);color:#9ca3af;padding:6px 12px;border-radius:50px;cursor:pointer;font-size:0.7rem;transition:all 0.3s;backdrop-filter:blur(10px);}.sf-btn:hover{border-color:rgba(255,215,0,0.3);color:#FFD700;}.sf-btn.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;font-weight:700;box-shadow:0 4px 12px rgba(255,215,0,0.2);}.fav-filter.active{background:linear-gradient(135deg,#FFD700,#FF8C00);color:#000;}.fav-filter{background:rgba(22,22,29,0.6);border:1px solid rgba(255,215,0,0.4);color:#FFD700;}.kp{font-size:0.55rem;color:#FF8C00;display:block;margin-top:3px;font-weight:500;}/* Live banner */.live-banner{position:sticky;top:0;z-index:999;background:linear-gradient(90deg,rgba(255,215,0,0.15),rgba(255,140,0,0.15));border:1px solid rgba(255,215,0,0.3);border-radius:14px;padding:12px 16px;margin:0 0 14px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;backdrop-filter:blur(12px);box-shadow:0 4px 16px rgba(0,0,0,0.3);cursor:pointer;transition:all 0.3s;}.live-banner:hover{transform:translateY(-1px);border-color:rgba(255,215,0,0.5);box-shadow:0 8px 24px rgba(255,215,0,0.15);}.live-banner.live{background:linear-gradient(90deg,rgba(239,68,68,0.2),rgba(239,68,68,0.1));border-color:rgba(239,68,68,0.5);animation:pulse 2s ease-in-out infinite;}@keyframes pulse{0%,100%{box-shadow:0 4px 16px rgba(239,68,68,0.3);}50%{box-shadow:0 4px 24px rgba(239,68,68,0.6);}}.lb-status{display:flex;align-items:center;gap:8px;font-size:0.78rem;font-weight:700;}.lb-dot{width:10px;height:10px;border-radius:50%;background:#FFD700;box-shadow:0 0 8px #FFD700;}.live-banner.live .lb-dot{background:#ef4444;box-shadow:0 0 12px #ef4444;animation:blink 1s ease-in-out infinite;}@keyframes blink{0%,100%{opacity:1;}50%{opacity:0.4;}}.lb-match{flex:1;font-size:0.85rem;font-weight:600;}.lb-time{font-family:monospace;font-size:0.95rem;font-weight:800;color:#FFD700;letter-spacing:1px;}.live-banner.live .lb-time{color:#ef4444;}.lb-jump{font-size:0.7rem;color:#9ca3af;padding:4px 10px;border:1px solid rgba(255,215,0,0.3);border-radius:6px;transition:all 0.3s;}.live-banner:hover .lb-jump{background:rgba(255,215,0,0.1);border-color:rgba(255,215,0,0.5);color:#FFD700;}/* Tonight filter highlight */.mc.tonight-highlight{border-color:rgba(255,215,0,0.5);box-shadow:0 0 24px rgba(255,215,0,0.15);}
.mr{display:flex;flex-direction:column;gap:8px;margin-bottom:20px;}.medal-row{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;}.medal-card{flex:1;min-width:100px;background:rgba(22,22,29,0.8);border-radius:14px;padding:14px;text-align:center;border:1px solid rgba(255,255,255,0.06);transition:all 0.3s;}.medal-card.gold{border-color:rgba(255,215,0,0.5);background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(22,22,29,0.8));}.medal-card.silver{border-color:rgba(192,192,192,0.4);}.medal-card.bronze{border-color:rgba(205,127,50,0.4);}.medal-card:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.3);}.mrank{font-size:1.5rem;margin-bottom:6px;}.mflag{font-size:1.8rem;margin-bottom:4px;}.mname{font-size:0.72rem;font-weight:600;color:#f5f5f7;margin-bottom:6px;}.mwin{font-size:1.1rem;font-weight:800;color:#FFD700;}.msf{font-size:0.65rem;color:#9ca3af;}.trophy-legend{display:flex;gap:14px;margin-bottom:14px;flex-wrap:wrap;align-items:center;}.tpc{font-size:0.65rem;padding:2px 8px;border-radius:50px;font-weight:600;}.tw{background:rgba(255,215,0,0.2);color:#FFD700;}.tf{background:rgba(148,163,184,0.2);color:#c0c0c0;}.ts{background:rgba(239,68,68,0.2);color:#ef4444;}.tq{background:rgba(234,179,8,0.2);color:#eab308;}.tr{background:rgba(34,197,94,0.2);color:#22c55e;}.ttbl{width:100%;border-collapse:collapse;font-size:0.65rem;}.ttbl th{text-align:left;padding:8px 10px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,0.08);font-weight:500;}.ttbl td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,0.03);}.ttbl tr:hover td{background:rgba(255,215,0,0.05);}.tpbar{display:flex;height:10px;border-radius:5px;overflow:hidden;gap:1px;}.tpw{background:linear-gradient(90deg,#FFD700,#FF8C00);}.tpf{background:rgba(192,192,192,0.6);}.tps{background:rgba(239,68,68,0.6);}.tpq{background:rgba(234,179,8,0.6);}.tpr{background:rgba(34,197,94,0.6);}.mchan{font-size:0.55rem;color:#9ca3af;margin-left:6px;}.bracket{margin-top:10px;}.bround{margin-bottom:20px;}.bround h3{font-size:0.85rem;color:#FFD700;margin:0 0 10px;padding:6px 12px;background:rgba(255,215,0,0.1);border-radius:8px;border-left:3px solid #FFD700;}.bgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;}.bgrid.finals-grid{grid-template-columns:repeat(2,1fr);max-width:500px;}.bmc{background:rgba(22,22,29,0.8);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:12px;transition:all 0.3s;}.bmc:hover{border-color:rgba(255,215,0,0.4);box-shadow:0 4px 16px rgba(0,0,0,0.2);}.bmc.tbd{opacity:0.5;}.bmtop{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.04);}.bmlbl{font-size:0.7rem;font-weight:700;color:#FFD700;}.bmhk{font-size:0.6rem;color:#9ca3af;}.bmteams{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;}.btm{flex:1;font-size:0.8rem;font-weight:600;}.bscore{font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;padding:0 8px;white-space:nowrap;}.bmtbd{color:#666;font-size:0.8rem;}.bmbbar{display:flex;height:18px;border-radius:4px;overflow:hidden;gap:1px;}.bmp{flex:0 0 auto;background:linear-gradient(90deg,rgba(34,197,94,0.8),rgba(34,197,94,0.6));display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}.bmd{flex:0 0 auto;background:rgba(148,148,160,0.6);display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}.bma{flex:0 0 auto;background:linear-gradient(90deg,rgba(239,68,68,0.8),rgba(239,68,68,0.6));display:flex;align-items:center;justify-content:center;font-size:0.5rem;color:#fff;font-weight:600;min-width:20px;}
.bnav{display:none;position:fixed;bottom:0;left:0;right:0;background:rgba(13,13,26,0.95);backdrop-filter:blur(20px);border-top:1px solid rgba(255,215,0,0.2);padding:8px 0;padding-bottom:max(8px,env(safe-area-inset-bottom));z-index:1000;box-shadow:0 -4px 20px rgba(0,0,0,0.3);}.bni{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;background:none;border:none;color:#9ca3af;cursor:pointer;padding:4px 8px;transition:all 0.2s;}.bni.active{color:#FFD700;}.bni:hover{color:#FFD700;}.bne{font-size:1.3rem;}.bnl{font-size:0.55rem;font-weight:500;}
@media(max-width:600px){body{overflow-x:hidden;max-width:100vw;}.bnav{display:flex;}.wrap{padding:8px;padding-bottom:70px;max-width:100vw;overflow-x:hidden;}.hero{padding:12px;border-radius:12px;}.hero h1{font-size:1.2rem;}.cd{gap:8px;}.cdn{font-size:1rem;}.stats{gap:4px;}.sc{padding:6px;}.scn{font-size:0.8rem;}.scl{font-size:0.4rem;}.tab-nav{gap:4px;}.tab{padding:6px 10px;font-size:0.6rem;}.gg{grid-template-columns:1fr;gap:8px;}.gc{font-size:0.85rem;}.gt{font-size:0.5rem;}.gt th,.gt td{padding:3px 4px;}.mhd{flex-wrap:wrap;gap:4px;padding:4px 6px;}.mcomp{font-size:0.5rem;}.mhkt,.mvenue,.mchan{font-size:0.45rem;}.mbody{padding:6px;gap:4px;flex-direction:column;}.mteam{flex:1 1 100%;font-size:0.7rem;min-width:auto;width:100%;}.mscore{font-size:1rem;padding:4px 8px;width:100%;text-align:center;justify-content:center;}.mfoot{padding:4px 6px;}.mxg{font-size:0.45rem;}.mc{padding:6px;margin-bottom:8px;}.ml{gap:6px;}}"""

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
<div class='live-banner' id='liveBanner' onclick='jumpToNext()'>
  <div class='lb-status'>
    <span class='lb-dot'></span>
    <span id='lbStatus'>下一場</span>
  </div>
  <div class='lb-match' id='lbMatch'>🔍 計算中…</div>
  <div class='lb-time' id='lbTime'>--:--:--</div>
  <div class='lb-jump' id='lbJump'>跳去 ↗</div>
</div>
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
<button class="sf-btn" id="tonightBtn" onclick="filterTonight(this)">🌙 今晚</button>
<button class="sf-btn" onclick="filterStage('GS',this)">📅 分組</button>
<button class="sf-btn" onclick="filterStage('R32',this)">🎯 32強</button>
<button class="sf-btn" onclick="filterStage('R16',this)">⚡ 16強</button>
<button class="sf-btn" onclick="filterStage('QF',this)">🔥 8強</button>
<button class="sf-btn" onclick="filterStage('SF',this)">🏆 準決</button>
<button class="sf-btn" onclick="filterStage('3RD',this)">🥉 季軍</button>
<button class="sf-btn" onclick="filterStage('FNL',this)">🏆 決賽</button>
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
  var ts2=document.querySelectorAll(".tab");
  for(var i=0;i<ts2.length;i++)if(ts2[i].getAttribute("onclick").indexOf(tab)>-1)ts2[i].classList.add("active");
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

/* === Live Banner: 下一場倒數 + 一 click 跳去 === */
function buildLiveBanner(){{
  const cards = Array.from(document.querySelectorAll('.mc'));
  const now = new Date();
  // Find next match (HKT > now) or live match (within 2hr of kickoff)
  const matches = cards
    .filter(c => c.getAttribute('data-hkt-iso'))
    .map(c => ({{
      el: c,
      dt: new Date(c.getAttribute('data-hkt-iso')),
      home: c.getAttribute('data-home'),
      away: c.getAttribute('data-away'),
    }}))
    .filter(m => !isNaN(m.dt.getTime()))
    .sort((a, b) => a.dt - b.dt);
  if (matches.length === 0) return;
  const upcoming = matches.find(m => m.dt > now);
  const lastFinished = matches.filter(m => m.dt <= now).pop();
  let target, isLive = false, elapsedMin = 0;
  if (upcoming) {{
    target = upcoming;
    const prev = matches[Math.max(0, matches.indexOf(upcoming) - 1)];
    if (prev && (target.dt - prev.dt) < 1000*60*60*3 && (target.dt - prev.dt) > 0) {{
      // Check if prev match finished within 2hr ago → could be live now
    }}
  }}
  // Check if any match is currently live (between kickoff and kickoff+2hr)
  const liveCandidate = matches.find(m => {{
    const diffMin = (now - m.dt) / 60000;
    return diffMin >= 0 && diffMin < 120;
  }});
  if (liveCandidate) {{
    target = liveCandidate;
    isLive = true;
    elapsedMin = Math.floor((now - target.dt) / 60000);
  }} else if (!upcoming) {{
    // All matches finished (e.g. final done)
    target = lastFinished || matches[matches.length - 1];
    isLive = false;
  }}
  if (!target) return;
  // Update DOM
  document.getElementById('lbMatch').textContent = `🇦 ${{target.home}} vs 🇧 ${{target.away}}`;
  document.getElementById('lbJump').setAttribute('data-target-home', target.home);
  const banner = document.getElementById('liveBanner');
  if (isLive) {{
    banner.classList.add('live');
    document.getElementById('lbStatus').textContent = `⚽ 進行中`;
    document.getElementById('lbTime').textContent = `+${{elapsedMin}}'`;
  }} else {{
    banner.classList.remove('live');
    document.getElementById('lbStatus').textContent = '下一場';
    const diffMs = target.dt - now;
    const totalSec = Math.max(0, Math.floor(diffMs / 1000));
    const days = Math.floor(totalSec / 86400);
    const hh = String(Math.floor((totalSec % 86400) / 3600)).padStart(2, '0');
    const mm = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
    const ss = String(totalSec % 60).padStart(2, '0');
    document.getElementById('lbTime').textContent = days > 0 ? `T-${{days}}d ${{hh}}:${{mm}}:${{ss}}` : `T-${{hh}}:${{mm}}:${{ss}}`;
  }}
  // Store target globally for jumpToNext
  window.__liveBannerTarget = target;
  // Highlight target card
  document.querySelectorAll('.mc').forEach(c => c.classList.remove('fav'));
  target.el.classList.add('fav');
}}
function jumpToNext(){{
  const t = window.__liveBannerTarget;
  if (!t || !t.el) return;
  t.el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
  t.el.style.transition = 'box-shadow 0.3s';
  t.el.style.boxShadow = '0 0 32px rgba(255,215,0,0.6)';
  setTimeout(() => {{ t.el.style.boxShadow = ''; }}, 1200);
}}
setInterval(buildLiveBanner, 1000);
buildLiveBanner();

/* === 今晚 filter: show only tonight's matches === */
function filterTonight(btn){{
  // Deactivate other stage buttons
  document.querySelectorAll('.sf-btn').forEach(b => {{
    if (b !== btn) b.classList.remove('active');
  }});
  btn.classList.toggle('active');
  if (!btn.classList.contains('active')) {{
    // Re-enable '全部'
    document.querySelector('.sf-btn').classList.add('active');
    document.querySelectorAll('.mc').forEach(c => c.classList.remove('hidden'));
    document.querySelectorAll('.md').forEach(d => d.classList.remove('hidden'));
    return;
  }}
  // Calculate tonight window: HKT 18:00 today → 12:00 next day
  const now = new Date();
  // Convert now to HKT
  const hktNow = new Date(now.getTime() + 8*60*60*1000);
  // tonight_start = HKT today 18:00
  const tonightHkt = new Date(Date.UTC(hktNow.getUTCFullYear(), hktNow.getUTCMonth(), hktNow.getUTCDate(), 18, 0, 0) - 8*60*60*1000);
  // tomorrow_end = HKT tomorrow 12:00
  const tomorrowHkt = new Date(tonightHkt.getTime() + 18*60*60*1000);
  document.querySelectorAll('.mc').forEach(c => {{
    const iso = c.getAttribute('data-hkt-iso');
    if (!iso) {{ c.classList.add('hidden'); return; }}
    const dt = new Date(iso);
    if (dt >= tonightHkt && dt < tomorrowHkt) {{
      c.classList.remove('hidden');
      c.classList.add('tonight-highlight');
    }} else {{
      c.classList.add('hidden');
      c.classList.remove('tonight-highlight');
    }}
  }});
  // Hide day dividers that have no visible matches
  document.querySelectorAll('.md').forEach(d => {{
    let next = d.nextElementSibling;
    let hasVisible = false;
    while (next && !next.classList.contains('md')) {{
      if (next.classList.contains('mc') && !next.classList.contains('hidden')) {{
        hasVisible = true; break;
      }}
      next = next.nextElementSibling;
    }}
    if (hasVisible) d.classList.remove('hidden');
    else d.classList.add('hidden');
  }});
  // Scroll to schedule
  document.getElementById('schedule').scrollIntoView({{behavior: 'smooth', block: 'start'}});
}}
</script>
</body>
</html>"""

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"OK! Generated 104 matches HTML", file=sys.stderr)
print(f"File size: {len(html)} bytes", file=sys.stderr)
print(f"Match count: {len(ALL_MATCHES)}", file=sys.stderr)