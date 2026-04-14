# Mem0 Identity Rules

This plugin follows Edgar's single-identity memory policy.

## Canonical identity

- `user_id` must always be `edgar`
- `agent_id` must always be `agent`

## Guardrails

- Do not create per-tool or per-model memory identities such as `codex`, `ollama`, `claude-code`, or `channel-fast`
- Do not store memory under technical transport names such as `mem0-mcp`
- Treat background workers as capabilities, not memory identities
- Session keys may differ, but memory storage and recall must converge on the same shared Mem0 scope

## Expected result

All assistants recall from the same shared pool, so a memory stored in one interaction remains searchable in later interactions regardless of which tool or background worker handled the task.
