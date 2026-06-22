from aicomp_sdk.attacks.contracts import AttackAlgorithmBase, AttackRunConfig
from src.local.env_factory import build_env
from attack_src import AttackAlgorithm

def test_adapter_is_contract_compliant_and_finds_under_mock():
    assert issubclass(AttackAlgorithm, AttackAlgorithmBase)
    env = build_env(guardrail="optimal", agent="mock", seed=1)
    findings = AttackAlgorithm({"branch_batch": 8, "policy": "mock"}).run(env, AttackRunConfig(time_budget_s=5.0))
    assert isinstance(findings, list) and len(findings) >= 1
