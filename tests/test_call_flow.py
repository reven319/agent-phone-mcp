"""Unit tests for agent-phone-mcp."""
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import init_db
from src.call_manager import (
    initiate_outbound_call,
    record_inbound_call,
    get_call_transcript_by_id,
    list_recent_calls,
    get_agent_numbers,
)
from src.mcp_server import handle_tool_call


def test_db_and_agent_numbers():
    init_db()
    numbers = get_agent_numbers()
    assert len(numbers) >= 1
    assert "+1-555-019-2026" in numbers[0]["number"]


def test_outbound_call():
    res = initiate_outbound_call(to_number="+1-555-432-1000", message="Test alert message")
    assert res["status"] == "completed"
    assert "Test alert message" in res["summary"]
    assert res["call_id"] is not None

    transcript_res = get_call_transcript_by_id(res["call_id"])
    assert transcript_res is not None
    assert "Agent:" in transcript_res["transcript"]


def test_inbound_call():
    res = record_inbound_call(from_number="+1-555-999-8888", caller_speech="Need assistance with API keys")
    assert res["direction"] == "inbound"
    assert res["call_id"] is not None
    assert "Need assistance" in res["transcript"]


def test_mcp_tools():
    # Test tools/call via handle_tool_call
    numbers = handle_tool_call("get_agent_phone_numbers", {})
    assert isinstance(numbers, list)

    outbound = handle_tool_call("place_phone_call", {
        "to_number": "+1-555-123-4567",
        "message": "MCP agent test dispatch"
    })
    assert outbound["status"] == "completed"

    recent = handle_tool_call("list_phone_calls", {"limit": 5})
    assert len(recent) >= 1


if __name__ == "__main__":
    print("[test] Running test_db_and_agent_numbers...")
    test_db_and_agent_numbers()
    print("[test] Running test_outbound_call...")
    test_outbound_call()
    print("[test] Running test_inbound_call...")
    test_inbound_call()
    print("[test] Running test_mcp_tools...")
    test_mcp_tools()
    print("\n[ok] All tests passed successfully!")
