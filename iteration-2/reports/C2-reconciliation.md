# Iteration 2 — C2 receipt reconciliation (append-only correction)

**Date:** 2026-10-19. This note does **not** alter any original Iteration 1 receipts, nor pretend that two independent read passes share one timestamp.

## Which prospective discovery is the C2 Git anchor?

The **first complete C2 query read** followed the connector import and independent audit around 13:14–13:15 UTC. Its independently source-audited native query results are stored as **full original bytes** in `iteration-2/receipts/discovery/native-search-I2-Q01.json.gz.base64` through `I2-Q08.json.gz.base64`, and its native manifest/audit as matching `.gz.base64` artifacts. These receipts were publicly committed before:

- [C2 anchor `3a6b7de`](https://github.com/opensiro/harness-build-example-game-development/commit/3a6b7debecb5719c4319eef9579d143a6f3062d1)
- [C3 comparison `0184e3d`](https://github.com/opensiro/harness-build-example-game-development/commit/0184e3d7e1432e6209ca248c4a075f2c5c7dbd89).

Original import log SHA256: `d2e14572693898025e1d75aa09815b94d98eb4d3c191783604d832600e1f9e21`. The pinned Index, dataset, connector patch and function search scope are documented in [C2 discovery](C2-discovery.md). The lossless archive's JSON Q01 SHA256 is `16524241a444786eb3bb753b5a04fb68b42def55749086563f6177d7726b4b39`.

## Why do the additional published SHA256 values differ?

A **subsequent** independent audit and native query read of the **same already-imported Cognee dataset** occurred around 14:04–14:06 UTC. Its per-query byte hashes, e.g. I2-Q01 `624963ea675f55239b4ec482eb0af4da6cf5f99b8aa0517f4cca5e71403d8e74`, appear in [raw-receipt-hashes.json](../receipts/discovery/raw-receipt-hashes.json). Repeated reads necessarily have different `recorded_at_utc` / `started_at_utc` / `finished_at_utc` and therefore different **byte hashes**, even when the underlying search-hit data are the same. They are **not** hashes of the Git-published first-run archives.

That later read was accompanied by [C2-discovery-status.md](C2-discovery-status.md) and an I2-E004 appended trace event declaring `C2_EXECUTED_RAW_PUBLICATION_INCOMPLETE`, which accurately described **that later read's local file-publication state at that moment**. It does **not** overturn the previously published first-run C2 source/audit/native receipts and cannot be used to date the earlier comparison as post-C2 if the first-run C2 were absent. Preserve both entries as historical observations.

This correction is append-only: it identifies the chronology, distinguishes the two reads, and declares the first-run C2 `PASS` anchor. It does **not** erase or re-time either experiment. Both passes stayed within the original eight frozen queries and six-function `CHUNKS_LEXICAL` scope; no full-body semantic/lexical search is claimed. Negative I2-Q08 unhelpful hits remain included.

## Reproducibility check

Decode the `.gz.base64` records as `base64 -d | gzip -d` and compare their SHA256 against the **first-run** table in [C2-discovery.md](C2-discovery.md). A separate source-only inspection in this iteration verified that the published archives decode and match all first-run hashes and lengths (583 included sources, 3,498 function chunks, all eight 20-hit queries). No game, external AI policy or model inference was executed to perform this check.

**Effective process checkpoint:** C1 → C2 `3a6b7de` → C3a `0184e3d` → C3b [architecture decision](C3-architecture-decision.md) → C4 source. The later duplicate I2-E004 event is superseded **only as a gate status conclusion**, never deleted as evidence.
