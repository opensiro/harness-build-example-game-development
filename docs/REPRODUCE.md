# Reproduction — Cognee-first game harness construction

This is a **source/provenance and architectural-construction** reproduction protocol, **not** a gameplay, model inference or benchmark procedure. Do **not** run `python -m game_harness` unless a separate runtime/gameplay authorization is given.

## 1. Governing immutable sources

| Surface | Frozen ref |
| --- | --- |
| Canonical bootstrap | `opensiro/vsm-oss-organization`, `184526ca9e1a5968b5133d84b47ad94c6921954d` |
| Experiment protocol | `opensiro/vsm-harness-skills`, merged PR #52 commit `5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25` |
| Canonical included assessment corpus | `opensiro/vsm-harness-index`, `b48b13e74d6938f833094d3f9afc1a11e61a8515` |
| OpenSiro Cognee source connector | `opensiro/cognee-community`, `d176484e85da55c84450d67040cb4a2d096353c7` |
| Connector's versioned package | `packages/connector/opensiro-vsm`; Cognee SDK `1.6.4`, Python `3.12` in original run |

This connector is in an **OpenSiro review branch**, not a released upstream connector. Its source must not be silently substituted with `cognee.add` directly, a generic document importer, source grep or cached historical results.

All assertions about *original* execution are backed by the [original data receipts](../receipts/discovery/). A fresh reproduction is a **different run**, not a recreation of the original timestamps.

## 2. Source-only artifact verification (no game execution)

Clone the public experiment repository and check out the published C4 revision for reproducible source/static checks:

```bash
git clone https://github.com/opensiro/harness-build-example-game-development.git
cd harness-build-example-game-development
git checkout experiment/game-cognee-first-20261018
python3 tools/check_source_only.py
python3 tools/verify_construction_source.py
```

These **inspect source text, AST, preserved receipts and Git ancestry**, and do not import `game_harness` or invoke `EpisodeRunner.run`. Reconfirm this property before execution if modifying the checkers. For immutable reproduction, replace the branch checkout with the full C4 SHA from this run's final commit.

## 3. Reconstruct the original connector discovery process

The following requires a clean Linux environment, Python 3.12, adequate free storage/memory and network access to public GitHub and Python packages. All model calls/embeddings can stay disabled; the connector uses native graph projection and `CHUNKS_LEXICAL` search.

**First attempt only:** choose a **new, never used** directory. If an import fails or is interrupted, preserve the failed attempt, choose a new directory/dataset, and keep its error receipt. Do not retry against any written dataset/store.

```bash
set -eu
RUN_DIR="$(mktemp -d)"
RESEARCH_REPO="$PWD"

git clone https://github.com/opensiro/vsm-harness-index.git "$RUN_DIR/index"
git -C "$RUN_DIR/index" checkout b48b13e74d6938f833094d3f9afc1a11e61a8515

git clone https://github.com/opensiro/cognee-community.git "$RUN_DIR/connector"
git -C "$RUN_DIR/connector" checkout d176484e85da55c84450d67040cb4a2d096353c7

git -C "$RUN_DIR/connector" apply "$RESEARCH_REPO/receipts/preflight/connector-shard-compat.patch"
git -C "$RUN_DIR/connector" diff --binary | sha256sum
# Expected patch SHA256:
# 5be20dfacb2f8d48608b2aa4b9d4fbc6a43050e1f799678e8770ecb48a00b070

python3.12 -m venv "$RUN_DIR/sdk"
"$RUN_DIR/sdk/bin/python" -m pip install -e "$RUN_DIR/connector/packages/connector/opensiro-vsm"
export PYTHONPATH="$RUN_DIR/connector/packages/connector/opensiro-vsm"
mkdir "$RUN_DIR/receipts"

# BEFORE THE FIRST IMPORT: review this run's frozen query plan at C1.
"$RUN_DIR/sdk/bin/python" -m cognee_community_connector_opensiro_vsm validate \
  --repo "$RUN_DIR/index" \
  --commit b48b13e74d6938f833094d3f9afc1a11e61a8515

# Actual connector ingestion, not direct SDK-only ingestion:
"$RUN_DIR/sdk/bin/python" "$RUN_DIR/connector/packages/connector/opensiro-vsm/examples/example.py" \
  --repo "$RUN_DIR/index" \
  --commit b48b13e74d6938f833094d3f9afc1a11e61a8515 \
  --store-root "$RUN_DIR/fresh-store-01" \
  --dataset game-cognee-b3345272-full-01 \
  --all --lexical \
  > "$RUN_DIR/receipts/connector-import-original.log" 2>&1

# Separate process; audit must PASS before searching:
"$RUN_DIR/sdk/bin/python" "$RESEARCH_REPO/tools/c2_native_receipts.py" \
  audit --root "$RUN_DIR"

"$RUN_DIR/sdk/bin/python" "$RESEARCH_REPO/tools/c2_native_receipts.py" \
  search --root "$RUN_DIR"
```

