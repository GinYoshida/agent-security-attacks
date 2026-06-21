from __future__ import annotations
import random
from aicomp_sdk.attacks.contracts import AttackCandidate, AttackRunConfig
from aicomp_sdk.core.cells import cell_signature
from aicomp_sdk.core.env.api import AttackEnvProtocol
from aicomp_sdk.core.predicates import eval_predicates
from aicomp_sdk.utils.timebox import Timebox
from src.engine.archive import ArchiveStore, Exemplar
from src.engine.selector import CellSelector
from src.engine.replay import ReplayVerifier
from src.recipes.policy import ActionPolicy


class SearchEngine:
    def __init__(self, selector: CellSelector, policy: ActionPolicy,
                 archive: ArchiveStore, verifier: ReplayVerifier,
                 branch_batch: int = 12) -> None:
        self.selector = selector
        self.policy = policy
        self.archive = archive
        self.verifier = verifier
        self.branch_batch = branch_batch

    def _sig(self, tr: dict) -> str:
        return str(cell_signature(
            tr["tool_events"],
            egress_data=tr.get("egress", []),
            user_messages=tr.get("user_messages", []),
        )["hash"])

    def run(self, env: AttackEnvProtocol, config: AttackRunConfig) -> list[AttackCandidate]:
        rng = random.Random(env.seed)
        tb = Timebox(float(config.time_budget_s))

        # Seed: reset env (zero tool events, untainted) to avoid OptimalGuardrail
        # blocking exfil branches due to web/email taint in last 5 tool-event sources.
        env.reset()
        seed_tr = env.export_trace_dict()
        self.archive.add(Exemplar(
            env.snapshot(),
            list(seed_tr["user_messages"]),
            self._sig(seed_tr),
            depth=1,
        ))

        raw_findings: dict[str, AttackCandidate] = {}

        while not tb.expired() and len(self.archive) > 0:
            ex = self.selector.select(self.archive, rng)
            ex.visits += 1

            for _ in range(self.branch_batch):
                if tb.expired():
                    break
                env.restore(ex.snapshot)
                action = self.policy.propose(ex, rng)
                res = env.interact(action, max_tool_hops=config.max_tool_hops)
                if res.agent_refused:
                    continue
                tr = env.export_trace_dict()
                h = self._sig(tr)
                preds = eval_predicates(tr)
                if h not in self.archive:
                    self.archive.add(Exemplar(
                        env.snapshot(),
                        list(tr["user_messages"]),
                        h,
                        score_hint=float(len(preds)),
                        depth=ex.depth + 1,
                    ))
                if preds:
                    ex.wins += 1
                    raw_findings[h] = AttackCandidate.from_messages(list(tr["user_messages"]))

        verified: list[AttackCandidate] = []
        for cand in raw_findings.values():
            if self.verifier.verify(env, cand, max_tool_hops=config.max_tool_hops):
                verified.append(cand)
        return verified
