# F6-CONV: verifiche per C2 (localita'): relazioni algebriche dei simboli e crescita del grado minimo.
import sympy as sp, mpmath as mp
tau, xi, k, a, sig = sp.symbols('tau xi kappa a sigma', real=True)
ok = lambda e: sp.simplify(e) == 0
print('== relazioni sui modi e^{tau t + xi x}, xi = i*kappa')
# Poisson e^{-t|D|}: tau = -|kappa| su entrambi i lati -> tau^2 + xi^2 = 0 (Laplace)
for sgn in (+1, -1):
    print('Poisson ramo', sgn, ':', ok(((-sgn*k)**2 + (sp.I*k)**2)))
# KG-semigruppo u_t = -sqrt(1-d_x^2) u: tau = -sqrt(1+kappa^2) -> tau^2 + xi^2 - 1 = 0
print('sqrt(1-dxx) -> tau^2+xi^2-1:', ok((-sp.sqrt(1+k**2))**2 + (sp.I*k)**2 - 1))
# memoria esponenziale u_t = int_{-inf}^t e^{-a(t-s)} u_xx(s) ds: tau = xi^2/(tau+a) -> telegrafo
T = sp.symbols('T')
s_ = sp.symbols('s', positive=True)
lap = sp.integrate(sp.exp(-a*s_)*sp.exp(-T*s_), (s_, 0, sp.oo), conds='none')
print('memoria esp.: kernel^ =', sp.simplify(lap), '-> tau(tau+a) - xi^2 = 0 (telegrafo)')
# frazionario s=p/q su kappa>0: tau = -kappa^(p/q) -> tau^q = (-1)^q kappa^p = (-1)^q (-i xi)^p  (algebrica)
p, q = 3, 2
kk = sp.symbols('kk', positive=True)
print('s=3/4 (|kappa|^{3/2}), kappa>0: tau^2 - kappa^3 = 0 :', ok((-kk**sp.Rational(p, q))**q - kk**p))
print()
print('== crescita del grado minimo: u_M = sum_{j=1}^M e^{-lambda_j t} cos(j x)  (dati M2 esatti, SVD a 60 cifre)')
mp.mp.dps = 60
def D(lams, A, B):
    # d_t^A d_x^B u(0,0)
    re = [1, 0, -1, 0][B % 4]
    return sum((-l)**A * mp.mpf(j)**B * re for j, l in enumerate(lams, start=1))
def mindeg(lams, mmax=6, extra=8):
    for m in range(mmax+1):
        mons = [(i, j) for i in range(m+1) for j in range(m+1-i)]
        K = 2*m + extra
        rows = [[D(lams, A+i, B+j) for (i, j) in mons] for A in range(K-m+1) for B in range(K-m+1-A)]
        M = mp.matrix(rows)
        # normalizza colonne
        for c in range(M.cols):
            nrm = mp.sqrt(sum(M[r, c]**2 for r in range(M.rows)))
            for r in range(M.rows): M[r, c] /= nrm
        sv = mp.svd_r(M, compute_uv=False)
        smin = min(sv[i] for i in range(len(sv))) if M.rows >= M.cols else 0
        if smin < mp.mpf('1e-40'):
            return m, mp.nstr(smin, 3)
    return '>%d' % mmax, None
for M_ in (2, 3, 4, 5):
    heat = [mp.mpf(j)**2 for j in range(1, M_+1)]
    frac = [mp.mpf(j)**mp.sqrt(2) for j in range(1, M_+1)]
    print('M=%d  calore (lambda=j^2): grado min %s   |  frazionario irr. (lambda=j^sqrt2): grado min %s'
          % (M_, mindeg(heat)[0], mindeg(frac)[0]))
