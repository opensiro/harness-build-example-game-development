"""Bounded game-playing agent runner with fail-closed source-evidence guards.

Adaptation of architectural *ideas*, not source code, from pinned Ascension:
- generation-matched legal-action admission (runner_actions.rs L235-267)
- fresh, settled effect receipt before progress (postconditions.rs L49-86)
The first recorded discovery was native Cognee Q01#1.
"""

from __future__ import annotations

from dataclasses import dataclass

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
    """Reject an inconsistent policy choice or an uncertain environment mutation."""


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
    """Policy decides; environment executes. The runner only admits and checks."""

    def __init__(
        self,
        environment: EnvironmentPort,
        policy: DecisionSource,
        *,
        max_decisions: int = 64,
        objective: str = "Finish the Veiled Duel without exceeding the budget",
    ):
        if max_decisions < 1:
            raise ValueError("max_decisions must be positive")
        if not objective.strip():
            raise ValueError("objective must not be empty")
        self.environment = environment
        self.policy = policy
        self.max_decisions = max_decisions
        self.objective = objective

    def run(self) -> RunReport:
        """Real episode operation. NOT invoked in this source-only experiment."""
        current = self.environment.observe()
        records: list[StepRecord] = []
        for step_index in range(self.max_decisions):
            if current.terminal:
                return RunReport("TERMINAL", current, tuple(records), self.max_decisions)
            catalog = self.environment.legal_actions(current.state_id, current.generation)
            verify_catalog(current, catalog)
            decision = self.policy.decide(
                DecisionInput(current, catalog, self.objective)
            )
            if not isinstance(decision, str) or not catalog.contains(decision):
                raise HarnessProtocolError("Policy chose an action not authorized for this generation")
            identity = ActionIdentity(
                operation_id=f"{current.state_id}:{current.generation}:{step_index}",
                state_id=current.state_id,
                generation=current.generation,
                action_id=decision,
            )
            receipt = self.environment.dispatch_action(identity)
            next_observation = verify_settlement(current, identity, receipt)
            records.append(
                StepRecord(
                    step_index=step_index,
                    action_id=decision,
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
        )
