# 🌱 MindBloom — Safe AI-Driven Chat for Student Mental Well-Being

**Author:** NAURIN | Jaya Prakash Narayan College of Engineering | CSE  
**Capstone Project** — AI & NLP | Mental Health Support System

---

## 📌 About the Project

MindBloom is a safe, AI-driven wellness chatbot that:
- Detects student mood in real-time using **VADER Sentiment Analysis**
- Generates **empathetic, personalised responses** via Claude AI
- Provides **relaxation techniques** (breathing, grounding, journaling)
- Has a **crisis safety layer** that instantly shows helplines for at-risk messages

---

## 🗂️ Project Structure

```
mindbloom/
├── app.py               ← Flask backend + Claude API + VADER
├── templates/
│   └── chat.html        ← Full chat UI (dark theme, mood detection)
├── requirements.txt     ← Python dependencies
├── Procfile             ← For Render/Railway deployment
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mindbloom.git
cd mindbloom
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
# Linux / Mac
export ANTHROPIC_API_KEY="your-api-key-here"
export FLASK_SECRET="any-random-secret-string"

# Windows
set ANTHROPIC_API_KEY=your-api-key-here
set FLASK_SECRET=any-random-secret-string
```

> Get your free Anthropic API key at: https://console.anthropic.com

### 4. Run locally
```bash
python app.py
```
Open: http://localhost:7860

---

## 🚀 Deployment Guide

### Option A — Render (Recommended, FREE)

1. Push this project to GitHub
2. Go to https://render.com → **New Web Service**
3. Connect your GitHub repo
4. Set these values:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add **Environment Variables:**
   - `ANTHROPIC_API_KEY` → your key
   - `FLASK_SECRET` → any random string
6. Click **Deploy** — your app will be live at `https://mindbloom.onrender.com`

### Option B — Railway (FREE tier available)

1. Go to https://railway.app → New Project → Deploy from GitHub
2. Add environment variables (same as above)
3. Railway auto-detects Procfile and deploys

### Option C — Hugging Face Spaces (FREE)

1. Create a Space at https://huggingface.co/spaces
2. Choose **Gradio** SDK (or Docker for Flask)
3. Upload files and set `ANTHROPIC_API_KEY` in Space Secrets

---

## 🛡️ Safety Features

| Feature | Description |
|---|---|
| Crisis detection | 10 dangerous phrases caught client-side before API call |
| Immediate helpline | iCall (9152987821) shown instantly for crisis messages |
| Session isolation | Each user has independent conversation history |
| No data storage | Conversations stored only in server session (not database) |

---

## 🔬 Technologies Used

| Layer | Technology |
|---|---|
| Sentiment Analysis | VADER (vaderSentiment) |
| AI Responses | Anthropic Claude (claude-sonnet) |
| Backend | Python Flask |
| Frontend | HTML5, CSS3, Vanilla JS |
| Deployment | Render / Railway / Hugging Face |

---

## 📞 Crisis Resources (India)

- **iCall (TISS):** 9152987821
- **Vandrevala Foundation:** 1860-2662-345
- **NIMHANS:** 080-46110007
- **International:** https://findahelpline.com

---

*MindBloom — Supporting Every Student, One Conversation at a Time 🌱*
