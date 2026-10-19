# Iteration 2 — C2 status (2026-10-19)

**C2_EXECUTED_BUT_PUBLICATION_INCOMPLETE; not a PASS checkpoint.**

C1 preregistration: `dc57a1a80a1db4f31e2a215513419e960416fb8e` (before new import). Dataset: `game-iter2-b5c73a233c13455986e10f86689e5dbc`. Index SHA `5cbb1035538b8f80fa3362f1c99652f4fd7c55e8`, OpenSiro connector SHA `d176484e85da55c84450d67040cb4a2d096353c7`, patch SHA256 `8718a48443e471ac14d45459af2718b87b986b6a8e523a44573368741644a9ae`.

Real pinned connector invocation completed with `PASS_FRESH_LOCAL_COGNEE_IMPORT`: 583 included full assessments, 12,201 nodes, 8,120 edges, 3,498 exact function grades. Independent, separate-process audit returned **PASS**, matching all 583 source identities and 3,498 grades with `states_exact=true`, `source_refs_exact=true`. Full audit data: [independent-audit.json](../receipts/discovery/independent-audit.json).

Eight preregistered **native** `cognee.search` `CHUNKS_LEXICAL` queries I2-Q01–I2-Q08 returned 20 unfiltered hits each; negative Q08 produced 20 irrelevant hits. Ingested corpus = 583 complete Markdown files. Searchable scope = only 3,498 S1/S2/S3/S3*/S4/S5 sections. **Not full-body or semantic retrieval.** No new full upstream source inspection yet.

Original 629,057 bytes of query JSON, and connector-import logs, remain saved in the isolated execution workspace; their SHA256 digests and sizes are published in [raw-receipt-hashes.json](../receipts/discovery/raw-receipt-hashes.json). [Original native query manifest](../receipts/discovery/native-search-manifest.json) is also published. Large original raw query receipt GitHub upload was blocked by the available tool boundary. Hashes and top-hit lists do **not** replace raw receipt publication.

**Fail-closed:** C2 public Git receipt gate incomplete; C3 candidate comparison, architecture choice, implementation of `game_harness/`, and C4 **not authorized yet under the skill**. No runtime or game/model API was invoked.

Status: `process_status=PARTIAL`; `build_status=PARTIAL`; `verification_level=SOURCE_ONLY`; `runtime_status=NOT_RUN`; `evaluation_level=NOT_RUN`; `model_quality_claim=NOT_EVALUATED`; `adaptation_outcome=NOT_DECIDED`; `discovery_contribution=INDETERMINATE`.
