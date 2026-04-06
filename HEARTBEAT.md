# HEARTBEAT.md

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
