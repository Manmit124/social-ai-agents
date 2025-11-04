"""Twitter Analysis Service - Analyze tweet style and patterns."""

import re
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter
from services.supabase_service import supabase_service
from services.twitter_data_service import twitter_data_service


class TwitterAnalysisService:
    """Service for analyzing Twitter data and generating style profiles."""
    
    def __init__(self):
        self.supabase = supabase_service.client
        
        # Common stop words to exclude from topic extraction
        self.stop_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
            'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
            'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
            'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
            'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
            'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
            'were', 'said', 'did', 'having', 'may', 'should', 'am', 'being', 'does'
        }
    
    def analyze_tweet_length(self, tweets: List[Dict]) -> Dict:
        """
        Calculate average tweet length statistics.
        
        Args:
            tweets: List of tweet objects
            
        Returns:
            dict: Length statistics with average, min, max
        """
        if not tweets:
            return {"average": 0, "min": 0, "max": 0}
        
        lengths = [len(tweet.get("tweet_text", "")) for tweet in tweets]
        
        return {
            "average": round(sum(lengths) / len(lengths)),
            "min": min(lengths),
            "max": max(lengths)
        }
    
    def analyze_tone(self, tweets: List[Dict]) -> str:
        """
        Detect writing tone based on language patterns.
        
        Args:
            tweets: List of tweet objects
            
        Returns:
            str: Detected tone (e.g., "casual_professional", "enthusiastic")
        """
        if not tweets:
            return "neutral"
        
        # Count various indicators
        exclamation_count = 0
        question_count = 0
        technical_terms = 0
        casual_words = 0
        
        # Technical keywords
        tech_keywords = {
            'api', 'code', 'dev', 'developer', 'programming', 'software', 'data',
            'algorithm', 'function', 'debug', 'deploy', 'build', 'test', 'framework',
            'library', 'database', 'server', 'client', 'backend', 'frontend', 'ai',
            'ml', 'machine learning', 'neural', 'model', 'python', 'javascript',
            'typescript', 'react', 'node', 'docker', 'kubernetes', 'aws', 'cloud'
        }
        
        # Casual keywords
        casual_keywords = {
            'lol', 'omg', 'wow', 'hey', 'yeah', 'nope', 'yep', 'gonna', 'wanna',
            'gotta', 'kinda', 'sorta', 'cool', 'awesome', 'amazing', 'love', 'hate',
            'tbh', 'imo', 'btw', 'rn', 'fr', 'ngl'
        }
        
        for tweet in tweets:
            text = tweet.get("tweet_text", "").lower()
            
            # Count punctuation
            exclamation_count += text.count('!')
            question_count += text.count('?')
            
            # Check for technical terms
            for term in tech_keywords:
                if term in text:
                    technical_terms += 1
            
            # Check for casual words
            for word in casual_keywords:
                if word in text:
                    casual_words += 1
        
        # Calculate ratios
        total_tweets = len(tweets)
        exclamation_ratio = exclamation_count / total_tweets
        question_ratio = question_count / total_tweets
        technical_ratio = technical_terms / total_tweets
        casual_ratio = casual_words / total_tweets
        
        # Determine tone
        if exclamation_ratio > 1.5:
            return "enthusiastic"
        elif technical_ratio > 0.5 and casual_ratio < 0.2:
            return "professional"
        elif technical_ratio > 0.3 and casual_ratio > 0.2:
            return "casual_professional"
        elif casual_ratio > 0.5:
            return "casual"
        elif question_ratio > 0.5:
            return "curious"
        else:
            return "informative"
    
    def analyze_emoji_usage(self, tweets: List[Dict]) -> Dict:
        """
        Analyze emoji usage patterns.
        
        Args:
            tweets: List of tweet objects
            
        Returns:
            dict: Emoji usage statistics
        """
        if not tweets:
            return {
                "uses_emojis": False,
                "percentage": 0,
                "common": []
            }
        
        # Emoji regex pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\U0001FA00-\U0001FA6F"  # extended symbols
            "]+",
            flags=re.UNICODE
        )
        
        tweets_with_emojis = 0
        all_emojis = []
        
        for tweet in tweets:
            text = tweet.get("tweet_text", "")
            emojis = emoji_pattern.findall(text)
            
            if emojis:
                tweets_with_emojis += 1
                # Split multi-emoji strings into individual emojis
                for emoji_str in emojis:
                    all_emojis.extend(list(emoji_str))
        
        percentage = round((tweets_with_emojis / len(tweets)) * 100) if tweets else 0
        
        # Get most common emojis (top 5)
        emoji_counter = Counter(all_emojis)
        common_emojis = [emoji for emoji, count in emoji_counter.most_common(5)]
        
        return {
            "uses_emojis": tweets_with_emojis > 0,
            "percentage": percentage,
            "common": common_emojis
        }
    
    def extract_topics(self, tweets: List[Dict]) -> List[str]:
        """
        Identify common topics from tweets.
        
        Args:
            tweets: List of tweet objects
            
        Returns:
            list: List of common topics
        """
        if not tweets:
            return []
        
        # Collect all hashtags
        all_hashtags = []
        all_words = []
        
        for tweet in tweets:
            # Get hashtags
            hashtags = tweet.get("hashtags_used", [])
            all_hashtags.extend(hashtags)
            
            # Get words from text (excluding hashtags and mentions)
            text = tweet.get("tweet_text", "")
            # Remove URLs, hashtags, mentions
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            text = re.sub(r'#\w+', '', text)
            text = re.sub(r'@\w+', '', text)
            
            # Extract words
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            # Filter stop words
            words = [w for w in words if w not in self.stop_words]
            all_words.extend(words)
        
        # Count hashtags
        hashtag_counter = Counter(all_hashtags)
        top_hashtags = [tag for tag, count in hashtag_counter.most_common(10)]
        
        # Count words
        word_counter = Counter(all_words)
        top_words = [word for word, count in word_counter.most_common(10)]
        
        # Combine and deduplicate
        topics = []
        
        # Prioritize hashtags as they're explicit topics
        topics.extend(top_hashtags[:5])
        
        # Add top words that aren't already in topics
        for word in top_words:
            if word.lower() not in [t.lower() for t in topics]:
                topics.append(word.capitalize())
            if len(topics) >= 10:
                break
        
        return topics[:10]
    
    def analyze_engagement_patterns(self, tweets: List[Dict]) -> Dict:
        """
        Find what content performs best.
        
        Args:
            tweets: List of tweet objects
            
        Returns:
            dict: Engagement patterns and insights
        """
        if not tweets:
            return {
                "best_topics": [],
                "best_length": 0,
                "best_time": "unknown",
                "avg_engagement": 0
            }
        
        # Calculate engagement for each tweet
        tweet_engagement = []
        for tweet in tweets:
            engagement = (
                tweet.get("likes_count", 0) + 
                tweet.get("retweets_count", 0) + 
                tweet.get("replies_count", 0)
            )
            tweet_engagement.append({
                "tweet": tweet,
                "engagement": engagement,
                "length": len(tweet.get("tweet_text", "")),
                "hashtags": tweet.get("hashtags_used", []),
                "posted_at": tweet.get("posted_at", "")
            })
        
        # Sort by engagement
        tweet_engagement.sort(key=lambda x: x["engagement"], reverse=True)
        
        # Get top 10 performing tweets
        top_tweets = tweet_engagement[:min(10, len(tweet_engagement))]
        
        if not top_tweets:
            return {
                "best_topics": [],
                "best_length": 0,
                "best_time": "unknown",
                "avg_engagement": 0
            }
        
        # Analyze top tweets
        top_hashtags = []
        top_lengths = []
        top_hours = []
        
        for item in top_tweets:
            top_hashtags.extend(item["hashtags"])
            top_lengths.append(item["length"])
            
            # Extract hour from posted_at
            posted_at = item["posted_at"]
            if posted_at:
                try:
                    if isinstance(posted_at, str):
                        dt = datetime.fromisoformat(posted_at.replace('Z', '+00:00'))
                    else:
                        dt = posted_at
                    top_hours.append(dt.hour)
                except:
                    pass
        
        # Find most common hashtags in top tweets
        hashtag_counter = Counter(top_hashtags)
        best_topics = [tag for tag, count in hashtag_counter.most_common(5)]
        
        # Calculate average length of top tweets
        best_length = round(sum(top_lengths) / len(top_lengths)) if top_lengths else 0
        
        # Find most common posting hour
        if top_hours:
            hour_counter = Counter(top_hours)
            best_hour = hour_counter.most_common(1)[0][0]
            # Convert to readable time
            if best_hour < 12:
                best_time = f"{best_hour}am"
            elif best_hour == 12:
                best_time = "12pm"
            else:
                best_time = f"{best_hour - 12}pm"
        else:
            best_time = "unknown"
        
        # Calculate average engagement
        avg_engagement = round(sum(item["engagement"] for item in tweet_engagement) / len(tweet_engagement))
        
        return {
            "best_topics": best_topics,
            "best_length": best_length,
            "best_time": best_time,
            "avg_engagement": avg_engagement,
            "top_performing_tweets": [
                {
                    "text": item["tweet"]["tweet_text"][:100] + "..." if len(item["tweet"]["tweet_text"]) > 100 else item["tweet"]["tweet_text"],
                    "engagement": item["engagement"],
                    "likes": item["tweet"].get("likes_count", 0),
                    "retweets": item["tweet"].get("retweets_count", 0)
                }
                for item in top_tweets[:5]
            ]
        }
    
    async def generate_style_profile(self, user_id: str) -> Dict:
        """
        Generate complete style profile for a user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Complete style profile
        """
        try:
            print(f"\n📊 Generating style profile for user {user_id}...")
            
            # Get user's tweets from database
            tweets = await twitter_data_service.get_user_tweets_from_db(user_id, limit=200)
            
            if not tweets:
                print("⚠️  No tweets found for analysis")
                return {
                    "error": "No tweets available for analysis",
                    "user_id": user_id
                }
            
            print(f"   Analyzing {len(tweets)} tweets...")
            
            # Run all analyses
            length_stats = self.analyze_tweet_length(tweets)
            tone = self.analyze_tone(tweets)
            emoji_stats = self.analyze_emoji_usage(tweets)
            topics = self.extract_topics(tweets)
            engagement_patterns = self.analyze_engagement_patterns(tweets)
            
            # Create profile object
            profile = {
                "user_id": user_id,
                "average_length": length_stats["average"],
                "min_length": length_stats["min"],
                "max_length": length_stats["max"],
                "tone": tone,
                "uses_emojis": emoji_stats["uses_emojis"],
                "emoji_percentage": emoji_stats["percentage"],
                "common_emojis": emoji_stats["common"],
                "common_hashtags": topics[:5],  # Top 5 as hashtags
                "preferred_topics": topics,
                "best_performing_content": engagement_patterns,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Save to database
            print("   💾 Saving style profile to database...")
            
            # Check if profile exists
            existing = self.supabase.table("twitter_style_profile")\
                .select("id")\
                .eq("user_id", user_id)\
                .execute()
            
            if existing.data:
                # Update existing profile
                response = self.supabase.table("twitter_style_profile")\
                    .update(profile)\
                    .eq("user_id", user_id)\
                    .execute()
            else:
                # Insert new profile
                response = self.supabase.table("twitter_style_profile")\
                    .insert(profile)\
                    .execute()
            
            print(f"✅ Style profile generated successfully!")
            print(f"   - Tone: {tone}")
            print(f"   - Avg length: {length_stats['average']} chars")
            print(f"   - Uses emojis: {emoji_stats['percentage']}%")
            print(f"   - Top topics: {', '.join(topics[:3])}")
            
            return profile
            
        except Exception as e:
            print(f"❌ Error generating style profile: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    async def get_style_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get existing style profile for a user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Style profile or None
        """
        try:
            response = self.supabase.table("twitter_style_profile")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error getting style profile: {e}")
            return None


# Create singleton instance
twitter_analysis_service = TwitterAnalysisService()

