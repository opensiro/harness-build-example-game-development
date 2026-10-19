# OpenSiro — Game Harness Construction via Cognee-First Discovery

> **Development-process research, not gameplay benchmarking.** This new public example documents a complete, source-backed path from a frozen game-agent task through **real native Cognee retrieval over canonical OpenSiro VSM assessments** to a separately decided and independently authored game harness. The harness was **not run**.

## What this experiment builds

**Veiled Duel** is an original minimal, turn-based game with a hidden opponent intent and bounded decisions. The harness separates a game environment's authoritative observations/actions from the policy's next-action choice. The project uses Python 3.12 standard library for the **game runtime**, has no game assets, and has no dependency on Cognee at game runtime.

- **Environment:** `game_harness/veiled_duel.py` — hidden intent, game rules, `reset / observe / legal_actions / step` (also `dispatch_action`), effects and authoritative receipts.
- **Agent/environment contract:** `game_harness/contracts.py` — frozen public `Observation`, generation-bound `LegalActionSet`, `DecisionInput`, `ActionIdentity`, `TransitionReceipt`, `DecisionSource` and `EnvironmentPort`.
- **Harness loop:** `game_harness/runner.py` — policy chooses among current legal actions; the runner checks generation, operation identity and a settled effect with a newer observation before advancing.
- **External policy interface:** `game_harness/policy_jsonl.py` — write one JSON-line observation/action request to stdout, read one JSON-line `{"action_id": "<allowed-id>"}` response from stdin. The harness deliberately does **not** select a model, call an API, embed an LLM, or score gameplay.
- **Opt-in entry point:** `python3 -m game_harness --seed 7 --max-turns 12 --max-decisions 64`. **This command executes the game and was NOT run during this experiment**. It requires an external policy process/operator to respond to every request. Output report goes to stderr; policy requests go to stdout.

The toy game's hidden intent makes partial observability explicit; the policy only receives the public projection, never the underlying opponent intent until an authorized `probe` action reveals it for the current turn. This is an original new implementation, not the former Game Development/MiniGrid example and not a copy of Ascension/Concordia source.

## Why Cognee was used

The purpose was to test **whether actual build-time Cognee discovery changes a developer's design choice**. The first recorded evidence for the selected mechanism came from native `Q01#1` for the included **Ascension** assessment, before full-source inspection. Its source describes a generation-bound authoritative legal-action catalog, separate model decisions, and settlement/effect checks. Reading Ascension's pinned upstream code then supported selecting only those bounded interface mechanisms, not its full distributed runtime. Alternatives from fresh results were reviewed and rejected based on documented scope/cost/complexity tradeoffs.

`discovery_contribution=DIRECT` means only that **the first recorded source of this selected mechanism was the native Cognee result**; it does not mean Cognee outperforms other retrieval tools, that the selected architecture is optimal, or that gameplay/model quality improved.

## Chronological public evidence

