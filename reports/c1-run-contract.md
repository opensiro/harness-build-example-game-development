# C1 — Frozen Construction Run Contract

**Experiment:** game-cognee-first-20261018
**Recorded UTC:** 2026-10-18T21:00:38Z
**State:** PRE-IMPORT / NO ARCHITECTURE SELECTED
**Protocol:** [merged Skills commit 5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25](https://github.com/opensiro/vsm-harness-skills/commit/5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25), `build-harness-cognee-first` 0.1.0.

## Task and acceptance

Construct an inspectable, minimal Python game-playing AI agent **harness**, with explicit environment observation, permitted action, environment feedback and bounded episode/task continuation interfaces. Support partial observation and termination metadata without choosing a game, game library, specific agent/model, planner, memory system, or organizational mechanism before Cognee results. The task output is the source artifact + explicit reproduction instructions and evidence chain. No claim about game success.

Minimum **NO_ADAPTATION** artifact, if source research rejects all additional mechanisms: an environment-neutral `reset/observe/step` adapter protocol, observation/action/result data contract, a policy-driver boundary, bounded orchestration entry point, explicit termination, and dependency/run instructions. Source-complete does not imply runtime-correct.

**Starting baseline:** an empty Python 3.12 project with README and documentation. There is no gameplay code, selected package or architecture; generic interface requirements are *acceptance constraints*, not source-derived design choices.

## Resources and permissions

- CPU-only Linux research host, Python 3.12; memory ~61 GiB with ~47 GiB available at preflight; host disk ~1.8 GiB free / 99% used; shared memory tmpfs ~18 GiB free (2026-10-18T20:54Z). A separate build workspace has ~34 GiB available. Stop instead of deleting unrelated data or silently sampling.
- Native OpenSiro Cognee connector + Cognee 1.6.4 (if installable). Isolated data store/dataset and fresh-only marker; use shared memory for disposable local research state if safe.
- No model provider chosen. Budget: 0 model calls, 0 gameplay episodes, 0 paid embeddings, 0 frontier inference, 0 gameplay CI. No secrets in receipts.
- Allowed: checkout/index provenance validation, pinned connector compatibility fix, fresh import, independent audit, native Cognee retrieval, subsequent public source comparison, code authoring, source/AST/static checks and GitHub review commits. No runtime execution of built harness without further permission.
- Network sources during C1/C2: public OpenSiro Index/Skills/Profile and OpenSiro Cognee connector. Only after C2 may third-party candidate implementations or public external research be inspected.
- No destructive remote actions, no merging branches or PRs that trigger gameplay CI.

## Immutable source pins

| Source | SHA / state |
| --- | --- |
| Bootstrap owner `opensiro/vsm-oss-organization` | `184526ca9e1a5968b5133d84b47ad94c6921954d` (current main preflight) |
| Skills and merged skill v0.1.0 | `5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25`; PR #52 merged |
| Canonical Index `opensiro/vsm-harness-index` | `b48b13e74d6938f833094d3f9afc1a11e61a8515` |
| OpenSiro connector `opensiro/cognee-community` | `d176484e85da55c84450d67040cb4a2d096353c7`, package `packages/connector/opensiro-vsm` (review branch; **not** upstream released) |
| Active corpus contract as advertised by Index README | Profile 0.2.4; Methodology 0.3.7; validate actual included content from pinned tree before import |

No prior game or Flash example implementation, candidate selection, architecture decision, results or query hits are an evidence source. Historical skill case study is only a description of evidence formats.

## Source selection policy (frozen)

**Include exactly every** pinned Index assessment with canonical front matter `status: included` and catalog/source consistency verified by the connector. Exclude `proposed`, `excluded-no-agentic-vsm` and files not canonically included. Preflight Index README advertises 581 included / 629 catalog, but that is **not** a validated connector import count. Validate against the pinned Git tree. If all records cannot be ingested due to limits, fail closed and publish a separate pre-import policy change rather than retrospectively claiming full-corpus coverage. Deterministic selection: all admitted IDs, sorted by `harness_id`.

Import entire original assessment Markdown via pinned connector; separately document graph, exact autonomy grades, lexical chunks and any content not indexed. **Import of full Markdown is not equivalent to full-body search.** Connector at pinned SHA has a known flat-path assumption `assessments/<id>.md`, while Index is sharded. Apply and hash the smallest source-path compatibility patch before connector invocation; record changed bytes and tests. The unpatched connector remains the pinned authority plus explicitly disclosed local compatibility delta. If fuller architectural search needs it, a separate full-document indexing extension must be implemented/audited on a fresh dataset before design selection.

## Frozen initial native retrieval plan

All first-pass queries below are task-first, contain **no prechosen candidate names** and use real `cognee.search` with `SearchType.CHUNKS_LEXICAL`, target imported dataset, maximum 15 returned chunks per query (where SDK permits). Record all native hits, ranks, zero/irrelevant hits and mode metadata without inventing relevance scores.

| ID | Exact query string | Intent |
| --- | --- | --- |
| Q01 | `game environment observation action feedback` | Game/environment interface loop |
| Q02 | `partial observability state observation belief` | Partial-observation context |
| Q03 | `sequential decisions multi step agent tasks` | Sequence management |
| Q04 | `long horizon planning memory game` | Long horizon concerns |
| Q05 | `environment feedback retries recovery` | Feedback and errors |
| Q06 | `tool action execution safety validation` | Action boundary |
| Q07 | `agent state persistence context across steps` | State handling |
| Q08 | `chlorophyll photosynthesis tectonic plates` | Negative control; include unhelpful matches |

Native query outputs may guide later *candidate* selection only after a passing imported-source and provenance audit. Search scope is explicitly the connector's six S1/S2/S3/S3*/S4/S5 function sections per assessment (6 chunks each) in its existing lexical mode, plus its separate typed graph metadata; it is **not full-body lexical search**. Do not promise coverage of front matter, rationale and general narrative text unless a proven separate extension adds them.

## Chronology and stop rule

C1 must be **publicly committed before first connector import or dataset index build**. C2 requires original pinned connector invocation/import receipt, independent new-process provenance audit PASS and native retrieval receipts; C3 requires comparison commit then separate decision commit; C4 requires produced harness source even for NO_ADAPTATION. If connector ingestion, independent audit, or native query fails, publish blocker without selecting candidates or implementing a game agent.

Status at C1: `process_status=PARTIAL`, `build_status=NOT_STARTED`, `verification_level=NOT_RUN`, `evaluation_level=NOT_RUN`, `adaptation_outcome=NOT_DECIDED`, `discovery_contribution=INDETERMINATE`, `model_quality_claim=NOT_EVALUATED`.
