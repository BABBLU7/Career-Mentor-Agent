from pathlib import Path

ROOT = Path(__file__).parent

files = {
    "backend/requirements.txt": r"""
Flask==3.1.3
flask-cors==6.0.1
""",

    "backend/app.py": r"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation import generate_recommendations

app = Flask(__name__)
CORS(app)

students = {}

@app.route("/api/health")
def health():
    return jsonify({"status": "success", "message": "Career Mentor API is running"})


@app.route("/api/student", methods=["POST"])
def create_student():
    data = request.json or {}

    student_id = str(len(students) + 1)

    student = {
        "id": student_id,
        "name": data.get("name", ""),
        "age": data.get("age", ""),
        "class_level": data.get("class_level", "10th"),
        "marks": data.get("marks", {}),
        "interests": data.get("interests", []),
        "strengths": data.get("strengths", []),
        "goals": data.get("goals", ""),
        "location": data.get("location", ""),
        "budget": data.get("budget", ""),
    }

    recommendations = generate_recommendations(student)
    student["recommendations"] = recommendations

    students[student_id] = student

    return jsonify(student)


@app.route("/api/student/<student_id>")
def get_student(student_id):
    student = students.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student)


@app.route("/api/reassess/<student_id>", methods=["POST"])
def reassess(student_id):
    student = students.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    updates = request.json or {}

    student.update({
        "interests": updates.get("interests", student["interests"]),
        "strengths": updates.get("strengths", student["strengths"]),
        "goals": updates.get("goals", student["goals"])
    })

    student["recommendations"] = generate_recommendations(student)

    return jsonify(student)


@app.route("/api/mentor", methods=["POST"])
def mentor():
    data = request.json or {}
    message = data.get("message", "").lower()

    if "diploma" in message or "polytechnic" in message:
        reply = (
            "Diploma and Polytechnic are valid alternatives after 10th. "
            "They provide technical and practical education and can lead "
            "towards employment or further higher education."
        )

    elif "iti" in message:
        reply = (
            "ITI is a skill-oriented pathway after 10th. It can be suitable "
            "for students who prefer practical and trade-based learning."
        )

    elif "design" in message or "creative" in message:
        reply = (
            "Creative pathways can include design, animation, UI/UX, "
            "visual communication, fashion, media and related fields. "
            "Portfolio-building is especially important in many of these areas."
        )

    elif "career" in message:
        reply = (
            "I can help you explore different pathways based on your "
            "subjects, interests, strengths and goals. You don't have to "
            "choose only MPC, BiPC, CEC or HEC."
        )

    else:
        reply = (
            "Tell me what you enjoy, what subjects you like, what you are "
            "good at, and what kind of future you imagine. I can then help "
            "you explore suitable education and career pathways."
        )

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
""",

    "backend/recommendation.py": r"""
PATHWAYS = [
    {
        "id": "engineering",
        "name": "Engineering & Technology",
        "category": "Academic",
        "icon": "💻",
        "description": "Technical and engineering-oriented education leading to technology and engineering careers.",
        "keywords": ["technology", "computers", "maths", "science", "problem solving", "engineering"],
        "routes": ["Intermediate / equivalent science route", "Diploma / Polytechnic", "Degree"],
        "careers": ["Software Developer", "Engineer", "Data Professional", "Cybersecurity Professional"],
        "skills": ["Mathematics", "Programming", "Problem Solving", "Technical Skills"]
    },
    {
        "id": "medical",
        "name": "Healthcare & Life Sciences",
        "category": "Academic",
        "icon": "🧬",
        "description": "Healthcare, biology and life-science related education and careers.",
        "keywords": ["biology", "health", "science", "medicine", "helping people"],
        "routes": ["Biology-oriented academic route", "Degree / Professional course"],
        "careers": ["Healthcare Professional", "Pharmacist", "Biotechnologist", "Life Science Professional"],
        "skills": ["Biology", "Scientific Thinking", "Communication", "Discipline"]
    },
    {
        "id": "commerce",
        "name": "Business & Finance",
        "category": "Academic",
        "icon": "📊",
        "description": "Business, finance, accounting, economics and management pathways.",
        "keywords": ["business", "finance", "commerce", "economics", "numbers", "management"],
        "routes": ["Commerce-oriented academic route", "Degree / Professional course"],
        "careers": ["Accountant", "Financial Analyst", "Business Professional", "Entrepreneur"],
        "skills": ["Numeracy", "Finance", "Communication", "Business Thinking"]
    },
    {
        "id": "humanities",
        "name": "Humanities, Law & Social Sciences",
        "category": "Academic",
        "icon": "⚖️",
        "description": "Humanities, law, psychology, social sciences and communication-related pathways.",
        "keywords": ["history", "society", "law", "writing", "people", "psychology", "communication"],
        "routes": ["Humanities-oriented academic route", "Degree / Professional course"],
        "careers": ["Law Professional", "Psychology Professional", "Civil Services Aspirant", "Researcher"],
        "skills": ["Writing", "Communication", "Critical Thinking", "Research"]
    },
    {
        "id": "diploma",
        "name": "Diploma & Polytechnic",
        "category": "Alternative",
        "icon": "🔧",
        "description": "Practical technical education for students who prefer hands-on and skill-oriented learning.",
        "keywords": ["technical", "hands on", "practical", "machines", "computers", "engineering"],
        "routes": ["Diploma / Polytechnic", "Lateral entry options may be available depending on rules"],
        "careers": ["Technician", "Technical Professional", "Junior Engineer", "IT Professional"],
        "skills": ["Practical Skills", "Technical Skills", "Problem Solving", "Hands-on Learning"]
    },
    {
        "id": "iti",
        "name": "ITI & Skilled Trades",
        "category": "Alternative",
        "icon": "🛠️",
        "description": "Trade and skill-based education focused on practical occupational skills.",
        "keywords": ["hands on", "trade", "practical", "machines", "repair", "technical"],
        "routes": ["ITI / Trade Training", "Apprenticeship / Employment"],
        "careers": ["Electrician", "Fitter", "Technician", "Mechanic", "Trade Professional"],
        "skills": ["Practical Skills", "Technical Skills", "Safety", "Discipline"]
    },
    {
        "id": "design",
        "name": "Design & Creative Careers",
        "category": "Creative",
        "icon": "🎨",
        "description": "Creative careers involving visual thinking, design, media and digital creativity.",
        "keywords": ["art", "drawing", "design", "creative", "animation", "fashion", "media"],
        "routes": ["Design Diploma / Degree", "Portfolio-based learning"],
        "careers": ["UI/UX Designer", "Graphic Designer", "Animator", "Fashion Professional", "Creative Professional"],
        "skills": ["Creativity", "Design", "Communication", "Portfolio Building"]
    },
    {
        "id": "media",
        "name": "Media & Communication",
        "category": "Creative",
        "icon": "🎥",
        "description": "Journalism, content, digital media, communication and production-related pathways.",
        "keywords": ["media", "writing", "communication", "video", "content", "storytelling"],
        "routes": ["Media Diploma / Degree", "Portfolio / Practical learning"],
        "careers": ["Content Creator", "Journalist", "Video Professional", "Communication Professional"],
        "skills": ["Communication", "Writing", "Storytelling", "Digital Media"]
    },
    {
        "id": "defence",
        "name": "Defence & Public Service",
        "category": "Service",
        "icon": "🛡️",
        "description": "Career exploration for students interested in defence, discipline and public service.",
        "keywords": ["defence", "army", "discipline", "fitness", "service", "public service"],
        "routes": ["Academic route + eligibility preparation", "Relevant recruitment pathways"],
        "careers": ["Defence Career", "Public Service Career"],
        "skills": ["Discipline", "Fitness", "Leadership", "Teamwork"]
    },
    {
        "id": "sports",
        "name": "Sports & Fitness",
        "category": "Specialized",
        "icon": "⚽",
        "description": "Sports, fitness, coaching and physical performance related pathways.",
        "keywords": ["sports", "fitness", "football", "cricket", "athletics", "physical"],
        "routes": ["Sports training", "Sports education / certification"],
        "careers": ["Athlete", "Coach", "Fitness Professional", "Sports Manager"],
        "skills": ["Fitness", "Discipline", "Teamwork", "Performance"]
    },
    {
        "id": "aviation",
        "name": "Aviation & Travel",
        "category": "Specialized",
        "icon": "✈️",
        "description": "Aviation, airport services, travel and related career areas.",
        "keywords": ["aviation", "airport", "travel", "aircraft", "hospitality"],
        "routes": ["Relevant diploma / degree / training", "Role-specific qualification"],
        "careers": ["Aviation Professional", "Airport Operations", "Travel Professional"],
        "skills": ["Communication", "Customer Service", "Discipline", "English"]
    },
    {
        "id": "hospitality",
        "name": "Hospitality & Tourism",
        "category": "Service",
        "icon": "🏨",
        "description": "Hospitality, tourism, food service and customer experience careers.",
        "keywords": ["hospitality", "hotel", "travel", "food", "tourism", "people"],
        "routes": ["Hospitality Diploma / Degree", "Skill-based training"],
        "careers": ["Hotel Professional", "Chef", "Travel Professional", "Event Professional"],
        "skills": ["Communication", "Customer Service", "Organization", "Teamwork"]
    },
    {
        "id": "agriculture",
        "name": "Agriculture & Environmental Careers",
        "category": "Specialized",
        "icon": "🌱",
        "description": "Agriculture, environmental science, food and rural technology pathways.",
        "keywords": ["agriculture", "plants", "environment", "nature", "farming", "biology"],
        "routes": ["Agriculture-related education", "Diploma / Degree / Skill training"],
        "careers": ["Agriculture Professional", "Environmental Professional", "Agri Entrepreneur"],
        "skills": ["Scientific Thinking", "Observation", "Problem Solving", "Field Skills"]
    },
    {
        "id": "entrepreneurship",
        "name": "Entrepreneurship & Business Building",
        "category": "Independent",
        "icon": "🚀",
        "description": "For students interested in building businesses, products or independent careers.",
        "keywords": ["business", "entrepreneurship", "startup", "leadership", "selling", "innovation"],
        "routes": ["Any suitable academic/skill route + business learning"],
        "careers": ["Entrepreneur", "Startup Founder", "Business Owner"],
        "skills": ["Leadership", "Communication", "Finance", "Problem Solving"]
    }
]


