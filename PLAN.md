# Social AI Agents - Multi-Platform OAuth Project Plan

## Project Overview
Build a multi-user, multi-platform social media AI agent that generates platform-specific content and posts to Twitter, LinkedIn, and Reddit using OAuth authentication.

**Branch:** `feat/oauth`

**Tech Stack:**
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
- **Backend:** Python 3.9+ with FastAPI + LangGraph (Agentic AI)
- **Database & Auth:** Supabase (PostgreSQL + Auth)
- **AI:** Google Gemini 2.0
- **Social APIs:** Twitter OAuth 2.0, LinkedIn OAuth 2.0, Reddit OAuth 2.0

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                        │
│  • Supabase Auth (Client-side)                               │
│  • React Query State Management                              │
│  • Next.js Middleware (Route Protection)                     │
│  • Content Generation UI                                     │
│  • Platform Selection & Preview                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              NEXT.JS API ROUTES (OAuth Only)                 │
│  • OAuth callbacks (Twitter, LinkedIn, Reddit)               │
│  • Proxy to Python backend                                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                 PYTHON BACKEND (FastAPI)                     │
│  • Supabase JWT Verification                                 │
│  • OAuth Token Management                                    │
│  • Agentic AI (LangGraph)                                    │
│  • Platform-specific content generation                      │
│  • Social media posting                                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    SUPABASE                                  │
│  • PostgreSQL Database                                       │
│  • Row Level Security (RLS)                                  │
│  • Authentication Service                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              SOCIAL MEDIA PLATFORMS                          │
│  • Twitter API v2 (OAuth 2.0)                                │
│  • LinkedIn API (OAuth 2.0) - Phase 2                        │
│  • Reddit API (OAuth 2.0) - Phase 3                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Database Schema (Supabase PostgreSQL)

### Table: `users` (Managed by Supabase Auth)
```sql
-- Supabase creates this automatically
id: uuid (primary key)
email: text
encrypted_password: text
created_at: timestamp
updated_at: timestamp
```

### Table: `profiles`
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see and edit their own profile
CREATE POLICY "Users can view own profile" ON profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);
```

### Table: `connected_accounts`
```sql
CREATE TABLE connected_accounts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  platform TEXT NOT NULL, -- 'twitter', 'linkedin', 'reddit'
  platform_user_id TEXT NOT NULL, -- User ID on the platform
  platform_username TEXT, -- @username on platform
  access_token TEXT NOT NULL,
  refresh_token TEXT,
  token_expires_at TIMESTAMP WITH TIME ZONE,
  scope TEXT[], -- OAuth scopes granted
  is_active BOOLEAN DEFAULT TRUE,
  connected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  UNIQUE(user_id, platform) -- One account per platform per user
);

-- Enable RLS
ALTER TABLE connected_accounts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own connected accounts
CREATE POLICY "Users can view own accounts" ON connected_accounts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own accounts" ON connected_accounts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own accounts" ON connected_accounts
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own accounts" ON connected_accounts
  FOR DELETE USING (auth.uid() = user_id);
```

### Table: `posts`
```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  platform TEXT NOT NULL, -- 'twitter', 'linkedin', 'reddit'
  user_prompt TEXT NOT NULL, -- Original user input
  generated_content TEXT NOT NULL, -- AI-generated content
  hashtags TEXT[], -- Generated hashtags
  platform_post_id TEXT, -- ID from social platform
  platform_post_url TEXT, -- URL to the post
  status TEXT DEFAULT 'posted', -- 'posted', 'failed', 'deleted'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own posts
CREATE POLICY "Users can view own posts" ON posts
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own posts" ON posts
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Indexes for performance
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

---

## Project Structure

