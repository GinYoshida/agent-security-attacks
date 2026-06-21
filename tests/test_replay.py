from aicomp_sdk.attacks.contracts import AttackCandidate
from src.local.env_factory import build_env
from src.recipes.evasion import clean_exfil_message
from src.engine.replay import ReplayVerifier

def test_verifier_accepts_reproducing_candidate():
    env = build_env(guardrail="optimal", agent="mock", seed=1)
    env.reset()
    v = ReplayVerifier()
    assert v.verify(env, AttackCandidate.from_messages([clean_exfil_message()])) is True

def test_verifier_rejects_nonfiring_candidate():
    env = build_env(guardrail="optimal", agent="mock", seed=1)
    env.reset()
    v = ReplayVerifier()
    assert v.verify(env, AttackCandidate.from_messages(["CALL web.search query=hello"])) is False
