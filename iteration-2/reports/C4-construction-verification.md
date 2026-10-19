# Iteration 2 — C4 constructed artifact and source verification

**Run:** `game-iter2-20261019` · **Scope:** prospective extension of the original Veiled Duel game harness; not an assessment of gameplay performance.

## Public chronological gate anchors

| Gate | Immutable commit | Result |
|---|---|---|
| C1 / source, requirements and first query plan | `dc57a1a80a1db4f31e2a215513419e960416fb8e` | PASS, published before first import |
| C2 / fresh connector ingest + independent audit + native queries | `3a6b7debecb5719c4319eef9579d143a6f3062d1` | PASS; original base64+gzip receipts in Git |
| C3a / comparison | `0184e3d7e1432e6209ca248c4a075f2c5c7dbd89` | PASS, source-backed, before selecting mechanism |
| C3b / ADR selection | `1bc4828ca94232373e8585f04f11d576f59deb8e` | PASS, 3 complementary choices |
| First C4 implementation | `01b77fe04d7e4ba8dad0cf9db1e08b0fdd207762` | AFTER ADR, source built |
| Static verification source HEAD | `0889d6f4e063775171550073aeb0c8a56838859f` | PASS_SOURCE_STATIC; all game modules AST parsed |

The final published C4 anchor is the Git commit containing this report and the complete source/trace/receipt set. Verify their ancestry via `git merge-base --is-ancestor` along the chain above. C2 receipt chronology is reconciled [append-only here](C2-reconciliation.md), not retroactively edited. The earlier Iteration 1 C1–C4 remains immutable.

## Newly produced architecture

- `game_harness/agent_context.py`: `AgentContext`, settled public `SettledEvent`, `PolicyDecision`, optional `ContextualDecisionSource`. Policy-private event context resets on each run; no hidden game state.
- `game_harness/runner.py`: backward-compatible `DecisionSource` handling plus optional context-aware proposal, legal/catalog validation, exactly one dispatch, settlement proof, **then** immutable context update; explicit episode/context/note budgets.
- `game_harness/policy_jsonl.py`: provider-agnostic JSONL with optional `agent_context`, bounded request/reply bytes and optional strategy/subgoal reply strings. Old action-only replies remain valid; no paid model or API provider.
- `iteration-2/docs/INTERFACES.md`: external AI connection contract, bounded feedback/strategy behavior, reproduction boundary.
- `iteration-2/reports/source-to-code.md`: `Requirement → Cognee hit → canonical assessment → pinned upstream source → comparison → ADR → local implementation` mapping.

Unchanged: `game_harness/contracts.py`, `game_harness/veiled_duel.py`, original historical reports, original receipts, and original traces.

## Static verification (actually performed)

`python3 iteration-2/tools/check_static.py` returned [PASS_SOURCE_STATIC](../receipts/verification/static-check.json), `verification_level=STATIC_CHECKED`. It uses AST parsing, source-order checks and immutable-baseline Git-byte comparisons; **it does not import game modules**. The check observed `dispatch_action` before `verify_settlement` before `AgentContext.after_settlement`, rejects changing original contracts/environment, and confirms no Cognee/model client runtime imports.

Pinned source SHA256:

| File | SHA256 |
|---|---|
| `game_harness/agent_context.py` | `a4feea39014684db4c7460ce0ef1cace6dd09560981cbfda4c5fc3b0f43e8b1c` |
| `game_harness/runner.py` | `b32c748059871a4992da7cba148604b96d61657dee9bb00b5c78611d319b9306` |
| `game_harness/policy_jsonl.py` | `386db6c84d598497072afb9272352c3b36b6a05beb7174b470b8d605fa567744` |

Additional checks: `git diff --check` succeeded; native Cognee receipts in Git were decoded and all **eight** first-run raw hashes validated; later native read responses had the same payload after removing differing UTC timestamp fields.

## Honest limitations

- **No game execution**, no external model calls, no runtime tests, no win-rate, no benchmark, no gameplay CI. Source-level construction is not proof the complete loop runs successfully.
- Raw native Cognee search indexed six S1/S2/S3/S3*/S4/S5 sections, not entire Markdown and not embeddings. First-run original query receipts and all irrelevant/negative hits are retained.
- A `TextIO` policy stream can block; reply/request byte caps are **not** a wall-clock timeout guarantee. Event FIFO is not semantic summary or exact token budgeting. Newly added strategy notes have no autonomous planning guarantees.
- No upstream code was copied; pinned sources influenced independently authored concepts. Do not attribute game-playing superiority or VSM function performance to canonical autonomy states.
- `JSONLinesDecisionSource` is a connection interface, not a paid model client. Policy-private notes have no environmental mutation authority.

## Completion contract

- `process_status=PASS` — C1 → first-run C2 → C3a comparison → distinct ADR → C4, with public chronological provenance and bounded receipt reconciliation.
- `build_status=PASS` — complete inspectable source/code-map for declared R1–R6 **at source level**.
- `verification_level=STATIC_CHECKED`.
- `runtime_status=NOT_RUN`.
- `evaluation_level=NOT_RUN`.
- `model_quality_claim=NOT_EVALUATED`.
- `adaptation_outcome=ADAPTED`.
- `discovery_contribution=DIRECT` for three bounded source-backed mechanism discoveries (details in ADR); **not** a claim of comparative retrieval effectiveness.

Only an independently authorized future execution may establish functional or gameplay correctness.
