"""Original, tiny hidden-intent turn-based game. Not a benchmark or game clone.

The environment (not the agent) owns the hidden opponent intent, authorized
actions, transition outcomes, and settled effect witness. Source-level design
influence: Ascension Q01#1 → reviewed action/observation runtime port.
"""

from __future__ import annotations

import random

from .contracts import ActionIdentity, LegalActionSet, Observation, TransitionReceipt


class VeiledDuel:
    """One-player bounded encounter with partial observation and turn feedback.

    No STS2, Pokémon, MiniGrid, AI2-THOR, game assets or external model is used.
    A "probe" reveals the current intent without completing a turn, consumes
    a step/generation, and cannot be repeated during that turn.
    """

    def __init__(self, seed: int = 7, max_turns: int = 12):
        if seed < 0 or max_turns < 1:
            raise ValueError("seed must be non-negative and max_turns positive")
        self._seed = seed
        self._max_turns = max_turns
        self.reset()

    def reset(self) -> Observation:
        self._random = random.Random(self._seed)
        self._state_id = f"veiled-duel-{self._seed:x}"
        self._generation = 0
        self._turn = 0
        self._player_health = 12
        self._opponent_health = 12
        self._intent = self._draw_intent()
        self._probe_used = False
        self._terminal = False
        self._outcome: str | None = None
        self._last_event = "Encounter ready. The opponent's intent is hidden."
        self._seen_operations: set[str] = set()
        return self.observe()

    def _draw_intent(self) -> str:
        return self._random.choice(("strike", "guard", "feint"))

    def observe(self) -> Observation:
        return Observation(
            state_id=self._state_id,
            generation=self._generation,
            turn=self._turn,
            player_health=self._player_health,
            opponent_health=self._opponent_health,
            visible_opponent_intent=self._intent if self._probe_used and not self._terminal else None,
            terminal=self._terminal,
            outcome=self._outcome,
            last_event=self._last_event,
        )

    def legal_actions(self, state_id: str, generation: int) -> LegalActionSet:
        if state_id != self._state_id or generation != self._generation:
            raise ValueError("Stale or wrong-world legal-action request")
        if self._terminal:
            actions: tuple[str, ...] = ()
        else:
            options = ["strike", "brace"]
            if not self._probe_used:
                options.append("probe")
            if self._player_health < 12:
                options.append("mend")
            actions = tuple(options)
        return LegalActionSet(self._state_id, self._generation, actions)

    def _rejected(self, identity: ActionIdentity) -> TransitionReceipt:
        return TransitionReceipt(
            status="REJECTED",
            operation_id=identity.operation_id,
            action_id=identity.action_id,
            before_state_id=identity.state_id,
            before_generation=identity.generation,
            after=None,
            effect_witness=None,
        )

    def dispatch_action(self, identity: ActionIdentity) -> TransitionReceipt:
        """Mutate only after a fresh identity and authoritative legality check.

        A duplicate operation is rejected rather than replayed. This local demo
        never claims remote exactly-once execution or distributed recovery.
        """
        if (
            self._terminal
            or not identity.operation_id
            or identity.operation_id in self._seen_operations
            or identity.state_id != self._state_id
            or identity.generation != self._generation
        ):
            return self._rejected(identity)
        if not self.legal_actions(self._state_id, self._generation).contains(identity.action_id):
            return self._rejected(identity)

        before = self._generation
        self._seen_operations.add(identity.operation_id)
        if identity.action_id == "probe":
            self._probe_used = True
            self._last_event = "The opponent's current intent is now visible."
            witness = "intent-projection-revealed"
        else:
            intent = self._intent
            if identity.action_id == "strike":
                damage = 1 if intent == "guard" else 3
                self._opponent_health = max(0, self._opponent_health - damage)
            elif identity.action_id == "brace":
                self._opponent_health = max(0, self._opponent_health - 1)
            elif identity.action_id == "mend":
                self._player_health = min(12, self._player_health + 3)

            incoming = {"strike": 2, "guard": 0, "feint": 1}[intent]
            if identity.action_id == "brace":
                incoming = max(0, incoming - 2)
            self._player_health = max(0, self._player_health - incoming)
            self._turn += 1
            self._probe_used = False
            if self._opponent_health <= 0 and self._player_health <= 0:
                self._outcome = "DRAW"
            elif self._opponent_health <= 0:
                self._outcome = "VICTORY"
            elif self._player_health <= 0:
                self._outcome = "DEFEAT"
            elif self._turn >= self._max_turns:
                self._outcome = "TURN_LIMIT"
            self._terminal = self._outcome is not None
            if not self._terminal:
                self._intent = self._draw_intent()
            self._last_event = (
                f"Turn {self._turn}: {identity.action_id} resolved against "
                f"{intent}; player health {self._player_health}, "
                f"opponent health {self._opponent_health}."
            )
            witness = "turn-resolved"
        self._generation += 1
        return TransitionReceipt(
            status="SETTLED",
            operation_id=identity.operation_id,
            action_id=identity.action_id,
            before_state_id=self._state_id,
            before_generation=before,
            after=self.observe(),
            effect_witness=witness,
        )
