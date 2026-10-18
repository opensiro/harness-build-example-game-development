#!/usr/bin/env python3
"""C2-only, pinned-connector independent audit and native Cognee lexical retrieval.

No game/model runtime operations. Invoke only after the original connector import.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

INDEX_SHA = "b48b13e74d6938f833094d3f9afc1a11e61a8515"
DATASET = "game-cognee-b3345272-full-01"
TAG = "opensiro_vsm_canonical_example"
QUERIES = [
    ("Q01", "game environment observation action feedback"),
    ("Q02", "partial observability state observation belief"),
    ("Q03", "sequential decisions multi step agent tasks"),
    ("Q04", "long horizon planning memory game"),
    ("Q05", "environment feedback retries recovery"),
    ("Q06", "tool action execution safety validation"),
    ("Q07", "agent state persistence context across steps"),
    ("Q08", "chlorophyll photosynthesis tectonic plates"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def configure(root: Path) -> None:
    store = root / "fresh-store-01"
    os.environ.update(
        SYSTEM_ROOT_DIRECTORY=str(store / "system"),
        DATA_ROOT_DIRECTORY=str(store / "data"),
        DLT_DATA_DIR=str(store / "dlt"),
        PIPELINES_DIR=str(store / "dlt" / "pipelines"),
        COGNEE_SKIP_CONNECTION_TEST="true",
        TELEMETRY_DISABLED="1",
    )


def raw_as_json(obj):
    """Preserve all native response fields without relevance filtering."""
    if hasattr(obj, "model_dump"):
        return raw_as_json(obj.model_dump(mode="json"))
    if isinstance(obj, dict):
        return {str(k): raw_as_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [raw_as_json(v) for v in obj]
    if isinstance(obj, (int, float, bool, str)) or obj is None:
        return obj
    if hasattr(obj, "__dict__"):
        return {"__native_type__": type(obj).__name__, **raw_as_json(vars(obj))}
    return {"__native_type__": type(obj).__name__, "__repr__": repr(obj)}


async def audit(root: Path):
    from cognee_community_connector_opensiro_vsm.source import read_snapshot
    from cognee_community_connector_opensiro_vsm.audit import audit_dataset

    snap = read_snapshot(root / "index", INDEX_SHA)
    result = await audit_dataset(
        snap, tuple(sorted(snap.accepted)), DATASET, TAG, lexical=True
    )
    assert result["status"] == "PASS"
    target = root / "receipts" / "independent-audit.json"
    target.write_text(json.dumps({
        "recorded_at_utc": utc_now(),
        "method": "pinned OpenSiro connector audit_dataset in distinct process",
        "connector_sha": "d176484e85da55c84450d67040cb4a2d096353c7",
        "connector_local_patch_sha256": "5be20dfacb2f8d48608b2aa4b9d4fbc6a43050e1f799678e8770ecb48a00b070",
        "result": result,
    }, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "graph_nodes": result["graph_nodes"],
                      "graph_edges": result["graph_edges"], "documents": result["documents"],
                      "grades": result["exact_grades"]}), flush=True)


async def search(root: Path):
    from cognee.modules.search.types import SearchType
    import cognee

    audit_doc = json.loads((root / "receipts" / "independent-audit.json").read_text())
    if audit_doc["result"]["status"] != "PASS" or audit_doc["result"]["dataset"] != DATASET:
        raise RuntimeError("Independent audit receipt is not PASS for this dataset")
    items = []
    for query_id, q in QUERIES:
        started = utc_now()
        response = await cognee.search(
            query_text=q, query_type=SearchType.CHUNKS_LEXICAL,
            datasets=[DATASET], top_k=15,
        )
        original = raw_as_json(response)
        document = {
            "query_id": query_id,
            "query_text": q,
            "started_at_utc": started,
            "finished_at_utc": utc_now(),
            "connector_sha": "d176484e85da55c84450d67040cb4a2d096353c7",
            "dataset": DATASET,
            "index_commit": INDEX_SHA,
            "native_api": "cognee.search",
            "search_type": "SearchType.CHUNKS_LEXICAL",
            "top_k": 15,
            "indexed_scope": "six S1-S5 markdown function sections per included assessment, not full body",
            "unfiltered_native_response": original,
            "negative_control": query_id == "Q08",
        }
        target = root / "receipts" / ("native-search-" + query_id + ".json")
        target.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
        items.append({"query_id": query_id, "query": q, "path": target.name, "bytes": target.stat().st_size})
        print(json.dumps({"query_id": query_id, "receipt_bytes": target.stat().st_size}), flush=True)
    (root / "receipts" / "native-search-manifest.json").write_text(
        json.dumps({"recorded_at_utc": utc_now(), "dataset": DATASET,
                    "queries": items, "mode": "CHUNKS_LEXICAL", "scope": "six function sections"}, indent=2) + "\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("audit", "search"))
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    configure(root)
    asyncio.run(audit(root) if args.stage == "audit" else search(root))


if __name__ == "__main__":
    main()
