"""
Subscription Service
Handles subscription management, post limits, and upgrades
"""

from typing import Optional, Dict
from datetime import datetime, timedelta
from services.supabase_service import supabase_service
import logging

logger = logging.getLogger(__name__)

class SubscriptionService:
    """Service for managing user subscriptions"""
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict]:
        """
        Get user's subscription details.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Subscription dict or None
        """
        try:
            response = supabase_service.client.table("subscriptions").select("*").eq("user_id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            
            # If no subscription exists, create free one
            return self.create_free_subscription(user_id)
        
        except Exception as e:
            logger.error(f"Error getting subscription: {str(e)}")
            return None
    
    def create_free_subscription(self, user_id: str) -> Dict:
        """
        Create a free subscription for new user.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Created subscription dict
        """
        try:
            subscription_data = {
                "user_id": user_id,
                "plan_type": "free",
                "status": "active",
                "posts_used": 0,
                "posts_limit": 5,
                "current_period_start": datetime.utcnow().isoformat(),
                "current_period_end": (datetime.utcnow() + timedelta(days=30)).isoformat()
            }
            
            response = supabase_service.client.table("subscriptions").insert(subscription_data).execute()
            
            if response.data and len(response.data) > 0:
                logger.info(f"✅ Created free subscription for user {user_id}")
                return response.data[0]
            
            raise Exception("Failed to create subscription")
        
        except Exception as e:
            logger.error(f"Error creating free subscription: {str(e)}")
            # If subscription already exists, return it
            return self.get_user_subscription(user_id)
    
    def can_user_post(self, user_id: str) -> tuple[bool, str]:
        """
        Check if user can post (hasn't exceeded limit).
        
        Args:
            user_id: User's UUID
            
        Returns:
            Tuple of (can_post: bool, message: str)
        """
        try:
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return False, "Subscription not found"
            
            # Check if subscription is active
            if subscription.get("status") != "active":
                return False, "Your subscription is not active"
            
            # Check if period has expired (reset monthly)
            period_end = subscription.get("current_period_end")
            if period_end:
                end_date = datetime.fromisoformat(period_end.replace('Z', '+00:00'))
                if datetime.utcnow() > end_date:
                    # Reset monthly limit
                    self.reset_monthly_limit(user_id)
                    subscription = self.get_user_subscription(user_id)
            
            posts_used = subscription.get("posts_used", 0)
            posts_limit = subscription.get("posts_limit", 5)
            
            # Pro plan has unlimited posts (posts_limit = -1)
            if posts_limit == -1:
                return True, "Unlimited posts available"
            
            # Free plan: Check if limit reached
            if posts_used >= posts_limit:
                return False, f"You've reached your monthly limit of {posts_limit} posts. Upgrade to Pro for unlimited posts."
            
            return True, f"{posts_limit - posts_used} posts remaining this month"
        
        except Exception as e:
            logger.error(f"Error checking post limit: {str(e)}")
            return False, "Error checking subscription status"
    
    def increment_post_count(self, user_id: str) -> bool:
        """
        Increment post count after successful post.
        
        Args:
            user_id: User's UUID
            
        Returns:
            True if successful
        """
        try:
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return False
            
            # Check if period expired (reset first)
            period_end = subscription.get("current_period_end")
            if period_end:
                end_date = datetime.fromisoformat(period_end.replace('Z', '+00:00'))
                if datetime.utcnow() > end_date:
                    self.reset_monthly_limit(user_id)
                    subscription = self.get_user_subscription(user_id)
            
            posts_used = subscription.get("posts_used", 0)
            posts_limit = subscription.get("posts_limit", 5)
            
            # Don't increment if already at limit (shouldn't happen, but safety check)
            if posts_limit != -1 and posts_used >= posts_limit:
                return False
            
            # Increment post count
            new_count = posts_used + 1
            
            supabase_service.client.table("subscriptions").update({
                "posts_used": new_count,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).execute()
            
            logger.info(f"✅ Incremented post count for user {user_id}: {new_count}")
            return True
        
        except Exception as e:
            logger.error(f"Error incrementing post count: {str(e)}")
            return False
    
    def upgrade_to_pro(self, user_id: str, razorpay_payment_id: str, razorpay_order_id: str) -> bool:
        """
        Upgrade user to Pro subscription.
        
        Args:
            user_id: User's UUID
            razorpay_payment_id: Razorpay payment ID
            razorpay_order_id: Razorpay order ID
            
        Returns:
            True if successful
        """
        try:
            # Calculate next period (1 month from now)
            now = datetime.utcnow()
            next_period_end = now + timedelta(days=30)
            
            update_data = {
                "plan_type": "pro",
                "status": "active",
                "posts_limit": -1,  # -1 means unlimited
                "posts_used": 0,  # Reset on upgrade
                "current_period_start": now.isoformat(),
                "current_period_end": next_period_end.isoformat(),
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_order_id": razorpay_order_id,
                "updated_at": now.isoformat()
            }
            
            response = supabase_service.client.table("subscriptions").update(update_data).eq("user_id", user_id).execute()
            
            if response.data:
                logger.info(f"✅ Upgraded user {user_id} to Pro")
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error upgrading to Pro: {str(e)}")
            return False
    
    def reset_monthly_limit(self, user_id: str) -> bool:
        """
        Reset monthly post limit (called at start of new billing period).
        
        Args:
            user_id: User's UUID
            
        Returns:
            True if successful
        """
        try:
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return False
            
            # Calculate next period
            now = datetime.utcnow()
            next_period_end = now + timedelta(days=30)
            
            # Get posts_limit (keep same plan)
            posts_limit = subscription.get("posts_limit", 5)
            
            update_data = {
                "posts_used": 0,
                "current_period_start": now.isoformat(),
                "current_period_end": next_period_end.isoformat(),
                "updated_at": now.isoformat()
            }
            
            supabase_service.client.table("subscriptions").update(update_data).eq("user_id", user_id).execute()
            
            logger.info(f"✅ Reset monthly limit for user {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error resetting monthly limit: {str(e)}")
            return False
    
    def get_subscription_status(self, user_id: str) -> Dict:
        """
        Get subscription status for frontend display.
        
        Args:
            user_id: User's UUID
            
        Returns:
            Status dict with plan, usage, etc.
        """
        try:
            subscription = self.get_user_subscription(user_id)
            
            if not subscription:
                return {
                    "plan_type": "free",
                    "posts_used": 0,
                    "posts_limit": 5,
                    "status": "active"
                }
            
            posts_used = subscription.get("posts_used", 0)
            posts_limit = subscription.get("posts_limit", 5)
            
            # Calculate remaining posts
            if posts_limit == -1:
                remaining = "unlimited"
            else:
                remaining = max(0, posts_limit - posts_used)
            
            return {
                "plan_type": subscription.get("plan_type", "free"),
                "status": subscription.get("status", "active"),
                "posts_used": posts_used,
                "posts_limit": posts_limit,
                "remaining": remaining,
                "current_period_end": subscription.get("current_period_end")
            }
        
        except Exception as e:
            logger.error(f"Error getting subscription status: {str(e)}")
            return {
                "plan_type": "free",
                "posts_used": 0,
                "posts_limit": 5,
                "status": "active"
            }


# Singleton instance
_subscription_service = None

def get_subscription_service() -> SubscriptionService:
    """Get or create SubscriptionService instance"""
    global _subscription_service
    if _subscription_service is None:
        _subscription_service = SubscriptionService()
    return _subscription_service

