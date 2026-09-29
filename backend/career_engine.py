# career_engine.py

PATHWAYS = [
    {
        "id": "science_math",
        "name": "Science + Mathematics (MPC)",
        "short_name": "MPC",
        "icon": "🔬",
        "description": "A strong route for students interested in mathematics, technology, engineering and analytical careers.",
        "interests": ["computers", "technology", "mathematics", "science", "problem_solving"],
        "subjects": ["mathematics", "physics", "computer_science"],
        "strengths": ["analytical", "logical", "problem_solving"],
        "work_styles": ["technical", "analytical", "independent"],
        "careers": ["Software Engineer", "Data Scientist", "Engineer", "Cybersecurity Analyst", "AI/ML Engineer"],
        "routes": ["Class 11-12 MPC → Engineering/Science Degree → Specialization → Career"],
        "skills": ["Programming", "Mathematics", "Problem Solving", "Data Analysis"],
        "watch_out": "Requires consistent mathematics and science preparation."
    },
    {
        "id": "science_biology",
        "name": "Science + Biology (BiPC)",
        "short_name": "BiPC",
        "icon": "🧬",
        "description": "Suitable for students interested in biology, medicine, healthcare and life sciences.",
        "interests": ["biology", "healthcare", "science", "research", "helping_people"],
        "subjects": ["biology", "chemistry", "science"],
        "strengths": ["scientific", "patient", "memory"],
        "work_styles": ["people_focused", "scientific", "structured"],
        "careers": ["Doctor", "Pharmacist", "Biotechnologist", "Physiotherapist", "Life Science Professional"],
        "routes": ["Class 11-12 BiPC → Degree/Professional Course → Specialization"],
        "skills": ["Biology", "Scientific Thinking", "Communication", "Research"],
        "watch_out": "Some healthcare careers require competitive entrance exams and professional qualifications."
    },
    {
        "id": "commerce",
        "name": "Commerce & Business",
        "short_name": "Commerce",
        "icon": "💼",
        "description": "A pathway for students interested in business, finance, accounting, economics and entrepreneurship.",
        "interests": ["business", "finance", "money", "entrepreneurship", "economics"],
        "subjects": ["commerce", "economics", "mathematics"],
        "strengths": ["numerical", "communication", "organizing"],
        "work_styles": ["business", "people_focused", "analytical"],
        "careers": ["Accountant", "Financial Analyst", "Business Analyst", "Entrepreneur", "Banking Professional"],
        "routes": ["Class 11-12 Commerce → B.Com/BBA/Economics/Professional Course → Career"],
        "skills": ["Financial Literacy", "Accounting", "Communication", "Business Analysis"],
        "watch_out": "Building practical business and digital skills alongside academics is important."
    },
    {
        "id": "humanities",
        "name": "Humanities & Social Sciences",
        "short_name": "Humanities",
        "icon": "📚",
        "description": "A flexible pathway for students interested in society, psychology, history, languages, public policy and communication.",
        "interests": ["history", "psychology", "society", "writing", "politics"],
        "subjects": ["social_science", "history", "languages"],
        "strengths": ["communication", "creative", "critical_thinking"],
        "work_styles": ["people_focused", "creative", "research"],
        "careers": ["Psychologist", "Civil Services Aspirant", "Journalist", "Teacher", "Policy Professional"],
        "routes": ["Class 11-12 Humanities → Degree → Higher Study/Competitive Exams/Career"],
        "skills": ["Writing", "Research", "Communication", "Critical Thinking"],
        "watch_out": "Career outcomes depend strongly on specialization, skills and further education."
    },
    {
        "id": "polytechnic",
        "name": "Diploma / Polytechnic",
        "short_name": "Polytechnic",
        "icon": "🛠️",
        "description": "A practical technical route for students who prefer hands-on learning and applied engineering.",
        "interests": ["technology", "machines", "electronics", "computers", "hands_on"],
        "subjects": ["mathematics", "science", "computer_science"],
        "strengths": ["practical", "technical", "problem_solving"],
        "work_styles": ["hands_on", "technical", "practical"],
        "careers": ["Junior Engineer", "Technician", "CAD Technician", "Network Technician", "Technical Specialist"],
        "routes": ["After Class 10 → Diploma/Polytechnic → Job or Lateral Entry Degree"],
        "skills": ["Technical Skills", "CAD", "Electronics", "Programming"],
        "watch_out": "Choose the specialization carefully because diploma branches lead to different career areas."
    },
    {
        "id": "iti",
        "name": "ITI & Skilled Trades",
        "short_name": "ITI",
        "icon": "🔧",
        "description": "A skill-focused route for students who prefer practical work, tools, machines and technical trades.",
        "interests": ["machines", "hands_on", "repair", "electronics", "construction"],
        "subjects": ["science", "mathematics"],
        "strengths": ["practical", "technical", "discipline"],
        "work_styles": ["hands_on", "practical", "field"],
        "careers": ["Electrician", "Fitter", "Technician", "Mechanic", "Welder"],
        "routes": ["After Class 10 → ITI Trade → Apprenticeship/Employment/Further Skill Training"],
        "skills": ["Trade Skills", "Equipment Handling", "Safety", "Practical Problem Solving"],
        "watch_out": "Income and opportunities vary by trade, location and experience."
    },
    {
        "id": "design_creative",
        "name": "Design & Creative Careers",
        "short_name": "Design",
        "icon": "🎨",
        "description": "For students who enjoy visual creativity, design, fashion, products and creative problem solving.",
        "interests": ["design", "art", "drawing", "fashion", "creativity"],
        "subjects": ["art", "design", "languages"],
        "strengths": ["creative", "visual", "communication"],
        "work_styles": ["creative", "independent", "project_based"],
        "careers": ["UI/UX Designer", "Graphic Designer", "Fashion Designer", "Product Designer", "Interior Designer"],
        "routes": ["Class 10/12 → Diploma/Degree in Design → Portfolio → Career"],
        "skills": ["Design Tools", "Visual Communication", "Portfolio Building", "Creativity"],
        "watch_out": "A strong portfolio is often as important as formal qualifications."
    },
    {
        "id": "media_animation",
        "name": "Media, Animation & Gaming",
        "short_name": "Media & Gaming",
        "icon": "🎮",
        "description": "For students interested in animation, gaming, filmmaking, digital content and storytelling.",
        "interests": ["gaming", "animation", "video", "content", "storytelling"],
        "subjects": ["art", "computer_science", "languages"],
        "strengths": ["creative", "technical", "storytelling"],
        "work_styles": ["creative", "project_based", "technical"],
        "careers": ["Game Developer", "3D Artist", "Animator", "Video Editor", "Content Creator"],
        "routes": ["Class 10/12 → Diploma/Degree/Skill Course → Portfolio → Industry"],
        "skills": ["3D Tools", "Video Editing", "Game Development", "Storytelling"],
        "watch_out": "Technology changes quickly, so continuous skill development is important."
    },
    {
        "id": "agriculture",
        "name": "Agriculture & Environmental Careers",
        "short_name": "Agriculture",
        "icon": "🌱",
        "description": "A pathway combining agriculture, biology, technology, environment and rural development.",
        "interests": ["agriculture", "nature", "environment", "biology", "farming"],
        "subjects": ["biology", "science", "social_science"],
        "strengths": ["scientific", "practical", "observation"],
        "work_styles": ["field", "scientific", "practical"],
        "careers": ["Agriculture Professional", "Agronomist", "Food Technologist", "Environmental Professional", "Agri Entrepreneur"],
        "routes": ["Class 10/12 → Agriculture Diploma/Degree → Specialization/Career"],
        "skills": ["Agriculture Technology", "Data Analysis", "Field Skills", "Research"],
        "watch_out": "Course and career opportunities vary by region and specialization."
    },
    {
        "id": "hospitality",
        "name": "Hospitality & Tourism",
        "short_name": "Hospitality",
        "icon": "🏨",
        "description": "For students who enjoy people interaction, travel, food, events and service-oriented careers.",
        "interests": ["travel", "food", "hospitality", "people", "events"],
        "subjects": ["languages", "commerce", "social_science"],
        "strengths": ["communication", "social", "organizing"],
        "work_styles": ["people_focused", "active", "service"],
        "careers": ["Hotel Manager", "Chef", "Event Manager", "Travel Professional", "Hospitality Entrepreneur"],
        "routes": ["Class 10/12 → Hospitality Diploma/Degree → Internship → Career"],
        "skills": ["Communication", "Customer Service", "Management", "Teamwork"],
        "watch_out": "Working hours can be flexible and may include weekends or holidays."
    },
    {
        "id": "healthcare_allied",
        "name": "Allied Healthcare",
        "short_name": "Allied Health",
        "icon": "🩺",
        "description": "Healthcare careers outside the doctor route, including diagnostics, therapy and health technology.",
        "interests": ["healthcare", "biology", "helping_people", "technology", "science"],
        "subjects": ["biology", "science", "chemistry"],
        "strengths": ["scientific", "patient", "practical"],
        "work_styles": ["people_focused", "scientific", "structured"],
        "careers": ["Medical Lab Professional", "Radiology Professional", "Physiotherapist", "Optometry Professional", "Healthcare Technician"],
        "routes": ["Class 10/12 → Relevant Diploma/Degree → Clinical Training → Career"],
        "skills": ["Healthcare Knowledge", "Patient Care", "Diagnostics", "Technology"],
        "watch_out": "Eligibility requirements differ between healthcare programs."
    },
    {
        "id": "law",
        "name": "Law & Legal Careers",
        "short_name": "Law",
        "icon": "⚖️",
        "description": "For students interested in law, argument, communication, society and problem solving.",
        "interests": ["law", "debate", "society", "politics", "writing"],
        "subjects": ["social_science", "languages", "history"],
        "strengths": ["communication", "critical_thinking", "argument"],
        "work_styles": ["people_focused", "research", "analytical"],
        "careers": ["Lawyer", "Legal Advisor", "Corporate Legal Professional", "Legal Researcher", "Compliance Professional"],
        "routes": ["Class 10 → 11-12 Any Suitable Stream → Law Degree/Entrance → Career"],
        "skills": ["Legal Research", "Communication", "Writing", "Critical Thinking"],
        "watch_out": "Different law programs and careers have different entrance and qualification requirements."
    },
    {
        "id": "sports_fitness",
        "name": "Sports & Fitness",
        "short_name": "Sports",
        "icon": "🏃",
        "description": "For students passionate about sports, fitness, coaching and physical performance.",
        "interests": ["sports", "fitness", "health", "competition", "coaching"],
        "subjects": ["physical_education", "biology", "science"],
        "strengths": ["physical", "discipline", "teamwork"],
        "work_styles": ["active", "field", "people_focused"],
        "careers": ["Athlete", "Fitness Trainer", "Sports Coach", "Sports Manager", "Physical Education Professional"],
        "routes": ["Class 10/12 → Sports Training/Education → Certification/Degree → Career"],
        "skills": ["Fitness", "Coaching", "Discipline", "Teamwork"],
        "watch_out": "Competitive sports careers can be uncertain and require sustained training."
    },
    {
        "id": "entrepreneurship",
        "name": "Entrepreneurship & Business Building",
        "short_name": "Entrepreneurship",
        "icon": "🚀",
        "description": "For students who want to create businesses, products or independent careers.",
        "interests": ["entrepreneurship", "business", "innovation", "technology", "leadership"],
        "subjects": ["commerce", "economics", "mathematics"],
        "strengths": ["leadership", "creative", "communication"],
        "work_styles": ["independent", "business", "project_based"],
        "careers": ["Founder", "Small Business Owner", "Startup Professional", "Product Builder", "Freelancer"],
        "routes": ["Any Suitable Academic/Vocational Route → Skills → Small Projects → Business/Startup"],
        "skills": ["Communication", "Finance", "Marketing", "Technology", "Leadership"],
        "watch_out": "Business outcomes are uncertain; start with small experiments and practical learning."
    },
    {
        "id": "defence_public_service",
        "name": "Defence & Public Service",
        "short_name": "Defence / Public Service",
        "icon": "🛡️",
        "description": "For students interested in disciplined service, public administration, defence and community-oriented careers.",
        "interests": ["defence", "public_service", "leadership", "discipline", "helping_people"],
        "subjects": ["social_science", "mathematics", "science"],
        "strengths": ["discipline", "leadership", "physical", "communication"],
        "work_styles": ["structured", "field", "team"],
        "careers": ["Defence Professional", "Police Professional", "Public Administration Professional", "Government Employee", "Public Service Professional"],
        "routes": ["Class 10/12 → Appropriate Academic/Training Route → Eligibility/Examination → Service"],
        "skills": ["Discipline", "Leadership", "General Awareness", "Communication", "Fitness"],
        "watch_out": "Eligibility, examinations, age limits and physical requirements vary by service and recruitment notification."
    }
]


