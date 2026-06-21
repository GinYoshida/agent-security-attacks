from aicomp_sdk.attacks.contracts import AttackRunConfig
from aicomp_sdk.core.predicates import eval_predicates
from src.local.env_factory import build_env
from src.engine.archive import ArchiveStore
from src.engine.selector import CellSelector
from src.engine.replay import ReplayVerifier
from src.recipes.policy import ActionPolicy
from src.engine.search import SearchEngine


def test_engine_finds_verified_exfiltration_under_optimal_mock():
    env = build_env(guardrail="optimal", agent="mock", seed=1)
    eng = SearchEngine(CellSelector(), ActionPolicy(), ArchiveStore(), ReplayVerifier(), branch_batch=8)
    findings = eng.run(env, AttackRunConfig(time_budget_s=5.0))
    assert len(findings) >= 1
    # every finding reproduces a predicate from scratch
    for c in findings:
        env.reset()
        for m in c.user_messages:
            env.interact(m, max_tool_hops=8)
        assert eval_predicates(env.export_trace_dict())
