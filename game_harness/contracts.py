"""Immutable agent/environment contract for a source-only game-harness example.

Design influence: Ascension's DecisionInput / EpisodeRuntimePort / legal-action
generation boundary, discovered through canonical Cognee hit Q01#1. This is an
independent Python implementation, not a port of the original Rust code.
Source: https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/policy_router.rs
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class Observation:
    """Only public game information; never includes unobserved opponent intent."""

    state_id: str
    generation: int
    turn: int
    player_health: int
    opponent_health: int
    visible_opponent_intent: str | None
    terminal: bool
    outcome: str | None
    last_event: str


@dataclass(frozen=True, slots=True)
class LegalActionSet:
    """Actions authorized for one exact source-of-truth observation generation."""

    state_id: str
    generation: int
    action_ids: tuple[str, ...]

    def contains(self, action_id: str) -> bool:
        return action_id in self.action_ids


@dataclass(frozen=True, slots=True)
class DecisionInput:
    observation: Observation
    legal_actions: LegalActionSet
    objective: str


@dataclass(frozen=True, slots=True)
class ActionIdentity:
    operation_id: str
    state_id: str
    generation: int
    action_id: str


@dataclass(frozen=True, slots=True)
class TransitionReceipt:
    status: Literal["SETTLED", "REJECTED", "UNKNOWN"]
    operation_id: str
    action_id: str
    before_state_id: str
    before_generation: int
    after: Observation | None
    effect_witness: str | None


class DecisionSource(Protocol):
    """An optional external model/controller owns the substantive next action."""

    def decide(self, decision_input: DecisionInput) -> str:
        """Return one action ID; the runner must still verify it against the catalog."""
        ...


class EnvironmentPort(Protocol):
    """Authoritative game boundary. No policy has direct mutation authority."""

    def observe(self) -> Observation:
        ...

    def legal_actions(self, state_id: str, generation: int) -> LegalActionSet:
        ...

    def dispatch_action(self, identity: ActionIdentity) -> TransitionReceipt:
        ...
