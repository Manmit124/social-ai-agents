import os
import tweepy
from typing import Optional, Dict


class TwitterService:
    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None
    ):
        """Initialize Twitter service with API credentials."""
        self.api_key = api_key or os.getenv("TWITTER_API_KEY")
        self.api_secret = api_secret or os.getenv("TWITTER_API_SECRET")
        self.access_token = access_token or os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Twitter API credentials not found in environment variables")
        
        # Initialize Tweepy client (v2 API for free tier)
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
    
    def validate_content(self, content: str) -> bool:
        """
        Validate tweet content meets Twitter requirements.
        
        Args:
            content: Tweet content to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not content or len(content.strip()) == 0:
            return False
        
        if len(content) > 280:
            return False
        
        return True
    
    async def post_tweet(self, content: str) -> Dict[str, str]:
        """
        Post a tweet to Twitter.
        
        Args:
            content: Tweet content to post
            
        Returns:
            Dictionary with tweet_id and url
        """
        try:
            # Validate content first
            if not self.validate_content(content):
                raise ValueError("Invalid tweet content")
            
            # Post tweet using Twitter API v2
            response = self.client.create_tweet(text=content)
            
            tweet_id = response.data['id']
            
            # Get username (we need to fetch this)
            me = self.client.get_me()
            username = me.data.username
            
            tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
            
            return {
                "tweet_id": tweet_id,
                "url": tweet_url
            }
        
        except tweepy.TweepyException as e:
            print(f"Twitter API error: {str(e)}")
            raise Exception(f"Failed to post tweet: {str(e)}")
        
        except Exception as e:
            print(f"Error posting tweet: {str(e)}")
            raise Exception(f"Failed to post tweet: {str(e)}")


