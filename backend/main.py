from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from models.schemas import (
    GenerateRequest,
    GenerateResponse,
    PostRequest,
    PostResponse,
    HistoryResponse,
    TweetHistoryItem
)
from agent.graph import run_agent
from services.twitter_service import TwitterService
from storage.tweet_storage import TweetStorage

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Agents Tweet API",
    description="Agentic AI for generating and posting tweets",
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
twitter_service = TwitterService()
tweet_storage = TweetStorage()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Agents Tweet API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_tweet(request: GenerateRequest):
    """
    Generate tweet content using the agentic AI workflow.
    
    Args:
        request: GenerateRequest with user prompt
        
    Returns:
        GenerateResponse with generated tweet data
    """
    try:
        print(f"\n📝 Received prompt: {request.prompt}")
        
        # Run the agent
        final_state = await run_agent(request.prompt)
        
        # Check if generation was successful
        if not final_state.get("is_valid"):
            error_msg = final_state.get("error", "Tweet generation failed")
            return GenerateResponse(
                success=False,
                error=error_msg
            )
        
        # Return the generated tweet data
        return GenerateResponse(
            success=True,
            data={
                "content": final_state.get("tweet_content", ""),
                "hashtags": final_state.get("hashtags", []),
                "final_content": final_state.get("final_content", ""),
                "char_count": final_state.get("char_count", 0),
            }
        )
    
    except Exception as e:
        print(f"❌ Error in generate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/post", response_model=PostResponse)
async def post_tweet(request: PostRequest):
    """
    Post the generated tweet to Twitter.
    
    Args:
        request: PostRequest with tweet content
        
    Returns:
        PostResponse with tweet URL
    """
    try:
        print(f"\n🐦 Posting tweet: {request.content[:50]}...")
        
        # Post to Twitter
        result = await twitter_service.post_tweet(request.content)
        
        # Save to history
        tweet_storage.save_tweet({
            "prompt": request.user_prompt,
            "content": request.content,
            "tweet_url": result.get("url")
        })
        
        print(f"✅ Tweet posted successfully: {result.get('url')}")
        
        return PostResponse(
            success=True,
            tweet_id=result.get("tweet_id"),
            url=result.get("url")
        )
    
    except Exception as e:
        print(f"❌ Error posting tweet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history", response_model=HistoryResponse)
async def get_tweet_history(limit: int = 50):
    """
    Get tweet history from storage.
    
    Args:
        limit: Maximum number of tweets to return
        
    Returns:
        HistoryResponse with list of tweets
    """
    try:
        tweets_data = tweet_storage.get_history(limit)
        
        # Convert to TweetHistoryItem models
        tweets = [TweetHistoryItem(**tweet) for tweet in tweets_data]
        
        return HistoryResponse(
            success=True,
            tweets=tweets
        )
    
    except Exception as e:
        print(f"❌ Error getting history: {str(e)}")
        return HistoryResponse(
            success=False,
            error=str(e),
            tweets=[]
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


