import json
import os
from typing import List, Dict
from datetime import datetime
import uuid


class TweetStorage:
    def __init__(self, file_path: str = "data/tweets_history.json"):
        """Initialize tweet storage with JSON file."""
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the data directory and file if they don't exist."""
        # Create directory if it doesn't exist
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create file with empty array if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def save_tweet(self, tweet_data: Dict) -> None:
        """
        Save a tweet to the history file.
        
        Args:
            tweet_data: Dictionary containing tweet information
                - prompt: User's original prompt
                - content: Generated tweet content
                - tweet_url: URL of posted tweet (optional)
        """
        try:
            # Read existing tweets
            tweets = self._read_tweets()
            
            # Create new tweet entry
            new_tweet = {
                "id": str(uuid.uuid4()),
                "prompt": tweet_data.get("prompt", ""),
                "content": tweet_data.get("content", ""),
                "posted_at": datetime.utcnow().isoformat() + "Z",
                "tweet_url": tweet_data.get("tweet_url")
            }
            
            # Add to beginning of list (newest first)
            tweets.insert(0, new_tweet)
            
            # Write back to file
            self._write_tweets(tweets)
        
        except Exception as e:
            print(f"Error saving tweet: {str(e)}")
            raise Exception(f"Failed to save tweet: {str(e)}")
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """
        Get tweet history.
        
        Args:
            limit: Maximum number of tweets to return
            
        Returns:
            List of tweet dictionaries
        """
        try:
            tweets = self._read_tweets()
            return tweets[:limit]
        
        except Exception as e:
            print(f"Error getting history: {str(e)}")
            return []
    
    def _read_tweets(self) -> List[Dict]:
        """Read tweets from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # If file is corrupted, return empty list
            return []
        except Exception as e:
            print(f"Error reading tweets: {str(e)}")
            return []
    
    def _write_tweets(self, tweets: List[Dict]) -> None:
        """Write tweets to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(tweets, f, indent=2)


