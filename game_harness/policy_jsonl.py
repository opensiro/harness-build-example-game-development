"""Provider-agnostic JSON-lines decision boundary for an external AI agent.

stdout transmits public observations and allowed actions; stdin must supply a
single JSON object {"action_id": "..."} per turn. The bridge does not select
or invoke any particular model, prompt provider, simulator, or evaluation API.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from typing import TextIO

from .contracts import DecisionInput


class JSONLinesDecisionSource:
    """Machine-readable external policy bridge. No built-in model inference."""

    def __init__(self, requests: TextIO, replies: TextIO):
        self.requests = requests
        self.replies = replies

    def decide(self, decision_input: DecisionInput) -> str:
        message = {
            "type": "decision_request",
            "objective": decision_input.objective,
            "observation": asdict(decision_input.observation),
            "legal_actions": asdict(decision_input.legal_actions),
        }
        self.requests.write(json.dumps(message, sort_keys=True) + "\n")
        self.requests.flush()
        line = self.replies.readline()
        if not line:
            raise ValueError("Decision source closed without providing an action")
        try:
            reply = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("Decision source returned malformed JSON") from exc
        if not isinstance(reply, dict) or not isinstance(reply.get("action_id"), str):
            raise ValueError('Decision reply must be {"action_id": "<legal action>"}')
        return reply["action_id"]
