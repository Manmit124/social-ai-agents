"""
Supabase service for database operations and JWT verification
"""

import os
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from jose import JWTError, jwt
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
        
        if not all([self.url, self.service_key, self.jwt_secret]):
            raise ValueError("Missing required Supabase environment variables")
        
        self.client: Client = create_client(self.url, self.service_key)
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        Verify Supabase JWT token and return user data
        """
        try:
            # Decode JWT with audience validation
            # Supabase uses "authenticated" as the default audience
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
                options={"verify_aud": True}
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user ID"
                )
            return payload
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile from Supabase
        """
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None
    
    def get_connected_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's connected social media accounts
        """
        try:
            response = self.client.table("connected_accounts").select("*").eq("user_id", user_id).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching connected accounts: {e}")
            return []
    
    def get_platform_connection(self, user_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get specific platform connection for user
        """
        try:
            response = self.client.table("connected_accounts").select("*").eq("user_id", user_id).eq("platform", platform).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching platform connection: {e}")
            return None
    
    def get_connected_account(self, user_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get specific platform connection for user (alias for get_platform_connection)
        """
        return self.get_platform_connection(user_id, platform)
    
    def save_connected_account(self, account_data: Dict[str, Any]) -> bool:
        """
        Save or update connected account
        """
        try:
            # Check if account already exists
            existing = self.get_platform_connection(account_data["user_id"], account_data["platform"])
            
            if existing:
                # Update existing account
                response = self.client.table("connected_accounts").update(account_data).eq("id", existing["id"]).execute()
            else:
                # Insert new account
                response = self.client.table("connected_accounts").insert(account_data).execute()
            
            return True
        except Exception as e:
            logger.error(f"Error saving connected account: {e}")
            return False
    
    def delete_connected_account(self, user_id: str, platform: str) -> bool:
        """
        Delete connected account
        """
        try:
            response = self.client.table("connected_accounts").delete().eq("user_id", user_id).eq("platform", platform).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting connected account: {e}")
            return False
    
    def update_platform_tokens(self, user_id: str, platform: str, access_token: str, refresh_token: str, expires_at: Any) -> bool:
        """
        Update access and refresh tokens for a connected account
        """
        try:
            from datetime import datetime
            
            # Convert datetime to ISO string if needed
            if isinstance(expires_at, datetime):
                expires_at_str = expires_at.isoformat()
            else:
                expires_at_str = expires_at
            
            update_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at_str,
                "is_active": True
            }
            
            response = self.client.table("connected_accounts").update(update_data).eq("user_id", user_id).eq("platform", platform).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating platform tokens: {e}")
            return False
    
    def save_post(self, post_data: Dict[str, Any]) -> Optional[str]:
        """
        Save post to database
        """
        try:
            response = self.client.table("posts").insert(post_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error saving post: {e}")
            return None
    
    def get_user_posts(self, user_id: str, platform: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's posts
        """
        try:
            query = self.client.table("posts").select("*").eq("user_id", user_id)
            
            if platform:
                query = query.eq("platform", platform)
            
            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error fetching user posts: {e}")
            return []

# Global instance
supabase_service = SupabaseService()
