from __future__ import annotations
import argparse
from collections import Counter
from aicomp_sdk.attacks.contracts import AttackRunConfig
from aicomp_sdk.core.predicates import eval_predicates
from aicomp_sdk.core.cells import cell_signature
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
    unique_hashes = set()
    pred_counter = Counter()
    for c in findings:
        env.reset()
        for m in c.user_messages:
            env.interact(m, max_tool_hops=8)
        tr = env.export_trace_dict()
        predicates = eval_predicates(tr)
        rows.append({"predicates": predicates})
        # Collect unique cell hash
        cell_hash = cell_signature(tr["tool_events"], egress_data=tr.get("egress", []), user_messages=tr.get("user_messages", []))["hash"]
        unique_hashes.add(cell_hash)
        # Collect predicate breakdown
        for p in predicates:
            pred_counter[p["predicate"]] += 1
    print("findings:", len(findings))
    print("unique_cells:", len(unique_hashes))
    print("predicate_breakdown:", dict(pred_counter))
    print("est_score:", score_attack(rows))

if __name__ == "__main__":
    main()
