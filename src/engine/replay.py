from __future__ import annotations
from aicomp_sdk.attacks.contracts import AttackCandidate
from aicomp_sdk.core.predicates import eval_predicates

class ReplayVerifier:
    def verify(self, env, candidate: AttackCandidate, max_tool_hops: int = 8) -> bool:
        snap = env.snapshot()
        try:
            env.reset()
            for msg in candidate.user_messages:
                env.interact(msg, max_tool_hops=max_tool_hops)
            preds = eval_predicates(env.export_trace_dict())
            return bool(preds)
        finally:
            env.restore(snap)
