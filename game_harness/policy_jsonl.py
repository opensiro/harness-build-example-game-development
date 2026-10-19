"""Provider-neutral JSON-lines bridge for an external AI decision process.

A request includes the current authoritative *public* observation/catalog and,
for context-aware runs, a bounded policy-private episode history. The external
reply proposes one action ID and optional policy notes. It does not execute a
game action or supply authoritative environmental state. Runtime NOT_RUN.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from typing import TextIO

from .agent_context import ContextualDecisionInput, PolicyDecision
from .contracts import DecisionInput


class JSONLinesDecisionSource:
    """No model provider calls; transport only, with bounded message sizes.

    A line read from an arbitrary TextIO stream has no generic wall-clock
    timeout. Host/process supervision must enforce one where necessary.
    """

    def __init__(
        self,
        requests: TextIO,
        replies: TextIO,
        *,
        max_request_bytes: int = 32768,
        max_reply_bytes: int = 4096,
    ):
        if max_request_bytes < 1 or max_reply_bytes < 1:
            raise ValueError("JSONL message budgets must be positive")
        self.requests = requests
        self.replies = replies
        self.max_request_bytes = max_request_bytes
        self.max_reply_bytes = max_reply_bytes

    def _exchange(
        self, decision_input: DecisionInput, *, agent_context: object | None
    ) -> PolicyDecision:
        message = {
            "type": "decision_request",
            "objective": decision_input.objective,
            "observation": asdict(decision_input.observation),
            "legal_actions": asdict(decision_input.legal_actions),
        }
        if agent_context is not None:
            message["agent_context"] = asdict(agent_context)
        serialized = json.dumps(message, sort_keys=True)
        if len(serialized.encode("utf-8")) > self.max_request_bytes:
            raise ValueError("Decision request exceeds JSONL byte budget")
        self.requests.write(serialized + "\n")
        self.requests.flush()

        # readline(size) bounds memory use for invalid or oversized replies.
        line = self.replies.readline(self.max_reply_bytes + 1)
        if not line:
            raise ValueError("Decision source closed without providing an action")
        if len(line.encode("utf-8")) > self.max_reply_bytes:
            raise ValueError("Decision source reply exceeds JSONL byte budget")
        try:
            reply = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("Decision source returned malformed JSON") from exc
        if not isinstance(reply, dict) or not isinstance(reply.get("action_id"), str):
            raise ValueError('Decision reply must include {"action_id": "<legal action>"}')
        for optional in ("subgoal", "strategy_note"):
            if optional in reply and not isinstance(reply[optional], str):
                raise ValueError(f"{optional} must be a string")
        return PolicyDecision(
            action_id=reply["action_id"],
            subgoal=reply.get("subgoal", ""),
            strategy_note=reply.get("strategy_note", ""),
        )

    def decide(self, decision_input: DecisionInput) -> str:
        """Backward-compatible action-only interface for existing users."""
        return self._exchange(decision_input, agent_context=None).action_id

    def decide_with_context(self, request: ContextualDecisionInput) -> PolicyDecision:
        """Return an untrusted proposed action/notes, not an applied transition."""
        return self._exchange(request.decision, agent_context=request.agent_context)
