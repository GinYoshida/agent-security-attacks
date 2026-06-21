from src.engine.archive import Exemplar, ArchiveStore

def _ex(h, score=0.0):
    return Exemplar(snapshot={}, user_messages=[h], cell_hash=h, score_hint=score)

def test_add_and_contains():
    a = ArchiveStore(max_cells=10)
    a.add(_ex("h1", 1.0))
    assert "h1" in a and a["h1"].score_hint == 1.0 and len(a) == 1

def test_eviction_drops_lowest_score():
    a = ArchiveStore(max_cells=2)
    a.add(_ex("low", 1.0)); a.add(_ex("mid", 5.0)); a.add(_ex("high", 9.0))
    assert len(a) == 2 and "low" not in a and "high" in a