def generate_recommendations(student):
    interests = [x.lower() for x in student.get("interests", [])]
    strengths = [x.lower() for x in student.get("strengths", [])]
    goals = student.get("goals", "").lower()

    text = " ".join(interests + strengths + [goals])

    scored = []

    for pathway in PATHWAYS:
        score = 0

        for keyword in pathway["keywords"]:
            if keyword in text:
                score += 2

        if score == 0:
            score = 1

        scored.append({
            **pathway,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    max_score = scored[0]["score"] if scored else 1

    for item in scored:
        item["match"] = min(
            95,
            max(45, round((item["score"] / max_score) * 92))
        )

        if item["score"] > 1:
            item["reason"] = (
                "This pathway matches some of the interests, strengths "
                "or goals provided in your assessment."
            )
        else:
            item["reason"] = (
                "This is an alternative pathway worth exploring before "
                "making a final decision."
            )

    return scored
""",

    "frontend/package.json": r"""
{
  "name": "career-mentor-agent",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "^5.0.4",
    "axios": "^1.12.2",
    "lucide-react": "^0.468.0",
    "react": "^19.1.1",
    "react-dom": "^19.1.1"
  },
  "devDependencies": {
    "vite": "^7.1.7"
  }
}
""",

    "frontend/vite.config.js": r"""
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  }
});
""",

    "frontend/index.html": r"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#172554" />
    <title>Career Mentor Agent</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",

    "frontend/src/main.jsx": r"""
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",

    "frontend/src/App.jsx": r"""
import { useState } from "react";
import axios from "axios";
import {
  ArrowRight,
  Award,
  BarChart3,
  Bot,
  CheckCircle2,
  ChevronRight,
  Compass,
  GraduationCap,
  Heart,
  Lightbulb,
  Map,
  MessageCircle,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  UserRound,
  Wrench,
  X
} from "lucide-react";

const API = "http://127.0.0.1:5000/api";

const interests = [
  "Technology",
  "Science",
  "Business",
  "Creativity",
  "Design",
  "Sports",
  "Helping People",
  "Writing",
  "Communication",
  "Machines",
  "Nature",
  "Travel",
  "Leadership",
  "Entrepreneurship",
  "Defence",
  "Media"
];

const strengths = [
  "Problem Solving",
  "Mathematics",
  "Communication",
  "Creativity",
  "Teamwork",
  "Leadership",
  "Practical Skills",
  "Analytical Thinking",
  "Writing",
  "Discipline",
  "Observation",
  "Technology"
];

const fallbackPaths = [
  {
    id: "engineering",
    name: "Engineering & Technology",
    category: "Academic",
    icon: "💻",
    description: "Technical and engineering-oriented education and careers.",
    match: 88,
    careers: ["Software Developer", "Engineer", "Data Professional"]
  },
  {
    id: "diploma",
    name: "Diploma & Polytechnic",
    category: "Alternative",
    icon: "🔧",
    description: "Practical technical education with hands-on learning.",
    match: 81,
    careers: ["Technician", "Technical Professional", "IT Professional"]
  },
  {
    id: "design",
    name: "Design & Creative Careers",
    category: "Creative",
    icon: "🎨",
    description: "Design, digital creativity, animation and visual careers.",
    match: 76,
    careers: ["UI/UX Designer", "Graphic Designer", "Animator"]
  }
];

function App() {
  const [screen, setScreen] = useState("welcome");
  const [student, setStudent] = useState(null);
  const [selectedPath, setSelectedPath] = useState(null);
  const [mentorOpen, setMentorOpen] = useState(false);

  const handleAssessment = (data) => {
    setStudent(data);
    setScreen("dashboard");
  };

  return (
    <div className="app-shell">
      {screen !== "welcome" && (
        <Sidebar screen={screen} setScreen={setScreen} />
      )}

      <main className={screen === "welcome" ? "main full" : "main"}>
        {screen === "welcome" && <Welcome onStart={() => setScreen("assessment")} />}
        {screen === "assessment" && (
          <Assessment onComplete={handleAssessment} />
        )}
        {screen === "dashboard" && (
          <Dashboard
            student={student}
            onExplore={() => setScreen("explorer")}
            onRoadmap={() => setScreen("roadmap")}
            onReassess={() => setScreen("assessment")}
          />
        )}
        {screen === "explorer" && (
          <Explorer
            student={student}
            selectedPath={selectedPath}
            setSelectedPath={setSelectedPath}
          />
        )}
        {screen === "roadmap" && <Roadmap student={student} />}
        {screen === "progress" && <Progress />}
        {screen === "reassessment" && (
          <Reassessment onComplete={() => setScreen("dashboard")} />
        )}
      </main>

      {screen !== "welcome" && (
        <button className="mentor-fab" onClick={() => setMentorOpen(true)}>
          <Bot size={21} />
          <span>Ask Mentor</span>
        </button>
      )}

      {mentorOpen && <Mentor onClose={() => setMentorOpen(false)} />}
    </div>
  );
}

function Sidebar({ screen, setScreen }) {
  const items = [
    ["dashboard", "Dashboard", BarChart3],
    ["explorer", "Career Explorer", Compass],
    ["roadmap", "My Roadmap", Map],
    ["progress", "Progress", TrendingUp],
    ["reassessment", "Reassess", RefreshCw]
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">
          <Sparkles size={21} />
        </div>
        <div>
          <strong>CareerMentor</strong>
          <span>AI Guidance</span>
        </div>
      </div>

      <div className="sidebar-label">YOUR JOURNEY</div>

      <nav>
        {items.map(([id, label, Icon]) => (
          <button
            key={id}
            className={`nav-item ${screen === id ? "active" : ""}`}
            onClick={() => setScreen(id)}
          >
            <Icon size={19} />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="privacy-card">
          <ShieldCheck size={20} />
          <div>
            <strong>Private by design</strong>
            <p>Your profile is used to personalize guidance.</p>
          </div>
        </div>

        <div className="mini-profile">
          <div className="avatar">S</div>
          <div>
            <strong>Student</strong>
            <span>10th Class</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

function Welcome({ onStart }) {
  return (
    <section className="welcome">
      <div className="welcome-glow glow-one"></div>
      <div className="welcome-glow glow-two"></div>

      <div className="welcome-content">
        <div className="eyebrow">
          <Sparkles size={16} />
          AI-POWERED CAREER GUIDANCE
        </div>

        <h1>
          Your career journey
          <br />
          <span>starts after 10th.</span>
        </h1>

        <p className="hero-copy">
          Explore academic and alternative pathways, understand your options,
          build a roadmap and keep adapting as your interests grow.
        </p>

        <button className="primary-btn large" onClick={onStart}>
          Start my journey
          <ArrowRight size={19} />
        </button>

        <div className="trust-row">
          <div><CheckCircle2 size={16} /> Multiple pathways</div>
          <div><CheckCircle2 size={16} /> Personalized roadmap</div>
          <div><CheckCircle2 size={16} /> Continuous guidance</div>
        </div>
      </div>

      <div className="hero-preview">
        <div className="preview-window">
          <div className="preview-top">
            <span></span><span></span><span></span>
          </div>

          <div className="preview-body">
            <div className="preview-title">
              <div>
                <small>YOUR CAREER EXPLORATION</small>
                <h3>Good evening, Student 👋</h3>
              </div>
              <div className="preview-avatar">S</div>
            </div>

            <div className="preview-stat-row">
              <div>
                <small>PROFILE</small>
                <strong>85%</strong>
              </div>
              <div>
                <small>PATHWAYS</small>
                <strong>14+</strong>
              </div>
              <div>
                <small>ROADMAP</small>
                <strong>Ready</strong>
              </div>
            </div>

            <div className="preview-card">
              <div className="preview-card-icon">💻</div>
              <div>
                <small>TOP MATCH</small>
                <strong>Engineering & Technology</strong>
                <span>Explore why this may fit you →</span>
              </div>
              <b>88%</b>
            </div>

            <div className="preview-card">
              <div className="preview-card-icon">🎨</div>
              <div>
                <small>ALTERNATIVE</small>
                <strong>Design & Creative Careers</strong>
                <span>Portfolio-focused pathway</span>
              </div>
              <b>76%</b>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Assessment({ onComplete }) {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    name: "",
    age: "",
    location: "",
    marks: "",
    interests: [],
    strengths: [],
    goals: ""
  });

  const toggle = (field, value) => {
    setForm((old) => ({
      ...old,
      [field]: old[field].includes(value)
        ? old[field].filter((x) => x !== value)
        : [...old[field], value]
    }));
  };

  const finish = async () => {
    try {
      const response = await axios.post(`${API}/student`, {
        name: form.name,
        age: form.age,
        location: form.location,
        marks: { overall: form.marks },
        interests: form.interests,
        strengths: form.strengths,
        goals: form.goals
      });

      onComplete(response.data);
    } catch {
      onComplete({
        ...form,
        recommendations: fallbackPaths
      });
    }
  };

  return (
    <section className="assessment-page">
      <div className="assessment-header">
        <div>
          <div className="eyebrow">STEP {step} OF 3</div>
          <h1>Let's understand you.</h1>
          <p>There is no right or wrong answer. Be honest about what interests you.</p>
        </div>

        <div className="progress-track">
          <div style={{ width: `${(step / 3) * 100}%` }}></div>
        </div>
      </div>

      <div className="assessment-card">
        {step === 1 && (
          <>
            <div className="section-icon blue"><UserRound /></div>
            <h2>Tell us about yourself</h2>
            <p className="section-subtitle">We'll use this only to personalize your journey.</p>

            <div className="form-grid">
              <Field label="Your name">
                <input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Enter your name"
                />
              </Field>

              <Field label="Age">
                <input
                  value={form.age}
                  onChange={(e) => setForm({ ...form, age: e.target.value })}
                  placeholder="e.g. 15"
                  type="number"
                />
              </Field>

              <Field label="Location">
                <input
                  value={form.location}
                  onChange={(e) => setForm({ ...form, location: e.target.value })}
                  placeholder="City / State"
                />
              </Field>

              <Field label="10th overall marks (optional)">
                <input
                  value={form.marks}
                  onChange={(e) => setForm({ ...form, marks: e.target.value })}
                  placeholder="e.g. 82%"
                />
              </Field>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <div className="section-icon purple"><Heart /></div>
            <h2>What interests you?</h2>
            <p className="section-subtitle">
              Select everything that genuinely sounds interesting.
            </p>

            <div className="chip-grid">
              {interests.map((item) => (
                <button
                  key={item}
                  className={`choice-chip ${form.interests.includes(item) ? "selected" : ""}`}
                  onClick={() => toggle("interests", item)}
                >
                  {form.interests.includes(item) && <CheckCircle2 size={16} />}
                  {item}
                </button>
              ))}
            </div>
          </>
        )}

        {step === 3 && (
          <>
            <div className="section-icon orange"><Lightbulb /></div>
            <h2>What are you naturally good at?</h2>
            <p className="section-subtitle">
              Choose your strengths, then tell us what kind of future you imagine.
            </p>

            <div className="chip-grid">
              {strengths.map((item) => (
                <button
                  key={item}
                  className={`choice-chip ${form.strengths.includes(item) ? "selected" : ""}`}
                  onClick={() => toggle("strengths", item)}
                >
                  {form.strengths.includes(item) && <CheckCircle2 size={16} />}
                  {item}
                </button>
              ))}
            </div>

            <Field label="What do you want from your future?">
              <textarea
                value={form.goals}
                onChange={(e) => setForm({ ...form, goals: e.target.value })}
                placeholder="Example: I want a practical career where I can build things..."
                rows="4"
              />
            </Field>
          </>
        )}

        <div className="assessment-actions">
          {step > 1 ? (
            <button className="secondary-btn" onClick={() => setStep(step - 1)}>
              Back
            </button>
          ) : <span></span>}

          {step < 3 ? (
            <button className="primary-btn" onClick={() => setStep(step + 1)}>
              Continue <ChevronRight size={18} />
            </button>
          ) : (
            <button className="primary-btn" onClick={finish}>
              Build my career map <Sparkles size={18} />
            </button>
          )}
        </div>
      </div>
    </section>
  );
}

function Field({ label, children }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

function Dashboard({ student, onExplore, onRoadmap, onReassess }) {
  const name = student?.name || "Student";
  const paths = student?.recommendations?.slice(0, 3) || fallbackPaths;

  return (
    <div className="page">
      <Header
        eyebrow="YOUR CAREER JOURNEY"
        title={`Good evening, ${name} 👋`}
        subtitle="Your future is a journey. Let's explore it one step at a time."
      />

      <div className="dashboard-grid">
        <div className="hero-card">
          <div className="hero-card-content">
            <div className="eyebrow light">YOUR NEXT STEP</div>
            <h2>Explore before you decide.</h2>
            <p>
              You don't have to choose a single career today. Compare different
              pathways and understand where each one can take you.
            </p>
            <button className="white-btn" onClick={onExplore}>
              Explore pathways <ArrowRight size={18} />
            </button>
          </div>
          <div className="hero-orbit">
            <div className="orbit-center">🧭</div>
            <div className="orbit-item one">💻</div>
            <div className="orbit-item two">🎨</div>
            <div className="orbit-item three">🚀</div>
            <div className="orbit-item four">🛠️</div>
          </div>
        </div>

        <div className="stats-grid">
          <StatCard icon={<UserRound />} label="Profile" value="85%" />
          <StatCard icon={<Compass />} label="Pathways found" value="14+" />
          <StatCard icon={<Target />} label="Roadmap" value="Ready" />
          <StatCard icon={<Award />} label="Progress" value="12%" />
        </div>
      </div>

      <section className="section-block">
        <div className="section-heading">
          <div>
            <div className="eyebrow">PERSONALIZED FOR YOU</div>
            <h2>Pathways to explore</h2>
          </div>
          <button className="text-btn" onClick={onExplore}>
            View all <ArrowRight size={17} />
          </button>
        </div>

        <div className="path-grid">
          {paths.map((path) => <PathCard key={path.id} path={path} />)}
        </div>
      </section>

      <div className="bottom-grid">
        <div className="roadmap-preview">
          <div className="section-heading">
            <div>
              <div className="eyebrow">YOUR ROADMAP</div>
              <h2>Start building your future</h2>
            </div>
            <button className="icon-btn" onClick={onRoadmap}>
              <ArrowRight size={18} />
            </button>
          </div>

          <div className="timeline">
            <TimelineItem done title="Complete career assessment" />
            <TimelineItem active title="Explore and compare pathways" />
            <TimelineItem title="Choose an education direction" />
            <TimelineItem title="Build skills and projects" />
          </div>
        </div>

        <div className="reassess-card">
          <div className="reassess-icon"><RefreshCw /></div>
          <h3>Things can change.</h3>
          <p>
            Your interests may change as you learn. Reassess anytime and let
            your roadmap adapt.
          </p>
          <button className="secondary-btn full-btn" onClick={onReassess}>
            Reassess my interests
          </button>
        </div>
      </div>
    </div>
  );
}

function Header({ eyebrow, title, subtitle }) {
  return (
    <header className="page-header">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      <div className="header-avatar">S</div>
    </header>
  );
}

function StatCard({ icon, label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function PathCard({ path, large = false }) {
  return (
    <div className={`path-card ${large ? "large" : ""}`}>
      <div className="path-top">
        <div className="path-icon">{path.icon}</div>
        <span className="category-pill">{path.category}</span>
      </div>

      <h3>{path.name}</h3>
      <p>{path.description}</p>

      <div className="match-row">
        <div>
          <span>Pathway match</span>
          <strong>{path.match}%</strong>
        </div>
        <div className="match-bar">
          <span style={{ width: `${path.match}%` }}></span>
        </div>
      </div>

      <div className="path-footer">
        <span>Explore pathway</span>
        <ChevronRight size={18} />
      </div>
    </div>
  );
}

function Explorer({ student, selectedPath, setSelectedPath }) {
  const paths = student?.recommendations?.length
    ? student.recommendations
    : fallbackPaths;

  return (
    <div className="page">
      <Header
        eyebrow="CAREER EXPLORER"
        title="You have more than one path."
        subtitle="Explore academic, technical, creative and skill-based pathways."
      />

      <div className="explorer-tools">
        <div className="search-box">
          <Search size={19} />
          <input placeholder="Search pathways, skills or careers..." />
        </div>

        <div className="filter-pills">
          <button className="filter active">All</button>
          <button className="filter">Academic</button>
          <button className="filter">Alternative</button>
          <button className="filter">Creative</button>
        </div>
      </div>

      <div className="explorer-layout">
        <div className="explorer-grid">
          {paths.map((path) => (
            <button
              className="path-button"
              key={path.id}
              onClick={() => setSelectedPath(path)}
            >
              <PathCard path={path} large />
            </button>
          ))}
        </div>

        {selectedPath && (
          <div className="detail-panel">
            <button className="close-detail" onClick={() => setSelectedPath(null)}>
              <X size={18} />
            </button>

            <div className="detail-icon">{selectedPath.icon}</div>
            <div className="eyebrow">{selectedPath.category}</div>
            <h2>{selectedPath.name}</h2>
            <p>{selectedPath.description}</p>

            <div className="detail-section">
              <h4>Possible routes</h4>
              {(selectedPath.routes || []).map((x) => (
                <div className="detail-line" key={x}>
                  <CheckCircle2 size={17} /> {x}
                </div>
              ))}
            </div>

            <div className="detail-section">
              <h4>Possible careers</h4>
              <div className="career-tags">
                {(selectedPath.careers || []).map((x) => (
                  <span key={x}>{x}</span>
                ))}
              </div>
            </div>

            <div className="why-box">
              <Lightbulb size={19} />
              <div>
                <strong>Why explore this?</strong>
                <p>
                  {selectedPath.reason ||
                    "This pathway is one of the options available based on your profile."}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Roadmap() {
  const steps = [
    ["01", "Understand yourself", "Complete your profile, interests and aptitude assessment.", true],
    ["02", "Explore pathways", "Compare education and career directions before choosing.", true],
    ["03", "Choose a direction", "Select a pathway while keeping alternative routes visible.", false],
    ["04", "Build your skills", "Learn relevant skills through courses, practice and projects.", false],
    ["05", "Gain experience", "Build a portfolio, participate in activities and seek opportunities.", false],
    ["06", "Reassess & adapt", "Review your goals and update your roadmap as you grow.", false]
  ];

  return (
    <div className="page">
      <Header
        eyebrow="MY ROADMAP"
        title="A roadmap that can change with you."
        subtitle="Your plan is a guide, not a permanent decision."
      />

      <div className="roadmap-banner">
        <div>
          <div className="eyebrow light">CURRENT JOURNEY</div>
          <h2>From 10th class to your future career</h2>
          <p>
            We'll keep your options open while turning your goals into practical milestones.
          </p>
        </div>
        <div className="roadmap-progress">
          <strong>2 / 6</strong>
          <span>milestones explored</span>
          <div><i></i></div>
        </div>
      </div>

      <div className="roadmap-list">
        {steps.map(([number, title, text, done]) => (
          <div className={`roadmap-step ${done ? "done" : ""}`} key={number}>
            <div className="step-number">{done ? <CheckCircle2 size={20} /> : number}</div>
            <div className="step-content">
              <span>MILESTONE {number}</span>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
            <ChevronRight size={20} className="step-arrow" />
          </div>
        ))}
      </div>
    </div>
  );
}

function Progress() {
  return (
    <div className="page">
      <Header
        eyebrow="PROGRESS"
        title="Keep moving forward."
        subtitle="Your career readiness grows through small, consistent steps."
      />

      <div className="progress-overview">
        <div className="progress-score">
          <div className="score-ring">
            <strong>32%</strong>
            <span>complete</span>
          </div>
          <div>
            <div className="eyebrow">CAREER JOURNEY</div>
            <h2>You're getting started.</h2>
            <p>Complete the next milestones to make your roadmap more useful.</p>
          </div>
        </div>

        <div className="progress-bars">
          <ProgressBar label="Profile" value={85} />
          <ProgressBar label="Career exploration" value={55} />
          <ProgressBar label="Skills" value={20} />
          <ProgressBar label="Projects" value={0} />
        </div>
      </div>

      <div className="section-heading standalone">
        <div>
          <div className="eyebrow">NEXT ACTIONS</div>
          <h2>What you can do now</h2>
        </div>
      </div>

      <div className="action-grid">
        <ActionCard icon={<Compass />} title="Explore 3 pathways" text="Compare different options before deciding." />
        <ActionCard icon={<Wrench />} title="Start a small project" text="Try something practical related to an interest." />
        <ActionCard icon={<MessageCircle />} title="Talk to your mentor" text="Ask questions when you're unsure." />
      </div>
    </div>
  );
}

function ProgressBar({ label, value }) {
  return (
    <div className="progress-item">
      <div><span>{label}</span><strong>{value}%</strong></div>
      <div className="bar"><span style={{ width: `${value}%` }}></span></div>
    </div>
  );
}

function ActionCard({ icon, title, text }) {
  return (
    <div className="action-card">
      <div className="action-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{text}</p>
      <ChevronRight size={18} />
    </div>
  );
}

function TimelineItem({ title, done, active }) {
  return (
    <div className={`timeline-item ${done ? "done" : ""} ${active ? "active" : ""}`}>
      <div className="timeline-dot">
        {done ? <CheckCircle2 size={17} /> : active ? <span></span> : null}
      </div>
      <span>{title}</span>
    </div>
  );
}

function Reassessment({ onComplete }) {
  const [selected, setSelected] = useState([]);

  const options = [
    "My interests changed",
    "I discovered a new subject",
    "I want more practical learning",
    "I want a different career direction",
    "I am unsure about my current path"
  ];

  return (
    <div className="page narrow">
      <Header
        eyebrow="REASSESSMENT"
        title="Things can change."
        subtitle="Tell us what's different and we'll help you explore again."
      />

      <div className="assessment-card reassessment-box">
        <div className="section-icon purple"><RefreshCw /></div>
        <h2>What's changed?</h2>
        <p className="section-subtitle">
          You can revisit your career direction whenever your interests or goals change.
        </p>

        <div className="chip-grid">
          {options.map((x) => (
            <button
              key={x}
              className={`choice-chip ${selected.includes(x) ? "selected" : ""}`}
              onClick={() =>
                setSelected(selected.includes(x)
                  ? selected.filter((i) => i !== x)
                  : [...selected, x])
              }
            >
              {selected.includes(x) && <CheckCircle2 size={16} />}
              {x}
            </button>
          ))}
        </div>

        <button className="primary-btn" onClick={onComplete}>
          Rebuild my exploration <RefreshCw size={18} />
        </button>
      </div>
    </div>
  );
}

function Mentor({ onClose }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi! I'm your Career Mentor. Ask me about pathways, diplomas, ITI, careers, skills or anything you're unsure about."
    }
  ]);

  const send = async () => {
    if (!message.trim()) return;

    const current = message;
    setMessages((m) => [...m, { role: "user", text: current }]);
    setMessage("");

    try {
      const response = await axios.post(`${API}/mentor`, { message: current });
      setMessages((m) => [...m, { role: "bot", text: response.data.reply }]);
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "bot",
          text: "I can help you explore different education and career pathways. Try asking about diploma, ITI, design, engineering or career choices."
        }
      ]);
    }
  };

  return (
    <div className="mentor-overlay">
      <div className="mentor-panel">
        <div className="mentor-header">
          <div className="mentor-title">
            <div className="mentor-avatar"><Bot size={21} /></div>
            <div>
              <strong>Career Mentor</strong>
              <span>AI guidance assistant</span>
            </div>
          </div>
          <button className="close-detail" onClick={onClose}><X size={19} /></button>
        </div>

        <div className="chat-body">
          {messages.map((m, i) => (
            <div className={`chat-message ${m.role}`} key={i}>
              {m.text}
            </div>
          ))}
        </div>

        <div className="chat-input">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Ask your mentor..."
          />
          <button onClick={send}><ArrowRight size={18} /></button>
        </div>
      </div>
    </div>
  );
}

export default App;
""",

    "frontend/src/index.css": r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
  font-family: "DM Sans", sans-serif;
  color: #172033;
  background: #f6f8fc;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  background: #f6f8fc;
}

