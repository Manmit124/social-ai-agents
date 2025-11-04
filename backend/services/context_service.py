"""Context Service - Manage user context from various data sources."""

import os
from typing import Dict, Optional
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from .github_analysis_service import GitHubAnalysisService
from .gemini_service import GeminiService

load_dotenv()


class ContextService:
    """Service for managing user context."""
    
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Missing Supabase credentials")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.github_analysis = GitHubAnalysisService()
        self.gemini_service = GeminiService()
    
    async def get_user_context(self, user_id: str) -> Optional[Dict]:
        """
        Get stored user context.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Context object or None if not found
        """
        result = self.supabase.table("user_context").select(
            "*"
        ).eq(
            "user_id", user_id
        ).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        
        return None
    
    async def context_exists(self, user_id: str) -> bool:
        """
        Check if user context exists.
        
        Args:
            user_id: User's UUID
            
        Returns:
            True if context exists, False otherwise
        """
        context = await self.get_user_context(user_id)
        return context is not None
    
    async def update_user_context(
        self, 
        user_id: str,
        use_ai: bool = True
    ) -> Dict:
        """
        Rebuild user context from latest data.
        
        Args:
            user_id: User's UUID
            use_ai: Whether to use AI for insights (costs API tokens)
            
        Returns:
            Updated context object
        """
        print(f"\n🔄 Updating context for user {user_id}...")
        
        # Get basic analysis (no AI cost)
        projects = await self.github_analysis.get_current_projects(user_id, days=30, limit=5)
        tech_stack = await self.github_analysis.get_tech_stack(user_id)
        recent_focus = await self.github_analysis.get_recent_focus(user_id, days=7)
        activity_stats = await self.github_analysis.calculate_activity_stats(user_id)
        
        # Prepare context data
        context_data = {
            "user_id": user_id,
            "current_projects": [p["repo"] for p in projects],
            "tech_stack": tech_stack,
            "recent_activity_summary": recent_focus,
            "activity_stats": activity_stats,
            "last_github_fetch": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }
        
        # Add AI insights if requested
        if use_ai and projects:
            print("🤖 Generating AI insights...")
            ai_insights = await self._generate_ai_insights(user_id, projects, tech_stack)
            context_data["ai_insights"] = ai_insights
        else:
            context_data["ai_insights"] = None
        
        # Check if context exists
        existing_context = await self.get_user_context(user_id)
        
        if existing_context:
            # Update existing context
            result = self.supabase.table("user_context").update(
                context_data
            ).eq(
                "user_id", user_id
            ).execute()
        else:
            # Create new context
            result = self.supabase.table("user_context").insert(
                context_data
            ).execute()
        
        print(f"✅ Context updated successfully")
        
        return result.data[0] if result.data else context_data
    
    async def _generate_ai_insights(
        self, 
        user_id: str,
        projects: list,
        tech_stack: list
    ) -> Dict:
        """
        Generate AI insights using Gemini.
        
        Args:
            user_id: User's UUID
            projects: List of current projects
            tech_stack: List of technologies
            
        Returns:
            AI insights object
        """
        # Get data for AI analysis
        analysis_data = await self.github_analysis.prepare_data_for_ai_analysis(user_id)
        
        # Build prompt for Gemini
        prompt = self._build_ai_prompt(analysis_data)
        
        try:
            # Call Gemini API using the same pattern as generate_tweet
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_service.client.models.generate_content(
                    model=self.gemini_service.model_name,
                    contents=prompt
                )
            )
            
            # Extract text from response
            response_text = response.text.strip()
            
            # Parse response (expecting JSON)
            import json
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            insights = json.loads(response_text)
            
            return {
                "focus_areas": insights.get("focus_areas", []),
                "key_achievements": insights.get("key_achievements", []),
                "summary_for_social": insights.get("summary_for_social", ""),
                "generated_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"❌ Error generating AI insights: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "focus_areas": [],
                "key_achievements": [],
                "summary_for_social": "Working on multiple projects",
                "generated_at": datetime.utcnow().isoformat(),
                "error": str(e)
            }
    
    def _build_ai_prompt(self, analysis_data: Dict) -> str:
        """
        Build prompt for AI analysis.
        
        Args:
            analysis_data: Prepared data from GitHub analysis
            
        Returns:
            Prompt string
        """
        projects_str = ", ".join([p["repo"] for p in analysis_data["projects"][:3]])
        tech_str = ", ".join(analysis_data["tech_stack"][:5])
        
        commits_str = "\n".join([
            f"- [{c['repo']}] {c['message']}"
            for c in analysis_data["major_commits"][:10]
        ])
        
        prompt = f"""Analyze this developer's recent GitHub activity and provide insights.

**Current Projects:** {projects_str}
**Technologies:** {tech_str}
**Total Recent Commits:** {analysis_data['total_commits']}

**Major Commits:**
{commits_str}

Please provide a JSON response with:
1. "focus_areas": Array of 2-3 main focus areas (e.g., ["API development", "Authentication"])
2. "key_achievements": Array of 2-3 key achievements (e.g., ["Built payment integration", "Improved performance"])
3. "summary_for_social": One engaging sentence for social media (max 200 chars, professional tone)

Example format:
{{
  "focus_areas": ["Building AI features", "API optimization"],
  "key_achievements": ["Implemented ML model", "Reduced API latency by 40%"],
  "summary_for_social": "Been deep in the code lately, building AI-powered features and optimizing APIs for better performance 🚀"
}}

Keep it authentic, professional, and engaging. Focus on technical achievements.
Return ONLY valid JSON, no additional text."""

        return prompt
    
    async def refresh_ai_insights(self, user_id: str) -> Dict:
        """
        Refresh only the AI insights (manual refresh by user).
        
        Args:
            user_id: User's UUID
            
        Returns:
            Updated context with new AI insights
        """
        print(f"\n🔄 Refreshing AI insights for user {user_id}...")
        
        # Get current context
        context = await self.get_user_context(user_id)
        
        if not context:
            # No context exists, create full context
            return await self.update_user_context(user_id, use_ai=True)
        
        # Get projects and tech stack from existing context
        projects_list = context.get("current_projects", [])
        projects = [{"repo": p} for p in projects_list]
        tech_stack = context.get("tech_stack", [])
        
        if not projects:
            return context
        
        # Generate new AI insights
        ai_insights = await self._generate_ai_insights(user_id, projects, tech_stack)
        
        # Update only AI insights
        result = self.supabase.table("user_context").update({
            "ai_insights": ai_insights,
            "last_updated": datetime.utcnow().isoformat()
        }).eq(
            "user_id", user_id
        ).execute()
        
        print(f"✅ AI insights refreshed successfully")
        
        return result.data[0] if result.data else context

