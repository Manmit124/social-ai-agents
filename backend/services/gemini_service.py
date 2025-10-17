import os
import google.generativeai as genai
from typing import List
from prompts.templates import TWEET_GENERATION_PROMPT, HASHTAG_GENERATION_PROMPT


class GeminiService:
    def __init__(self, api_key: str = None):
        """Initialize Gemini service with API key."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_tweet(self, user_prompt: str) -> str:
        """
        Generate tweet content based on user prompt.
        
        Args:
            user_prompt: The user's input prompt
            
        Returns:
            Generated tweet content (without hashtags)
        """
        try:
            prompt = TWEET_GENERATION_PROMPT.format(user_prompt=user_prompt)
            response = self.model.generate_content(prompt)
            
            # Extract text from response
            tweet_content = response.text.strip()
            
            # Ensure it's not too long (max 250 chars to leave room for hashtags)
            if len(tweet_content) > 250:
                tweet_content = tweet_content[:247] + "..."
            
            return tweet_content
        
        except Exception as e:
            print(f"Error generating tweet: {str(e)}")
            raise Exception(f"Failed to generate tweet: {str(e)}")
    
    async def generate_hashtags(self, tweet_content: str) -> List[str]:
        """
        Generate relevant hashtags for the tweet content.
        
        Args:
            tweet_content: The generated tweet content
            
        Returns:
            List of hashtags (e.g., ['#AI', '#Tech'])
        """
        try:
            prompt = HASHTAG_GENERATION_PROMPT.format(tweet_content=tweet_content)
            response = self.model.generate_content(prompt)
            
            # Extract hashtags from response
            hashtags_text = response.text.strip()
            
            # Parse hashtags
            hashtags = []
            for word in hashtags_text.split():
                if word.startswith('#'):
                    hashtags.append(word)
            
            # Return max 3 hashtags
            return hashtags[:3]
        
        except Exception as e:
            print(f"Error generating hashtags: {str(e)}")
            # Return empty list if hashtag generation fails
            return []


