#!/bin/bash
# World Cup daily update — fetch results + gen HTML + git push
# Used by World Cup Daily Consolidated cron job
set +e  # 唔 exit on error — fetch 失敗都要繼續 gen + push (用 cache)
cd "$(dirname "$0")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Daily update start ==="

# Step 1: Fetch latest results (會用 cache fallback if API fail)
echo "[$(date '+%H:%M:%S')] Step 1/3: Fetching results..."
python3 fetch_results.py
FETCH_EXIT=$?
echo "[$(date '+%H:%M:%S')] fetch_results.py exit: $FETCH_EXIT"

# Step 2: Generate dashboard HTML
echo "[$(date '+%H:%M:%S')] Step 2/3: Generating dashboard HTML..."
python3 gen_wc.py
GEN_EXIT=$?
echo "[$(date '+%H:%M:%S')] gen_wc.py exit: $GEN_EXIT"

# Step 3: Git commit + push
echo "[$(date '+%H:%M:%S')] Step 3/3: Commit + push to GitHub..."
git add -A
if ! git diff --cached --quiet; then
    git commit -m "Auto update: $(date '+%m%d')"
    PUSH_RESULT=$(git push origin main 2>&1)
    PUSH_EXIT=$?
    echo "[$(date '+%H:%M:%S')] git push exit: $PUSH_EXIT"
    echo "$PUSH_RESULT"
else
    echo "[$(date '+%H:%M:%S')] No changes to commit"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Daily update done ==="
exit 0
