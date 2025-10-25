#!/usr/bin/env python3
"""
Quick script to verify Twitter OAuth setup
Run this before starting your app to catch configuration issues early
"""

import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def check_env_var(name, required=True):
    """Check if an environment variable is set"""
    value = os.getenv(name)
    if not value:
        if required:
            print(f"❌ MISSING: {name}")
            return False
        else:
            print(f"⚠️  OPTIONAL: {name} (not set)")
            return True
    else:
        # Show partial value for verification
        if len(value) > 20:
            display = f"{value[:10]}...{value[-5:]}"
        else:
            display = f"{value[:5]}..."
        print(f"✅ {name}: {display}")
        return True

def main():
    print("=" * 60)
    print("🔍 Twitter OAuth Configuration Checker")
    print("=" * 60)
    print()
    
    all_good = True
    
    print("📋 Checking Supabase Configuration...")
    print("-" * 60)
    all_good &= check_env_var("SUPABASE_URL")
    all_good &= check_env_var("SUPABASE_SERVICE_KEY")
    all_good &= check_env_var("SUPABASE_JWT_SECRET")
    print()
    
    print("🐦 Checking Twitter OAuth 2.0 Configuration...")
    print("-" * 60)
    all_good &= check_env_var("TWITTER_CLIENT_ID")
    all_good &= check_env_var("TWITTER_CLIENT_SECRET")
    all_good &= check_env_var("TWITTER_REDIRECT_URI")
    print()
    
    print("🤖 Checking Gemini AI Configuration...")
    print("-" * 60)
    all_good &= check_env_var("GEMINI_API_KEY")
    print()
    
    print("⚙️  Checking Server Configuration...")
    print("-" * 60)
    check_env_var("CORS_ORIGINS", required=False)
    check_env_var("FRONTEND_URL", required=False)
    check_env_var("PORT", required=False)
    print()
    
    # Validate Twitter redirect URI format
    redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
    if redirect_uri:
        print("🔗 Validating Redirect URI...")
        print("-" * 60)
        if not redirect_uri.startswith("http"):
            print(f"❌ Redirect URI must start with http:// or https://")
            print(f"   Current: {redirect_uri}")
            all_good = False
        elif not "/api/auth/twitter/callback" in redirect_uri:
            print(f"⚠️  Redirect URI should end with /api/auth/twitter/callback")
            print(f"   Current: {redirect_uri}")
        else:
            print(f"✅ Redirect URI format looks good: {redirect_uri}")
        print()
    
    # Check Twitter Client ID format
    client_id = os.getenv("TWITTER_CLIENT_ID")
    if client_id:
        print("🔑 Validating Twitter Client ID...")
        print("-" * 60)
        if len(client_id) < 20:
            print(f"⚠️  Twitter Client ID seems too short (length: {len(client_id)})")
            print(f"   Make sure you're using OAuth 2.0 Client ID, not API Key")
        else:
            print(f"✅ Client ID length looks good ({len(client_id)} characters)")
        print()
    
    print("=" * 60)
    if all_good:
        print("✅ All required configuration variables are set!")
        print()
        print("📝 Next Steps:")
        print("   1. Make sure you've configured Twitter Developer Portal:")
        print("      - App permissions: Read and Write")
        print("      - Callback URL matches TWITTER_REDIRECT_URI")
        print("   2. Start the backend: python main.py")
        print("   3. Start the frontend: npm run dev")
        print("   4. Test OAuth flow from Settings page")
        print()
        print("📚 For detailed setup instructions, see:")
        print("   TWITTER_OAUTH_SETUP.md")
    else:
        print("❌ Configuration incomplete!")
        print()
        print("📝 To fix:")
        print("   1. Copy env.example to .env in backend directory")
        print("   2. Fill in all required values")
        print("   3. See TWITTER_OAUTH_SETUP.md for detailed instructions")
        print()
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()

