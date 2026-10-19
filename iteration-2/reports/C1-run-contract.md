# Iteration 2 — C1 preregistration (functional extension, source-only)

- Run ID: `game-iter2-20261019`.
- Branch: `experiment/game-cognee-iteration-2-20261019` in `opensiro/harness-build-example-game-development`.
- Recorded: 2026-10-19 UTC (Git commit time is the public chronological anchor).
- State: **PRE-IMPORT, PRE-DISCOVERY, NO MECHANISM SELECTED**.
- Stage: prospective second iteration of an **existing** game-playing harness; **not** retrospective repair of original C1–C4.
- Original baseline `main` commit: `3a93532d70b6dccad2d5e83a7a0e6532456fff6b`. Original reports, receipts, traces and dates are immutable. Previously retrieved candidates are not Iteration 2 discovery hits.

## Source authority and pins (frozen before first import)

| Surface | Actual immutable pin / treatment |
|---|---|
| OpenSiro bootstrap | `opensiro/vsm-oss-organization@2ba6658b39872943757a7a0ed560785cdaf14470`, START_HERE → docs/ECOSYSTEM.md |
| Construction skill | `opensiro/vsm-harness-skills@5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25`, experimental `build-harness-cognee-first` **0.1.0** and all three references |
| Canonical Index | `opensiro/vsm-harness-index@5cbb1035538b8f80fa3362f1c99652f4fd7c55e8`; canonical status read from each pinned assessment and reconciled to `data/catalog.psv` |
| Profile | `opensiro/vsm-harness-profile@527fe01ccf1ee22e54bd9525285a89a93179c1e7`; Index active Profile **0.2.4** |
| Assessment methodology | `opensiro/vsm-harness-skills@5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25`; Index active Methodology **0.3.7** |
| OpenSiro Cognee connector | `opensiro/cognee-community@d176484e85da55c84450d67040cb4a2d096353c7`, package `packages/connector/opensiro-vsm`. Deliberately pinned because today's connector `main@5e78950e408d66cbb3787ed9af6a7f5a37d6e20a` **does not contain** this package. Connector pin is *not* proof of execution. |

**Known compatibility issue:** pinned connector has flat `assessments/<id>.md` assumptions; current Index stores `assessments/<first-two>/<id>.md`. Before import inspect and record an explicit minimal path patch and SHA-256. Validate the patched connector against **this Index pin**, not the historical 581-record run. If another schema mismatch exists, capture error and fail closed rather than reusing earlier receipts. A path patch alone never proves compatibility.

## Functional gap: observations from unchanged Iteration 1 sources (pre-discovery requirements)

The baseline supplies `Observation`, `LegalActionSet`, `DecisionInput`, `ActionIdentity`, `TransitionReceipt`, external `DecisionSource`, environment `dispatch_action`, bounded `EpisodeRunner`, and a JSONL policy bridge. It validates legal actions and settled/fresh transitions. It does **not** maintain an explicit policy-private sequential context/history, communicate prior action feedback as a structured next-decision input, maintain a mutable objective/plan, or have a dedicated failure-budget/source timeout policy. The JSONL `readline()` is unbounded. Current `max_decisions` limits accepted loop iterations, but not external policy latency/tokens.

These are requirements, **not selected mechanisms**:

| ID | Requirement and source-level acceptance |
|---|---|
| R1 | A real external AI decision source can obtain a provider-neutral next-action request; no paid provider is selected or invoked |
| R2 | Agent-private context includes bounded previous public observations, chosen actions and authoritative post-action feedback, while hidden environment state remains inaccessible |
| R3 | Longitudinal goals and any adaptation to feedback are expressible without embedding game-specific strategy into the authoritative environment |
| R4 | Policy failures, invalid replies and budgets have explicit fail-closed behavior; no blind redispatch after uncertain effects |
| R5 | Explicit transition boundary remains `Observe → Context → Decide → Validate → Execute → Feedback → Context update`, without modifying legal-action/receipt authority |
| R6 | Source structure supports later extension to additional decision backends and optional context strategies without rewriting game rules or constructing a general game engine |

