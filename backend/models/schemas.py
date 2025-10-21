from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    platform: str = Field(default="twitter", pattern="^(twitter|linkedin|reddit)$")


class GenerateResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


class PostRequest(BaseModel):
    content: str = Field(..., min_length=1)
    user_prompt: str
    platform: str = Field(default="twitter", pattern="^(twitter|linkedin|reddit)$")
    hashtags: Optional[List[str]] = []


class PostResponse(BaseModel):
    success: bool
    post_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None


class PostHistoryItem(BaseModel):
    id: str
    platform: str
    user_prompt: str
    generated_content: str
    hashtags: List[str] = []
    platform_post_id: Optional[str] = None
    platform_post_url: Optional[str] = None
    status: str
    created_at: str


class HistoryResponse(BaseModel):
    success: bool
    posts: List[PostHistoryItem] = []
    error: Optional[str] = None


# Legacy support
class TweetHistoryItem(BaseModel):
    id: str
    prompt: str
    content: str
    posted_at: str
    tweet_url: Optional[str] = None


