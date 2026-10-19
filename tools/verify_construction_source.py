#!/usr/bin/env python3
"""Read-only construction verification. Never imports or executes game_harness.

Run from a checkout of the experiment:
    python3 tools/verify_construction_source.py

Only source parsing, byte-level receipts, immutable Git ancestry and evidence
manifests are checked. No game episode, model inference or runtime test occurs.
"""

from __future__ import annotations

import ast
import gzip
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "game_harness"
DISCOVERY = ROOT / "receipts" / "discovery"
INDEX_SHA = "b48b13e74d6938f833094d3f9afc1a11e61a8515"
ANCHORS = (
    ("C1", "b3345272ee01c89bf2dc86870d35602b1e3894c8"),
    ("C2", "d6c757f701501f1f555c009d5163c6852e33e33f"),
    ("C3_COMPARISON", "f3f948aa2057644e6c64c5b6a0f34f1658f3b3b0"),
    ("C3_DECISION", "cb33282d1cb5454841f87dd486df86da60cae787"),
    ("C4_FIRST_IMPLEMENTATION", "ee8da1ca036ab4d853c134180b0b6f1716e9e346"),
)
FROZEN_QUERIES = (
    "game environment observation action feedback",
    "partial observability state observation belief",
    "sequential decisions multi step agent tasks",
    "long horizon planning memory game",
    "environment feedback retries recovery",
    "tool action execution safety validation",
    "agent state persistence context across steps",
    "chlorophyll photosynthesis tectonic plates",
)
RUNTIME_FILES = (
    "__init__.py",
    "__main__.py",
    "contracts.py",
    "veiled_duel.py",
    "runner.py",
    "policy_jsonl.py",
)
REQUIRED_CLASSES = {
    "contracts.py": {
        "Observation": (),
        "LegalActionSet": ("contains",),
        "DecisionInput": (),
        "ActionIdentity": (),
        "TransitionReceipt": (),
        "DecisionSource": ("decide",),
        "EnvironmentPort": ("reset", "observe", "legal_actions", "dispatch_action", "step"),
    },
    "veiled_duel.py": {
        "VeiledDuel": ("reset", "observe", "legal_actions", "dispatch_action", "step"),
    },
    "runner.py": {
        "EpisodeRunner": ("run",),
        "HarnessProtocolError": (),
    },
    "policy_jsonl.py": {"JSONLinesDecisionSource": ("decide",)},
}
ALLOWED_RUNTIME_IMPORT_ROOTS = {
    "__future__", "argparse", "dataclasses", "json", "random", "sys", "typing",
}


