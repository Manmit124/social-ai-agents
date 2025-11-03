"""
Test script for Day 3: Smart Refresh Logic

This script helps you test the smart refresh functionality.

To test manually:
1. Run the backend server: python main.py
2. Use these curl commands or test in the frontend:

# Test 1: Check GitHub Status (with refresh recommendations)
curl -X GET http://localhost:8000/api/github/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Expected Response:
{
  "success": true,
  "data": {
    "total_commits": 50,
    "last_fetch_time": "2024-01-15T10:30:00Z",
    "last_commit_date": "2024-01-14T15:20:00Z",
    "needs_refresh": false,
    "hours_since_fetch": 2.5,
    "refresh_reason": "Data is fresh (2.5 hours old)",
    "has_data": true,
    "repositories_count": 5,
    "repositories": ["repo1", "repo2", "repo3", "repo4", "repo5"]
  }
}

# Test 2: Check if Refresh is Needed (custom threshold)
curl -X GET "http://localhost:8000/api/github/refresh-check?hours_threshold=12" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Expected Response:
{
  "success": true,
  "data": {
    "should_refresh": false,
    "hours_since_fetch": 2.5,
    "last_fetch_time": "2024-01-15T10:30:00Z",
    "reason": "Data is fresh (2.5 hours old)"
  }
}

# Test 3: Fetch Data (incremental refresh)
curl -X POST http://localhost:8000/api/github/fetch-data \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

Expected Response (First Time):
{
  "success": true,
  "message": "Fetched 47 new commits from 5 repositories",
  "data": {
    "new_commits": 47,
    "skipped_duplicates": 0,
    "repositories_checked": 5,
    "fetch_type": "initial"
  }
}

Expected Response (Refresh):
{
  "success": true,
  "message": "Fetched 3 new commits from 5 repositories",
  "data": {
    "new_commits": 3,
    "skipped_duplicates": 44,
    "repositories_checked": 5,
    "fetch_type": "refresh"
  }
}

# Test 4: Get Activity
curl -X GET "http://localhost:8000/api/github/activity?limit=10&days=7" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Test Scenarios:
==============

Scenario 1: First Time User
---------------------------
1. User has never fetched data
2. Call GET /api/github/status
3. Expected: needs_refresh = true, reason = "No data fetched yet"
4. Call POST /api/github/fetch-data
5. Expected: fetch_type = "initial", new_commits > 0
6. Call GET /api/github/status again
7. Expected: needs_refresh = false, has_data = true

Scenario 2: Fresh Data
---------------------
1. User fetched data 2 hours ago
2. Call GET /api/github/status
3. Expected: needs_refresh = false, hours_since_fetch = 2.0
4. Reason: "Data is fresh (2.0 hours old)"

Scenario 3: Stale Data (> 24 hours)
----------------------------------
1. User fetched data 25 hours ago
2. Call GET /api/github/status
3. Expected: needs_refresh = true, hours_since_fetch = 25.0
4. Reason: "Data is 25.0 hours old (threshold: 24h)"
5. Call POST /api/github/fetch-data
6. Expected: Only new commits fetched (incremental)

Scenario 4: Custom Threshold
---------------------------
1. Call GET /api/github/refresh-check?hours_threshold=12
2. If data is 15 hours old:
   Expected: should_refresh = true
3. If data is 8 hours old:
   Expected: should_refresh = false

Frontend Testing:
================

1. Open Settings Page
2. You should see GitHubDataStatus component showing:
   - Status badge (Fresh/Needs Refresh/No Data)
   - Total commits count
   - Repositories count
   - Last updated time
   - Refresh button

3. Test Refresh Button:
   - Click "Refresh Data" or "Fetch GitHub Data"
   - Should show loading state
   - Should update status after completion
   - Should show success message

4. Test GitHubActivity component:
   - Should display recent commits
   - Filter by days (7, 30, 90, all)
   - Filter by limit (10, 25, 50, 100)
   - Should show repository name and language

Database Verification:
=====================

-- Check fetch log with timing
SELECT 
    last_fetch_time,
    last_commit_date,
    total_commits_fetched,
    fetch_type,
    EXTRACT(EPOCH FROM (NOW() - last_fetch_time))/3600 as hours_since_fetch
FROM github_data_fetch_log
ORDER BY last_fetch_time DESC
LIMIT 5;

-- Verify incremental fetch (no duplicates)
SELECT 
    commit_hash,
    COUNT(*) as count
FROM github_activity
GROUP BY commit_hash
HAVING COUNT(*) > 1;
-- Should return 0 rows (no duplicates)

-- Check commits by date
SELECT 
    DATE(commit_date) as date,
    COUNT(*) as commits_count
FROM github_activity
GROUP BY DATE(commit_date)
ORDER BY date DESC
LIMIT 10;

Success Criteria:
================
✅ Status endpoint returns accurate refresh recommendations
✅ Refresh check works with custom thresholds
✅ Initial fetch gets all commits (last 30 days)
✅ Incremental refresh only gets new commits
✅ No duplicate commits in database
✅ Frontend displays status correctly
✅ Refresh button works and updates UI
✅ Time ago displays correctly
✅ Activity list shows commits with filters
"""

print(__doc__)

