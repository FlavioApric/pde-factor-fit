"""The four worked examples of the model-expansion paper must pass all their checks."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

EX = Path(__file__).resolve().parents[1] / "code"
EXPECTED = {"ex_L6_dirac.py": 7, "ex_L7_poschl_teller.py": 11, "ex_L8_stark.py": 5, "ex_L9_L10_dict.py": 12}


@pytest.mark.parametrize("script,n", sorted(EXPECTED.items()))
def test_example_passes(script, n):
    out = subprocess.run([sys.executable, "-I", script], cwd=EX, capture_output=True, text=True, timeout=600).stdout
    m = re.search(r"(\d+)/(\d+) PASS", out)
    assert m, out[-500:]
    assert int(m.group(1)) == int(m.group(2)) == n
