"""Quick symbolic checks behind the proof packages (the full list and status is claude/verification_results.md)."""
import subprocess
import sys
from pathlib import Path

import pytest

V = Path(__file__).resolve().parents[1] / "code" / "verification"
QUICK = ["s10col_sym.py", "opf5c_gd.py", "s8_galois.py", "c12_counterexample.py",
         "s10a_q6.py", "s8_osc.py", "p1_checks.py", "s8_carleman.py"]


@pytest.mark.parametrize("script", QUICK)
def test_check_runs_clean(script):
    p = V / script
    r = subprocess.run([sys.executable, "-I", p.name], cwd=p.parent, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-800:]