Construction acceptance: changes to `game_harness/` fulfilling R1–R6, a trace mapping selected mechanisms to real retrieval and pinned code, docs and static/provenance checks. A **NO_ADAPTATION** outcome still must produce an inspectable bounded harness satisfying R1–R6 using original authorship. Mere retention of today's incomplete scaffold is not a successful C4.

## Safety, environment and budget

- Target: one original Veiled Duel environment, existing Python 3.12 standard-library runtime, no new production infra / control plane / scheduler.
- Discovery tooling: pinned OpenSiro connector with native Cognee SDK, isolated research venv/storage on available CLI Linux workspace, no model API/inference, no paid endpoints, no embeddings/LLM.
- Budget ceiling: 12 GiB *incremental* temporary data, first-pass full included corpus if feasible; no external model calls; 8 native retrieval requests plus any *separately logged* follow-up expansion. Any infeasibility must be documented before deterministic sampling.
- Game, `python -m game_harness`, `EpisodeRunner.run`, `game_harness` runtime tests, gameplay CI and model-provider calls are **forbidden** in this iteration. Source inspection, AST parse, `git` ancestry/sha, `py_compile` in inert/static scope only if no imports/episode execution.
- No credentials in any publication. Original files under `receipts/`, `reports/`, `traces/` are not modified; Iteration 2 evidence goes under `iteration-2/`.
- New isolated Cognee dataset and unique attempt root for each import. Failure preserves attempt and error receipt; retries must use a new dataset. Original C1–C4 not referenced as discovery output.

## Corpus selection and frozen native Cognee query plan

Before import, select **all and only included** assessment Markdown files from the pinned Index at `5cbb103...`, reconcile to canonical `data/catalog.psv` and preserve selection digest/counts. No pre-chosen sources, no sample or architecture whitelist. Counts **unknown until fresh pinned source validation**. Preserve full documents as ingestion sources; actual indexed fields may only be six S1–S5 function-section lexical chunks. Report these as different scopes; if non-function narrative is needed, perform a separately audited full-body index build in a **new dataset before C3**.

Native first pass: `cognee.search` / `SearchType.CHUNKS_LEXICAL`, `top_k=20` where supported; preserve raw, unfiltered hits, empty/irrelevant/error outcomes. Do not rename keywords to favorite candidate systems.

| Query ID | Exact query | Investigates |
|---|---|---|
| I2-Q01 | `game agent observation feedback action history context` | consecutive-observation context |
| I2-Q02 | `persistent agent memory episodic state decisions` | bounded policy-private memory |
| I2-Q03 | `multi step planning goals strategy replanning` | goals and strategy updates |
| I2-Q04 | `decision source failure timeout retry budget` | decision-source failure/budget |
| I2-Q05 | `agent controller environment tools feedback execution` | authoritative side-effect boundary |
| I2-Q06 | `context compaction history summarization observation` | long context management |
| I2-Q07 | `sequential partial observability prior outcomes planning` | hidden-state safety and history |
| I2-Q08 | `photosynthetic jellyfish volcanic granite astronomy` | negative/irrelevant control |

Original `Iteration 1` receipts, any workspace cache, index text grep, and any upstream code encountered through previous conversations are **not** substitutes for this search.

## Checkpoints and stop rule

C1 = immutable publication of this contract + initial append-only Iteration 2 trace, **before connector import**. C2 = original new connector import plus independent source/graph/grade audit PASS plus native Cognee queries with precise indexed/ingested coverage. C3 = post-C2 shortlist → complete canonical assessments → upstream code pinned inspection → comparison commit → separate decision commit. C4 = new source, documentation and independently checkable source-level provenance after C3.

At any failed import, audit, or native search gate: stop dependent comparisons and functional changes; publish exact blocker/receipts, report `process_status=PARTIAL`, `build_status=NOT_STARTED` (Iteration 2), `runtime_status=NOT_RUN`, `evaluation_level=NOT_RUN`, `discovery_contribution=INDETERMINATE`.
