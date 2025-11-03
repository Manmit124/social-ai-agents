"""
Test script for GitHub Data Collection (Day 2)

This script helps you test the GitHub data collection flow.

To test manually:
1. Run the backend server: python main.py
2. Use these curl commands or Postman:

# Step 1: Connect GitHub account (if not already connected)
# Go to: http://localhost:8000/api/auth/github/login
# (Requires JWT token in Authorization header)

# Step 2: Fetch GitHub data
curl -X POST http://localhost:8000/api/github/fetch-data \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# Step 3: Check GitHub status
curl -X GET http://localhost:8000/api/github/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Step 4: Get GitHub activity
curl -X GET "http://localhost:8000/api/github/activity?limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

Expected Results:
- fetch-data: Should return success with count of commits fetched
- status: Should show total_commits, last_fetch_time, needs_refresh
- activity: Should return list of commits with repository info

Database Verification:
Run these SQL queries in Supabase SQL Editor:

-- Check if tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('github_activity', 'github_data_fetch_log');

-- Check github_activity data
SELECT 
    repository_name,
    commit_message,
    commit_date,
    language
FROM github_activity
ORDER BY commit_date DESC
LIMIT 10;

-- Check fetch log
SELECT 
    last_fetch_time,
    last_commit_date,
    total_commits_fetched,
    fetch_type
FROM github_data_fetch_log
ORDER BY last_fetch_time DESC
LIMIT 5;

-- Count commits per repository
SELECT 
    repository_name,
    COUNT(*) as commit_count
FROM github_activity
GROUP BY repository_name
ORDER BY commit_count DESC;
"""

print(__doc__)

