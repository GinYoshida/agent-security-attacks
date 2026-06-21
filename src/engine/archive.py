from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Exemplar:
    snapshot: dict[str, Any]
    user_messages: list[str]
    cell_hash: str
    score_hint: float = 0.0
    visits: int = 0
    depth: int = 0
    wins: int = 0

class ArchiveStore:
    def __init__(self, max_cells: int = 5000) -> None:
        self.max_cells = max_cells
        self._cells: dict[str, Exemplar] = {}

    def add(self, ex: Exemplar) -> None:
        self._cells[ex.cell_hash] = ex
        if len(self._cells) > self.max_cells:
            victim = min(self._cells.values(), key=lambda e: e.score_hint)
            del self._cells[victim.cell_hash]

    def __contains__(self, h: str) -> bool:
        return h in self._cells

    def __getitem__(self, h: str) -> Exemplar:
        return self._cells[h]

    def values(self) -> list[Exemplar]:
        return list(self._cells.values())

    def __len__(self) -> int:
        return len(self._cells)
