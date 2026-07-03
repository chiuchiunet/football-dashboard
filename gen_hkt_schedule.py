#!/usr/bin/env python3
"""Generate HKT-converted schedule for all matches.

Sources of truth:
- Group Stage: official_schedule_utc.json (FIFA-accurate, already HKT-converted)
- R32+: hardcoded venue mapping + zoneinfo convert

Output: hkt_schedule.json with hkt_display field for sub-agent to use directly.
"""
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

DATA = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(DATA, "real_results.json")
OFFICIAL = os.path.join(DATA, "official_schedule_utc.json")
OUTPUT = os.path.join(DATA, "hkt_schedule.json")

# R32+ venue mapping (from FIFA 2026 official schedule)
# match_id → venue city (English, used to lookup timezone)
R32_VENUES = {
    '80': 'Miami',           # 7月1日 12:00 EDT (UTC-4)
    '81': 'Los Angeles',     # 7月1日 17:00 PDT (UTC-7)
    '82': 'Dallas',          # 7月1日 13:00 CDT (UTC-5)
    '83': 'Atlanta',         # 7月2日 19:00 EDT (UTC-4)
    '84': 'Houston',         # 7月2日 12:00 CDT (UTC-5)
    '85': 'East Rutherford', # 7月2日 20:00 EDT (UTC-4) — NYC area
    '86': 'Miami',           # 7月3日 18:00 EDT (UTC-4)
    '87': 'Atlanta',         # 7月3日 20:30 EDT (UTC-4)
    '88': 'Dallas',          # 7月3日 13:00 CDT (UTC-5)
    # R16 venues (TBD — placeholders, will be wrong until real schedule fetched)
    '89': 'TBD', '90': 'TBD', '91': 'TBD', '92': 'TBD',
    '93': 'TBD', '94': 'TBD', '95': 'TBD', '96': 'TBD',
    '97': 'TBD', '98': 'TBD', '99': 'TBD', '100': 'TBD',
    '101': 'TBD', '102': 'TBD',
    '103': 'TBD', '104': 'TBD',
}

# Venue city → IANA timezone
VENUE_TZ = {
    'Atlanta': 'America/New_York',
    'East Rutherford': 'America/New_York',
    'Miami': 'America/New_York',
    'New York': 'America/New_York',
    'Boston': 'America/New_York',
    'Philadelphia': 'America/New_York',
    'Dallas': 'America/Chicago',
    'Houston': 'America/Chicago',
    'Kansas City': 'America/Chicago',
    'Los Angeles': 'America/Los_Angeles',
    'San Francisco': 'America/Los_Angeles',
    'Seattle': 'America/Los_Angeles',
    'Mexico City': 'America/Mexico_City',
    'Guadalajara': 'America/Mexico_City',
    'Monterrey': 'America/Mexico_City',
    'Toronto': 'America/Toronto',
    'Vancouver': 'America/Vancouver',
}


def venue_to_hkt(date_str: str, venue: str):
    """Convert 'MM/DD/YYYY HH:MM' venue local time → HKT datetime."""
    tz_name = VENUE_TZ.get(venue, 'America/New_York')
    naive = datetime.strptime(date_str, '%m/%d/%Y %H:%M')
    venue_dt = naive.replace(tzinfo=ZoneInfo(tz_name))
    return venue_dt.astimezone(ZoneInfo('Asia/Hong_Kong'))


def main():
    with open(INPUT) as f:
        data = json.load(f)
    matches = data.get('matches', {})

    # Load official schedule (Group Stage HKT)
    with open(OFFICIAL) as f:
        official = json.load(f)

    hkt_matches = {}

    for match_id, m in matches.items():
        hkt_iso = ''
        hkt_display = m.get('date', '')
        venue = ''
        source = 'unknown'

        date_str = m.get('date', '')
        home = m.get('home_team', '')
        away = m.get('away_team', '')
        match_type = m.get('type', '')

        # Group Stage: use official schedule
        if match_type == 'group':
            for entry in official:
                if entry.get('home') == home and entry.get('away') == away:
                    venue = entry.get('venue_stadium', '')
                    date_hkt = entry.get('date_hkt', '')
                    time_hkt = entry.get('time_hkt', '')
                    if date_hkt and time_hkt:
                        hkt_display = f"{date_hkt} {time_hkt} HKT"
                        try:
                            hkt_naive = datetime.strptime(
                                f"{date_hkt} {time_hkt}", "%Y-%m-%d %H:%M"
                            )
                            hkt_iso = hkt_naive.replace(
                                tzinfo=ZoneInfo('Asia/Hong_Kong')
                            ).isoformat()
                        except Exception:
                            pass
                        source = 'official_schedule_utc'
                    break
            else:
                source = 'group_no_official_match'

        # R32+: use hardcoded venue mapping
        elif match_type in ('r32', 'r16', 'qf', 'sf', 'final', 'third'):
            if match_id in R32_VENUES and R32_VENUES[match_id] != 'TBD':
                venue = R32_VENUES[match_id]
                try:
                    hkt_dt = venue_to_hkt(date_str, venue)
                    hkt_iso = hkt_dt.isoformat()
                    hkt_display = hkt_dt.strftime('%m/%d %H:%M HKT')
                    source = f'computed venue={venue} ({VENUE_TZ.get(venue)})'
                except Exception as e:
                    source = f'error: {e}'
            else:
                source = 'no_venue_mapping'

        hkt_matches[match_id] = {
            **m,
            'hkt_iso': hkt_iso,
            'hkt_display': hkt_display,
            'venue': venue,
            'source': source,
        }

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(
            {
                'generated_at': datetime.now().isoformat(),
                'matches': hkt_matches,
            },
            f, ensure_ascii=False, indent=2
        )

    # Summary
    n_official = sum(1 for v in hkt_matches.values() if v.get('source') == 'official_schedule_utc')
    n_computed = sum(1 for v in hkt_matches.values() if 'computed' in v.get('source', ''))
    n_no_venue = sum(1 for v in hkt_matches.values() if v.get('source') == 'no_venue_mapping')
    n_group_no = sum(1 for v in hkt_matches.values() if v.get('source') == 'group_no_official_match')

    print(f"Generated HKT schedule: {len(hkt_matches)} matches")
    print(f"  Official (Group Stage): {n_official}")
    print(f"  Computed (R32+): {n_computed}")
    print(f"  Group w/o official: {n_group_no}")
    print(f"  No venue mapping (R16+): {n_no_venue}")
    print(f"  Output: {OUTPUT}")

    # Show R32 HKT for verification
    print("\n=== R32 HKT preview ===")
    for k in sorted(R32_VENUES.keys()):
        if k in hkt_matches and 'computed' in hkt_matches[k].get('source', ''):
            v = hkt_matches[k]
            print(f"  #{k}: {v.get('date')} ({v.get('venue')}) → {v.get('hkt_display')}")


if __name__ == '__main__':
    main()
