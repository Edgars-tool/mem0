"""
Conversation Journal MCP Server
Journals conversations, reflections, and insights using Mem0.
Track key decisions, learnings, and insights from AI interactions.
"""

import os
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mem0 import MemoryClient

client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
app = Server("mem0-conversation-journal")

DEFAULT_USER = os.environ.get("MEM0_USER_ID", "journal_user")
DEFAULT_AGENT = "conversation-journal-mcp"

ENTRY_TYPES = ["insight", "decision", "reflection", "summary", "action", "question", "idea"]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="journal_entry",
            description="Add a journal entry: insight, decision, reflection, or summary from a conversation",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "The journal entry content"},
                    "entry_type": {
                        "type": "string",
                        "enum": ENTRY_TYPES,
                        "description": "Type of entry: insight, decision, reflection, summary, action, question, or idea",
                    },
                    "session": {"type": "string", "description": "Session or topic name (optional)"},
                    "importance": {
                        "type": "string",
                        "enum": ["low", "normal", "high", "critical"],
                        "description": "Importance level of this entry",
                    },
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="search_journal",
            description="Search journal entries semantically",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "entry_type": {
                        "type": "string",
                        "enum": ENTRY_TYPES + ["any"],
                        "description": "Filter by entry type (optional)",
                    },
                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_recent_entries",
            description="Get recent journal entries",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of recent entries to fetch (default: 10)", "default": 10},
                    "entry_type": {
                        "type": "string",
                        "enum": ENTRY_TYPES + ["any"],
                        "description": "Filter by entry type (optional)",
                    },
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="summarize_session",
            description="Get a summary of all journal entries for a specific session or topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "session": {"type": "string", "description": "Session or topic name to summarize"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["session"],
            },
        ),
        Tool(
            name="list_insights",
            description="List all insights and important learnings from the journal",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="list_decisions",
            description="List all decisions recorded in the journal",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="list_action_items",
            description="List all action items recorded in the journal",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="delete_entry",
            description="Delete a journal entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry_id": {"type": "string", "description": "Memory ID of the entry to delete"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["entry_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    user_id = arguments.get("user_id", DEFAULT_USER)

    if name == "journal_entry":
        content = arguments["content"]
        entry_type = arguments.get("entry_type", "insight")
        session = arguments.get("session", "")
        importance = arguments.get("importance", "normal")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        memory_text = f"[JOURNAL:{entry_type.upper()}]"
        if importance in ("high", "critical"):
            memory_text += f" [{importance.upper()}]"
        memory_text += f" {content}"
        if session:
            memory_text += f" | Session: {session}"
        memory_text += f" | Date: {timestamp}"

        result = client.add(
            [{"role": "user", "content": memory_text}],
            user_id=user_id,
            agent_id=DEFAULT_AGENT,
            metadata={"type": "journal", "entry_type": entry_type, "importance": importance, "session": session},
        )
        memory_id = result.get("results", [{}])[0].get("id", "unknown")
        return [TextContent(type="text", text=f"Journal entry saved!\nID: {memory_id}\nType: {entry_type} | Importance: {importance}\n{content}")]

    elif name == "search_journal":
        query = arguments["query"]
        entry_type = arguments.get("entry_type", "any")
        limit = arguments.get("limit", 10)
        results = client.search(query, user_id=user_id, agent_id=DEFAULT_AGENT, limit=limit)
        memories = results.get("results", [])
        if entry_type != "any":
            memories = [m for m in memories if f"[JOURNAL:{entry_type.upper()}]" in m.get("memory", "")]
        if not memories:
            return [TextContent(type="text", text=f"No journal entries found for: '{query}'")]
        items = []
        for i, m in enumerate(memories, 1):
            items.append(f"{i}. [{m.get('score', 'N/A'):.3f}] ID: {m['id']}\n   {m['memory'][:300]}{'...' if len(m['memory']) > 300 else ''}")
        return [TextContent(type="text", text=f"Found {len(memories)} journal entries for '{query}':\n\n" + "\n\n".join(items))]

    elif name == "get_recent_entries":
        limit = arguments.get("limit", 10)
        entry_type = arguments.get("entry_type", "any")
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = all_memories.get("results", [])
        if entry_type != "any":
            memories = [m for m in memories if f"[JOURNAL:{entry_type.upper()}]" in m.get("memory", "")]
        memories = memories[-limit:]
        if not memories:
            return [TextContent(type="text", text="No journal entries found.")]
        items = []
        for m in memories:
            items.append(f"- ID: {m['id']}\n  {m['memory'][:200]}{'...' if len(m['memory']) > 200 else ''}")
        return [TextContent(type="text", text=f"Recent journal entries ({len(memories)}):\n\n" + "\n\n".join(items))]

    elif name == "summarize_session":
        session = arguments["session"]
        results = client.search(session, user_id=user_id, agent_id=DEFAULT_AGENT, limit=50)
        memories = results.get("results", [])
        session_memories = [m for m in memories if session.lower() in m.get("memory", "").lower()]
        if not session_memories:
            return [TextContent(type="text", text=f"No journal entries found for session: '{session}'")]
        by_type = {}
        for m in session_memories:
            mem = m["memory"]
            for et in ENTRY_TYPES:
                if f"[JOURNAL:{et.upper()}]" in mem:
                    by_type.setdefault(et, []).append(mem)
                    break
            else:
                by_type.setdefault("other", []).append(mem)
        output = [f"Session Summary: {session}\n{'='*40}"]
        for et, entries in by_type.items():
            output.append(f"\n{et.upper()}S ({len(entries)}):")
            for e in entries:
                output.append(f"  - {e[:200]}")
        return [TextContent(type="text", text="\n".join(output))]

    elif name == "list_insights":
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = [m for m in all_memories.get("results", []) if "[JOURNAL:INSIGHT]" in m.get("memory", "")]
        if not memories:
            return [TextContent(type="text", text="No insights recorded yet.")]
        items = [f"- ID: {m['id']}\n  {m['memory']}" for m in memories]
        return [TextContent(type="text", text=f"All Insights ({len(memories)}):\n\n" + "\n\n".join(items))]

    elif name == "list_decisions":
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = [m for m in all_memories.get("results", []) if "[JOURNAL:DECISION]" in m.get("memory", "")]
        if not memories:
            return [TextContent(type="text", text="No decisions recorded yet.")]
        items = [f"- ID: {m['id']}\n  {m['memory']}" for m in memories]
        return [TextContent(type="text", text=f"All Decisions ({len(memories)}):\n\n" + "\n\n".join(items))]

    elif name == "list_action_items":
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = [m for m in all_memories.get("results", []) if "[JOURNAL:ACTION]" in m.get("memory", "")]
        if not memories:
            return [TextContent(type="text", text="No action items recorded yet.")]
        items = [f"- ID: {m['id']}\n  {m['memory']}" for m in memories]
        return [TextContent(type="text", text=f"All Action Items ({len(memories)}):\n\n" + "\n\n".join(items))]

    elif name == "delete_entry":
        entry_id = arguments["entry_id"]
        try:
            client.delete(entry_id)
            return [TextContent(type="text", text=f"Journal entry {entry_id} deleted.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error deleting entry: {str(e)}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
