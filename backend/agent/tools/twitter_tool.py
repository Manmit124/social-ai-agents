"""
Twitter-specific tools and utilities for content generation
"""

from typing import Dict, Any


# Twitter-specific constraints
TWITTER_MAX_LENGTH = 280
TWITTER_HASHTAG_LIMIT = 5


def get_twitter_constraints() -> Dict[str, Any]:
    """
    Get Twitter-specific content constraints.
    
    Returns:
        Dictionary with Twitter constraints
    """
    return {
        "max_length": TWITTER_MAX_LENGTH,
        "hashtag_limit": TWITTER_HASHTAG_LIMIT,
        "tone": "casual and engaging",
        "style": "concise and punchy",
        "best_practices": [
            "Keep it under 280 characters",
            "Use 2-3 relevant hashtags maximum",
            "Start with a hook to grab attention",
            "Use emojis sparingly but effectively",
            "Ask questions to encourage engagement",
            "Keep sentences short and impactful"
        ]
    }


def get_twitter_prompt_context() -> str:
    """
    Get Twitter-specific prompt context for content generation.
    
    Returns:
        Context string to add to prompts
    """
    return """
You are creating content specifically for Twitter. Follow these guidelines:
- Maximum 280 characters (including spaces and hashtags)
- Casual, conversational tone
- Short, punchy sentences
- Use 2-3 relevant hashtags maximum
- Emojis are welcome but don't overuse
- Focus on engagement and virality
- Start with a strong hook
- Make it shareable and quotable
"""


def validate_twitter_content(content: str) -> tuple[bool, str]:
    """
    Validate content for Twitter-specific requirements.
    
    Args:
        content: The content to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not content:
        return False, "Content is empty"
    
    if len(content) > TWITTER_MAX_LENGTH:
        return False, f"Content exceeds {TWITTER_MAX_LENGTH} characters (current: {len(content)})"
    
    # Count hashtags
    hashtag_count = content.count('#')
    if hashtag_count > TWITTER_HASHTAG_LIMIT:
        return False, f"Too many hashtags ({hashtag_count}). Maximum is {TWITTER_HASHTAG_LIMIT}"
    
    return True, ""


def optimize_twitter_content(content: str, hashtags: list[str]) -> str:
    """
    Optimize content for Twitter by combining content and hashtags.
    
    Args:
        content: Main content
        hashtags: List of hashtags
        
    Returns:
        Optimized Twitter content
    """
    # Limit hashtags
    limited_hashtags = hashtags[:TWITTER_HASHTAG_LIMIT]
    
    # Combine content and hashtags
    if limited_hashtags:
        hashtag_string = " ".join(f"#{tag.strip('#')}" for tag in limited_hashtags)
        combined = f"{content}\n\n{hashtag_string}"
    else:
        combined = content
    
    # Ensure it fits within Twitter's limit
    if len(combined) > TWITTER_MAX_LENGTH:
        # Try with fewer hashtags
        if limited_hashtags:
            # Remove hashtags one by one until it fits
            while limited_hashtags and len(combined) > TWITTER_MAX_LENGTH:
                limited_hashtags.pop()
                if limited_hashtags:
                    hashtag_string = " ".join(f"#{tag.strip('#')}" for tag in limited_hashtags)
                    combined = f"{content}\n\n{hashtag_string}"
                else:
                    combined = content
        
        # If still too long, truncate content
        if len(combined) > TWITTER_MAX_LENGTH:
            available_length = TWITTER_MAX_LENGTH - 3  # Reserve 3 chars for "..."
            combined = content[:available_length] + "..."
    
    return combined