```
social-ai-agents/
├── frontend/                           # Next.js Frontend
│   ├── app/
│   │   ├── (auth)/                    # Auth routes group
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── signup/
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/               # Protected routes
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx           # Main dashboard
│   │   │   ├── connections/
│   │   │   │   └── page.tsx           # Manage connections
│   │   │   ├── history/
│   │   │   │   └── page.tsx           # Post history
│   │   │   └── layout.tsx             # Dashboard layout
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── twitter/
│   │   │   │   │   ├── login/
│   │   │   │   │   │   └── route.ts
│   │   │   │   │   └── callback/
│   │   │   │   │       └── route.ts
│   │   │   │   ├── linkedin/          # Phase 2
│   │   │   │   └── reddit/            # Phase 3
│   │   │   └── proxy/
│   │   │       └── [...path]/
│   │   │           └── route.ts       # Proxy to Python
│   │   ├── layout.tsx
│   │   ├── page.tsx                   # Landing page
│   │   └── globals.css
│   │
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── SignupForm.tsx
│   │   │   └── AuthProvider.tsx       # Supabase auth + React Query
│   │   ├── connections/
│   │   │   ├── ConnectTwitter.tsx
│   │   │   ├── ConnectedAccount.tsx
│   │   │   └── ConnectionsList.tsx
│   │   ├── generator/
│   │   │   ├── ContentGenerator.tsx   # Main generator
│   │   │   ├── PlatformSelector.tsx
│   │   │   ├── ContentPreview.tsx
│   │   │   └── PostButton.tsx
│   │   ├── history/
│   │   │   ├── PostHistory.tsx
│   │   │   └── PostCard.tsx
│   │   └── ui/                        # shadcn/ui components
│   │
│   ├── hooks/
│   │   ├── auth/
│   │   │   └── useAuth.ts             # React Query auth hook
│   │   ├── api/
│   │   │   ├── useConnections.ts      # OAuth connections
│   │   │   ├── useContent.ts          # Content generation
│   │   │   └── usePosts.ts            # Post history
│   │   └── useRealtime.ts             # Real-time updates
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts              # Browser client
│   │   │   ├── server.ts              # Server client
│   │   │   └── middleware.ts          # Auth middleware
│   │   ├── api.ts                     # API client
│   │   ├── queryClient.ts             # React Query setup
│   │   └── utils.ts
│   │
│   ├── middleware.ts                  # Next.js middleware for auth
│   ├── .env.local
│   └── package.json
│
├── backend/                            # Python Backend
│   ├── main.py                        # FastAPI app
│   ├── requirements.txt
│   ├── .env
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── supabase_auth.py          # Verify Supabase tokens
│   │   └── dependencies.py            # FastAPI dependencies
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py                   # Core LangGraph agent
│   │   ├── nodes.py                   # Agent nodes
│   │   ├── state.py                   # Agent state
│   │   └── tools/                     # Platform-specific tools
│   │       ├── __init__.py
│   │       ├── twitter_tool.py        # Twitter content generation
│   │       ├── linkedin_tool.py       # Phase 2
│   │       └── reddit_tool.py         # Phase 3
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py         # Gemini API
│   │   ├── supabase_service.py       # Supabase operations
│   │   └── social/
│   │       ├── __init__.py
│   │       ├── twitter_service.py    # Twitter OAuth 2.0 & posting
│   │       ├── linkedin_service.py   # Phase 2
│   │       └── reddit_service.py     # Phase 3
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                # Pydantic models
│   │
│   └── prompts/
│       ├── __init__.py
│       └── templates.py              # Platform-specific prompts
│
├── .gitignore
├── README.md
├── PLAN.md                            # This file
└── SETUP.md
```

---

## Implementation Phases

### **Phase 1: Foundation & Twitter OAuth (Days 1-3)**

#### Day 1: Supabase Setup & Client-Side Authentication
**Backend:**
- ✅ Set up Supabase project
- ✅ Create database tables (profiles, connected_accounts, posts)
- ✅ Configure RLS policies
- ✅ Add Supabase service to backend
- ✅ Create JWT verification middleware

