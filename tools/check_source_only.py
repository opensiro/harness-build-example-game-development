#!/usr/bin/env python3
"""Source-only checks. NEVER import the game package or execute a game episode.

Use the AST to verify that the promised source artifact contains the required
interfaces, boundaries and guard predicates. This is NOT a functional/runtime test.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "game_harness"
EXPECTED_FILES = {
    "__init__.py",
    "__main__.py",
    "contracts.py",
    "policy_jsonl.py",
    "runner.py",
    "veiled_duel.py",
}
BANNED_IMPORT_PREFIXES = {
    "cognee",
    "openai",
    "anthropic",
    "google.generativeai",
    "torch",
    "gymnasium",
    "minigrid",
    "ai2thor",
    "requests",
}


def function_names(node: ast.ClassDef) -> set[str]:
    return {
        part.name
        for part in node.body
        if isinstance(part, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def class_members(tree: ast.AST, name: str) -> set[str]:
    matches = [
        n for n in getattr(tree, "body", [])
        if isinstance(n, ast.ClassDef) and n.name == name
    ]
    assert len(matches) == 1, f"Expected exactly one class {name}"
    return function_names(matches[0])


def names_called(tree: ast.AST) -> set[str]:
    calls: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                calls.add(n.func.id)
            elif isinstance(n.func, ast.Attribute):
                calls.add(n.func.attr)
    return calls


def main() -> None:
    actual = {f.name for f in SOURCE_ROOT.glob("*.py")}
    assert EXPECTED_FILES <= actual, f"Missing source: {EXPECTED_FILES - actual}"
    trees = {}
    hashes = {}
    for p in sorted(SOURCE_ROOT.glob("*.py")):
        contents = p.read_bytes()
        trees[p.stem] = ast.parse(contents.decode("utf-8"), filename=str(p))
        hashes[p.relative_to(ROOT).as_posix()] = hashlib.sha256(contents).hexdigest()
        for node in ast.walk(trees[p.stem]):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module] if node.level == 0 and node.module else []
            else:
                continue
            assert not any(
                name == prefix or name.startswith(prefix + ".")
                for name in modules for prefix in BANNED_IMPORT_PREFIXES
            ), f"Runtime-only or prohibited dependency in {p.name}: {modules}"

    c = trees["contracts"]
    for clazz in (
        "Observation", "LegalActionSet", "DecisionInput", "ActionIdentity",
        "TransitionReceipt", "DecisionSource", "EnvironmentPort"
    ):
        class_members(c, clazz)
    assert {"reset", "observe", "legal_actions", "dispatch_action", "step"} <= class_members(
        c, "EnvironmentPort"
    )

    env = trees["veiled_duel"]
    assert {"reset", "observe", "legal_actions", "dispatch_action", "step"} <= class_members(
        env, "VeiledDuel"
    )
    assert {"_rejected", "_draw_intent"} <= class_members(env, "VeiledDuel")
    assert {"legal_actions", "_rejected", "TransitionReceipt"} <= names_called(env)

    runner = trees["runner"]
    assert {"run"} <= class_members(runner, "EpisodeRunner")
    assert {"verify_catalog", "verify_settlement"} <= {
        node.name for node in runner.body if isinstance(node, ast.FunctionDef)
    }
    assert {"verify_catalog", "verify_settlement", "dispatch_action"} <= names_called(runner)

    policy = trees["policy_jsonl"]
    assert {"decide"} <= class_members(policy, "JSONLinesDecisionSource")
    assert "readline" in names_called(policy)

    cli = trees["__main__"]
    assert "main" in {
        node.name for node in cli.body if isinstance(node, ast.FunctionDef)
    }

    print(json.dumps({
        "status": "PASS_STATIC_AST_ONLY",
        "verification_level": "STATIC_CHECKED",
        "evaluation_level": "NOT_RUN",
        "game_episode_calls": 0,
        "model_inference_calls": 0,
        "game_modules_imported_by_checker": 0,
        "checked_source_files": hashes,
        "checked_contracts": [
            "immutable observation and decision data classes present",
            "reset/observe/legal_actions/step port surface present",
            "concrete VeiledDuel adapter has required methods",
            "runner contains admission and settlement guard functions",
            "external JSONL decision source with no provider dependency",
            "entrypoint source present but not invoked",
        ],
        "limitations": "AST checks cannot establish gameplay or runtime correctness",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
