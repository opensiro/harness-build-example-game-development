"""Original Veiled Duel agent harness, built from recorded Cognee-first research.

Runtime is NOT_RUN and no gameplay/model quality is evaluated in this study.
"""

from .contracts import (
    ActionIdentity,
    DecisionInput,
    DecisionSource,
    EnvironmentPort,
    LegalActionSet,
    Observation,
    TransitionReceipt,
)
from .policy_jsonl import JSONLinesDecisionSource
from .runner import EpisodeRunner, HarnessProtocolError, RunReport, StepRecord
from .veiled_duel import VeiledDuel

__all__ = [
    "ActionIdentity",
    "DecisionInput",
    "DecisionSource",
    "EnvironmentPort",
    "LegalActionSet",
    "Observation",
    "TransitionReceipt",
    "JSONLinesDecisionSource",
    "EpisodeRunner",
    "HarnessProtocolError",
    "RunReport",
    "StepRecord",
    "VeiledDuel",
]
