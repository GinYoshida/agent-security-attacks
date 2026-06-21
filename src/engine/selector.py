from __future__ import annotations
import math
import random
from src.engine.archive import ArchiveStore, Exemplar

class CellSelector:
    def __init__(self, exploration: float = 1.4) -> None:
        self.exploration = exploration

    def select(self, archive: ArchiveStore, rng: random.Random) -> Exemplar:
        cells = archive.values()
        total_visits = sum(e.visits for e in cells)
        best: Exemplar | None = None
        best_score = -1.0
        for e in sorted(cells, key=lambda x: x.cell_hash):
            mean_win = e.wins / (e.visits + 1)
            explore = self.exploration * math.sqrt(math.log(total_visits + 1) / (e.visits + 1))
            score = mean_win + explore + 0.01 * e.score_hint + rng.uniform(0, 1e-6)
            if score > best_score:
                best_score, best = score, e
        assert best is not None
        return best
