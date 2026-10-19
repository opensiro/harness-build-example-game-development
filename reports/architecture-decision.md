# C3b — Architecture Decision ADR-001

**Decision status:** ADOPTED after comparison, before any game-harness implementation.  
**Comparison ancestor:** `f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0` ([candidate comparison](https://github.com/opensiro/harness-build-example-game-development/commit/f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0)).  
**C2 ancestor:** `d6c757f701501f1f555c009d5163c6852e33e33f`.  
**Cognee contribution:** `DIRECT` (narrow: first recorded source of the selected source-backed mechanism in this independent experiment).  
**Adaptation outcome:** `ADAPTED` — pending C4 implementation.

## Decision

Select **OPT-A — the bounded generation-bound legal-action and verified transition pattern discovered in Ascension** via native `Q01#1`, rather than the full Ascension Rust/MCP/control-plane architecture. This is a fresh Python source adaptation, not a source code copy.

Build an original **Veiled Duel** game environment: a tiny, turn-based, imperfect-information duel with a hidden opponent intent, a bounded turn/step budget, and a single agent's legal choices such as attack, defend, peek and recover. The game, rules, names, balance and deterministic environment adapter will be written specifically for this experiment. No imported game ROM, STS2 gameplay content, benchmark, external simulator, model or provider is required.

Expose a policy `DecisionSource` protocol that can be implemented by an external model/agent; provide a JSON-lines policy bridge and no embedded model call. The environment alone owns the true game state and hidden intent. The model receives only an immutable public `DecisionInput` containing observation, generation-bound permitted actions and objective. The runner must reject choices not in the *current* legal-action catalog. After an admitted action it must verify the environment's settled receipt, operation identity, effect witness and strictly newer state generation before making the next choice. Unknown effects must **fail closed**, not be retried blindly. This source-only synchronous demo will not pretend to implement Ascension's full distributed recovery or authenticated management machinery.

### Explicit trace from first discovery

`Q01#1` (actual native `SearchType.CHUNKS_LEXICAL` hit, original in `receipts/discovery/native-search-Q01.json`) → complete pinned Index [Ascension assessment](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/as/ascension.md), assessment SHA256 `cd2a74a004f62a4bcf11fa2185d94e767b02ce3b23b2ec012ca86f44619ab6f3` → pinned upstream [DecisionInput/policy_router.rs L22–64](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/policy_router.rs#L22-L64), [runtime port/runner.rs L87–125](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner.rs#L87-L125), [admission/runner_actions.rs L235–267](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner_actions.rs#L235-L267), [settlement/postconditions.rs L49–86](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/postconditions.rs#L49-L86) → [comparative review `f3f948aa`](https://github.com/opensiro/harness-build-example-game-development/commit/f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0) → ADR-001 → subsequent original Python source.

`DIRECT` is warranted only for this narrow first-discovery observation: our frozen task and generic queries predate connector import, and the first recorded candidate is Ascension `Q01#1`. It **does not** establish that Cognee discovered the universally best source, improved game outcomes, or that all assessment body content was searched. Retrieval covered six function sections only. Cross-candidate judgment was subsequently performed by reading full assessments and code.

## Rejected or bounded alternatives

| ID | Decision | Source-based reason |
| --- | --- | --- |
| OPT-B | REJECT full Concordia simulation/GM architecture | Multi-entity social interaction, generative Game Master and component contracts exceed the single-player artifact. The independent environment authority boundary is inherent to OPT-A and will not be falsely credited as a second adapted Concordia subsystem. |
| OPT-C | REJECT Continual Harness self-evolving prompts/skills/subagents/memory | Needs many inference calls and persistent mutation surfaces; not required for demonstrating a construction trace. `S4=A` is not a quality ranking. |
| OPT-D | REJECT LLaMAR multi-robot planner/verifier | Requires vision/spatial simulator and inter-agent coordination; the partial-observation idea can be demonstrated more simply with a hidden local state. |
| OPT-0 | REJECT no-adaptation | A usable minimal artifact is possible without adaptation, but actual `Q01#1` and upstream source justify a bounded generation/settlement mechanism. |

## Frozen source-to-code plan

- `game_harness/contracts.py` — immutable Observation, LegalActionSet, DecisionInput, ActionIdentity, TransitionReceipt and policy/environment protocols.
- `game_harness/veiled_duel.py` — original authoritative hidden-intent environment with generation-bound legal actions and *only environment-authored* settlement receipts.
- `game_harness/runner.py` — action-choice admission, generation match, bounded step loop and strict postcondition guard.
- `game_harness/policy_jsonl.py` — optional external agent/model JSON-lines decision adapter; no direct model provider.
- `game_harness/__main__.py` — inspectable entry point, not executed during this study.
- `reports/construction-verification.md`, `reports/source-to-code.md`, updated README, hashes and trace after construction.

Implementation will be source-only, stdlib Python 3.12, with **zero game/model runs**. Allowed validation: source/AST/static import-surface checks only; runtime harness/games/tests/CI remain `NOT_RUN`. External model not selected. The Rust source is a documented design influence only, not copied code; MIT source and all other inspected licenses retain their original notices.

## Limitations declared before build

1. An invented toy hidden-information game is not a performance benchmark nor a faithful reproduction of Slay the Spire 2.
2. No demonstrated model competence, win rate, simulator reachability, or runnable episode verification.
3. The local synchronous environment cannot prove external distributed action ambiguity/reconciliation; unknown receipts trigger a stop only.
4. Cognee search returned irrelevant controls; full assessment bodies were ingested but only S1–S5 chunks indexed.
5. No VSM grade is promoted into a gameplay metric. C3 decision source links document an engineering rationale, not scientific superiority.

**Status:** C3 comparison and decision order complete; C4 code/source validation is still pending. `process_status=PARTIAL`; `build_status=NOT_STARTED`; `evaluation_level=NOT_RUN`; `model_quality_claim=NOT_EVALUATED`.
