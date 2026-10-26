"""Model Context Protocol (MCP) server for agent-phone-mcp.

Exposes phone-line capabilities (outbound calling, transcript retrieval,
inbound simulation, call logs) as MCP tools for AI agents.
"""
import sys
import os
import json
from typing import Dict, Any, List

# Support running directly or as a module
try:
    from .db import init_db
    from .call_manager import (
        initiate_outbound_call,
        record_inbound_call,
        get_call_transcript_by_id,
        list_recent_calls,
        get_agent_numbers,
    )
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.db import init_db
    from src.call_manager import (
        initiate_outbound_call,
        record_inbound_call,
        get_call_transcript_by_id,
        list_recent_calls,
        get_agent_numbers,
    )

# Initialize database schema
init_db()

TOOLS_SPEC = [
    {
        "name": "place_phone_call",
        "description": "Places an outbound phone call from the agent's phone line to a recipient, delivering a voice message and transcribing the conversation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "to_number": {
                    "type": "string",
                    "description": "Recipient phone number (e.g., +1-555-012-3456)."
                },
                "message": {
                    "type": "string",
                    "description": "The message or goal the agent wants to convey during the phone call."
                }
            },
            "required": ["to_number", "message"]
        }
    },
    {
        "name": "get_call_transcript",
        "description": "Retrieves the full speech-to-text transcript and summary for a past phone call by call ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "call_id": {
                    "type": "integer",
                    "description": "Unique call ID."
                }
            },
            "required": ["call_id"]
        }
    },
    {
        "name": "list_phone_calls",
        "description": "Lists recent inbound and outbound calls with their status, duration, and brief summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of recent calls to retrieve (default: 10)."
                }
            }
        }
    },
    {
        "name": "simulate_incoming_call",
        "description": "Simulates an inbound phone call from a customer or client delivering a voice message to the agent.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_number": {
                    "type": "string",
                    "description": "Caller phone number."
                },
                "speech_text": {
                    "type": "string",
                    "description": "What the caller says during the call."
                }
            },
            "required": ["from_number", "speech_text"]
        }
    },
    {
        "name": "get_agent_phone_numbers",
        "description": "Returns active phone numbers assigned to this agent.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Any:
    if name == "place_phone_call":
        return initiate_outbound_call(arguments.get("to_number", ""), arguments.get("message", ""))
    elif name == "get_call_transcript":
        res = get_call_transcript_by_id(int(arguments.get("call_id", 0)))
        return res if res else {"error": f"Call ID {arguments.get('call_id')} not found"}
    elif name == "list_phone_calls":
        limit = int(arguments.get("limit", 10))
        return list_recent_calls(limit=limit)
    elif name == "simulate_incoming_call":
        return record_inbound_call(arguments.get("from_number", ""), arguments.get("speech_text", ""))
    elif name == "get_agent_phone_numbers":
        return get_agent_numbers()
    else:
        return {"error": f"Unknown tool: {name}"}


def run_stdio_mcp():
    """Standard JSON-RPC 2.0 loop for MCP stdio transport."""
    sys.stderr.write("[MCP] agent-phone-mcp stdio server running...\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "agent-phone-mcp",
                            "version": "0.1.0"
                        }
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS_SPEC
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                result_data = handle_tool_call(tool_name, args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_data, indent=2)
                            }
                        ]
                    }
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not implemented"
                    }
                }

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"[MCP error] {str(e)}\n")
            sys.stderr.flush()


if __name__ == "__main__":
    run_stdio_mcp()
