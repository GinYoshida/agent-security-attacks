"""Competition attack adapter (Go-Explore engine).

Policy selection via config["policy"]:
  - "nl"   (default): NLActionPolicy emits natural-language exfil instructions
           for the real gpt-oss-20b agent. This is the scoring submission path,
           still pending real-agent calibration on Kaggle.
  - "mock": ActionPolicy emits `CALL <tool> ...` directives that steer the
           local SteerableMockAgent only (used by the local test harness).
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
from src.recipes.nl_policy import NLActionPolicy

_POLICIES = {"nl": NLActionPolicy, "mock": ActionPolicy}

class AttackAlgorithm(AttackAlgorithmBase):
    def __init__(self, config: Mapping[str, Any] | None = None) -> None:
        super().__init__(config)

    def run(self, env: AttackEnvProtocol, config: AttackRunConfig) -> list[AttackCandidate]:
        bb = int(self.config.get("branch_batch", 12))
        max_cells = int(self.config.get("max_cells", 5000))
        policy_name = str(self.config.get("policy", "nl"))
        policy = _POLICIES[policy_name]()
        engine = SearchEngine(CellSelector(), policy, ArchiveStore(max_cells),
                              ReplayVerifier(), branch_batch=bb)
        return engine.run(env, config)
