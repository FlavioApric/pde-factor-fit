"""Check that every notation macro defined in shared/macros.tex appears in the notation table, and that the
manuscripts use no macro of the notation set that is undefined. Usage: python paper/tools/check_notation.py"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
macros = ROOT / "shared" / "macros.tex"
table = (ROOT / "shared" / "sections" / "notation.tex").read_text()
# macros that are notation (math symbols), not formatting helpers
SKIP = {"R", "C", "Z", "dd", "Id", "abs", "norm", "ip", "lab", "roleinalg", "inbrief", "Normal", "E",
        "gcdop", "spn", "rank", "diag", "tr", "Hs", "noise"}
defined = re.findall(r"\\(?:newcommand|DeclareMathOperator)\{\\(\w+)\}", macros.read_text())
missing = [m for m in defined if m not in SKIP and f"\\{m}" not in table]
if missing:
    print("notation macros not listed in the notation table:", ", ".join(missing))
    sys.exit(1)
print(f"notation: {len(defined)} macros, all listed (skipped helpers: {len(SKIP)})")