_PATHWAY_CACHE = None


def load_pathways():
    """Return pathways from MongoDB when available, else the built-in list."""
    global _PATHWAY_CACHE
    if _PATHWAY_CACHE is not None:
        return _PATHWAY_CACHE

    try:
        from db import fetch_pathways
        docs = fetch_pathways()
        if docs:
            _PATHWAY_CACHE = docs
            return _PATHWAY_CACHE
    except Exception as error:
        print(f"[career_engine] MongoDB unavailable, using built-in data: {error}")

    _PATHWAY_CACHE = PATHWAYS
    return _PATHWAY_CACHE


def clean_list(value):
    if not isinstance(value, list):
        return []
    return [str(item).strip().lower() for item in value if str(item).strip()]


def calculate_score(profile, pathway):
    interests = clean_list(profile.get("interests"))
    subjects = clean_list(profile.get("subjects"))
    strengths = clean_list(profile.get("strengths"))
    work_styles = clean_list(profile.get("work_styles"))

    pathway_interests = clean_list(pathway.get("interests"))
    pathway_subjects = clean_list(pathway.get("subjects"))
    pathway_strengths = clean_list(pathway.get("strengths"))
    pathway_work_styles = clean_list(pathway.get("work_styles"))

    matched_interests = [x for x in interests if x in pathway_interests]
    matched_subjects = [x for x in subjects if x in pathway_subjects]
    matched_strengths = [x for x in strengths if x in pathway_strengths]
    matched_work_styles = [x for x in work_styles if x in pathway_work_styles]

    score = (
        len(matched_interests) * 12
        + len(matched_subjects) * 8
        + len(matched_strengths) * 7
        + len(matched_work_styles) * 6
    )

    goal = str(profile.get("goal", "")).lower()

    if goal == "keep_options_open" and pathway["id"] in [
        "science_math",
        "commerce",
        "humanities",
        "polytechnic",
        "design_creative"
    ]:
        score += 5

    if goal == "start_early" and pathway["id"] in ["polytechnic", "iti"]:
        score += 8

    if goal == "professional_career" and pathway["id"] in [
        "science_math",
        "science_biology",
        "law",
        "healthcare_allied"
    ]:
        score += 4

    if not interests and not subjects and not strengths and not work_styles:
        score = 8

    return {
        "score": score,
        "matched_interests": matched_interests,
        "matched_subjects": matched_subjects,
        "matched_strengths": matched_strengths,
        "matched_work_styles": matched_work_styles
    }


