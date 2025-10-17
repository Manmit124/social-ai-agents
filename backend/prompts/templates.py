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


