# Backend Code Documentation - Complete A to Z Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Authentication Flow](#authentication-flow)
5. [Agent System (AI Content Generation)](#agent-system)
6. [API Endpoints](#api-endpoints)
7. [Database Integration](#database-integration)
8. [OAuth Integration](#oauth-integration)
9. [Code Flow Examples](#code-flow-examples)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│                  Sends JWT Token + Request                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (main.py)                  │
│  1. Verify JWT Token (Supabase)                              │
│  2. Check User Permissions                                   │
│  3. Process Request                                          │
└─────────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                    ↓
┌──────────────────┐              ┌──────────────────┐
│  Agent System    │              │  OAuth Services  │
│  (LangGraph)     │              │  (Twitter API)   │
│                  │              │                  │
│  • Plan          │              │  • Connect       │
│  • Generate      │              │  • Post          │
│  • Validate      │              │  • Revoke        │
│  • Hashtags      │              │                  │
│  • Finalize      │              └──────────────────┘
└──────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│                    Gemini AI (Google)                        │
│  • Generate platform-specific content                        │
│  • Generate hashtags                                         │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│                  Supabase Database                           │
│  • Store posts                                               │
│  • Store connected accounts                                  │
│  • User profiles                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
backend/
├── agent/                      # AI Agent System (LangGraph)
│   ├── __init__.py
│   ├── state.py               # Agent state definition
│   ├── graph.py               # Agent workflow graph
│   ├── nodes.py               # Agent processing nodes
│   └── tools/                 # Platform-specific tools
│       ├── __init__.py
│       └── twitter_tool.py    # Twitter utilities
│
├── auth/                       # Authentication
│   └── supabase_auth.py       # JWT verification
│
├── models/                     # Data models
│   ├── __init__.py
│   └── schemas.py             # Pydantic models
│
├── prompts/                    # AI prompts
│   ├── __init__.py
│   └── templates.py           # Platform-specific prompts
│
├── services/                   # External services
│   ├── __init__.py
│   ├── gemini_service.py      # Google Gemini AI
│   ├── supabase_service.py    # Database operations
│   ├── twitter_service.py     # Legacy Twitter service
│   └── social/                # OAuth services
│       ├── __init__.py
│       └── twitter_service.py # Twitter OAuth 2.0
│
├── storage/                    # Local storage (legacy)
│   ├── __init__.py
│   └── tweet_storage.py
│
├── data/                       # Data files
│   └── tweets_history.json
│
├── main.py                     # FastAPI application
└── requirements.txt            # Python dependencies
```

---

## Core Components

### 1. Main Application (`main.py`)

**Purpose**: Entry point for the FastAPI application. Defines all API endpoints.

**Key Features**:
- CORS configuration for frontend communication
- API endpoint routing
- Request/response handling
- Authentication middleware integration

**Initialization**:
```python
app = FastAPI(
    title="AI Agents Tweet API",
    description="Agentic AI for generating and posting tweets",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 2. Authentication System (`auth/supabase_auth.py`)

**Purpose**: Verify JWT tokens from Supabase and extract user information.

**How It Works**:

1. **Token Extraction**: Gets Bearer token from Authorization header
2. **JWT Verification**: Validates token signature and claims
3. **User Identification**: Extracts user ID from token

**Code Breakdown**:

```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Steps:
    1. Extract token from credentials
    2. Verify JWT signature using Supabase secret
    3. Check audience claim (must be "authenticated")
    4. Extract user ID from "sub" claim
    5. Return user ID
    """
    token = credentials.credentials
    
    # Verify token
    payload = supabase_service.verify_jwt_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(401, "Invalid token")
    
    return user_id
```

**JWT Token Structure**:
```json
{
  "sub": "user-uuid-here",           // User ID
  "aud": "authenticated",             // Audience
  "email": "user@example.com",
  "role": "authenticated",
  "iat": 1234567890,                  // Issued at
  "exp": 1234567890                   // Expires at
}
```

---

### 3. Supabase Service (`services/supabase_service.py`)

**Purpose**: Handle all database operations and JWT verification.

**Key Methods**:

#### `verify_jwt_token(token: str) -> Dict`
```python
def verify_jwt_token(self, token: str) -> Dict[str, Any]:
    """
    Verifies Supabase JWT token
    
    Process:
    1. Decode JWT using HS256 algorithm
    2. Verify signature with SUPABASE_JWT_SECRET
    3. Check audience claim = "authenticated"
    4. Extract and return payload
    
    Returns: Token payload with user data
    Raises: HTTPException if invalid
    """
```

#### `get_connected_accounts(user_id: str) -> List[Dict]`
```python
def get_connected_accounts(self, user_id: str) -> List[Dict[str, Any]]:
    """
    Get user's connected social media accounts
    
    Process:
    1. Query connected_accounts table
    2. Filter by user_id
    3. Return all connected accounts
    
    Returns: List of account objects with tokens
    """
```

#### `save_post(post_data: Dict) -> Optional[str]`
```python
def save_post(self, post_data: Dict[str, Any]) -> Optional[str]:
    """
    Save a post to database
    
    Process:
    1. Insert into posts table
    2. Return post ID
    
    Post data structure:
    {
        "user_id": "uuid",
        "platform": "twitter",
        "user_prompt": "original prompt",
        "generated_content": "AI generated text",
        "hashtags": ["#AI", "#Tech"],
        "platform_post_id": "tweet_id",
        "platform_post_url": "https://twitter.com/...",
        "status": "posted"
    }
    """
```

---

## Agent System (AI Content Generation)

### Overview

The agent system uses **LangGraph** to create a state machine that processes content generation through multiple steps.

### Agent State (`agent/state.py`)

**Purpose**: Define the data structure that flows through the agent.

```python
class AgentState(TypedDict):
    user_prompt: str          # User's input: "Write about AI"
    platform: str             # Target platform: "twitter"
    tweet_content: str        # Generated content (without hashtags)
    hashtags: List[str]       # Generated hashtags: ["#AI", "#Tech"]
    final_content: str        # Combined content + hashtags
    char_count: int           # Character count of final content
    is_valid: bool            # Whether content passes validation
    error: Optional[str]      # Error message if any
    step: str                 # Current processing step
```

### Agent Graph (`agent/graph.py`)

**Purpose**: Define the workflow of content generation.

**Workflow Diagram**:

```
START
  ↓
[Plan Node] ─────────────────────────────────┐
  ↓                                          │
[Generate Node] ─────────────────────────────┤
  ↓                                          │
[Validate Node]                              │
  ↓                                          │
  ├─ Valid? ──→ [Hashtag Node]               │
  │               ↓                          │
  │             [Finalize Node]              │
  │               ↓                          │
  │             END                          │
  │                                          │
  └─ Invalid? ──→ END (with error) ──────────┘
```

**Code Explanation**:

```python
def create_agent_graph():
    """
    Creates the LangGraph workflow
    
    Steps:
    1. Create StateGraph with AgentState
    2. Add nodes (plan, generate, validate, hashtags, finalize)
    3. Define edges (connections between nodes)
    4. Add conditional logic (valid → hashtags, invalid → end)
    5. Compile graph
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("plan", plan_node)
    workflow.add_node("generate", generate_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("add_hashtags", hashtag_node)
    workflow.add_node("finalize", finalize_node)
    
    # Define flow
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "generate")
    workflow.add_edge("generate", "validate")
    
    # Conditional: if valid → hashtags, else → end
    workflow.add_conditional_edges(
        "validate",
        lambda state: "add_hashtags" if state.get("is_valid") else "end",
        {"add_hashtags": "add_hashtags", "end": END}
    )
    
    workflow.add_edge("add_hashtags", "finalize")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()
```

**Run Agent Function**:

```python
async def run_agent(user_prompt: str, platform: str = "twitter") -> AgentState:
    """
    Execute the agent workflow
    
    Process:
    1. Create agent graph
    2. Initialize state with user input
    3. Run graph (processes through all nodes)
    4. Return final state with generated content
    
    Example:
    Input:  "Write about AI in healthcare"
    Output: {
        "tweet_content": "AI is revolutionizing healthcare...",
        "hashtags": ["#AI", "#Healthcare"],
        "final_content": "AI is revolutionizing healthcare...\n\n#AI #Healthcare",
        "char_count": 95,
        "is_valid": True
    }
    """
```

### Agent Nodes (`agent/nodes.py`)

Each node is a processing step in the workflow.

#### 1. Plan Node

```python
async def plan_node(state: AgentState) -> AgentState:
    """
    Validates the user input
    
    Process:
    1. Check if prompt is not empty
    2. Set is_valid flag
    3. Return state
    
    Purpose: Early validation before expensive AI calls
    """
    if not state.get("user_prompt") or len(state["user_prompt"].strip()) == 0:
        state["error"] = "User prompt is empty"
        state["is_valid"] = False
        return state
    
    state["is_valid"] = True
    return state
```

#### 2. Generate Node

```python
async def generate_node(state: AgentState) -> AgentState:
    """
    Generates content using Gemini AI
    
    Process:
    1. Get platform from state
    2. Call Gemini service with platform-specific prompt
    3. Store generated content in state
    4. Mark as valid if successful
    
    Example:
    Input:  user_prompt="Write about AI", platform="twitter"
    Output: tweet_content="AI is transforming how we work..."
    """
    platform = state.get("platform", "twitter")
    gemini_service = get_gemini_service()
    
    # Generate with platform-specific prompt
    tweet_content = await gemini_service.generate_tweet(
        state["user_prompt"], 
        platform
    )
    
    state["tweet_content"] = tweet_content
    state["is_valid"] = True
    return state
```

#### 3. Validate Node

```python
async def validate_node(state: AgentState) -> AgentState:
    """
    Validates generated content
    
    Process:
    1. Check content length (must be ≤ 280 chars for Twitter)
    2. Check content is not empty
    3. Set is_valid flag
    
    Purpose: Ensure content meets platform requirements
    """
    is_valid = validate_tweet_length(state.get("tweet_content", ""))
    state["is_valid"] = is_valid
    
    if not is_valid:
        state["error"] = "Tweet content is invalid or too long"
    
    return state
```

#### 4. Hashtag Node

```python
async def hashtag_node(state: AgentState) -> AgentState:
    """
    Generates relevant hashtags
    
    Process:
    1. Get platform from state
    2. Call Gemini to generate hashtags
    3. Store hashtags in state
    4. Continue even if hashtag generation fails
    
    Example:
    Input:  tweet_content="AI is transforming healthcare"
    Output: hashtags=["#AI", "#Healthcare", "#Innovation"]
    """
    platform = state.get("platform", "twitter")
    gemini_service = get_gemini_service()
    
    hashtags = await gemini_service.generate_hashtags(
        state["tweet_content"], 
        platform
    )
    
    state["hashtags"] = hashtags
    return state
```

#### 5. Finalize Node

```python
async def finalize_node(state: AgentState) -> AgentState:
    """
    Combines content with hashtags
    
    Process:
    1. Combine tweet_content + hashtags
    2. Calculate character count
    3. Final validation
    4. Return complete state
    
    Example:
    Input:  
        tweet_content="AI is transforming healthcare"
        hashtags=["#AI", "#Healthcare"]
    Output: 
        final_content="AI is transforming healthcare\n\n#AI #Healthcare"
        char_count=50
    """
    final_content = combine_content_and_hashtags(
        state["tweet_content"],
        state.get("hashtags", [])
    )
    
    state["final_content"] = final_content
    state["char_count"] = get_char_count(final_content)
    state["is_valid"] = validate_tweet_length(final_content)
    
    return state
```

---

### Gemini Service (`services/gemini_service.py`)

**Purpose**: Interface with Google Gemini AI for content generation.

#### Generate Content

```python
async def generate_tweet(self, user_prompt: str, platform: str = "twitter") -> str:
    """
    Generate platform-specific content
    
    Process:
    1. Get platform-specific prompt template
    2. Format prompt with user input
    3. Call Gemini API
    4. Extract and validate response
    5. Apply length limits
    6. Return generated content
    
    Platform Limits:
    - Twitter: 250 chars (leave room for hashtags)
    - LinkedIn: 1300 chars
    - Reddit: 10000 chars
    
    Example:
    Input:  "Write about AI", platform="twitter"
    Prompt: "You are a Twitter expert. Create engaging tweet...
             User Prompt: Write about AI
             Requirements: Max 250 chars, casual tone..."
    Output: "AI is revolutionizing how we work, learn, and create! 🚀"
    """
    # Get platform-specific prompt
    prompt = get_platform_prompt(platform, "generation", user_prompt=user_prompt)
    
    # Call Gemini
    response = await self.client.models.generate_content(
        model=self.model_name,
        contents=prompt
    )
    
    content = response.text.strip()
    
    # Apply length limit
    max_length = 250 if platform == "twitter" else 1300
    if len(content) > max_length:
        content = content[:max_length - 3] + "..."
    
    return content
```

#### Generate Hashtags

```python
async def generate_hashtags(self, content: str, platform: str = "twitter") -> List[str]:
    """
    Generate relevant hashtags
    
    Process:
    1. Skip if platform doesn't use hashtags (Reddit)
    2. Get platform-specific hashtag prompt
    3. Call Gemini API
    4. Parse hashtags from response
    5. Apply platform limits
    6. Return hashtag list
    
    Platform Limits:
    - Twitter: 3 hashtags max
    - LinkedIn: 5 hashtags max
    - Reddit: 0 (doesn't use hashtags)
    
    Example:
    Input:  "AI is revolutionizing healthcare"
    Output: ["#AI", "#Healthcare", "#Innovation"]
    """
    if platform == "reddit":
        return []  # Reddit doesn't use hashtags
    
    prompt = get_platform_prompt(platform, "hashtags", content=content)
    response = await self.client.models.generate_content(
        model=self.model_name,
        contents=prompt
    )
    
    # Parse hashtags
    hashtags = []
    for word in response.text.split():
        if word.startswith('#'):
            hashtags.append(word)
    
    # Apply limit
    max_hashtags = 3 if platform == "twitter" else 5
    return hashtags[:max_hashtags]
```

---

### Platform-Specific Prompts (`prompts/templates.py`)

**Purpose**: Define AI prompts tailored to each platform's style and requirements.

```python
PLATFORM_PROMPTS = {
    "twitter": {
        "generation": """
        You are a Twitter expert.
        Create engaging tweet for: {user_prompt}
        
        Requirements:
        - Max 250 characters
        - Casual, conversational tone
        - Short, punchy sentences
        - No hashtags (added separately)
        - Use emojis sparingly
        - Make it shareable
        """,
        "hashtags": """
        Generate 2-3 trending Twitter hashtags for: {content}
        Return only hashtags: #AI #Tech #Innovation
        """
    },
    "linkedin": {
        "generation": """
        You are a LinkedIn professional.
        Create engaging post for: {user_prompt}
        
        Requirements:
        - Max 1300 characters
        - Professional yet conversational
        - Use paragraphs
        - Strong opening hook
        - Add value/insights
        - No hashtags (added separately)
        """,
        "hashtags": """
        Generate 3-5 professional LinkedIn hashtags for: {content}
        Return only hashtags: #Leadership #Business #Innovation
        """
    },
    "reddit": {
        "generation": """
        You are a Reddit community member.
        Create authentic post for: {user_prompt}
        
        Requirements:
        - Authentic, genuine tone
        - No marketing speak
        - Provide value
        - Start discussion
        - No hashtags (Reddit doesn't use them)
        """,
        "hashtags": "Reddit doesn't use hashtags."
    }
}
```

---

## API Endpoints

### 1. Generate Content (`POST /api/generate`)

**Purpose**: Generate platform-specific content using AI.

**Flow Diagram**:
```
Request → Verify JWT → Extract User ID → Run Agent → Return Content
```

**Code Breakdown**:

```python
@app.post("/api/generate")
async def generate_content(
    request: GenerateRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Step-by-step process:
    
    1. AUTHENTICATION
       - Extract Bearer token from Authorization header
       - Verify JWT with Supabase
       - Get user_id from token
    
    2. VALIDATION
       - Check prompt is not empty
       - Validate platform (twitter/linkedin/reddit)
    
    3. CONTENT GENERATION
       - Run agent with prompt and platform
       - Agent goes through: plan → generate → validate → hashtags → finalize
       - Get final state with generated content
    
    4. RESPONSE
       - Return generated content, hashtags, char count
       - Or return error if generation failed
    """
    
    # 1. Authentication
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")
    
    token = authorization.split(" ")[1]
    user_data = supabase_service.verify_jwt_token(token)
    user_id = user_data.get("sub")
    
    # 2. Run Agent
    final_state = await run_agent(request.prompt, request.platform)
    
    # 3. Check Result
    if not final_state.get("is_valid"):
        return GenerateResponse(
            success=False,
            error=final_state.get("error")
        )
    
    # 4. Return Success
    return GenerateResponse(
        success=True,
        data={
            "platform": request.platform,
            "content": final_state.get("tweet_content"),
            "hashtags": final_state.get("hashtags"),
            "final_content": final_state.get("final_content"),
            "char_count": final_state.get("char_count"),
        }
    )
```

**Request Example**:
```json
{
  "prompt": "Write about the future of AI in healthcare",
  "platform": "twitter"
}
```

**Response Example**:
```json
{
  "success": true,
  "data": {
    "platform": "twitter",
    "content": "AI is revolutionizing healthcare with predictive diagnostics...",
    "hashtags": ["#AI", "#Healthcare", "#Innovation"],
    "final_content": "AI is revolutionizing healthcare...\n\n#AI #Healthcare #Innovation",
    "char_count": 95
  }
}
```

---

### 2. Post Content (`POST /api/post`)

**Purpose**: Post generated content to social media using user's OAuth tokens.

**Flow Diagram**:
```
Request → Verify JWT → Get User's Connected Account → 
Post to Platform → Save to Database → Return URL
```

**Code Breakdown**:

```python
@app.post("/api/post")
async def post_content(
    request: PostRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Step-by-step process:
    
    1. AUTHENTICATION
       - Verify JWT token
       - Extract user_id
    
    2. CHECK CONNECTED ACCOUNT
       - Query database for user's connected account
       - Verify account exists for platform
       - Check account is active
    
    3. POST TO PLATFORM
       - Use user's OAuth access token (NOT app token)
       - Call platform API (Twitter/LinkedIn/Reddit)
       - Get post ID and URL from response
    
    4. SAVE TO DATABASE
       - Store post in Supabase
       - Include: user_id, platform, content, hashtags, post_url
       - Mark status as "posted"
    
    5. RETURN RESULT
       - Return post URL for user to view
    """
    
    # 1. Authentication
    token = authorization.split(" ")[1]
    user_data = supabase_service.verify_jwt_token(token)
    user_id = user_data.get("sub")
    
    # 2. Get Connected Account
    account = supabase_service.get_platform_connection(user_id, request.platform)
    
    if not account:
        raise HTTPException(400, f"No {request.platform} account connected")
    
    if not account.get("is_active"):
        raise HTTPException(400, f"Account not active")
    
    # 3. Post to Platform
    if request.platform == "twitter":
        twitter_oauth = TwitterOAuthService()
        result = await twitter_oauth.post_tweet(
            request.content,
            account["access_token"]  # User's token, not app token!
        )
    
    # 4. Save to Database
    post_data = {
        "user_id": user_id,
        "platform": request.platform,
        "user_prompt": request.user_prompt,
        "generated_content": request.content,
        "hashtags": request.hashtags,
        "platform_post_id": result.get("tweet_id"),
        "platform_post_url": result.get("url"),
        "status": "posted"
    }
    
    supabase_service.save_post(post_data)
    
    # 5. Return Success
    return PostResponse(
        success=True,
        post_id=result.get("tweet_id"),
        url=result.get("url")
    )
```

**Request Example**:
```json
{
  "content": "AI is revolutionizing healthcare...\n\n#AI #Healthcare",
  "user_prompt": "Write about AI in healthcare",
  "platform": "twitter",
  "hashtags": ["#AI", "#Healthcare"]
}
```

**Response Example**:
```json
{
  "success": true,
  "post_id": "1234567890",
  "url": "https://twitter.com/i/web/status/1234567890"
}
```

---

### 3. Get History (`GET /api/history`)

**Purpose**: Fetch user's post history from database.

**Code Breakdown**:

```python
@app.get("/api/history")
async def get_post_history(
    authorization: Optional[str] = Header(None),
    platform: Optional[str] = None,
    limit: int = 50
):
    """
    Process:
    
    1. AUTHENTICATION
       - Verify JWT token
       - Extract user_id
    
    2. QUERY DATABASE
       - Get posts for user_id
       - Filter by platform if specified
       - Order by created_at DESC
       - Limit results
    
    3. FORMAT RESPONSE
       - Convert database records to PostHistoryItem models
       - Include all post metadata
    
    4. RETURN RESULTS
    """
    
    # 1. Authentication
    token = authorization.split(" ")[1]
    user_data = supabase_service.verify_jwt_token(token)
    user_id = user_data.get("sub")
    
    # 2. Query Database
    posts_data = supabase_service.get_user_posts(user_id, platform, limit)
    
    # 3. Format Response
    posts = []
    for post in posts_data:
        posts.append(PostHistoryItem(
            id=post.get("id"),
            platform=post.get("platform"),
            user_prompt=post.get("user_prompt"),
            generated_content=post.get("generated_content"),
            hashtags=post.get("hashtags", []),
            platform_post_url=post.get("platform_post_url"),
            status=post.get("status"),
            created_at=post.get("created_at")
        ))
    
    # 4. Return
    return HistoryResponse(success=True, posts=posts)
```

---

### 4. Twitter OAuth Login (`GET /api/auth/twitter/login`)

**Purpose**: Initiate Twitter OAuth flow.

**Code Breakdown**:

```python
@app.get("/api/auth/twitter/login")
async def twitter_login(authorization: Optional[str] = Header(None)):
    """
    Process:
    
    1. VERIFY USER
       - Check JWT token
       - Get user_id
    
    2. GENERATE OAUTH STATE
       - Create random state for CSRF protection
       - Generate PKCE code_verifier and code_challenge
    
    3. BUILD AUTHORIZATION URL
       - Twitter OAuth URL with parameters:
         * client_id
         * redirect_uri
         * scope (tweet.read, tweet.write, users.read, offline.access)
         * state (CSRF token)
         * code_challenge (PKCE)
    
    4. STORE STATE
       - Temporarily store state + code_verifier + user_id
       - Needed for callback verification
    
    5. RETURN URL
       - Frontend redirects user to this URL
       - User authorizes app on Twitter
       - Twitter redirects back to callback
    """
    
    # 1. Verify User
    token = authorization.split(" ")[1]
    user_data = supabase_service.verify_jwt_token(token)
    user_id = user_data.get("sub")
    
    # 2. Generate State
    state = secrets.token_urlsafe(32)
    
    # 3. Get Authorization URL
    auth_url, code_verifier, state = twitter_oauth.get_authorization_url(state)
    
    # 4. Store State
    oauth_states[state] = {
        "user_id": user_id,
        "code_verifier": code_verifier
    }
    
    # 5. Return URL
    return {"success": True, "auth_url": auth_url}
```

---

### 5. Twitter OAuth Callback (`GET /api/auth/twitter/callback`)

**Purpose**: Handle Twitter OAuth redirect and save tokens.

**Code Breakdown**:

```python
@app.get("/api/auth/twitter/callback")
async def twitter_callback(code: str, state: str):
    """
    Process:
    
    1. VERIFY STATE
       - Check state parameter matches stored state
       - Prevents CSRF attacks
    
    2. EXCHANGE CODE FOR TOKEN
       - Use authorization code + code_verifier
       - Call Twitter token endpoint
       - Get access_token, refresh_token, expires_in
    
    3. GET USER INFO
       - Use access_token to call Twitter API
       - Get user's Twitter ID and username
    
    4. SAVE TO DATABASE
       - Store in connected_accounts table:
         * user_id (from our database)
         * platform = "twitter"
         * platform_user_id (Twitter user ID)
         * platform_username (Twitter @username)
         * access_token (for posting tweets)
         * refresh_token (for renewing access)
         * token_expires_at
         * scope
         * is_active = true
    
    5. CLEANUP & REDIRECT
       - Delete temporary state
       - Redirect to frontend settings page
    """
    
    # 1. Verify State
    if state not in oauth_states:
        raise HTTPException(400, "Invalid state")
    
    oauth_data = oauth_states[state]
    user_id = oauth_data["user_id"]
    code_verifier = oauth_data["code_verifier"]
    
    # 2. Exchange Code
    token_response = await twitter_oauth.exchange_code_for_token(
        code, 
        code_verifier
    )
    
    # 3. Get User Info
    user_info = await twitter_oauth.get_user_info(
        token_response["access_token"]
    )
    twitter_user = user_info["data"]
    
    # 4. Save to Database
    account_data = {
        "user_id": user_id,
        "platform": "twitter",
        "platform_user_id": twitter_user["id"],
        "platform_username": twitter_user["username"],
        "access_token": token_response["access_token"],
        "refresh_token": token_response.get("refresh_token"),
        "token_expires_at": calculate_expiry(token_response["expires_in"]),
        "scope": token_response.get("scope", "").split(),
        "is_active": True
    }
    
    supabase_service.save_connected_account(account_data)
    
    # 5. Cleanup & Redirect
    del oauth_states[state]
    return RedirectResponse(url=f"{FRONTEND_URL}/settings?connected=twitter")
```

---

## OAuth Integration

### Twitter OAuth Service (`services/social/twitter_service.py`)

**Purpose**: Handle Twitter OAuth 2.0 with PKCE flow.

#### PKCE (Proof Key for Code Exchange)

**Why PKCE?**
- Protects against authorization code interception
- Required for public clients (SPAs, mobile apps)
- More secure than client_secret

**How it works**:

```python
def generate_pkce_pair(self) -> tuple[str, str]:
    """
    Generate PKCE pair
    
    Process:
    1. Generate random code_verifier (43-128 chars)
    2. Hash code_verifier with SHA256
    3. Base64 encode hash = code_challenge
    
    Example:
    code_verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    code_challenge = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
    
    Flow:
    1. Send code_challenge to Twitter (authorization request)
    2. Twitter stores code_challenge
    3. Send code_verifier to Twitter (token request)
    4. Twitter verifies: SHA256(code_verifier) == code_challenge
    """
    # Generate verifier
    code_verifier = base64.urlsafe_b64encode(
        secrets.token_bytes(32)
    ).decode('utf-8').rstrip('=')
    
    # Generate challenge
    code_challenge = hashlib.sha256(
        code_verifier.encode('utf-8')
    ).digest()
    code_challenge = base64.urlsafe_b64encode(
        code_challenge
    ).decode('utf-8').rstrip('=')
    
    return code_verifier, code_challenge
```

#### Post Tweet

```python
async def post_tweet(self, text: str, access_token: str) -> Dict:
    """
    Post tweet to Twitter API v2
    
    Process:
    1. Prepare request with user's access_token
    2. Call Twitter API POST /2/tweets
    3. Parse response to get tweet ID
    4. Construct tweet URL
    5. Return result
    
    Important: Uses USER'S access_token, not app token!
    This posts as the user, not as the app.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {"text": text}
    
    response = await httpx.AsyncClient().post(
        "https://api.twitter.com/2/tweets",
        headers=headers,
        json=data
    )
    
    result = response.json()
    tweet_id = result.get("data", {}).get("id")
    url = f"https://twitter.com/i/web/status/{tweet_id}"
    
    return {
        "tweet_id": tweet_id,
        "url": url
    }
```

---

## Code Flow Examples

### Example 1: Complete Content Generation Flow

```
User Action: Click "Generate Content"
├─ Frontend sends POST /api/generate
│  ├─ Headers: Authorization: Bearer <jwt_token>
│  └─ Body: { "prompt": "Write about AI", "platform": "twitter" }
│
├─ Backend: main.py::generate_content()
│  ├─ Extract JWT token from header
│  ├─ Call supabase_service.verify_jwt_token(token)
│  │  ├─ Decode JWT with HS256
│  │  ├─ Verify signature
│  │  ├─ Check audience = "authenticated"
│  │  └─ Return user_id
│  │
│  ├─ Call run_agent(prompt, platform)
│  │  ├─ Create agent graph
│  │  ├─ Initialize state: { user_prompt, platform, ... }
│  │  │
│  │  ├─ Execute: plan_node(state)
│  │  │  ├─ Validate prompt not empty
│  │  │  └─ Return state with is_valid=True
│  │  │
│  │  ├─ Execute: generate_node(state)
│  │  │  ├─ Call gemini_service.generate_tweet(prompt, platform)
│  │  │  │  ├─ Get platform prompt: get_platform_prompt("twitter", "generation")
│  │  │  │  ├─ Format: "You are Twitter expert... User: Write about AI"
│  │  │  │  ├─ Call Gemini API
│  │  │  │  ├─ Get response: "AI is transforming how we work..."
│  │  │  │  └─ Return content
│  │  │  └─ Store in state.tweet_content
│  │  │
│  │  ├─ Execute: validate_node(state)
│  │  │  ├─ Check length ≤ 280
│  │  │  └─ Set is_valid=True
│  │  │
│  │  ├─ Execute: hashtag_node(state)
│  │  │  ├─ Call gemini_service.generate_hashtags(content, platform)
│  │  │  │  ├─ Get hashtag prompt
│  │  │  │  ├─ Call Gemini API
│  │  │  │  ├─ Parse: "#AI #Tech #Innovation"
│  │  │  │  └─ Return ["#AI", "#Tech", "#Innovation"]
│  │  │  └─ Store in state.hashtags
│  │  │
│  │  ├─ Execute: finalize_node(state)
│  │  │  ├─ Combine content + hashtags
│  │  │  ├─ Calculate char_count
│  │  │  ├─ Final validation
│  │  │  └─ Return final state
│  │  │
│  │  └─ Return final_state
│  │
│  └─ Return GenerateResponse with generated content
│
└─ Frontend receives response and displays to user
```

### Example 2: Complete Posting Flow

```
User Action: Click "Post to Twitter"
├─ Frontend sends POST /api/post
│  ├─ Headers: Authorization: Bearer <jwt_token>
│  └─ Body: {
│       "content": "AI is transforming...\n\n#AI #Tech",
│       "user_prompt": "Write about AI",
│       "platform": "twitter",
│       "hashtags": ["#AI", "#Tech"]
│     }
│
├─ Backend: main.py::post_content()
│  ├─ Verify JWT → get user_id
│  │
│  ├─ Get connected account
│  │  ├─ Call supabase_service.get_platform_connection(user_id, "twitter")
│  │  ├─ Query: SELECT * FROM connected_accounts 
│  │  │         WHERE user_id = ? AND platform = 'twitter'
│  │  └─ Return: {
│  │       "access_token": "user_twitter_token",
│  │       "platform_username": "@johndoe",
│  │       "is_active": true
│  │     }
│  │
│  ├─ Check account exists and is active
│  │
│  ├─ Post to Twitter
│  │  ├─ Call twitter_oauth.post_tweet(content, access_token)
│  │  ├─ POST https://api.twitter.com/2/tweets
│  │  │  ├─ Headers: Authorization: Bearer <user_access_token>
│  │  │  └─ Body: { "text": "AI is transforming...\n\n#AI #Tech" }
│  │  ├─ Twitter Response: {
│  │  │    "data": { "id": "1234567890", "text": "..." }
│  │  │  }
│  │  └─ Return: {
│  │       "tweet_id": "1234567890",
│  │       "url": "https://twitter.com/i/web/status/1234567890"
│  │     }
│  │
│  ├─ Save to database
│  │  ├─ Call supabase_service.save_post({
│  │  │    "user_id": user_id,
│  │  │    "platform": "twitter",
│  │  │    "user_prompt": "Write about AI",
│  │  │    "generated_content": "AI is transforming...",
│  │  │    "hashtags": ["#AI", "#Tech"],
│  │  │    "platform_post_id": "1234567890",
│  │  │    "platform_post_url": "https://twitter.com/...",
│  │  │    "status": "posted"
│  │  │  })
│  │  └─ INSERT INTO posts (...) VALUES (...)
│  │
│  └─ Return PostResponse with URL
│
└─ Frontend displays success + link to tweet
```

---

## Database Schema

### connected_accounts Table

```sql
CREATE TABLE connected_accounts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),  -- Links to Supabase auth
  platform TEXT,                            -- 'twitter', 'linkedin', 'reddit'
  platform_user_id TEXT,                    -- User ID on that platform
  platform_username TEXT,                   -- @username
  access_token TEXT,                        -- OAuth access token
  refresh_token TEXT,                       -- OAuth refresh token
  token_expires_at TIMESTAMP,               -- When token expires
  scope TEXT[],                             -- OAuth scopes granted
  is_active BOOLEAN,                        -- Account status
  connected_at TIMESTAMP,                   -- When connected
  updated_at TIMESTAMP,                     -- Last updated
  
  UNIQUE(user_id, platform)                 -- One account per platform per user
);
```

### posts Table

```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),  -- Who created this post
  platform TEXT,                            -- Where it was posted
  user_prompt TEXT,                         -- Original user input
  generated_content TEXT,                   -- AI-generated content
  hashtags TEXT[],                          -- Generated hashtags
  platform_post_id TEXT,                    -- ID from social platform
  platform_post_url TEXT,                   -- URL to view post
  status TEXT,                              -- 'posted', 'failed', 'deleted'
  created_at TIMESTAMP                      -- When posted
);
```

---

## Environment Variables

```bash
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
SUPABASE_JWT_SECRET=your-jwt-secret

# Google Gemini AI
GEMINI_API_KEY=AIzaSyxxx...

# Twitter OAuth 2.0
TWITTER_CLIENT_ID=your-client-id
TWITTER_CLIENT_SECRET=your-client-secret
TWITTER_REDIRECT_URI=http://localhost:8000/api/auth/twitter/callback

# App Config
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
PORT=8000
```

---

## Security Considerations

### 1. JWT Verification
- Always verify JWT signature
- Check audience claim
- Validate expiration
- Never trust client-provided user_id

### 2. OAuth Token Storage
- Store tokens encrypted in database
- Never expose tokens in API responses
- Use user's tokens, not app tokens for posting
- Implement token refresh logic

### 3. CORS Configuration
- Restrict origins to known domains
- Don't use wildcard (*) in production
- Enable credentials for cookie support

### 4. Rate Limiting
- Implement rate limits on API endpoints
- Protect against abuse
- Use user_id for per-user limits

---

## Error Handling

### Common Error Patterns

```python
# Authentication Error
if not authorization:
    raise HTTPException(401, "Not authenticated")

# Validation Error
if not request.prompt:
    raise HTTPException(400, "Prompt is required")

# Not Found Error
if not account:
    raise HTTPException(404, "Account not found")

# External API Error
try:
    result = await twitter_api.post()
except Exception as e:
    raise HTTPException(500, f"Failed to post: {str(e)}")
```

---

## Testing the Backend

### 1. Test Content Generation

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about AI in healthcare",
    "platform": "twitter"
  }'
```

### 2. Test Posting

```bash
curl -X POST http://localhost:8000/api/post \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI is transforming healthcare...",
    "user_prompt": "Write about AI",
    "platform": "twitter",
    "hashtags": ["#AI", "#Healthcare"]
  }'
```

### 3. Test History

```bash
curl http://localhost:8000/api/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Summary

This backend implements a **multi-user, multi-platform AI content generation system** with:

1. **Authentication**: JWT-based auth with Supabase
2. **AI Agent**: LangGraph-powered content generation
3. **Platform Support**: Twitter (LinkedIn/Reddit coming)
4. **OAuth Integration**: Secure token management
5. **Database**: User posts and connections in Supabase
6. **Security**: Proper token verification and user isolation

The system is designed to be **scalable**, **secure**, and **extensible** for adding more platforms.

