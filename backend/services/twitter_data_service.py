"""Twitter Data Service - Handle storing and retrieving Twitter data."""

import re
from typing import Dict, List, Optional
from datetime import datetime
from services.supabase_service import supabase_service


class TwitterDataService:
    """Service for managing Twitter data in Supabase."""
    
    def __init__(self):
        self.supabase = supabase_service.client
    
    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from tweet text.
        
        Args:
            text: Tweet text
            
        Returns:
            list: List of hashtags (without # symbol)
        """
        hashtags = re.findall(r'#(\w+)', text)
        return list(set(hashtags))  # Remove duplicates
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract @mentions from tweet text.
        
        Args:
            text: Tweet text
            
        Returns:
            list: List of mentions (without @ symbol)
        """
        mentions = re.findall(r'@(\w+)', text)
        return list(set(mentions))  # Remove duplicates
    
    async def save_twitter_tweets(
        self, 
        user_id: str, 
        tweets_data: List[Dict]
    ) -> Dict:
        """
        Save tweets to database.
        
        Args:
            user_id: User's UUID
            tweets_data: List of tweet objects from Twitter API
            
        Returns:
            dict: Summary with counts of new/existing tweets
        """
        new_tweets_count = 0
        existing_tweets_count = 0
        errors = []
        
        for tweet in tweets_data:
            try:
                tweet_id = tweet.get("id")
                tweet_text = tweet.get("text", "")
                created_at = tweet.get("created_at")
                
                # Get public metrics
                metrics = tweet.get("public_metrics", {})
                likes_count = metrics.get("like_count", 0)
                retweets_count = metrics.get("retweet_count", 0)
                replies_count = metrics.get("reply_count", 0)
                
                # Extract hashtags and mentions
                hashtags = self.extract_hashtags(tweet_text)
                mentions = self.extract_mentions(tweet_text)
                
                # Check if tweet already exists
                existing = self.supabase.table("twitter_activity")\
                    .select("id")\
                    .eq("tweet_id", tweet_id)\
                    .execute()
                
                if existing.data:
                    existing_tweets_count += 1
                    continue
                
                # Insert new tweet
                tweet_record = {
                    "user_id": user_id,
                    "tweet_id": tweet_id,
                    "tweet_text": tweet_text,
                    "posted_at": created_at,
                    "likes_count": likes_count,
                    "retweets_count": retweets_count,
                    "replies_count": replies_count,
                    "hashtags_used": hashtags,
                    "mentions_used": mentions,
                    "raw_data": tweet,
                    "collected_at": datetime.utcnow().isoformat()
                }
                
                self.supabase.table("twitter_activity")\
                    .insert(tweet_record)\
                    .execute()
                
                new_tweets_count += 1
                
            except Exception as e:
                errors.append(f"Error saving tweet {tweet.get('id')}: {str(e)}")
                print(f"❌ Error saving tweet: {e}")
        
        return {
            "new_tweets": new_tweets_count,
            "existing_tweets": existing_tweets_count,
            "total_processed": len(tweets_data),
            "errors": errors
        }
    
    async def get_user_tweets_from_db(
        self, 
        user_id: str, 
        limit: int = 100
    ) -> List[Dict]:
        """
        Get stored tweets from database.
        
        Args:
            user_id: User's UUID
            limit: Maximum number of tweets to retrieve
            
        Returns:
            list: List of tweet records ordered by posted_at DESC
        """
        try:
            response = self.supabase.table("twitter_activity")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("posted_at", desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error fetching tweets from DB: {e}")
            return []
    
    async def update_twitter_fetch_log(
        self, 
        user_id: str, 
        last_tweet_id: Optional[str], 
        total_count: int,
        fetch_type: str = "manual"
    ) -> Dict:
        """
        Update or create fetch log entry.
        
        Args:
            user_id: User's UUID
            last_tweet_id: ID of the most recent tweet fetched
            total_count: Total number of tweets fetched
            fetch_type: Type of fetch (manual, automatic, etc.)
            
        Returns:
            dict: Updated fetch log record
        """
        try:
            # Check if log exists for user
            existing = self.supabase.table("twitter_data_fetch_log")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
            
            log_data = {
                "user_id": user_id,
                "last_fetch_time": datetime.utcnow().isoformat(),
                "last_tweet_id": last_tweet_id,
                "total_tweets_fetched": total_count,
                "fetch_type": fetch_type,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            if existing.data:
                # Update existing log
                response = self.supabase.table("twitter_data_fetch_log")\
                    .update(log_data)\
                    .eq("user_id", user_id)\
                    .execute()
            else:
                # Create new log
                response = self.supabase.table("twitter_data_fetch_log")\
                    .insert(log_data)\
                    .execute()
            
            return response.data[0] if response.data else {}
            
        except Exception as e:
            print(f"❌ Error updating fetch log: {e}")
            return {}
    
    async def get_fetch_log(self, user_id: str) -> Optional[Dict]:
        """
        Get the latest fetch log for a user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Fetch log record or None
        """
        try:
            response = self.supabase.table("twitter_data_fetch_log")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error getting fetch log: {e}")
            return None
    
    async def get_tweet_stats(self, user_id: str) -> Dict:
        """
        Get statistics about user's stored tweets.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Statistics including total tweets, avg engagement, etc.
        """
        try:
            tweets = await self.get_user_tweets_from_db(user_id, limit=1000)
            
            if not tweets:
                return {
                    "total_tweets": 0,
                    "avg_likes": 0,
                    "avg_retweets": 0,
                    "avg_replies": 0,
                    "total_hashtags": 0,
                    "total_mentions": 0
                }
            
            total_likes = sum(t.get("likes_count", 0) for t in tweets)
            total_retweets = sum(t.get("retweets_count", 0) for t in tweets)
            total_replies = sum(t.get("replies_count", 0) for t in tweets)
            
            all_hashtags = []
            all_mentions = []
            for t in tweets:
                all_hashtags.extend(t.get("hashtags_used", []))
                all_mentions.extend(t.get("mentions_used", []))
            
            return {
                "total_tweets": len(tweets),
                "avg_likes": round(total_likes / len(tweets), 2),
                "avg_retweets": round(total_retweets / len(tweets), 2),
                "avg_replies": round(total_replies / len(tweets), 2),
                "total_hashtags": len(set(all_hashtags)),
                "total_mentions": len(set(all_mentions)),
                "most_recent_tweet": tweets[0].get("posted_at") if tweets else None
            }
        except Exception as e:
            print(f"❌ Error calculating tweet stats: {e}")
            return {}


# Create singleton instance
twitter_data_service = TwitterDataService()