button,
input,
textarea {
  font: inherit;
}

button {
  cursor: pointer;
}

.app-shell {
  min-height: 100vh;
  display: flex;
}

.main {
  margin-left: 248px;
  width: calc(100% - 248px);
  min-height: 100vh;
}

.main.full {
  margin-left: 0;
  width: 100%;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 248px;
  background: #fff;
  border-right: 1px solid #e9edf5;
  padding: 25px 17px;
  display: flex;
  flex-direction: column;
  z-index: 20;
}

.brand {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 3px 9px 30px;
}

.brand-mark {
  width: 39px;
  height: 39px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  color: #fff;
  background: linear-gradient(135deg, #315bea, #7c4dff);
}

.brand strong {
  display: block;
  font-family: "Plus Jakarta Sans";
  font-size: 15px;
}

.brand span {
  display: block;
  color: #8790a3;
  font-size: 11px;
  margin-top: 2px;
}

.sidebar-label {
  color: #a0a7b7;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.3px;
  padding: 0 12px 10px;
}

.nav-item {
  width: 100%;
  border: 0;
  background: transparent;
  color: #697386;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 11px;
  margin: 3px 0;
  text-align: left;
  font-weight: 600;
}

.nav-item:hover {
  background: #f5f7fc;
  color: #2c4dcc;
}

.nav-item.active {
  color: #284bc7;
  background: #edf2ff;
}

.sidebar-bottom {
  margin-top: auto;
}

.privacy-card {
  background: #f7f9fd;
  border: 1px solid #edf0f6;
  border-radius: 14px;
  padding: 13px;
  display: flex;
  gap: 9px;
  color: #647089;
}

.privacy-card svg {
  color: #3c62d7;
  flex-shrink: 0;
}

.privacy-card strong {
  font-size: 11px;
  color: #34415c;
}

.privacy-card p {
  margin: 4px 0 0;
  font-size: 10px;
  line-height: 1.4;
}

.mini-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 17px 7px 0;
}

