# C4 — Constructed Game Harness and Verification Boundary

**Experiment:** `game-cognee-first-20261018`  
**Governing protocol:** `build-harness-cognee-first v0.1.0`, merged Skills SHA `5d36fd2e40e4e8a1711b1f315f7a60a9a78a2a25`.  
**Construction:** ADOPTED architecture OPT-A, recorded at **C3 ADR commit** `cb33282d1cb5454841f87dd486df86da60cae787`. First actual implementation commit `ee8da1ca036ab4d853c134180b0b6f1716e9e346` follows it.  
**Subject:** development-process repeatability and traceability — *not game win rate or model quality*.

## Constructed source

A new, original, compact Python 3.12 `game_harness` package with:

- `contracts.py`: immutable observation/action/receipt data types and the agent/environment interfaces.
- `veiled_duel.py`: new partially observable, turn-based hidden-intent game, authoritative legal-action catalog, state generations and terminal outcomes.
- `runner.py`: bounded `EpisodeRunner`; validates current-generation candidate action against the authorized catalog, and requires a settled, identity-matched, witnessed state transition with a newer observation before progressing.
- `policy_jsonl.py`: external AI-agent policy bridge using newline-delimited JSON; does not call or require an inference provider.
- `__init__.py`, `__main__.py`: public package and **opt-in executable entry point**.

No previous version's MiniGrid or other game harness was reused. The only adaptation claimed is the narrowed generation-bound legal-action/settlement pattern traced to the **first native Cognee Q01#1** discovery result for Ascension, complete canonical assessment, and its pinned upstream Rust code. See [`source-to-code.md`](source-to-code.md) for every link. Other implementation features (toy game rules, JSONL transport) are original construction glue rather than invented Cognee discoveries.

## Original discovery and causal order

| Checkpoint | Public SHA / source |
| --- | --- |
| C1 frozen task/query/corpus selection | `b3345272ee01c89bf2dc86870d35602b1e3894c8` |
| C2 original native import, independent audit PASS, raw native queries | `d6c757f701501f1f555c009d5163c6852e33e33f` |
| C3a full-assessment/upstream alternative comparison | `f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0` |
| C3b distinct architecture decision | `cb33282d1cb5454841f87dd486df86da60cae787` |
| C4 first source implementation | `ee8da1ca036ab4d853c134180b0b6f1716e9e346` |
| C4 final receipts, hashes, trace and status | This report and `receipts/verification/` in the final **post-implementation** publication commit |

Verified ancestry through the static evidence script: **C1 → C2 → C3a → C3b → C4-first** (all consecutive merge-base `--is-ancestor` checks PASS). The final C4 publication must also have the first implementation as an ancestor. Commit order attests public evidence chronology, not private thinking.

## Exact source/static verification performed

Allowed checks performed after constructing the source:

1. [`tools/check_source_only.py`](../tools/check_source_only.py): AST parse all Python game-harness modules, source SHA256, required data/protocol/method presence, duplicate method guard, no direct runtime Cognee or model dependencies. Does **not** import the game.
2. [`tools/verify_construction_source.py`](../tools/verify_construction_source.py): source AST parse and compilation without execution, allowed module-import surface, original compressed connector-log SHA256, C2 import/audit/manifests and all eight original native receipts, canonical identity matching, ancestry among C1/C2/C3/C4-first commits. Does **not** call the game runtime.
3. Output retained under `receipts/verification/static-check.json`, `receipts/verification/provenance-check.log`, and `receipts/verification/game-harness-source-sha256.txt`. The checker itself is a **source-only** tool, not a gameplay test.

The source/AST checker reported `PASS_STATIC_AST_ONLY`; evidence checker reported `NATIVE_RECEIPT_OK Q01`–`Q08`, `PROVENANCE_STATIC_OK included=581 chunks=3486 native_queries=8`, four ancestry `CHRONOLOGY_OK` confirmations, and `STATIC_CHECKED: source/evidence/chronology only; GAMEPLAY NOT_RUN`.

### Explicit limits

- The **581 full source Markdown documents** were imported into a fresh Cognee dataset, but native lexical retrieval was limited to the **six S1–S5 function sections** per assessment (3,486 chunks), **not full-body retrieval**; native Q08 deliberately returned irrelevant hits.
- **Late source-content inconsistency observed, not retroactively repaired:** the pinned Continual Harness assessment's frontmatter has `status: included` and canonical catalog membership (which govern connector admission), while its final narrative sentence still says `status: proposed`. Its full Markdown was read and compared as a **canonically included** record; this stale prose was not used to claim an admission transition or influence OPT-A selection.
- No source-free speculation about other harnesses and no performance inference from VSM autonomy labels. `discovery_contribution=DIRECT` is limited to the **observed first architectural lead**, not comparative Cognee superiority.
- **No game episodes were run.** The Python package was *not imported or instantiated for gameplay verification*. No runtime harness tests, model inference, win-rate benchmark, gameplay CI or actual agent evaluation occurred.
- Original toy-game rules/termination logic and the JSONL external-policy bridge are **inspectable and syntactically checked, not behaviorally proven**. Dynamic defects may remain.
- The toy environment's pseudorandom opponent intent uses a deterministic seed, which is also reflected in its current state identifier. Partial observability here means the **direct public observation omits unprobed intent**, **not** that a policy with access to seed/source cannot infer future intent. This is not an adversarial secrecy guarantee.
- Ascension's remote recovery/idempotency/reconciliation, authenticated MCP gateway, Rust code and tooling are **not** implemented; the synchronous new harness stops on unknown effects rather than attempting distributed settlement.
- Model and upstream code usage: no provider selected, no API credentials required, no copied upstream source. Licensing: new code MIT; inspected upstream license notices retained with source links.
- Do not trigger a gameplay CI workflow indirectly by merging a PR. No automated game/test actions were added to this repository.

## Frozen final state (development-process claims only)

| Field | Result | Meaning |
| --- | --- | --- |
| `process_status` | **PASS** | Public C1→C2→C3a→C3b→C4 source-construction/evidence chain, with correct chronology |
| `build_status` | **PASS** | Inspectable original Python source, dependencies/entrypoint and source-to-code mapping complete |
| `verification_level` | **STATIC_CHECKED** | Source, AST, dependency-surface, provenance and immutable Git ancestry only |
| `runtime_status` | **NOT_RUN** | No game or model execution |
| `evaluation_level` | **NOT_RUN** | No gameplay benchmark or runtime functional check |
| `model_quality_claim` | **NOT_EVALUATED** | No improvement in gameplay/strategy shown or claimed |
| `adaptation_outcome` | **ADAPTED** | One bounded Ascension-informed mechanism selected and newly constructed |
| `discovery_contribution` | **DIRECT** | First recorded selected mechanism originated at native Cognee `Q01#1`, limited to the search index's section scope |

A successfully traced development process and complete source artifact do **not** imply a functionally verified agent. A future test of the game harness or inference backend must be separately authorized and independently recorded.

## Reproduce

See [fresh connector reproduction](../docs/REPRODUCE.md) and [public original receipts](../receipts/discovery/). Source-only checks: `python3 tools/check_source_only.py` and `python3 tools/verify_construction_source.py`. **Do not invoke `python3 -m game_harness`** for this source-only research reproduction.
