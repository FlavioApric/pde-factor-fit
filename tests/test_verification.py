"""Quick symbolic checks behind the proof packages (the full list and status is verification/RESULTS.md)."""
import subprocess
import sys
from pathlib import Path

import pytest

V = Path(__file__).resolve().parents[1] / "verification"
QUICK = ["S10-COL/s10col_sym.py", "OP-F5C/opf5c_gd.py", "S8-VAR/s8_galois.py", "C1C2/c12_counterexample.py",
         "S10-OPEN-A/s10a_q6.py", "S8-VAR/s8_osc.py", "P1/p1_checks.py", "S8-VAR/s8_carleman.py"]


@pytest.mark.parametrize("script", QUICK)
def test_check_runs_clean(script):
    p = V / script
    r = subprocess.run([sys.executable, "-I", p.name], cwd=p.parent, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-800:]
