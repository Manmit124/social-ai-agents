"""Twitter OAuth 2.0 service with PKCE."""

import os
import secrets
import hashlib
import base64
from typing import Dict, Optional
from datetime import datetime, timedelta
import httpx
from dotenv import load_dotenv

load_dotenv()


class TwitterOAuthService:
    """Handle Twitter OAuth 2.0 with PKCE flow."""
    
    def __init__(self):
        self.client_id = os.getenv("TWITTER_CLIENT_ID")
        self.client_secret = os.getenv("TWITTER_CLIENT_SECRET")
        self.redirect_uri = os.getenv("TWITTER_REDIRECT_URI", "http://localhost:8000/api/auth/twitter/callback")
        
        # Twitter OAuth 2.0 endpoints
        self.auth_url = "https://twitter.com/i/oauth2/authorize"
        self.token_url = "https://api.twitter.com/2/oauth2/token"
        self.revoke_url = "https://api.twitter.com/2/oauth2/revoke"
        self.user_url = "https://api.twitter.com/2/users/me"
        
        # OAuth scopes
        self.scopes = [
            "tweet.read",
            "tweet.write",
            "users.read",
            "offline.access"  # For refresh token
        ]
    
    def generate_pkce_pair(self) -> tuple[str, str]:
        """
        Generate PKCE code verifier and challenge.
        
        Returns:
            tuple: (code_verifier, code_challenge)
        """
        # Generate code verifier (43-128 characters)
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
        code_verifier = code_verifier.rstrip('=')
        
        # Generate code challenge (SHA256 hash of verifier)
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.rstrip('=')
        
        return code_verifier, code_challenge
    
    def get_authorization_url(self, state: str) -> tuple[str, str, str]:
        """
        Generate Twitter authorization URL.
        
        Args:
            state: Random state parameter for CSRF protection
            
        Returns:
            tuple: (auth_url, code_verifier, state)
        """
        code_verifier, code_challenge = self.generate_pkce_pair()
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        
        # Build URL
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        auth_url = f"{self.auth_url}?{query_string}"
        
        return auth_url, code_verifier, state
    
    async def exchange_code_for_token(
        self, 
        code: str, 
        code_verifier: str
    ) -> Dict:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from Twitter
            code_verifier: PKCE code verifier
            
        Returns:
            dict: Token response with access_token, refresh_token, etc.
        """
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier
        }
        
        # Add client secret for confidential clients
        if self.client_secret:
            auth = (self.client_id, self.client_secret)
        else:
            auth = None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data=data,
                auth=auth,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Token exchange failed: {response.text}")
            
            return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict:
        """
        Refresh an expired access token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            dict: New token response
        """
        data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.client_id
        }
        
        if self.client_secret:
            auth = (self.client_id, self.client_secret)
        else:
            auth = None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data=data,
                auth=auth,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Token refresh failed: {response.text}")
            
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get Twitter user information.
        
        Args:
            access_token: Valid access token
            
        Returns:
            dict: User information
        """
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        params = {
            "user.fields": "id,name,username,profile_image_url"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_url,
                headers=headers,
                params=params
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get user info: {response.text}")
            
            return response.json()
    
    async def revoke_token(self, token: str) -> bool:
        """
        Revoke an access or refresh token.
        
        Args:
            token: Token to revoke
            
        Returns:
            bool: True if successful
        """
        data = {
            "token": token,
            "token_type_hint": "access_token"
        }
        
        if self.client_secret:
            auth = (self.client_id, self.client_secret)
        else:
            auth = None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.revoke_url,
                data=data,
                auth=auth,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            return response.status_code == 200
    
    async def post_tweet(self, text: str, access_token: str) -> Dict:
        """
        Post a tweet to Twitter.
        
        Args:
            text: Tweet text
            access_token: Valid access token
            
        Returns:
            dict: Tweet response with tweet_id and url
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.twitter.com/2/tweets",
                headers=headers,
                json=data
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to post tweet: {response.text}")
            
            result = response.json()
            tweet_data = result.get("data", {})
            tweet_id = tweet_data.get("id")
            
            # Construct tweet URL
            url = f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None
            
            return {
                "tweet_id": tweet_id,
                "post_id": tweet_id,
                "url": url,
                "raw_response": result
            }
    
    def calculate_token_expiry(self, expires_in: int) -> datetime:
        """
        Calculate token expiration datetime.
        
        Args:
            expires_in: Seconds until expiration
            
        Returns:
            datetime: Expiration time (timezone-aware UTC)
        """
        from datetime import timezone
        return datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    
    def is_token_expired(self, expires_at: datetime) -> bool:
        """
        Check if token is expired.
        
        Args:
            expires_at: Token expiration datetime
            
        Returns:
            bool: True if expired
        """
        from datetime import timezone
        
        # Ensure both datetimes are timezone-aware
        now = datetime.now(timezone.utc)
        
        # If expires_at is naive, assume UTC
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        # Add 5 minute buffer
        return now >= (expires_at - timedelta(minutes=5))

