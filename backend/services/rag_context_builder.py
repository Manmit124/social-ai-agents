"""
RAG Context Builder Service - Build rich context for AI content generation.

This service combines:
- Semantic search results (relevant commits)
- User context (projects, tech stack)
- Twitter style profile
- Recent activity

To create comprehensive context for better AI-generated content.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

from .embedding_service import get_embedding_service
from .github_data_service import GitHubDataService
from .context_service import ContextService


class RAGContextBuilder:
    """Service for building RAG context for content generation."""
    
    def __init__(self):
        """Initialize the RAG context builder."""
        self.embedding_service = get_embedding_service()
        self.github_data_service = GitHubDataService()
        self.context_service = ContextService()
    
    async def build_context_for_generation(
        self,
        user_id: str,
        user_prompt: str,
        include_recent: bool = True,
        max_commits: int = 5
    ) -> Dict[str, any]:
        """
        Build complete context for AI content generation using RAG.
        
        This combines semantic search with user context to provide
        the AI with relevant, personalized information.
        
        Args:
            user_id: User's UUID
            user_prompt: User's content generation prompt
            include_recent: Include recent commits even if not semantically similar
            max_commits: Maximum number of commits to include
            
        Returns:
            dict: {
                "relevant_commits": [...],  # Semantically similar commits
                "recent_commits": [...],    # Recent activity (if include_recent)
                "user_context": {...},      # Projects, tech stack, etc.
                "prompt_analysis": {...},   # What the prompt is about
                "formatted_context": str    # Ready-to-use text for AI
            }
        """
        print(f"\n🔍 Building RAG context for prompt: '{user_prompt}'")
        
        context = {
            "relevant_commits": [],
            "recent_commits": [],
            "user_context": {},
            "prompt_analysis": {},
            "formatted_context": ""
        }
        
        try:
            # 1. Semantic Search: Find relevant commits
            print("   📊 Searching for semantically similar commits...")
            relevant_commits = await self._get_relevant_commits(
                user_id,
                user_prompt,
                limit=max_commits
            )
            context["relevant_commits"] = relevant_commits
            print(f"   ✅ Found {len(relevant_commits)} relevant commits")
            
            # 2. Get recent activity (optional)
            if include_recent and len(relevant_commits) < max_commits:
                print("   📅 Getting recent commits...")
                recent_commits = await self._get_recent_commits(
                    user_id,
                    limit=max_commits - len(relevant_commits),
                    exclude_hashes=[c["commit_hash"] for c in relevant_commits]
                )
                context["recent_commits"] = recent_commits
                print(f"   ✅ Found {len(recent_commits)} recent commits")
            
            # 3. Get user context (projects, tech stack)
            print("   👤 Getting user context...")
            user_context = await self.context_service.get_user_context(user_id)
            if user_context:
                context["user_context"] = {
                    "projects": user_context.get("projects", []),
                    "tech_stack": user_context.get("tech_stack", []),
                    "focus_areas": user_context.get("ai_insights", {}).get("focus_areas", []),
                    "key_achievements": user_context.get("ai_insights", {}).get("key_achievements", [])
                }
                print(f"   ✅ Loaded user context")
            
            # 4. Analyze prompt
            context["prompt_analysis"] = self._analyze_prompt(user_prompt)
            
            # 5. Format context for AI
            context["formatted_context"] = self._format_context_for_prompt(context)
            
            print(f"   ✅ RAG context built successfully")
            
            return context
        
        except Exception as e:
            print(f"   ❌ Error building RAG context: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Return minimal context on error
            return {
                "relevant_commits": [],
                "recent_commits": [],
                "user_context": {},
                "prompt_analysis": {},
                "formatted_context": "",
                "error": str(e)
            }
    
    async def _get_relevant_commits(
        self,
        user_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get commits semantically similar to the query.
        
        Args:
            user_id: User's UUID
            query: Search query (user prompt)
            limit: Maximum number of commits
            
        Returns:
            list: Relevant commits with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            # Search for similar commits
            results = await self.github_data_service.search_similar_commits(
                user_id,
                query_embedding,
                limit=limit,
                min_similarity=0.5  # Only include reasonably similar commits
            )
            
            return results
        
        except Exception as e:
            print(f"      ⚠️ Error getting relevant commits: {str(e)}")
            return []
    
    async def _get_recent_commits(
        self,
        user_id: str,
        limit: int = 3,
        exclude_hashes: List[str] = None
    ) -> List[Dict]:
        """
        Get recent commits (last 7 days).
        
        Args:
            user_id: User's UUID
            limit: Maximum number of commits
            exclude_hashes: Commit hashes to exclude (already included)
            
        Returns:
            list: Recent commits
        """
        try:
            exclude_hashes = exclude_hashes or []
            
            # Get recent commits
            commits = await self.github_data_service.get_user_github_activity(
                user_id,
                limit=limit * 2,  # Get more to account for exclusions
                days=7
            )
            
            # Filter out excluded commits
            filtered = [
                c for c in commits 
                if c.get("commit_hash") not in exclude_hashes
            ]
            
            # Add similarity score (0 for recent commits)
            for commit in filtered:
                commit["similarity"] = 0.0
                commit["source"] = "recent"
            
            return filtered[:limit]
        
        except Exception as e:
            print(f"      ⚠️ Error getting recent commits: {str(e)}")
            return []
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, any]:
        """
        Analyze the user prompt to understand intent.
        
        Args:
            prompt: User's content generation prompt
            
        Returns:
            dict: Prompt analysis
        """
        prompt_lower = prompt.lower()
        
        # Detect topics
        topics = []
        if any(word in prompt_lower for word in ["api", "endpoint", "service", "rest"]):
            topics.append("API Development")
        if any(word in prompt_lower for word in ["ml", "machine learning", "ai", "model"]):
            topics.append("Machine Learning")
        if any(word in prompt_lower for word in ["bug", "fix", "issue", "resolved"]):
            topics.append("Bug Fixes")
        if any(word in prompt_lower for word in ["feature", "new", "added", "implemented"]):
            topics.append("New Features")
        if any(word in prompt_lower for word in ["ui", "frontend", "design", "interface"]):
            topics.append("Frontend")
        if any(word in prompt_lower for word in ["backend", "server", "database"]):
            topics.append("Backend")
        
        # Detect intent
        intent = "general"
        if any(word in prompt_lower for word in ["recent", "latest", "today", "this week"]):
            intent = "recent_work"
        elif any(word in prompt_lower for word in ["achievement", "proud", "success"]):
            intent = "showcase"
        elif any(word in prompt_lower for word in ["learning", "learned", "discovered"]):
            intent = "learning"
        
        return {
            "topics": topics,
            "intent": intent,
            "length": len(prompt.split())
        }
    
    def _format_context_for_prompt(self, context: Dict) -> str:
        """
        Format the context as text for AI prompt.
        
        Args:
            context: Context dictionary
            
        Returns:
            str: Formatted context text
        """
        lines = []
        
        # Add relevant commits
        if context["relevant_commits"]:
            lines.append("YOUR ACTUAL WORK (Use these specific details):")
            lines.append("")
            for i, commit in enumerate(context["relevant_commits"][:3], 1):
                similarity = commit.get("similarity", 0)
                repo = commit['repository_name']
                msg = commit['commit_message']
                lines.append(f"Commit {i} ({similarity*100:.0f}% relevant):")
                lines.append(f"  Repository: {repo}")
                lines.append(f"  What you did: {msg}")
                lines.append("")
        
        # Add recent commits
        if context["recent_commits"]:
            lines.append("📅 RECENT ACTIVITY:")
            for i, commit in enumerate(context["recent_commits"][:2], 1):
                date = commit.get("commit_date", "")
                if date:
                    try:
                        date_obj = datetime.fromisoformat(date.replace("Z", "+00:00"))
                        date_str = date_obj.strftime("%b %d")
                    except:
                        date_str = "Recently"
                else:
                    date_str = "Recently"
                
                lines.append(
                    f"{i}. [{commit['repository_name']}] {commit['commit_message']} ({date_str})"
                )
            lines.append("")
        
        # Add user context
        user_ctx = context.get("user_context", {})
        if user_ctx:
            # Projects
            if user_ctx.get("projects"):
                projects = user_ctx["projects"][:3]
                lines.append(f"💼 ACTIVE PROJECTS: {', '.join(projects)}")
            
            # Tech stack
            if user_ctx.get("tech_stack"):
                tech = user_ctx["tech_stack"][:5]
                lines.append(f"🛠️  TECH STACK: {', '.join(tech)}")
            
            # Focus areas
            if user_ctx.get("focus_areas"):
                focus = user_ctx["focus_areas"][:2]
                lines.append(f"🎯 FOCUS AREAS: {', '.join(focus)}")
            
            if any([user_ctx.get("projects"), user_ctx.get("tech_stack"), user_ctx.get("focus_areas")]):
                lines.append("")
        
        return "\n".join(lines)
    
    async def get_context_for_tweet_generation(
        self,
        user_id: str,
        user_prompt: str
    ) -> str:
        """
        Get formatted context specifically for tweet generation.
        
        This is a simplified version that returns just the formatted text.
        
        Args:
            user_id: User's UUID
            user_prompt: User's content generation prompt
            
        Returns:
            str: Formatted context text ready for AI prompt
        """
        context = await self.build_context_for_generation(
            user_id,
            user_prompt,
            include_recent=True,
            max_commits=5
        )
        
        return context.get("formatted_context", "")
    
    async def get_relevant_commits_for_topic(
        self,
        user_id: str,
        topic: str,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get commits relevant to a specific topic.
        
        Args:
            user_id: User's UUID
            topic: Topic to search for (e.g., "API", "ML", "bug fixes")
            limit: Maximum number of commits
            
        Returns:
            list: Relevant commits
        """
        # Expand topic into a more detailed query
        topic_queries = {
            "api": "API endpoints and services development",
            "ml": "machine learning and AI models",
            "bug": "bug fixes and issue resolution",
            "feature": "new features and functionality",
            "ui": "user interface and frontend design",
            "backend": "backend services and database work"
        }
        
        query = topic_queries.get(topic.lower(), topic)
        
        return await self._get_relevant_commits(user_id, query, limit)


# Singleton instance
_rag_context_builder = None

def get_rag_context_builder() -> RAGContextBuilder:
    """
    Get or create the singleton RAGContextBuilder instance.
    
    Returns:
        Shared RAGContextBuilder instance
    """
    global _rag_context_builder
    if _rag_context_builder is None:
        _rag_context_builder = RAGContextBuilder()
    return _rag_context_builder

