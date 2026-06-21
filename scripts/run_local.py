from __future__ import annotations
import argparse
from aicomp_sdk.attacks.contracts import AttackRunConfig
from aicomp_sdk.core.predicates import eval_predicates
from aicomp_sdk.scoring import score_attack
from src.local.env_factory import build_env
from attack_src import AttackAlgorithm

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--guardrail", default="optimal")
    ap.add_argument("--agent", default="mock")
    ap.add_argument("--budget-s", type=float, default=10.0)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    env = build_env(guardrail=a.guardrail, agent=a.agent, seed=a.seed)
    findings = AttackAlgorithm().run(env, AttackRunConfig(time_budget_s=a.budget_s))
    rows = []
    for c in findings:
        env.reset()
        for m in c.user_messages:
            env.interact(m, max_tool_hops=8)
        tr = env.export_trace_dict()
        rows.append({"predicates": eval_predicates(tr)})
    print("findings:", len(findings), "est_score:", score_attack(rows))

if __name__ == "__main__":
    main()
