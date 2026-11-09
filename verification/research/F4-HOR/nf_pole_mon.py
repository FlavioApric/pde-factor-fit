# F4-HOR · controlli (non metodo) per H-v2 NF, H-v1 PAINLEVE (decomposizione in poli), H-v3 MON-1
import sympy as sp
t, x, nu, eps = sp.symbols('t x nu epsilon', positive=True)
k1, k2, k3 = sp.symbols('k1 k2 k3', nonzero=True)
ok = lambda b: 'OK' if b else 'FAIL'
# ---------- NF-1: correzione di 2o ordine = simbolo -Q2/Q1 alla frequenza somma ----------
# Burgers in forma di Hammerstein: Q1(d) u + Q2(d) u^2 = 0, Q1 = dt - nu dx^2, Q2 = (1/2) dx
Q1 = lambda tau, xi: tau - nu*xi**2
Q2 = lambda tau, xi: xi/2
z = lambda k: (nu*k**2, k)                     # modo e^{k x + nu k^2 t} in V(Q1)
e = lambda k: sp.exp(k*x + nu*k**2*t)
def H2(za, zb):
    s = (za[0]+zb[0], za[1]+zb[1]); return -Q2(*s)/Q1(*s)
c1, c2 = sp.symbols('c1 c2')
v = c1*e(k1) + c2*e(k2)
u2 = sum(ca*cb*H2(z(ka), z(kb))*e(ka)*e(kb) for ca, ka in [(c1, k1), (c2, k2)] for cb, kb in [(c1, k1), (c2, k2)])
u = eps*v + eps**2*u2
res = sp.diff(u, t) + u*sp.diff(u, x) - nu*sp.diff(u, x, 2)
print('NF-1 Burgers: residuo O(eps^2) nullo:', ok(sp.simplify(sp.expand(res).coeff(eps, 2)) == 0))
print('   H2 incrociato (coeff. di c1 c2 e1 e2, simmetrizzato) =', sp.simplify(2*H2(z(k1), z(k2))))
# confronto con lo sviluppo di Cole-Hopf: u = -2 nu dx log(1 + psi), psi = eps*(a1 e1 + a2 e2)
a1, a2 = -c1/(2*nu*k1), -c2/(2*nu*k2)          # scelta che fa coincidere il 1o ordine: -2nu psi_x = eps v
psi = eps*(a1*e(k1) + a2*e(k2))
uCH = -2*nu*sp.diff(sp.log(1+psi), x)
ser = sp.series(uCH, eps, 0, 3).removeO()
print('   Cole-Hopf al 1o ordine = v:', ok(sp.simplify(ser.coeff(eps, 1) - v) == 0))
print('   Cole-Hopf al 2o ordine = u2 (forma normale):', ok(sp.simplify(ser.coeff(eps, 2) - u2) == 0))
# trasformazione esatta inversa: w = u * exp(-(1/2nu) dx^{-1} u) risolve il calore (u da Cole-Hopf normalizzata)
phi = 1 + e(k1) + e(k2)
uex = -2*nu*sp.diff(phi, x)/phi
w = uex*phi                          # exp(-(1/2nu) int u) = phi (normalizzazione phi -> 1 a -inf)
print('   w = u*exp(-(1/2nu) int u) risolve w_t = nu w_xx:', ok(sp.simplify(sp.diff(w, t) - nu*sp.diff(w, x, 2)) == 0))
# KdV-Burgers u_t + u u_x = nu u_xx - d u_xxx : divisore e assenza di risonanze reali (modi di Fourier)
d = sp.symbols('d', positive=True)
om = lambda k: -nu*k**2 + sp.I*d*k**3      # e^{i k x + om t}
div2 = sp.factor(sp.expand(om(k1) + om(k2) - om(k1+k2)))
print('NF KdV-Burgers: divisore quadratico =', div2)
div3 = sp.expand(om(k1)+om(k2)+om(k3)-om(k1+k2+k3))
print('   divisore cubico: Re =', sp.factor(sp.re(div3.subs({k1: sp.Symbol('a', real=True), k2: sp.Symbol('b', real=True), k3: sp.Symbol('c', real=True)}))),
      '; Im =', sp.factor(sp.im(div3.subs({k1: sp.Symbol('a', real=True), k2: sp.Symbol('b', real=True), k3: sp.Symbol('c', real=True)}))))
