"""agent-phone-mcp — FastAPI entry point & Webhook server."""
import sys
import os
import argparse
from typing import Optional, Dict, Any

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

try:
    from .db import init_db
    from .call_manager import (
        initiate_outbound_call,
        record_inbound_call,
        get_call_transcript_by_id,
        list_recent_calls,
        get_agent_numbers
    )
    from .mcp_server import run_stdio_mcp
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.db import init_db
    from src.call_manager import (
        initiate_outbound_call,
        record_inbound_call,
        get_call_transcript_by_id,
        list_recent_calls,
        get_agent_numbers
    )
    from src.mcp_server import run_stdio_mcp

# Initialize SQLite tables
init_db()

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="agent-phone-mcp",
        description="Open, local-first Model Context Protocol (MCP) server & webhook bridge for AI voice agents.",
        version="0.1.0"
    )

    class OutboundCallRequest(BaseModel):
        to_number: str
        message: str

    class InboundWebhookPayload(BaseModel):
        from_number: str
        speech_text: str

    @app.get("/")
    async def root():
        return {
            "name": "agent-phone-mcp",
            "status": "online",
            "description": "Model Context Protocol voice agent bridge",
            "endpoints": {
                "health": "/",
                "calls": "/api/calls",
                "outbound": "/api/calls/outbound",
                "webhook_incoming": "/api/webhooks/incoming",
                "numbers": "/api/numbers"
            }
        }

    @app.get("/api/numbers")
    async def get_numbers():
        return {"numbers": get_agent_numbers()}

    @app.get("/api/calls")
    async def get_calls(limit: int = 10):
        return {"calls": list_recent_calls(limit=limit)}

    @app.get("/api/calls/{call_id}")
    async def get_call(call_id: int):
        call = get_call_transcript_by_id(call_id)
        if not call:
            raise HTTPException(status_code=404, detail=f"Call {call_id} not found")
        return call

    @app.post("/api/calls/outbound")
    async def trigger_outbound_call(payload: OutboundCallRequest):
        return initiate_outbound_call(to_number=payload.to_number, message=payload.message)

    @app.post("/api/webhooks/incoming")
    async def handle_inbound_call_webhook(payload: InboundWebhookPayload):
        return record_inbound_call(from_number=payload.from_number, caller_speech=payload.speech_text)
else:
    app = None


def start():
    parser = argparse.ArgumentParser(description="agent-phone-mcp runner")
    parser.add_argument("--mcp", action="store_true", help="Run MCP stdio server")
    parser.add_argument("--host", default="127.0.0.1", help="Web server host")
    parser.add_argument("--port", type=int, default=8000, help="Web server port")
    args = parser.parse_args()

    if args.mcp:
        run_stdio_mcp()
    else:
        if not FASTAPI_AVAILABLE:
            print("[agent-phone-mcp] FastAPI or uvicorn not installed.")
            print("[agent-phone-mcp] To run as an MCP server with zero dependencies, run:")
            print("                  python src/main.py --mcp")
            print("[agent-phone-mcp] To run the HTTP webhook server, install dependencies:")
            print("                  pip install fastapi uvicorn")
            sys.exit(1)
        import uvicorn
        print(f"[agent-phone-mcp] Starting FastAPI webhook server on http://{args.host}:{args.port}")
        uvicorn.run("src.main:app", host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    start()
