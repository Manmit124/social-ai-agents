# Personal Context Engine - Step-by-Step Development Plan

## Project Overview

**Goal:** Build an AI agent that reads your real-life data (GitHub activity, past Twitter posts) and generates personalized posts based on your actual work and writing style using Level 3 RAG with embeddings.

**Focus:** Learning AI agents, RAG, embeddings, semantic search - All on free tier ($0 cost)

**Tech Stack (All Free):**
- Backend: Render (free tier)
- Frontend: Vercel (free tier)
- Database: Supabase with pgvector (free tier: 500MB)
- Embeddings: HuggingFace sentence-transformers (free, runs locally)
- AI: Google Gemini (free tier)
- APIs: GitHub OAuth (free), Twitter API (already have access)

---

## Phase 1: GitHub Integration (Week 1)

### Day 1: GitHub OAuth Setup

#### Tool: GitHub Developer Portal
- **What:** Create GitHub OAuth application
- **Where:** https://github.com/settings/developers
- **Action:** Create new OAuth app
- **Settings needed:**
  - Application name: "AI Agents Tweet"
  - Homepage URL: Your frontend URL (localhost:3000 for dev)
  - Authorization callback URL: http://localhost:8000/api/auth/github/callback
- **Result:** Get Client ID and Client Secret

#### Tool: Backend - FastAPI
- **File to create:** `backend/services/social/github_service.py`
- **Methods to create:**
  1. `__init__()` - Initialize with Client ID, Secret, Redirect URI
  2. `get_authorization_url(state)` - Generate GitHub OAuth URL
  3. `exchange_code_for_token(code, state)` - Exchange code for access token
  4. `get_user_info(access_token)` - Get GitHub user info
  5. `get_repositories(access_token)` - Get user's repositories
  6. `get_commits(access_token, repo_owner, repo_name)` - Get commits from repo

#### Tool: Backend - main.py
- **Endpoint to add:** `GET /api/auth/github/login`
  - **Method:** Uses GitHub service `get_authorization_url()`
  - **Returns:** Authorization URL for frontend redirect
  - **Auth required:** Yes (user must be logged in)

- **Endpoint to add:** `GET /api/auth/github/callback`
  - **Method:** Receives code and state from GitHub
  - **Calls:** `exchange_code_for_token()`
  - **Calls:** `get_user_info()` to get username
  - **Stores:** Token in `connected_accounts` table
  - **Redirects:** To frontend settings page

#### Tool: Database - Supabase
- **Table to use:** `connected_accounts` (existing)
- **Action:** Add GitHub record when OAuth succeeds
- **Fields to store:**
  - platform: "github"
  - platform_user_id: GitHub username
  - platform_username: GitHub username
  - access_token: GitHub access token
  - is_active: true

#### Tool: Frontend - React
- **File to create:** `frontend/components/connections/ConnectGitHub.tsx`
- **Component structure:**
  - Button: "Connect GitHub"
  - Uses `useConnections` hook (similar to Twitter)
  - On click: Calls backend `/api/auth/github/login`
  - Redirects to GitHub OAuth page

#### Tool: Frontend - API Hook
- **File to update:** `frontend/hooks/api/useConnections.ts`
- **Method to add:** `connectGitHub()`
  - Calls backend endpoint
  - Handles redirect
  - Updates React Query cache

#### Example Flow:
1. User clicks "Connect GitHub"
2. Frontend calls backend `/api/auth/github/login`
3. Backend generates OAuth URL
4. User redirected to GitHub
5. User authorizes app
6. GitHub redirects to `/api/auth/github/callback?code=xxx`
7. Backend exchanges code for token
8. Backend stores token in database
9. Backend redirects to frontend settings page
10. Frontend shows "GitHub connected ✅"

---

### Day 2: GitHub Data Collection

#### Tool: Backend - GitHub Service
- **File to update:** `backend/services/social/github_service.py`
- **New methods to add:**

  1. `get_user_repositories(access_token)`
     - **What:** Get all user's repositories
     - **API endpoint:** `GET https://api.github.com/user/repos`
     - **Parameters:** `access_token` in Authorization header
     - **Returns:** List of repositories with: name, language, description, updated_at, etc.
     - **Handles:** Pagination (GitHub returns 30 per page)

  2. `get_repository_commits(access_token, owner, repo, since_date=None)`
     - **What:** Get commits from a repository
     - **API endpoint:** `GET https://api.github.com/repos/{owner}/{repo}/commits`
     - **Parameters:** 
       - `since`: ISO date (if provided, only commits after this date)
       - `per_page`: 100 (max)
     - **Returns:** List of commits with: sha, message, date, author
     - **Important:** Parse commit message from nested structure

  3. `get_user_info(access_token)`
     - **What:** Get authenticated user's info
     - **API endpoint:** `GET https://api.github.com/user`
     - **Returns:** username, name, email, etc.

  4. `batch_fetch_commits(access_token, repos, since_date=None)`
     - **What:** Fetch commits from multiple repos efficiently
     - **Method:** Uses async/await to fetch multiple repos in parallel
     - **Returns:** Combined list of all commits
     - **Optimization:** Fetch repos simultaneously, not one by one

#### Tool: Backend - main.py
- **New endpoint:** `POST /api/github/fetch-data`
  - **Auth required:** Yes (JWT token)
  - **What it does:**
    1. Gets user's GitHub token from database
    2. Calls `get_user_repositories()` to get all repos
    3. For each repo, calls `get_repository_commits()`
    4. Filters commits from last 30 days
    5. Stores commits in `github_activity` table
    6. Updates `github_data_fetch_log` table
  - **Returns:** Success message with count of commits fetched

#### Tool: Database - Supabase
- **Table to create:** `github_activity`
  - **Fields:**
    - `id` (UUID, primary key)
    - `user_id` (UUID, foreign key to auth.users)
    - `repository_name` (TEXT)
    - `commit_hash` (TEXT, unique - prevents duplicates)
    - `commit_message` (TEXT)
    - `commit_date` (TIMESTAMP)
    - `language` (TEXT - from repository)
    - `raw_data` (JSONB - full API response)
    - `collected_at` (TIMESTAMP, default NOW())
  - **Indexes:** 
    - Index on `user_id` for fast queries
    - Index on `commit_date` for time-based queries
    - Unique constraint on `commit_hash` to prevent duplicates

- **Table to create:** `github_data_fetch_log`
  - **Fields:**
    - `id` (UUID, primary key)
    - `user_id` (UUID, foreign key)
    - `last_fetch_time` (TIMESTAMP)
    - `last_commit_date` (TIMESTAMP - most recent commit collected)
    - `total_commits_fetched` (INT)
    - `fetch_type` (TEXT - "initial", "refresh", "manual")
    - `created_at` (TIMESTAMP)

