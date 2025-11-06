# Mataroo.com

An AI-powered social media content generator that creates engaging posts using agentic AI workflows. Generate and publish content across multiple platforms with intelligent automation.

## Features

- 🤖 **Agentic AI**: LangGraph-based agent with multi-step workflow
- ✍️ **Content Generation**: Gemini Pro for creative social media content
- 🏷️ **Smart Hashtags**: Automatic hashtag generation
- 🔐 **OAuth 2.0**: Secure Twitter authentication with PKCE
- 🐦 **Multi-Platform**: Twitter, LinkedIn, Reddit support (expanding)
- 📊 **Post History**: Track all your published content
- 👤 **User Authentication**: Supabase-powered auth system
- 🎨 **Modern UI**: Next.js with Tailwind CSS and shadcn/ui

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- LangGraph (Agentic AI)
- Google Gemini Pro
- Tweepy (Twitter API)

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui components

## Project Structure

```
ai-agents-tweet/
├── backend/           # Python backend
│   ├── agent/        # LangGraph agent
│   ├── services/     # Gemini & Twitter services
│   ├── storage/      # JSON storage
│   └── main.py       # FastAPI app
├── frontend/         # Next.js frontend
│   ├── app/         # Pages
│   ├── components/  # React components
│   └── lib/         # API client
└── docs/            # Documentation
    ├── BACKEND_DOCUMENTATION.md
    ├── PLAN.md
    ├── PYTHON_LEARNING_GUIDE.md
    ├── SETUP.md
    ├── TWITTER_OAUTH_SETUP.md
    └── TWITTER_POST.md
```

## Setup Instructions

### Backend Setup

1. **Create virtual environment:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Get API Keys:**
   - **Gemini API**: https://makersuite.google.com/app/apikey
   - **Twitter API**: https://developer.twitter.com/

5. **Run the backend:**
   ```bash
   python main.py
   # Server runs on http://localhost:8000
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env.local
   # Update NEXT_PUBLIC_API_URL if needed
   ```

3. **Install Tailwind dependencies:**
   ```bash
   npm install tailwindcss-animate
   ```

4. **Run the frontend:**
   ```bash
   npm run dev
   # App runs on http://localhost:3000
   ```

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a prompt (e.g., "Write about AI and creativity")
3. Click "Generate Tweet"
4. Review the generated content with hashtags
5. Click "Post to Twitter" to publish
6. View your posted tweet and history

## API Endpoints

### Backend API

- `GET /` - API info
- `GET /health` - Health check
- `POST /api/generate` - Generate tweet from prompt
- `POST /api/post` - Post tweet to Twitter
- `GET /api/history` - Get tweet history

## Environment Variables

### Backend (.env)
```bash
GEMINI_API_KEY=your_gemini_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
CORS_ORIGINS=http://localhost:3000
PORT=8000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deployment

### Backend (Render)
1. Push code to GitHub
2. Create Web Service on Render
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Frontend (Vercel)
1. Push code to GitHub
2. Import project in Vercel
3. Set root directory: `frontend`
4. Add `NEXT_PUBLIC_API_URL` environment variable
5. Deploy

## Documentation

For detailed documentation, see the `docs/` folder:

- **[SETUP.md](docs/SETUP.md)** - Detailed setup instructions
- **[BACKEND_DOCUMENTATION.md](docs/BACKEND_DOCUMENTATION.md)** - Backend architecture and API reference
- **[PLAN.md](docs/PLAN.md)** - Project implementation plan
- **[PYTHON_LEARNING_GUIDE.md](docs/PYTHON_LEARNING_GUIDE.md)** - Python learning resources
- **[TWITTER_OAUTH_SETUP.md](docs/TWITTER_OAUTH_SETUP.md)** - Twitter OAuth configuration
- **[TWITTER_POST.md](docs/TWITTER_POST.md)** - Twitter posting guide

## Learning Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Gemini API](https://ai.google.dev/)
- [Twitter API](https://developer.twitter.com/en/docs)

## License

MIT

## Author

Built with ❤️ using AI Agents

source venv/bin/activate && python3 main.py
 source venv/bin/activate && pip install -r requirements.txt