"""
Task Memory MCP Server
Manages tasks, todos, and project memory using Mem0.
"""

import os
import json
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from mem0 import MemoryClient

# Initialize Mem0 client
client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
app = Server("mem0-task-memory")

DEFAULT_USER = os.environ.get("MEM0_USER_ID", "task_user")
DEFAULT_AGENT = "task-memory-mcp"


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add_task",
            description="Add a new task or todo item to memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Task description"},
                    "project": {"type": "string", "description": "Project name (optional)"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority"},
                    "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format (optional)"},
                    "user_id": {"type": "string", "description": "User ID (optional, defaults to env var)"},
                },
                "required": ["task"],
            },
        ),
        Tool(
            name="search_tasks",
            description="Search tasks and todos by keyword or project",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List all tasks, optionally filtered by project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Filter by project (optional)"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed and store the completion",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Memory ID of the task"},
                    "notes": {"type": "string", "description": "Completion notes (optional)"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="add_project_context",
            description="Add context, notes, or decisions for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Project name"},
                    "context": {"type": "string", "description": "Context or notes to remember"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["project", "context"],
            },
        ),
        Tool(
            name="get_project_summary",
            description="Get a summary of all memories for a project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Project name"},
                    "user_id": {"type": "string", "description": "User ID (optional)"},
                },
                "required": ["project"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    user_id = arguments.get("user_id", DEFAULT_USER)

    if name == "add_task":
        task = arguments["task"]
        project = arguments.get("project", "general")
        priority = arguments.get("priority", "medium")
        due_date = arguments.get("due_date", "")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        memory_text = f"[TASK] {task} | Project: {project} | Priority: {priority} | Created: {created_at}"
        if due_date:
            memory_text += f" | Due: {due_date}"
        memory_text += " | Status: pending"

        result = client.add(
            [{"role": "user", "content": memory_text}],
            user_id=user_id,
            agent_id=DEFAULT_AGENT,
            metadata={"type": "task", "project": project, "priority": priority, "status": "pending"},
        )
        memory_id = result.get("results", [{}])[0].get("id", "unknown")
        return [TextContent(type="text", text=f"Task added successfully!\nID: {memory_id}\nTask: {task}\nProject: {project} | Priority: {priority}")]

    elif name == "search_tasks":
        query = arguments["query"]
        results = client.search(query, user_id=user_id, agent_id=DEFAULT_AGENT, limit=10)
        memories = results.get("results", [])
        if not memories:
            return [TextContent(type="text", text=f"No tasks found for query: '{query}'")]
        items = []
        for m in memories:
            items.append(f"- ID: {m['id']}\n  {m['memory']}")
        return [TextContent(type="text", text=f"Found {len(memories)} result(s) for '{query}':\n\n" + "\n".join(items))]

    elif name == "list_tasks":
        project_filter = arguments.get("project")
        all_memories = client.get_all(user_id=user_id, agent_id=DEFAULT_AGENT)
        memories = all_memories.get("results", [])
        if project_filter:
            memories = [m for m in memories if project_filter.lower() in m.get("memory", "").lower()]
        if not memories:
            label = f"project '{project_filter}'" if project_filter else "user"
            return [TextContent(type="text", text=f"No tasks found for {label}.")]
        items = []
        for m in memories:
            items.append(f"- ID: {m['id']}\n  {m['memory']}")
        return [TextContent(type="text", text=f"Tasks ({len(memories)}):\n\n" + "\n".join(items))]

    elif name == "complete_task":
        task_id = arguments["task_id"]
        notes = arguments.get("notes", "")
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            memory = client.get(task_id)
            original = memory.get("memory", "")
            updated = original.replace("Status: pending", f"Status: completed | Completed: {completed_at}")
            if notes:
                updated += f" | Notes: {notes}"
            client.update(task_id, updated)
            return [TextContent(type="text", text=f"Task {task_id} marked as completed!\n{updated}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error completing task: {str(e)}")]

    elif name == "add_project_context":
        project = arguments["project"]
        context = arguments["context"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        memory_text = f"[PROJECT CONTEXT] Project: {project} | {context} | Recorded: {timestamp}"
        result = client.add(
            [{"role": "user", "content": memory_text}],
            user_id=user_id,
            agent_id=DEFAULT_AGENT,
            metadata={"type": "project_context", "project": project},
        )
        return [TextContent(type="text", text=f"Project context saved for '{project}'.\n{context}")]

    elif name == "get_project_summary":
        project = arguments["project"]
        results = client.search(project, user_id=user_id, agent_id=DEFAULT_AGENT, limit=20)
        memories = results.get("results", [])
        if not memories:
            return [TextContent(type="text", text=f"No memories found for project '{project}'.")]
        items = []
        for m in memories:
            items.append(f"- {m['memory']}")
        return [TextContent(type="text", text=f"Project Summary: {project}\n\n" + "\n".join(items))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
