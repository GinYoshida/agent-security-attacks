from __future__ import annotations
import re
from pathlib import Path

MODULES = [
    "src/engine/archive.py", "src/engine/selector.py", "src/engine/replay.py",
    "src/recipes/evasion.py", "src/recipes/policy.py", "src/recipes/nl_policy.py",
    "src/engine/search.py", "attack_src.py",
]
_LOCAL_IMPORT = re.compile(r"^(from|import)\s+(src|attack_src)\b.*$", re.M)
_FUTURE_IMPORT = re.compile(r"^from __future__ import .*$", re.M)

def main() -> None:
    parts = []
    for m in MODULES:
        text = Path(m).read_text()
        text = _LOCAL_IMPORT.sub("", text)
        text = _FUTURE_IMPORT.sub("", text)
        parts.append(f"# --- {m} ---\n{text}\n")
    out = ("from __future__ import annotations\n"
           "# AUTO-GENERATED. Edit src/ then run scripts/build_attack.py.\n\n"
           + "\n".join(parts))
    Path("attack.py").write_text(out)
    print("wrote attack.py")

if __name__ == "__main__":
    main()