.avatar,
.header-avatar,
.preview-avatar {
  display: grid;
  place-items: center;
  background: #dfe7ff;
  color: #3152bf;
  font-weight: 800;
}

.avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.mini-profile strong,
.mini-profile span {
  display: block;
}

.mini-profile strong {
  font-size: 12px;
}

.mini-profile span {
  color: #8d96a8;
  font-size: 10px;
  margin-top: 2px;
}

.page {
  padding: 38px 46px 60px;
  max-width: 1500px;
  margin: auto;
}

.page.narrow {
  max-width: 1050px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 30px;
}

.page-header h1,
.assessment-header h1,
.welcome h1 {
  font-family: "Plus Jakarta Sans";
  letter-spacing: -1.3px;
  margin: 7px 0 8px;
  color: #182239;
}

.page-header h1 {
  font-size: 31px;
}

.page-header p,
.assessment-header p {
  color: #7c869a;
  margin: 0;
}

.header-avatar {
  width: 45px;
  height: 45px;
  border-radius: 14px;
}

.eyebrow {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.4px;
  color: #4e64c6;
}

.eyebrow.light {
  color: #cbd7ff;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(270px, 1fr);
  gap: 20px;
}

.hero-card {
  min-height: 285px;
  border-radius: 23px;
  padding: 32px;
  position: relative;
  overflow: hidden;
  color: #fff;
  background:
    radial-gradient(circle at 85% 20%, rgba(117, 135, 255, .38), transparent 30%),
    linear-gradient(125deg, #1d347e, #263e9a 52%, #3c51bd);
}

.hero-card-content {
  position: relative;
  z-index: 2;
  max-width: 490px;
}

.hero-card h2 {
  font-family: "Plus Jakarta Sans";
  font-size: 29px;
  margin: 9px 0;
  letter-spacing: -.8px;
}

.hero-card p {
  color: #d7def8;
  line-height: 1.6;
  max-width: 470px;
}

.white-btn,
.primary-btn,
.secondary-btn,
.text-btn,
.icon-btn {
  border: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 700;
}

.white-btn {
  margin-top: 12px;
  padding: 11px 16px;
  border-radius: 10px;
  color: #263c92;
  background: #fff;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 13px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e9edf5;
  border-radius: 17px;
  padding: 19px;
  display: flex;
  flex-direction: column;
}

.stat-icon {
  width: 37px;
  height: 37px;
  border-radius: 10px;
  background: #eef2ff;
  color: #4560ca;
  display: grid;
  place-items: center;
  margin-bottom: 14px;
}

.stat-card span {
  color: #8791a5;
  font-size: 11px;
}

.stat-card strong {
  margin-top: 4px;
  font-family: "Plus Jakarta Sans";
  font-size: 19px;
}

.section-block {
  margin-top: 35px;
}

.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-heading h2 {
  font-family: "Plus Jakarta Sans";
  font-size: 20px;
  margin: 5px 0 0;
  letter-spacing: -.5px;
}

.text-btn {
  color: #4560ca;
  background: transparent;
}

.path-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 17px;
}