#### Tool: Backend - Database Service
- **File to create:** `backend/services/github_data_service.py`
- **Methods to create:**

  1. `save_github_commits(user_id, commits_data)`
     - **What:** Save commits to database
     - **Logic:** 
       - For each commit, check if `commit_hash` exists
       - If exists: Skip (don't duplicate)
       - If new: Insert with all fields
     - **Returns:** Count of new commits saved

  2. `get_user_github_activity(user_id, limit=100)`
     - **What:** Get user's stored GitHub activity
     - **Query:** Order by `commit_date` DESC, limit results
     - **Returns:** List of commits from database

  3. `update_fetch_log(user_id, last_commit_date, total_count, fetch_type)`
     - **What:** Update fetch log after data collection
     - **Logic:** Insert or update log entry

#### Example Flow:
1. User clicks "Fetch GitHub Data" button
2. Frontend calls `POST /api/github/fetch-data`
3. Backend gets user's GitHub token from `connected_accounts`
4. Backend calls GitHub API: Get all repos
5. Backend calls GitHub API: Get commits from each repo (parallel)
6. Backend filters: Only commits from last 30 days
7. Backend saves to `github_activity` table (skip duplicates)
8. Backend updates `github_data_fetch_log`
9. Returns: "Fetched 47 new commits"

---

### Day 3: Smart Refresh Logic

#### Tool: Backend - GitHub Service
- **File to update:** `backend/services/social/github_service.py`
- **New method:**

  `get_commits_since_date(access_token, owner, repo, since_date)`
  - **What:** Only fetch commits after a specific date
  - **Method:** Use GitHub API `since` parameter
  - **Why:** Efficient - only get new commits, not all history

#### Tool: Backend - Data Service
- **File to update:** `backend/services/github_data_service.py`
- **New methods:**

  1. `get_last_fetch_info(user_id)`
     - **What:** Get user's last fetch information
     - **Returns:** `last_commit_date`, `last_fetch_time`, `fetch_count`
     - **Purpose:** Know when to refresh

  2. `should_refresh_data(user_id, hours_threshold=24)`
     - **What:** Check if data needs refresh
     - **Logic:** 
       - Get last fetch time
       - If > 24 hours old: Return true
       - Else: Return false
     - **Returns:** Boolean

  3. `get_last_commit_date(user_id)`
     - **What:** Get most recent commit date from stored data
     - **Query:** MAX(commit_date) from github_activity
     - **Returns:** Date or None

#### Tool: Backend - main.py
- **Endpoint to update:** `POST /api/github/fetch-data`
- **New logic:**
  1. Check `get_last_fetch_info(user_id)`
  2. If first time: Fetch last 30 days (full fetch)
  3. If has data: Get `last_commit_date`
  4. Fetch only commits AFTER `last_commit_date` (incremental)
  5. Save only new commits
  6. Update fetch log

- **New endpoint:** `GET /api/github/status`
  - **What:** Get data freshness info
  - **Returns:**
    - `last_fetch_time`: When last fetched
    - `total_commits`: Count of stored commits
    - `needs_refresh`: Boolean (if > 24 hours old)
    - `last_commit_date`: Most recent commit date

#### Tool: Frontend - React
- **File to create:** `frontend/components/github/GitHubDataStatus.tsx`
- **Component shows:**
  - "Last updated: 2 hours ago"
  - Button: "Refresh Data"
  - Total commits count
  - Status badge: "Fresh" or "Needs Refresh"

- **File to update:** `frontend/hooks/api/useGitHub.ts`
- **New hooks:**
  - `useGitHubStatus()` - Get fetch status
  - `useFetchGitHubData()` - Mutation to fetch data
  - Auto-suggests refresh if data stale

#### Example Flow:
**First time:**
1. User clicks "Fetch Data"
2. Backend: No previous fetch → Full fetch (30 days)
3. Saves 200 commits
4. Updates log: `last_fetch_time = now`, `last_commit_date = latest commit`

**Second time (next day):**
1. User clicks "Refresh"
2. Backend: Check `last_commit_date` = "2024-01-15"
3. Fetch commits AFTER "2024-01-15"
4. Finds 5 new commits
5. Saves only those 5
6. Updates log with new date

**Automatic suggestion:**
1. Frontend checks status every time user opens page
2. If `last_fetch_time` > 24 hours → Show: "Your data is 25 hours old, refresh?"
3. User can click to refresh

---

### Day 4: GitHub Data Analysis

#### Tool: Backend - Analysis Service
- **File to create:** `backend/services/github_analysis_service.py`
- **Methods to create:**

  1. `get_current_projects(user_id, days=7)`
     - **What:** Find most active repositories
     - **Logic:**
       - Get commits from last 7 days
       - Count commits per repository
       - Sort by count DESC
       - Return top 5 repos
     - **Returns:** List of: `[{"repo": "ai-project", "commits": 12}, ...]`

  2. `get_tech_stack(user_id)`
     - **What:** Identify technologies used
     - **Logic:**
       - Get all unique `language` values from commits
       - Get unique languages from repositories
       - Combine and count frequency
     - **Returns:** List: `["Python", "TypeScript", "React", ...]`

  3. `identify_major_commits(user_id, days=30)`
     - **What:** Filter out minor commits, keep significant ones
     - **Logic:**
       - Get commits from database
       - Filter keywords:
         - Keep: "Added", "Created", "Implemented", "Merged", "Released"
         - Skip: "Fixed typo", "Updated readme", "Code cleanup"
       - Return filtered list
     - **Returns:** List of major commits only

  4. `get_recent_focus(user_id, days=7)`
     - **What:** Summarize what user worked on recently
     - **Logic:**
       - Get commits from last 7 days
       - Extract common themes from commit messages
       - Group by repository
       - Create summary text
     - **Returns:** String like: "Working on API endpoints and database optimization in ai-project"

  5. `calculate_activity_stats(user_id)`
     - **What:** Calculate activity metrics
     - **Returns:**
       - `commits_last_7_days`: Count
       - `commits_last_30_days`: Count
       - `most_active_day`: Day of week
       - `most_active_time`: Hour of day
       - `average_commits_per_day`: Float

#### Tool: Database - Supabase
- **Table to create:** `user_context` (if not exists)
  - **Fields:**
    - `id` (UUID, primary key)
    - `user_id` (UUID, foreign key, unique)
    - `current_projects` (TEXT[] - array of repo names)
    - `tech_stack` (TEXT[] - array of languages)
    - `recent_activity_summary` (TEXT)
    - `last_github_fetch` (TIMESTAMP)
    - `last_twitter_fetch` (TIMESTAMP)
    - `last_updated` (TIMESTAMP)
  - **Index:** On `user_id` for fast lookup

#### Tool: Backend - Context Service
- **File to create:** `backend/services/context_service.py`
- **Methods to create:**

  1. `update_user_context(user_id)`
     - **What:** Rebuild user context from latest data
     - **Logic:**
       1. Call `get_current_projects()` → Store in context
       2. Call `get_tech_stack()` → Store in context
       3. Call `get_recent_focus()` → Store summary
       4. Update `last_github_fetch` timestamp
       5. Save to `user_context` table
     - **Runs:** After every data fetch

  2. `get_user_context(user_id)`
     - **What:** Get stored user context
     - **Returns:** Context object with all fields
     - **Purpose:** Fast access without recalculating

#### Tool: Backend - main.py
- **New endpoint:** `GET /api/github/context`
  - **What:** Get user's GitHub context summary
  - **Returns:**
    - `current_projects`: Array
    - `tech_stack`: Array
    - `recent_activity`: Summary text
    - `activity_stats`: Metrics object
  - **Use:** Display on frontend dashboard

- **New endpoint:** `GET /api/github/analysis`
  - **What:** Get detailed analysis
  - **Returns:**
    - `major_commits`: List of significant commits
    - `project_breakdown`: Commits per project
    - `timeline`: Activity over time

#### Tool: Frontend - React
- **File to create:** `frontend/components/github/GitHubContext.tsx`
- **Component displays:**
  - Current projects (cards with commit counts)
  - Tech stack (badges)
  - Recent activity summary
  - Activity chart (optional)

#### Example Flow:
1. User fetches GitHub data
2. Backend saves commits to database
3. Backend automatically calls `update_user_context()`
4. Analysis service runs:
   - Finds: Top 3 projects = ["ai-project", "blog", "api"]
   - Finds: Tech stack = ["Python", "React", "TypeScript"]
   - Creates summary: "Working on ML features in ai-project"
5. Saves to `user_context` table
6. Frontend can fetch and display context instantly

---

### Day 5: Testing and Refinement

#### Tool: Manual Testing
- **Test cases:**

  1. **OAuth Flow:**
     - Connect GitHub account
     - Verify token stored in database
     - Test token refresh if needed

  2. **Data Fetching:**
     - Fetch initial data (should get 30 days)
     - Verify commits saved in database
     - Check for duplicates (same commit hash shouldn't be stored twice)

  3. **Refresh Logic:**
     - Wait 1 hour, refresh (should only get new commits)
     - Verify no duplicates
     - Check fetch log updated

  4. **Analysis:**
     - Check context generated correctly
     - Verify tech stack identified
     - Check major commits filtered properly

  5. **Edge Cases:**
     - User with no commits
     - User with private repos (may need different scopes)
     - API rate limiting (GitHub allows 5000 requests/hour)

#### Tool: Backend - Error Handling
- **Scenarios to handle:**

  1. **GitHub API errors:**
     - Rate limit exceeded (429) → Return error, suggest retry later
     - Invalid token (401) → Prompt user to reconnect
     - Network errors → Retry with exponential backoff

  2. **Data errors:**
     - Missing required fields → Skip invalid records, log warning
     - Duplicate commits → Skip silently (expected behavior)

  3. **Database errors:**
     - Connection issues → Retry logic
     - Constraint violations → Handle gracefully

#### Tool: Frontend - User Experience
- **Improvements:**
  - Loading states during fetch
  - Progress indicator for large fetches
  - Error messages if fetch fails
  - Success notifications
  - Data visualization (charts/graphs)

---

## Phase 2: Twitter Reading and Analysis (Week 2)

### Day 1: Twitter Reading API

#### Tool: Backend - Twitter Service (Update)
- **File to update:** `backend/services/social/twitter_service.py`
- **New methods to add:**

  1. `get_user_tweets(access_token, max_results=100)`
     - **What:** Get user's past tweets
     - **API endpoint:** `GET /2/users/me/tweets`
     - **Parameters:**
       - `max_results`: 100 (max per request)
       - `tweet.fields`: "created_at,public_metrics"
       - `expansions`: For user info
     - **Handles:** Pagination with `next_token`
     - **Returns:** List of tweets with: id, text, created_at, metrics

  2. `get_tweet_metrics(access_token, tweet_ids)`
     - **What:** Get engagement metrics for tweets
     - **Note:** Metrics included in `get_user_tweets` response
     - **Returns:** Likes, retweets, replies counts

  3. `batch_fetch_all_tweets(access_token, limit=100)`
     - **What:** Fetch multiple pages of tweets
     - **Logic:**
       - Call `get_user_tweets()` first time
       - If `next_token` exists, call again with pagination
       - Continue until limit reached or no more tweets
     - **Returns:** All tweets (up to limit)

#### Tool: Database - Supabase
- **Table to create:** `twitter_activity`
  - **Fields:**
    - `id` (UUID, primary key)
    - `user_id` (UUID, foreign key)
    - `tweet_id` (TEXT, unique)
    - `tweet_text` (TEXT)
    - `posted_at` (TIMESTAMP)
    - `likes_count` (INT)
    - `retweets_count` (INT)
    - `replies_count` (INT)
    - `hashtags_used` (TEXT[] - extracted from tweet)
    - `mentions_used` (TEXT[] - @mentions)
    - `raw_data` (JSONB)
    - `collected_at` (TIMESTAMP)
  - **Indexes:**
    - Index on `user_id`
    - Index on `posted_at` for time queries
    - Unique on `tweet_id`

- **Table to create:** `twitter_data_fetch_log`
  - **Fields:**
    - `id` (UUID)
    - `user_id` (UUID)
    - `last_fetch_time` (TIMESTAMP)
    - `last_tweet_id` (TEXT - most recent tweet collected)
    - `total_tweets_fetched` (INT)
    - `fetch_type` (TEXT)

#### Tool: Backend - Data Service
- **File to create:** `backend/services/twitter_data_service.py`
- **Methods to create:**

  1. `save_twitter_tweets(user_id, tweets_data)`
     - **What:** Save tweets to database
     - **Logic:** Check for duplicate `tweet_id`, skip if exists
     - **Extracts:** Hashtags and mentions from tweet text
     - **Returns:** Count of new tweets saved

  2. `get_user_tweets_from_db(user_id, limit=100)`
     - **What:** Get stored tweets
     - **Returns:** List ordered by `posted_at` DESC

  3. `update_twitter_fetch_log(user_id, last_tweet_id, total_count)`
     - **What:** Update fetch log

#### Tool: Backend - main.py
- **New endpoint:** `POST /api/twitter/fetch-tweets`
  - **Auth required:** Yes
  - **What it does:**
    1. Get user's Twitter token
    2. Call `batch_fetch_all_tweets()` (get last 100 tweets)
    3. Save to `twitter_activity` table
    4. Update fetch log
  - **Returns:** Count of tweets fetched

#### Example Flow:
1. User clicks "Fetch My Tweets"
2. Backend gets Twitter access token (already have from OAuth)
3. Backend calls Twitter API: Get user's tweets (last 100)
4. Backend parses response:
   - Extract: tweet text, date, likes, retweets
   - Extract: hashtags (#AI, #Python)
   - Extract: mentions (@username)
5. Save to `twitter_activity` table
6. Update `twitter_data_fetch_log`
7. Returns: "Fetched 87 tweets"

---

### Day 2: Tweet Style Analysis

#### Tool: Backend - Analysis Service
- **File to create:** `backend/services/twitter_analysis_service.py`
- **Methods to create:**

  1. `analyze_tweet_length(tweets)`
     - **What:** Calculate average tweet length
     - **Logic:**
       - Get all tweet texts
       - Calculate length for each
       - Calculate average, min, max
     - **Returns:** `{"average": 120, "min": 45, "max": 280}`

  2. `analyze_tone(tweets)`
     - **What:** Detect writing tone
     - **Logic:**
       - Analyze language patterns:
         - Exclamation marks → Enthusiastic
         - Technical terms → Professional
         - Casual words → Casual
         - Question marks → Curious
       - Use keyword detection or simple heuristics
     - **Returns:** `"casual_professional"` or `"enthusiastic"` etc.

  3. `analyze_emoji_usage(tweets)`
     - **What:** Check if user uses emojis
     - **Logic:**
       - Count tweets with emojis
       - Calculate percentage
       - Identify common emojis used
     - **Returns:** `{"uses_emojis": true, "percentage": 65, "common": ["🚀", "✨", "💡"]}`

  4. `extract_topics(tweets)`
     - **What:** Identify common topics
     - **Logic:**
       - Extract hashtags used
       - Count frequency
       - Identify common words (excluding stop words)
     - **Returns:** List of topics: `["AI", "Python", "Web Development"]`

  5. `analyze_engagement_patterns(tweets)`
     - **What:** Find what content performs best
     - **Logic:**
       - Calculate average engagement (likes + retweets)
       - Find top 10 performing tweets
       - Extract patterns:
         - Topics that perform well
         - Length that performs well
         - Time of day
     - **Returns:** `{"best_topics": [...], "best_length": 120, "best_time": "10am"}`

  6. `generate_style_profile(user_id)`
     - **What:** Create complete style profile
     - **Logic:**
       - Call all analysis methods
       - Combine results
       - Save to `twitter_style_profile` table
     - **Returns:** Complete profile object

#### Tool: Database - Supabase
- **Table to create:** `twitter_style_profile`
  - **Fields:**
    - `id` (UUID)
    - `user_id` (UUID, unique)
    - `average_length` (INT)
    - `min_length` (INT)
    - `max_length` (INT)
    - `tone` (TEXT)
    - `uses_emojis` (BOOLEAN)
    - `emoji_percentage` (INT)
    - `common_emojis` (TEXT[])
    - `common_hashtags` (TEXT[])
    - `preferred_topics` (TEXT[])
    - `best_performing_content` (JSONB - patterns)
    - `last_updated` (TIMESTAMP)

#### Tool: Backend - main.py
- **New endpoint:** `GET /api/twitter/style-profile`
  - **What:** Get user's Twitter style profile
  - **Returns:** Complete style analysis

- **Update endpoint:** `POST /api/twitter/fetch-tweets`
  - **After saving tweets:** Automatically call `generate_style_profile()`

#### Tool: Frontend - React
- **File to create:** `frontend/components/twitter/TwitterStyleProfile.tsx`
- **Component shows:**
  - Writing style summary
  - Average tweet length
  - Tone indicator
  - Common emojis/hashtags
  - Best performing topics

#### Example Flow:
1. User fetches tweets (Day 1)
2. Tweets saved to database
3. Backend automatically runs analysis:
   - Calculates: Average length = 125 chars
   - Detects: Tone = "Casual professional"
   - Finds: Uses emojis 70% of time
   - Extracts: Top topics = ["AI", "Python", "Tech"]
   - Identifies: Best posts are about "AI tutorials"
4. Saves to `twitter_style_profile` table
5. Frontend can display style profile
6. This profile used later for content generation

---

### Day 3: Best Performing Content Analysis

#### Tool: Backend - Analysis Service (Update)
- **File to update:** `backend/services/twitter_analysis_service.py`
- **New methods:**

  1. `identify_top_performing_tweets(user_id, top_n=10)`
     - **What:** Find tweets with highest engagement
     - **Logic:**
       - Get all tweets from database
       - Calculate engagement score: `likes + (retweets * 2)`
       - Sort by score DESC
       - Return top N
     - **Returns:** List of best tweets

  2. `analyze_winning_patterns(top_tweets)`
     - **What:** Find patterns in successful tweets
     - **Logic:**
       - Analyze top tweets:
         - Common topics
         - Average length
         - Common hashtags
         - Time posted
         - Presence of questions
         - Use of emojis
     - **Returns:** Patterns object

  3. `compare_with_average(top_tweets, all_tweets)`
     - **What:** See what's different about best tweets
     - **Returns:** Insights like "Best tweets are 20% longer than average"

  4. `generate_content_recommendations(user_id)`
     - **What:** Suggest content ideas based on success
     - **Logic:**
       - Use winning patterns
       - Suggest: "Post about AI topics, use emojis, keep length ~140 chars"
     - **Returns:** Recommendations text

#### Tool: Backend - main.py
- **New endpoint:** `GET /api/twitter/insights`
  - **What:** Get content performance insights
  - **Returns:**
    - Top performing tweets
    - Winning patterns
    - Recommendations

#### Tool: Database - Update
- **Table to update:** `user_context`
- **Add field:** `best_performing_content` (JSONB)
  - Stores: Top tweets, patterns, recommendations

#### Tool: Frontend - React
- **File to create:** `frontend/components/twitter/TwitterInsights.tsx`
- **Component shows:**
  - Chart: Engagement over time
  - List: Top 5 tweets
  - Card: "What works best"
  - Recommendations panel

#### Example Flow:
1. User has 200 tweets in database
2. Backend analyzes:
   - Finds top 10 tweets (by engagement)
   - Identifies: Best tweets average 145 chars (vs 120 average)
   - Finds: 80% of top tweets mention "AI"
   - Finds: Top tweets posted Tuesday mornings
3. Generates recommendations:
   - "Your best content is about AI, keep posts ~145 chars"
   - "Post on Tuesdays at 10am for best engagement"
4. Saves to `user_context` table
5. Used later to guide content generation

---

## Phase 3: Level 3 RAG with Embeddings (Week 3)

### Day 1: Embedding Setup

#### Tool: Python Library
- **Package to install:** `sentence-transformers`
  - **Command:** `pip install sentence-transformers`
  - **What it does:** Provides embedding models
  - **Free:** Yes, open source

#### Tool: Backend - Embedding Service
- **File to create:** `backend/services/embedding_service.py`
- **Methods to create:**

  1. `__init__()`
     - **What:** Initialize embedding model
     - **Model to use:** `all-MiniLM-L6-v2`
       - **Why:** Small (80MB), fast, good quality
       - **Dimensions:** 384 (output vector size)
       - **Memory:** ~200MB RAM
     - **Logic:** Load model on service initialization (one time)
     - **Caching:** Model stays in memory for reuse

  2. `generate_embedding(text)`
     - **What:** Convert text to embedding vector
     - **Input:** String (commit message, tweet text, etc.)
     - **Process:**
       1. Model encodes text
       2. Returns numpy array of 384 numbers
       3. Convert to list format
     - **Returns:** List of 384 floats: `[0.23, -0.45, 0.67, ...]`
     - **Example:**
       - Input: "Added ML prediction endpoint"
       - Output: `[0.234, -0.456, 0.678, ...]` (384 numbers)

  3. `generate_embeddings_batch(texts)`
     - **What:** Generate embeddings for multiple texts efficiently
     - **Input:** List of strings
     - **Why:** Faster than one-by-one
     - **Returns:** List of embedding vectors

  4. `calculate_similarity(embedding1, embedding2)`
     - **What:** Calculate cosine similarity between two embeddings
     - **Returns:** Float between 0 and 1 (1 = identical, 0 = unrelated)
     - **Use:** Compare similarity of texts

#### Tool: Testing
- **Test cases:**
  1. Generate embedding for sample text
  2. Verify output is 384 dimensions
  3. Test batch generation (10 texts at once)
  4. Test similarity: "API endpoint" vs "Created API" should be high (>0.8)

#### Example Flow:
1. Backend starts up
2. `EmbeddingService` initialized
3. Model `all-MiniLM-L6-v2` downloaded (first time, ~80MB)
4. Model loaded into memory (~200MB RAM)
5. Ready to generate embeddings

**Usage:**
- Input: "Added ML prediction endpoint"
- Call: `generate_embedding()`
- Output: Vector of 384 numbers
- Store: Ready for vector database

---

### Day 2: Supabase pgvector Setup

#### Tool: Database - Supabase SQL Editor
- **Step 1: Enable extension**
  - **SQL:** `CREATE EXTENSION IF NOT EXISTS vector;`
  - **What:** Enables vector operations in PostgreSQL
  - **Runs:** Once per database

#### Tool: Database - Update Tables
- **Table to update:** `github_activity`
- **Add column:**
  ```sql
  ALTER TABLE github_activity 
  ADD COLUMN embedding vector(384);
  ```
  - **Type:** `vector(384)` - 384 dimensions (matches model)
  - **Nullable:** Yes (not all commits have embeddings yet)

#### Tool: Database - Create Index
- **Index for similarity search:**
  ```sql
  CREATE INDEX github_activity_embedding_idx 
  ON github_activity 
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
  ```
  - **Type:** `ivfflat` - Fast approximate search
  - **Distance:** `vector_cosine_ops` - Cosine similarity
  - **Lists:** 100 (for clustering, adjust based on data size)
  - **Why:** Makes similarity search fast

#### Tool: Database Service
- **File to update:** `backend/services/github_data_service.py`
- **New methods:**

  1. `save_commit_embedding(user_id, commit_hash, embedding)`
     - **What:** Store embedding in database
     - **SQL:** UPDATE github_activity SET embedding = ? WHERE commit_hash = ?
     - **Note:** Embedding must be PostgreSQL vector format

  2. `get_commits_with_embeddings(user_id)`
     - **What:** Get commits that have embeddings
     - **Query:** WHERE embedding IS NOT NULL
     - **Returns:** Commits ready for search

  3. `get_embedding_for_commit(commit_hash)`
     - **What:** Get stored embedding for a commit
     - **Use:** For testing/debugging

#### Tool: Testing
- **Test cases:**
  1. Verify extension enabled: `SELECT * FROM pg_extension WHERE extname = 'vector';`
  2. Insert test embedding: Verify vector column accepts array
  3. Test index: Query should use index (check EXPLAIN)

#### Example Flow:
1. Open Supabase SQL editor
2. Run: `CREATE EXTENSION IF NOT EXISTS vector;`
3. Verify: Extension created
4. Update table: Add `embedding vector(384)` column
5. Create index: For fast similarity search
6. Ready to store embeddings!

---

### Day 3: Generate and Store Embeddings

#### Tool: Backend - Embedding Job
- **File to create:** `backend/services/embedding_job_service.py`
- **Methods to create:**

  1. `generate_embeddings_for_user(user_id)`
     - **What:** Generate embeddings for all user's commits that don't have them
     - **Logic:**
       1. Get commits from `github_activity` WHERE embedding IS NULL
       2. For each commit:
          - Get `commit_message` text
          - Call `embedding_service.generate_embedding()`
          - Save embedding to database
       3. Process in batches (50 at a time for efficiency)
     - **Returns:** Count of embeddings generated

  2. `generate_embedding_for_new_commits(user_id)`
     - **What:** Only generate for commits added since last run
     - **Logic:**
       - Get commits WHERE embedding IS NULL AND collected_at > last_run
       - Generate embeddings for these only
     - **Use:** After data refresh

  3. `get_embedding_status(user_id)`
     - **What:** Check embedding generation progress
     - **Returns:**
       - `total_commits`: Count of all commits
       - `commits_with_embeddings`: Count with embeddings
       - `commits_needing_embeddings`: Count without embeddings
       - `percentage_complete`: Float

#### Tool: Backend - main.py
- **New endpoint:** `POST /api/embeddings/generate`
  - **Auth required:** Yes
  - **What:** Trigger embedding generation
  - **Process:**
    1. Get user's commits without embeddings
    2. Generate embeddings (batch process)
    3. Save to database
    4. Return status
  - **Returns:** Count generated, status message

- **New endpoint:** `GET /api/embeddings/status`
  - **What:** Check embedding generation status
  - **Returns:** Status object with counts and percentage

#### Tool: Background Processing
- **Option 1: Synchronous** (for small datasets)
  - Generate embeddings in request handler
  - User waits for completion
  - Simple but may timeout for large datasets

- **Option 2: Async job** (recommended)
  - Start job, return immediately
  - Process in background
  - User can check status
  - Better UX for large datasets

#### Tool: Error Handling
- **Scenarios:**
  1. Model not loaded → Initialize on first use
  2. Memory error → Process smaller batches
  3. Database error → Retry with backoff
  4. Invalid text → Skip or handle empty strings

#### Example Flow:
1. User has 200 commits in database
2. None have embeddings yet (embedding IS NULL)
3. User clicks "Generate Embeddings"
4. Backend:
   - Gets 200 commits
   - Processes in batches of 50:
     - Batch 1: Commits 1-50 → Generate embeddings → Save
     - Batch 2: Commits 51-100 → Generate embeddings → Save
     - ... (4 batches total)
   - All embeddings saved
5. Status: "200/200 embeddings generated (100%)"
6. Ready for semantic search!

---

### Day 4: Semantic Search Implementation

#### Tool: Backend - Search Service
- **File to create:** `backend/services/semantic_search_service.py`
- **Methods to create:**

  1. `search_similar_commits(user_id, query_text, limit=5)`
     - **What:** Find commits similar to query
     - **Process:**
       1. Convert `query_text` to embedding using `embedding_service`
       2. Query database using pgvector similarity search
       3. SQL query:
          ```sql
          SELECT *, embedding <-> query_embedding AS distance
          FROM github_activity
          WHERE user_id = ? AND embedding IS NOT NULL
          ORDER BY distance ASC
          LIMIT ?
          ```
       4. `distance` = cosine distance (lower = more similar)
       5. Convert distance to similarity score: `1 - distance`
     - **Returns:** List of commits with similarity scores

  2. `search_by_topic(user_id, topic, limit=5)`
     - **What:** Find commits about a specific topic
     - **Example:** "API work", "bug fixes", "new features"
     - **Uses:** `search_similar_commits()` with topic as query

  3. `search_by_work_context(user_id, context_description, limit=5)`
     - **What:** Find commits related to work context
     - **Example:** "What have I been working on with APIs?"
     - **Returns:** Relevant commits

  4. `get_most_relevant_for_generation(user_id, user_prompt)`
     - **What:** Get best commits for content generation context
     - **Logic:**
       - Search for commits similar to user prompt
       - Combine with time-based filtering (prefer recent)
       - Prioritize major commits (not bug fixes)
       - Return top 3-5 most relevant
     - **Returns:** Curated list of commits

#### Tool: Backend - main.py
- **New endpoint:** `POST /api/search/commits`
  - **Auth required:** Yes
  - **Body:** `{"query": "API work", "limit": 5}`
  - **Returns:**
    - List of commits
    - Each with: commit_message, repository, similarity_score, date

- **New endpoint:** `GET /api/search/commits/topic/:topic`
  - **Query params:** topic (e.g., "API", "ML", "bug")
  - **Returns:** Commits about that topic

#### Tool: Testing
- **Test queries:**
  1. "API endpoint" → Should find commits with "API", "endpoint", "service"
  2. "machine learning" → Should find "ML", "prediction", "model"
  3. "bug fix" → Should find "fixed", "resolved", "patch"

#### Example Flow:
**Scenario: User wants to post about their API work**

1. User prompt: "Generate tweet about my API work"
2. Backend receives prompt
3. Search service:
   - Converts "API work" to embedding: `[0.24, -0.44, ...]`
   - Queries database: Find commits with similar embeddings
   - SQL finds:
     - "Added ML prediction endpoint" (similarity: 0.92)
     - "Created API service" (similarity: 0.88)
     - "Built REST endpoint" (similarity: 0.85)
     - "Fixed API bug" (similarity: 0.78)
   - Returns top 3
4. These commits used as context for generation

---

### Day 5: RAG Integration

#### Tool: Backend - Context Builder
- **File to create:** `backend/services/rag_context_builder.py`
- **Methods to create:**

  1. `build_context_for_generation(user_id, user_prompt)`
     - **What:** Build complete context for AI generation
     - **Process:**
       1. **Semantic search:** Find relevant commits using user prompt
       2. **Get style profile:** Get Twitter style from database
       3. **Get user context:** Get current projects, tech stack
       4. **Combine:** Build structured context object
     - **Returns:** Context object ready for prompt

  2. `format_context_for_prompt(context)`
     - **What:** Format context as text for AI prompt
     - **Structure:**
       ```
       User's Current Work (from GitHub):
       - Recent commit: "Added ML prediction endpoint" (yesterday)
       - Active project: ai-project
       - Tech stack: Python, FastAPI
       
       User's Writing Style (from Twitter):
       - Tone: Casual professional
       - Average length: 125 characters
       - Uses emojis: Yes (🚀, ✨)
       - Best topics: AI, Python, Tech
       
       User's Recent Activity:
       - Working on API endpoints
       - Most active: ai-project repository
       ```
     - **Returns:** Formatted context string

#### Tool: Backend - Generation Service (Update)
- **File to update:** `backend/agent/nodes.py` (or generation node)
- **Update method:** `generate_node()` or content generation function

**New logic:**
1. Before generation:
   - Call `rag_context_builder.build_context_for_generation()`
   - Get relevant commits, style profile, user context
2. Format context into prompt
3. Augment AI prompt with context:
   ```
   Original prompt: "Generate a tweet about AI"
   
   Augmented prompt:
   "Context about the user:
   [formatted context here]
   
   Generate a tweet about AI that:
   - Mentions their actual work (ML prediction endpoint)
   - Matches their style (casual, ~125 chars, uses emojis)
   - References their tech stack (Python, FastAPI)"
   ```
4. Generate with Gemini API (existing)
5. Result: Personalized content

#### Tool: Backend - main.py
- **Update endpoint:** `POST /api/generate`
- **New flow:**
  1. User sends: `{"prompt": "Post about my work", "platform": "twitter"}`
  2. Backend:
     - Calls `build_context_for_generation()`
     - Gets relevant commits, style, context
     - Formats for prompt
     - Calls agent with augmented context
     - Agent generates personalized content
  3. Returns: Generated content matching user's style and work

#### Tool: Testing
- **Test scenarios:**
  1. Generic prompt → Should use context → Generate personalized
  2. Specific prompt → Should find relevant commits → Use in generation
  3. No GitHub data → Fallback to generic generation
  4. No Twitter style → Use default style guidelines

#### Example Flow:
**Complete RAG Flow:**

1. **User request:** "Generate tweet about my latest work"
2. **Retrieval:**
   - Semantic search: "latest work" → Finds recent commits
   - Gets: "Added ML endpoint" (yesterday), "Improved API" (3 days ago)
3. **Augmentation:**
   - Combines: Commits + Twitter style + User context
   - Formats: Context string
4. **Generation:**
   - Prompt: "User's latest work: Added ML endpoint. Their style: casual, ~125 chars, emojis. Generate tweet..."
   - Gemini generates: "Just shipped a ML prediction endpoint! FastAPI + Python working like magic 🚀"
5. **Result:**
   - Personalized (mentions actual work)
   - Matches style (casual, emojis, right length)
   - Ready to post

---

## Phase 4: Agent Architecture Enhancement (Week 4)

### Day 1: Multi-Source Data Agent

#### Tool: LangGraph - New Nodes
- **File to update:** `backend/agent/nodes.py`
- **New node to create:**

  `data_collection_node(state)`
  - **What:** Collects data from all sources
  - **Process:**
    1. Check if GitHub data is fresh (< 24 hours old)
       - If stale: Trigger refresh (async or suggest to user)
    2. Check if Twitter style is fresh
       - If stale: Fetch latest tweets and update style
    3. Get user context from database
    4. Update agent state with collected data
  - **Returns:** Updated state with data

#### Tool: LangGraph - Graph Update
- **File to update:** `backend/agent/graph.py`
- **New workflow:**
  ```
  START
    ↓
  data_collection_node (NEW)
    ↓
  context_aggregation_node (NEW - Day 2)
    ↓
  generate_node (EXISTING - but enhanced)
    ↓
  validate_node (EXISTING)
    ↓
  finalize_node (EXISTING)
    ↓
  END
  ```

#### Tool: Error Handling
- **Scenarios:**
  1. GitHub data unavailable → Use cached data, log warning
  2. Twitter token expired → Use last known style profile
  3. Network error → Graceful fallback
  4. Missing data → Generate with available context

#### Example Flow:
1. User wants to generate post
2. Agent starts → Enters `data_collection_node`
3. Node checks:
   - GitHub: Last fetch 2 hours ago → Fresh, use cached
   - Twitter: Last fetch 1 day ago → Stale, suggest refresh (but use cached for now)
4. Node gets:
   - GitHub commits from database
   - Twitter style from database
   - User context from database
5. Updates state with all data
6. Proceeds to next node

---

### Day 2: Context Aggregation Agent

#### Tool: LangGraph - New Node
- **File to update:** `backend/agent/nodes.py`
- **New node:**

  `context_aggregation_node(state)`
  - **What:** Combines and prioritizes context from all sources
  - **Process:**
    1. Get GitHub commits from state (from data collection node)
    2. Get Twitter style from state
    3. Get user context (current projects, tech stack)
    4. Use semantic search: Find commits relevant to user's prompt
    5. Build unified context:
       - Recent work (from GitHub commits)
       - Writing style (from Twitter)
       - Current focus (from user context)
    6. Prioritize:
       - Most recent commits
       - Most relevant to prompt
       - Major commits (not bug fixes)
   - **Returns:** State with aggregated context

#### Tool: Context Structure
- **State structure:**
  ```python
  {
    "retrieved_commits": [...],  # From semantic search
    "writing_style": {...},      # From Twitter
    "current_projects": [...],   # From GitHub analysis
    "tech_stack": [...],         # From GitHub
    "context_summary": "...",    # Formatted for prompt
  }
  ```

#### Example Flow:
1. State comes from `data_collection_node`
2. `context_aggregation_node` receives:
   - All GitHub commits
   - Twitter style profile
   - User prompt: "Post about my work"
3. Node:
   - Runs semantic search: "my work" → Finds 3 relevant commits
   - Gets writing style: casual, 125 chars, uses emojis
   - Gets current projects: ["ai-project"]
   - Combines into context summary
4. Updates state with aggregated context
5. Passes to generation node

---

### Day 3: Enhanced Generation Agent

#### Tool: LangGraph - Update Node
- **File to update:** `backend/agent/nodes.py`
- **Node to update:** `generate_node(state)`

**Current logic (generic):**
- Takes user prompt
- Generates content with Gemini

**New logic (context-aware):**
1. Get aggregated context from state
2. Build augmented prompt:
   ```
   Base prompt: [user's original prompt]
   
   Context:
   - Recent work: [retrieved commits]
   - Writing style: [style profile]
   - Current focus: [user context]
   
   Instructions:
   - Reference actual work from context
   - Match user's writing style
   - Keep length around [average_length] characters
   ```
3. Generate with Gemini API (with augmented prompt)
4. Result: Personalized, style-matched content

#### Tool: Prompt Template
- **File to create:** `backend/prompts/rag_template.py`
- **Template structure:**
  ```
  You are generating a {platform} post for a developer.
  
  Context about the developer:
  - Current Work: {recent_commits}
  - Active Projects: {current_projects}
  - Tech Stack: {tech_stack}
  
  Their Writing Style:
  - Tone: {tone}
  - Average Length: {average_length} characters
  - Uses Emojis: {uses_emojis}
  - Common Topics: {topics}
  
  Instructions:
  1. Generate content about: {user_prompt}
  2. Reference their actual work from context
  3. Match their writing style exactly
  4. Keep length around {average_length} characters
  5. Use emojis if they typically do
  
  Generate the post:
  ```

#### Example Flow:
1. State arrives at `generate_node` with aggregated context
2. Node extracts:
   - User prompt: "Post about my work"
   - Commits: "Added ML endpoint", "Improved API"
   - Style: casual, 125 chars, emojis
3. Builds prompt using template
4. Calls Gemini with augmented prompt
5. Gemini generates: "Just shipped a ML prediction endpoint! FastAPI + Python working like magic 🚀"
6. Content is personalized, matches style, references actual work
7. Passes to validation node

---

### Day 4: Agent Learning Loop

#### Tool: Database - New Table
- **Table to create:** `post_performance`
- **Purpose:** Track how generated posts perform
- **Fields:**
  - id: UUID
  - user_id: UUID (foreign key)
  - post_id: UUID (links to posts table)
  - generated_content: TEXT
  - context_used: JSONB (what commits/style were used)
  - posted_at: TIMESTAMP
  - engagement_metrics: JSONB (likes, retweets, etc.)
  - collected_at: TIMESTAMP

#### Tool: Backend - Performance Tracking
- **File to create:** `backend/services/performance_tracker.py`
- **Methods to create:**
  1. `track_post(post_id, context_used)` - Record what context was used
  2. `update_engagement(post_id, metrics)` - Update with Twitter engagement
  3. `analyze_successful_patterns(user_id)` - Find what works best
  4. `get_best_context_types(user_id)` - Return context that led to best posts

#### Tool: LangGraph - Learning Node
- **File to update:** `backend/agent/nodes.py`
- **New node (optional, for future):**
  `learning_node(state)`
  - **What:** Analyzes what context types work best
  - **Process:**
    1. Check recent post performance
    2. Identify patterns:
       - Which commits led to best engagement?
       - Which style elements work best?
       - Which topics resonate?
    3. Update user preferences
    4. Store insights for future use
  - **Returns:** State with learned preferences

#### Tool: Backend - Context Optimization
- **File to update:** `backend/services/context_optimizer.py`
- **Methods to create:**
  1. `get_optimal_context(user_id, prompt)` - Returns best context based on past success
  2. `prioritize_commits(commits, user_id)` - Orders commits by historical success
  3. `adjust_style_recommendations(user_id)` - Updates style suggestions based on performance

#### Example Flow:
1. User generates and posts content
2. System tracks:
   - What commits were used
   - What style was applied
   - Post engagement (from Twitter API)
3. After 10-20 posts, patterns emerge:
   - "Commits about new features get 2x engagement"
   - "Technical style performs better than casual"
   - "Morning posts get more engagement"
4. Agent uses insights for future generations

---

### Day 5: Polish and Integration Testing

#### Tool: Testing - End-to-End Flow
- **Test scenario 1: New user journey**
  1. User signs up
  2. Connects GitHub account
  3. System fetches commits (first time)
  4. Generates embeddings
  5. User connects Twitter (already done)
  6. System analyzes Twitter style
  7. User generates post: "Post about my work"
  8. System:
     - Retrieves relevant commits (semantic search)
     - Gets writing style
     - Generates personalized content
  9. User posts to Twitter
  10. System tracks performance

- **Test scenario 2: Existing user**
  1. User already has data
  2. User generates post
  3. System uses cached context
  4. Fast generation (no API calls)

- **Test scenario 3: Data refresh**
  1. User hasn't refreshed in 25 hours
  2. System suggests refresh
  3. User clicks refresh
  4. System fetches only new commits
  5. Generates embeddings for new commits
  6. Updates context

#### Tool: Error Handling Review
- **Checkpoints:**
  1. GitHub API fails → Use cached data
  2. Twitter API fails → Use cached style
  3. Embedding generation fails → Fall back to text search
  4. Vector database full → Archive old embeddings
  5. No context available → Generate generic content with warning

#### Tool: Performance Optimization
- **Optimizations:**
  1. Batch embedding generation (50 at a time)
  2. Cache embeddings (never regenerate)
  3. Use database indexes for fast queries
  4. Limit semantic search results (top 5)
  5. Cache user context (refresh every 24 hours)

---

## Phase 5: Advanced Features & Optimization (Week 5 - Optional)

### Day 1: Advanced Semantic Search

#### Tool: Multiple Query Strategies
- **File to update:** `backend/services/semantic_search.py`
- **Advanced methods:**
  1. `multi_query_search(user_prompt)` - Generate multiple query variations
     - Example: "my work" → ["API development", "recent commits", "current projects"]
     - Search with all variations
     - Combine results
  2. `hybrid_search(user_prompt)` - Combine semantic + keyword search
     - Semantic: Find similar meaning
     - Keyword: Find exact matches
     - Merge and rank results

#### Tool: Query Expansion
- **Method:** `expand_query(user_prompt)`
- **What:** Expand user's prompt to find more relevant commits
  - Example:
    - User: "API"
    - Expanded: ["API endpoint", "REST API", "API service", "API development"]
  - Search with all variations

---

### Day 2: Context Compression

#### Tool: Context Summarization
- **File to create:** `backend/services/context_compressor.py`
- **Method:** `compress_context(context)`
- **What:** Summarize large context to fit in AI prompt
- **Process:**
  1. Too many commits? → Summarize to 3 most important
  2. Long commit messages? → Extract key points
  3. Redundant info? → Remove duplicates
- **Result:** Smaller, focused context for better generation

#### Tool: Smart Context Selection
- **Method:** `select_best_context(commits, user_prompt, limit=5)`
- **What:** Choose most relevant commits intelligently
- **Criteria:**
  1. Relevance score (from semantic search)
  2. Recency (more recent = more relevant)
  3. Importance (major commits > bug fixes)
  4. Diversity (avoid similar commits)

---

### Day 3: Real-time Context Updates

#### Tool: GitHub Webhook Integration (Optional)
- **What:** Get notified when new commits are pushed
- **Setup:**
  1. Create GitHub webhook
  2. Point to backend endpoint: `/api/webhooks/github`
  3. When commit pushed → Webhook fires
  4. Backend receives notification
  5. Fetch new commit immediately
  6. Generate embedding
  7. Update context
- **Result:** Always up-to-date without manual refresh

---

### Day 4: Analytics Dashboard

#### Tool: Frontend - Analytics Component
- **File to create:** `frontend/components/analytics/ContentAnalytics.tsx`
- **Features:**
  1. Show post performance over time
  2. Graph engagement metrics
  3. Show which context types work best
  4. Display writing style insights

#### Tool: Backend - Analytics Endpoint
- **Endpoint:** `GET /api/analytics/content-performance`
- **Returns:**
  - Engagement trends
  - Best performing posts
  - Context effectiveness
  - Style recommendations

---

## Complete Workflow Summary

### Full End-to-End Flow:

```
1. USER CONNECTS ACCOUNTS:
   - GitHub OAuth → Token stored
   - Twitter OAuth → Already done ✅

2. DATA COLLECTION (First Time):
   - Fetch GitHub commits (last 30 days)
   - Store in `github_activity` table
   - Fetch Twitter posts (last 100)
   - Store in `twitter_activity` table

3. PROCESSING:
   - Generate embeddings for commits
   - Store in vector column
   - Analyze Twitter style
   - Store in `twitter_style_profile`
   - Extract insights → `user_context`

4. USER GENERATES POST:
   - User prompt: "Post about my work"
   - ↓
   AGENT WORKFLOW:
   
   a. DATA COLLECTION NODE:
      - Check if GitHub data fresh (< 24 hours)
      - If stale, refresh (fetch new commits only)
      - Get Twitter style (from cache)
      
   b. SEMANTIC SEARCH NODE:
      - Convert prompt to embedding
      - Search vector database
      - Find top 5 relevant commits
      
   c. CONTEXT AGGREGATION NODE:
      - Combine: Retrieved commits + Twitter style
      - Build unified context summary
      
   d. GENERATION NODE:
      - Augment prompt with context
      - Generate with Gemini
      - Personalized, style-matched content
      
   e. VALIDATION NODE:
      - Check content quality
      - Verify style match
      
   f. FINALIZE NODE:
      - Format for Twitter
      - Return to user

5. USER POSTS:
   - Review generated content
   - Post to Twitter
   - Track performance

6. LEARNING (Background):
   - Monitor post engagement
   - Identify successful patterns
   - Update preferences
   - Improve future generations
```

---

## Database Schema Summary

### Tables Overview:

1. **connected_accounts** (existing)
   - GitHub OAuth tokens
   - Twitter OAuth tokens

2. **github_activity** (new)
   - Commit data
   - Embeddings (vector column)
   - Raw API responses

3. **github_data_fetch_log** (new)
   - Track fetch history
   - Last commit date
   - Refresh timing

4. **twitter_activity** (new)
   - Past tweets
   - Engagement metrics

5. **twitter_style_profile** (new)
   - Writing style analysis
   - Preferences
   - Patterns

6. **user_context** (new)
   - Aggregated insights
   - Current projects
   - Tech stack
   - Preferences

7. **posts** (existing)
   - Generated posts
   - Post history

8. **post_performance** (new, optional)
   - Engagement tracking
   - Success patterns

---

## Tools & Libraries Reference

### Python Packages:
```
fastapi              # Already have
langgraph            # Already have
google-genai         # Already have
supabase             # Already have
httpx                # Already have
sentence-transformers # NEW - For embeddings
psycopg2             # Already have (for Supabase)
python-dotenv        # Already have
```

### Frontend Packages:
```
next                 # Already have
react                # Already have
@tanstack/react-query # Already have
@supabase/supabase-js # Already have
```

### External Services (All Free):
- **Render:** Backend hosting
- **Vercel:** Frontend hosting
- **Supabase:** Database + Auth (500MB free)
- **HuggingFace:** Embedding models (free)
- **GitHub:** OAuth + API (free)
- **Twitter:** OAuth + API (already have)
- **Gemini:** AI generation (free tier)

---

## Daily Development Checklist

### Phase 1 Checklist (Week 1 - GitHub):
- [ ] Day 1: GitHub OAuth working
- [ ] Day 2: Can fetch and store commits
- [ ] Day 3: Smart refresh logic implemented
- [ ] Day 4: Data analysis working
- [ ] Day 5: Tested end-to-end

### Phase 2 Checklist (Week 2 - Twitter Reading):
- [ ] Day 1: Can read past tweets
- [ ] Day 2: Style analysis working
- [ ] Day 3: Best content identification working

### Phase 3 Checklist (Week 3 - RAG with Embeddings):
- [ ] Day 1: Embeddings generating
- [ ] Day 2: Vector database set up
- [ ] Day 3: Embeddings stored for all commits
- [ ] Day 4: Semantic search working
- [ ] Day 5: RAG integrated in generation

### Phase 4 Checklist (Week 4 - Agent Enhancement):
- [ ] Day 1: Multi-source data agent working
- [ ] Day 2: Context aggregation working
- [ ] Day 3: Enhanced generation using context
- [ ] Day 4: Learning loop implemented
- [ ] Day 5: Full integration tested

---

## Success Criteria

### Must Have:
✅ Users can connect GitHub and Twitter
✅ System collects and stores their data
✅ System generates embeddings
✅ Semantic search finds relevant commits
✅ Generated content is personalized
✅ Content matches user's writing style
✅ Everything works on free tier

### Nice to Have:
- Automatic data refresh
- Performance analytics
- Learning from engagement
- Real-time webhooks

---

## Learning Outcomes

### By End of Project, You'll Understand:
1. **OAuth Flows:** GitHub OAuth implementation
2. **API Integration:** REST APIs, data fetching, pagination
3. **Embeddings:** Converting text to vectors, semantic meaning
4. **Vector Databases:** pgvector, similarity search, indexing
5. **RAG:** Retrieval, augmentation, generation patterns
6. **Agent Architecture:** Multi-node workflows, state management
7. **Context Building:** Multi-source data aggregation
8. **Personalization:** Using real data for AI generation
9. **Caching Strategies:** Efficient data refresh
10. **Performance Optimization:** Batch processing, indexing

---

## Next Steps After Completion

### Future Enhancements (Optional):
1. **LinkedIn Integration** (Phase 2 from original plan)
2. **Reddit Integration** (Phase 3 from original plan)
3. **Scheduled Posts** (Queue system)
4. **Multi-Account Support** (Team features)
5. **Advanced Analytics** (Engagement predictions)
6. **Content Calendar** (Visual planning)
7. **Fine-tuning** (Train model on user's style)

---

## Troubleshooting Guide

### Common Issues:

**Issue:** GitHub API rate limit
- **Solution:** Use tokens efficiently, implement caching

**Issue:** Embedding generation slow
- **Solution:** Batch process, cache results

**Issue:** Vector database full
- **Solution:** Archive old data, keep last 90 days

**Issue:** Semantic search not finding relevant commits
- **Solution:** Check embedding quality, adjust similarity threshold

**Issue:** Generated content not matching style
- **Solution:** Review style analysis, improve prompt template

---

**Plan Complete! Ready for step-by-step development. 🚀**