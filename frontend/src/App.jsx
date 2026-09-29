import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

const interestOptions = [
  "Technology",
  "Computers",
  "Mathematics",
  "Science",
  "Biology",
  "Healthcare",
  "Business",
  "Finance",
  "Entrepreneurship",
  "Design",
  "Creativity",
  "Gaming",
  "Animation",
  "Media",
  "Travel",
  "Agriculture",
  "Nature",
  "Law",
  "Sports",
  "Helping People",
];

const subjectOptions = [
  "Mathematics",
  "Physics",
  "Chemistry",
  "Biology",
  "Computer Science",
  "Accountancy",
  "Economics",
  "Business Studies",
  "History",
  "Geography",
  "Languages",
  "Art",
  "Physical Education",
  "Social Science",
  "Science",
];

const strengthOptions = [
  "Logical Thinking",
  "Problem Solving",
  "Mathematical Thinking",
  "Analytical Thinking",
  "Creativity",
  "Communication",
  "Leadership",
  "Teamwork",
  "Empathy",
  "Observation",
  "Discipline",
  "Practical Thinking",
];

const workOptions = [
  "Technical",
  "Analytical",
  "Creative",
  "People Focused",
  "Hands On",
  "Independent",
  "Team Based",
  "Project Based",
];

const pathwayIcons = {
  "Science + Mathematics": "🔬",
  "Science + Biology": "🧬",
  "Commerce & Business": "📊",
  "Humanities & Social Sciences": "🌍",
  "Diploma / Polytechnic": "🛠️",
  "ITI & Skilled Trades": "🔧",
  "Design & Creative Careers": "🎨",
  "Media, Animation & Gaming": "🎮",
  "Agriculture & Environmental Careers": "🌱",
  "Hospitality & Tourism": "🏨",
  "Allied Healthcare": "🩺",
  "Law & Legal Careers": "⚖️",
  "Sports & Fitness": "🏃",
  "Entrepreneurship & Business Building": "🚀",
  "Defence & Public Service": "🛡️",
};

