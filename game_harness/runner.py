"""Bounded Observe → Context → Decide → Validate → Execute → Feedback loop.

The environment alone authorizes and mutates game state. Iteration 2 context
records only verified public effects (I2-M1), accepts external strategy notes
(I2-M2), and bounds episode-local event history (I2-M3). Runtime NOT_RUN.
"""

from __future__ import annotations

from dataclasses import dataclass

from .agent_context import AgentContext, ContextualDecisionInput, PolicyDecision
from .contracts import (
    ActionIdentity,
    DecisionInput,
    DecisionSource,
    EnvironmentPort,
    LegalActionSet,
    Observation,
    TransitionReceipt,
)


class HarnessProtocolError(RuntimeError):
    """Fail closed on invalid policy choice, source failure or uncertain effect."""


@dataclass(frozen=True, slots=True)
class StepRecord:
    step_index: int
    action_id: str
    operation_id: str
    before_generation: int
    after_generation: int
    effect_witness: str


@dataclass(frozen=True, slots=True)
class RunReport:
    stop_reason: str
    observation: Observation
    decisions: tuple[StepRecord, ...]
    max_decisions: int
    agent_context: AgentContext | None = None


def verify_catalog(observation: Observation, catalog: LegalActionSet) -> None:
    if catalog.state_id != observation.state_id or catalog.generation != observation.generation:
        raise HarnessProtocolError("Legal-action catalog is not bound to the current observation")
    if not catalog.action_ids:
        raise HarnessProtocolError("Nonterminal environment did not offer a legal action")
    if len(set(catalog.action_ids)) != len(catalog.action_ids):
        raise HarnessProtocolError("Duplicated legal action IDs")
    if any(not isinstance(action, str) or not action.strip() for action in catalog.action_ids):
        raise HarnessProtocolError("Malformed action ID")


def verify_settlement(
    before: Observation, identity: ActionIdentity, receipt: TransitionReceipt
) -> Observation:
    """An acknowledgement or ambiguous result cannot prove a state mutation."""
    if receipt.status != "SETTLED":
        raise HarnessProtocolError(
            f"Effect is not settled ({receipt.status}); stop without blind retry"
        )
    if (
        receipt.operation_id != identity.operation_id
        or receipt.action_id != identity.action_id
        or receipt.before_state_id != identity.state_id
        or receipt.before_generation != identity.generation
    ):
        raise HarnessProtocolError("Operation identity mismatch")
    if receipt.after is None or not receipt.effect_witness:
        raise HarnessProtocolError("No fresh observation or effect witness")
    if receipt.after.state_id != before.state_id:
        raise HarnessProtocolError("Cross-environment receipt")
    if receipt.after.generation <= before.generation:
        raise HarnessProtocolError("Post-action observation is not fresher than pre-action")
    return receipt.after


class EpisodeRunner:
    """The external source decides; only the environment executes.

    Legacy DecisionSource.decide(DecisionInput)->str remains supported. A source
    with decide_with_context(ContextualDecisionInput)->PolicyDecision receives
    bounded episode-private history and may propose a subgoal/strategy note.
    """

    def __init__(
        self,
        environment: EnvironmentPort,
        policy: DecisionSource,
        *,
        max_decisions: int = 64,
        objective: str = "Finish the Veiled Duel without exceeding the budget",
        max_context_events: int = 8,
        max_feedback_chars: int = 512,
        max_subgoal_chars: int = 256,
        max_strategy_chars: int = 512,
    ):
        if max_decisions < 1:
            raise ValueError("max_decisions must be positive")
        if not objective.strip():
            raise ValueError("objective must not be empty")
        if min(max_context_events, max_feedback_chars, max_subgoal_chars, max_strategy_chars) < 1:
            raise ValueError("Agent context budgets must be positive")
        self.environment = environment
        self.policy = policy
        self.max_decisions = max_decisions
        self.objective = objective
        self.max_context_events = max_context_events
        self.max_feedback_chars = max_feedback_chars
        self.max_subgoal_chars = max_subgoal_chars
        self.max_strategy_chars = max_strategy_chars

    def _propose(self, decision: DecisionInput, context: AgentContext) -> PolicyDecision:
        """Errors from the decision source stop the episode before dispatch."""
        try:
            contextual = getattr(self.policy, "decide_with_context", None)
            if callable(contextual):
                proposal = contextual(ContextualDecisionInput(decision, context))
            else:
                proposal = self.policy.decide(decision)
        except (EOFError, OSError, TimeoutError, UnicodeError, ValueError) as exc:
            raise HarnessProtocolError("Decision source failed before environment dispatch") from exc

        if isinstance(proposal, str):
            proposal = PolicyDecision(action_id=proposal)
        if not isinstance(proposal, PolicyDecision):
            raise HarnessProtocolError("Decision source must return an action or PolicyDecision")
        if not isinstance(proposal.action_id, str):
            raise HarnessProtocolError("Decision proposal has no string action ID")
        if not isinstance(proposal.subgoal, str) or not isinstance(proposal.strategy_note, str):
            raise HarnessProtocolError("Policy-private metadata must be strings")
        if (
            len(proposal.subgoal) > self.max_subgoal_chars
            or len(proposal.strategy_note) > self.max_strategy_chars
        ):
            raise HarnessProtocolError("Policy-private metadata exceeds declared budget")
        if not decision.legal_actions.contains(proposal.action_id):
            raise HarnessProtocolError("Policy chose an action not authorized for this generation")
        return proposal

    def run(self) -> RunReport:
        """An opt-in real episode. NOT invoked in the construction experiment."""
        current = self.environment.observe()
        context = AgentContext(episode_state_id=current.state_id)
        records: list[StepRecord] = []
        for step_index in range(self.max_decisions):
            if current.terminal:
                return RunReport(
                    "TERMINAL", current, tuple(records), self.max_decisions, context
                )
            catalog = self.environment.legal_actions(current.state_id, current.generation)
            verify_catalog(current, catalog)
            proposal = self._propose(DecisionInput(current, catalog, self.objective), context)
            identity = ActionIdentity(
                operation_id=f"{current.state_id}:{current.generation}:{step_index}",
                state_id=current.state_id,
                generation=current.generation,
                action_id=proposal.action_id,
            )
            # Dispatch exactly once; no retry when a side effect is uncertain.
            receipt = self.environment.dispatch_action(identity)
            next_observation = verify_settlement(current, identity, receipt)
            # Policy context changes ONLY after verified settlement.
            context = context.after_settlement(
                step_index=step_index,
                action_id=proposal.action_id,
                before_generation=current.generation,
                observation=next_observation,
                effect_witness=receipt.effect_witness or "",
                subgoal=proposal.subgoal or context.subgoal,
                strategy_note=proposal.strategy_note or context.strategy_note,
                max_events=self.max_context_events,
                max_feedback_chars=self.max_feedback_chars,
            )
            records.append(
                StepRecord(
                    step_index=step_index,
                    action_id=proposal.action_id,
                    operation_id=identity.operation_id,
                    before_generation=current.generation,
                    after_generation=next_observation.generation,
                    effect_witness=receipt.effect_witness or "",
                )
            )
            current = next_observation
        return RunReport(
            "TERMINAL" if current.terminal else "DECISION_BUDGET_EXHAUSTED",
            current,
            tuple(records),
            self.max_decisions,
            context,
        )
