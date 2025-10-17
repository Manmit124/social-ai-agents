from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)


class GenerateResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


class PostRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=280)
    user_prompt: str


class PostResponse(BaseModel):
    success: bool
    tweet_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None


class TweetHistoryItem(BaseModel):
    id: str
    prompt: str
    content: str
    posted_at: str
    tweet_url: Optional[str] = None


class HistoryResponse(BaseModel):
    success: bool
    tweets: List[TweetHistoryItem] = []
    error: Optional[str] = None