function App() {
  const [page, setPage] = useState("home");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const [profile, setProfile] = useState({
    name: "",
    marks: "",
    interests: [],
    subjects: [],
    strengths: [],
    work_style: [],
    goal: "keep_options_open",
    budget: "medium",
    location: "",
    study_preference: "degree",
    work_preference: "flexible",
  });

  const [compareList, setCompareList] = useState([]);
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your Career Mentor. Ask me anything about career options after Class 10.",
    },
  ]);
  const [chatInput, setChatInput] = useState("");

  const toggleArrayValue = (field, value) => {
    setProfile((current) => {
      const values = current[field];

      return {
        ...current,
        [field]: values.includes(value)
          ? values.filter((item) => item !== value)
          : [...values, value],
      };
    });
  };

  const submitAssessment = async (event) => {
    event.preventDefault();

    if (!profile.name.trim()) {
      alert("Please enter your name.");
      return;
    }

    if (profile.interests.length === 0) {
      alert("Please select at least one interest.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/api/recommend`,
        profile
      );

      setResults(response.data);
      setPage("results");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
      console.error(error);
      alert(
        "Unable to connect to the Career Mentor backend. Make sure Flask is running on port 5000."
      );
    } finally {
      setLoading(false);
    }
  };

  const startAssessment = () => {
    setPage("assessment");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const goHome = () => {
    setPage("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const toggleCompare = (pathway) => {
    setCompareList((current) => {
      const exists = current.some((item) => item.id === pathway.id);

      if (exists) {
        return current.filter((item) => item.id !== pathway.id);
      }

      if (current.length >= 3) {
        alert("You can compare up to 3 pathways.");
        return current;
      }

      return [...current, pathway];
    });
  };

  const sendChat = () => {
    const question = chatInput.trim();

    if (!question) return;

    const lower = question.toLowerCase();

    let answer =
      "Tell me more about your interests, favourite subjects, strengths, or the type of work you want to do. I can help you explore different career paths.";

    if (
      lower.includes("computer") ||
      lower.includes("coding") ||
      lower.includes("software")
    ) {
      answer =
        "If you like computers, you have several options after Class 10. You can explore Science + Mathematics, Polytechnic, ITI technical routes, Media/Animation/Gaming, or Entrepreneurship. You do not have to choose only one route.";
    } else if (
      lower.includes("doctor") ||
      lower.includes("medical") ||
      lower.includes("health")
    ) {
      answer =
        "Healthcare is broader than becoming a doctor. You can explore Science + Biology as well as allied healthcare areas such as medical laboratory work, imaging, physiotherapy and healthcare technology.";
    } else if (
      lower.includes("business") ||
      lower.includes("commerce") ||
      lower.includes("finance")
    ) {
      answer =
        "Commerce can lead to accounting, finance, banking, business analysis, marketing and entrepreneurship. You can also combine business skills with technology.";
    } else if (
      lower.includes("design") ||
      lower.includes("drawing") ||
      lower.includes("creative")
    ) {
      answer =
        "Creative students can explore Design, UI/UX, Fashion, Graphic Design, Animation, Gaming, Media and Content Creation. Building a portfolio is especially useful.";
    } else if (
      lower.includes("10th") ||
      lower.includes("class 10") ||
      lower.includes("after 10")
    ) {
      answer =
        "After Class 10, you are not limited to MPC, BiPC, CEC or HEC. You can also consider Polytechnic, ITI, vocational education, Design, Media, Agriculture, Hospitality, Allied Healthcare, Law, Sports and Entrepreneurship.";
    } else if (
      lower.includes("job") ||
      lower.includes("quick")
    ) {
      answer =
        "If your priority is becoming job-ready sooner, explore skill-focused options such as ITI, Polytechnic, vocational education and selected certificate-based pathways. Always check recognition and actual placement opportunities before enrolling.";
    } else if (
      lower.includes("confused") ||
      lower.includes("don't know") ||
      lower.includes("dont know")
    ) {
      answer =
        "That's completely okay. Start by identifying what you enjoy, what subjects you can tolerate studying for several years, what kind of work environment you prefer, and whether you want a degree, diploma or skill-based route.";
    }

    setChatMessages((current) => [
      ...current,
      { role: "user", text: question },
      { role: "assistant", text: answer },
    ]);

    setChatInput("");
  };

  const renderHeader = () => (
    <header className="navbar">
      <div className="nav-inner">
        <button className="brand" onClick={goHome}>
          <span className="brand-icon">CM</span>
          <span>
            <strong>CareerMentor</strong>
            <small>AI Career Guidance</small>
          </span>
        </button>

        <nav>
          <button
            className={page === "home" ? "nav-active" : ""}
            onClick={goHome}
          >
            Home
          </button>

          <button
            className={page === "assessment" ? "nav-active" : ""}
            onClick={startAssessment}
          >
            Assessment
          </button>

          <button
            className={page === "mentor" ? "nav-active" : ""}
            onClick={() => setPage("mentor")}
          >
            Mentor
          </button>

          {results && (
            <button
              className={page === "results" ? "nav-active" : ""}
              onClick={() => setPage("results")}
            >
              My Results
            </button>
          )}
        </nav>
      </div>
    </header>
  );

  const renderHome = () => (
    <main>
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            ✨ Career guidance starting after Class 10
          </div>

          <h1>
            Your career journey
            <span> starts here.</span>
          </h1>

          <p>
            Discover career pathways based on your interests, strengths,
            subjects, goals and preferred way of learning — not just a
            traditional stream.
          </p>

          <div className="hero-actions">
            <button className="primary-btn" onClick={startAssessment}>
              Discover My Path →
            </button>

            <button
              className="secondary-btn"
              onClick={() => setPage("mentor")}
            >
              💬 Talk to Mentor
            </button>
          </div>

          <div className="hero-stats">
            <div>
              <strong>15+</strong>
              <span>Career Routes</span>
            </div>

            <div>
              <strong>5</strong>
              <span>Personalized Matches</span>
            </div>

            <div>
              <strong>1 Year</strong>
              <span>Action Roadmap</span>
            </div>
          </div>
        </div>

        <div className="hero-card">
          <div className="floating-card card-one">
            <span>🎯</span>
            <div>
              <strong>Personalized</strong>
              <small>Based on your profile</small>
            </div>
          </div>

          <div className="mentor-visual">
            <div className="visual-circle">
              🧭
            </div>

            <div className="orbit orbit-one">🎓</div>
            <div className="orbit orbit-two">💡</div>
            <div className="orbit orbit-three">🚀</div>
          </div>

          <div className="floating-card card-two">
            <span>🛣️</span>
            <div>
              <strong>Clear Roadmap</strong>
              <small>Know what to do next</small>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <span className="eyebrow">WHY CAREERMENTOR</span>
          <h2>More than choosing a stream.</h2>
          <p>
            Career decisions should consider the whole student, not just marks.
          </p>
        </div>

        <div className="feature-grid">
          <Feature
            icon="🧠"
            title="Know Yourself"
            text="Understand your interests, strengths, subjects and preferred work style."
          />

          <Feature
            icon="🧭"
            title="Explore Paths"
            text="Look beyond traditional streams and discover practical alternatives."
          />

          <Feature
            icon="🎯"
            title="Get Matched"
            text="Receive personalized pathways with clear reasons behind each match."
          />

          <Feature
            icon="📅"
            title="Take Action"
            text="Turn your career direction into a practical one-year roadmap."
          />
        </div>
      </section>

      <section className="pathway-preview">
        <div className="section-heading left">
          <span className="eyebrow">EXPLORE POSSIBILITIES</span>
          <h2>There is more than one way forward.</h2>
          <p>
            Traditional academic streams are only part of the picture.
          </p>
        </div>

        <div className="mini-pathways">
          {[
            ["🔬", "Science & Technology"],
            ["📊", "Commerce & Business"],
            ["🎨", "Design & Creative"],
            ["🛠️", "Polytechnic & ITI"],
            ["🩺", "Healthcare"],
            ["🎮", "Media & Gaming"],
            ["🌱", "Agriculture"],
            ["🚀", "Entrepreneurship"],
          ].map(([icon, title]) => (
            <div className="mini-pathway" key={title}>
              <span>{icon}</span>
              <strong>{title}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <div>
          <span className="eyebrow">READY?</span>
          <h2>Start discovering your possibilities.</h2>
          <p>
            The assessment takes only a few minutes.
          </p>
        </div>

        <button className="primary-btn" onClick={startAssessment}>
          Take Career Assessment →
        </button>
      </section>
    </main>
  );

  const renderAssessment = () => (
    <main className="assessment-page">
      <div className="assessment-header">
        <span className="eyebrow">CAREER ASSESSMENT</span>
        <h1>Let's understand you first.</h1>
        <p>
          There are no right or wrong answers. Choose what genuinely feels
          closest to you.
        </p>
      </div>

      <form className="assessment-form" onSubmit={submitAssessment}>
        <div className="form-section">
          <div className="form-section-title">
            <span>01</span>
            <div>
              <h2>Basic Information</h2>
              <p>Tell us where you are starting from.</p>
            </div>
          </div>

          <div className="form-grid">
            <label>
              Your Name
              <input
                type="text"
                placeholder="Enter your name"
                value={profile.name}
                onChange={(e) =>
                  setProfile({ ...profile, name: e.target.value })
                }
              />
            </label>

            <label>
              Class 10 Marks (%)
              <input
                type="number"
                min="0"
                max="100"
                placeholder="Example: 85"
                value={profile.marks}
                onChange={(e) =>
                  setProfile({ ...profile, marks: e.target.value })
                }
              />
            </label>

            <label>
              City / State
              <input
                type="text"
                placeholder="Example: Hyderabad, Telangana"
                value={profile.location}
                onChange={(e) =>
                  setProfile({ ...profile, location: e.target.value })
                }
              />
            </label>

            <label>
              Budget Preference
              <select
                value={profile.budget}
                onChange={(e) =>
                  setProfile({ ...profile, budget: e.target.value })
                }
              >
                <option value="low">Prefer lower-cost options</option>
                <option value="medium">Moderate budget</option>
                <option value="high">Budget is flexible</option>
              </select>
            </label>
          </div>
        </div>

        <OptionSection
          number="02"
          title="What interests you?"
          subtitle="Select everything that sounds interesting."
          options={interestOptions}
          selected={profile.interests}
          onToggle={(value) => toggleArrayValue("interests", value)}
        />

        <OptionSection
          number="03"
          title="Which subjects do you enjoy?"
          subtitle="Select the subjects you like or feel comfortable with."
          options={subjectOptions}
          selected={profile.subjects}
          onToggle={(value) => toggleArrayValue("subjects", value)}
        />

        <OptionSection
          number="04"
          title="What are your strengths?"
          subtitle="Choose the qualities that describe you."
          options={strengthOptions}
          selected={profile.strengths}
          onToggle={(value) => toggleArrayValue("strengths", value)}
        />

        <OptionSection
          number="05"
          title="How do you prefer to work?"
          subtitle="Think about the environment where you would enjoy working."
          options={workOptions}
          selected={profile.work_style}
          onToggle={(value) => toggleArrayValue("work_style", value)}
        />

        <div className="form-section">
          <div className="form-section-title">
            <span>06</span>
            <div>
              <h2>Your Future Preference</h2>
              <p>These help us understand what kind of route you want.</p>
            </div>
          </div>

          <div className="form-grid">
            <label>
              Main Career Goal
              <select
                value={profile.goal}
                onChange={(e) =>
                  setProfile({ ...profile, goal: e.target.value })
                }
              >
                <option value="keep_options_open">
                  Keep my options open
                </option>
                <option value="specific_field">
                  I already have a field in mind
                </option>
              </select>
            </label>

            <label>
              Study Preference
              <select
                value={profile.study_preference}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    study_preference: e.target.value,
                  })
                }
              >
                <option value="degree">Degree / Long-term education</option>
                <option value="diploma">Diploma / Polytechnic</option>
                <option value="short_course">
                  Shorter skill-based course
                </option>
                <option value="flexible">Open to different routes</option>
              </select>
            </label>

            <label>
              Work Preference
              <select
                value={profile.work_preference}
                onChange={(e) =>
                  setProfile({
                    ...profile,
                    work_preference: e.target.value,
                  })
                }
              >
                <option value="flexible">I'm flexible</option>
                <option value="quick_job">Become job-ready sooner</option>
                <option value="professional">
                  Build a professional career
                </option>
                <option value="entrepreneur">
                  Build something of my own
                </option>
              </select>
            </label>
          </div>
        </div>

        <div className="assessment-submit">
          <div>
            <strong>Ready to discover your paths?</strong>
            <span>Your results will include matches and a roadmap.</span>
          </div>

          <button className="primary-btn" type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze My Career Path →"}
          </button>
        </div>
      </form>
    </main>
  );

  const renderResults = () => {
    if (!results) {
      return (
        <main className="empty-page">
          <h1>No results yet.</h1>
          <button className="primary-btn" onClick={startAssessment}>
            Take Assessment
          </button>
        </main>
      );
    }

    return (
      <main className="results-page">
        <section className="results-hero">
          <div>
            <span className="eyebrow">YOUR CAREER REPORT</span>
            <h1>
              Great to meet you,{" "}
              <span>{results.student?.name || profile.name}.</span>
            </h1>
            <p>{results.summary}</p>
          </div>

          <div className="report-badge">
            <span>🎯</span>
            <strong>Personalized</strong>
            <small>Career Guidance</small>
          </div>
        </section>

        <section className="results-section">
          <div className="section-heading left">
            <span className="eyebrow">TOP MATCHES</span>
            <h2>Paths worth exploring</h2>
            <p>
              These recommendations are based on the information you provided.
            </p>
          </div>

          <div className="recommendation-grid">
            {results.recommendations?.map((pathway, index) => (
              <PathwayCard
                key={pathway.id || index}
                pathway={pathway}
                rank={index + 1}
                compareList={compareList}
                onCompare={toggleCompare}
              />
            ))}
          </div>
        </section>

        {results.alternatives?.length > 0 && (
          <section className="results-section alternative-section">
            <div className="section-heading left">
              <span className="eyebrow">ALTERNATIVES</span>
              <h2>Other paths to explore</h2>
            </div>

            <div className="alternative-grid">
              {results.alternatives.map((pathway) => (
                <div className="alternative-card" key={pathway.id}>
                  <span className="alternative-icon">
                    {pathway.icon || pathwayIcons[pathway.name] || "🧭"}
                  </span>
                  <div>
                    <h3>{pathway.name}</h3>
                    <p>{pathway.description}</p>
                    <span className="match-pill">
                      {pathway.match_label}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {compareList.length >= 2 && (
          <section className="results-section">
            <div className="section-heading left">
              <span className="eyebrow">DECISION SUPPORT</span>
              <h2>Compare your selected paths</h2>
            </div>

            <div className="comparison-table-wrapper">
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th>Category</th>
                    {compareList.map((item) => (
                      <th key={item.id}>
                        {item.icon || pathwayIcons[item.name] || "🧭"}{" "}
                        {item.name}
                      </th>
                    ))}
                  </tr>
                </thead>

                <tbody>
                  <tr>
                    <td>Careers</td>
                    {compareList.map((item) => (
                      <td key={item.id}>
                        {item.careers?.slice(0, 4).join(", ") || "Explore"}
                      </td>
                    ))}
                  </tr>

                  <tr>
                    <td>Education Routes</td>
                    {compareList.map((item) => (
                      <td key={item.id}>
                        {item.routes?.[0] || "Explore route"}
                      </td>
                    ))}
                  </tr>

                  <tr>
                    <td>Skills</td>
                    {compareList.map((item) => (
                      <td key={item.id}>
                        {item.skills?.slice(0, 4).join(", ") || "Build skills"}
                      </td>
                    ))}
                  </tr>

                  <tr>
                    <td>Match</td>
                    {compareList.map((item) => (
                      <td key={item.id}>
                        <strong>{item.match_label}</strong>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        )}

        {results.roadmap && (
          <section className="results-section">
            <div className="section-heading left">
              <span className="eyebrow">YOUR ACTION PLAN</span>
              <h2>12-month career roadmap</h2>
              <p>
                A starting plan. You can adjust it as you learn more about
                yourself.
              </p>
            </div>

            <div className="roadmap">
              {results.roadmap.map((step, index) => (
                <div className="roadmap-item" key={index}>
                  <div className="roadmap-number">{index + 1}</div>

                  <div className="roadmap-content">
                    <span>{step.period}</span>
                    <h3>{step.title}</h3>

                    <ul>
                      {step.actions?.map((action, actionIndex) => (
                        <li key={actionIndex}>{action}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="results-tools">
          <div className="tool-card">
            <span>💬</span>
            <div>
              <h3>Still confused?</h3>
              <p>Talk to the Career Mentor about your options.</p>
            </div>
            <button
              className="secondary-btn"
              onClick={() => setPage("mentor")}
            >
              Ask Mentor
            </button>
          </div>

          <div className="tool-card">
            <span>🔄</span>
            <div>
              <h3>Want another perspective?</h3>
              <p>Change your answers and explore different pathways.</p>
            </div>
            <button className="secondary-btn" onClick={startAssessment}>
              Retake
            </button>
          </div>
        </section>

        <div className="important-note">
          <strong>⚠️ Important:</strong>{" "}
          {results.important_note ||
            "This tool provides guidance and should not replace discussions with parents, teachers or qualified career counselors."}
        </div>
      </main>
    );
  };

  const renderMentor = () => (
    <main className="mentor-page">
      <section className="mentor-header">
        <span className="eyebrow">CAREER MENTOR</span>
        <h1>Ask. Explore. Understand.</h1>
        <p>
          Ask questions about career choices after Class 10.
        </p>
      </section>

      <div className="chat-shell">
        <div className="chat-top">
          <div className="mentor-avatar">CM</div>
          <div>
            <strong>Career Mentor</strong>
            <span>Guidance Assistant</span>
          </div>
          <div className="online-dot"></div>
        </div>

        <div className="chat-messages">
          {chatMessages.map((message, index) => (
            <div
              key={index}
              className={
                message.role === "user"
                  ? "message user-message"
                  : "message assistant-message"
              }
            >
              {message.text}
            </div>
          ))}
        </div>

        <div className="suggestion-row">
          {[
            "What can I do after 10th?",
            "I like computers",
            "I don't want MPC",
            "I want a quick job",
          ].map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => {
                setChatInput(suggestion);
              }}
            >
              {suggestion}
            </button>
          ))}
        </div>

        <div className="chat-input-row">
          <input
            type="text"
            placeholder="Ask your career question..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendChat();
            }}
          />

          <button className="primary-btn" onClick={sendChat}>
            Send →
          </button>
        </div>
      </div>
    </main>
  );

  return (
    <div className="app">
      {renderHeader()}

      {page === "home" && renderHome()}
      {page === "assessment" && renderAssessment()}
      {page === "results" && renderResults()}
      {page === "mentor" && renderMentor()}

      <footer className="footer">
        <div className="footer-inner">
          <div>
            <strong>CareerMentor</strong>
            <p>
              Helping students explore possibilities and plan their next step.
            </p>
          </div>

          <div className="footer-links">
            <button onClick={goHome}>Home</button>
            <button onClick={startAssessment}>Assessment</button>
            <button onClick={() => setPage("mentor")}>Mentor</button>
          </div>
        </div>

        <div className="footer-bottom">
          <span>Career Mentor Agent</span>
          <span>Guidance • Exploration • Planning</span>
        </div>
      </footer>
    </div>
  );
}

function Feature({ icon, title, text }) {
  return (
    <div className="feature-card">
      <div className="feature-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
  );
}

function OptionSection({
  number,
  title,
  subtitle,
  options,
  selected,
  onToggle,
}) {
  return (
    <div className="form-section">
      <div className="form-section-title">
        <span>{number}</span>
        <div>
          <h2>{title}</h2>
          <p>{subtitle}</p>
        </div>
      </div>

      <div className="option-grid">
        {options.map((option) => {
          const active = selected.includes(option);

          return (
            <button
              type="button"
              className={`option-chip ${active ? "selected" : ""}`}
              key={option}
              onClick={() => onToggle(option)}
            >
              {active && <span>✓</span>}
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
}

function PathwayCard({
  pathway,
  rank,
  compareList,
  onCompare,
}) {
  const icon =
    pathway.icon || pathwayIcons[pathway.name] || "🧭";

  const selected = compareList.some(
    (item) => item.id === pathway.id
  );

  return (
    <article className="recommendation-card">
      <div className="recommendation-top">
        <div className="pathway-icon">{icon}</div>

        <div className="rank">
          #{rank}
        </div>
      </div>

      <span className="match-label">
        {pathway.match_label || "Explore"}
      </span>

      <h3>{pathway.name}</h3>

      <p className="pathway-description">
        {pathway.description}
      </p>

      <div className="match-reason">
        <strong>Why this fits</strong>
        <p>{pathway.reason}</p>
      </div>

      {(pathway.matched_interests?.length > 0 ||
        pathway.matched_subjects?.length > 0 ||
        pathway.matched_strengths?.length > 0) && (
        <div className="match-details">
          {pathway.matched_interests?.length > 0 && (
            <div>
              <small>Interests</small>
              <p>{pathway.matched_interests.join(", ")}</p>
            </div>
          )}

          {pathway.matched_subjects?.length > 0 && (
            <div>
              <small>Subjects</small>
              <p>{pathway.matched_subjects.join(", ")}</p>
            </div>
          )}

          {pathway.matched_strengths?.length > 0 && (
            <div>
              <small>Strengths</small>
              <p>{pathway.matched_strengths.join(", ")}</p>
            </div>
          )}
        </div>
      )}

      <div className="career-list">
        <strong>Possible careers</strong>

        <div className="tag-list">
          {pathway.careers?.slice(0, 5).map((career) => (
            <span key={career}>{career}</span>
          ))}
        </div>
      </div>

      <div className="route-box">
        <strong>Education route</strong>
        <p>{pathway.routes?.[0]}</p>
      </div>

      <div className="card-actions">
        <button
          className={`compare-btn ${selected ? "selected" : ""}`}
          onClick={() => onCompare(pathway)}
        >
          {selected ? "✓ Added to Compare" : "＋ Compare"}
        </button>
      </div>

      {pathway.watch_out && (
        <div className="watch-out">
          <strong>Keep in mind</strong>
          <p>{pathway.watch_out}</p>
        </div>
      )}
    </article>
  );
}

export default App;