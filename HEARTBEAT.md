# HEARTBEAT.md

## ⚠️ Timezone Lesson (重要！2026-07-03)

**唔同地區有唔同時間！** 任何 World Cup schedule 處理都要小心：
- `real_results.json` 嘅 `date` 字段係 **venue local time** (EDT/CDT/MDT/PDT)
- **唔可以照搬**呢個 field 當 HKT 寫 message
- HKT = UTC+8，EDT = UTC-4，CDT = UTC-5，MDT = UTC-6，PDT = UTC-7
- **DST 期間 (6-11月)**：HKT = venue + 12 (EDT) / + 13 (CDT) / + 14 (MDT) / + 15 (PDT)

**Solution:** 用 `gen_hkt_schedule.py` pre-compute HKT time，sub-agent 直接 read `hkt_schedule.json` 入面 `hkt_display` 字段。
- Group Stage: 從 `official_schedule_utc.json` 攞 FIFA 官方 HKT
- R32+: hardcoded venue mapping + zoneinfo convert (見 gen_hkt_schedule.py R32_VENUES)

**Cron job:** `World Cup Daily Consolidated (12:00 HKT)` (jobId: `ce1867d0-1f2f-4059-a983-9b6bd3cb0454`)

## Pending Tasks

### Football Dashboard Enhancement (完整版)
- **Status**: In progress
- **Deadline**: Tomorrow
- **Details**:
  1. Add corner totals prediction (角球總數)
  2. Add half-time result prediction (半場結果)  
  3. Add head-to-head record display (對賽記錄)
  4. Add goal rate/ratio prediction (入球率)
  
- **Research needed**: 
  - Check if football-data.org API provides corner/half-time data
  - May need to fetch additional API data for new prediction types
  - Can use existing team_form data for some heuristics

### Database Changes Already Done
- ✅ Added `name_cn` column to `teams` table (45 teams translated)
- ✅ Added new prediction columns: `corners_over_prob`, `corners_under_prob`, `home_half_prob`, `away_half_prob`, `h2h_record`
- ✅ Updated `generate_html.py` to load team names from DB

### Key Files
- `/home/ubuntu/.openclaw/workspace-football/generate_html.py` - Dashboard
- `/home/ubuntu/.openclaw/workspace-football/predict.py` - Prediction model
- `/home/ubuntu/.openclaw/workspace-football/models/poisson.py` - Poisson model
- `/home/ubuntu/.openclaw/workspace-football/fetch_data.py` - Data fetcher
