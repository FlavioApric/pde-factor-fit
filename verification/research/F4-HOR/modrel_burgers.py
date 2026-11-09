# F4-HOR · H-ii-a MODREL · controllo (non metodo): relazioni a coefficienti costanti
#   sum_{j,alpha} c_{j,alpha} d^alpha (u^j) = 0,  j in {0 (costante), 1, 2}, |alpha| <= K,
# per soluzioni di Burgers u_t + u u_x = nu u_xx ottenute con Cole-Hopf, nu = 1.
# ESATTO: u e' razionale in E_i = exp(k_i x + nu k_i^2 t); derivazioni D_x E_i = k_i E_i,
# D_t E_i = nu k_i^2 E_i; numeratore polinomiale in E_i (algebricamente indipendenti) = 0.
import sympy as sp
nu = sp.Integer(1)
def setup(ks):
    E = sp.symbols(f'E0:{len(ks)}')
    phi = 1 + sum(E)
    Dx = lambda f: sum(sp.diff(f, Ei)*k*Ei for Ei, k in zip(E, ks))
    Dt = lambda f: sum(sp.diff(f, Ei)*nu*k**2*Ei for Ei, k in zip(E, ks))
    u = sp.together(-2*nu*Dx(phi)/phi)
    assert sp.simplify(Dt(u) + u*Dx(u) - nu*Dx(Dx(u))) == 0
    return E, u, Dx, Dt
def relations(ks, K):
    E, u, Dx, Dt = setup(ks)
    alphas = [(a, b) for a in range(K+1) for b in range(K+1) if a+b <= K]
    feats, names = [sp.Integer(1)], ['1']
    for j in (1, 2):
        for (a, b) in alphas:
            f = u**j
            for _ in range(a): f = Dt(f)
            for _ in range(b): f = Dx(f)
            feats.append(sp.together(f)); names.append(f'dt^{a}dx^{b}(u^{j})')
    c = sp.symbols(f'c0:{len(feats)}')
    num = sp.numer(sp.together(sum(ci*fi for ci, fi in zip(c, feats))))
    eqs = sp.Poly(sp.expand(num), *E).coeffs()
    A = sp.Matrix([[sp.diff(eq, ci) for ci in c] for eq in eqs])
    return names, A.nullspace()
def show(label, ks, K):
    names, ns = relations(ks, K)
    print(f'== {label}, |alpha| <= {K}: {len(names)} feature, dim spazio relazioni = {len(ns)}')
    for v in ns:
        piv = [vi for vi in v if vi != 0][0]
        v = v/piv
        print('    ' + ' + '.join(f'({vi})*{n}' for vi, n in zip(v, names) if vi != 0))
show('1-shock (k=1)', [1], 2)
show('2-shock (k=1,2)', [1, 2], 2)
show('2-shock (k=1,2)', [1, 2], 3)
print('Atteso per 2-shock: solo i multipli R.(Burgers) di ordine <= K: K=2 -> 1, K=3 -> 3')
