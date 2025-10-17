from .state import AgentState
from .tools import validate_tweet_length, combine_content_and_hashtags, get_char_count
from services.gemini_service import GeminiService
import os


# Initialize Gemini service lazily
_gemini_service = None

def get_gemini_service():
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service


async def plan_node(state: AgentState) -> AgentState:
    """
    Planning node - analyzes the user prompt.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    print("🤔 Planning: Analyzing user prompt...")
    
    state["step"] = "planning"
    state["error"] = None
    
    # Basic validation
    if not state.get("user_prompt") or len(state["user_prompt"].strip()) == 0:
        state["error"] = "User prompt is empty"
        state["is_valid"] = False
        return state
    
    state["is_valid"] = True
    return state


async def generate_node(state: AgentState) -> AgentState:
    """
    Generation node - calls Gemini to generate tweet content.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated content
    """
    print("✍️  Generating: Creating tweet content...")
    
    state["step"] = "generating"
    
    try:
        # Generate tweet content using Gemini
        gemini_service = get_gemini_service()
        tweet_content = await gemini_service.generate_tweet(state["user_prompt"])
        state["tweet_content"] = tweet_content
        state["is_valid"] = True
        
    except Exception as e:
        state["error"] = f"Generation failed: {str(e)}"
        state["is_valid"] = False
    
    return state


async def validate_node(state: AgentState) -> AgentState:
    """
    Validation node - checks if generated content is valid.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with validation result
    """
    print("✅ Validating: Checking tweet quality...")
    
    state["step"] = "validating"
    
    # Validate tweet length
    is_valid = validate_tweet_length(state.get("tweet_content", ""))
    state["is_valid"] = is_valid
    
    if not is_valid:
        state["error"] = "Tweet content is invalid or too long"
    
    return state


async def hashtag_node(state: AgentState) -> AgentState:
    """
    Hashtag node - generates relevant hashtags.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with hashtags
    """
    print("🏷️  Hashtags: Generating relevant hashtags...")
    
    state["step"] = "hashtags"
    
    try:
        # Generate hashtags using Gemini
        gemini_service = get_gemini_service()
        hashtags = await gemini_service.generate_hashtags(state["tweet_content"])
        state["hashtags"] = hashtags
        
    except Exception as e:
        print(f"Hashtag generation failed: {str(e)}")
        # Continue without hashtags
        state["hashtags"] = []
    
    return state


async def finalize_node(state: AgentState) -> AgentState:
    """
    Finalization node - combines content with hashtags.
    
    Args:
        state: Current agent state
        
    Returns:
        Final state with combined content
    """
    print("🎯 Finalizing: Preparing final tweet...")
    
    state["step"] = "finalizing"
    
    # Combine content with hashtags
    final_content = combine_content_and_hashtags(
        state["tweet_content"],
        state.get("hashtags", [])
    )
    
    state["final_content"] = final_content
    state["char_count"] = get_char_count(final_content)
    
    # Final validation
    state["is_valid"] = validate_tweet_length(final_content)
    
    if not state["is_valid"]:
        state["error"] = "Final content exceeds character limit"
    
    print(f"✨ Done! Character count: {state['char_count']}/280")
    
    return state

