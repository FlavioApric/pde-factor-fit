"""benchmarks/final_report.py on a hand-built LoopResult (no run_loop: the test takes seconds)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from benchmarks.final_report import final_report, slices, symbol_of  # noqa: E402

from pdefactor.loop import FactorReport, Level, LoopResult  # noqa: E402
from pdefactor.symbols import tau, xi  # noqa: E402
from pdefactor.synthetic import case, grid  # noqa: E402


def _fr(coefs, W, kap):
    return FactorReport(sympy=sum(complex(c) * tau**a * xi**b for (a, b), c in coefs.items()), W=W,
                        coef={k: (complex(v), complex(v), complex(v)) for k, v in coefs.items()},
                        status="clean", kappa_support=list(kap))


def _result():
    kap = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    f1 = _fr({(1, 0): 1, (0, 1): 1.0}, 0.77, kap)  # transport tau + xi
    f2 = _fr({(1, 0): 1, (0, 2): -0.3}, 0.23, kap)  # diffusion tau - 0.3 xi^2
    return LoopResult(label="FIT-COMPATIBLE", factors=[f1, f2], p_k={2: 1.0}, structures={((1, 1), (1, 2)): 1.0},
                      history=[Level(bounds=(3, 4), p_fit=1.0, heldout=(0.9, 0.1))], regrouped=False,
                      bounds=(3, 4), labels={"FIT-COMPATIBLE": 1.0})


def test_final_report_sections_and_images(tmp_path):
    t, x, u = grid(case("transport_plus_diffusion"))
    R = final_report(_result(), samples=[u], t=t, x=x, sigma=0.0, truth=case("transport_plus_diffusion"),
                     out=tmp_path)
    J = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    for k in ("pde", "model", "factors", "fit", "friedrichs", "interaction", "parameters", "distances"):
        assert k in J
    assert J["pde"]["truth"]["factor_set_match"]
    assert "gamma_N_block_gram" in J["friedrichs"]
    assert any(k.startswith("loop.") for k in J["parameters"]["constants"])
    for f in R["images_files"]:
        assert (tmp_path / f).exists()
    md = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "law identified" not in md.lower()
    # the two u_j explain the data
    assert J["fit"]["joint_rel_residual"] < 1e-6


def test_symbol_image_dark_on_dispersion_curve():
    """Diffusion tau - 0.3 xi^2: kernel at tau = -0.3 kappa^2 (real), so the damping slice is ~zero there."""
    Q = symbol_of({(1, 0): (1, 1, 1), (0, 2): (-0.3, -0.3, -0.3)})
    K = np.linspace(-3, 3, 7)
    MU = np.concatenate([-0.3 * K**2, np.linspace(-3, 3, 9)])
    _, damp = slices(Q, K, np.sort(MU), np.linspace(-1, 1, 5))
    assert np.all(damp.min(axis=0) < -6)  # log10|Q| on the curve: numerically 0


def test_kernel_gap_is_a_distance():
    """Same operator -> gap 0; transport vs diffusion -> gap > 0."""
    from benchmarks.final_report import kernel_angles
    t, x, _ = grid(case("transport_plus_diffusion"))
    kap = np.array([-2.0, -1.0, 1.0, 2.0])
    A = symbol_of({(1, 0): (1, 1, 1), (0, 1): (1, 1, 1)})
    B = symbol_of({(1, 0): (1, 1, 1), (0, 2): (-0.3, -0.3, -0.3)})
    assert kernel_angles(A, A, kap, t, x)[1] < 1e-6
    assert kernel_angles(A, B, kap, t, x)[1] > 0.1
