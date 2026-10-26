# Product Hunt Launch Kit — Agent Phone MCP

> Ready-to-copy submission kit for launching on [Product Hunt](https://www.producthunt.com/posts/new).

---

## 1. Core Listing Info

* **Name:** `Agent Phone MCP`
* **Tagline (under 60 chars):**
  > Dedicated phone lines & live call voice tools for AI agents
* **Link / GitHub:** `https://github.com/your-username/agent-phone-mcp` (or your repo/demo URL)
* **Pricing:** `Free` / `Open Source`
* **Topics / Tags:**
  * `Artificial Intelligence`
  * `Developer Tools`
  * `Open Source`
  * `Tech`
  * `API`

---

## 2. Description (Markdown / Formatted)

**Short Pitch:**
> Agent Phone MCP is an open-source, local-first Model Context Protocol (MCP) server that equips AI agents (in Claude Code, Cursor, Antigravity) with dedicated voice lines. It enables agents to place outbound calls, receive customer voice messages, and auto-transcribe calls directly into the agent's context window.

**Key Highlights:**
* 📞 **Autonomous Calling:** Agents can dispatch voice calls to alert humans, confirm appointments, or verify operational status.
* 🎙️ **Inbound Voice Bridge:** Webhook handler transcribes incoming caller voice messages and presents them as structured MCP tool responses.
* 🔒 **Local-First & Private:** Embedded SQLite storage with zero mandatory cloud lock-in or third-party audio recording retention.
* ⚡ **Zero-Dependency Core:** Runs out-of-the-box on standard Python with built-in JSON-RPC stdio transport for any MCP client.

---

## 3. First Maker Comment (Copy & Paste)

```markdown
Hey Product Hunt! 👋

Over the past year, AI agents in tools like Claude Code, Cursor, and Antigravity have become incredible at editing code, searching docs, and executing terminal commands. But they were still trapped behind a text screen. 

When an agent needs to alert an on-call engineer, confirm an urgent client request, or take an incoming customer voice message, setting up commercial voice SaaS often means paying heavy monthly subscriptions and handing audio retention to third-party clouds.

We built **Agent Phone MCP** to solve this:
- **100% Open & Local-First:** Built around the open Model Context Protocol (MCP) standard.
- **5 Native Agent Tools:** Outbound calling, incoming call listener, real-time speech transcription, and call history querying.
- **Dual Transport:** Runs via standard stdio for local agent sessions, or as an HTTP webhook bridge for live VoIP/SIP providers like Twilio.

The project is completely open source under MIT. We’d love to hear your feedback, see what custom voice workflows you build, and answer any questions!
```

---

## 4. Visuals Checklist

When submitting on Product Hunt:
1. **Thumbnail (240x240):** An icon combining a phone handset with a robotic/agent circuit badge.
2. **Screenshots (1270x760 recommended):**
   * Screenshot 1: Agent terminal session invoking `place_phone_call` via MCP.
   * Screenshot 2: Structured JSON-RPC transcript delivered into Claude Code / Cursor.
   * Screenshot 3: SQLite call log & audit table schema.