.path-card {
  background: #fff;
  border: 1px solid #e9edf5;
  border-radius: 17px;
  padding: 19px;
  transition: .2s ease;
  text-align: left;
}

.path-card:hover {
  transform: translateY(-2px);
  border-color: #d7def5;
  box-shadow: 0 12px 30px rgba(31, 48, 90, .07);
}

.path-button {
  border: 0;
  background: transparent;
  padding: 0;
  text-align: left;
}

.path-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.path-icon,
.detail-icon {
  width: 43px;
  height: 43px;
  display: grid;
  place-items: center;
  background: #f0f3ff;
  border-radius: 12px;
  font-size: 21px;
}

.category-pill {
  background: #f3f5fa;
  color: #7a8396;
  border-radius: 20px;
  padding: 5px 9px;
  font-size: 9px;
  font-weight: 800;
}

.path-card h3 {
  margin: 17px 0 7px;
  font-family: "Plus Jakarta Sans";
  font-size: 15px;
}

.path-card p {
  color: #7c869a;
  line-height: 1.55;
  font-size: 12px;
  min-height: 38px;
}

.match-row {
  margin-top: 17px;
}

.match-row > div:first-child {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
  color: #8b94a6;
}

.match-row strong {
  color: #314fb7;
}

.match-bar,
.bar {
  height: 5px;
  background: #edf0f6;
  border-radius: 5px;
  overflow: hidden;
  margin-top: 7px;
}

