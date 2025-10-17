from typing import List


def validate_tweet_length(content: str) -> bool:
    """
    Validate that tweet content is within Twitter's character limit.
    
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


def combine_content_and_hashtags(content: str, hashtags: List[str]) -> str:
    """
    Combine tweet content with hashtags.
    
    Args:
        content: Tweet content
        hashtags: List of hashtags
        
    Returns:
        Combined content with hashtags
    """
    if not hashtags:
        return content
    
    # Add hashtags with proper spacing
    hashtags_str = " ".join(hashtags)
    combined = f"{content}\n\n{hashtags_str}"
    
    # Ensure it's within 280 characters
    if len(combined) > 280:
        # Try without newlines
        combined = f"{content} {hashtags_str}"
        
        # If still too long, remove hashtags one by one
        while len(combined) > 280 and hashtags:
            hashtags.pop()
            hashtags_str = " ".join(hashtags)
            combined = f"{content} {hashtags_str}" if hashtags else content
    
    return combined


def get_char_count(content: str) -> int:
    """
    Get character count of content.
    
    Args:
        content: Content to count
        
    Returns:
        Character count
    """
    return len(content)