The helper's dataset name and `fresh-store-01` directory are currently fixed to their **original-run values**. This is safe only because `RUN_DIR` is a genuinely new isolated store. A retry must use a new `RUN_DIR`; when adapting the helper to a different dataset identity, record that configuration delta with the new run.

**Important:** the original host reused a preinstalled compatible Cognee SDK to avoid downloading dependencies. The clean `pip install -e` path above describes a dependency-resolution route, **not a claim that this clean installation was executed during the original experiment**. If it fails, report a packaging/environment blocker, not a connector import result.

## 4. What the exact queries can find

The frozen C1 first pass is Q01–Q08 in [`reports/c1-run-contract.md`](../reports/c1-run-contract.md). The eight unmodified original native query receipts appear as `receipts/discovery/native-search-Qxx.json`, with `top_k=15` and `SearchType.CHUNKS_LEXICAL`.

- `source_ingested_scope`: full contents of **581** accepted assessment Markdown documents held as pinned Cognee document source Data.
- `lexical_or_semantic_index_scope`: exactly **3,486** chunks across **six function sections per included assessment**. Introductory rationale/front matter/body sections outside S1–S5 are **not full-document lexical hits**.
- `inspected_source_scope`: the **four** selected complete canonical assessment documents and reviewed upstream Git files **after** native query publication.

Negative Q08 returned irrelevant records. Every native hit is a lead, not a proven architecture. Use [source-to-code traceability](../reports/source-to-code.md) and [C3 comparison](../reports/candidate-comparison.md) for the downstream (non-retrieval) evidence chain.

## 5. Reconstruct the engineering decision, without running the game

Review the immutable commits in this order:

1. [C1 contract](https://github.com/opensiro/harness-build-example-game-development/commit/b3345272ee01c89bf2dc86870d35602b1e3894c8).
2. [C2 query receipts](https://github.com/opensiro/harness-build-example-game-development/commit/d6c757f701501f1f555c009d5163c6852e33e33f).
3. [C3 candidate comparison](https://github.com/opensiro/harness-build-example-game-development/commit/f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0).
4. [C3 separate architecture decision](https://github.com/opensiro/harness-build-example-game-development/commit/cb33282d1cb5454841f87dd486df86da60cae787).
5. [First original implementation](https://github.com/opensiro/harness-build-example-game-development/commit/ee8da1ca036ab4d853c134180b0b6f1716e9e346) and C4 final source commits.

Check ancestry with `git merge-base --is-ancestor` for each adjacent pair. It attests **public artifact order**; not the unobservable private origin of developer intent. The independent evidence link at C3 is explicit native Q01#1 → canonical Ascension → pinned Rust upstream → original Python source.

## 6. Deliberately out of scope

No game episodes, gameplay CI, runtime harness unit/smoke tests, hosted inference, model quality benchmark, win-rate improvement, or proof of operational correctness were performed. Results use `evaluation_level=NOT_RUN`, `runtime_status=NOT_RUN`, `model_quality_claim=NOT_EVALUATED`. Source-level completion must never be relabeled an empirically validated agent.
