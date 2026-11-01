
"""
llm_mentor.py
-------------
Gemini-powered AI Career Mentor.
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Gemini configuration
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_TOKENS = 1000
MAX_HISTORY_MESSAGES = 20


def is_configured():
    """Check whether Gemini API key is available."""
    return bool(os.getenv("GEMINI_API_KEY"))


# --------------------------------------------------
# 1. SYSTEM PROMPT
# --------------------------------------------------

BASE_SYSTEM_PROMPT = """
You are Career Mentor, a friendly, intelligent AI assistant.

You help students with:
- Career guidance and education.
- Computer science and programming.
- Artificial Intelligence and Machine Learning.
- Data Structures and Algorithms.
- Web development and software engineering.
- College subjects and academic questions.
- Interview preparation and job opportunities.
- Learning roadmaps and technical projects.

IMPORTANT RULES:

1. Always answer the student's actual question.
2. Do not restrict yourself to career guidance.
3. Explain technical concepts in simple beginner-friendly English.
4. Provide practical examples whenever useful.
5. Use headings and bullet points for longer explanations.
6. Give complete answers instead of unrelated suggestions.
7. Ask follow-up questions only when necessary.
8. Never repeat fixed answers for different questions.
9. Be friendly, helpful and encouraging.
10. Never invent facts or guarantee jobs or salaries.

Keep simple answers short and provide detailed explanations
when the student requests them.

Reply in the same language as the student.
"""


def build_system_prompt(profile=None, results=None):
    """Build a personalized system prompt."""

    prompt = BASE_SYSTEM_PROMPT

    if not profile and not results:
        return prompt

    lines = [
        "\nStudent assessment information:"
    ]

    if profile:

        lines.append(
            f"- Name: {profile.get('name') or 'Student'}"
        )

        if profile.get("marks"):
            lines.append(
                f"- Class 10 marks: {profile['marks']}%"
            )

        if profile.get("location"):
            lines.append(
                f"- Location: {profile['location']}"
            )

        for label, key in [
            ("Interests", "interests"),
            ("Favourite subjects", "subjects"),
            ("Strengths", "strengths"),
            ("Preferred work style", "work_style"),
        ]:

            values = profile.get(key) or []

            if values:
                lines.append(
                    f"- {label}: {', '.join(values)}"
                )

        lines.append(
            f"- Budget: {profile.get('budget', 'not given')}"
        )

        lines.append(
            f"- Study preference: "
            f"{profile.get('study_preference', 'not given')}"
        )

        lines.append(
            f"- Work preference: "
            f"{profile.get('work_preference', 'not given')}"
        )

    if results and results.get("recommendations"):

        lines.append("\nRecommended career pathways:")

        for i, item in enumerate(
            results["recommendations"][:5],
            start=1
        ):

            lines.append(
                f"{i}. {item.get('name')} "
                f"({item.get('match_label', '')})"
            )

    return prompt + "\n".join(lines)


# --------------------------------------------------
# 2. CLEAN CHAT HISTORY
# --------------------------------------------------

def clean_messages(messages):
    """Validate and clean conversation history."""

    cleaned = []

    for message in (messages or [])[-MAX_HISTORY_MESSAGES:]:

        role = message.get("role")

        message_text = str(
            message.get("text")
            or message.get("content")
            or ""
        ).strip()

        if role not in ("user", "assistant"):
            continue

        if not message_text:
            continue

        if cleaned and cleaned[-1]["role"] == role:

            cleaned[-1]["content"] += (
                "\n" + message_text[:2000]
            )

        else:

            cleaned.append({
                "role": role,
                "content": message_text[:2000]
            })

    # Conversation must start with user
    while cleaned and cleaned[0]["role"] != "user":
        cleaned.pop(0)

    return cleaned


# --------------------------------------------------
# 3. GEMINI API CALL
# --------------------------------------------------

def ask_mentor(messages, profile=None, results=None):
    """Send conversation to Gemini and return its reply."""

    history = clean_messages(messages)

    if not history:
        raise ValueError("No valid messages were provided.")

    if history[-1]["role"] != "user":
        raise ValueError(
            "The last message must be from the student."
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing from backend/.env"
        )

    # Initialize Gemini client
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=60000
        )
    )

    # Convert chat history into Gemini format
    contents = []

    for message in history:

        gemini_role = (
            "user"
            if message["role"] == "user"
            else "model"
        )

        contents.append({
            "role": gemini_role,
            "parts": [
                {"text": message["content"]}
            ]
        })

    print(
        f"Gemini request started using {MODEL}...",
        flush=True
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(
                profile,
                results
            ),
            max_output_tokens=MAX_TOKENS,
            temperature=0.7
        )
    )

    print("Gemini response received!", flush=True)

    reply = (response.text or "").strip()

    if not reply:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return reply
