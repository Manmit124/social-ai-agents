# Twitter OAuth Setup Guide

## 🎯 Overview

This guide will help you set up Twitter OAuth 2.0 authentication for your AI Agents Tweet application. You need to configure your Twitter Developer account and then update your environment variables.

---

## 📋 Prerequisites

- A Twitter/X account
- Access to Twitter Developer Portal

---

## 🔧 Step 1: Create Twitter Developer Account

### 1.1 Sign up for Developer Access

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Click **"Sign up for Free Account"** if you haven't already
4. Fill out the application form:
   - **What's your use case?** Select "Making a bot" or "Building tools for Twitter users"
   - **Will you make Twitter content available to a government entity?** Select "No"
   - Accept the Developer Agreement and Policy
5. Verify your email address

### 1.2 Create a New Project

1. Once approved, click **"+ Create Project"**
2. Fill in project details:
   - **Project Name:** `AI Agents Tweet` (or any name you prefer)
   - **Use Case:** Select "Making a bot" or "Exploring the API"
   - **Project Description:** "AI-powered social media content generator"

---

## 🔑 Step 2: Create an App with OAuth 2.0

### 2.1 Create App

1. After creating the project, click **"+ Add App"**
2. Choose **"Development"** environment (free tier)
3. **App Name:** `ai-agents-tweet-app` (must be unique across Twitter)
4. Click **"Complete"**

### 2.2 Save Your API Keys (Important!)

After creating the app, you'll see:
- **API Key** (Client ID)
- **API Key Secret** (Client Secret)

⚠️ **IMPORTANT:** Copy these immediately! Twitter only shows the Client Secret once.

Save them temporarily in a text file:
```
API Key (Client ID): xxxxxxxxxxxxxxxxxxxxx
API Key Secret (Client Secret): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2.3 Configure App Settings

1. Go to your app's **"Settings"** tab
2. Scroll to **"User authentication settings"**
3. Click **"Set up"**

### 2.4 Configure OAuth 2.0 Settings

Fill in the following:

#### App Permissions
- ✅ **Read and write** (required to post tweets)
- ✅ **Request email from users** (optional, but recommended)

#### Type of App
- Select **"Web App, Automated App or Bot"**

#### App Info

**Callback URI / Redirect URL:**
```
http://localhost:8000/api/auth/twitter/callback
```

⚠️ **Important:** This MUST match exactly what you'll put in your `.env` file

**Website URL:**
```
http://localhost:3000
```

**Organization name:** Your name or company name

**Organization website:** 
```
http://localhost:3000
```
(or your actual website if you have one)

**Terms of service:** (optional)
```
http://localhost:3000/terms
```

**Privacy policy:** (optional)
```
http://localhost:3000/privacy
```

4. Click **"Save"**

### 2.5 Get Your Client ID

After saving, you'll see:
- **Client ID:** This is your OAuth 2.0 Client ID (different from API Key)
- **Client Secret:** Click "Generate" if you need a new one

⚠️ **IMPORTANT:** The **Client ID** for OAuth 2.0 is what you need for `TWITTER_CLIENT_ID`

---

## 🔐 Step 3: Configure Environment Variables

### 3.1 Create Backend .env File

Create a file at `/Users/manmit/Dev/idea/ai-agents-tweet/backend/.env`:

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret

# Twitter OAuth 2.0 Configuration
TWITTER_CLIENT_ID=your_oauth2_client_id_here
TWITTER_CLIENT_SECRET=your_oauth2_client_secret_here
TWITTER_REDIRECT_URI=http://localhost:8000/api/auth/twitter/callback

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key

# Server Configuration
CORS_ORIGINS=http://localhost:3000
FRONTEND_URL=http://localhost:3000
PORT=8000
```

### 3.2 Where to Find Each Value

#### Supabase Values:
1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Select your project
3. Go to **Settings** → **API**
   - **SUPABASE_URL:** Project URL
   - **SUPABASE_SERVICE_KEY:** service_role key (under "Project API keys")
4. Go to **Settings** → **API** → **JWT Settings**
   - **SUPABASE_JWT_SECRET:** JWT Secret

#### Twitter Values:
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Select your app
3. Go to **"Keys and tokens"** tab
   - **TWITTER_CLIENT_ID:** OAuth 2.0 Client ID
   - **TWITTER_CLIENT_SECRET:** OAuth 2.0 Client Secret (regenerate if needed)

#### Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy the key

### 3.3 Create Frontend .env.local File

Create a file at `/Users/manmit/Dev/idea/ai-agents-tweet/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000

# Supabase Configuration (for frontend)
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## 🧪 Step 4: Test the Setup

### 4.1 Start Backend

```bash
cd /Users/manmit/Dev/idea/ai-agents-tweet/backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4.2 Start Frontend

Open a new terminal:

```bash
cd /Users/manmit/Dev/idea/ai-agents-tweet/frontend
npm run dev
```

You should see:
```
▲ Next.js 14.x.x
- Local:        http://localhost:3000
```

### 4.3 Test OAuth Flow

1. Open http://localhost:3000
2. Sign up or log in to your app
3. Go to **Settings** page
4. Click **"Connect Twitter"** button
5. You should be redirected to Twitter's authorization page
6. Click **"Authorize app"**
7. You should be redirected back to your app with success message

---

## 🐛 Troubleshooting

### Issue: "Invalid redirect_uri"

**Solution:**
- Make sure the callback URL in Twitter Developer Portal exactly matches your `.env` file
- Both should be: `http://localhost:8000/api/auth/twitter/callback`
- No trailing slashes!

### Issue: "Invalid client_id"

**Solution:**
- Make sure you're using the **OAuth 2.0 Client ID**, not the API Key
- Go to Twitter Developer Portal → Your App → Keys and tokens
- Look for "OAuth 2.0 Client ID"

### Issue: "Unauthorized" or 401 errors

**Solution:**
- Check that you're logged into your app (Supabase authentication)
- Make sure your Supabase JWT secret is correct
- Check browser console for authentication errors

### Issue: "Client authentication failed"

**Solution:**
- Verify your `TWITTER_CLIENT_SECRET` is correct
- Try regenerating the OAuth 2.0 Client Secret in Twitter Developer Portal
- Update your `.env` file with the new secret

### Issue: Backend errors about missing environment variables

**Solution:**
- Make sure `.env` file is in the `backend/` directory
- Check that all required variables are set
- Restart the backend server after changing `.env`

### Issue: Twitter says "App is suspended"

**Solution:**
- Check your Twitter Developer Portal for any policy violations
- Make sure your app complies with Twitter's Developer Agreement
- Contact Twitter Support if needed

---

## 🔒 Security Best Practices

1. **Never commit `.env` files to Git**
   - Add `.env` to `.gitignore`
   - Use `.env.example` for templates

2. **Use different credentials for production**
   - Development: localhost URLs
   - Production: actual domain URLs

3. **Rotate secrets regularly**
   - Regenerate OAuth secrets periodically
   - Update environment variables

4. **Limit token scopes**
   - Only request permissions you need
   - Current scopes: `tweet.read`, `tweet.write`, `users.read`, `offline.access`

---

## 📚 Additional Resources

- [Twitter OAuth 2.0 Documentation](https://developer.twitter.com/en/docs/authentication/oauth-2-0)
- [Twitter API v2 Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Supabase Authentication Docs](https://supabase.com/docs/guides/auth)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## ✅ Checklist

Before testing, make sure you have:

- [ ] Created Twitter Developer account
- [ ] Created a Twitter project and app
- [ ] Enabled OAuth 2.0 with Read and Write permissions
- [ ] Set callback URL to `http://localhost:8000/api/auth/twitter/callback`
- [ ] Copied OAuth 2.0 Client ID and Client Secret
- [ ] Created `backend/.env` with all required variables
- [ ] Created `frontend/.env.local` with Supabase config
- [ ] Started backend server (port 8000)
- [ ] Started frontend server (port 3000)
- [ ] Logged into your app with Supabase auth
- [ ] Tested Twitter connection from Settings page

---

## 🚀 Production Deployment

When deploying to production:

1. **Update Twitter App Settings:**
   - Add production callback URL: `https://your-domain.com/api/auth/twitter/callback`
   - Add production website URL: `https://your-domain.com`

2. **Update Environment Variables:**
   - `TWITTER_REDIRECT_URI=https://your-domain.com/api/auth/twitter/callback`
   - `FRONTEND_URL=https://your-domain.com`
   - `CORS_ORIGINS=https://your-domain.com`

3. **Consider upgrading Twitter API tier** if you need:
   - Higher rate limits
   - More API features
   - Production-level support

---

**Need help?** Check the troubleshooting section or review the backend logs for detailed error messages.

