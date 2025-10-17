# AI Agents Tweet - Project Plan

## Project Overview
Build an agentic AI application that generates tweet content from user prompts using Google Gemini and posts to Twitter with user confirmation.

**Tech Stack:**
- **Backend:** Python 3.9+ with FastAPI + LangGraph (Agentic AI)
- **Frontend:** Next.js 14 with Tailwind CSS + shadcn/ui
- **AI:** Google Gemini Pro
- **Social:** Twitter API (Free Tier)
- **Storage:** JSON file for tweet history
- **Deployment:** Render (backend) + Vercel (frontend)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                         │
│                    (Next.js Frontend)                        │
│                                                              │
│  [Text Input] → [Generate Button] → [Preview Card]          │
│                                      ↓                       │
│                                [Confirm Post Button]         │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP Request
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API SERVER                        │
│                    (FastAPI + Python)                        │
│                                                              │
│  POST /api/generate  →  Returns generated tweet              │
│  POST /api/post      →  Posts to Twitter                    │
│  GET  /api/history   →  Returns tweet history               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC AI LAYER                          │
│                      (LangGraph)                             │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │  [Start] → [Plan] → [Generate] → [Validate]     │      │
│  │              ↓         ↓            ↓            │      │
│  │         [Gemini]  [Hashtags]  [Check Length]    │      │
│  │                                  ↓               │      │
│  │                              [Return]            │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│                                                              │
│  • Google Gemini API (Content Generation)                   │
│  • Twitter API v2 (Posting Tweets)                          │
│  • tweets_history.json (Local Storage)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
ai-agents-tweet/
│
├── backend/                              # Python Backend
│   ├── main.py                          # FastAPI app entry point
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                             # Environment variables (gitignored)
│   ├── .env.example                     # Environment template
│   │
│   ├── agent/                           # LangGraph Agent
│   │   ├── __init__.py
│   │   ├── graph.py                    # Agent state graph definition
│   │   ├── nodes.py                    # Agent node functions
│   │   ├── state.py                    # Agent state schema
│   │   └── tools.py                    # Agent tools (functions)
│   │
│   ├── services/                        # External service integrations
│   │   ├── __init__.py
│   │   ├── gemini_service.py           # Gemini API wrapper
│   │   └── twitter_service.py          # Twitter API wrapper
│   │
│   ├── prompts/                         # Prompt engineering
│   │   ├── __init__.py
│   │   └── templates.py                # Prompt templates
│   │
│   ├── storage/                         # Data storage
│   │   ├── __init__.py
│   │   └── tweet_storage.py            # JSON file operations
│   │
│   ├── models/                          # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py                  # Request/Response models
│   │
│   └── data/                            # Data files
│       └── tweets_history.json         # Tweet storage (gitignored)
│
├── frontend/                             # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx                  # Root layout
│   │   ├── page.tsx                    # Home page
│   │   ├── globals.css                 # Global styles
│   │   └── api/                        # API routes (proxy to backend)
│   │       └── proxy/
│   │           └── [...path]/
│   │               └── route.ts
│   │
│   ├── components/                      # React components
│   │   ├── ui/                         # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── textarea.tsx
│   │   │   └── ...
│   │   ├── TweetGenerator.tsx          # Main form component
│   │   ├── TweetPreview.tsx            # Preview card
│   │   └── TweetHistory.tsx            # History list
│   │
│   ├── lib/
│   │   ├── utils.ts                    # Utility functions
│   │   └── api.ts                      # API client
│   │
│   ├── .env.local                       # Frontend env vars
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── components.json                  # shadcn/ui config
│
├── .gitignore                            # Git ignore rules
├── README.md                             # Project documentation
└── PLAN.md                               # This file

```

---

## Backend Implementation Details

### 1. Agent Flow (LangGraph)

```python
# agent/graph.py - State Graph Definition

State Flow:
┌─────────┐
│  START  │
└────┬────┘
     ↓
┌────────────────┐
│  PLAN_NODE     │  # Agent analyzes the prompt
│                │  # Decides on tweet strategy
└────┬───────────┘
     ↓
┌────────────────┐
│ GENERATE_NODE  │  # Calls Gemini to generate content
│                │  # Uses prompt template
└────┬───────────┘
     ↓
┌────────────────┐
│ VALIDATE_NODE  │  # Check character limit (280)
│                │  # Basic quality check
└────┬───────────┘
     ↓
┌────────────────┐
│ HASHTAG_NODE   │  # Suggest relevant hashtags
│                │  # Add if under char limit
└────┬───────────┘
     ↓
┌────────────────┐
│  FINALIZE_NODE │  # Prepare final tweet
│                │  # Return to user
└────┬───────────┘
     ↓
