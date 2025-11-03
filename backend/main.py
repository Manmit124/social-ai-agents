from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
load_dotenv()

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os
import secrets
from typing import Optional

from models.schemas import (
    GenerateRequest,
    GenerateResponse,
    PostRequest,
    PostResponse,
    HistoryResponse,
    PostHistoryItem,
    TweetHistoryItem
)
from auth.supabase_auth import get_current_user
from agent.graph import run_agent
from storage.tweet_storage import TweetStorage
from services.social.twitter_service import TwitterOAuthService
from services.social.github_service import GitHubOAuthService
from services.supabase_service import supabase_service
from services.github_data_service import GitHubDataService

# Initialize FastAPI app
app = FastAPI(
    title="Mataru.ai API",
    description="AI-powered social media content generator with agentic workflows",
    version="1.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
tweet_storage = TweetStorage()
twitter_oauth = TwitterOAuthService()
github_oauth = GitHubOAuthService()
github_data_service = GitHubDataService()

# Store OAuth states temporarily (in production, use Redis or database)
oauth_states = {}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Mataru.ai API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Generate content using the agentic AI workflow.
    
    Args:
        request: GenerateRequest with user prompt and platform
        authorization: JWT token in Authorization header
        
    Returns:
        GenerateResponse with generated content data
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        print(f"\n📝 User {user_id} - Received prompt for {request.platform}: {request.prompt}")
        
        # Run the agent with platform parameter
        final_state = await run_agent(request.prompt, request.platform)
        
        # Check if generation was successful
        if not final_state.get("is_valid"):
            error_msg = final_state.get("error", "Content generation failed")
            return GenerateResponse(
                success=False,
                error=error_msg
            )
        
        # Return the generated content data
        return GenerateResponse(
            success=True,
            data={
                "platform": request.platform,
                "content": final_state.get("tweet_content", ""),
                "hashtags": final_state.get("hashtags", []),
                "final_content": final_state.get("final_content", ""),
                "char_count": final_state.get("char_count", 0),
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in generate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/post", response_model=PostResponse)
async def post_content(
    request: PostRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Post the generated content to the specified platform using user's connected account.
    
    Args:
        request: PostRequest with content, platform, and hashtags
        authorization: JWT token in Authorization header
        
    Returns:
        PostResponse with post URL
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        print(f"\n🚀 User {user_id} - Posting to {request.platform}: {request.content[:50]}...")
        
        # Get user's connected account for this platform
        account = supabase_service.get_platform_connection(user_id, request.platform)
        
        if not account:
            raise HTTPException(
                status_code=400,
                detail=f"No {request.platform} account connected. Please connect your account first."
            )
        
        if not account.get("is_active"):
            raise HTTPException(
                status_code=400,
                detail=f"Your {request.platform} account is not active. Please reconnect."
            )
        
        # Debug: Check what fields we have
        print(f"📊 Account data fields: {list(account.keys())}")
        print(f"📊 Has expires_at: {account.get('expires_at') is not None}")
        print(f"📊 Has refresh_token: {account.get('refresh_token') is not None}")
        
        # Post to platform using user's tokens
        result = None
        if request.platform == "twitter":
            # Use Twitter OAuth service with user's access token
            twitter_oauth = TwitterOAuthService()
            
            # Check if token is expired and refresh if needed
            access_token = account["access_token"]
            if account.get("expires_at"):
                from datetime import datetime, timezone
                
                # Parse the expires_at timestamp
                expires_at_str = account["expires_at"]
                if isinstance(expires_at_str, str):
                    # Handle ISO format with or without timezone
                    if expires_at_str.endswith('Z'):
                        expires_at_str = expires_at_str.replace('Z', '+00:00')
                    expires_at = datetime.fromisoformat(expires_at_str)
                    # Ensure it's timezone-aware
                    if expires_at.tzinfo is None:
                        expires_at = expires_at.replace(tzinfo=timezone.utc)
                else:
                    expires_at = expires_at_str
                
                if twitter_oauth.is_token_expired(expires_at):
                    print(f"🔄 Token expired, refreshing for user {user_id}...")
                    try:
                        # Refresh the token
                        token_response = await twitter_oauth.refresh_access_token(account["refresh_token"])
                        
                        # Update the access token
                        access_token = token_response["access_token"]
                        
                        # Update tokens in database
                        new_expires_at = twitter_oauth.calculate_token_expiry(token_response.get("expires_in", 7200))
                        supabase_service.update_platform_tokens(
                            user_id,
                            request.platform,
                            access_token,
                            token_response.get("refresh_token", account["refresh_token"]),
                            new_expires_at
                        )
                        print(f"✅ Token refreshed successfully for user {user_id}")
                    except Exception as e:
                        print(f"❌ Failed to refresh token: {str(e)}")
                        raise HTTPException(
                            status_code=401,
                            detail="Your session has expired. Please reconnect your account."
                        )
            
            result = await twitter_oauth.post_tweet(
                request.content,
                access_token
            )
        elif request.platform == "linkedin":
            # LinkedIn posting will be implemented in Phase 2
            raise HTTPException(status_code=501, detail="LinkedIn posting not yet implemented")
        elif request.platform == "reddit":
            # Reddit posting will be implemented in Phase 3
            raise HTTPException(status_code=501, detail="Reddit posting not yet implemented")
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to post content")
        
        # Save to Supabase
        post_data = {
            "user_id": user_id,
            "platform": request.platform,
            "user_prompt": request.user_prompt,
            "generated_content": request.content,
            "hashtags": request.hashtags or [],
            "platform_post_id": result.get("post_id") or result.get("tweet_id"),
            "platform_post_url": result.get("url"),
            "status": "posted"
        }
        
        post_id = supabase_service.save_post(post_data)
        
        print(f"✅ Posted successfully to {request.platform}: {result.get('url')}")
        
        return PostResponse(
            success=True,
            post_id=result.get("post_id") or result.get("tweet_id"),
            url=result.get("url")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error posting content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history", response_model=HistoryResponse)
async def get_post_history(
    authorization: Optional[str] = Header(None),
    platform: Optional[str] = None,
    limit: int = 50
):
    """
    Get user's post history from Supabase.
    
    Args:
        authorization: JWT token in Authorization header
        platform: Optional filter by platform
        limit: Maximum number of posts to return
        
    Returns:
        HistoryResponse with list of posts
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Get posts from Supabase
        posts_data = supabase_service.get_user_posts(user_id, platform, limit)
        
        # Convert to PostHistoryItem models
        posts = []
        for post in posts_data:
            posts.append(PostHistoryItem(
                id=post.get("id"),
                platform=post.get("platform"),
                user_prompt=post.get("user_prompt", ""),
                generated_content=post.get("generated_content", ""),
                hashtags=post.get("hashtags", []),
                platform_post_id=post.get("platform_post_id"),
                platform_post_url=post.get("platform_post_url"),
                status=post.get("status", "posted"),
                created_at=post.get("created_at", "")
            ))
        
        return HistoryResponse(
            success=True,
            posts=posts
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting history: {str(e)}")
        return HistoryResponse(
            success=False,
            error=str(e),
            posts=[]
        )


@app.get("/api/auth/twitter/login")
async def twitter_login(authorization: Optional[str] = Header(None)):
    """
    Initiate Twitter OAuth flow.
    Requires user to be authenticated (JWT token in Authorization header).
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Get authorization URL
        auth_url, code_verifier, state = twitter_oauth.get_authorization_url(state)
        
        # Store state and code_verifier temporarily
        oauth_states[state] = {
            "user_id": user_id,
            "code_verifier": code_verifier
        }
        
        # Return auth URL for frontend to redirect
        return {
            "success": True,
            "auth_url": auth_url
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error initiating Twitter OAuth: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/twitter/callback")
async def twitter_callback(
    code: str = Query(...),
    state: str = Query(...)
):
    """
    Handle Twitter OAuth callback.
    Exchange code for tokens and save to database.
    """
    try:
        # Verify state
        if state not in oauth_states:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        oauth_data = oauth_states[state]
        user_id = oauth_data["user_id"]
        code_verifier = oauth_data["code_verifier"]
        
        # Exchange code for tokens
        token_response = await twitter_oauth.exchange_code_for_token(code, code_verifier)
        
        # Get user info from Twitter
        user_info = await twitter_oauth.get_user_info(token_response["access_token"])
        twitter_user = user_info["data"]
        
        # Calculate token expiry
        expires_at = twitter_oauth.calculate_token_expiry(token_response["expires_in"])
        
        # Save to database
        account_data = {
            "user_id": user_id,
            "platform": "twitter",
            "platform_user_id": twitter_user["id"],
            "platform_username": twitter_user["username"],
            "access_token": token_response["access_token"],
            "refresh_token": token_response.get("refresh_token"),
            "expires_at": expires_at.isoformat(),  # Fixed: was token_expires_at
            "scope": token_response.get("scope", "").split(),
            "is_active": True
        }
        
        success = supabase_service.save_connected_account(account_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save connection")
        
        # Clean up state
        del oauth_states[state]
        
        # Redirect to frontend success page
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(url=f"{frontend_url}/settings?connected=twitter")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in Twitter callback: {str(e)}")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(url=f"{frontend_url}/settings?error={str(e)}")


@app.get("/api/auth/github/login")
async def github_login(authorization: Optional[str] = Header(None)):
    """
    Initiate GitHub OAuth flow.
    Requires user to be authenticated (JWT token in Authorization header).
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Get authorization URL
        auth_url, state = github_oauth.get_authorization_url(state)
        
        # Store state temporarily
        oauth_states[state] = {
            "user_id": user_id
        }
        
        # Return auth URL for frontend to redirect
        return {
            "success": True,
            "auth_url": auth_url
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error initiating GitHub OAuth: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...)
):
    """
    Handle GitHub OAuth callback.
    Exchange code for tokens and save to database.
    """
    try:
        # Verify state
        if state not in oauth_states:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        oauth_data = oauth_states[state]
        user_id = oauth_data["user_id"]
        
        # Exchange code for tokens
        token_response = await github_oauth.exchange_code_for_token(code)
        
        # Get user info from GitHub
        user_info = await github_oauth.get_user_info(token_response["access_token"])
        
        # Save to database
        account_data = {
            "user_id": user_id,
            "platform": "github",
            "platform_user_id": str(user_info["id"]),
            "platform_username": user_info["login"],
            "access_token": token_response["access_token"],
            "refresh_token": None,  # GitHub doesn't use refresh tokens by default
            "expires_at": None,  # GitHub tokens don't expire by default
            "scope": token_response.get("scope", "").split(","),
            "is_active": True
        }
        
        success = supabase_service.save_connected_account(account_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save connection")
        
        # Clean up state
        del oauth_states[state]
        
        # Redirect to frontend success page
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(url=f"{frontend_url}/settings?connected=github")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in GitHub callback: {str(e)}")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(url=f"{frontend_url}/settings?error={str(e)}")


@app.get("/api/connections")
async def get_connections(authorization: Optional[str] = Header(None)):
    """
    Get user's connected social media accounts.
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Get connected accounts
        accounts = supabase_service.get_connected_accounts(user_id)
        
        # Remove sensitive data
        safe_accounts = []
        for account in accounts:
            safe_accounts.append({
                "platform": account["platform"],
                "platform_username": account.get("platform_username"),
                "is_active": account.get("is_active", True),
                "connected_at": account.get("connected_at")
            })
        
        return {
            "success": True,
            "connections": safe_accounts
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting connections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/connections/{platform}")
async def disconnect_account(
    platform: str,
    authorization: Optional[str] = Header(None)
):
    """
    Disconnect a social media account.
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Get account to revoke token
        account = supabase_service.get_platform_connection(user_id, platform)
        
        if account and platform == "twitter":
            # Revoke token on Twitter
            await twitter_oauth.revoke_token(account["access_token"])
        
        # Delete from database
        success = supabase_service.delete_connected_account(user_id, platform)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to disconnect account")
        
        return {
            "success": True,
            "message": f"{platform.capitalize()} account disconnected"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error disconnecting account: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/github/fetch-data")
async def fetch_github_data(
    authorization: Optional[str] = Header(None),
    days: int = 30
):
    """
    Fetch GitHub commits and store in database.
    
    Args:
        authorization: JWT token in Authorization header
        days: Number of days to fetch (default: 30)
        
    Returns:
        Success message with count of commits fetched
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        print(f"\n📦 User {user_id} - Fetching GitHub data...")
        
        # Get user's GitHub connection
        github_account = supabase_service.get_platform_connection(user_id, "github")
        
        if not github_account:
            raise HTTPException(
                status_code=400,
                detail="No GitHub account connected. Please connect your account first."
            )
        
        if not github_account.get("is_active"):
            raise HTTPException(
                status_code=400,
                detail="Your GitHub account is not active. Please reconnect."
            )
        
        access_token = github_account["access_token"]
        username = github_account["platform_username"]
        
        # Check if this is first fetch or refresh
        last_fetch_info = await github_data_service.get_last_fetch_info(user_id)
        fetch_type = "initial" if not last_fetch_info else "refresh"
        
        # Get last commit date for incremental fetch
        since_date = None
        if fetch_type == "refresh":
            since_date = await github_data_service.get_last_commit_date(user_id)
            print(f"📅 Last commit date: {since_date}")
        
        # Fetch commits from GitHub
        print(f"🔄 Fetching commits from GitHub (last {days} days)...")
        result = await github_oauth.batch_fetch_commits(
            access_token=access_token,
            username=username,
            since_date=since_date,
            days=days,
            max_repos=20
        )
        
        commits = result["commits"]
        print(f"✅ Fetched {len(commits)} commits from {result['repositories_checked']} repositories")
        
        # Save commits to database
        if commits:
            print(f"💾 Saving commits to database...")
            save_result = await github_data_service.save_github_commits(user_id, commits)
            
            new_commits = save_result["new_commits"]
            skipped = save_result["skipped"]
            
            print(f"✅ Saved {new_commits} new commits (skipped {skipped} duplicates)")
            
            # Update fetch log
            from datetime import datetime
            last_commit_date = None
            if commits:
                last_commit_date_str = commits[0]["commit"]["author"]["date"]
                last_commit_date = datetime.fromisoformat(last_commit_date_str.replace("Z", "+00:00"))
            
            await github_data_service.update_fetch_log(
                user_id=user_id,
                last_commit_date=last_commit_date,
                total_count=new_commits,
                fetch_type=fetch_type
            )
            
            return {
                "success": True,
                "message": f"Fetched {new_commits} new commits from {result['repositories_checked']} repositories",
                "data": {
                    "new_commits": new_commits,
                    "skipped_duplicates": skipped,
                    "repositories_checked": result['repositories_checked'],
                    "fetch_type": fetch_type
                }
            }
        else:
            return {
                "success": True,
                "message": "No new commits found",
                "data": {
                    "new_commits": 0,
                    "skipped_duplicates": 0,
                    "repositories_checked": result['repositories_checked'],
                    "fetch_type": fetch_type
                }
            }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching GitHub data: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/github/activity")
async def get_github_activity(
    authorization: Optional[str] = Header(None),
    limit: int = 100,
    days: Optional[int] = None
):
    """
    Get user's stored GitHub activity.
    
    Args:
        authorization: JWT token in Authorization header
        limit: Maximum number of commits to return (default: 100)
        days: Only return commits from last N days (optional)
        
    Returns:
        List of commits from database
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Get activity from database
        activity = await github_data_service.get_user_github_activity(
            user_id=user_id,
            limit=limit,
            days=days
        )
        
        # Get additional stats
        total_commits = await github_data_service.get_commit_count(user_id)
        repositories = await github_data_service.get_repositories(user_id)
        last_fetch_info = await github_data_service.get_last_fetch_info(user_id)
        
        return {
            "success": True,
            "data": {
                "commits": activity,
                "total_commits": total_commits,
                "repositories": repositories,
                "last_fetch": last_fetch_info
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting GitHub activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/github/status")
async def get_github_status(authorization: Optional[str] = Header(None)):
    """
    Get GitHub data freshness status with smart refresh recommendations.
    
    Args:
        authorization: JWT token in Authorization header
        
    Returns:
        Status information about GitHub data with refresh recommendations
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Get comprehensive refresh recommendation
        recommendation = await github_data_service.get_refresh_recommendation(user_id)
        
        # Get repositories list
        repositories = await github_data_service.get_repositories(user_id)
        
        return {
            "success": True,
            "data": {
                "total_commits": recommendation["total_commits_stored"],
                "last_fetch_time": recommendation["last_fetch_time"],
                "last_commit_date": recommendation["last_commit_date"],
                "needs_refresh": recommendation["should_refresh"],
                "hours_since_fetch": recommendation["hours_since_fetch"],
                "refresh_reason": recommendation["reason"],
                "has_data": recommendation["has_data"],
                "repositories_count": len(repositories),
                "repositories": repositories
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting GitHub status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/github/refresh-check")
async def check_refresh_needed(
    authorization: Optional[str] = Header(None),
    hours_threshold: int = 24
):
    """
    Check if GitHub data needs refresh based on custom threshold.
    
    Args:
        authorization: JWT token in Authorization header
        hours_threshold: Hours after which data is considered stale (default: 24)
        
    Returns:
        Simple refresh check result
    """
    try:
        # Verify user is authenticated
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        token = authorization.split(" ")[1]
        user_data = supabase_service.verify_jwt_token(token)
        user_id = user_data.get("sub")
        
        # Check if refresh is needed
        refresh_check = await github_data_service.should_refresh_data(user_id, hours_threshold)
        
        return {
            "success": True,
            "data": refresh_check
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error checking refresh status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


