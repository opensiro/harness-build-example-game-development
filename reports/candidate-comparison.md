# C3a — Source-backed Candidate Comparison (PRE-DECISION)

**Published after C2:** [native connector/import/audit/query receipts at `d6c757f701501f1f555c009d5163c6852e33e33f`](https://github.com/opensiro/harness-build-example-game-development/commit/d6c757f701501f1f555c009d5163c6852e33e33f). This document compares alternatives only. **No architecture, game environment or preferred mechanism is selected in this commit.** A separate subsequent architecture-decision commit is mandatory.

The four candidates below originate from **fresh native Cognee retrieval**, not outside search and not the previous game experiment. Every shortlisted candidate's **complete included assessment** was read from pinned Index `b48b13e74d6938f833094d3f9afc1a11e61a8515`. Code was independently inspected at each assessment's reviewed upstream Git SHA. VSM autonomy grades describe organizational ownership, **not** game performance or design ranking.

## Search trace and authoritative sources

| Candidate | Original native hit(s) | Full canonical assessment SHA256 | Upstream Git SHA |
| --- | --- | --- | --- |
| **A — Ascension** | `Q01#1`, `Q04#11` (game observation/action) | `cd2a74a004f62a4bcf11fa2185d94e767b02ce3b23b2ec012ca86f44619ab6f3` | `53312ddbb074f7c187e5f59d88b6585da797fe17` |
| **B — Concordia** | `Q01#2` S2, `Q01#4` S3, `Q04#15` | `b8c6237718c4add0b75cf810762133385fe1e5f1bba8826d8fe45af9efe24bbb` | `3e30a207bb2b75f9cf837fa6b657c466ca450765` |
| **C — Continual Harness** | `Q01#3` S1, `Q07#5` S4 | `d75b2bba758dcb3b57a03c1c14ce13bfe5b51ff3b1a26ee9505ba36895c789fa` | `bbab97ad73e460b7cd7c08527d10ced30cc03fbe` |
| **D — LLaMAR** | `Q01#8` S1, `Q02#9` S1, `Q04#2` S4 | `3cf66302e838af7fe2b46b9dcfb4158622ea63574f75c9f643c8c75c82e275d1` | `d2b74cac79a0f070d87a150712f8e2ae174920be` |

Complete assessment URLs:
[A](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/as/ascension.md),
[B](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/co/concordia.md),
[C](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/co/continual-harness.md),
[D](https://github.com/opensiro/vsm-harness-index/blob/b48b13e74d6938f833094d3f9afc1a11e61a8515/assessments/ll/llamar.md).

## Mechanism/source inspection

### A — Ascension (MIT)

**Potential mechanism:** authoritative, generation-bound observation and legal-action catalog; policy proposes among legal actions; a separate runtime port applies them; the resulting effect must be settled and based on a fresh observation before advancing. The legal-action source is outside the model.

- [`EpisodeRuntimePort` observe/legal_actions/dispatch, runner.rs L35–125](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner.rs#L35-L125).
- [`DecisionInput` and policy interface, policy_router.rs L22–64](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/policy_router.rs#L22-L64).
- [Generation matching / admission, runner_actions.rs L235–267](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/runner_actions.rs#L235-L267).
- [Accepted/unknown/settled receipt and fresh generation, postconditions.rs L49–86](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/crates/harness/src/episode/postconditions.rs#L49-L86).
- [Pinned MIT license](https://github.com/AI-Ascension/sts2-harness/blob/53312ddbb074f7c187e5f59d88b6585da797fe17/LICENSE).

**Fit:** direct game-playing source, explicit partial-observation authority boundary, bounded action sequence, inexpensive source-level adaptation possible without connecting to a commercial game. **Cost/risk:** original Rust/MCP/gateway/recovery/management infrastructure is far beyond a source-only prototype; live STS2 gameplay depends on an external copyrighted game; adapting settlement for a synchronous deterministic local environment may require only a subset of checks rather than the full distributed recovery system.

### B — Concordia (Apache-2.0)

**Potential mechanism:** sequential entity acts, but putative event is resolved by the Game Master and only then returned as changed observation. This separates *proposal* from *authoritative world transition*.

- [Turn-based engine and actor/GM boundary, sequential.py L67–73](https://github.com/google-deepmind/concordia/blob/3e30a207bb2b75f9cf837fa6b657c466ca450765/concordia/environment/engines/sequential.py#L67-L73).
- [Observation → acting entity → putative action → Game Master resolve, sequential.py L265–335](https://github.com/google-deepmind/concordia/blob/3e30a207bb2b75f9cf837fa6b657c466ca450765/concordia/environment/engines/sequential.py#L265-L335).
- [Simultaneous-move alternative, simultaneous.py L69–80](https://github.com/google-deepmind/concordia/blob/3e30a207bb2b75f9cf837fa6b657c466ca450765/concordia/environment/engines/simultaneous.py#L69-L80).
- [Pinned Apache-2.0 license](https://github.com/google-deepmind/concordia/blob/3e30a207bb2b75f9cf837fa6b657c466ca450765/LICENSE).

**Fit:** good conceptual separation of agent choices and authoritative environment transition for a turn-based game. **Cost/risk:** general social simulation, multiple agents and often model-driven Game Master are excessive; Game Master world adjudication is **not** automatically VSM S3. A deterministic local rules engine would be narrower than Concordia's generative world model.

### C — Continual Harness (MIT)

**Potential mechanism:** continuing game agent loops through a tool/environment adapter with persistent trajectory context. Optional `HarnessEvolver` consumes recent trajectories and performs four separate model-driven changes (prompt, subagents, skills, memory) mid-episode.

- [Agent scaffold and environment wiring, run.py L53–60, L128–132, L272–278](https://github.com/sethkarten/continual-harness/blob/bbab97ad73e460b7cd7c08527d10ced30cc03fbe/run.py#L53-L60).
- [Adaptive evolution scheduling / trajectory-consuming passes, harness_evolver.py L98–141](https://github.com/sethkarten/continual-harness/blob/bbab97ad73e460b7cd7c08527d10ced30cc03fbe/agents/utils/harness_evolver.py#L98-L141).
- [Agent runtime and evolver wiring, PokeAgent.py L262–309](https://github.com/sethkarten/continual-harness/blob/bbab97ad73e460b7cd7c08527d10ced30cc03fbe/agents/PokeAgent.py#L262-L309).
- [Pinned MIT license](https://github.com/sethkarten/continual-harness/blob/bbab97ad73e460b7cd7c08527d10ced30cc03fbe/LICENSE).

**Fit:** demonstrates long-horizon continuity and history as input to later choices. **Cost/risk:** full harness self-evolution and emulator/ROM dependencies are not needed to demonstrate source-driven construction; model calls to generate persistent code/skills would violate the current no-inference execution boundary, if run. **S4=A** is an ownership classification, not evidence that evolution improves game quality.

### D — LLaMAR (MIT)

**Potential mechanism:** multiple partial-observation robot streams, planner with whole-team open subtasks, action per robot, environment outcomes, in-band verifier, then updated plan.

- [Episode planner/actor/env.step/verifier/replan, llamar.py L89–166](https://github.com/nsidn98/LLaMAR/blob/d2b74cac79a0f070d87a150712f8e2ae174920be/AI2Thor/baselines/llamar/llamar.py#L89-L166).
- [Partially observable whole-team input and state, llamar_utils_multiagent.py L42–68](https://github.com/nsidn98/LLaMAR/blob/d2b74cac79a0f070d87a150712f8e2ae174920be/AI2Thor/baselines/llamar/llamar_utils_multiagent.py#L42-L68).
- [Actual cross-agent blocking/failure correction, llamar_utils_multiagent.py L109–156](https://github.com/nsidn98/LLaMAR/blob/d2b74cac79a0f070d87a150712f8e2ae174920be/AI2Thor/baselines/llamar/llamar_utils_multiagent.py#L109-L156).
- [Pinned MIT license](https://github.com/nsidn98/LLaMAR/blob/d2b74cac79a0f070d87a150712f8e2ae174920be/LICENSE).

**Fit:** demonstrates embodied partial observations, shared long-horizon plan and feedback, plus real inter-agent interference. **Cost/risk:** AI2-THOR/SAR simulator, vision inputs, multiple robot streams and per-step model calls are much heavier than needed for a construction-only example. The in-band verifier is not independently established S3*.

## Compared construction alternatives (not selected yet)

| ID | Source-backed candidate construction | Distinct tradeoff |
| --- | --- | --- |
| OPT-A | Small original turn-based hidden-information card encounter; explicit generation-bound legal-action catalog and result settlement from Ascension | Narrow interface, no emulator or frontier inference; may under-represent asynchronous-effect recovery |
| OPT-B | Text-based multi-entity social simulation using Concordia-like turn resolution and Game Master feedback | Clear independent rule authority; unnecessary multiple agents and scenario construction |
| OPT-C | Long-running emulator-integrated game agent with trajectory-driven harness evolution from Continual Harness | Highest persistence/adaptation depth but high runtime/model and third-party asset burden |
| OPT-D | Multi-robot partially observed world with shared planner/verifier from LLaMAR | Shows coordination/partial observability but requires heavyweight simulator and multiagent operation |
| OPT-0 | Minimal environment-neutral observation/action/feedback driver without an adapted source mechanism | Smallest deliverable; a legitimate NO_ADAPTATION option, but cannot claim a positive Cognee-driven mechanism if retrieval did not influence it |

**No option has been chosen here.** Later decision must explicitly record selected/rejected IDs, tradeoffs, query/hit evidence and `discovery_contribution`. Implementations and game environment choice must come strictly **after** a distinct decision commit.

## Search boundaries and candidates not shortlisted

All original hits are retained, including irrelevant `Q08` (15 hits on unrelated assessments, not validated relevance). `Q02` was dominated by S3* audit passages and does not imply useful partial-observability mechanisms. Other hits (e.g., `hypha`, `harness-r1`, `browser-harness`, `turix-cua`) remain in the original receipts as uncovered/not fully compared possibilities; their appearance in a result does not imply endorsement or rejection after complete source inspection. Full-body architectural information outside the six function sections was **not searchable**, even though the complete shortlisted assessment documents were later read. This is a substantive recall limitation and the comparison cannot claim the global best possible architecture.

No gameplay, model inference, simulator action, unit/runtime harness evaluation or benchmarking was run.
