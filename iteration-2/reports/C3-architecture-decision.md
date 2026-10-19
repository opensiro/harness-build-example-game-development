# ADR-I2-001 — Episode-local contextual agent loop (C3b)

**Decision:** ADOPT a bounded three-part adaptation of the unchanged Veiled Duel harness.
**Stage:** C3b; documented **after** the [C3a comparison commit `0184e3d7e1432e6209ca248c4a075f2c5c7dbd89`](https://github.com/opensiro/harness-build-example-game-development/commit/0184e3d7e1432e6209ca248c4a075f2c5c7dbd89) and the [passing new C2 discovery commit `3a6b7debecb5719c4319eef9579d143a6f3062d1`](https://github.com/opensiro/harness-build-example-game-development/commit/3a6b7debecb5719c4319eef9579d143a6f3062d1). **No Iteration 2 code was adapted at the time of this decision.**
**Run:** `game-iter2-20261019`. The unchanged Iteration 1 build is `main@3a93532d70b6dccad2d5e83a7a0e6532456fff6b`.

## Design choice, retrieval and alternatives

| Decision | Requirement → native query hit → full assessment → pinned upstream inspection | Selected independent adaptation | discovery_contribution |
|---|---|---|---|
| **I2-M1: Settled public feedback history** | R2/R5 → `I2-Q01#1` BALROG → [canonical BALROG](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/ba/balrog.md) → [pinned `NaiveAgent.act`](https://github.com/balrog-ai/BALROG/blob/b7afe79e3e4265811cfa985ed7c95c4d1a11e3f5/balrog/agents/naive.py#L14-L41) + [evaluator feedback](https://github.com/balrog-ai/BALROG/blob/b7afe79e3e4265811cfa985ed7c95c4d1a11e3f5/balrog/evaluator.py#L245-L345) | A **public-observation-only**, episode-scoped event sequence updated **after** `verify_settlement`; policy sees settled last action and its effect next turn; never receives hidden game state | **DIRECT** — first recorded mechanism lead came from new Q01#1; BabyAI Q01#3 is an independent corroborating option |
| **I2-M2: Strategy/goal in external decision envelope** | R1/R3/R5 → `I2-Q03#16` and `I2-Q06#18` Dexto → [canonical Dexto](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/de/dexto.md) → [pinned session context](https://github.com/truffle-ai/dexto/blob/ac56fbfcd8e7a682fc0e96c690e5b6362980181d/packages/core/src/session/chat-session.ts#L65-L160) | Optional bounded `strategy_note` and `subgoal` in external policy reply; a context-aware decision interface wraps the already-frozen `DecisionInput`. Notes live in agent context, **never** modify authoritative observation/legal actions; preserve legacy `decide(DecisionInput)->str` providers | **DIRECT** — the retrieved Dexto session boundary and pinned source materially shaped a separate context envelope |
| **I2-M3: Deterministic bounded sliding context and fail-closed source budgets** | R4/R6 → `I2-Q06#1` agent-runtime → [canonical agent-runtime](https://github.com/opensiro/vsm-harness-index/blob/5cbb1035538b8f80fa3362f1c99652f4fd7c55e8/assessments/ag/agent-runtime.md) → [pinned `WorkflowContext`](https://github.com/tsharp/agent-runtime/blob/07ebca8ec36d15eae2d264d4998fa6857f9e0b51/src/context/mod.rs#L1-L125) | Fixed-size FIFO of settled public event records, bounded note/message/reply strings, existing `max_decisions`, no blind retry after malformed/failed policy or ambiguous environment outcome | **DIRECT** for the sliding-history limit, **CORROBORATIVE** for fail-closed behavior (already required by local baseline; no claim the retrieval originated its safety gate) |

Each selection has a complete provenance chain: `Requirement → native Cognee I2 query and hit → pinned included assessment → pinned upstream file → C3a alternatives → this ADR → new source in C4`. The hits came from a dataset of **583 full imported Markdown documents** with only **3,498 six-function lexical chunks** searchable. This is not whole-document retrieval, a model-performance ranking, or a claim that a VSM autonomy grade confers better game performance. I2-Q08 returned irrelevant negative-control hits; preserve them.

## Rejections

- **NO_ADAPTATION**: existing generation/settlement boundary is valuable but has no explicit feedback history or agent-private longitudinal strategy; fails R2/R3/R4.
- **Neural memory** (BabyAI), **cross-run skill distillation** (Genesis Agent), **self-editing and cross-run reconfiguration** (Continual Harness): stronger claims require model/training/persistent storage or unapproved provider actions.
- **Full external orchestration/control plane** (LLaMAR, HumanLayer, full Dexto) and **Rust context-runtime port** (agent-runtime): unnecessary for a single game; no code copied.
- **Automatic summarization/tokenization**: source-only run without LLM inference cannot justify calling it semantic summarization, and char/event limits are not true token budgets.
- **Automatic retries/timeouts on arbitrary stdin**: blocking `TextIO.readline` has no generic guaranteed wall-clock timeout. Do not claim one. A caller can use an external decision process with its own timeout supervision; parse, byte caps and failures must fail closed locally.

## Implementation contract (BEFORE adaptation)

1. Add a small provider-neutral **episode context** module, no Cognee runtime dependency, with immutable snapshots, bounded public transition history, and optional policy-private `subgoal`/`strategy_note` strings.
2. Add a **contextual decision envelope**, retaining existing legacy `DecisionSource.decide` clients. JSONL replies may contain `action_id` and optional bounded `subgoal` and `strategy_note`. Absence keeps existing contract valid.
3. Extend `EpisodeRunner` to assemble context for each decision, verify legal action, dispatch once, verify a fresh settled receipt, and **only then** advance context. Policy errors raise `HarnessProtocolError` before dispatch; no retries of uncertain effects.
4. Bound history lengths and serialized JSONL request/reply sizes; preserve `max_decisions` and terminal semantics. Validate the external policy metadata as untrusted data.
5. Expose public input/output contract and source-to-code mapping; no model is selected, no game/provider/test CI run. Source/AST/static checks are allowed but do not prove functionality.

**Stop boundary:** implementation is permitted **only in commits after this ADR's Git SHA**. C4 must record an implementation SHA descendant and separate final source verification; keep Iteration 1 receipts immutable. `runtime_status=NOT_RUN`, `evaluation_level=NOT_RUN`, `model_quality_claim=NOT_EVALUATED`.
