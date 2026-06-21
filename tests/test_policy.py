import random
from src.engine.archive import Exemplar
from src.recipes.policy import ActionPolicy
from src.recipes.evasion import is_keyword_clean

def _ex():
    return Exemplar(snapshot={}, user_messages=["seed"], cell_hash="h")

def test_propose_is_bounded_and_clean():
    p = ActionPolicy()
    for i in range(200):
        msg = p.propose(_ex(), random.Random(i))
        assert len(msg) <= 2000
        if "http.post" in msg:
            assert is_keyword_clean(msg)

def test_exfil_urls_vary():
    p = ActionPolicy()
    msgs = {p.propose(_ex(), random.Random(i)) for i in range(300)}
    exfil = {m for m in msgs if "http.post" in m}
    assert len(exfil) >= 20  # arg variation mints distinct directives
