import random
from src.engine.archive import Exemplar, ArchiveStore
from src.engine.selector import CellSelector

def test_prefers_unvisited_winning_cell():
    a = ArchiveStore()
    a.add(Exemplar(snapshot={}, user_messages=["a"], cell_hash="a", visits=50, wins=0))
    a.add(Exemplar(snapshot={}, user_messages=["b"], cell_hash="b", visits=1, wins=1))
    sel = CellSelector()
    picks = [sel.select(a, random.Random(i)).cell_hash for i in range(20)]
    assert picks.count("b") > picks.count("a")
