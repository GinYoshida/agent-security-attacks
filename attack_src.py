"""Competition attack adapter (Go-Explore engine).

CALIBRATION-PHASE SCAFFOLD — NOT a scoring submission yet.
The active policy is the mock-only ActionPolicy, whose `CALL <tool> ...`
directives only steer the local SteerableMockAgent. Against the real
gpt-oss-20b agent these emit no tool calls, so the evaluator discards every
finding (score ~0). This bundle validates the engine/replay/harness only.
To make a scoring submission: wire NLActionPolicy (src/recipes/nl_policy.py)
into the engine and calibrate it against the real agent via Kaggle.
"""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
from aicomp_sdk.attacks.contracts import AttackAlgorithmBase, AttackCandidate, AttackRunConfig
from aicomp_sdk.core.env.api import AttackEnvProtocol
from src.engine.archive import ArchiveStore
from src.engine.selector import CellSelector
from src.engine.replay import ReplayVerifier
from src.engine.search import SearchEngine
from src.recipes.policy import ActionPolicy

class AttackAlgorithm(AttackAlgorithmBase):
    def __init__(self, config: Mapping[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, env: AttackEnvProtocol, config: AttackRunConfig) -> list[AttackCandidate]:
        bb = int(self.config.get("branch_batch", 12))
        max_cells = int(self.config.get("max_cells", 5000))
        engine = SearchEngine(CellSelector(), ActionPolicy(), ArchiveStore(max_cells),
                              ReplayVerifier(), branch_batch=bb)
        return engine.run(env, config)
