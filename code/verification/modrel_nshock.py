# F4-HOR · MODREL · controllo della congettura "N-shock: relazione extra di grado N+1 in u"
# Burgers nu = 1, phi = 1 + sum_{i<=N} exp(k_i x + k_i^2 t); dizionario (u,...,u^D), |alpha| <= K.
import sympy as sp, sys
def run(ks, D, K):
    E = sp.symbols(f'E0:{len(ks)}')
    Dx = lambda f: sum(sp.diff(f, Ei)*k*Ei for Ei, k in zip(E, ks))
    Dt = lambda f: sum(sp.diff(f, Ei)*k**2*Ei for Ei, k in zip(E, ks))
    phi = 1 + sum(E); u = sp.together(-2*Dx(phi)/phi)
    alphas = [(a, b) for a in range(K+1) for b in range(K+1) if a+b <= K]
    feats = []
    for j in range(1, D+1):
        for (a, b) in alphas:
            f = u**j
            for _ in range(a): f = Dt(f)
            for _ in range(b): f = Dx(f)
            feats.append(sp.together(f))
    c = sp.symbols(f'c0:{len(feats)}')
    num = sp.numer(sp.together(sum(ci*fi for ci, fi in zip(c, feats))))
    eqs = sp.Poly(sp.expand(num), *E).coeffs()
    A = sp.Matrix([[sp.diff(eq, ci) for ci in c] for eq in eqs])
    return len(feats), len(A.nullspace())
for ks, D, K in [([1], 1, 2), ([1], 2, 2), ([1, 2], 2, 2), ([1, 2], 3, 2), ([1, 2, 3], 2, 2), ([1, 2, 3], 3, 2), ([1, 2, 3], 4, 1)]:
    nf, dim = run(ks, D, K)
    print(f'N={len(ks)} shock (k={ks}), dizionario u^1..u^{D}, |alpha|<={K}: {nf} feature, dim relazioni = {dim}', flush=True)
print('Multipli di Burgers di ordine <= K: K=1 -> 0, K=2 -> 1')
