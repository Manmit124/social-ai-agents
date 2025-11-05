"""
Embedding Job Service - Manages batch embedding generation for GitHub commits.

This service handles:
- Batch processing of commits without embeddings
- Progress tracking
- Error handling and retries
- Efficient API usage with batching
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

from .embedding_service import get_embedding_service
from .github_data_service import GitHubDataService

load_dotenv()


class EmbeddingJobService:
    """Service for managing embedding generation jobs."""
    
    def __init__(self):
        """Initialize the embedding job service."""
        self.embedding_service = get_embedding_service()
        self.github_data_service = GitHubDataService()
        self.default_batch_size = 50  # Process 50 commits at a time
    
    async def generate_embeddings_for_user(
        self,
        user_id: str,
        batch_size: Optional[int] = None,
        max_commits: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate embeddings for all user's commits that don't have them.
        
        Processes commits in batches for efficiency and API rate limiting.
        
        Args:
            user_id: User's UUID
            batch_size: Number of commits to process per batch (default: 50)
            max_commits: Maximum total commits to process (optional)
            
        Returns:
            dict: {
                "total_processed": int,
                "embeddings_generated": int,
                "failed": int,
                "batches_processed": int,
                "stats": {...}
            }
        """
        batch_size = batch_size or self.default_batch_size
        
        print(f"\n🔄 Starting embedding generation for user {user_id}")
        print(f"   Batch size: {batch_size}")
        
        total_processed = 0
        total_generated = 0
        total_failed = 0
        batches_processed = 0
        
        try:
            # Get initial stats
            initial_stats = await self.github_data_service.get_embedding_stats(user_id)
            commits_to_process = initial_stats["commits_without_embeddings"]
            
            if commits_to_process == 0:
                print("   ✅ All commits already have embeddings!")
                return {
                    "total_processed": 0,
                    "embeddings_generated": 0,
                    "failed": 0,
                    "batches_processed": 0,
                    "stats": initial_stats,
                    "message": "All commits already have embeddings"
                }
            
            print(f"   Found {commits_to_process} commits without embeddings")
            
            # Apply max_commits limit if specified
            if max_commits:
                commits_to_process = min(commits_to_process, max_commits)
                print(f"   Limited to {commits_to_process} commits")
            
            # Process in batches
            while total_processed < commits_to_process:
                # Calculate remaining commits
                remaining = commits_to_process - total_processed
                current_batch_size = min(batch_size, remaining)
                
                print(f"\n   📦 Processing batch {batches_processed + 1}...")
                print(f"      Progress: {total_processed}/{commits_to_process}")
                
                # Get commits without embeddings
                commits = await self.github_data_service.get_commits_without_embeddings(
                    user_id,
                    limit=current_batch_size
                )
                
                if not commits:
                    print("      No more commits to process")
                    break
                
                # Extract commit messages
                commit_messages = [commit["commit_message"] for commit in commits]
                
                try:
                    # Generate embeddings in batch
                    embeddings = self.embedding_service.generate_embeddings_batch(
                        commit_messages,
                        task_type="RETRIEVAL_DOCUMENT"
                    )
                    
                    print(f"      ✅ Generated {len(embeddings)} embeddings")
                    
                    # Prepare batch data for saving
                    commit_embeddings = []
                    for i, commit in enumerate(commits):
                        if i < len(embeddings):
                            commit_embeddings.append({
                                "commit_hash": commit["commit_hash"],
                                "embedding": embeddings[i]
                            })
                    
                    # Save embeddings to database
                    result = await self.github_data_service.save_commit_embeddings_batch(
                        user_id,
                        commit_embeddings
                    )
                    
                    total_generated += result["success"]
                    total_failed += result["failed"]
                    total_processed += len(commits)
                    batches_processed += 1
                    
                    print(f"      💾 Saved {result['success']} embeddings")
                    if result["failed"] > 0:
                        print(f"      ⚠️  Failed to save {result['failed']} embeddings")
                
                except Exception as e:
                    print(f"      ❌ Error processing batch: {str(e)}")
                    total_failed += len(commits)
                    total_processed += len(commits)
                    batches_processed += 1
                    continue
            
            # Get final stats
            final_stats = await self.github_data_service.get_embedding_stats(user_id)
            
            print(f"\n✅ Embedding generation complete!")
            print(f"   Total processed: {total_processed}")
            print(f"   Successfully generated: {total_generated}")
            print(f"   Failed: {total_failed}")
            print(f"   Batches: {batches_processed}")
            print(f"   Progress: {final_stats['percentage_complete']}%")
            
            return {
                "total_processed": total_processed,
                "embeddings_generated": total_generated,
                "failed": total_failed,
                "batches_processed": batches_processed,
                "stats": final_stats,
                "message": f"Generated {total_generated} embeddings in {batches_processed} batches"
            }
        
        except Exception as e:
            print(f"❌ Error in embedding generation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Get current stats even if error occurred
            try:
                current_stats = await self.github_data_service.get_embedding_stats(user_id)
            except:
                current_stats = {}
            
            return {
                "total_processed": total_processed,
                "embeddings_generated": total_generated,
                "failed": total_failed,
                "batches_processed": batches_processed,
                "stats": current_stats,
                "error": str(e),
                "message": f"Partial completion: {total_generated} embeddings generated before error"
            }
    
    async def generate_embedding_for_new_commits(
        self,
        user_id: str,
        batch_size: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Generate embeddings only for new commits (without embeddings).
        
        This is useful after a data refresh to only process new commits.
        
        Args:
            user_id: User's UUID
            batch_size: Number of commits to process per batch
            
        Returns:
            dict: Generation results
        """
        print(f"\n🆕 Generating embeddings for new commits only...")
        
        # Get commits without embeddings
        commits = await self.github_data_service.get_commits_without_embeddings(
            user_id,
            limit=batch_size or self.default_batch_size
        )
        
        if not commits:
            return {
                "total_processed": 0,
                "embeddings_generated": 0,
                "failed": 0,
                "message": "No new commits to process"
            }
        
        print(f"   Found {len(commits)} new commits")
        
        # Extract commit messages
        commit_messages = [commit["commit_message"] for commit in commits]
        
        try:
            # Generate embeddings in batch
            embeddings = self.embedding_service.generate_embeddings_batch(
                commit_messages,
                task_type="RETRIEVAL_DOCUMENT"
            )
            
            # Prepare batch data for saving
            commit_embeddings = []
            for i, commit in enumerate(commits):
                if i < len(embeddings):
                    commit_embeddings.append({
                        "commit_hash": commit["commit_hash"],
                        "embedding": embeddings[i]
                    })
            
            # Save embeddings to database
            result = await self.github_data_service.save_commit_embeddings_batch(
                user_id,
                commit_embeddings
            )
            
            print(f"   ✅ Generated and saved {result['success']} embeddings")
            
            return {
                "total_processed": len(commits),
                "embeddings_generated": result["success"],
                "failed": result["failed"],
                "message": f"Processed {len(commits)} new commits"
            }
        
        except Exception as e:
            print(f"   ❌ Error generating embeddings for new commits: {str(e)}")
            return {
                "total_processed": len(commits),
                "embeddings_generated": 0,
                "failed": len(commits),
                "error": str(e),
                "message": "Failed to process new commits"
            }
    
    async def get_embedding_status(self, user_id: str) -> Dict[str, any]:
        """
        Get detailed status of embedding generation progress.
        
        Args:
            user_id: User's UUID
            
        Returns:
            dict: {
                "total_commits": int,
                "commits_with_embeddings": int,
                "commits_needing_embeddings": int,
                "percentage_complete": float,
                "ready_for_search": bool,
                "estimated_batches_remaining": int,
                "status_message": str
            }
        """
        stats = await self.github_data_service.get_embedding_stats(user_id)
        
        # Calculate estimated batches remaining
        commits_needing = stats["commits_without_embeddings"]
        estimated_batches = (commits_needing + self.default_batch_size - 1) // self.default_batch_size
        
        # Generate status message
        if stats["percentage_complete"] == 100:
            status_message = "All commits have embeddings - ready for semantic search!"
        elif stats["percentage_complete"] >= 75:
            status_message = f"Almost done! {commits_needing} commits remaining"
        elif stats["percentage_complete"] >= 50:
            status_message = f"Halfway there! {commits_needing} commits remaining"
        elif stats["percentage_complete"] > 0:
            status_message = f"In progress: {commits_needing} commits remaining"
        else:
            status_message = f"Not started: {commits_needing} commits need embeddings"
        
        return {
            "total_commits": stats["total_commits"],
            "commits_with_embeddings": stats["commits_with_embeddings"],
            "commits_needing_embeddings": stats["commits_without_embeddings"],
            "percentage_complete": stats["percentage_complete"],
            "ready_for_search": stats["ready_for_search"],
            "estimated_batches_remaining": estimated_batches,
            "estimated_api_calls": estimated_batches,  # 1 API call per batch
            "status_message": status_message
        }
    
    async def regenerate_embeddings(
        self,
        user_id: str,
        force: bool = False
    ) -> Dict[str, any]:
        """
        Regenerate embeddings for commits that already have them.
        
        Useful if embedding model is updated or embeddings are corrupted.
        
        Args:
            user_id: User's UUID
            force: If True, regenerate all embeddings
            
        Returns:
            dict: Regeneration results
        """
        if not force:
            return {
                "success": False,
                "message": "Use force=True to regenerate existing embeddings"
            }
        
        print(f"\n🔄 Regenerating ALL embeddings for user {user_id}")
        print("   ⚠️  This will replace existing embeddings")
        
        # Get all commits (with or without embeddings)
        commits = await self.github_data_service.get_user_github_activity(
            user_id,
            limit=1000
        )
        
        if not commits:
            return {
                "success": False,
                "message": "No commits found"
            }
        
        # Use the main generation method
        result = await self.generate_embeddings_for_user(user_id)
        
        return {
            "success": True,
            "message": "Regenerated all embeddings",
            **result
        }


# Singleton instance
_embedding_job_service = None

def get_embedding_job_service() -> EmbeddingJobService:
    """
    Get or create the singleton EmbeddingJobService instance.
    
    Returns:
        Shared EmbeddingJobService instance
    """
    global _embedding_job_service
    if _embedding_job_service is None:
        _embedding_job_service = EmbeddingJobService()
    return _embedding_job_service

