# Iteration 2 — source-to-code traceability

**Run:** `game-iter2-20261019`. Comparison predecision commit `0184e3d7e1432e6209ca248c4a075f2c5c7dbd89`; ADR-before-code commit `1bc4828ca94232373e8585f04f11d576f59deb8e`; first source change `01b77fe04d7e4ba8dad0cf9db1e08b0fdd207762`.

The new Cognee corpus is `opensiro/vsm-harness-index@5cbb1035538b8f80fa3362f1c99652f4fd7c55e8` via OpenSiro connector `d176484e85da55c84450d67040cb4a2d096353c7`. See [C2 archived receipts](../receipts/discovery/) and [C2 chronology reconciliation](C2-reconciliation.md). Native hits come from **six function sections**, not full Markdown search. VSM grades are ownership metadata, not engineering-performance rankings.

| Requirement | Cognee discovery and canonical source | Inspected upstream pinned source | Comparison / architecture | Locally authored implementation |
|---|---|---|---|---|
| R2/R5: feed settled public experience into later decisions | `I2-Q01#1` BALROG, [full assessment](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/ba/balrog.md) | [BALROG `NaiveAgent.act`](https://github.com/balrog-ai/BALROG/blob/b7afe79e3e4265811cfa985ed7c95c4d1a11e3f5/balrog/agents/naive.py#L14-L41) | [C3a](C3-candidate-comparison.md) → ADR I2-M1; alternative BabyAI `I2-Q01#3` rejected for deep neural policy requirements; `discovery_contribution=DIRECT` | `game_harness/agent_context.py`: `SettledEvent`, `AgentContext.after_settlement`; `game_harness/runner.py`: context update strictly **after** receipt verification |
| R1/R3/R5: external strategy and subgoal are untrusted policy-private data | `I2-Q03#16` + `I2-Q06#18` Dexto, [full assessment](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/de/dexto.md) | [Dexto `ChatSession`](https://github.com/truffle-ai/dexto/blob/ac56fbfcd8e7a682fc0e96c690e5b6362980181d/packages/core/src/session/chat-session.ts#L65-L160) | [C3a](C3-candidate-comparison.md) → ADR I2-M2; full provider framework/persistent session rejected; `discovery_contribution=DIRECT` | `game_harness/agent_context.py`: `PolicyDecision` and `ContextualDecisionInput`; `game_harness/policy_jsonl.py`: context-aware message and optional note fields; `runner.py`: bounded policy metadata |
| R4/R6: keep event context small, fail closed on invalid source | `I2-Q06#1` agent-runtime, [full assessment](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/ag/agent-runtime.md) | [Rust `WorkflowContext`](https://github.com/tsharp/agent-runtime/blob/07ebca8ec36d15eae2d264d4998fa6857f9e0b51/src/context/mod.rs#L1-L125) | [C3a](C3-candidate-comparison.md) → ADR I2-M3; agent-runtime token/summarization strategies not copied; `discovery_contribution=DIRECT` for bounded FIFO history, `CORROBORATIVE` for preexisting local fail-closed checks | `agent_context.py`: FIFO `events[-max_events:]`; `runner.py`: context and notes caps, legacy policy compatibility and no blind retry; `policy_jsonl.py`: request/reply size bounds |
| R5: existing authoritative execution boundary | Original Iteration 1 `Q01#1` Ascension is **not** a fresh adapted mechanism here (though newly surfaced as `I2-Q01#2`) | Original Iteration 1 source ref, unchanged | **PRESERVE**, no adaptation credit | `game_harness/contracts.py` and `veiled_duel.py` remain byte-identical to `main@3a93532d` |

## What is local design vs borrowed principle?

All new Python files/code are independently authored. BALROG informed action/feedback prompt continuity, not its evaluator/client. Dexto informed session-local separation, not its services. agent-runtime informed a finite window, not its Rust context manager. **Neither a source hit nor the existence of a new class proves runtime behavior.**

The flow is **public observe → recent settled context → external policy decision → generation-bound catalog validation → one authoritative dispatch → settlement verification → append feedback/optional notes → next decision**. Control of hidden game state never crosses into the policy module; the agent's strategy notes are not executable game commands.

## Evidence and verification limitations

- Search index: 3,498 function-section chunks; complete 583 documents ingested but **not full-document searchable** in this experiment.
- Deterministic finite event history is not semantic memory or long-horizon planning quality.
- A `TextIO` policy source can still block; byte/event limits and fail-closed errors are not a wall-clock timeout guarantee.
- [Static receipt](../receipts/verification/static-check.json) verifies AST/source/Git evidence only; runtime correctness and gameplay quality are `NOT_RUN` / `NOT_EVALUATED`.
