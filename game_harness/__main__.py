"""Opt-in external policy entry point. Not executed during this experiment.

Invoking this module starts an episode and expects a separate policy/controller
process over JSON lines. For this reason do not run it as a construction check.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import sys

from .policy_jsonl import JSONLinesDecisionSource
from .runner import EpisodeRunner
from .veiled_duel import VeiledDuel


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Veiled Duel — external agent policy bridge")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--max-turns", type=int, default=12)
    parser.add_argument("--max-decisions", type=int, default=64)
    args = parser.parse_args(argv)

    environment = VeiledDuel(seed=args.seed, max_turns=args.max_turns)
    policy = JSONLinesDecisionSource(requests=sys.stdout, replies=sys.stdin)
    report = EpisodeRunner(
        environment, policy, max_decisions=args.max_decisions
    ).run()
    # stdout belongs exclusively to the JSON-lines decision protocol.
    print(json.dumps(asdict(report), sort_keys=True), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
