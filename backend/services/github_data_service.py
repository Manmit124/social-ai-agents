"""GitHub Data Service - Handles storing and retrieving GitHub activity data."""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class GitHubDataService:
    """Service for managing GitHub activity data in database."""
    
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Missing Supabase credentials")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
    
    async def save_github_commits(
        self, 
        user_id: str, 
        commits_data: List[Dict]
    ) -> Dict[str, int]:
        """
        Save GitHub commits to database.
        
        Args:
            user_id: User's UUID
            commits_data: List of commit objects from GitHub API
            
        Returns:
            dict: {"new_commits": count, "skipped": count}
        """
        new_commits = 0
        skipped = 0
        
        for commit in commits_data:
            try:
                # Extract commit data
                commit_hash = commit.get("sha")
                commit_message = commit.get("commit", {}).get("message", "")
                commit_date_str = commit.get("commit", {}).get("author", {}).get("date")
                
                # Parse date
                commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
                
                # Get repository info
                repo_info = commit.get("repository", {})
                repository_name = repo_info.get("name", "unknown")
                language = repo_info.get("language")
                
                # Check if commit already exists
                existing = self.supabase.table("github_activity").select("id").eq(
                    "commit_hash", commit_hash
                ).execute()
                
                if existing.data:
                    skipped += 1
                    continue
                
                # Insert new commit
                self.supabase.table("github_activity").insert({
                    "user_id": user_id,
                    "repository_name": repository_name,
                    "commit_hash": commit_hash,
                    "commit_message": commit_message,
                    "commit_date": commit_date.isoformat(),
                    "language": language,
                    "raw_data": commit
                }).execute()
                
                new_commits += 1
                
            except Exception as e:
                print(f"Error saving commit {commit.get('sha', 'unknown')}: {str(e)}")
                skipped += 1
                continue
        
        return {
            "new_commits": new_commits,
            "skipped": skipped
        }
    
    async def get_user_github_activity(
        self, 
        user_id: str, 
        limit: int = 100,
        days: Optional[int] = None
    ) -> List[Dict]:
        """
        Get user's stored GitHub activity.
        
        Args:
            user_id: User's UUID
            limit: Maximum number of commits to return
            days: Only return commits from last N days (optional)
            
        Returns:
            list: List of commits from database
        """
        query = self.supabase.table("github_activity").select("*").eq(
            "user_id", user_id
        ).order("commit_date", desc=True).limit(limit)
        
        # Filter by date if specified
        if days:
            since_date = datetime.utcnow() - timedelta(days=days)
            query = query.gte("commit_date", since_date.isoformat())
        
        result = query.execute()
        return result.data
    
    async def update_fetch_log(
        self,
        user_id: str,
        last_commit_date: Optional[datetime],
        total_count: int,
        fetch_type: str = "manual"
    ) -> Dict:
        """
        Update fetch log after data collection.
        
        Args:
            user_id: User's UUID
            last_commit_date: Most recent commit date collected
            total_count: Number of commits fetched
            fetch_type: Type of fetch ('initial', 'refresh', 'manual')
            
        Returns:
            dict: Created log entry
        """
        log_data = {
            "user_id": user_id,
            "last_fetch_time": datetime.utcnow().isoformat(),
            "last_commit_date": last_commit_date.isoformat() if last_commit_date else None,
            "total_commits_fetched": total_count,
            "fetch_type": fetch_type
        }
        
        result = self.supabase.table("github_data_fetch_log").insert(log_data).execute()
        return result.data[0] if result.data else {}
    
    async def get_last_fetch_info(self, user_id: str) -> Optional[Dict]:
        """
        Get user's last fetch information.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Last fetch info or None if never fetched
        """
        result = self.supabase.table("github_data_fetch_log").select("*").eq(
            "user_id", user_id
        ).order("last_fetch_time", desc=True).limit(1).execute()
        
        return result.data[0] if result.data else None
    
    async def get_last_commit_date(self, user_id: str) -> Optional[datetime]:
        """
        Get most recent commit date from stored data.
        
        Args:
            user_id: User's UUID
            
        Returns:
            datetime: Most recent commit date or None
        """
        result = self.supabase.table("github_activity").select("commit_date").eq(
            "user_id", user_id
        ).order("commit_date", desc=True).limit(1).execute()
        
        if result.data:
            date_str = result.data[0]["commit_date"]
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        
        return None
    
    async def get_commit_count(self, user_id: str) -> int:
        """
        Get total number of commits stored for user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            int: Total commit count
        """
        result = self.supabase.table("github_activity").select(
            "id", count="exact"
        ).eq("user_id", user_id).execute()
        
        return result.count if result.count else 0
    
    async def get_repositories(self, user_id: str) -> List[str]:
        """
        Get list of unique repositories for user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            list: List of repository names
        """
        result = self.supabase.table("github_activity").select(
            "repository_name"
        ).eq("user_id", user_id).execute()
        
        # Get unique repository names
        repos = set(item["repository_name"] for item in result.data)
        return sorted(list(repos))
    
    async def should_refresh_data(self, user_id: str, hours_threshold: int = 24) -> Dict[str, any]:
        """
        Check if data needs refresh based on time threshold.
        
        Args:
            user_id: User's UUID
            hours_threshold: Hours after which data is considered stale (default: 24)
            
        Returns:
            dict: {
                "should_refresh": Boolean,
                "hours_since_fetch": Float,
                "last_fetch_time": ISO string or None,
                "reason": String explanation
            }
        """
        last_fetch_info = await self.get_last_fetch_info(user_id)
        
        if not last_fetch_info:
            return {
                "should_refresh": True,
                "hours_since_fetch": None,
                "last_fetch_time": None,
                "reason": "No data fetched yet"
            }
        
        last_fetch_time_str = last_fetch_info["last_fetch_time"]
        last_fetch_time = datetime.fromisoformat(last_fetch_time_str.replace("Z", "+00:00"))
        
        # Calculate hours since last fetch
        now = datetime.utcnow().replace(tzinfo=last_fetch_time.tzinfo)
        hours_since_fetch = (now - last_fetch_time).total_seconds() / 3600
        
        should_refresh = hours_since_fetch > hours_threshold
        
        if should_refresh:
            reason = f"Data is {hours_since_fetch:.1f} hours old (threshold: {hours_threshold}h)"
        else:
            reason = f"Data is fresh ({hours_since_fetch:.1f} hours old)"
        
        return {
            "should_refresh": should_refresh,
            "hours_since_fetch": round(hours_since_fetch, 2),
            "last_fetch_time": last_fetch_time_str,
            "reason": reason
        }
    
    async def get_refresh_recommendation(self, user_id: str) -> Dict[str, any]:
        """
        Get comprehensive refresh recommendation with context.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Detailed refresh recommendation with stats
        """
        refresh_check = await self.should_refresh_data(user_id)
        total_commits = await self.get_commit_count(user_id)
        last_commit_date = await self.get_last_commit_date(user_id)
        
        return {
            "should_refresh": refresh_check["should_refresh"],
            "hours_since_fetch": refresh_check["hours_since_fetch"],
            "last_fetch_time": refresh_check["last_fetch_time"],
            "reason": refresh_check["reason"],
            "total_commits_stored": total_commits,
            "last_commit_date": last_commit_date.isoformat() if last_commit_date else None,
            "has_data": total_commits > 0
        }

