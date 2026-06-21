from __future__ import annotations
import os
from collections.abc import Callable
from pathlib import Path

from aicomp_sdk.core.env.sandbox import SandboxEnv
from aicomp_sdk.agents.deterministic_agent import VulnerableDeterministicAgent
from aicomp_sdk.guardrails.optimal import Guardrail as OptimalGuardrail
from aicomp_sdk.attacks.baselines.guardrail_allow import Guardrail as AllowGuardrail
from src.local.mock_agent import SteerableMockAgent

def _fixtures_dir() -> Path:
    override = os.environ.get("AICOMP_FIXTURES")
    if override:
        return Path(override)
    return Path("vendor/aicomp_pkg/aicomp_sdk/fixtures")

def _build_agent(agent: str):
    if agent == "deterministic":
        return VulnerableDeterministicAgent()
    if agent == "mock":
        return SteerableMockAgent()
    raise ValueError(f"unknown agent: {agent}")

def _build_guardrail(guardrail: str):
    if guardrail == "optimal":
        return OptimalGuardrail()
    if guardrail == "allow":
        return AllowGuardrail()
    raise ValueError(f"unknown guardrail: {guardrail}")

def build_env(*, guardrail: str = "optimal", agent: str = "deterministic", seed: int = 0) -> SandboxEnv:
    return SandboxEnv(
        seed=seed,
        fixtures_dir=_fixtures_dir(),
        agent=_build_agent(agent),
        guardrail=_build_guardrail(guardrail),
    )

def make_env_factory(**kwargs) -> Callable[[], SandboxEnv]:
    return lambda: build_env(**kwargs)
