# F4-HOR · MODREL · controllo: dizionario allargato (u, u^2, u^3), 2-shock di Burgers (nu=1, k=1,2)
# e controllo KdV 2-solitone con (u, u^2): rango del modulo delle sizigie fino all'ordine K.
import sympy as sp
def relations(E, u, Dx, Dt, powers, K):
    alphas = [(a, b) for a in range(K+1) for b in range(K+1) if a+b <= K]
    feats, names = [], []
    for j in powers:
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
def show(label, names, ns):
    print(f'== {label}: {len(names)} feature, dim relazioni = {len(ns)}')
    for v in ns:
        piv = [vi for vi in v if vi != 0][0]; v = v/piv
        print('    ' + ' + '.join(f'({vi})*{n}' for vi, n in zip(v, names) if vi != 0))
# Burgers 2-shock
ks = [1, 2]; E = sp.symbols('E0:2')
Dx = lambda f: sum(sp.diff(f, Ei)*k*Ei for Ei, k in zip(E, ks))
Dt = lambda f: sum(sp.diff(f, Ei)*k**2*Ei for Ei, k in zip(E, ks))
phi = 1 + sum(E); u = sp.together(-2*Dx(phi)/phi)
show('Burgers 2-shock, (u,u^2,u^3), K=2', *relations(E, u, Dx, Dt, (1, 2, 3), 2))
# KdV u_t + 6 u u_x + u_xxx = 0, 2-solitone di Hirota: u = 2 (log f)_xx
k1, k2 = sp.Integer(1), sp.Integer(2)
A12 = ((k1-k2)/(k1+k2))**2
E = sp.symbols('E0:2')   # E_i = exp(k_i x - k_i^3 t)
kk = [k1, k2]
Dx = lambda f: sum(sp.diff(f, Ei)*k*Ei for Ei, k in zip(E, kk))
Dt = lambda f: sum(sp.diff(f, Ei)*(-k**3)*Ei for Ei, k in zip(E, kk))
f = 1 + E[0] + E[1] + A12*E[0]*E[1]
u = sp.together(2*Dx(Dx(f)/f))
assert sp.simplify(Dt(u) + 6*u*Dx(u) + Dx(Dx(Dx(u)))) == 0
show('KdV 2-solitone, (u,u^2), K=3', *relations(E, u, Dx, Dt, (1, 2), 3))
