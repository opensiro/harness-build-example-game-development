#!/usr/bin/env python3
"""Static-source and Git-provenance verification ONLY; never imports a game module."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import subprocess


BASE = "3a93532d70b6dccad2d5e83a7a0e6532456fff6b"
ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game_harness"


def git(*args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    ).stdout


def run_source_check() -> dict:
    sources = {}
    modules = {}
    for path in sorted(GAME.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
        modules[path.name] = (text, tree)
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()

    # Baseline authority and all original Iteration 1 provenance remain unchanged.
    for rel in ("game_harness/contracts.py", "game_harness/veiled_duel.py"):
        historical = git("show", BASE + ":" + rel)
        if historical != (ROOT / rel).read_bytes():
            raise ValueError("Original environment/contract altered: " + rel)
    prior_evidence_changes = git("diff", "--name-only", BASE, "HEAD", "--", "receipts", "reports", "traces")
    if prior_evidence_changes.strip():
        raise ValueError("Immutable Iteration 1 evidence was changed")

    runner, runner_ast = modules["runner.py"]
    policy, policy_ast = modules["policy_jsonl.py"]
    context, context_ast = modules["agent_context.py"]
    runner_class = next(
        n for n in runner_ast.body
        if isinstance(n, ast.ClassDef) and n.name == "EpisodeRunner"
    )
    methods = {n.name for n in runner_class.body if isinstance(n, ast.FunctionDef)}
    assert {"run", "_propose"}.issubset(methods)

    # Structural check only: the runner's source records context after settling.
    run_body = ast.get_source_segment(
        runner, next(n for n in runner_class.body if isinstance(n, ast.FunctionDef) and n.name == "run")
    )
    assert run_body is not None
    first_dispatch = run_body.index("receipt = self.environment.dispatch_action(identity)")
    verify = run_body.index("next_observation = verify_settlement(current, identity, receipt)")
    update = run_body.index("context = context.after_settlement(")
    assert first_dispatch < verify < update
    assert "max_context_events" in runner
    assert "raise HarnessProtocolError" in runner
    assert "max_request_bytes" in policy and "max_reply_bytes" in policy
    assert "self.replies.readline(self.max_reply_bytes + 1)" in policy
    assert "def decide_with_context" in policy and "def decide(" in policy
    assert "class AgentContext" in context and "class PolicyDecision" in context
    assert "self.environment.dispatch_action" not in context
    forbidden_runtime_imports = ("cognee", "torch", "transformers", "requests")
    for _, tree in modules.values():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports = [name.name for name in node.names]
            elif isinstance(node, ast.ImportFrom):
                imports = [node.module or ""]
            else:
                continue
            if any(i.split(".")[0] in forbidden_runtime_imports for i in imports):
                raise ValueError("Unexpected runtime research/model import")
    return {
        "status": "PASS_SOURCE_STATIC",
        "verification_level": "STATIC_CHECKED",
        "runtime_status": "NOT_RUN",
        "evaluation_level": "NOT_RUN",
        "baseline_commit": BASE,
        "scope": "AST parse; source ordering heuristics; baseline Git-bytes/provenance check",
        "modules_parsed": sorted(sources),
        "source_sha256": sources,
        "limitations": [
            "No module imported or executed",
            "No game, model API, JSONL transport, or runtime tests executed",
            "AST/text checks are not proof of runtime correctness",
            "No generic wall-clock timeout for external TextIO source",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_source_check(), indent=2, sort_keys=True))
