# Iteration 2 — contextual game-harness interfaces

**Construction-only documentation:** no game run, model invocation, runtime unit test or gameplay CI was performed. The actual game entry point `python -m game_harness` remains opt-in and was **not invoked**.

## One-step external decision protocol

Veiled Duel and `EnvironmentPort` retain authority for `Observation`, generation-bound legal actions, and settled game transitions. The runner requests a decision; the external policy may choose among the provided action IDs but **cannot authorize or enact any action**.

JSONL request on stdout (illustrative shape, not a captured runtime message):

```json
{
  "type": "decision_request",
  "objective": "Finish the Veiled Duel without exceeding the budget",
  "observation": {"state_id": "veiled-duel-7", "generation": 1, "turn": 0, "player_health": 12, "opponent_health": 12, "visible_opponent_intent": "strike", "terminal": false, "outcome": null, "last_event": "The opponent's current intent is now visible."},
  "legal_actions": {"state_id": "veiled-duel-7", "generation": 1, "action_ids": ["strike", "brace", "mend"]},
  "agent_context": {
    "episode_state_id": "veiled-duel-7",
    "events": [
      {"step_index": 0, "action_id": "probe", "before_generation": 0, "after_generation": 1, "effect_witness": "intent-projection-revealed", "feedback": "The opponent's current intent is now visible.", "player_health": 12, "opponent_health": 12, "visible_opponent_intent": "strike"}
    ],
    "subgoal": "Avoid damage this turn",
    "strategy_note": "The probe revealed strike"
  }
}
```

The `agent_context` field is new and backward-compatible for policy processes that ignore additional request fields. Initial history is empty. Only **verified settled** transitions appear in `events`; the original `Observation` is public-only and no hidden opponent intent leaks before the game itself reveals it. The sample is schematic, not a gameplay result.

Policy reply on stdin:

```json
{"action_id":"brace","subgoal":"Stay alive","strategy_note":"Prefer defense after observed strike intent"}
```

Only `action_id` is required. Optional strings `subgoal` and `strategy_note` update policy-private context **after** authoritative settlement. Empty strings mean 'keep previous value'; there is no automatic goal synthesis. These notes cannot modify legal actions or game state. Existing external policy processes may continue returning only `{"action_id":"brace"}`.

## Native Python interfaces

- `DecisionSource.decide(DecisionInput) -> str` — existing provider-neutral legacy API.
- `ContextualDecisionSource.decide_with_context(ContextualDecisionInput) -> PolicyDecision` — opt-in API with `AgentContext`.
- `PolicyDecision.action_id` — untrusted proposal; `subgoal` and `strategy_note` are capped free-text hints.
- `AgentContext.after_settlement(...)` — constructs a new immutable episode context **only after** verified receipt. Sliding window contains recent settled public events.
- `EpisodeRunner.run()` — binds current public observation and legal catalog, receives a proposal, validates generation and legality, dispatches exactly once, validates settlement, records feedback, and continues.
- `RunReport.agent_context` — optional final policy-private context for later analysis, not an authoritative world snapshot.

`game_harness/veiled_duel.py`, `game_harness/contracts.py`, and the original public `DecisionSource` are unchanged. No new game engine, Cognee runtime dependency, new model client, scheduler or control plane.

## Bounded failure behavior

Defaults in `EpisodeRunner`: `max_decisions=64`, `max_context_events=8`, `max_feedback_chars=512`, `max_subgoal_chars=256`, `max_strategy_chars=512`. `JSONLinesDecisionSource` sets `max_request_bytes=32768` and `max_reply_bytes=4096`; oversized/malformed/unavailable replies fail closed **before** environment dispatch. The runner never retries an uncertain environment effect; an unsettled/identity-mismatched receipt raises `HarnessProtocolError` before updating memory.

An arbitrary `TextIO.readline` can still block indefinitely waiting for a reply, and `write` / `flush` may block. **No generic latency timeout guarantee** is claimed. Users must supervise the external process with an independent timeout mechanism as needed; this construction does not add one. A bounded recent-event history is **not** semantic summarization or an exact model token budget. A class/API definition is **not** proof of runtime correctness.

## Reproduce source-only inspection (not game execution)

```bash
git checkout experiment/game-cognee-iteration-2-20261019
python3 iteration-2/tools/check_static.py
```

The checker reads source text and Python AST without importing `game_harness`; it never calls `EpisodeRunner.run`, provider APIs, or any game module. `python -m game_harness` remains prohibited in this experiment. See [C3 ADR](../reports/C3-architecture-decision.md), [new discovery](../reports/C2-discovery.md), and [original first iteration](../../README.md).
