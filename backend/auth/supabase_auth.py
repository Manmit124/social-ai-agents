"""
Supabase authentication middleware and dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from services.supabase_service import supabase_service

# HTTP Bearer token scheme
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify Supabase JWT token and return user ID
    """
    token = credentials.credentials
    
    try:
        payload = supabase_service.verify_jwt_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user_with_profile(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify JWT token and return user with profile data
    """
    user_id = await get_current_user(credentials)
    profile = supabase_service.get_user_profile(user_id)
    
    return {
        "user_id": user_id,
        "profile": profile
    }
