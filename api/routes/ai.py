from fastapi import APIRouter
from dotenv import load_dotenv
from schemas.ai import AIRequest, AIResponse
import os
from openai import OpenAI

router = APIRouter()

load_dotenv(dotenv_path="../.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(message: str, state: dict) -> str:
    return f"""
You are an AI assistant that helps users book or cancel appointments.

CONTEXT
Today: {state["current_date"]}
State: {state}
User message: {message}
TASK
Detect intent
Extract date/time (if any)
Decide next_action
Reply briefly and naturally
INTENTS
"book" → booking request
"cancel" → cancel request
"question" → general question
"unknown" → unclear/irrelevant
DATE & TIME
Convert relative dates ("today", "tomorrow", "next Monday") → YYYY-MM-DD
Use today's date as reference
Missing date/time → null
DECISION LOGIC (STRICT ORDER)
1. Greeting

If only greeting (e.g. "hi", "hello"):
→ next_action = "answer_question"

2. Booking (intent = "book")
Use conversation context to resolve partial inputs:
If dates suggested and user says "30" → map to matching date
If times suggested and user says "15" → map to matching time
If user selects a date not in suggested options:
→ next_action = "show_slots"
→ reply: date  let me check for available dates
If user selects a time not in suggested options:
→ next_action = "show_slots"
→ reply: time unavailable + let me check for available slots
Flow:
No date → "suggest_dates"
Date but no time → "show_slots"
Date + time → "confirm_booking"
Do NOT set time before date. If user mention time before date, request for date
3. Cancel (intent = "cancel")

→ next_action = "cancel_booking"

4. Fallback

If unclear, خارج scope, or low confidence:
→ next_action = "answer_question"
→ reply: politely say you cannot help

RULES
Keep replies short and friendly
Do NOT invent availability or slots
Be ACCURATE on times. If available times 12:00, 10:00 and user say 11, then we dont have available times
Only confirm when next_action = "confirm_booking"
Always guide user to next step
NEVER say that a time or date is available unless is mentioned on the context, say checking for available dates

---

## OUTPUT FORMAT (STRICT JSON)

Return ONLY valid JSON:

{{
"intent": "book | cancel | question | unknown",
"date": "YYYY-MM-DD | null",
"time": "HH:MM | null",
"next_action": "suggest_dates | show_slots | confirm_booking | cancel_booking | answer_question",
"reply": "short natural message",
}}
"""


@router.post("/ai/decision", response_model=AIResponse)
def ai_decision(data: AIRequest):
    prompt = build_prompt(data.message, data.state)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are a structured JSON generator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content

    import json

    try:
        parsed = json.loads(content)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print("RAW CONTENT:", content)
        parsed = {
            "intent": "unknown",
            "next_action": "ask_question",
            "reply": "Sorry, I didn’t understand that."
        }

    return parsed