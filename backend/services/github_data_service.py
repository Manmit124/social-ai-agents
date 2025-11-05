"""GitHub Data Service - Handles storing and retrieving GitHub activity data."""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import json

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
            # Handle various ISO format variations
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except ValueError:
                # If parsing fails, try parsing with dateutil
                from dateutil import parser
                return parser.isoparse(date_str)
        
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
        # Handle various ISO format variations
        try:
            last_fetch_time = datetime.fromisoformat(last_fetch_time_str.replace("Z", "+00:00"))
        except ValueError:
            # If parsing fails, try parsing with dateutil
            from dateutil import parser
            last_fetch_time = parser.isoparse(last_fetch_time_str)
        
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
    
    # ========================================================================
    # EMBEDDING METHODS (Phase 3 - Semantic Search)
    # ========================================================================
    
    async def save_commit_embedding(
        self,
        user_id: str,
        commit_hash: str,
        embedding: List[float]
    ) -> bool:
        """
        Save embedding vector for a commit.
        
        Args:
            user_id: User's UUID
            commit_hash: Commit SHA hash
            embedding: Embedding vector (768 dimensions)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert embedding list to PostgreSQL vector format
            # Supabase expects the vector as a string representation
            embedding_str = json.dumps(embedding)
            
            # Update the commit with the embedding
            result = self.supabase.table("github_activity").update({
                "embedding": embedding_str
            }).eq("user_id", user_id).eq("commit_hash", commit_hash).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            print(f"❌ Error saving embedding for commit {commit_hash}: {str(e)}")
            return False
    
    async def save_commit_embeddings_batch(
        self,
        user_id: str,
        commit_embeddings: List[Dict[str, any]]
    ) -> Dict[str, int]:
        """
        Save multiple commit embeddings efficiently.
        
        Args:
            user_id: User's UUID
            commit_embeddings: List of dicts with 'commit_hash' and 'embedding'
            
        Returns:
            dict: {"success": count, "failed": count}
        """
        success = 0
        failed = 0
        
        for item in commit_embeddings:
            commit_hash = item.get("commit_hash")
            embedding = item.get("embedding")
            
            if not commit_hash or not embedding:
                failed += 1
                continue
            
            result = await self.save_commit_embedding(user_id, commit_hash, embedding)
            if result:
                success += 1
            else:
                failed += 1
        
        return {
            "success": success,
            "failed": failed
        }
    
    async def get_commits_without_embeddings(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get commits that don't have embeddings yet.
        
        Args:
            user_id: User's UUID
            limit: Maximum number of commits to return
            
        Returns:
            list: Commits without embeddings
        """
        try:
            result = self.supabase.table("github_activity").select(
                "id, commit_hash, commit_message, commit_date, repository_name, language"
            ).eq("user_id", user_id).is_("embedding", "null").order(
                "commit_date", desc=True
            ).limit(limit).execute()
            
            return result.data
            
        except Exception as e:
            print(f"❌ Error getting commits without embeddings: {str(e)}")
            return []
    
    async def get_commits_with_embeddings(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get commits that have embeddings.
        
        Args:
            user_id: User's UUID
            limit: Maximum number of commits to return
            
        Returns:
            list: Commits with embeddings
        """
        try:
            result = self.supabase.table("github_activity").select(
                "id, commit_hash, commit_message, commit_date, repository_name, language, embedding"
            ).eq("user_id", user_id).not_.is_("embedding", "null").order(
                "commit_date", desc=True
            ).limit(limit).execute()
            
            # Parse embeddings from JSON strings
            for commit in result.data:
                if commit.get("embedding"):
                    try:
                        commit["embedding"] = json.loads(commit["embedding"])
                    except:
                        commit["embedding"] = None
            
            return result.data
            
        except Exception as e:
            print(f"❌ Error getting commits with embeddings: {str(e)}")
            return []
    
    async def get_embedding_for_commit(
        self,
        commit_hash: str
    ) -> Optional[List[float]]:
        """
        Get stored embedding for a specific commit.
        
        Args:
            commit_hash: Commit SHA hash
            
        Returns:
            list: Embedding vector or None if not found
        """
        try:
            result = self.supabase.table("github_activity").select(
                "embedding"
            ).eq("commit_hash", commit_hash).execute()
            
            if result.data and result.data[0].get("embedding"):
                embedding_str = result.data[0]["embedding"]
                return json.loads(embedding_str)
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting embedding for commit {commit_hash}: {str(e)}")
            return None
    
    async def search_similar_commits(
        self,
        user_id: str,
        query_embedding: List[float],
        limit: int = 10,
        min_similarity: float = 0.5
    ) -> List[Dict]:
        """
        Search for commits similar to the query using vector similarity.
        
        Uses cosine similarity (1 - cosine distance) for ranking.
        
        Args:
            user_id: User's UUID
            query_embedding: Query embedding vector (768 dimensions)
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold (0-1)
            
        Returns:
            list: Similar commits with similarity scores
        """
        try:
            # Convert query embedding to PostgreSQL vector format
            query_vector_str = json.dumps(query_embedding)
            
            # Use pgvector's cosine distance operator (<=>)
            # Note: Supabase Python client might need RPC call for vector operations
            # We'll use a stored procedure approach
            
            result = self.supabase.rpc(
                'search_similar_commits',
                {
                    'query_user_id': user_id,
                    'query_embedding': query_vector_str,
                    'match_threshold': 1 - min_similarity,  # Convert similarity to distance
                    'match_count': limit
                }
            ).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Error searching similar commits: {str(e)}")
            print(f"   Note: You may need to create the search_similar_commits RPC function in Supabase")
            # Fallback: Get all commits with embeddings and calculate similarity in Python
            return await self._search_similar_commits_fallback(user_id, query_embedding, limit, min_similarity)
    
    async def _search_similar_commits_fallback(
        self,
        user_id: str,
        query_embedding: List[float],
        limit: int,
        min_similarity: float
    ) -> List[Dict]:
        """
        Fallback method to search similar commits using Python-based similarity calculation.
        
        This is less efficient but works without database functions.
        """
        try:
            # Get all commits with embeddings
            commits = await self.get_commits_with_embeddings(user_id, limit=1000)
            
            if not commits:
                return []
            
            # Calculate similarity for each commit
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
            
            query_vec = np.array(query_embedding).reshape(1, -1)
            results = []
            
            for commit in commits:
                if not commit.get("embedding"):
                    continue
                
                commit_vec = np.array(commit["embedding"]).reshape(1, -1)
                similarity = float(cosine_similarity(query_vec, commit_vec)[0][0])
                
                if similarity >= min_similarity:
                    results.append({
                        "id": commit["id"],
                        "commit_hash": commit["commit_hash"],
                        "commit_message": commit["commit_message"],
                        "commit_date": commit["commit_date"],
                        "repository_name": commit["repository_name"],
                        "language": commit["language"],
                        "similarity": round(similarity, 4)
                    })
            
            # Sort by similarity (highest first)
            results.sort(key=lambda x: x["similarity"], reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            print(f"❌ Error in fallback similarity search: {str(e)}")
            return []
    
    async def get_embedding_stats(self, user_id: str) -> Dict[str, any]:
        """
        Get statistics about embeddings for a user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: Statistics about embeddings
        """
        try:
            total_commits = await self.get_commit_count(user_id)
            
            # Count commits with embeddings
            result = self.supabase.table("github_activity").select(
                "id", count="exact"
            ).eq("user_id", user_id).not_.is_("embedding", "null").execute()
            
            commits_with_embeddings = result.count if result.count else 0
            commits_without_embeddings = total_commits - commits_with_embeddings
            
            percentage = (commits_with_embeddings / total_commits * 100) if total_commits > 0 else 0
            
            return {
                "total_commits": total_commits,
                "commits_with_embeddings": commits_with_embeddings,
                "commits_without_embeddings": commits_without_embeddings,
                "percentage_complete": round(percentage, 2),
                "ready_for_search": commits_with_embeddings > 0
            }
            
        except Exception as e:
            print(f"❌ Error getting embedding stats: {str(e)}")
            return {
                "total_commits": 0,
                "commits_with_embeddings": 0,
                "commits_without_embeddings": 0,
                "percentage_complete": 0,
                "ready_for_search": False
            }

