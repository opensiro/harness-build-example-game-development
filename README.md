# Game Harness Construction via Cognee-First Discovery

This repository is a **new, independent, evidence-first construction experiment**.

**Research question:** How can a game-playing AI agent harness be constructed by discovering and adapting mechanisms through real Cognee queries over canonical OpenSiro VSM assessments, then inspecting the pinned upstream implementations?

The object of study is the **harness development process**, not gameplay performance.

## Protocol

- Mandatory skill: [build-harness-cognee-first v0.1.0](https://github.com/opensiro/vsm-harness-skills/blob/96ebaec765496dc030001c0b2b571a65674a01b1/skills/build-harness-cognee-first/SKILL.md), an experimental draft in [PR #52](https://github.com/opensiro/vsm-harness-skills/pull/52).
- Evidence checkpoints: C1 preflight → C2 native Cognee import/audit/retrieval → C3 compared upstream mechanisms and a subsequent architecture decision → C4 source construction.
- **Fail-closed:** No game environment, benchmark, agent mechanism or candidate source is chosen before passing Cognee Gate 1.
- **Execution boundary:** No game episodes, model inference, gameplay CI, runtime harness tests or performance evaluations without separate authorization.

## Current status

This initial README establishes a clean repository baseline only. Check the experiment branch and its `reports/`, `receipts/`, and `traces/` paths for actual evidence. Do not interpret a planned checkpoint as completed evidence.

- `process_status: PARTIAL`
- `build_status: NOT_STARTED`
- `verification_level: NOT_RUN`
- `evaluation_level: NOT_RUN`
- `model_quality_claim: NOT_EVALUATED`

No original implementation has been reused.
