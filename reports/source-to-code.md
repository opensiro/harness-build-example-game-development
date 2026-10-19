# Source-to-code traceability — Game Harness Construction

**Scope:** build-time engineering decisions, not game performance. The actual first source of the adopted mechanism is the frozen native `Q01#1` Cognee hit, retained at [Q01 raw receipt](../receipts/discovery/native-search-Q01.json). The four-candidate [comparison](candidate-comparison.md) was committed at `f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0`, followed by a **separate** [ADR-001](architecture-decision.md) at `cb33282d1cb5454841f87dd486df86da60cae787`. The [first implementation](https://github.com/opensiro/harness-build-example-game-development/commit/ee8da1ca036ab4d853c134180b0b6f1716e9e346) follows that decision.

## Provenance chain

`Q01#1` → [canonical complete Ascension assessment at pinned Index b48b13e](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/as/ascension.md) (SHA256 `cd2a74a004f62a4bcf11fa2185d94e767b02ce3b23b2ec012ca86f44619ab6f3`) → pinned [Ascension upstream 53312dd](https://github.com/AI-Ascension/sts2-harness/tree/53312ddbb074f7c187e5f59d88b6585da797fe17) → [comparison](candidate-comparison.md) → [ADR-001](architecture-decision.md) → original Python source after the decision commit.

| Implemented component | Native/source provenance | Verified source mechanism and adaptation boundary |
| --- | --- | --- |
| [`game_harness/contracts.py`](../game_harness/contracts.py) | `Q01#1`; [Ascension `policy_router.rs` L22–64](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/policy_router.rs#L22-L64), [`runner.rs` L87–125](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner.rs#L87-L125) | Frozen `Observation`, `LegalActionSet`, `DecisionInput`, `ActionIdentity`, `TransitionReceipt` and policy/environment protocols. Not a Rust port; no external MCP/gateway leases. |
| [`game_harness/veiled_duel.py`](../game_harness/veiled_duel.py) | `Q01#1`; [Ascension runtime port](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner.rs#L87-L125) and [generation/admission](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner_actions.rs#L235-L267) | **New** hidden-intent turn-based game; all hidden state and transition authority stay in the environment, which generates current actions and settled receipts. It is not Slay the Spire 2 or imported assets. |
| [`game_harness/runner.py`](../game_harness/runner.py) | `Q01#1`; [legal-action check](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner_actions.rs#L235-L267) and [postconditions](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/postconditions.rs#L49-L86) | Bounded policy-decision loop, generation-matched legal-action admission, receipt operation identity/effect witness, strictly newer observation and fail-closed unknowns. Does **not** implement remote reconciliation, independent auditor or exactly-once distributed delivery. |
| [`game_harness/policy_jsonl.py`](../game_harness/policy_jsonl.py) | `Q01#1`; [policy boundary](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/policy_router.rs#L63-L64) | New generic stdio bridge for an external agent; transports public `DecisionInput` and its selected action ID; no provider inference, no Cognee dependency at runtime. The bridge itself is construction plumbing, **not** a claimed independently discovered source mechanism. |
| [`game_harness/__main__.py`](../game_harness/__main__.py) | ADR-001 source-completeness/entrypoint acceptance | Optional launcher `python3 -m game_harness`. Source exists, **not executed**. This is implementation plumbing, not a separate source-derived innovation. |
| [`game_harness/__init__.py`](../game_harness/__init__.py) | ADR-001 construction contract | Python package export declarations; no invented Cognee architectural credit. |

## Alternative decisions and non-adapted components

The actual retrieved source comparison included [Concordia](candidate-comparison.md#b--concordia-apache-20), [Continual Harness](candidate-comparison.md#c--continual-harness-mit), and [LLaMAR](candidate-comparison.md#d--llamar-mit). These were compared as alternatives and **not** silently fused into the selected harness:

- **Concordia:** no multi-entity Game Master or generative event resolution copied; only the generic principle that the environment adjudicates an agent proposal overlaps with the selected game interface.
- **Continual Harness:** no automatic self-editing prompts, skills, subagents, or persistent adaptation; no model calls.
- **LLaMAR:** no simulated multi-robot coordination, planner/verifier or whole-team control. Partial observability in the toy game is a game requirement and environment contract, not a copied LLaMAR implementation.
- **NO_ADAPTATION:** considered and rejected because `Q01#1` and pinned upstream code justified a concrete minimal action-generation/settlement boundary.

## Verification and licensing boundaries

Only the newly authored source is included. Ascension, Continual Harness and LLaMAR were examined at MIT-licensed revisions, Concordia at Apache-2.0; their code was **not** copied. The source mapping establishes traceable design decisions, not functional equivalence, code-level test coverage or any gameplay improvement.

The `SOURCE_ONLY` / `STATIC_CHECKED` records check syntax, structural interfaces and provenance; gameplay, policy/model inference, win rate, long-horizon success and runtime correctness remain `NOT_RUN` / `NOT_EVALUATED`. The comparison is bounded by S1–S5 lexical search, not full-body indexed retrieval.