**Frontend:**
- ✅ Install Supabase client + React Query
- ✅ Create useAuth hook with React Query
- ✅ Build login/signup pages (client-side auth)
- ✅ Implement protected routes with middleware
- ✅ Add Next.js middleware for route protection

**Files to Create:**
```
backend/auth/supabase_auth.py
backend/services/supabase_service.py
frontend/lib/supabase/client.ts
frontend/lib/supabase/server.ts
frontend/lib/queryClient.ts
frontend/hooks/auth/useAuth.ts
frontend/app/(auth)/login/page.tsx
frontend/app/(auth)/signup/page.tsx
frontend/components/auth/AuthProvider.tsx
frontend/middleware.ts
```

#### Day 2: Twitter OAuth 2.0 + React Query
**Backend:**
- ✅ Update Twitter service to OAuth 2.0
- ✅ Create OAuth flow endpoints
- ✅ Token storage in Supabase
- ✅ Token refresh logic

**Frontend:**
- ✅ Create useConnections hook with React Query
- ✅ "Connect Twitter" button with React Query mutations
- ✅ OAuth callback handling
- ✅ Display connected accounts with caching
- ✅ Disconnect functionality with optimistic updates

**Files to Create/Update:**
```
backend/services/social/twitter_service.py (OAuth 2.0)
frontend/app/api/auth/twitter/login/route.ts
frontend/app/api/auth/twitter/callback/route.ts
frontend/hooks/api/useConnections.ts
frontend/components/connections/ConnectTwitter.tsx
frontend/components/connections/ConnectedAccount.tsx
```