.match-bar span,
.bar span {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #4d69dd, #7890f2);
  border-radius: inherit;
}

.path-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid #f0f2f6;
  margin-top: 16px;
  padding-top: 13px;
  color: #4d62bd;
  font-size: 11px;
  font-weight: 700;
}

.bottom-grid {
  display: grid;
  grid-template-columns: 1.6fr .8fr;
  gap: 18px;
  margin-top: 20px;
}

.roadmap-preview,
.reassess-card {
  background: #fff;
  border: 1px solid #e9edf5;
  border-radius: 18px;
  padding: 22px;
}

.icon-btn {
  width: 35px;
  height: 35px;
  border-radius: 10px;
  color: #405cc6;
  background: #eef2ff;
}

.timeline {
  margin-top: 15px;
}

.timeline-item {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 9px 0;
  color: #9aa2b2;
  font-size: 12px;
}

.timeline-dot {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  border: 1px solid #e0e4ec;
}

.timeline-item.done {
  color: #3e54a9;
}

.timeline-item.done .timeline-dot {
  color: #4b64cc;
  background: #eef2ff;
  border: 0;
}

.timeline-item.active {
  color: #253352;
  font-weight: 700;
}

.timeline-item.active .timeline-dot {
  background: #edf2ff;
  border-color: #cbd5fb;
}

.timeline-item.active .timeline-dot span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4b64cc;
}

.reassess-icon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: #f1efff;
  color: #6853c8;
}

.reassess-card h3 {
  font-family: "Plus Jakarta Sans";
  margin: 17px 0 7px;
}

.reassess-card p {
  color: #7c869a;
  line-height: 1.6;
  font-size: 12px;
}

.full-btn {
  width: 100%;
  margin-top: 9px;
}

.secondary-btn {
  padding: 11px 15px;
  border-radius: 10px;
  color: #526078;
  background: #f2f4f8;
}

.primary-btn {
  padding: 11px 16px;
  border-radius: 10px;
  color: #fff;
  background: #3455d1;
  box-shadow: 0 7px 18px rgba(52, 85, 209, .18);
}

.primary-btn.large {
  padding: 14px 19px;
  margin-top: 12px;
}

.welcome {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr .9fr;
  align-items: center;
  padding: 60px max(6vw, 35px);
  position: relative;
  overflow: hidden;
  background: #f8faff;
}

.welcome-content {
  position: relative;
  z-index: 2;
  max-width: 640px;
}

.welcome h1 {
  font-size: clamp(42px, 5vw, 70px);
  line-height: 1.05;
}

.welcome h1 span {
  color: #4765d4;
}

