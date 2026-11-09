"""Helper comune per gli script PR-C2b (nessuna dipendenza esterna oltre sympy)."""
import sympy as sp

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
RESULTS = []


def check(name, expr, simp=True):
    """PASS se expr si semplifica a 0."""
    e = sp.simplify(expr) if simp else expr
    if e != 0:
        e2 = sp.simplify(sp.expand(sp.powsimp(sp.expand_func(e), force=True)))
        e = e2
    ok = (e == 0)
    RESULTS.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "   residuo: " + str(e)))
    return ok


def check_true(name, cond, info=""):
    ok = bool(cond)
    RESULTS.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name + (("   " + info) if info else ""))
    return ok


def summary(tag):
    n = len(RESULTS)
    k = sum(1 for _, ok in RESULTS if ok)
    print(f"== {tag}: {k}/{n} PASS")


def quotient_dim(polys, gens):
    """dim_C C[gens]/(polys) (None se infinita) via base di Groebner grevlex."""
    G = sp.groebner(polys, *gens, order='grevlex')
    if list(G.exprs) == [1]:
        return 0
    lead = [sp.Poly(g, *gens).monoms(order='grevlex')[0] for g in G.exprs]
    # per dimensione zero ogni variabile deve avere una potenza pura come leading monomial
    bounds = []
    for i in range(len(gens)):
        pure = [m[i] for m in lead if all(m[j] == 0 for j in range(len(gens)) if j != i)]
        if not pure:
            return None
        bounds.append(min(pure))
    import itertools
    cnt = 0
    for mono in itertools.product(*[range(b) for b in bounds]):
        if not any(all(mono[j] >= m[j] for j in range(len(gens))) for m in lead):
            cnt += 1
    return cnt
