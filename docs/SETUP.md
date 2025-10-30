# Quick Setup Guide

## ✅ What's Been Built

Your AI Agents Tweet application is complete with:

- ✅ **Backend** - Python FastAPI + LangGraph agent
- ✅ **Frontend** - Next.js with Tailwind CSS + shadcn/ui
- ✅ **Agent Flow** - Multi-step AI workflow (Plan → Generate → Validate → Hashtags → Finalize)
- ✅ **Services** - Gemini & Twitter integration
- ✅ **Storage** - JSON-based tweet history

## 🚀 Getting Started

### Step 1: Install Backend Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Configure Backend API Keys

Edit `backend/.env` file with your actual API keys:

```bash
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_actual_gemini_key

# Get from: https://developer.twitter.com/
TWITTER_API_KEY=your_actual_key
TWITTER_API_SECRET=your_actual_secret
TWITTER_ACCESS_TOKEN=your_actual_token
TWITTER_ACCESS_TOKEN_SECRET=your_actual_token_secret

CORS_ORIGINS=http://localhost:3000
PORT=8000
```

### Step 3: Run Backend

```bash
# Make sure you're in backend/ and venv is activated
python main.py
```

Backend will run on: http://localhost:8000

### Step 4: Install Frontend Dependencies

Open a **new terminal**:

```bash
cd frontend
npm install
npm install tailwindcss-animate
```

### Step 5: Configure Frontend

Create `frontend/.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 6: Run Frontend

```bash
# In frontend directory
npm run dev
```

Frontend will run on: http://localhost:3000

## 🧪 Testing the Application

1. Open http://localhost:3000
2. Enter a prompt: "Write about AI transforming education"
3. Click "Generate Tweet"
4. Watch the agent work through the steps
5. Review the generated tweet with hashtags
6. Click "Post to Twitter" (make sure you have valid Twitter API keys)
7. Check your tweet history

## 📝 Important Notes

### If you don't have API keys yet:

**Gemini API (Free):**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env`

**Twitter API (Free Tier):**
1. Go to https://developer.twitter.com/
2. Create an account and project
3. Create an app with "Read and Write" permissions
4. Generate API keys and tokens
5. Copy all 4 credentials into `.env`

### Common Issues:

**Backend won't start:**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Check all dependencies installed: `pip install -r requirements.txt`
- Verify Python version: `python3 --version` (should be 3.9+)

**Frontend errors:**
- Run `npm install` in frontend directory
- Make sure `.env.local` exists with correct API URL
- Check backend is running on port 8000

**Import errors in Python:**
- Make sure you're running from `backend/` directory
- Virtual environment must be activated

## 📚 Project Structure

```
backend/
├── agent/              # LangGraph agent (the AI brain)
│   ├── graph.py       # Agent state machine
│   ├── nodes.py       # Agent steps (plan, generate, validate, etc.)
│   ├── state.py       # Agent state schema
│   └── tools.py       # Helper functions
├── services/
│   ├── gemini_service.py    # Gemini API integration
│   └── twitter_service.py   # Twitter API integration
├── storage/
│   └── tweet_storage.py     # JSON file storage
├── main.py            # FastAPI server
└── requirements.txt

frontend/
├── app/
│   ├── page.tsx       # Main page
│   └── layout.tsx     # Root layout
├── components/
│   ├── TweetGenerator.tsx   # Main form
│   ├── TweetPreview.tsx     # Preview card
│   └── TweetHistory.tsx     # History list
└── lib/
    └── api.ts         # API client
```

## 🎯 How the Agent Works

When you click "Generate Tweet":

1. **Plan Node** - Analyzes your prompt
2. **Generate Node** - Calls Gemini to create content
3. **Validate Node** - Checks character count and quality
4. **Hashtag Node** - Generates relevant hashtags
5. **Finalize Node** - Combines content with hashtags

All of this happens automatically using LangGraph's state machine!

## 🔥 Next Steps

Once everything works:

1. **Learn the code** - Read through the agent logic in `backend/agent/`
2. **Customize prompts** - Edit `backend/prompts/templates.py`
3. **Add features** - Try adding image generation, scheduling, etc.
4. **Deploy** - Use the PLAN.md deployment guide for Render + Vercel

## 💡 Tips for Learning

- **Python async/await** is just like Node.js
- **FastAPI** feels like Express.js
- **LangGraph** is like a state machine with AI
- **Pydantic** models are like TypeScript types

## 🆘 Need Help?

Check:
- `PLAN.md` - Detailed implementation plan
- `README.md` - Full documentation
- Backend logs - Run with `python main.py` to see agent steps
- Browser console - Check for frontend errors

---

**Ready to run!** 🚀

Start both servers and open http://localhost:3000


