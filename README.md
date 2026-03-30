# Auditly
# 🤖 AI Code Review Agent

> *Because waiting 2 days for a PR review is so 2023.*

An AI-powered code reviewer built with **Google ADK** and **Gemini 2.5 Flash** — deployed on **Google Cloud Run**. Paste any code, get back a structured review with issues, severity ratings, suggestions, and an overall score. Instantly. Like a senior engineer in your pocket.

---

## 🎬 Demo

> User pastes broken Python code →
> Agent finds **4 critical issues, 2 warnings** →
> Returns structured review with **score 3/10** →
> All in seconds. 🔥

---

## ✨ Features

- 🔴 **Critical / Warning / Info** severity classification
- 📍 **Line-by-line** issue detection
- 💡 **Actionable suggestions** for every issue
- 🏆 **Overall score** out of 10
- 👏 **Positive notes** — it finds the good stuff too
- 💬 **Built-in Chat UI** — no frontend needed
- ☁️ **Serverless** — scales automatically on Cloud Run

---

## 🏗️ Architecture

```
User pastes code
      ↓
root_agent         → Greets user, saves code to session state
      ↓
review_workflow    → SequentialAgent pipeline
      ↓
  code_analyzer    → Reads code from state, calls Gemini, returns JSON review
      ↓
  response_formatter → Formats JSON into clean human-readable response
      ↓
User sees the review ✅
```

---

## 🧠 How It Works

Two AI agents run in a sequential pipeline:

| Agent | Role |
|---|---|
| `code_analyzer` | Analyzes code, returns structured JSON with issues & score |
| `response_formatter` | Converts JSON into a friendly, readable review |

They share data through **session state** — like sticky notes passed between agents. No database needed.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Core language |
| 🤖 Google ADK | Agent orchestration & chat UI |
| ✨ Gemini 2.5 Flash | AI model powering the review |
| ☁️ Google Cloud Run | Serverless deployment |
| 🏔️ Vertex AI | Model hosting |

---

## 📁 Project Structure

```
code_review_agent/
├── agent.py          # All agent logic & pipeline
├── __init__.py       # Package entry point
├── requirements.txt  # Dependencies
├── .env              # Environment variables (never commit this!)
└── .env.example      # Template for environment variables
```

---

## 🚀 Getting Started

### Prerequisites
- Google Cloud account
- `gcloud` CLI installed
- Python 3.11+

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/code-review-agent.git
cd code-review-agent
```

### 2. Set up environment variables
```bash
cp .env.example .env
```
Fill in your values in `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
MODEL=gemini-2.5-flash
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run locally
```bash
uvx --from google-adk==1.14.0 adk web .
```

---

## ☁️ Deploy to Cloud Run

### 1. Set your project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable required services
```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  compute.googleapis.com
```

### 3. Create a service account
```bash
gcloud iam service-accounts create code-review-sa \
  --display-name="Service Account for Code Review Agent"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:code-review-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### 4. Deploy
```bash
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --service_name=code-review-agent \
  --with_ui \
  . \
  -- \
  --service-account=code-review-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

Your agent will be live at a public Cloud Run URL! 🎉

---

## 📊 Sample Output

```json
{
  "summary": "Code defines a function to calculate average but contains syntax errors.",
  "issues": [
    {
      "line_hint": "line 4",
      "severity": "critical",
      "description": "Missing colon after function definition.",
      "suggestion": "def calculate_average(numbers):"
    }
  ],
  "overall_score": 3,
  "positive_notes": [
    "Core logic for calculating average is correct.",
    "Good use of f-strings for output formatting."
  ]
}
```

---

## 💡 Fun Fact

```
🧠 Writing the AI code     →  20 mins
🐛 Debugging cloud infra   →  5 hrs 40 mins
```
*Coding is easy. Debugging in AI is a spiritual journey. The cloud is the final boss. 💀*

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — feel free to use, modify, and build on this.

---

## 👨‍💻 Author

Built with ☕ and way too many cloud permission errors.

⭐ **Star this repo if it helped you!**
