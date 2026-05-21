# Task Management Agent 🤖

A FastAPI-powered REST API that helps you manage your tasks intelligently. Simply send a text message or voice audio, and the agent will automatically classify it, generate a title, add notes, extract deadlines, and create the task directly in **Google Tasks**.

---

## ✨ Features

- 🎙️ **Audio & Text Input** — Send a voice note or plain text to create a task
- 🧠 **AI-Powered Classification** — Zero-shot classification places tasks into categories (Personal, Work, Shopping, etc.)
- ✍️ **Auto Title & Notes Generation** — An LLM generates a concise title and description from your input
- 📅 **Smart Date Extraction** — Detects deadlines from natural language (e.g. "next Monday", "15 de junio")
- 📋 **Google Tasks Integration** — Tasks are created in the right task list inside your Google account
- 🔐 **OAuth2 Authentication** — Secure Google login with encrypted token storage
- ⚡ **Async Queue Processing** — Task creation is handled asynchronously via Redis + RQ

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL (async via SQLAlchemy + asyncpg) |
| Queue | Redis + RQ |
| Auth | Google OAuth2 + JWT |
| LLM | HuggingFace Transformers (classification + generation) |
| Transcription | OpenAI Whisper |
| Google API | google-api-python-client |
| Security | Fernet encryption, python-jose |

---

## 📁 Project Structure

```
ramcodez3-task-management-agent/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── bus/
│   │   └── bus.py               # Redis queue setup
│   ├── handlers/
│   │   └── worker_logic.py      # Background worker logic
│   ├── models/                  # SQLAlchemy DB models
│   ├── routes/
│   │   ├── auth_route.py        # Google OAuth2 login/callback
│   │   └── task_route.py        # Task endpoints
│   ├── schemas/                 # Pydantic schemas
│   ├── services/
│   │   ├── database_service/    # DB access layer
│   │   ├── extract_date/        # NLP date extraction
│   │   ├── google_services/     # Google Tasks API wrappers
│   │   └── llm_services/        # Classification & generation LLMs
│   └── utils/                   # JWT, encryption, DB, transcription
├── .env.example
├── pyproject.toml
└── ruff.toml
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- `ffmpeg` installed on your system (for audio transcription)
- A [Google Cloud project](https://console.cloud.google.com/) with the **Tasks API** enabled and OAuth2 credentials

### Installation

This project uses [**uv**](https://docs.astral.sh/uv/) as the package manager. Make sure you have it installed:

```bash
pip install uv
```

```bash
# Clone the repository
git clone https://github.com/your-username/task-management-agent.git
cd task-management-agent

# Install dependencies
uv sync

# Copy and fill in environment variables
cp .env.example .env
```

### Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/yourdb
CLASSIFICATION_LLM=facebook/bart-large-mnli   # or any zero-shot model
GENERATION_LLM=google/flan-t5-base            # or any seq2seq model
REDIS_TOKEN=redis://localhost:6379
ENCRYPTION_KEY=your-fernet-key                # generate with Fernet.generate_key()
JWT_SECRET=your-jwt-secret
```

Place your `credentials.json` (downloaded from Google Cloud Console) in the project root.

### Run the API

```bash
cd app
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start the Worker

In a separate terminal:

```bash
uv run rq worker tasks
```

---

## 📡 API Endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/auth/login` | Redirects to Google OAuth2 login |
| `GET` | `/api/v1/auth/callback` | Handles OAuth2 callback, returns JWT |

### Tasks

All task endpoints require a `Bearer` token in the `Authorization` header.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/task/generate-task` | Create a task from text or audio |
| `GET` | `/api/v1/task/` | Get all tasks from a task list |
| `GET` | `/api/v1/task/pending_task` | Get all pending (incomplete) tasks |
| `GET` | `/api/v1/task/{date}` | Get tasks due on a specific date (`YYYY-MM-DD`) |

#### Example: Create a task from text

```bash
curl -X POST "http://localhost:8000/api/v1/task/generate-task" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "message=Buy groceries before next Friday"
```

#### Example: Create a task from audio

```bash
curl -X POST "http://localhost:8000/api/v1/task/generate-task" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "audio=@voice_note.ogg"
```

---

## 🔄 How It Works

```
User sends text or audio
        │
        ▼
   Audio? → Whisper transcribes to text
        │
        ▼
  Message enqueued in Redis (RQ)
        │
        ▼
  Worker picks up the job:
    1. LLM classifies the task → selects/creates Google Task List
    2. LLM generates title + description
    3. Date extractor finds the deadline
    4. Task is created in Google Tasks
```

---

## 🔐 Security

- Google OAuth2 refresh tokens are stored **encrypted** using Fernet symmetric encryption.
- API access is protected via **JWT tokens** (8-hour expiry).
- All sensitive configuration is managed through environment variables.

---

## 📄 License

Licensed under the [Apache License 2.0](LICENSE).

Copyright 2026 Aram Musset y Santiago Parra
