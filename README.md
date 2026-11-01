# Career Mentor Agent (with Claude LLM)

## Run it (2 terminals)

### Terminal 1 - Backend
    cd backend
    python -m venv venv
    venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Mac/Linux)
    pip install -r requirements.txt
    copy .env.example .env         (Windows)   |   cp .env.example .env       (Mac/Linux)
    # open .env and paste your ANTHROPIC_API_KEY
    python app.py

### Terminal 2 - Frontend
    cd frontend
    npm install
    npm run dev

Open the link Vite prints (usually http://localhost:5173) -> click "Talk to Mentor".

Check the LLM is on: http://127.0.0.1:5000/api/health  ->  "llm_enabled": true

## What changed
- backend/llm_mentor.py  (NEW)  talks to Claude
- backend/app.py                new POST /api/chat endpoint
- backend/requirements.txt      + anthropic, python-dotenv
- backend/.env.example  (NEW)   where your API key goes
- frontend/src/App.jsx          Mentor chat now calls /api/chat (old keyword answers kept as fallback)
- frontend/src/index.css        typing-dots animation
