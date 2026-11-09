# F6-ENC: algebra di Lie generata da d^2 e x^k nell'algebra di Weyl (aritmetica esatta, niente SymPy).
# k=1 (Avron-Herbst): dimensione finita (Heisenberg + d^2): span{d^2, x, d, 1}.
# k=2 (lens): sl(2) (+ identita'): span{d^2, x^2, x d + 1/2}.
# k>=3: grado in x non limitato => dimensione infinita (evidenza; candidato per P1-Q3).
from fractions import Fraction
from math import comb, perm
def mul(A, B):
    C = {}
    for (i, j), a in A.items():
        for (m, n), b in B.items():
            # x^i d^j x^m d^n = sum_r C(j,r) m!/(m-r)! x^{i+m-r} d^{j-r+n}
            for r in range(0, min(j, m) + 1):
                key = (i + m - r, j - r + n)
                C[key] = C.get(key, 0) + a*b*comb(j, r)*perm(m, r)
    return {k: v for k, v in C.items() if v != 0}
def br(A, B):
    P, Q = mul(A, B), mul(B, A)
    keys = set(P) | set(Q)
    R = {k: P.get(k, 0) - Q.get(k, 0) for k in keys}
    return {k: Fraction(v) for k, v in R.items() if v != 0}
def rank_add(basis, v, keys):
    # eliminazione gaussiana incrementale
    vec = dict(v)
    for piv, b in basis:
        if piv in vec:
            f = vec[piv]/b[piv]
            for k2, val in b.items():
                vec[k2] = vec.get(k2, 0) - f*val
            vec = {k2: val for k2, val in vec.items() if val != 0}
    if vec:
        piv = max(vec)
        basis.append((piv, vec)); return True
    return False
def generate(k, depth):
    D2 = {(0, 2): Fraction(1)}; Xk = {(k, 0): Fraction(1)}
    basis = []; elems = []
    for g in (D2, Xk):
        if rank_add(basis, g, None): elems.append(g)
    dims = [len(elems)]; maxdeg = []
    frontier = list(elems)
    for _ in range(depth):
        new = []
        for a in elems:
            for b in frontier:
                c = br(a, b)
                if c and rank_add(basis, c, None):
                    new.append(c)
        elems += new; frontier = new
        dims.append(len(elems))
        maxdeg.append(max((i for e in elems for (i, j) in e), default=0))
        if not new: break
        if len(elems) > 60: break
    return dims, maxdeg
for k in (1, 2, 3, 4):
    dims, md = generate(k, 5)
    print('k=%d  dimensioni per profondita\':' % k, dims, ' grado max in x:', md)
d1, _ = generate(1, 6); d2, _ = generate(2, 6); d3, m3 = generate(3, 4)
print(('OK  ' if d1[-1] == 4 else 'FAIL'), 'k=1 dimensione 4')
print(('OK  ' if d2[-1] == 3 else 'FAIL'), 'k=2 dimensione 3 (sl2; l\'identita\' compare solo come costante 1/2 dentro x d + 1/2)')
print(('OK  ' if m3[-1] > m3[0] else 'FAIL'), 'k=3 grado in x crescente (dimensione infinita, evidenza)')
