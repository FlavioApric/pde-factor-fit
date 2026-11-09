# OP-F5D: controllo numerico (NON prova) di OPF5D-T6 (stima O(sqrt(nu)) via Cole-Hopf, senza Kuznetsov)
# u0 = sin x su T, t = 2 > t* = 1. u = (x - E_mu y)/t, v = (x - a(x))/t (Lax-Oleinik).
# Verifica: (a) eps(x) = G_nu - G_0 - nu log(4 pi nu / M) >= 0; (b) int_T eps <= 4 pi nu log(tM);
# (c) ||u - v||_L1 <= 8 pi sqrt(2 nu log(tM)/t), tM = 1 + t ||u0'||; (d) ZS: B_3 + eta^2 B_1 = 0 sul 1-solitone NLS.
import numpy as np, sympy as sp
ok = 0; tot = 0
def chk(name, c, info=''):
    global ok, tot; tot += 1; ok += bool(c); print(('OK  ' if c else 'FAIL'), name, info)
t = 2.0; M = 1.0/t + 1.0; tM = t*M
U0 = lambda y: 1.0 - np.cos(y)            # int_0^y sin
NX = 1200
xs = np.linspace(0, 2*np.pi, NX, endpoint=False); dx = xs[1]-xs[0]
for nu in (1e-2, 2.5e-3, 6.25e-4):
    h = min(np.sqrt(nu)/40, 2e-3)
    ys = np.arange(-6.0, 2*np.pi+6.0, h)
    L1 = 0.0; epsint = 0.0; epsmin = np.inf
    for x in xs:
        Phi = U0(ys) + (x-ys)**2/(2*t)
        j = np.argmin(Phi); m0 = Phi[j]
        # raffinamento del minimo (parabola)
        if 0 < j < len(ys)-1:
            a_, b_, c_ = Phi[j-1], Phi[j], Phi[j+1]
            den = a_ - 2*b_ + c_
            s = 0.5*(a_-c_)/den if den > 0 else 0.0
            amin = ys[j] + s*h; m0 = b_ - 0.25*(a_-c_)*s
        else:
            amin = ys[j]
        w = np.exp(-(Phi-m0)/(2*nu)); I = w.sum()*h
        m = (w*ys).sum()*h/I
        L1 += abs(m-amin)/t*dx
        e = 2*nu*np.log(I/np.sqrt(4*np.pi*nu/M))
        epsint += e*dx; epsmin = min(epsmin, e)
    bound = 8*np.pi*np.sqrt(2*nu*np.log(tM)/t)
    chk(f'nu={nu}: eps >= 0', epsmin > -1e-6, f'(min eps = {epsmin:.2e})')
    chk(f'nu={nu}: int eps <= 4 pi nu log(tM)', epsint <= 4*np.pi*nu*np.log(tM), f'({epsint:.3e} <= {4*np.pi*nu*np.log(tM):.3e})')
    chk(f'nu={nu}: ||u-v||_L1 <= 8 pi sqrt(2 nu log(tM)/t)', L1 <= bound, f'(L1 = {L1:.4e}, L1/nu = {L1/nu:.2f}, bound = {bound:.3e})')
# (d) NLS focusing, 1-solitone q = 2 eta sech(2 eta x) (zeta_1 = i eta): relazione con Omega = zeta^2 + eta^2
x = sp.symbols('x', real=True); eta = sp.symbols('eta', positive=True)
q = 2*eta/sp.cosh(2*eta*x); r = -q
D = lambda e, k=1: sp.diff(e, x, k)
A = [sp.Integer(1)]; B = [sp.Integer(0)]; C = [sp.Integer(0)]
for mm in range(0, 4):
    B.append(sp.I/2*(D(B[mm])+2*q*A[mm])); C.append(-sp.I/2*(D(C[mm])-2*r*A[mm]))
    k = mm+1
    s = sum(A[i]*A[k-i] for i in range(1, k)) + sum(B[i]*C[k-i] for i in range(0, k+1))
    A.append(-s/2)
rel = sp.simplify((B[3] + eta**2*B[1]).rewrite(sp.exp))
chk('ZS 1-solitone: B_3 + eta^2 B_1 = 0 (Omega = zeta^2+eta^2, beta_2=1, beta_0=eta^2)', sp.simplify(rel) == 0)
rel2 = sp.simplify((B[2]).rewrite(sp.exp))
chk('ZS 1-solitone: nessuna relazione di grado 1 (B_2 != 0)', sp.simplify(rel2) != 0)
print(f'TOTALE {ok}/{tot}')