def get_match_label(score):
    if score >= 45:
        return "Strong Match"
    if score >= 25:
        return "Good Match"
    return "Explore"


def readable(value):
    return str(value).replace("_", " ").title()


def build_reason(data, pathway):
    matches = []

    if data["matched_interests"]:
        matches.append(
            "your interest in " +
            ", ".join(readable(x) for x in data["matched_interests"][:3])
        )

    if data["matched_subjects"]:
        matches.append(
            "your preference for " +
            ", ".join(readable(x) for x in data["matched_subjects"][:2])
        )

    if data["matched_strengths"]:
        matches.append(
            "your strengths in " +
            ", ".join(readable(x) for x in data["matched_strengths"][:2])
        )

    if data["matched_work_styles"]:
        matches.append(
            "your preferred " +
            ", ".join(readable(x) for x in data["matched_work_styles"][:2]) +
            " work style"
        )

    if not matches:
        return (
            f"{pathway['name']} is included as an option because there is "
            "not enough profile information yet to make a strong match."
        )

    return "This pathway fits because it connects with " + ", ".join(matches) + "."


def build_summary(profile, recommendations):
    name = profile.get("name") or "Student"

    if not recommendations:
        return f"{name}, we need a little more information to personalize your career options."

    first = recommendations[0]

    return (
        f"{name}, your profile currently shows the strongest alignment with "
        f"{first['name']}. This is a starting recommendation, not a final "
        "career decision. Exploring multiple pathways and gaining real-world "
        "experience can help you make a better-informed choice."
    )


