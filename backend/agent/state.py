from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    """State schema for the tweet generation agent."""
    user_prompt: str                # Original user input
    platform: str                   # Target platform (twitter, linkedin, reddit)
    tweet_content: str              # Generated tweet content
    hashtags: List[str]             # Suggested hashtags
    final_content: str              # Tweet + hashtags combined
    char_count: int                 # Character count
    is_valid: bool                  # Validation status
    error: Optional[str]            # Error message if any
    step: str                       # Current step name


