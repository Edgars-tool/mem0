"""
Knowledge Base MCP Server
Personal knowledge base and notes management using Mem0.
Save articles, learnings, code snippets, and notes with semantic search.
"""

import os
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mem0 import MemoryClient

client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
app = Server("mem0-knowledge-base")

DEFAULT_USER = os.environ.get("MEM0_USER_ID", "kb_user")
DEFAULT_AGENT = "knowledge-base-mcp"

CATEGORIES = ["article", "snippet", "learning", "reference", "idea", "note", "link"]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="save_knowledge",
            description="Save a piece of knowledge, note, snippet, or article to your personal knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title or short label for this knowledge"},
                    "content": {"type": "string", "description": "The content, note, snippet, or article text"},
                    "category": {
                        "type": "string",
                        "enum": CATEGORIES,
                        "description": "Category: article, snippet, learning, reference, idea, note, or link",
                    },
                    "tags": {"type": "string", "description": "Comma-separated tags (e.g. 'python,async,fastapi')"},
                    "source": {"type": "string", "description": "Source URL or reference (optional)"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="search_knowledge",
            description="Semantically search your personal knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural language search query"},
                    "category": {
                        "type": "string",
                        "enum": CATEGORIES + ["any"],
                        "description": "Filter by category (optional, defaults to 'any')",
                    },
                    "limit": {"type": "integer", "description": "Max results (default: 10)", "default": 10},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_knowledge",
            description="List all knowledge entries, optionally filtered by tag or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "description": "Filter by tag (optional)"},
                    "category": {"type": "string", "enum": CATEGORIES + ["any"], "description": "Filter by category (optional)"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="update_knowledge",
            description="Update an existing knowledge entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "knowledge_id": {"type": "string", "description": "Memory ID of the knowledge entry"},
                    "content": {"type": "string", "description": "New content to replace the existing entry"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["knowledge_id", "content"],
            },
        ),
        Tool(
            name="delete_knowledge",
            description="Delete a knowledge entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "knowledge_id": {"type": "string", "description": "Memory ID of the knowledge entry"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["knowledge_id"],
            },
        ),
        Tool(
            name="get_knowledge",
            description="Retrieve a specific knowledge entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "knowledge_id": {"type": "string", "description": "Memory ID of the knowledge entry"},
                },
                "required": ["knowledge_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    user_id = arguments.get("user_id", DEFAULT_USER)

    if name == "save_knowledge":
        title = arguments["title"]
        content = arguments["content"]
        category = arguments.get("category", "note")
        tags = arguments.get("tags", "")
        source = arguments.get("source", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        memory_text = f"[{category.upper()}] {title}\n{content}"
        if tags:
            memory_text += f"\nTags: {tags}"
        if source:
            memory_text += f"\nSource: {source}"
        memory_text += f"\nSaved: {timestamp}"

        result = client.add(
            [{"role": "user", "content": memory_text}],
            user_id=user_id,
            agent_id=DEFAULT_AGENT,
            metadata={"type": "knowledge", "category": category, "title": title, "tags": tags},
        )
        memory_id = result.get("results", [{}])[0].get("id", "unknown")
        return [TextContent(type="text", text=f"Knowledge saved!\nID: {memory_id}\nTitle: {title}\nCategory: {category}" + (f"\nTags: {tags}" if tags else ""))]

    elif name == "search_knowledge":
        query = arguments["query"]
        category = arguments.get("category", "any")
        limit = arguments.get("limit", 10)
        results = client.search(query, user_id=user_id, agent_id=DEFAULT_AGENT, limit=limit)
        memories = results.get("results", [])
        if category != "any":
            memories = [m for m in memories if f"[{category.upper()}]" in m.get("memory", "")]
        if not memories:
            return [TextContent(type="text", text=f"No knowledge found for: '{query}'")]
        items = []
        for i, m in enumerate(memories, 1):
            items.append(f"{i}. ID: {m['id']}\n   Score: {m.get('score', 'N/A')}\n   {m['memory'][:300]}{'...' if len(m['memory']) > 300 else ''}")
        return [TextContent(type="text", text=f"Found {len(memories)} result(s) for '{query}':\n\n" + "\n\n".join(items))]

    elif name == "list_knowledge":
        tag_filter = arguments.get("tag", "").lower()
        category_filter = arguments.get("category", "any")
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = all_memories.get("results", [])
        if category_filter != "any":
            memories = [m for m in memories if f"[{category_filter.upper()}]" in m.get("memory", "")]
        if tag_filter:
            memories = [m for m in memories if tag_filter in m.get("memory", "").lower()]
        if not memories:
            return [TextContent(type="text", text="No knowledge entries found.")]
        items = []
        for m in memories:
            preview = m["memory"][:150] + "..." if len(m["memory"]) > 150 else m["memory"]
            items.append(f"- ID: {m['id']}\n  {preview}")
        return [TextContent(type="text", text=f"Knowledge Base ({len(memories)} entries):\n\n" + "\n\n".join(items))]

    elif name == "update_knowledge":
        knowledge_id = arguments["knowledge_id"]
        content = arguments["content"]
        try:
            client.update(knowledge_id, content)
            return [TextContent(type="text", text=f"Knowledge entry {knowledge_id} updated successfully.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error updating knowledge: {str(e)}")]

    elif name == "delete_knowledge":
        knowledge_id = arguments["knowledge_id"]
        try:
            client.delete(knowledge_id)
            return [TextContent(type="text", text=f"Knowledge entry {knowledge_id} deleted.")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error deleting knowledge: {str(e)}")]

    elif name == "get_knowledge":
        knowledge_id = arguments["knowledge_id"]
        try:
            memory = client.get(knowledge_id)
            return [TextContent(type="text", text=f"ID: {knowledge_id}\n\n{memory.get('memory', 'Not found')}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error retrieving knowledge: {str(e)}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
