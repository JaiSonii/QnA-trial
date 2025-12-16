# Hemut Trial Project: Real-Time Q&A Dashboard

A full-stack, real-time Question & Answer platform built for the Hemut trial assessment. This application allows guests to ask questions and view live updates, while administrators can manage, escalate, and resolve queries.

## 🚀 Features

### Core Functionality
- **Real-Time Updates:** Uses WebSockets to push new questions and replies to all connected clients instantly.
- **Role-Based Access Control:**
  - **Guests:** Can post questions, view the feed, and reply to threads.
  - **Admins:** Can view dashboard statistics, "Escalate" questions to the top, and "Mark Resolved".
- **Live Sorting:** Questions are sorted by status (Escalated first) and then by timestamp.
- **Legacy Validation:** Implemented raw `XMLHttpRequest` for frontend form validation as per specific assessment requirements.

### Features Implemented
- **AI RAG Integration:** Includes a mock RAG service that auto-generates suggestions for questions based on keywords (e.g., "login", "event", "admin").
- **Community Threads:** Expanded the data model to support community replies separate from the official Admin Answer.
- **Webhooks:** System triggers POST requests to registered external URLs when a question is answered.

---

## 🛠️ Tech Stack

- **Frontend:** Next.js 15 (React 19), Tailwind CSS, Shadcn UI.
- **Backend:** FastAPI (Python 3.12), SQLModel, SQLite.
- **Infrastructure:** Docker & Docker Compose.
- **Protocols:** HTTP/REST, WebSockets, Webhooks.

---

## 📦 Quick Start (Docker)

The easiest way to run the application is via Docker Compose.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JaiSonii/QnA-trial
   cd QnA-trial
   ``` 
2.  **Start the services:**

    ```bash
    docker-compose up --build
    ```

3.  **Access the Application:**

      - **Frontend:** [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)
      - **Backend API Docs:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

-----

## 🏃 Manual Installation

If you prefer running without Docker:

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt # or install from pyproject.toml
uvicorn app.main:create_app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

-----

## 🔑 How to Use

### 1\. Creating an Admin Account

The system automatically assigns roles based on the email domain during registration.

  - Go to `/register`.
  - Use an email ending in `@admin.com` (e.g., `jai@admin.com`) to create an **Admin** account.
  - Use any other email (e.g., `guest@gmail.com`) to create a **Guest** account.

### 2\. Testing the AI

Ask a question containing specific keywords to trigger the mock RAG service:

  - *"How do I login?"*
  - *"When does the event start?"*
  - *"What can an admin do?"*

The system will immediately append an `(AI Suggestion)` to these questions.

### 3\. Testing XHR Validation

The assessment required using `XMLHttpRequest` for validation. This logic is isolated in `frontend/src/lib/legacyApi.ts`.

  - Try submitting a blank question.
  - The error is caught via the XHR `readyState` and `status` checks before reaching the main API handler.

-----

## 📂 Project Structure

```bash
├── backend/
│   ├── app/
│   │   ├── api/          # Routes (auth, questions, webhooks)
│   │   ├── core/         # Config, Database, Security
│   │   ├── models/       # SQLModel Database Tables
│   │   ├── services/     # Business Logic (RAG, Webhooks, WS)
│   │   └── main.py       # App Entrypoint
│   └── hemut_qa.db       # SQLite Database (generated on run)
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js App Router Pages
│   │   ├── components/   # UI Components (QuestionCard, etc.)
│   │   └── lib/
│   │       ├── api.ts        # Modern Axios API calls
│   │       └── legacyApi.ts  # Required XHR Implementation
└── docker-compose.yml
```

## 🧪 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

**Key Endpoints:**

  - `POST /questions/`: Submit a new question (triggers WebSocket broadcast).
  - `PATCH /questions/{id}/answer`: Mark as answered (Admin only, triggers Webhooks).
  - `PATCH /questions/{id}/status`: Change status to "Escalated" (Admin only).
  - `WS /questions/ws`: WebSocket endpoint for real-time feeds.