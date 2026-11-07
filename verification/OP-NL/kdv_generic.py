"""OP-NL: generic (k symbolic) generator Pi(k;y) of the total family of KdV 2-solitons (PROOF_PACKAGE §3).
Search for weighted-homogeneous polynomials of weight W in (k1,k2; y0,y1,y2), wt k_i = 1, wt y_j = j+2,
vanishing at random points (k, X) mod p. Expect: none for W < 16, exactly one (up to scalar) for W = 16,
with coefficient of y0^8 a nonzero constant."""
import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modlin import P, rank_mod, weighted_monomials
from kdv_checks_lib import jet_point

random.seed(77)
ok = 0
tot = 0


def report(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info, flush=True)


N, K = 2, 2
wts = [1] * N + [j + 2 for j in range(K + 1)]
results = {}
for W in range(1, 17):
    monos = weighted_monomials(wts, W, exact=True)
    rows = []
    for _ in range(len(monos) + 40):
        while True:
            ks = [random.randrange(1, P) for _ in range(N)]
            if len(set(ks)) == N and (ks[0] + ks[1]) % P:
                break
        y = jet_point(ks, K)
        vals = list(ks) + y
        row = []
        for m in monos:
            v = 1
            for i, e in enumerate(m):
                if e:
                    v = v * pow(vals[i], e, P) % P
            row.append(v)
        rows.append(row)
    rk, ker = rank_mod(rows)
    results[W] = (len(monos), len(monos) - rk, ker, monos)
    print("INFO W=%d #mon=%d nullity=%d" % (W, len(monos), len(monos) - rk), flush=True)

report("no isobaric relation of weight 1..15", all(results[W][1] == 0 for W in range(1, 16)))
n16, nul16, ker16, monos16 = results[16]
report("exactly one isobaric relation of weight 16", nul16 == 1)
if nul16 == 1:
    v = ker16[0]
    idx = monos16.index((0, 0, 8, 0, 0))
    report("coefficient of y0^8 is a nonzero constant", v[idx] % P != 0)
    odd = [monos16[i] for i in range(len(monos16)) if v[i] % P and (monos16[i][0] % 2 or monos16[i][1] % 2)]
    report("coefficients even in k1 and in k2 separately", not odd, "(#odd terms=%d)" % len(odd))
    # symmetry k1<->k2
    pos = {m: i for i, m in enumerate(monos16)}
    asym = [m for m in monos16 if (v[pos[m]] - v[pos[(m[1], m[0]) + m[2:]]]) % P]
    report("symmetric in k1 <-> k2", not asym)
    ydeg = max(sum(m[2:]) for i, m in enumerate(monos16) if v[i] % P)
    report("total y-degree 8", ydeg == 8)
print("TOTAL %d/%d OK" % (ok, tot))
