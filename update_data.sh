#!/bin/bash
# Update NFL Dashboard Data - Runs both Vegas scraper and predictions

echo "🏈 NFL DASHBOARD DATA UPDATE"
echo "================================"
echo ""

# Step 1: Fetch Vegas lines (try advanced scraper first, fall back to standard)
echo "📊 Step 1: Fetching this weekend's Vegas lines..."
python3 scripts/fetch_vegas_lines_advanced.py
echo ""

# Step 2: Generate predictions
echo "🤖 Step 2: Generating model predictions..."
python3 scripts/fetch_nflfastr_data.py
echo ""

echo "✅ Data update complete!"
echo "📈 View dashboard: npm run dev"
echo "🌐 Open: http://localhost:3000"
echo ""
echo "💡 Tip: For live Vegas lines, sign up for a free API:"
echo "   - The-Odds-API: https://the-odds-api.com (500 requests/month free)"