┌─────────┐
│   END   │
└─────────┘
```

**Agent State Schema:**
```python
class AgentState(TypedDict):
    user_prompt: str          # Original user input
    tweet_content: str        # Generated tweet
    hashtags: List[str]       # Suggested hashtags
    char_count: int           # Character count
    is_valid: bool            # Validation status
    error: Optional[str]      # Error message if any
    step: str                 # Current step name
```

**Agent Tools:**
- `generate_tweet_content(prompt: str) -> str` - Calls Gemini
- `validate_tweet(content: str) -> bool` - Checks length/quality
- `suggest_hashtags(content: str) -> List[str]` - Generates hashtags
- `combine_content_and_hashtags(content: str, hashtags: List[str]) -> str` - Merges

### 2. API Endpoints

**POST /api/generate**
```python
Request:
{
  "prompt": "Write about AI and creativity"
}

Response:
{
  "success": true,
  "data": {
    "content": "AI is transforming creativity...",
    "hashtags": ["#AI", "#Creativity"],
    "char_count": 145,
    "steps": [
      {"step": "planning", "message": "Analyzing prompt..."},
      {"step": "generating", "message": "Creating content..."},
      {"step": "validating", "message": "Checking quality..."},
      {"step": "finalizing", "message": "Adding hashtags..."}
    ]
  }
}
```

**POST /api/post**
```python
Request:
{
  "content": "AI is transforming creativity... #AI #Creativity",
  "user_prompt": "Write about AI and creativity"
}

Response:
{
  "success": true,
  "tweet_id": "1234567890",
  "url": "https://twitter.com/user/status/1234567890"
}
```

**GET /api/history**
```python
Response:
{
  "success": true,
  "tweets": [
    {
      "id": "uuid-1",
      "prompt": "Write about AI",
      "content": "AI is...",
      "posted_at": "2025-10-17T10:30:00Z",
      "tweet_url": "https://twitter.com/..."
    }
  ]
}
```

### 3. Core Services

**Gemini Service (`services/gemini_service.py`)**
```python
class GeminiService:
    def __init__(self, api_key: str):
        # Initialize Gemini client
        
    async def generate_tweet(self, prompt: str) -> str:
        # Call Gemini with optimized prompt
        # Return tweet content
        
    async def generate_hashtags(self, content: str) -> List[str]:
        # Generate relevant hashtags
```

**Twitter Service (`services/twitter_service.py`)**
```python
class TwitterService:
    def __init__(self, credentials: dict):
        # Initialize Tweepy client (Free tier compatible)
        
    async def post_tweet(self, content: str) -> dict:
        # Post to Twitter
        # Return tweet ID and URL
        
    def validate_content(self, content: str) -> bool:
        # Check if content meets Twitter requirements
```

**Tweet Storage (`storage/tweet_storage.py`)**
```python
class TweetStorage:
    def __init__(self, file_path: str = "data/tweets_history.json"):
        # Initialize JSON file storage
        
    def save_tweet(self, tweet_data: dict) -> None:
        # Append to JSON file
        
    def get_history(self, limit: int = 50) -> List[dict]:
        # Read from JSON file
```

### 4. Prompt Engineering

**System Prompt Template (`prompts/templates.py`)**
```python
TWEET_GENERATION_PROMPT = """
You are an expert social media content creator specializing in Twitter/X.

Task: Create an engaging tweet based on the user's prompt.

Requirements:
- Maximum 250 characters (to leave room for hashtags)
- Engaging and conversational tone
- Clear and concise
- Include relevant emojis if appropriate
- Do not include hashtags (will be added separately)

User Prompt: {user_prompt}

Generate only the tweet content, nothing else.
"""

HASHTAG_GENERATION_PROMPT = """
Based on this tweet content, suggest 2-3 relevant hashtags.

Tweet: {tweet_content}

Return only hashtags separated by spaces, like: #AI #Tech #Innovation
"""
```

---

## Frontend Implementation Details

### 1. Main Component Structure

**TweetGenerator Component (`components/TweetGenerator.tsx`)**
```typescript
Features:
- Textarea for user prompt
- "Generate Tweet" button
- Loading state with skeleton
- Shows agent steps in real-time (optional)
- Displays generated preview

States:
- prompt: string
- loading: boolean
- generatedTweet: TweetData | null
- error: string | null
```

**TweetPreview Component (`components/TweetPreview.tsx`)**
```typescript
Features:
- Card showing generated content
- Character count display
- Hashtags shown separately
- "Post to Twitter" button
- "Regenerate" button
- Success/error feedback

