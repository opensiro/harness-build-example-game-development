# Iteration 2 — C2: independent fresh Cognee discovery

**Run:** `game-iter2-20261019` · **Source:** `opensiro/vsm-harness-index@5cbb1035538b8f80fa3362f1c99652f4fd7c55e8` · **Connector:** `opensiro/cognee-community@d176484e85da55c84450d67040cb4a2d096353c7` plus [published two-line sharded-path delta](../receipts/preflight/connector-source-path.patch), SHA256 `8718a48443e471ac14d45459af2718b87b986b6a8e523a44573368741644a9ae`.

C1 predecessor (pre-import): [`dc57a1a80a1db4f31e2a215513419e960416fb8e`](https://github.com/opensiro/harness-build-example-game-development/commit/dc57a1a80a1db4f31e2a215513419e960416fb8e). First connector import began **2026-10-19T13:01:24Z**, after C1 and the published compatibility/preflight receipts. Original Iteration 1 C1–C4 artifacts are unchanged and **not** used as new retrieval results.

## Actual execution (not a simulation)

- Python 3.12, real Cognee SDK **1.6.4**, pinned source connector's `examples/example.py --all --lexical`, independent Linux workspace; no model API / embeddings / game execution.
- Fresh attempt ID `b5c73a233c13455986e10f86689e5dbc`; Cognee dataset `game-iter2-b5c73a233c13455986e10f86689e5dbc`. No previous dataset reused.
- Full **583 included** pinned Markdown documents admitted; **48 excluded** and **12 proposed** rejected by membership policy. Source validation: `PASS_SOURCE_VALIDATION`.
- Connector result: `PASS_FRESH_LOCAL_COGNEE_IMPORT`, `PipelineRunCompleted` (exit 0), elapsed 673.837 seconds. Graph: **12,201 nodes**, **8,120 edges**; source-scoped nodes **12,201**; `all_states_exact=true`.
- Independent **separate-process** connector audit `audit_dataset`: **PASS**, 583 Cognee document source identities, **3,498 exact grades**, source provenance and graph scopes checked.
- Distinct native process invoked `cognee.search(query_type=SearchType.CHUNKS_LEXICAL, datasets=[dataset], top_k=20)` for preregistered **I2-Q01–I2-Q08**. All **eight calls succeeded**, each returned 20 raw ranked hits. I2-Q08 is the deliberately unrelated negative control; its irrelevant matches were **retained**, not filtered or silently discarded. Unfiltered original response envelopes, including rank/metadata, are retained.

## Exact searchable vs ingested vs inspected scopes

| Scope | What can be asserted |
| --- | --- |
| `source_ingested_scope` | Complete Markdown for each of 583 canonical included assessments imported via connector source `Data`. |
| `lexical_or_semantic_index_scope` | Precisely **3,498 Cognee `DocumentChunk` nodes**, six S1/S2/S3/S3*/S4/S5 function sections × 583 assessments, including project/repository header. **CHUNKS_LEXICAL only**. Not full-body lexical or semantic indexing. |
| `inspected_source_scope` | **NONE YET** at C2: complete assessment and pinned upstream-code inspections are deliberately deferred until post-C2 candidate comparison. |
| Known gap | Front matter, introductory rationale, and nonfunction prose may be stored but are **not automatically discoverable** via these chunks. Rank is lexical retrieval, not evidence that a system fits a game agent. |

**Coverage decision before C3:** The frozen task queries generated native top-20 hits. Evaluate their task relevance first, preserving irrelevant records. If S1–S5 section-only hits do not support a sufficient candidate comparison, stop and create a **separately identified fresh full-body indexing dataset**, with its own patch, raw receipt, native queries and audit, before claiming that full text influenced design. No full-body or semantic search claim is made here.

## Lossless original receipts

The external connector emitted a **4,522,318 byte** original UTF-8 log with SHA256 `d2e14572693898025e1d75aa09815b94d98eb4d3c191783604d832600e1f9e21`. To fit source hosting as text, it is stored in [base64 of gzip](../receipts/discovery/connector-import-original.log.gz.base64) (decode base64 then decompress gzip; original bytes are restored losslessly). Compressed-gzip SHA256: `f70ca5bcea05532623a5d50a7ebf9ffa6cb6b1cba6881d7d9eb631f30cb0ae9f`.

[Independent audit](../receipts/discovery/independent-audit.json.gz.base64) original JSON SHA256: `934c560f356935c87536271ff2d5e228791bc3db46ccb6a8fddc2844692964ef`.

[Native query manifest](../receipts/discovery/native-search-manifest.json.gz.base64) original SHA256: `71d2c273acfaeda34b45dfdda8e80f4b29ecfc11eb00f3813063739b15151032`.

Every raw query JSON is stored losslessly as `../receipts/discovery/native-search-I2-QNN.json.gz.base64`. Original uncompressed SHA256:

| Query | SHA256 of raw JSON | Hits |
| --- | --- | --- |
| I2-Q01 | `16524241a444786eb3bb753b5a04fb68b42def55749086563f6177d7726b4b39` | 20 |
| I2-Q02 | `7631cd4479540d4d0787a801e9ed0b63410a16ccbf702c59be1babc716d8a531` | 20 |
| I2-Q03 | `9727873e4f06f446fe3fdb543fe0fecb609627431e449a663ed4c7e7cdba16d6` | 20 |
| I2-Q04 | `5bdc720454fe18ca6e246e2946006151d103fe654c948912f1fd3f00a9a016d1` | 20 |
| I2-Q05 | `a3a2c4e2989b27e65b260eff36a35302503f49713eb8fde3b32a9e71be3a08bc` | 20 |
| I2-Q06 | `3af64ba16f8ca346f6efeadef284c45b566a9581032c5cef2d7fcd86cb2e02d2` | 20 |
| I2-Q07 | `8b1178335629ad5b54e610e0a21a9588af19d90d04a8aef6c1da6a4e6a5e8855` | 20 |
| I2-Q08 | `c2e5a18a0b6d287042252c854b1d9c7befee38db254c9cb6f91339e26dbf7c46` | 20 |

Rehydrate in a clean shell (does not run the game): `base64 --decode < FILE.gz.base64 | gzip -d > FILE`; verify the above original SHA256 with `sha256sum FILE`. Both insertion of entire Markdown into `Data` and selected function-section lexical indexing belong to the **original pinned connector path**; no custom SDK-only importer was substituted.

## C2 status and boundary

**Gate 1 / C2: PASS** for the scoped six-section native lexical search and independently audited source ingestion. **No mechanism shortlisted, selected or implemented yet**. Next permitted step: assess retrieved hits, read full pinned canonical assessments/upstream source, publish alternatives comparison, then a separate C3 architecture decision. Runtime, game-playing performance and model quality remain `NOT_RUN` / `NOT_EVALUATED`.
