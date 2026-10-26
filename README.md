# Agent Phone MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)

An open-source, local-first **Model Context Protocol (MCP)** server that equips AI agents with dedicated voice phone lines, automated outbound calling, incoming webhook handling, and real-time speech transcription directly into agent context.

Inspired by recent voice agent advances on ProductHunt, built to be private, self-hostable, and zero-lock-in.

---

## Features

- 📞 **Autonomous Outbound Calling:** Let Claude Code, Cursor, or Antigravity place phone calls to confirm operational events, alert developers, or conduct voice inquiries.
- 🎙️ **Incoming Call Webhook & Transcription:** Inbound voice handler records, auto-transcribes, and summarizes messages into structured MCP context.
- ⚡ **Zero-Dependency MCP Core:** Pure Python JSON-RPC stdio transport using built-in standard libraries (`sqlite3`), requiring zero external pip packages to start.
- 🌐 **Optional FastAPI Webhook Bridge:** Full REST API and VoIP webhook support for Twilio / SIP integration.
- 🔒 **Local & Private:** Zero mandatory third-party audio recording retention. All call metadata and transcripts stay in local SQLite (`data.db`).

---

## 5 Native MCP Tools

1. `place_phone_call`: Dispatches outbound calls to a recipient number, speaks the agent's message, and logs the full dialog transcript.
2. `simulate_incoming_call`: Simulates inbound voice calls from customers or external systems directly into the agent's context.
3. `get_call_transcript`: Fetches the word-for-word transcript and structured summary of any past call by ID.
4. `list_phone_calls`: Lists recent incoming/outgoing calls, durations, and statuses.
5. `get_agent_phone_numbers`: Retrieves active phone lines assigned to the agent.

---

## Quickstart

### 1. Run as an MCP Server (Zero Setup)

Connect directly to your AI agent via stdio:

```bash
python src/main.py --mcp
```

### 2. Configure with your MCP Client

Add `agent-phone-mcp` to your MCP configuration (e.g., `claude_desktop_config.json` or Antigravity/Cursor MCP settings):

```json
{
  "mcpServers": {
    "agent-phone": {
      "command": "python",
      "args": [
        "path/to/agent-phone-mcp/src/main.py",
        "--mcp"
      ]
    }
  }
}
```

### 3. Run the Verification Tests

```bash
python tests/test_call_flow.py
```

### 4. Optional: Run HTTP Webhook Server (FastAPI)

```bash
pip install -r requirements.txt
python src/main.py --port 8000
```

---

## Architecture

```
┌─────────────────────────────────┐
│     AI Agent (Claude / Cursor)   │
└────────────────┬────────────────┘
                 │ stdio / JSON-RPC
                 ▼
┌─────────────────────────────────┐
│       agent-phone-mcp           │
│   (MCP Server / Tools Engine)   │
└────────┬───────────────┬────────┘
         │               │
         ▼               ▼
┌─────────────────┐ ┌───────────────┐
│ Embedded SQLite │ │ FastAPI VoIP  │
│    (data.db)    │ │   Webhooks    │
└─────────────────┘ └───────────────┘
```

---

## License

MIT License. Free and open source.
