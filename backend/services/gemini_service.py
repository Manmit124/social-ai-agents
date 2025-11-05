import os
import asyncio
from google import genai
from typing import List
from prompts.templates import TWEET_GENERATION_PROMPT, HASHTAG_GENERATION_PROMPT, get_platform_prompt


class GeminiService:
    def __init__(self, api_key: str = None):
        """Initialize Gemini service with API key."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize the new Gemini client
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash-lite"
    
    async def generate_tweet(self, user_prompt: str, platform: str = "twitter", use_raw_prompt: bool = False) -> str:
        """
        Generate content based on user prompt and platform.
        
        Args:
            user_prompt: The user's input prompt (may include RAG context)
            platform: Target platform (twitter, linkedin, reddit)
            use_raw_prompt: If True, use prompt as-is (for RAG-enhanced prompts)
            
        Returns:
            Generated content (without hashtags)
        """
        try:
            # If using raw prompt (RAG-enhanced), use it directly
            # Otherwise, wrap in platform-specific template
            if use_raw_prompt:
                prompt = user_prompt
            else:
                # Use platform-specific prompt template
                prompt = get_platform_prompt(platform, "generation", user_prompt=user_prompt)
            
            # Run sync operation in thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
            )
            
            # Extract text from response
            content = response.text.strip()
            
            # Platform-specific length limits
            max_length = 250 if platform == "twitter" else 1300 if platform == "linkedin" else 10000
            
            # Ensure it's not too long
            if len(content) > max_length:
                content = content[:max_length - 3] + "..."
            
            return content
        
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            raise Exception(f"Failed to generate content: {str(e)}")
    
    async def generate_hashtags(self, content: str, platform: str = "twitter") -> List[str]:
        """
        Generate relevant hashtags for the content.
        
        Args:
            content: The generated content
            platform: Target platform (twitter, linkedin, reddit)
            
        Returns:
            List of hashtags (e.g., ['#AI', '#Tech'])
        """
        try:
            # Reddit doesn't use hashtags
            if platform == "reddit":
                return []
            
            # Use platform-specific prompt
            prompt = get_platform_prompt(platform, "hashtags", content=content)
            
            # Run sync operation in thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
            )
            
            # Extract hashtags from response
            hashtags_text = response.text.strip()
            
            # Parse hashtags
            hashtags = []
            for word in hashtags_text.split():
                if word.startswith('#'):
                    hashtags.append(word)
            
            # Platform-specific hashtag limits
            max_hashtags = 3 if platform == "twitter" else 5
            
            # Return limited hashtags
            return hashtags[:max_hashtags]
        
        except Exception as e:
            print(f"Error generating hashtags: {str(e)}")
            # Return empty list if hashtag generation fails
            return []