Props:
- content: string
- hashtags: string[]
- charCount: number
- onPost: () => Promise<void>
- onRegenerate: () => void
```

**TweetHistory Component (`components/TweetHistory.tsx`)**
```typescript
Features:
- List of previously posted tweets
- Shows prompt + generated content
- Links to Twitter posts
- Timestamp display
- Pagination (if needed)
```

### 2. UI Design (Tailwind + shadcn/ui)

**Layout:**
```
┌────────────────────────────────────────────────────────┐
│  AI Tweet Generator                         [Dark Mode]│
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  What would you like to tweet about?             │ │
│  │                                                  │ │
│  │  [Large Textarea - User Prompt Input]           │ │
│  │                                                  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  [Generate Tweet Button]                               │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Preview                                         │ │
│  │  ┌────────────────────────────────────────────┐ │ │
│  │  │ Generated tweet content appears here...    │ │ │
│  │  │                                            │ │ │
│  │  │ #Hashtag1 #Hashtag2                        │ │ │
│  │  └────────────────────────────────────────────┘ │ │
│  │                                                  │ │
│  │  Character count: 145/280                        │ │
│  │                                                  │ │
│  │  [Regenerate] [Post to Twitter]                  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Recent Tweets                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ • Tweet 1 - [View on Twitter]                    │ │
│  │ • Tweet 2 - [View on Twitter]                    │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### 3. API Client (`lib/api.ts`)

```typescript
export const api = {
  async generateTweet(prompt: string) {
    const response = await fetch('/api/proxy/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    return response.json();
  },
  
  async postTweet(content: string, prompt: string) {
    const response = await fetch('/api/proxy/post', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, user_prompt: prompt })
    });
    return response.json();
  },
  
  async getHistory() {
    const response = await fetch('/api/proxy/history');
    return response.json();
  }
};
```

---

## Environment Variables

### Backend (`.env`)
```bash
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Twitter API (Free Tier)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# API Configuration
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
PORT=8000
```

### Frontend (`.env.local`)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
# For production: https://your-backend.render.com
```

---

## Dependencies

### Backend (`requirements.txt`)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0

# AI & Agent
google-generativeai==0.3.1
langchain==0.1.0
langchain-google-genai==0.0.5
langgraph==0.0.20

# Twitter
tweepy==4.14.0

# Utilities
python-multipart==0.0.6
aiofiles==23.2.1
```

### Frontend (`package.json`)
```json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "tailwindcss": "3.3.0",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.294.0",
    "tailwind-merge": "^2.1.0"
  },
  "devDependencies": {
    "@types/node": "20.10.0",
    "@types/react": "18.2.42",
    "typescript": "5.3.2",
    "autoprefixer": "10.4.16",
    "postcss": "8.4.32"
  }
}
```

---

## Implementation Order

### Phase 1: Backend Foundation (Day 1)
1. ✅ Set up project structure
2. ✅ Install dependencies
3. ✅ Configure environment variables
4. ✅ Create FastAPI app skeleton
5. ✅ Test basic endpoint

### Phase 2: Services Integration (Day 1-2)
1. ✅ Implement Gemini service
2. ✅ Test Gemini API connection
3. ✅ Implement Twitter service
4. ✅ Test Twitter API (read-only first)
5. ✅ Implement JSON storage

### Phase 3: Agent Development (Day 2-3)
1. ✅ Define agent state schema
2. ✅ Create agent nodes
3. ✅ Build state graph
4. ✅ Implement tools
5. ✅ Test agent flow locally

### Phase 4: API Endpoints (Day 3)
1. ✅ Implement /generate endpoint
2. ✅ Implement /post endpoint
3. ✅ Implement /history endpoint
4. ✅ Add error handling
5. ✅ Test all endpoints

### Phase 5: Frontend Setup (Day 4)
1. ✅ Initialize Next.js project
2. ✅ Set up Tailwind CSS
3. ✅ Install shadcn/ui
4. ✅ Create component structure
5. ✅ Set up API proxy

### Phase 6: Frontend Implementation (Day 4-5)
1. ✅ Build TweetGenerator component
2. ✅ Build TweetPreview component
3. ✅ Build TweetHistory component
4. ✅ Implement API client
5. ✅ Add loading states and error handling

### Phase 7: Integration & Testing (Day 5-6)
1. ✅ Connect frontend to backend
2. ✅ Test full flow end-to-end
3. ✅ Fix bugs and edge cases
4. ✅ Improve UX/UI
5. ✅ Add final touches

### Phase 8: Deployment (Day 6-7)
1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update environment variables
4. ✅ Test production deployment
5. ✅ Monitor and debug

---

## Deployment Guide

### Backend Deployment (Render)