.hero-copy {
  max-width: 570px;
  color: #717c92;
  font-size: 17px;
  line-height: 1.7;
}

.trust-row {
  display: flex;
  gap: 20px;
  margin-top: 27px;
  color: #778197;
  font-size: 11px;
  font-weight: 600;
  flex-wrap: wrap;
}

.trust-row div {
  display: flex;
  align-items: center;
  gap: 6px;
}

.trust-row svg {
  color: #4e69d1;
}

.hero-preview {
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 2;
}

.preview-window {
  width: min(450px, 90%);
  border-radius: 23px;
  background: #fff;
  box-shadow: 0 30px 70px rgba(38, 55, 104, .16);
  border: 1px solid #e5eaf3;
  overflow: hidden;
  transform: rotate(1.5deg);
}

.preview-top {
  height: 31px;
  border-bottom: 1px solid #eef1f6;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0 13px;
}

.preview-top span {
  width: 7px;
  height: 7px;
  background: #d7dce7;
  border-radius: 50%;
}

.preview-body {
  padding: 22px;
}

.preview-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-title small,
.preview-card small {
  font-size: 8px;
  font-weight: 800;
  color: #99a1b0;
  letter-spacing: 1px;
}

.preview-title h3 {
  font-family: "Plus Jakarta Sans";
  font-size: 16px;
  margin: 5px 0 0;
}

.preview-avatar {
  width: 35px;
  height: 35px;
  border-radius: 10px;
}

.preview-stat-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin: 20px 0;
}

.preview-stat-row div {
  background: #f7f8fb;
  padding: 10px;
  border-radius: 10px;
}

.preview-stat-row small {
  display: block;
  color: #9aa1af;
  font-size: 7px;
}

.preview-stat-row strong {
  display: block;
  margin-top: 4px;
  font-size: 12px;
}

.preview-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 10px;
  border: 1px solid #edf0f5;
  border-radius: 13px;
  padding: 11px;
  margin-top: 9px;
}

.preview-card-icon {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  display: grid;
  place-items: center;
  background: #eef2ff;
}

.preview-card strong {
  display: block;
  font-size: 10px;
  margin: 3px 0;
}

.preview-card span {
  display: block;
  color: #8d95a5;
  font-size: 8px;
}

.preview-card > b {
  font-size: 11px;
  color: #4260c7;
}

.welcome-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: .25;
}

.glow-one {
  background: #b9c8ff;
  top: -200px;
  right: -100px;
}

.glow-two {
  background: #dfc9ff;
  bottom: -250px;
  left: -150px;
}

.assessment-page {
  max-width: 1050px;
  margin: auto;
  padding: 55px 35px;
}

.assessment-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 30px;
  margin-bottom: 30px;
}

.assessment-header h1 {
  font-size: 34px;
}

.progress-track {
  width: 250px;
  height: 7px;
  background: #e8ebf2;
  border-radius: 7px;
  overflow: hidden;
}

.progress-track div {
  height: 100%;
  background: #4763d0;
}

.assessment-card {
  background: #fff;
  border: 1px solid #e6eaf2;
  border-radius: 21px;
  padding: 31px;
  box-shadow: 0 15px 45px rgba(40, 54, 91, .05);
}

.section-icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 13px;
  margin-bottom: 17px;
}

.section-icon.blue {
  color: #4161d2;
  background: #edf2ff;
}

.section-icon.purple {
  color: #6b54c8;
  background: #f1efff;
}

.section-icon.orange {
  color: #c97935;
  background: #fff1e7;
}

.assessment-card h2 {
  font-family: "Plus Jakarta Sans";
  margin: 0 0 6px;
  font-size: 22px;
}

.section-subtitle {
  color: #8790a2;
  margin: 0 0 25px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.field {
  display: block;
  margin-top: 20px;
}

.field > span {
  display: block;
  font-size: 11px;
  font-weight: 700;
  color: #505b70;
  margin-bottom: 7px;
}

.field input,
.field textarea {
  width: 100%;
  border: 1px solid #dfe4ed;
  border-radius: 10px;
  padding: 12px 13px;
  outline: none;
  color: #29334a;
  background: #fbfcfe;
  resize: vertical;
}

.field input:focus,
.field textarea:focus {
  border-color: #6b7ed4;
  box-shadow: 0 0 0 3px #eef1ff;
}

.chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
}

.choice-chip {
  border: 1px solid #e1e5ee;
  background: #fff;
  color: #59657b;
  border-radius: 10px;
  padding: 10px 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
}

.choice-chip:hover {
  border-color: #bbc7ec;
}

.choice-chip.selected {
  background: #edf2ff;
  border-color: #9eafea;
  color: #3451b7;
}

.assessment-actions {
  border-top: 1px solid #edf0f4;
  margin-top: 28px;
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
}

