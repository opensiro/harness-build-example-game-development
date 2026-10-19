# C2 — Native Cognee Discovery and Provenance

Experiment: `game-cognee-first-20261018`  
Source pin: `b48b13e74d6938f833094d3f9afc1a11e61a8515`  
Connector pin: `d176484e85da55c84450d67040cb4a2d096353c7`  
Skill contract: merged `5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25` (`build-harness-cognee-first` v0.1.0).  
Pre-import C1 anchor: `b3345272ee01c89bf2dc86870d35602b1e3894c8`.

## Execution, not simulated retrieval

1. Fresh isolated store `fresh-store-01`, dataset `game-cognee-b3345272-full-01`. The original OpenSiro connector CLI at `packages/connector/opensiro-vsm/examples/example.py` was invoked with `--all --lexical` and the pinned Index SHA, using Cognee SDK 1.6.4 on Python 3.12.
2. Exactly one one-line compatibility patch changed canonical assessment path matching from `assessments/<id>.md` to `assessments/<id[:2]>/<id>.md`. Patch recorded as `receipts/preflight/connector-shard-compat.patch`, git-diff SHA256 `5be20dfacb2f8d48608b2aa4b9d4fbc6a43050e1f799678e8770ecb48a00b070`. The pinned connector source and patch are not conflated.
3. Pinned full-corpus source validation: **581 included**, 48 excluded, 14 proposed; catalog 629. All 581 `included` Markdown documents successfully imported. No sampling.
4. Original connector invocation completed with `PASS_FRESH_LOCAL_COGNEE_IMPORT`: **581 imported documents, 12,161 graph nodes, 8,094 graph edges, 3,486 exact VSM grades**, no model/inference calls. Its native JSON stdout is copied without rewriting into `receipts/discovery/connector-import-native.json`. The raw console log and its SHA256 are retained as a compressed attached source receipt.
5. Independent **separate-process** `audit_dataset` from the pinned OpenSiro connector returned **PASS**, verifying **all 581 source identities, document SHA256/review-ref graph provenance, all 3,486 literal function grades and graph/source-reference ownership**. Raw audit returned in `receipts/discovery/independent-audit.json`.
6. Eight exact C1 queries (`Q01`–`Q08`) executed through actual `cognee.search` with `SearchType.CHUNKS_LEXICAL` and `top_k=15` on the freshly imported dataset, **after** audit PASS. Each returned 15 unfiltered native search hits, including the irrelevant negative control `Q08`; zero-overlap/unhelpful results are **not** proof of domain relevance. Original per-query native responses retained in `receipts/discovery/native-search-Qxx.json`.

## Three non-equivalent scopes

| Scope | Observed boundary |
| --- | --- |
| `source_ingested_scope` | 581 full pinned canonical assessment Markdown documents, including entire bodies in Cognee source Data records |
| `lexical_or_semantic_index_scope` | Exactly six S1/S2/S3/S3*/S4/S5 function-section `DocumentChunk` nodes per assessment, **3,486 searchable chunks**; BM25/native `CHUNKS_LEXICAL`. Not full-body, not semantic, no embedding/model calls. |
| `inspected_source_scope` | **None yet at C2.** Full candidate assessments and pinned upstream implementations are only permitted after this commit. |

The lexical result only suggests text-bearing sections to inspect; it does not demonstrate a complete-body search, the correctness of any architectural mechanism, gameplay performance, an S4 performance ranking, or superiority of Cognee. `TLDR.md` was not the search corpus. No source shortlist, game choice, architecture decision, or adaptation has been made before C2.

## Evidence manifest

- `reports/c1-run-contract.md`: frozen task, full-corpus policy and query plan.
- `receipts/preflight/source-validation.json`: canonical source validation.
- `receipts/preflight/connector-shard-compat.patch`: one-line reproducible connector fix.
- `receipts/discovery/connector-import-native.json`: actual native connector import stdout JSON.
- `receipts/discovery/connector-import-original.log.gz`: verbatim compressed native connector console log.
- `receipts/discovery/connector-import-log-sha256.txt`: hash of uncompressed original log.
- `receipts/discovery/pinned-source-manifest.json`: complete pinned connector source manifest containing source IDs, SHA256, pinned review refs and grades.
- `receipts/discovery/independent-audit.json`: full separate-process audit report, including all 581 IDs.
- `receipts/discovery/native-search-Q01.json` through `Q08.json`: raw unfiltered native search responses and query execution metadata.
- `receipts/discovery/native-search-manifest.json`: frozen query receipt index and byte sizes.
- `tools/c2_native_receipts.py`: audit and query harness (research-only, not the game harness).

## Gate state

C1: PASS, publicly committed before first connector import.  
C2: **PASS once this report and all originals are anchored in a public Git commit, before any shortlist comparison**.  
C3/C4: NOT_STARTED.  
`process_status=PARTIAL`, `build_status=NOT_STARTED`, `verification_level=SOURCE_ONLY` (for source/audit, not game runtime), `evaluation_level=NOT_RUN`, `model_quality_claim=NOT_EVALUATED`, `discovery_contribution=INDETERMINATE`.

Possible next step, only after C2: inspect the raw Q01–Q08 hits for relevant candidate evidence, read the **full** pinned assessments, inspect upstream sources at their documented review SHAs, compare alternatives and publish the comparison **before** any decision.
