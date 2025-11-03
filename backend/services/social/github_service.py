"""GitHub OAuth 2.0 service."""

import os
from typing import Dict, List, Optional
from datetime import datetime
import httpx
from dotenv import load_dotenv

load_dotenv()


class GitHubOAuthService:
    """Handle GitHub OAuth 2.0 flow."""
    
    def __init__(self):
        self.client_id = os.getenv("GITHUB_CLIENT_ID")
        self.client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/auth/github/callback")
        
        # GitHub OAuth 2.0 endpoints
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.user_url = "https://api.github.com/user"
        self.repos_url = "https://api.github.com/user/repos"
        
        # OAuth scopes
        self.scopes = [
            "read:user",      # Read user profile
            "user:email",     # Read user email
            "repo"            # Access repositories (public and private)
        ]
    
    def get_authorization_url(self, state: str) -> tuple[str, str]:
        """
        Generate GitHub authorization URL.
        
        Args:
            state: Random state parameter for CSRF protection
            
        Returns:
            tuple: (auth_url, state)
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "state": state,
            "allow_signup": "true"
        }
        
        # Build URL
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        auth_url = f"{self.auth_url}?{query_string}"
        
        return auth_url, state
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access token.
        
        Args:
            code: Authorization code from GitHub
            
        Returns:
            dict: Token response with access_token
        """
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        headers = {
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data=data,
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Token exchange failed: {response.text}")
            
            result = response.json()
            
            # Check for error in response
            if "error" in result:
                raise Exception(f"GitHub OAuth error: {result.get('error_description', result['error'])}")
            
            return result
    
    async def verify_token(self, access_token: str) -> bool:
        """
        Verify if a GitHub token is still valid.
        
        Args:
            access_token: Token to verify
            
        Returns:
            bool: True if valid, False if invalid/revoked
        """
        try:
            await self.get_user_info(access_token)
            return True
        except Exception as e:
            if "invalid or has been revoked" in str(e):
                return False
            raise
    
    async def get_user_info(self, access_token: str) -> Dict:
        """
        Get GitHub user information.
        
        Args:
            access_token: Valid access token
            
        Returns:
            dict: User information
            
        Raises:
            Exception: If token is invalid or revoked (401)
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_url,
                headers=headers
            )
            
            if response.status_code == 401:
                raise Exception("GitHub token is invalid or has been revoked. Please reconnect your account.")
            
            if response.status_code != 200:
                raise Exception(f"Failed to get user info: {response.text}")
            
            return response.json()
    
    async def get_repositories(
        self, 
        access_token: str, 
        per_page: int = 100,
        sort: str = "updated"
    ) -> List[Dict]:
        """
        Get user's repositories.
        
        Args:
            access_token: Valid access token
            per_page: Number of repos per page (max 100)
            sort: Sort by 'created', 'updated', 'pushed', 'full_name'
            
        Returns:
            list: List of repositories
            
        Raises:
            Exception: If token is invalid or revoked (401)
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        params = {
            "per_page": per_page,
            "sort": sort,
            "direction": "desc"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.repos_url,
                headers=headers,
                params=params
            )
            
            if response.status_code == 401:
                raise Exception("GitHub token is invalid or has been revoked. Please reconnect your account.")
            
            if response.status_code != 200:
                raise Exception(f"Failed to get repositories: {response.text}")
            
            return response.json()
    
    async def get_commits(
        self, 
        access_token: str, 
        owner: str, 
        repo: str,
        since: Optional[str] = None,
        per_page: int = 100
    ) -> List[Dict]:
        """
        Get commits from a repository.
        
        Args:
            access_token: Valid access token
            owner: Repository owner (username)
            repo: Repository name
            since: Only commits after this date (ISO 8601 format)
            per_page: Number of commits per page (max 100)
            
        Returns:
            list: List of commits
            
        Raises:
            Exception: If token is invalid or revoked (401)
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        params = {
            "per_page": per_page
        }
        
        if since:
            params["since"] = since
        
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                commits_url,
                headers=headers,
                params=params
            )
            
            if response.status_code == 401:
                raise Exception("GitHub token is invalid or has been revoked. Please reconnect your account.")
            
            if response.status_code != 200:
                raise Exception(f"Failed to get commits: {response.text}")
            
            return response.json()
    
    async def get_user_commits(
        self,
        access_token: str,
        username: str,
        since: Optional[datetime] = None,
        max_repos: int = 10
    ) -> List[Dict]:
        """
        Get recent commits from user's repositories.
        
        Args:
            access_token: Valid access token
            username: GitHub username
            since: Only commits after this date
            max_repos: Maximum number of repositories to check
            
        Returns:
            list: List of commits with repository info
        """
        # Get user's repositories
        repos = await self.get_repositories(access_token, per_page=max_repos)
        
        all_commits = []
        since_str = since.isoformat() if since else None
        
        # Get commits from each repository
        for repo in repos[:max_repos]:
            try:
                repo_name = repo["name"]
                commits = await self.get_commits(
                    access_token,
                    username,
                    repo_name,
                    since=since_str,
                    per_page=30
                )
                
                # Add repository info to each commit
                for commit in commits:
                    commit["repository"] = {
                        "name": repo_name,
                        "full_name": repo["full_name"],
                        "language": repo.get("language"),
                        "description": repo.get("description")
                    }
                    all_commits.append(commit)
                    
            except Exception as e:
                print(f"Error getting commits from {repo['name']}: {str(e)}")
                continue
        
        # Sort by date (most recent first)
        all_commits.sort(
            key=lambda x: x["commit"]["author"]["date"],
            reverse=True
        )
        
        return all_commits

