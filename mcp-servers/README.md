# Mem0 MCP Servers

A collection of practical Model Context Protocol (MCP) servers built on top of the Mem0 memory layer.

## Available MCP Servers

| Server | Description | Language |
|--------|-------------|----------|
| `task-memory/` | Task & project memory management MCP | Python |
| `knowledge-base/` | Personal knowledge base & notes MCP | Python |
| `conversation-journal/` | Conversation journal & reflection MCP | Python |

## Quick Start

All servers require a Mem0 API key. Get yours at [app.mem0.ai](https://app.mem0.ai).

```bash
pip install mem0ai mcp
export MEM0_API_KEY="m0-your-api-key"
```

## MCP Config (Claude Desktop / Cursor / Windsurf)

Add to your MCP config file:

```json
{
  "mcpServers": {
    "mem0-tasks": {
      "command": "python",
      "args": ["/path/to/mcp-servers/task-memory/server.py"],
      "env": { "MEM0_API_KEY": "m0-your-key" }
    },
    "mem0-knowledge": {
      "command": "python",
      "args": ["/path/to/mcp-servers/knowledge-base/server.py"],
      "env": { "MEM0_API_KEY": "m0-your-key" }
    },
    "mem0-journal": {
      "command": "python",
      "args": ["/path/to/mcp-servers/conversation-journal/server.py"],
      "env": { "MEM0_API_KEY": "m0-your-key" }
    }
  }
}
```

## License

Apache 2.0
