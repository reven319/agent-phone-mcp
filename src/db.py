"""Zero-dependency SQLite database layer for agent-phone-mcp using standard library sqlite3."""
import os
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "data.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(os.path.abspath(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL,
                direction TEXT DEFAULT 'outbound',
                status TEXT DEFAULT 'completed',
                duration_seconds INTEGER DEFAULT 0,
                audio_url TEXT,
                transcript TEXT,
                summary TEXT,
                sentiment TEXT DEFAULT 'neutral',
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE NOT NULL,
                label TEXT DEFAULT 'Main Agent Line',
                provider TEXT DEFAULT 'simulator',
                is_active INTEGER DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        # Seed default line if not present
        cursor.execute("SELECT count(*) as count FROM agent_numbers")
        row = cursor.fetchone()
        if row["count"] == 0:
            cursor.execute("""
                INSERT INTO agent_numbers (phone_number, label, provider, is_active, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, ("+1-555-019-2026", "Godmode Agent Primary Line", "simulator", 1, datetime.utcnow().isoformat()))
        conn.commit()
