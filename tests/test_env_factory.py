from src.local.env_factory import build_env, make_env_factory

def test_build_optimal_deterministic_env_runs():
    env = build_env(guardrail="optimal", agent="deterministic", seed=1)
    env.reset()
    env.interact("open page_2", max_tool_hops=4)
    tr = env.export_trace_dict()
    assert set(["seed", "user_messages", "tool_events", "egress"]).issubset(tr.keys())
    assert tr["user_messages"][-1] == "open page_2"

def test_make_env_factory_returns_fresh_envs():
    f = make_env_factory(guardrail="allow", agent="mock", seed=3)
    a, b = f(), f()
    assert a is not b
