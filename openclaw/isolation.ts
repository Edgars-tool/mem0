/**
 * Canonical memory identity helpers.
 *
 * Edgar's setup uses a single shared memory identity:
 * - user_id is always the stable Edgar identity
 * - agent_id is always the generic shared "agent" identity
 *
 * Session keys are still parsed where useful for diagnostics, but they no
 * longer influence which Mem0 agent namespace is used for storage or recall.
 */

export const CANONICAL_AGENT_ID = "agent";

// ============================================================================
// Trigger filtering — skip non-interactive sessions
// ============================================================================

/**
 * Triggers that should NOT run autocapture/autorecall.
 * These are system-initiated sessions (cron jobs, heartbeats, automation
 * pipelines) whose prompts would pollute the user's memory store.
 */
const SKIP_TRIGGERS = new Set(["cron", "heartbeat", "automation", "schedule"]);

/**
 * Returns true if the session trigger is non-interactive and memory
 * hooks should be skipped entirely.
 *
 * Also detects cron-style session keys (e.g. "agent:main:cron:<id>")
 * as a fallback when the trigger field is not set.
 */
export function isNonInteractiveTrigger(
  trigger: string | undefined,
  sessionKey: string | undefined,
): boolean {
  if (trigger && SKIP_TRIGGERS.has(trigger.toLowerCase())) return true;

  // Fallback: detect cron/heartbeat from the session key pattern
  if (sessionKey) {
    if (/:cron:/i.test(sessionKey) || /:heartbeat:/i.test(sessionKey))
      return true;
  }

  return false;
}

/**
 * Returns true if the session key indicates a subagent (ephemeral) session.
 * Subagent UUIDs are random per-spawn, so their namespaces are always empty
 * on recall and orphaned after capture.
 */
export function isSubagentSession(sessionKey: string | undefined): boolean {
  if (!sessionKey) return false;
  return /:subagent:/i.test(sessionKey);
}

/**
 * Parse an agent ID from a session key.
 *
 * OpenClaw session key formats:
 *   - Main agent:  "agent:main:main"
 *   - Subagent:    "agent:main:subagent:<uuid>"
 *   - Named agent: "agent:<agentId>:<session>"
 *
 * Returns the subagent UUID for subagent sessions, or the parsed agent ID for
 * named agents. This is a parser only; it does not determine Mem0 namespace.
 */
export function extractAgentId(
  sessionKey: string | undefined,
): string | undefined {
  if (!sessionKey) return undefined;

  // Check for subagent pattern: "agent:<parent>:subagent:<uuid>"
  const subagentMatch = sessionKey.match(/:subagent:([^:]+)$/);
  if (subagentMatch?.[1]) return `subagent-${subagentMatch[1]}`;

  // Check for named agent pattern: "agent:<agentId>:<session>"
  const match = sessionKey.match(/^agent:([^:]+):/);
  const agentId = match?.[1];
  if (!agentId) return undefined;
  if (agentId === "main") return "haodai";
  return agentId;
}

/**
 * Derive the effective user_id from a session key.
 * User identity stays stable across all agents.
 */
export function effectiveUserId(
  baseUserId: string,
  sessionKey?: string,
): string {
  void sessionKey;
  return baseUserId;
}

/** Preserve legacy export name, but always return the canonical shared agent id. */
export function agentUserId(baseUserId: string, agentId: string): string {
  void baseUserId;
  void agentId;
  return CANONICAL_AGENT_ID;
}

/**
 * Resolve user_id with priority: explicit userId > configured.
 */
export function resolveUserId(
  baseUserId: string,
  opts: { agentId?: string; userId?: string },
  currentSessionId?: string,
): string {
  void opts.agentId;
  void currentSessionId;
  if (opts.userId) return opts.userId;
  return baseUserId;
}

/**
 * Derive agent_id from the current session.
 * Edgar's memory policy uses one shared agent namespace for all tools.
 */
export function effectiveAgentId(
  sessionKey?: string,
): string | undefined {
  void sessionKey;
  return CANONICAL_AGENT_ID;
}

/**
 * Resolve agent_id to the canonical shared value, ignoring per-tool names.
 */
export function resolveAgentId(
  opts: { agentId?: string },
  currentSessionId?: string,
): string | undefined {
  void opts.agentId;
  void currentSessionId;
  return CANONICAL_AGENT_ID;
}