**Steps:**
1. Push code to GitHub repository
2. Create new Web Service on Render
3. Connect GitHub repo
4. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
5. Add environment variables in Render dashboard
6. Deploy!

**Free Tier Limits:**
- Spins down after 15 minutes of inactivity
- Cold start: ~30 seconds
- 750 hours/month free

### Frontend Deployment (Vercel)

**Steps:**
1. Push code to GitHub repository
2. Import project in Vercel
3. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
4. Add environment variable: `NEXT_PUBLIC_API_URL`
5. Deploy!

**Free Tier Limits:**
- Unlimited bandwidth
- 100 GB-hours/month
- Instant deployments

---

## API Keys Setup Guide

### 1. Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to backend `.env`: `GEMINI_API_KEY=your_key`

**Free Tier:**
- 60 requests per minute
- Sufficient for this project

### 2. Twitter API Keys (Free Tier)

1. Go to: https://developer.twitter.com/
2. Sign in and create a new project
3. Create an app in the project
4. Generate keys:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
5. Set permissions to "Read and Write"
6. Add to backend `.env`

**Free Tier Limits:**
- 1,500 tweets per month
- 50 tweets per 24 hours
- Rate limited

---

## Testing Strategy

### Backend Tests
```bash
# Test Gemini connection
python -c "from services.gemini_service import GeminiService; ..."

# Test Twitter connection (read-only)
python -c "from services.twitter_service import TwitterService; ..."

# Test agent flow
python -c "from agent.graph import run_agent; ..."

# Test API endpoints
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test tweet about AI"}'
```

### Frontend Tests
```bash
# Run development server
npm run dev

# Test in browser
# 1. Enter prompt
# 2. Click generate
# 3. Verify preview
# 4. Click post (test mode)
```

---

## Learning Resources

### Python for Node.js Developers
- FastAPI docs: https://fastapi.tiangolo.com/
- Python async/await: Similar to Node.js
- Type hints: Similar to TypeScript

### LangGraph & Agentic AI
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- LangChain docs: https://python.langchain.com/
- Agent concepts: ReAct pattern, tool calling

### Twitter API
- Twitter API docs: https://developer.twitter.com/en/docs/twitter-api
- Tweepy docs: https://docs.tweepy.org/

---

## Troubleshooting

### Common Issues

**Backend:**
- Virtual environment not activated → `source venv/bin/activate`
- Module not found → `pip install -r requirements.txt`
- API key errors → Check `.env` file
- CORS errors → Update `CORS_ORIGINS` in backend

**Frontend:**
- API connection failed → Check `NEXT_PUBLIC_API_URL`
- shadcn/ui components missing → `npx shadcn-ui@latest add button`
- Build errors → Check TypeScript types

**Deployment:**
- Render: Check build logs, verify Python version
- Vercel: Check environment variables, build settings

---

## Future Enhancements (Optional)

1. **Advanced Agent Features:**
   - Multi-tweet threads
   - Image generation (DALL-E/Midjourney)
   - Sentiment analysis before posting
   - A/B testing different versions

2. **Better Storage:**
   - PostgreSQL database (Supabase free tier)
   - User authentication
   - Multiple user support

3. **Scheduling:**
   - Queue system for scheduled posts
   - Best time to post suggestions

4. **Analytics:**
   - Track engagement metrics
   - Show which prompts work best

5. **More Platforms:**
   - LinkedIn integration
   - Threads (Meta)
   - Bluesky

---

## Success Metrics

**You'll know it's working when:**
- ✅ You can enter a prompt
- ✅ Agent generates a tweet (with hashtags)
- ✅ Preview shows correctly
- ✅ Clicking "Post" successfully tweets
- ✅ Tweet appears in history
- ✅ You can see it on Twitter

**Learning Goals Achieved:**
- ✅ Understand Python async/await
- ✅ Build with FastAPI
- ✅ Implement agentic AI with LangGraph
- ✅ Tool calling patterns
- ✅ LLM orchestration
- ✅ API integration (Gemini + Twitter)
- ✅ Full-stack deployment

---

## Timeline Estimate

- **Backend:** 2-3 days
- **Frontend:** 2 days
- **Integration:** 1 day
- **Deployment:** 1 day
- **Total:** ~6-7 days (at learning pace)

If you focus and work efficiently: **3-4 days possible**

---

## Next Steps

1. ✅ Review this plan
2. ✅ Ask any questions
3. ✅ Get API keys ready (Gemini + Twitter)
4. ✅ Start implementation (backend first)
5. ✅ Build, test, deploy!

---

**Ready to build? Let's start with the backend! 🚀**

---

*Last Updated: October 17, 2025*
*Version: 1.0*

