"""
MindBloom — Safe AI-Driven Chat for Student Mental Well-Being
Author : NAURIN | Jaya Prakash Narayan College of Engineering | CSE
"""

from flask import Flask, render_template, request, jsonify, session
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import anthropic
import uuid
import json
import re
import logging
import os

app   = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "mindbloom-secret-change-in-prod")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vader  = SentimentIntensityAnalyzer()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ─── Crisis phrases ────────────────────────────────────────────────────────────
CRISIS_PHRASES = [
    "kill myself", "suicide", "hurt myself", "end my life",
    "don't want to live", "want to die", "self harm", "cut myself",
    "no reason to live", "end it all"
]

# ─── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are MindBloom, a compassionate AI wellness companion for students.

Detect the user's emotional state and respond ONLY with valid JSON:

{
  "mood": "<crisis|severely_distressed|anxious|stressed|sad|lonely|burnt_out|positive|neutral>",
  "mood_label": "<short label e.g. 'Feeling Overwhelmed'>",
  "empathy": "<2-3 warm sentences acknowledging their feeling specifically>",
  "motivation": "<1-2 sentences of genuine encouragement tailored to their situation>",
  "relaxation": {
    "title": "<technique name>",
    "steps": ["step1", "step2", "step3", "step4"]
  },
  "crisis_note": "<if mood is crisis: caring message + iCall: 9152987821. else empty string>"
}

Rules:
- Never say 'just relax' or 'don't worry'
- Be specific to what they said, not generic
- For crisis mood always populate crisis_note
- Return ONLY valid JSON, nothing else
"""


def is_crisis(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in CRISIS_PHRASES)


def detect_emotion_vader(text: str, history: list) -> str:
    score = vader.polarity_scores(text)["compound"]
    if score <= -0.6:  return "severely_distressed"
    if score <  -0.15: return "sad_or_stressed"
    if score >   0.4:  return "positive"
    if len(text.split()) <= 4 and history:
        return history[-1].get("emotion", "neutral")
    return "neutral"


def call_claude(user_message: str, history: list) -> dict:
    messages = []
    for h in history[-8:]:
        messages.append({"role": "user",      "content": h["user"]})
        messages.append({"role": "assistant", "content": h["bot_raw"]})
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model      = "claude-sonnet-4-20250514",
        max_tokens = 1000,
        system     = SYSTEM_PROMPT,
        messages   = messages
    )

    raw = response.content[0].text.strip()
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        raise ValueError("No JSON in response")
    return json.loads(match.group(0)), raw


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session["history"]    = []
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data    = request.get_json(force=True)
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    history = session.get("history", [])

    # Crisis guard
    if is_crisis(message):
        logger.warning("CRISIS detected | session=%s", session.get("session_id"))
        crisis_reply = {
            "mood"       : "crisis",
            "mood_label" : "You Matter",
            "empathy"    : "I'm really concerned about you. What you're feeling is real and overwhelming — but you don't have to face this alone.",
            "motivation" : "Your life has value. Please reach out to someone who can help right now.",
            "relaxation" : {"title": "Slow Breath", "steps": [
                "Breathe in slowly for 4 counts",
                "Hold for 4 counts",
                "Breathe out for 6 counts",
                "Repeat — help is on the way"
            ]},
            "crisis_note": "Please call iCall immediately: 9152987821 | Text HOME to 741741 | Emergency: 112"
        }
        return jsonify({"response": crisis_reply, "time": datetime.now().strftime("%H:%M")})

    # Call Claude
    try:
        parsed, raw = call_claude(message, history)
    except Exception as e:
        logger.error("Claude API error: %s", e)
        # Fallback to VADER
        emotion = detect_emotion_vader(message, history)
        parsed  = {
            "mood"       : emotion,
            "mood_label" : "Here for you",
            "empathy"    : "I hear you. Something seems to be weighing on you right now.",
            "motivation" : "Every step to reach out for support is an act of courage.",
            "relaxation" : {"title": "Box Breathing", "steps": [
                "Breathe in for 4 counts",
                "Hold for 4 counts",
                "Breathe out for 4 counts",
                "Hold for 4 counts"
            ]},
            "crisis_note": ""
        }
        raw = json.dumps(parsed)

    history.append({
        "user"    : message,
        "bot_raw" : raw,
        "emotion" : parsed.get("mood", "neutral"),
        "time"    : datetime.now().isoformat()
    })
    session["history"] = history[-10:]

    return jsonify({"response": parsed, "time": datetime.now().strftime("%H:%M")})


@app.route("/reset", methods=["POST"])
def reset():
    session["history"] = []
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=7860)