def require(condition: bool, description: str) -> None:
    if not condition:
        raise AssertionError(description)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_source() -> dict[str, ast.AST]:
    trees = {}
    for name in RUNTIME_FILES:
        path = SOURCE_DIR / name
        require(path.is_file(), f"Missing code artifact: {name}")
        original = path.read_text(encoding="utf-8")
        tree = ast.parse(original, filename=str(path))
        # Compile syntax without executing/importing any function or module.
        compile(tree, str(path), "exec", dont_inherit=True)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    require(alias.name.partition(".")[0] in ALLOWED_RUNTIME_IMPORT_ROOTS,
                            f"Unreviewed runtime dependency: {name}: {alias.name}")
            if isinstance(node, ast.ImportFrom) and node.level == 0:
                require(
                    (node.module or "").partition(".")[0] in ALLOWED_RUNTIME_IMPORT_ROOTS,
                    f"Unreviewed runtime dependency: {name}: {node.module}",
                )
        trees[name] = tree
        print(f"STATIC_SOURCE_OK {name}")
    for filename, definitions in REQUIRED_CLASSES.items():
        declared = {
            node.name: node for node in trees[filename].body
            if isinstance(node, ast.ClassDef)
        }
        for cls, methods in definitions.items():
            require(cls in declared, f"Missing class {filename}::{cls}")
            declared_methods = {
                node.name for node in declared[cls].body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            require(set(methods) <= declared_methods, f"Missing methods {filename}::{cls}")
    return trees


def verify_provenance() -> None:
    source_validation = read_json(ROOT / "receipts" / "preflight" / "source-validation.json")
    require(source_validation["source_pin"] == INDEX_SHA, "C1 Index SHA mismatch")
    require(
        (source_validation["accepted"], source_validation["excluded"],
         source_validation["proposed"]) == (581, 48, 14),
        "Canonical admission differs from recorded source preflight",
    )
    imported = read_json(DISCOVERY / "connector-import-native.json")
    audit = read_json(DISCOVERY / "independent-audit.json")["result"]
    manifest = read_json(DISCOVERY / "pinned-source-manifest.json")
    require(imported["status"] == "PASS_FRESH_LOCAL_COGNEE_IMPORT", "Cognee import not PASS")
    require(imported["index_commit"] == INDEX_SHA, "Imported source differs from C1")
    for key, wanted in (
        ("documents", 581), ("graph_nodes", 12161), ("graph_edges", 8094),
        ("graded_facts", 3486),
    ):
        require(imported[key] == wanted, f"Native import {key} mismatched")
    require(audit["status"] == "PASS" and audit["states_exact"] and audit["source_refs_exact"],
            "Independent audit not PASS")
    require(audit["index_commit"] == INDEX_SHA, "Audit source differs from C1")
    require(all(audit[k] == imported[k] for k in ("documents", "graph_nodes", "graph_edges")),
            "Audit and import disagree")
    require(audit["exact_grades"] == imported["graded_facts"], "VSM grades differ")
    require(manifest["count"] == 581 and manifest["index_commit"] == INDEX_SHA,
            "Source manifest not full included corpus")
    ids = {
        "opensiro/vsm-harness-index:" + item["harness_id"]
        for item in manifest["assessments"]
    }
    require(len(ids) == 581, "Duplicate/noncanonical included source manifest IDs")
    require(set(audit["all_validated_sources"]) ==
            {item["harness_id"] for item in manifest["assessments"]},
            "Audit IDs do not match full source manifest")

    original = gzip.decompress((DISCOVERY / "connector-import-original.log.gz").read_bytes())
    logged_sha = (DISCOVERY / "connector-import-log-sha256.txt").read_text().split()[0]
    require(hashlib.sha256(original).hexdigest() == logged_sha,
            "Compressed original connector log is not byte-preserved")
    require(b"PASS_FRESH_LOCAL_COGNEE_IMPORT" in original,
            "Original connector log lacks native PASS")
    manifest_queries = read_json(DISCOVERY / "native-search-manifest.json")["queries"]
    require(len(manifest_queries) == 8, "Missing original native query receipts")
    for i, expected in enumerate(FROZEN_QUERIES, 1):
        receipt_path = DISCOVERY / f"native-search-Q{i:02d}.json"
        doc = read_json(receipt_path)
        require(doc["query_id"] == f"Q{i:02d}" and doc["query_text"] == expected,
                f"Q{i:02d}: first-pass query differs from C1")
        require(doc["index_commit"] == INDEX_SHA and doc["search_type"] ==
                "SearchType.CHUNKS_LEXICAL" and doc["top_k"] == 15,
                f"Q{i:02d}: native retrieval contract changed")
        require(doc["negative_control"] == (i == 8),
                f"Q{i:02d}: control label changed")
        responses = doc["unfiltered_native_response"]
        require(len(responses) == 1, "Unexpected number of returned dataset result groups")
        hits = responses[0]["search_result"]
        require(len(hits) == 15, f"Q{i:02d}: recorded hit count differs")
        require(all(hit.get("document_id") in ids for hit in hits),
                f"Q{i:02d}: non-admitted result hit")
        require(
            manifest_queries[i - 1]["query_id"] == doc["query_id"],
            f"Q{i:02d}: native manifest order mismatch",
        )
        print(f"NATIVE_RECEIPT_OK Q{i:02d} hits={len(hits)}")
    print("PROVENANCE_STATIC_OK included=581 chunks=3486 native_queries=8")


def verify_order() -> None:
    for (left, parent), (right, child) in zip(ANCHORS, ANCHORS[1:]):
        result = subprocess.run(
            ("git", "merge-base", "--is-ancestor", parent, child),
            cwd=ROOT, check=False, capture_output=True,
        )
        require(result.returncode == 0, f"Commit ancestry failed: {left} -> {right}")
        print(f"CHRONOLOGY_OK {left} -> {right}")
    current = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT,
        check=True, text=True, capture_output=True,
    ).stdout.strip()
    final = subprocess.run(
        ("git", "merge-base", "--is-ancestor", ANCHORS[-1][1], current),
        cwd=ROOT, check=False,
    )
    require(final.returncode == 0, "Implementation commit is not an ancestor of HEAD")


def main() -> None:
    parse_source()
    verify_provenance()
    verify_order()
    print("STATIC_CHECKED: source/evidence/chronology only; GAMEPLAY NOT_RUN")


if __name__ == "__main__":
    main()
