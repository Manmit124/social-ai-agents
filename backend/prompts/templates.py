TWEET_GENERATION_PROMPT = """You are an expert social media content creator specializing in Twitter/X.

Task: Create an engaging tweet based on the user's prompt.

Requirements:
- Maximum 250 characters (to leave room for hashtags)
- Engaging and conversational tone
- Clear and concise
- Include relevant emojis if appropriate
- Do not include hashtags (will be added separately)

User Prompt: {user_prompt}

Generate only the tweet content, nothing else.
"""


HASHTAG_GENERATION_PROMPT = """Based on this tweet content, suggest 2-3 relevant and popular hashtags.

Tweet: {tweet_content}

Return only hashtags separated by spaces, like: #AI #Tech #Innovation

Do not include any other text, just the hashtags.
"""


# Platform-specific prompts
PLATFORM_PROMPTS = {
    "twitter": {
        "generation": """You are an expert social media content creator specializing in Twitter/X.

Task: Create an engaging tweet based on the user's prompt.

Twitter-specific requirements:
- Maximum 250 characters (to leave room for hashtags)
- Casual, conversational tone
- Short, punchy sentences
- No hashtags (they will be added separately)
- Use emojis sparingly but effectively
- Start with a hook to grab attention
- Make it shareable and quotable

User Prompt: {user_prompt}

Generate only the tweet content, nothing else.
""",
        "hashtags": """Based on this tweet, suggest 2-3 relevant Twitter hashtags.

Tweet: {content}

Return only hashtags separated by spaces, like: #AI #Tech #Innovation

Do not include any other text, just the hashtags.
"""
    },
    "linkedin": {
        "generation": """You are a professional content creator specializing in LinkedIn.

Task: Create engaging LinkedIn post content based on the user's prompt.

LinkedIn-specific requirements:
- Maximum 1300 characters (LinkedIn's first-view limit)
- Professional yet conversational tone
- Use paragraphs and line breaks for readability
- Include a strong opening hook
- Add value through insights or tips
- No hashtags in main content (they will be added separately)
- Can be longer and more detailed than Twitter
- Focus on professional growth, industry insights, or thought leadership

User Prompt: {user_prompt}

Generate only the post content, nothing else.
""",
        "hashtags": """Based on this LinkedIn post, suggest 3-5 relevant professional hashtags.

Post: {content}

Return only hashtags separated by spaces, like: #Leadership #BusinessStrategy #Innovation

Do not include any other text, just the hashtags.
"""
    },
    "reddit": {
        "generation": """You are a content creator specializing in Reddit posts.

Task: Create a Reddit post based on the user's prompt.

Reddit-specific requirements:
- Authentic and conversational tone
- No hashtags (Reddit doesn't use them)
- Be genuine and avoid marketing speak
- Provide value or start a discussion
- Can be detailed and informative
- Respect Reddit's culture of authenticity

User Prompt: {user_prompt}

Generate only the post content, nothing else.
""",
        "hashtags": """Reddit doesn't use hashtags. Return an empty string.
"""
    }
}


def get_platform_prompt(platform: str, prompt_type: str, **kwargs) -> str:
    """
    Get platform-specific prompt.
    
    Args:
        platform: Platform name (twitter, linkedin, reddit)
        prompt_type: Type of prompt (generation, hashtags)
        **kwargs: Variables to format into the prompt
        
    Returns:
        Formatted prompt string
    """
    platform = platform.lower()
    
    if platform not in PLATFORM_PROMPTS:
        platform = "twitter"  # Default to Twitter
    
    prompt_template = PLATFORM_PROMPTS[platform].get(prompt_type, "")
    
    if not prompt_template:
        # Fallback to default prompts
        if prompt_type == "generation":
            prompt_template = TWEET_GENERATION_PROMPT
        elif prompt_type == "hashtags":
            prompt_template = HASHTAG_GENERATION_PROMPT
    
    return prompt_template.format(**kwargs)


