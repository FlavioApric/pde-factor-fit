"""End to end: GP samples of transport_plus_diffusion -> core v2 per sample -> factor-set posterior.
usage: e2e_tpd.py n noise [families] ; compares noise levels handed to the core."""
import sys, time, json, numpy as np
from pdefactor.synthetic import case, grid, sample_scattered
from pdefactor.interp import fit_gp, run_core_on_samples, factor_set_posterior
n, nz = int(sys.argv[1]), float(sys.argv[2])
fams = tuple(sys.argv[3].split(",")) if len(sys.argv) > 3 else ("matern52", "matern52e", "matern52e+matern52e")
f = case("transport_plus_diffusion"); tg, xg, u = grid(f)
t, x, y, s = sample_scattered(f, n, noise=nz, rng=1)
t0 = time.time(); p = fit_gp(t, x, y, grid=(tg, xg), S=16, families=fams); tgp = time.time() - t0
print("gp", round(tgp, 1), "s; cov", {k: round(v, 3) for k, v in p.coverage(u).items()}, "fam", {k: round(v, 3) for k, v in p.info["family_posterior"].items()})
import sympy as sp
from pdefactor.symbols import tau, xi
TRUE = [sp.Poly(tau + xi, tau, xi), sp.Poly(tau - sp.Rational(3, 10) * xi**2, tau, xi)]


def _close(fs, tol=0.05):
    """factor set == {tau + xi, tau - 0.3 xi^2} up to coefficient tolerance tol (max abs diff)."""
    try:
        P = [sp.Poly(sp.sympify(f, locals={"tau": tau, "xi": xi}), tau, xi) for f in fs]
    except Exception:
        return False
    if len(P) != 2:
        return False
    d = lambda a, b: max(abs(complex(c)) for c in (a - b).coeffs()) if (a - b).coeffs() else 0.0
    return any(d(P[0], A) < tol and d(P[1], B) < tol for A, B in [TRUE, TRUE[::-1]])


for lbl, sig in [("smooth", p.effective_noise()), ("white", p.effective_noise("white"))]:
    t0 = time.time(); res = run_core_on_samples(p.samples, tg, xg, sig, p.weights); tc = time.time() - t0
    hit = sum(w for r, w in res if r.label == "FIT-COMPATIBLE" and _close(sorted(next(iter(factor_set_posterior([(r, 1.0)])))[1])))
    rec = {"n": n, "noise": nz, "kind": lbl, "core_noise": sig, "P_true": hit, "coverage": p.coverage(u), "gp_time": tgp, "core_time": tc,
           "family_posterior": p.info["family_posterior"], "sets": [[v, k[0], sorted(k[1])] for k, v in factor_set_posterior(res).items()]}
    open("sessions/S-INTERP/out/e2e_tpd.jsonl", "a").write(json.dumps(rec) + chr(10))
    top = [r.structures[0][2] if r.structures else 0 for r, _ in res]
    print(f"{lbl:10s} noise={sig:.2e} P(true set)={hit:.3f} core {tc:.0f}s labels",
          {l: round(sum(w for r, w in res if r.label == l), 3) for l in {r.label for r, _ in res}}, "median p_top", round(float(np.median(top)), 3))
    for k, v in list(factor_set_posterior(res).items())[:3]:
        print("    ", round(v, 3), k[0], sorted(k[1]))
