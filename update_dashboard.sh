#!/bin/bash
# Football Dashboard Auto-Update Script
# 1. Fetch latest results via API
# 2. Regenerate HTML dashboard
# 3. Push to GitHub (Vercel auto-deploy)

set -e

BASE="/home/ubuntu/.openclaw/workspace-football"
cd "$BASE"

# Load API key from .env
export $(grep FOOTBALL_API_KEY .env | xargs)

echo "📊 Fetching latest results..."
python3 fetch_results_api.py

echo "🔄 Regenerating dashboard..."
python3 generate_html.py

echo "📤 Pushing to GitHub..."
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
git add -A
git commit -m "Auto-update dashboard via API - $TIMESTAMP"
git push origin main

echo "✅ Dashboard update complete!"
