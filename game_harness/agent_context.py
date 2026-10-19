"""Episode-private, bounded decision context. Not authoritative game state.

Iteration 2 ADR-I2-001: BALROG public action/feedback history (I2-Q01#1),
Dexto session boundary (I2-Q03#16), and agent-runtime sliding context
(I2-Q06#1). Independently written Python; no upstream code copied.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .contracts import DecisionInput, Observation


@dataclass(frozen=True, slots=True)
class SettledEvent:
    """Only an observed, verified effect is admitted to next-turn history."""

    step_index: int
    action_id: str
    before_generation: int
    after_generation: int
    effect_witness: str
    feedback: str
    player_health: int
    opponent_health: int
    visible_opponent_intent: str | None


@dataclass(frozen=True, slots=True)
class AgentContext:
    """Ephemeral policy-private information, reset at each EpisodeRunner.run."""

    episode_state_id: str
    events: tuple[SettledEvent, ...] = ()
    subgoal: str = ""
    strategy_note: str = ""

    def after_settlement(
        self,
        *,
        step_index: int,
        action_id: str,
        before_generation: int,
        observation: Observation,
        effect_witness: str,
        subgoal: str,
        strategy_note: str,
        max_events: int,
        max_feedback_chars: int,
    ) -> AgentContext:
        """Append public feedback only after the runner accepts a settled receipt."""
        if observation.state_id != self.episode_state_id:
            raise ValueError("Agent context may not cross episode identities")
        if max_events < 1 or max_feedback_chars < 1:
            raise ValueError("Context budgets must be positive")
        if observation.generation <= before_generation:
            raise ValueError("Unsettled generation cannot enter agent history")
        event = SettledEvent(
            step_index=step_index,
            action_id=action_id,
            before_generation=before_generation,
            after_generation=observation.generation,
            effect_witness=effect_witness,
            feedback=observation.last_event[:max_feedback_chars],
            player_health=observation.player_health,
            opponent_health=observation.opponent_health,
            visible_opponent_intent=observation.visible_opponent_intent,
        )
        return AgentContext(
            episode_state_id=self.episode_state_id,
            events=(self.events + (event,))[-max_events:],
            subgoal=subgoal,
            strategy_note=strategy_note,
        )


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Untrusted external proposal. An action is never self-authorizing."""

    action_id: str
    subgoal: str = ""
    strategy_note: str = ""


@dataclass(frozen=True, slots=True)
class ContextualDecisionInput:
    decision: DecisionInput
    agent_context: AgentContext


class ContextualDecisionSource(Protocol):
    """Optional extension: legacy DecisionSource.decide remains supported."""

    def decide_with_context(self, request: ContextualDecisionInput) -> PolicyDecision:
        ...