def build_roadmap(profile, recommendations):
    first = recommendations[0] if recommendations else None

    target = first["name"] if first else "your shortlisted pathways"

    return [
        {
            "stage": "0–30 Days",
            "title": "Understand Yourself",
            "actions": [
                "Review your interests, subjects, strengths and preferred work style.",
                f"Research {target} and at least two alternative pathways.",
                "Talk to a teacher, parent, counselor or working professional."
            ]
        },
        {
            "stage": "1–3 Months",
            "title": "Explore in Practice",
            "actions": [
                "Try beginner-level projects, videos, workshops or introductory courses.",
                "Compare course duration, eligibility, cost and location.",
                "Identify the subjects and skills you need to strengthen."
            ]
        },
        {
            "stage": "3–6 Months",
            "title": "Build Your Foundation",
            "actions": [
                "Start structured learning in your chosen area.",
                "Complete at least one practical project or activity.",
                "Track your progress and reconsider options if your interests change."
            ]
        },
        {
            "stage": "6–12 Months",
            "title": "Prepare Your Next Step",
            "actions": [
                "Shortlist suitable courses or institutions.",
                "Prepare for relevant entrance tests or eligibility requirements.",
                "Build a portfolio, certificates, projects or other evidence of skills.",
                "Review your decision with a trusted adult or career counselor."
            ]
        }
    ]


