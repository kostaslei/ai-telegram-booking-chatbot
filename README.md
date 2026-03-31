# 🤖 AI Appointment Booking Chatbot (Telegram)

An end-to-end AI-powered appointment booking assistant built with **Telegram, n8n, FastAPI, and LLMs**, fully containerized using **Docker Compose**.

This project demonstrates how to design and orchestrate a **stateful conversational system** with modern AI tooling and workflow automation.

---

## 🚀 Overview

This chatbot allows users to:

- 📅 Book appointments  
- 🕒 View available time slots  
- ❌ Cancel bookings  
- 💬 Interact naturally in a multi-turn conversation  

The system uses an LLM as a **decision engine** to interpret user intent and drive workflow logic.

---

## 🧠 Key Skills Demonstrated

- **LLM Integration**
  - Structured JSON outputs
  - Prompt engineering for deterministic flows
  - Intent + action extraction

- **Workflow Automation (n8n)**
  - Event-driven architecture
  - Conditional routing (Switch nodes)
  - API orchestration

- **Backend Development (FastAPI)**
  - REST API design
  - Stateful user management
  - In-memory data handling

- **Conversational AI**
  - Multi-turn dialogue handling
  - Slot filling (date, time)
  - Handling incomplete inputs

- **System Design**
  - Webhook-based architecture
  - Dockerized services
  - Clear separation of concerns

---

## 🏗️ Architecture
```
User (Telegram)
   ↓
Telegram Webhook
   ↓
n8n (Docker)
   ↓
   ├── FastAPI (Docker - API & state)
   └── OpenAI API (decision engine)
   ↓
Telegram Response
```

---

## 🔄 System Flow

1. User sends a message via Telegram  
2. Telegram triggers webhook → n8n  
3. n8n:
   - Extracts `user_id` + message  
   - Fetches user state from FastAPI  
   - Sends message + state to LLM  
4. LLM returns structured JSON:
```json
{
  "intent": "book",
  "date": "2026-03-30",
  "time": "10:00",
  "next_action": "show_slots"
}
```
5. n8n routes logic based on next_action
6. FastAPI handles booking / availability
7. Response sent back to Telegram

---

## 🧩 Conversation Design

The chatbot is stateful (multi-turn).

Each user has a state object:
```json
{
  "intent": "book",
  "date": null,
  "time": null,
  "next_action": "ask_date",
  "reply": "short natural message"
}
```
### Example Interaction
```
User: hello
Bot: Hi! How can I help?

User: I want to book
Bot: What date works for you?

User: tomorrow
Bot: Here are available slots...

User: 10am
Bot: Your booking is confirmed!
```
---

## 🧠 LLM as Decision Engine

The LLM is responsible for:

- Intent detection
- Entity extraction (date, time)
- Deciding the next action

**Output format**
```json
{
  "intent": "book | cancel | question",
  "date": "YYYY-MM-DD | null",
  "time": "HH:MM | null",
  "next_action": "greet | ask_date | show_slots | confirm_booking | cancel_booking | answer_question",
  "reply": "LLM response"
}
```

---

## 🔧 FastAPI Backend
### Features
- In-memory storage (no database)
- Booking management
- User state tracking
  
### Endpoints

|Method|         Endpoint          |    Description    |
| ---- | ------------------------- | ----------------- |
|GET   |  /api/availability?date=  |Get available slots|
|GET   |  /api/available-dates     |Get suggested dates|
|POST  |    /api/book              |  Book appointment |
|POST  |    /api/cancel            |  Cancel booking   |
|GET   |   /api/state/{user_id}    |  Get user state   |
|POST  |    /api/state             |   Update state    |
|DELETE|     /api/state/{user_id}  |    Clear state    |

---

## ⚙️ n8n Workflow

### Core responsibilities:

- Telegram webhook handling
- State retrieval + updates
- LLM orchestration
- Conditional routing via Switch
- API calls (availability, booking, cancel)

---

## 🐳 Getting Started (Docker Compose)
1. **Clone the repository**
```
git clone https://github.com/kostaslei/ai-telegram-booking-chatbot
cd ai-telegram-booking-chatbot
```
2. **Start the full system**
```docker-compose up --build```

This will start:

- n8n (workflow automation)
- FastAPI (booking + state API)

---

## 🔗 Service Communication

**Inside Docker:**
```http://host.docker.internal:8000```

---

## 🌐 Telegram Webhook Setup
1. Start ngrok:
```ngrok http 5678```
2. Set your Telegram webhook to:
```https://<ngrok-url>/webhook/telegram```

---

## ⚠️ Limitations
- In-memory storage (resets on restart)
- No authentication
- No persistence
- Not production deployed

## 🧪 Edge Cases Handled
- First interaction (no state)
- Missing date/time (multi-turn flow)
- Greeting vs intent detection
- No available slots fallback

📈 Future Improvements
- Add database (PostgreSQL / Redis)
- Full Docker Compose networking (no host.docker.internal)
- Calendar integrations (Google Calendar)
- Admin dashboard
- Observability (logs, metrics)
- Retry & error handling

---

## 💡 Why This Project Matters

This project demonstrates:

- How to combine LLMs + deterministic workflows
- How to build real-world AI automation systems
- How to design production-like architectures

---

## 🛠️ Tech Stack
- Python (FastAPI)
- n8n
- OpenAI API
- Telegram Bot API
- Docker & Docker Compose
- ngrok
  
## 📬 Contact

Feel free to reach out or explore the code.
