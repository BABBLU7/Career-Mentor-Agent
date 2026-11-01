# 🚀 Career Mentor Agent

An AI-powered Career Mentor that helps students explore career opportunities, understand technical concepts, and receive personalized guidance through an intelligent conversational assistant.

<p align="center">
  <a href="https://career-mentor-agent-82bl.onrender.com">
    <strong>🌐 Live Website — Try Career Mentor Agent</strong>
  </a>
</p>

## 📌 About the Project

Career Mentor Agent is an AI-powered web application designed to make career guidance and learning more accessible.

It combines a modern React frontend, a Python Flask backend, and Google's Gemini AI to provide interactive conversations, career recommendations, and explanations of academic and technical topics.

## ✨ Key Features

- **AI-Powered Chatbot:** Interactive conversations powered by Google Gemini.
- **Career Guidance:** Explore career options and receive guidance based on your interests.
- **Career Recommendations:** Discover relevant career pathways.
- **Technical Learning Support:** Ask questions about programming, computer science, and other technical subjects.
- **Modern User Interface:** Responsive frontend built with React.
- **REST API Integration:** Frontend and backend communicate through Flask APIs.

## 🌐 Live Demo

**Try the application here:**

https://career-mentor-agent.onrender.com

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | React.js |
| Build Tool | Vite |
| Backend | Python, Flask |
| AI Integration | Google Gemini API |
| API Communication | REST API |
| Package Management | npm, pip |
| Version Control | Git, GitHub |
| Deployment | Render |

## 🏗️ Project Architecture

```text
Career-Mentor-Agent/
│
├── backend/
│   ├── app.py
│   ├── career_engine.py
│   ├── llm_mentor.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── setup_project.py
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/BABBLU7/Career-Mentor-Agent.git
cd Career-Mentor-Agent
```

### 2. Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` folder.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Replace `your_gemini_api_key` with your own Google Gemini API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### 4. Start the Backend

```bash
python app.py
```

Backend runs at:

```text
http://127.0.0.1:5000
```

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

Open the frontend URL in your browser.

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome route |
| GET | `/api/health` | Check backend health |
| GET | `/api/pathways` | Retrieve career pathways |
| POST | `/api/recommend` | Generate career recommendations |
| POST | `/api/chat` | Interact with the AI mentor |

## 🔐 Security

- API credentials are stored in environment variables.
- `.env` files are excluded using `.gitignore`.
- Never expose private API keys in source code or public repositories.

## 🎯 Project Objective

The main objective is to build an intelligent career guidance platform that combines conversational AI and career recommendation capabilities to support students in their educational and professional journeys.

## 👨‍💻 Developer

**Babblu Yerra**

B.Tech – Artificial Intelligence and Data Science

GitHub: [@BABBLU7](https://github.com/BABBLU7)

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!

---

<p align="center">
  <strong>Built with ❤️ using React, Flask, Python and Google Gemini AI.</strong>
</p>