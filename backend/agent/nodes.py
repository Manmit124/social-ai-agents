from .state import AgentState
from .tools import validate_tweet_length, combine_content_and_hashtags, get_char_count
from services.gemini_service import GeminiService
from services.rag_context_builder import get_rag_context_builder
import os


# Initialize services lazily
_gemini_service = None
_rag_context_builder = None

def get_gemini_service():
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service

def get_rag_builder():
    global _rag_context_builder
    if _rag_context_builder is None:
        _rag_context_builder = get_rag_context_builder()
    return _rag_context_builder


async def plan_node(state: AgentState) -> AgentState:
    """
    Planning node - analyzes the user prompt and fetches RAG context.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with RAG context
    """
    print("🤔 Planning: Analyzing user prompt...")
    
    state["step"] = "planning"
    state["error"] = None
    
    # Basic validation
    if not state.get("user_prompt") or len(state["user_prompt"].strip()) == 0:
        state["error"] = "User prompt is empty"
        state["is_valid"] = False
        return state
    
    # Fetch RAG context if user_id is provided
    user_id = state.get("user_id")
    if user_id:
        try:
            print("🔍 Fetching relevant context from your work...")
            rag_builder = get_rag_builder()
            context_text = await rag_builder.get_context_for_tweet_generation(
                user_id,
                state["user_prompt"]
            )
            state["rag_context"] = context_text
            if context_text:
                print(f"✅ Found relevant context ({len(context_text)} chars)")
            else:
                print("ℹ️  No additional context found")
        except Exception as e:
            print(f"⚠️  Warning: Could not fetch RAG context: {str(e)}")
            state["rag_context"] = ""
    else:
        state["rag_context"] = ""
    
    state["is_valid"] = True
    return state


async def generate_node(state: AgentState) -> AgentState:
    """
    Generation node - calls Gemini to generate content with RAG context.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated content
    """
    platform = state.get("platform", "twitter")
    print(f"✍️  Generating: Creating {platform} content...")
    
    state["step"] = "generating"
    
    try:
        # Build enhanced prompt with RAG context
        user_prompt = state["user_prompt"]
        rag_context = state.get("rag_context", "")
        
        gemini_service = get_gemini_service()
        
        # If we have RAG context, enhance the prompt and use raw mode
        if rag_context:
            # Build platform-specific requirements
            if platform == "twitter":
                requirements = """Twitter Requirements:
- Maximum 250 characters (leave room for hashtags)
- Casual, conversational tone
- Use emojis sparingly
- Make it shareable and authentic"""
            elif platform == "linkedin":
                requirements = """LinkedIn Requirements:
- Professional yet conversational
- Maximum 1300 characters
- Focus on insights and value
- Use paragraphs for readability"""
            else:
                requirements = """Requirements:
- Authentic and conversational
- Provide value
- Be genuine"""
            
            enhanced_prompt = f"""{rag_context}

USER REQUEST: {user_prompt}

{requirements}

IMPORTANT: Generate content based on the SPECIFIC commits shown above. You MUST:
1. Reference actual commit messages (e.g., "upgraded to google-genai 1.0.0", "refactored GeminiService")
2. Mention specific version numbers, technologies, or features from the commits
3. Talk about actual problems solved or features built (not generic "building" or "working on")
4. Use the exact repository names and technical details shown above
5. Make it sound like you're sharing what you ACTUALLY did, not what you're "diving into"

DO NOT use generic phrases like "been diving deep" or "building AI agents". Instead, say what you ACTUALLY built based on the commits above."""
            
            print(f"   📊 Using RAG context ({len(rag_context)} chars)")
            tweet_content = await gemini_service.generate_tweet(enhanced_prompt, platform, use_raw_prompt=True)
        else:
            # No RAG context, use standard template
            print(f"   ℹ️  No RAG context available, using standard template")
            tweet_content = await gemini_service.generate_tweet(user_prompt, platform, use_raw_prompt=False)
        
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
    platform = state.get("platform", "twitter")
    print("🏷️  Hashtags: Generating relevant hashtags...")
    
    state["step"] = "hashtags"
    
    try:
        # Generate hashtags using Gemini with platform-specific prompts
        gemini_service = get_gemini_service()
        hashtags = await gemini_service.generate_hashtags(state["tweet_content"], platform)
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

