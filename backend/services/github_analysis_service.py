"""GitHub Analysis Service - Analyze GitHub activity data."""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class GitHubAnalysisService:
    """Service for analyzing GitHub activity data."""
    
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Missing Supabase credentials")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
        
        # Keywords for filtering commits
        self.noise_keywords = [
            "typo", "readme", "formatting", "whitespace", "comment",
            "indent", "style", "lint", "cleanup", "minor", "docs only"
        ]
        
        self.major_keywords = [
            "added", "implemented", "created", "built", "released",
            "merged", "feature", "new", "initial", "integrate"
        ]
    
    async def get_current_projects(
        self, 
        user_id: str, 
        days: int = 7,
        limit: int = 5
    ) -> List[Dict]:
        """
        Find most active repositories.
        
        Args:
            user_id: User's UUID
            days: Number of days to look back
            limit: Maximum number of projects to return
            
        Returns:
            List of dicts: [{"repo": "ai-project", "commits": 12}, ...]
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get commits from last N days
        result = self.supabase.table("github_activity").select(
            "repository_name"
        ).eq(
            "user_id", user_id
        ).gte(
            "commit_date", since_date.isoformat()
        ).execute()
        
        if not result.data:
            return []
        
        # Count commits per repository
        repo_counts = Counter([commit["repository_name"] for commit in result.data])
        
        # Sort by count and return top N
        projects = [
            {"repo": repo, "commits": count}
            for repo, count in repo_counts.most_common(limit)
        ]
        
        return projects
    
    async def get_tech_stack(self, user_id: str) -> List[str]:
        """
        Identify technologies used.
        
        Args:
            user_id: User's UUID
            
        Returns:
            List of languages: ["Python", "TypeScript", "React", ...]
        """
        # Get all unique languages from commits
        result = self.supabase.table("github_activity").select(
            "language"
        ).eq(
            "user_id", user_id
        ).not_.is_(
            "language", "null"
        ).execute()
        
        if not result.data:
            return []
        
        # Count language frequency
        language_counts = Counter([
            commit["language"] 
            for commit in result.data 
            if commit.get("language")
        ])
        
        # Return languages sorted by frequency
        tech_stack = [lang for lang, _ in language_counts.most_common(10)]
        
        return tech_stack
    
    async def identify_major_commits(
        self, 
        user_id: str, 
        days: int = 30,
        limit: int = 20
    ) -> List[Dict]:
        """
        Filter out minor commits, keep significant ones.
        
        Args:
            user_id: User's UUID
            days: Number of days to look back
            limit: Maximum number of commits to return
            
        Returns:
            List of major commits
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get recent commits
        result = self.supabase.table("github_activity").select(
            "*"
        ).eq(
            "user_id", user_id
        ).gte(
            "commit_date", since_date.isoformat()
        ).order(
            "commit_date", desc=True
        ).limit(100).execute()
        
        if not result.data:
            return []
        
        major_commits = []
        
        for commit in result.data:
            message = commit.get("commit_message", "").lower()
            
            # Skip if contains noise keywords
            if any(keyword in message for keyword in self.noise_keywords):
                continue
            
            # Keep if contains major keywords or is substantial
            if any(keyword in message for keyword in self.major_keywords) or len(message) > 50:
                major_commits.append(commit)
            
            if len(major_commits) >= limit:
                break
        
        return major_commits
    
    async def get_recent_focus(
        self, 
        user_id: str, 
        days: int = 7
    ) -> str:
        """
        Summarize what user worked on recently.
        
        Args:
            user_id: User's UUID
            days: Number of days to look back
            
        Returns:
            Summary string
        """
        projects = await self.get_current_projects(user_id, days=days, limit=3)
        
        if not projects:
            return "No recent activity"
        
        # Create simple summary
        if len(projects) == 1:
            summary = f"Working on {projects[0]['repo']} ({projects[0]['commits']} commits)"
        elif len(projects) == 2:
            summary = f"Working on {projects[0]['repo']} and {projects[1]['repo']}"
        else:
            top_repos = ", ".join([p['repo'] for p in projects[:2]])
            summary = f"Working on {top_repos}, and {projects[2]['repo']}"
        
        return summary
    
    async def calculate_activity_stats(self, user_id: str) -> Dict:
        """
        Calculate activity metrics.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Dict with activity statistics
        """
        now = datetime.utcnow()
        
        # Get commits from last 7 days
        seven_days_ago = now - timedelta(days=7)
        result_7d = self.supabase.table("github_activity").select(
            "commit_date"
        ).eq(
            "user_id", user_id
        ).gte(
            "commit_date", seven_days_ago.isoformat()
        ).execute()
        
        # Get commits from last 30 days
        thirty_days_ago = now - timedelta(days=30)
        result_30d = self.supabase.table("github_activity").select(
            "commit_date"
        ).eq(
            "user_id", user_id
        ).gte(
            "commit_date", thirty_days_ago.isoformat()
        ).execute()
        
        commits_7d = len(result_7d.data) if result_7d.data else 0
        commits_30d = len(result_30d.data) if result_30d.data else 0
        
        # Calculate average
        avg_per_day = round(commits_30d / 30, 1) if commits_30d > 0 else 0
        
        # Find most active day of week
        most_active_day = "N/A"
        most_active_time = "N/A"
        
        if result_30d.data:
            # Parse commit dates and find patterns
            days_of_week = []
            hours_of_day = []
            
            for commit in result_30d.data:
                try:
                    commit_dt = datetime.fromisoformat(commit["commit_date"].replace("Z", "+00:00"))
                    days_of_week.append(commit_dt.strftime("%A"))
                    hours_of_day.append(commit_dt.hour)
                except:
                    continue
            
            if days_of_week:
                day_counter = Counter(days_of_week)
                most_active_day = day_counter.most_common(1)[0][0]
            
            if hours_of_day:
                hour_counter = Counter(hours_of_day)
                most_active_hour = hour_counter.most_common(1)[0][0]
                
                # Convert to readable time
                if most_active_hour < 12:
                    most_active_time = f"{most_active_hour}:00 AM"
                elif most_active_hour == 12:
                    most_active_time = "12:00 PM"
                else:
                    most_active_time = f"{most_active_hour - 12}:00 PM"
        
        return {
            "commits_last_7_days": commits_7d,
            "commits_last_30_days": commits_30d,
            "average_commits_per_day": avg_per_day,
            "most_active_day": most_active_day,
            "most_active_time": most_active_time
        }
    
    async def prepare_data_for_ai_analysis(
        self, 
        user_id: str
    ) -> Dict:
        """
        Prepare data for AI analysis.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Dict with data ready for AI prompt
        """
        # Get major commits
        major_commits = await self.identify_major_commits(user_id, days=30, limit=15)
        
        # Get projects and tech stack
        projects = await self.get_current_projects(user_id, days=30, limit=5)
        tech_stack = await self.get_tech_stack(user_id)
        
        # Format commit messages for AI
        commit_messages = [
            {
                "repo": commit.get("repository_name"),
                "message": commit.get("commit_message", "").split("\n")[0][:100],  # First line, max 100 chars
                "date": commit.get("commit_date")
            }
            for commit in major_commits[:15]  # Only send top 15
        ]
        
        return {
            "projects": projects,
            "tech_stack": tech_stack,
            "major_commits": commit_messages,
            "total_commits": len(major_commits)
        }