.explorer-tools {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.search-box {
  background: #fff;
  border: 1px solid #e3e7ef;
  border-radius: 11px;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 0 13px;
  width: 330px;
  color: #9aa2b0;
}

.search-box input {
  border: 0;
  outline: 0;
  padding: 11px 0;
  width: 100%;
}

.filter-pills {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.filter {
  border: 1px solid #e2e6ee;
  background: #fff;
  color: #707a8e;
  padding: 9px 12px;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 700;
}

.filter.active {
  background: #edf2ff;
  color: #3855bd;
  border-color: #cbd6fa;
}

.explorer-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 19px;
  align-items: start;
}

.explorer-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.detail-panel {
  position: sticky;
  top: 25px;
  background: #fff;
  border: 1px solid #e2e6ef;
  border-radius: 19px;
  padding: 23px;
}

.close-detail {
  border: 0;
  background: #f2f4f8;
  color: #677287;
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  float: right;
}

.detail-icon {
  clear: both;
  margin-top: 14px;
  margin-bottom: 17px;
}

.detail-panel h2 {
  font-family: "Plus Jakarta Sans";
  font-size: 21px;
  margin: 7px 0;
}

.detail-panel > p {
  color: #7d8799;
  line-height: 1.6;
  font-size: 12px;
}

.detail-section {
  border-top: 1px solid #edf0f5;
  margin-top: 19px;
  padding-top: 17px;
}

.detail-section h4 {
  margin: 0 0 11px;
  font-size: 11px;
}

.detail-line {
  color: #657086;
  font-size: 11px;
  margin: 8px 0;
  display: flex;
  gap: 7px;
}

.detail-line svg {
  color: #536bd0;
  flex-shrink: 0;
}

.career-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.career-tags span {
  background: #f4f6fa;
  padding: 7px 9px;
  border-radius: 7px;
  font-size: 10px;
  color: #606b7e;
}

.why-box {
  margin-top: 19px;
  background: #f1f4ff;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  gap: 9px;
  color: #4055a9;
}

.why-box p {
  color: #68749a;
  font-size: 10px;
  line-height: 1.5;
  margin: 4px 0 0;
}

.roadmap-banner {
  border-radius: 20px;
  padding: 27px 29px;
  color: #fff;
  background: linear-gradient(120deg, #243b8e, #3d58c3);
  display: flex;
  justify-content: space-between;
  gap: 30px;
  align-items: center;
}

.roadmap-banner h2 {
  font-family: "Plus Jakarta Sans";
  margin: 7px 0;
  font-size: 23px;
}

.roadmap-banner p {
  color: #d7def7;
  margin: 0;
  font-size: 12px;
}

.roadmap-progress {
  min-width: 150px;
  text-align: right;
}

.roadmap-progress strong {
  display: block;
  font-size: 26px;
}

.roadmap-progress span {
  color: #d2daf5;
  font-size: 10px;
}

.roadmap-progress div {
  height: 6px;
  margin-top: 10px;
  background: rgba(255,255,255,.2);
  border-radius: 6px;
}

.roadmap-progress i {
  display: block;
  height: 100%;
  width: 33%;
  background: #fff;
  border-radius: inherit;
}

.roadmap-list {
  margin-top: 20px;
  display: grid;
  gap: 9px;
}

.roadmap-step {
  background: #fff;
  border: 1px solid #e8ebf2;
  border-radius: 15px;
  padding: 16px;
  display: grid;
  grid-template-columns: 42px 1fr auto;
  gap: 13px;
  align-items: center;
}

.step-number {
  width: 39px;
  height: 39px;
  border-radius: 11px;
  display: grid;
  place-items: center;
  background: #f1f3f7;
  color: #8992a3;
  font-size: 10px;
  font-weight: 800;
}

.roadmap-step.done .step-number {
  color: #4c64c5;
  background: #edf2ff;
}

.step-content span {
  color: #9ba2b0;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 1px;
}

.step-content h3 {
  margin: 4px 0;
  font-size: 13px;
}

.step-content p {
  color: #838c9d;
  font-size: 11px;
  margin: 0;
}

.step-arrow {
  color: #a4abba;
}

.progress-overview {
  background: #fff;
  border: 1px solid #e7ebf2;
  border-radius: 19px;
  padding: 25px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.progress-score {
  display: flex;
  align-items: center;
  gap: 22px;
}

.score-ring {
  width: 125px;
  height: 125px;
  border-radius: 50%;
  background: conic-gradient(#4d66d1 32%, #edf0f6 0);
  display: grid;
  place-content: center;
  text-align: center;
  position: relative;
}

.score-ring::after {
  content: "";
  position: absolute;
  inset: 9px;
  background: #fff;
  border-radius: 50%;
}

.score-ring strong,
.score-ring span {
  position: relative;
  z-index: 1;
}

.score-ring strong {
  font-family: "Plus Jakarta Sans";
  font-size: 23px;
}

.score-ring span {
  font-size: 8px;
  color: #8992a3;
}

.progress-score h2 {
  font-family: "Plus Jakarta Sans";
  font-size: 18px;
  margin: 6px 0;
}

.progress-score p {
  color: #808a9d;
  font-size: 11px;
  line-height: 1.5;
}

.progress-bars {
  display: grid;
  gap: 16px;
  align-content: center;
}

.progress-item > div:first-child {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
}

.progress-item strong {
  color: #4962c5;
}

.section-heading.standalone {
  margin-top: 32px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.action-card {
  background: #fff;
  border: 1px solid #e7ebf2;
  border-radius: 16px;
  padding: 18px;
}

.action-icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  background: #eef2ff;
  color: #4b63c7;
  border-radius: 10px;
}

.action-card h3 {
  font-size: 13px;
  margin: 15px 0 5px;
}

.action-card p {
  color: #818b9d;
  font-size: 11px;
  line-height: 1.5;
  margin: 0 0 13px;
}

.action-card > svg {
  color: #5267be;
}

.reassessment-box {
  max-width: 850px;
  margin: 10px auto;
}

.mentor-fab {
  position: fixed;
  right: 25px;
  bottom: 24px;
  z-index: 50;
  border: 0;
  border-radius: 30px;
  padding: 12px 17px;
  color: #fff;
  background: #263f9a;
  box-shadow: 0 12px 30px rgba(30, 47, 108, .25);
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 12px;
}

.mentor-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(19, 28, 49, .28);
  display: flex;
  justify-content: flex-end;
}

.mentor-panel {
  width: min(430px, 100%);
  height: 100%;
  background: #fff;
  box-shadow: -15px 0 50px rgba(26, 36, 64, .15);
  display: flex;
  flex-direction: column;
}

.mentor-header {
  padding: 19px;
  border-bottom: 1px solid #e9edf4;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mentor-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mentor-avatar {
  width: 39px;
  height: 39px;
  border-radius: 11px;
  background: #edf2ff;
  color: #4560ca;
  display: grid;
  place-items: center;
}

.mentor-title strong,
.mentor-title span {
  display: block;
}

.mentor-title strong {
  font-size: 13px;
}

.mentor-title span {
  font-size: 9px;
  color: #9199a8;
  margin-top: 2px;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fc;
}

.chat-message {
  max-width: 82%;
  padding: 11px 13px;
  border-radius: 13px;
  margin-bottom: 11px;
  font-size: 12px;
  line-height: 1.55;
}

.chat-message.bot {
  background: #fff;
  border: 1px solid #e7ebf2;
  color: #59657a;
}

.chat-message.user {
  margin-left: auto;
  background: #3655ca;
  color: #fff;
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 13px;
  border-top: 1px solid #e8ebf1;
}

.chat-input input {
  flex: 1;
  border: 1px solid #dfe4ed;
  border-radius: 10px;
  padding: 11px;
  outline: none;
}

.chat-input button {
  width: 40px;
  border: 0;
  border-radius: 10px;
  color: #fff;
  background: #3655ca;
}

@media (max-width: 1050px) {
  .dashboard-grid,
  .bottom-grid,
  .progress-overview {
    grid-template-columns: 1fr;
  }

  .path-grid {
    grid-template-columns: 1fr 1fr;
  }

  .explorer-layout {
    grid-template-columns: 1fr;
  }

  .detail-panel {
    position: static;
  }
}

@media (max-width: 800px) {
  .sidebar {
    width: 70px;
    padding: 18px 9px;
  }

  .brand > div:last-child,
  .sidebar-label,
  .nav-item span,
  .privacy-card,
  .mini-profile > div:last-child {
    display: none;
  }

  .brand {
    justify-content: center;
    padding-bottom: 25px;
  }

  .nav-item {
    justify-content: center;
  }

  .main {
    margin-left: 70px;
    width: calc(100% - 70px);
  }

  .page {
    padding: 28px 22px 50px;
  }

  .welcome {
    grid-template-columns: 1fr;
    gap: 40px;
    padding: 50px 25px;
  }

  .hero-preview {
    order: 2;
  }

  .assessment-header {
    display: block;
  }

  .progress-track {
    margin-top: 20px;
    width: 100%;
  }

  .form-grid,
  .action-grid,
  .path-grid,
  .explorer-grid {
    grid-template-columns: 1fr;
  }

  .roadmap-banner {
    display: block;
  }

  .roadmap-progress {
    text-align: left;
    margin-top: 20px;
  }
}

@media (max-width: 500px) {
  .main {
    margin-left: 0;
    width: 100%;
  }

  .sidebar {
    display: none;
  }

  .page-header h1 {
    font-size: 25px;
  }

  .hero-card {
    padding: 24px;
  }

  .hero-orbit {
    display: none;
  }

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .assessment-page {
    padding: 30px 15px;
  }

  .assessment-card {
    padding: 21px;
  }

  .mentor-fab span {
    display: none;
  }
}
"""
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created: {relative_path}")

print("\n========================================")
print("Career Mentor Agent files created!")
print("========================================")