
from flask import Flask, request, jsonify
from flask_cors import CORS

from career_engine import recommend, get_all_pathways
from llm_mentor import ask_mentor, is_configured

app = Flask(__name__)
CORS(app)


@app.get("/")
def home():
    return jsonify({
        "message": "Career Mentor Agent API is running",
        "status": "success"
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Career Mentor Agent",
        "llm_enabled": is_configured()
    })


@app.get("/api/pathways")
def pathways():
    all_pathways = get_all_pathways()

    return jsonify({
        "count": len(all_pathways),
        "pathways": all_pathways
    })


@app.post("/api/recommend")
def recommendations():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No student profile was provided."
            }), 400

        if not data.get("name"):
            data["name"] = "Student"

        result = recommend(data)
        return jsonify(result)

    except Exception as error:
        print("Recommendation error:", repr(error))

        return jsonify({
            "error": "Unable to generate recommendations.",
            "details": str(error)
        }), 500


@app.post("/api/chat")
def chat():
    """Send the conversation to the Gemini AI mentor."""

    data = request.get_json(silent=True) or {}
    messages = data.get("messages") or []

    if not messages:
        return jsonify({
            "error": "No messages were provided."
        }), 400

    if not is_configured():
        return jsonify({
            "error": "Gemini API is not configured. Check backend/.env",
            "fallback": True
        }), 503

    try:
        reply = ask_mentor(
            messages,
            profile=data.get("profile"),
            results=data.get("results")
        )

        return jsonify({"reply": reply})

    except Exception as error:
        print("Gemini LLM error:", repr(error))

        return jsonify({
            "error": str(error),
            "fallback": True
        }), 502


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "API endpoint not found."
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
