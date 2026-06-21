from __future__ import annotations
import random
from src.recipes.nl_policy import NLActionPolicy
from src.engine.archive import Exemplar

def _dummy_exemplar() -> Exemplar:
    return Exemplar(snapshot={}, user_messages=[], cell_hash="x")

def test_messages_non_empty_and_within_length():
    policy = NLActionPolicy()
    exemplar = _dummy_exemplar()
    for seed in range(200):
        rng = random.Random(seed)
        msg = policy.propose(exemplar, rng)
        assert isinstance(msg, str)
        assert len(msg) > 0, f"Empty message at seed {seed}"
        assert len(msg) <= 2000, f"Message too long at seed {seed}: {len(msg)}"

def test_url_variance_over_seeds():
    policy = NLActionPolicy()
    exemplar = _dummy_exemplar()
    messages = set()
    for seed in range(300):
        rng = random.Random(seed)
        msg = policy.propose(exemplar, rng)
        messages.add(msg)
    assert len(messages) >= 20, f"Too few distinct messages: {len(messages)}"
