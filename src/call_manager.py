"""Call management and simulation logic for agent-phone-mcp using sqlite3."""
import random
from datetime import datetime
from typing import Optional, List, Dict, Any
from .db import get_connection


def initiate_outbound_call(to_number: str, message: str) -> Dict[str, Any]:
    """Initiates an outbound phone call and records the simulated dialogue and transcript."""
    duration = random.randint(25, 95)
    
    simulated_transcript = (
        f"Agent: Hello! I'm calling regarding: '{message}'. Do you have a moment to talk?\n"
        f"Recipient: Yes, I can hear you clearly. Could you give me more details?\n"
        f"Agent: Absolutely. We have confirmed the request and updated the context.\n"
        f"Recipient: Perfect, thank you for confirming. Have a good day!\n"
        f"Agent: Thank you, goodbye!"
    )
    summary = f"Call completed to {to_number}. Discussed '{message}'. Recipient acknowledged and confirmed receipt."
    created_at = datetime.utcnow().isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calls (phone_number, direction, status, duration_seconds, transcript, summary, sentiment, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (to_number, "outbound", "completed", duration, simulated_transcript, summary, "positive", created_at))
        call_id = cursor.lastrowid
        conn.commit()

        return {
            "call_id": call_id,
            "phone_number": to_number,
            "status": "completed",
            "duration_seconds": duration,
            "summary": summary,
            "transcript": simulated_transcript,
            "created_at": created_at
        }


def record_inbound_call(from_number: str, caller_speech: str) -> Dict[str, Any]:
    """Records an incoming call from a customer/user, transcribing speech into agent context."""
    duration = random.randint(20, 60)
    transcript = (
        f"Caller: {caller_speech}\n"
        f"Agent (Auto-Attendant): Thank you for calling Godmode Agent Line. Your message has been transcribed and delivered to the agent."
    )
    summary = f"Inbound call from {from_number}. Caller noted: '{caller_speech[:80]}...'"
    created_at = datetime.utcnow().isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO calls (phone_number, direction, status, duration_seconds, transcript, summary, sentiment, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (from_number, "inbound", "completed", duration, transcript, summary, "neutral", created_at))
        call_id = cursor.lastrowid
        conn.commit()

        return {
            "call_id": call_id,
            "phone_number": from_number,
            "direction": "inbound",
            "duration_seconds": duration,
            "summary": summary,
            "transcript": transcript,
            "created_at": created_at
        }


def get_call_transcript_by_id(call_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves full transcript and metadata for a specific call ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM calls WHERE id = ?", (call_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return dict(row)


def list_recent_calls(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns recent incoming and outgoing phone calls."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id as call_id, phone_number, direction, status, duration_seconds, summary, created_at FROM calls ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def get_agent_numbers() -> List[Dict[str, Any]]:
    """Lists available phone numbers configured for the agent."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number as number, label, provider FROM agent_numbers WHERE is_active = 1")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