| Stage | Published artifact | Commit |
| --- | --- | --- |
| **C1 — preregistration, before connector import** | [Frozen task, source pins and eight query strings](reports/c1-run-contract.md) + initial [trace](traces/decision-trace.jsonl) | [`b3345272`](https://github.com/opensiro/harness-build-example-game-development/commit/b3345272ee01c89bf2dc86870d35602b1e3894c8) |
| **C2 — actual import, independent audit, native retrieval** | [Discovery report](reports/discovery.md), [original connector/import/audit/query receipts](receipts/discovery/) | [`d6c757f`](https://github.com/opensiro/harness-build-example-game-development/commit/d6c757f701501f1f555c009d5163c6852e33e33f) |
| **C3a — comparison before mechanism selection** | [Assessment + pinned upstream inspection and alternatives](reports/candidate-comparison.md) | [`f3f948a`](https://github.com/opensiro/harness-build-example-game-development/commit/f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0) |
| **C3b — separate architectural decision** | [ADR-001 with selected/rejected options](reports/architecture-decision.md) | [`cb33282`](https://github.com/opensiro/harness-build-example-game-development/commit/cb33282d1cb5454841f87dd486df86da60cae787) |
| **C4 — implementation after decision** | Original [`game_harness/`](game_harness/) source, [source-to-code links](reports/source-to-code.md), [construction verification](reports/construction-verification.md), [trace](traces/decision-trace.jsonl) | First implementation [`ee8da1c`](https://github.com/opensiro/harness-build-example-game-development/commit/ee8da1ca036ab4d853c134180b0b6f1716e9e346); final C4 anchor is the branch's evidence publication commit |

Git ancestry and artifact hashes are checked and published as part of C4. Documentation reports are immutable evidence of their respective stage; do not reinterpret the earlier case study or retrofit discovery chronology.

## Cognee corpus and exact search coverage

| Property | Verified observation |
| --- | --- |
| Pinned Index | [`b48b13e`](https://github.com/opensiro/vsm-harness-index/commit/b48b13e74d6938f833094d3f9afc1a11e61a8515) |
| OpenSiro connector | [`d176484`](https://github.com/opensiro/cognee-community/commit/d176484e85da55c84450d67040cb4a2d096353c7), package `packages/connector/opensiro-vsm`; minimal sharded-path [patch](receipts/preflight/connector-shard-compat.patch) |
| Included full Markdown imports | **581** included assessment documents; proposed/excluded deliberately not imported |
| Original Cognee graph | **12,161 nodes**, **8,094 edges**, **3,486 exact autonomy grade facts** |
| Searchable lexical index | **3,486 section chunks**, exactly six S1/S2/S3/S3*/S4/S5 sections per included assessment; **not full-body search** |
| Native discovery | `cognee.search`, `SearchType.CHUNKS_LEXICAL`, eight frozen Q01–Q08, top 15 unfiltered hits each, including irrelevant/negative control results |
| Independent audit | **PASS** for 581 source identities, literal grades, SHA/review references and graph source ownership |
| Later full-source inspection | Four shortlisted **complete** assessments and upstream source files at reviewed Git SHAs, **after C2** |

**Importing full Markdown is not full-document retrieval.** Lexical search in this experiment covered only six function sections per document. The source-to-code claim is confined to those hits followed by full pinned assessment/upstream inspection. `TLDR.md` was not the search input.

## Reproduce the research and construct the source

Follow [`docs/REPRODUCE.md`](docs/REPRODUCE.md) for fresh dataset instructions and source/static checks. Research dependencies are separate from the game runtime; the connector's pinned experimental branch and its exact compatibility patch must be reconstructed, rather than silently replaced with a generic importer. Do not reuse the original fresh-only dataset name after a failed import.

For **source-only** validation, which does not import or execute the game modules:

```bash
python3 tools/check_source_only.py
```

Optional `python3 -m game_harness` **runs an actual game episode**; it was not authorized or used in this experiment. No CI workflow is supplied to run episodes or inference.

## Evidence status

- `process_status: PASS` — scoped **development-process** C1→C2→comparison→decision→C4 evidence, not gameplay correctness (subject to published final C4 ancestry check).
- `build_status: PASS` — inspectable constructed source with documented implementation mapping; **not** functionality-verified.
- `verification_level: STATIC_CHECKED` — source AST and structural checks only.
- `evaluation_level: NOT_RUN`.
- `runtime_status: NOT_RUN`.
- `model_quality_claim: NOT_EVALUATED`.
- `adaptation_outcome: ADAPTED`.
- `discovery_contribution: DIRECT` — narrow evidence-first attribution; no comparative retrieval-quality claim.

See [limitations](reports/construction-verification.md). The canonical VSM function grades are **organizational ownership labels**, never harness or gameplay performance rankings.

## Protocol and licensing

- Canonical bootstrap: [START_HERE.md](https://github.com/opensiro/vsm-oss-organization/blob/main/START_HERE.md) → [ECOSYSTEM.md](https://github.com/opensiro/vsm-oss-organization/blob/main/docs/ECOSYSTEM.md).
- Governing experimental skill: [`build-harness-cognee-first v0.1.0` as merged in Skills PR #52](https://github.com/opensiro/vsm-harness-skills/commit/5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25).
- Newly authored repository source is under [MIT](LICENSE); code from inspected upstream repositories was **not copied**. Source licenses and study references remain attributed in the [candidate comparison](reports/candidate-comparison.md).


---

## Iteration 2 — prospective context-aware agent extension (2026-10-19)

The original Iteration 1 evidence and receipts above remain unchanged. A separate, chronologically published **second iteration** extends the same Veiled Duel source with an episode-private history of *verified* public feedback, optional external policy subgoal/strategy fields, bounded context, and fail-closed malformed-policy handling. This is a **source-only construction** experiment, not game evaluation.

Follow the separate [Iteration 2 C1–C4 construction report](iteration-2/reports/C4-construction-verification.md), [independent Cognee discovery](iteration-2/reports/C2-discovery.md), [architecture comparison and ADR](iteration-2/reports/C3-architecture-decision.md), [implementation trace](iteration-2/reports/source-to-code.md) and [external AI JSONL interface](iteration-2/docs/INTERFACES.md). The fresh retrieval indexed S1–S5 sections only; see the [C2 receipt reconciliation](iteration-2/reports/C2-reconciliation.md).

**Iteration 2:** `process_status=PASS`, `build_status=PASS` (inspectable source), `verification_level=STATIC_CHECKED`; `runtime_status=NOT_RUN`, `evaluation_level=NOT_RUN`, `model_quality_claim=NOT_EVALUATED`. Neither iteration establishes model/game performance.
