# 🎓 Career Mentor Agent

### AI-Powered Career Guidance Platform for Students

Career Mentor Agent is a web-based career guidance platform designed to help students explore suitable career pathways based on their **interests, subjects, strengths, goals, and preferred work style**.

Instead of suggesting careers based only on marks or traditional streams, the system analyzes a student's profile and recommends multiple career pathways with explanations and a practical roadmap.

## 🌐 Live Website

👉 **[Visit Career Mentor Agent](https://career-mentor-agent-82bl.onrender.com)**

## 🚀 Features

* 🎯 Personalized career recommendations
* 🧠 Interest, subject, strength and work-style analysis
* 🛣️ Multiple career pathways
* 📊 Top career matches
* 💡 Explanation for why each pathway matches
* 📅 One-year career action roadmap
* 🔍 Alternative pathways for exploration
* 🗄️ MongoDB database integration
* 🌐 Deployed full-stack web application

## 🧭 Career Pathways

The system currently includes **15 career pathways**, including:

* 🔬 Science + Mathematics (MPC)
* 🧬 Science + Biology (BiPC)
* 💼 Commerce & Business
* 📚 Humanities & Social Sciences
* 🛠️ Diploma / Polytechnic
* 🔧 ITI & Skilled Trades
* 🎨 Design & Creative Careers
* 🎮 Media, Animation & Gaming
* 🌱 Agriculture & Environmental Careers
* 🏨 Hospitality & Tourism
* 🩺 Allied Healthcare
* ⚖️ Law & Legal Careers
* 🏃 Sports & Fitness
* 🚀 Entrepreneurship & Business Building
* 🛡️ Defence & Public Service

## 🧠 How It Works

1. Student enters their basic information.
2. Student selects interests, subjects, strengths and work preferences.
3. The backend analyzes the profile.
4. Each career pathway receives a compatibility score.
5. The system returns the top matches.
6. The student receives explanations and alternative pathways.
7. A one-year roadmap helps the student plan the next steps.

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* Axios
* CSS

### Backend

* Python
* Flask
* Flask-CORS
* Gunicorn

### Database

* MongoDB
* MongoDB Atlas
* PyMongo

### Deployment

* GitHub
* Render

## 📁 Project Structure

```text
Career-Mentor-Agent/
│
├── backend/
│   ├── app.py
│   ├── career_engine.py
│   ├── db.py
│   └── requirements.txt
│
├── database/
│   ├── pathways.json
│   ├── seed_mongodb.py
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── README.md
├── setup_project.py
└── .gitignore
```

## 🔐 Important

Environment variables and database credentials are kept outside the public repository using `.env` files and deployment environment variables.

Never share MongoDB passwords, API keys or other private credentials publicly.

## 🎯 Project Goal

The goal of Career Mentor Agent is to help students understand that choosing a career is not limited to selecting a traditional academic stream.

The platform encourages students to **understand themselves, explore multiple possibilities, compare pathways and take practical next steps**.

---

## 👨‍💻 Project

**Career Mentor Agent**

Built as a full-stack AI-oriented career guidance project using React, Flask and MongoDB.