def recommend(profile):
    scored = []

    for pathway in load_pathways():
        result = calculate_score(profile, pathway)

        item = {
            **pathway,
            **result
        }

        item["match_label"] = get_match_label(item["score"])
        item["reason"] = build_reason(item, pathway)

        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)

    recommendations = scored[:5]
    alternatives = scored[5:9]

    for item in recommendations:
        item.pop("interests", None)
        item.pop("subjects", None)
        item.pop("strengths", None)
        item.pop("work_styles", None)

    for item in alternatives:
        item.pop("interests", None)
        item.pop("subjects", None)
        item.pop("strengths", None)
        item.pop("work_styles", None)

    result = {
        "student": {
            "name": profile.get("name") or "Student",
            "class_level": profile.get("class_level", "After Class 10"),
            "goal": profile.get("goal", ""),
            "budget": profile.get("budget", ""),
            "location": profile.get("location", ""),
            "study_preference": profile.get("study_preference", ""),
            "work_preference": profile.get("work_preference", "")
        },
        "summary": build_summary(profile, recommendations),
        "recommendations": recommendations,
        "alternatives": alternatives,
        "roadmap": build_roadmap(profile, recommendations),
        "important_note": (
            "Career recommendations are guidance based on the information "
            "provided by the student. They should not be treated as a guaranteed "
            "career outcome. Course availability, fees, eligibility, admissions, "
            "entrance examinations and job opportunities can change by institution "
            "and location. Verify important requirements from official sources "
            "and discuss major decisions with a parent, teacher or qualified "
            "career counselor."
        )
    }

    return result


def get_all_pathways():
    return load_pathways()