#### Day 3: Agent Refactoring & React Query Integration
**Backend:**
- ✅ Refactor agent to accept platform parameter
- ✅ Create Twitter-specific tool
- ✅ Update content generation for Twitter
- ✅ Multi-user post endpoint (uses user's tokens)
- ✅ Save posts to Supabase

**Frontend:**
- ✅ Create useContent and usePosts hooks with React Query
- ✅ Update dashboard with auth + React Query
- ✅ Platform selector component with caching
- ✅ Content generator with React Query mutations
- ✅ Post history with React Query + real-time updates

**Files to Update:**
```
backend/agent/graph.py
backend/agent/tools/twitter_tool.py
backend/main.py (multi-user endpoints)
frontend/hooks/api/useContent.ts
frontend/hooks/api/usePosts.ts
frontend/components/generator/ContentGenerator.tsx
frontend/components/generator/PlatformSelector.tsx
frontend/components/history/PostHistory.tsx
```

---

### **Phase 2: LinkedIn Integration (Days 4-5)**

#### Day 4: LinkedIn OAuth
- ✅ Create LinkedIn OAuth service
- ✅ Add LinkedIn connection flow
- ✅ Store LinkedIn tokens

#### Day 5: LinkedIn Content Generation
- ✅ Create LinkedIn tool (longer content, professional tone)
- ✅ Platform-specific prompts for LinkedIn
- ✅ LinkedIn posting API integration

**Files to Create:**
```
backend/services/social/linkedin_service.py
backend/agent/tools/linkedin_tool.py
frontend/app/api/auth/linkedin/login/route.ts
frontend/app/api/auth/linkedin/callback/route.ts
frontend/components/connections/ConnectLinkedIn.tsx
```

---

### **Phase 3: Reddit Integration (Days 6-7)**

#### Day 6: Reddit OAuth
- ✅ Create Reddit OAuth service
- ✅ Add Reddit connection flow
- ✅ Store Reddit tokens

#### Day 7: Reddit Content Generation
- ✅ Create Reddit tool (title + body format)
- ✅ Subreddit selection
- ✅ Reddit posting API integration

**Files to Create:**
```
backend/services/social/reddit_service.py
backend/agent/tools/reddit_tool.py
frontend/app/api/auth/reddit/login/route.ts
frontend/app/api/auth/reddit/callback/route.ts
frontend/components/connections/ConnectReddit.tsx
frontend/components/generator/SubredditSelector.tsx
```

---

## Core Agent Architecture

### LangGraph Agent Flow

```python
# agent/graph.py

State Flow:
┌─────────────┐
│   START     │
└──────┬──────┘
       ↓
┌─────────────────┐
│  ROUTE_NODE     │  # Determines which platform tool to use
│  (platform?)    │
└──────┬──────────┘
       ↓
    ┌──┴──────────────────────────┐
    │                             │
    ↓                             ↓
┌───────────────┐          ┌──────────────┐
│ TWITTER_TOOL  │          │ LINKEDIN_TOOL│ (Phase 2)
│               │          │              │
│ • Max 280ch   │          │ • Max 3000ch │
│ • Hashtags    │          │ • Professional│
│ • Casual tone │          │ • No hashtags │
└───────┬───────┘          └──────┬───────┘
        ↓                         ↓
┌────────────────────────────────────┐
│        VALIDATE_NODE               │
│        (check content)             │
└────────────┬───────────────────────┘
             ↓
┌────────────────────────────────────┐
│        FINALIZE_NODE               │
│        (prepare for posting)       │
└────────────┬───────────────────────┘
             ↓
        ┌────────┐
        │  END   │
        └────────┘
```

### Agent State Schema

```python
# agent/state.py

class AgentState(TypedDict):
    user_id: str                    # Supabase user ID
    user_prompt: str                # Original user input
    platform: str                   # 'twitter', 'linkedin', 'reddit'
    generated_content: str          # Platform-specific content
    hashtags: Optional[List[str]]   # For Twitter
    title: Optional[str]            # For Reddit
    char_count: int                 # Character count
    is_valid: bool                  # Validation status
    error: Optional[str]            # Error message
    metadata: dict                  # Platform-specific metadata
```

### Platform Tools

```python
# agent/tools/twitter_tool.py

async def generate_twitter_content(state: AgentState) -> AgentState:
    """
    Generate Twitter-optimized content:
    - Max 280 characters (250 + hashtags)
    - Casual, engaging tone
    - Include emojis
    - Generate 2-3 hashtags
    """
    prompt = TWITTER_PROMPT_TEMPLATE.format(
        user_prompt=state["user_prompt"]
    )
    
    content = await gemini_service.generate(prompt)
    hashtags = await gemini_service.generate_hashtags(content)
    
    state["generated_content"] = content
    state["hashtags"] = hashtags
    state["char_count"] = len(content + " ".join(hashtags))
    
    return state
```

---

## API Endpoints

### Authentication (Client-Side with Supabase)

**Authentication is handled entirely on the frontend using Supabase Auth:**

```typescript
// hooks/auth/useAuth.ts
export function useAuth() {
  const queryClient = useQueryClient()
  const router = useRouter()

  // Get auth data with React Query caching
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['auth'],
    queryFn: getAuthData,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
    refetchOnWindowFocus: false,
  })

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) => 
      loginUser(email, password),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] })
    }
  })

  // Signup mutation
  const signupMutation = useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) => 
      signupUser(email, password),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] })
    }
  })

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: logoutUser,
    onSuccess: () => {
      queryClient.clear() // Clear all cached data
      router.push('/login')
    }
  })

  return {
    user: data?.user || null,
    profile: data?.profile || null,
    isAuthenticated: !!data?.user,
    isLoading,
    isLoggingIn: loginMutation.isPending,
    isSigningUp: signupMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    login: loginMutation.mutate,
    signup: signupMutation.mutate,
    logout: logoutMutation.mutate,
    refetch,
    error,
    loginError: loginMutation.error,
    signupError: signupMutation.error,
    logoutError: logoutMutation.error,
  }
}
```

---

### Social OAuth Endpoints (Next.js API Routes)

**GET /api/auth/twitter/login**
```typescript
Response: Redirect to Twitter OAuth
```

**GET /api/auth/twitter/callback**
```typescript
Query Params: code, state

Response: Redirect to dashboard with success message
```

---

### Content Generation Endpoints (Python Backend)

**POST /api/generate**
```python
Headers:
{
  "Authorization": "Bearer {supabase_access_token}"
}

Request:
{
  "prompt": "Write about AI in healthcare",
  "platform": "twitter"  # or "linkedin", "reddit"
}

Response:
{
  "success": true,
  "data": {
    "content": "AI is revolutionizing healthcare...",
    "hashtags": ["#AI", "#Healthcare", "#Innovation"],
    "char_count": 245,
    "platform": "twitter"
  }
}
```

**POST /api/post**
```python
Headers:
{
  "Authorization": "Bearer {supabase_access_token}"
}

Request:
{
  "content": "AI is revolutionizing healthcare... #AI #Healthcare",
  "platform": "twitter",
  "user_prompt": "Write about AI in healthcare"
}

Response:
{
  "success": true,
  "post_id": "uuid",
  "platform_post_id": "1234567890",
  "platform_post_url": "https://twitter.com/user/status/1234567890"
}
```

**GET /api/history**
```python
Headers:
{
  "Authorization": "Bearer {supabase_access_token}"
}

Query Params: ?platform=twitter&limit=50

Response:
{
  "success": true,
  "posts": [
    {
      "id": "uuid",
      "platform": "twitter",
      "content": "...",
      "platform_post_url": "...",
      "created_at": "2025-10-17T..."
    }
  ]
}
```

---

### Connection Management Endpoints (Python Backend)

**GET /api/connections**
```python
Headers:
{
  "Authorization": "Bearer {supabase_access_token}"
}

Response:
{
  "success": true,
  "connections": [
    {
      "platform": "twitter",
      "platform_username": "@johndoe",
      "is_active": true,
      "connected_at": "2025-10-17T..."
    }
  ]
}
```

**DELETE /api/connections/{platform}**
```python
Headers:
{
  "Authorization": "Bearer {supabase_access_token}"
}

Response:
{
  "success": true,
  "message": "Twitter account disconnected"
}
```

---

## Environment Variables

### Backend (.env)
```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# Twitter OAuth 2.0
TWITTER_CLIENT_ID=your_twitter_client_id
TWITTER_CLIENT_SECRET=your_twitter_client_secret
TWITTER_REDIRECT_URI=http://localhost:3000/api/auth/twitter/callback

# LinkedIn OAuth 2.0 (Phase 2)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:3000/api/auth/linkedin/callback

# Reddit OAuth 2.0 (Phase 3)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_REDIRECT_URI=http://localhost:3000/api/auth/reddit/callback

# API Configuration
CORS_ORIGINS=http://localhost:3000
PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_public_key

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Dependencies Updates

### Backend (requirements.txt)
```txt
# FastAPI and Server
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0

# AI & Agent Framework
google-genai
langchain==0.1.0
langchain-google-genai==0.0.5
langgraph==0.0.20

# Social Media APIs
tweepy==4.14.0              # Twitter API
httpx==0.25.2               # For OAuth flows

# Database
supabase==2.3.0             # Supabase Python client
gotrue==1.3.0               # Supabase auth

# Utilities
python-multipart==0.0.6
aiofiles==23.2.1
python-jose[cryptography]    # JWT handling
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@supabase/supabase-js": "^2.39.0",
    "@supabase/auth-helpers-nextjs": "^0.8.7",
    "@tanstack/react-query": "^5.0.0",
    "@tanstack/react-query-devtools": "^5.0.0",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "lucide-react": "^0.294.0",
    "tailwind-merge": "^2.1.0",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "@types/react": "^18.2.42",
    "@types/react-dom": "^18.2.17",
    "typescript": "^5.3.2",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-config-next": "14.0.4",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.0"
  }
}
```

---

## Security Considerations

### 1. **Row Level Security (RLS)**
All tables have RLS enabled. Users can only:
- ✅ View their own data
- ✅ Insert their own data
- ✅ Update their own data
- ✅ Delete their own data

### 2. **Token Storage**
- ❌ Never store tokens in frontend/localStorage
- ✅ Store encrypted in Supabase (server-side)
- ✅ Refresh tokens automatically
- ✅ Implement token expiry checks

### 3. **API Authentication**
```python
# backend/auth/dependencies.py

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verify Supabase JWT token from frontend"""
    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
        return user_id
    except:
        raise HTTPException(401, "Invalid token")

# Usage in endpoints
@app.post("/api/post")
async def post_content(
    request: PostRequest,
    user_id: str = Depends(get_current_user)
):
    # user_id is verified from Supabase JWT
    pass
```

### 4. **OAuth State Parameter**
- ✅ Generate random state for each OAuth flow
- ✅ Store in session/cookie
- ✅ Verify on callback

### 5. **CORS Configuration**
```python
# Only allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Strategy

### Phase 1 Testing
1. ✅ Test Supabase auth (client-side signup, login, logout)
2. ✅ Test React Query state management
3. ✅ Test Twitter OAuth flow
4. ✅ Test content generation for Twitter
5. ✅ Test posting to Twitter (with user's token)
6. ✅ Test post history retrieval with caching
7. ✅ Test RLS policies (try accessing other user's data)

### Test User Flow
```
1. Sign up → Create account (client-side)
2. Login → Get session (React Query)
3. Connect Twitter → OAuth flow
4. Generate content → AI creates tweet (React Query mutation)
5. Preview → See content (cached)
6. Post → Publish to Twitter (optimistic updates)
7. View history → See past posts (React Query + real-time)
8. Disconnect → Remove Twitter connection (optimistic updates)
9. Logout → End session (clear all cache)
```

---

## Deployment Guide

### Backend (Render)
```bash
# Build Command
pip install -r backend/requirements.txt

# Start Command
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT

# Environment Variables (add in Render dashboard)
- SUPABASE_URL
- SUPABASE_SERVICE_KEY
- SUPABASE_JWT_SECRET
- GEMINI_API_KEY
- TWITTER_CLIENT_ID
- TWITTER_CLIENT_SECRET
- TWITTER_REDIRECT_URI (update to production URL)
- FRONTEND_URL (update to Vercel URL)
```

### Frontend (Vercel)
```bash
# Framework Preset: Next.js
# Root Directory: frontend
# Build Command: npm run build

# Environment Variables (add in Vercel dashboard)
- NEXT_PUBLIC_SUPABASE_URL
- NEXT_PUBLIC_SUPABASE_ANON_KEY
- NEXT_PUBLIC_API_URL (Render backend URL)
- NEXT_PUBLIC_APP_URL (Vercel URL)
```

### Supabase
1. Create project at https://supabase.com
2. Run SQL scripts to create tables
3. Configure auth settings
4. Add production URLs to allowed domains

### Twitter Developer Portal
1. Update Callback URLs to production
2. Add Vercel URL to Website URL
3. Verify OAuth 2.0 settings

---

## Migration from Current Version

### What Changes
- ❌ Remove: `backend/.env` Twitter credentials (now per-user)
- ❌ Remove: `backend/data/tweets_history.json` (now in Supabase)
- ❌ Remove: `backend/services/twitter_service.py` (OAuth 1.0a)
- ❌ Remove: `/api/auth/login`, `/api/auth/signup` routes (client-side auth)
- ✅ Add: Supabase integration
- ✅ Add: OAuth 2.0 flows
- ✅ Add: Multi-user support
- ✅ Add: React Query state management
- ✅ Add: Client-side authentication
- ✅ Update: Agent to handle platform-specific generation

### What Stays the Same
- ✅ Core agent logic (LangGraph)
- ✅ Gemini integration
- ✅ Frontend UI components (update for auth + React Query)
- ✅ FastAPI structure

---

## Success Metrics

### Phase 1 Complete When:
- ✅ Users can sign up/login (client-side with Supabase)
- ✅ React Query manages all state (auth, connections, posts)
- ✅ Users can connect Twitter via OAuth 2.0
- ✅ Users can generate Twitter content (with React Query mutations)
- ✅ Users can post to their Twitter (with optimistic updates)
- ✅ Users can view their post history (with caching + real-time)
- ✅ Multi-user works (User A can't see User B's data)

### Phase 2 Complete When:
- ✅ All Phase 1 features
- ✅ Users can connect LinkedIn
- ✅ Platform selector shows Twitter + LinkedIn
- ✅ Content generation works for LinkedIn (longer, professional)
- ✅ Posting to LinkedIn works

### Phase 3 Complete When:
- ✅ All Phase 1 & 2 features
- ✅ Users can connect Reddit
- ✅ Platform selector shows all 3 platforms
- ✅ Content generation for Reddit (title + body)
- ✅ Posting to Reddit works

---

## Learning Objectives

By completing this project, you'll learn:

### Backend
- ✅ FastAPI with JWT verification middleware
- ✅ OAuth 2.0 flow implementation
- ✅ Supabase Python client
- ✅ JWT token verification from frontend
- ✅ LangGraph agent with conditional routing
- ✅ Platform-specific tool creation

### Frontend
- ✅ Next.js 14 App Router
- ✅ Supabase client-side authentication
- ✅ React Query state management
- ✅ Protected routes & middleware
- ✅ OAuth callback handling
- ✅ Optimistic updates & caching

### Database
- ✅ PostgreSQL schema design
- ✅ Row Level Security (RLS)
- ✅ Database relationships
- ✅ Indexes for performance

### Architecture
- ✅ Multi-user SaaS patterns
- ✅ OAuth integration patterns
- ✅ Hybrid Next.js + Python architecture
- ✅ Secure token storage

---

## Troubleshooting

### Common Issues

**Supabase Connection:**
- Check URL and keys in .env
- Verify RLS policies are correct
- Check browser network tab for errors

**OAuth Callback:**
- Ensure redirect URIs match exactly
- Check state parameter validation
- Verify OAuth app permissions

**Token Refresh:**
- Implement token refresh before expiry
- Handle refresh token rotation
- Store new tokens in database

**CORS Errors:**
- Update CORS_ORIGINS in backend
- Add Vercel URL to allowed origins
- Check credentials flag

---

## Next Steps After Phase 3

### Potential Features:
1. **Analytics Dashboard**
   - Track post performance
   - Engagement metrics
   - Best posting times

2. **Scheduled Posts**
   - Queue system
   - Cron jobs
   - Time zone handling

3. **Cross-Posting**
   - Post to multiple platforms at once
   - Platform-specific variations

4. **Team Collaboration**
   - Multiple users per account
   - Approval workflows

5. **AI Improvements**
   - Learn from past successful posts
   - A/B testing content variations
   - Sentiment analysis

---

## Timeline

**Week 1:**
- Day 1: Supabase setup + Auth ✅
- Day 2: Twitter OAuth 2.0 ✅
- Day 3: Multi-user agent ✅

**Week 2:**
- Day 4-5: LinkedIn integration ✅
- Day 6-7: Testing & bug fixes ✅

**Week 3:**
- Day 8-9: Reddit integration ✅
- Day 10: Polish & deployment ✅

---

## Resources

### Documentation
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Twitter OAuth 2.0](https://developer.twitter.com/en/docs/authentication/oauth-2-0)
- [LinkedIn OAuth](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [Reddit OAuth](https://github.com/reddit-archive/reddit/wiki/OAuth2)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Next.js App Router](https://nextjs.org/docs/app)

---

**Branch:** `feat/oauth`  
**Status:** Ready to implement  
**Last Updated:** October 17, 2025  
**Version:** 2.0 (OAuth Multi-Platform)