# KdV (nu = 0): divisore quadratico
omK = lambda k: sp.I*k**3                   # u_t + u_xxx = 0, e^{ikx + om t}: om = i k^3
print('NF KdV: divisore quadratico =', sp.factor(sp.expand(omK(k1)+omK(k2)-omK(k1+k2))))
# ---------- PAINLEVE / poli: decomposizione u = sum_j -2nu/(x - x_j(t)) ----------
a = sp.symbols('a', positive=True)
r = sp.symbols('r')
X = sp.symbols('X')
lead = sp.expand((a*(r/X)*sp.diff(r/X, X) - nu*sp.diff(r/X, X, 2))*X**3)
print('PAINLEVE Burgers u_t + a u u_x = nu u_xx: bilancio dominante -> r =', sp.solve(sp.Eq(lead, 0), r))
phiH = x**2 + 2*nu*t                          # polinomio del calore
upol = -2*nu*sp.diff(phiH, x)/phiH
print('   phi = x^2 + 2 nu t risolve il calore:', ok(sp.simplify(sp.diff(phiH, t) - nu*sp.diff(phiH, x, 2)) == 0))
print('   u = -2nu phi_x/phi risolve Burgers:', ok(sp.simplify(sp.diff(upol, t) + upol*sp.diff(upol, x) - nu*sp.diff(upol, x, 2)) == 0))
x1 = sp.I*sp.sqrt(2*nu*t); x2 = -x1
print('   u = -2nu[1/(x-x1) + 1/(x-x2)]:', ok(sp.simplify(upol - (-2*nu/(x-x1) - 2*nu/(x-x2))) == 0))
print('   dinamica dei poli x1\' = -2nu/(x1-x2):', ok(sp.simplify(sp.diff(x1, t) - (-2*nu/(x1-x2))) == 0))
# ogni polo da solo: u_j = -2nu/(x - x_j(t)) e' soluzione di Burgers solo se x_j costante
xj = sp.Function('xj')(t)
uj = -2*nu/(x - xj)
print('   polo singolo e\' soluzione <=> xj\' = 0: residuo =', sp.simplify(sp.diff(uj, t) + uj*sp.diff(uj, x) - nu*sp.diff(uj, x, 2)))
# KdV razionale: u_t + 6 u u_x + u_xxx = 0
uk = -2/x**2
print('KdV razionale u = -2/x^2:', ok(sp.simplify(sp.diff(uk, t) + 6*uk*sp.diff(uk, x) + sp.diff(uk, x, 3)) == 0))
rK = sp.symbols('rK')
leadK = sp.expand((6*(rK/X**2)*sp.diff(rK/X**2, X) + sp.diff(rK/X**2, X, 3))*X**5)
print('   bilancio dominante KdV (doppio polo) -> rK =', sp.solve(sp.Eq(leadK, 0), rK))
# ---------- MON-1: identificazione non parametrica di (nu, f') in u_t + (f(u))_x = nu u_xx ----------
def mon1(u):
    ux, uxx, ut = sp.diff(u, x), sp.diff(u, x, 2), sp.diff(u, t)
    # f'(u) = (nu u_xx - u_t)/u_x deve dipendere solo da u: condizione d(.) ^ du = 0, lineare in nu
    N = lambda g: sp.diff(g, x)*sp.diff(u, t) - sp.diff(g, t)*sp.diff(u, x)   # (dg ^ du)/(dx^dt)
    A = sp.simplify(N(uxx/ux)); B = sp.simplify(N(ut/ux))
    return A, B, ux, uxx, ut
nu0 = sp.Integer(1)
for lab, phi in [('1-shock', 1 + sp.exp(x + t)), ('2-shock', 1 + sp.exp(x + t) + sp.exp(2*x + 4*t))]:
    U = sp.simplify(-2*nu0*sp.diff(phi, x)/phi)
    A, B, ux, uxx, ut = mon1(U)
    if sp.simplify(A) == 0:
        print(f'MON-1 {lab}: d(u_xx/u_x)^du = 0 => nu NON identificato (atteso per onda viaggiante); d(u_t/u_x)^du =', sp.simplify(B))
    else:
        nusol = sp.simplify(B/A)
        fp = sp.simplify((nusol*uxx - ut)/ux)
        print(f'MON-1 {lab}: nu identificato =', nusol, "; f'(u) - u =", sp.simplify(fp - U))
