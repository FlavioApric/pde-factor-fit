# Verifiche per il recepimento dell'audit S-CHECK-F8-ENC (fix ENC-1, ENC-2, ENC-6, ENC-7, ENC-10, ENC-5).
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import numpy as np

res = []
def check(name, ok, info=""):
    res.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL") + " " + name + ("  " + info if info else ""))

t, x, y, p, k, F = sp.symbols('t x y p k F', real=True)

# 1. ENC-1: stima corretta di A9(b2). Simbolo esatto di E^mult in Fourier:
#    hat(E f)(p) = fhat(p+Ft)[exp(-i(p^2 t + pFt^2 + F^2t^3/3)) - exp(-i p^2 t)]
#    modulo, con p' = p + Ft: |1 - exp(i(F t^2 p' - 2F^2 t^3/3))| |fhat(p')|
pp = sp.symbols('pp', real=True)
ph_exact = (p**2*t + p*F*t**2 + F**2*t**3/3) - p**2*t
ph_sub = sp.expand(ph_exact.subs(p, pp - F*t))
check("A9(b2) fase dopo traslazione = F t^2 p' - 2F^2t^3/3",
      sp.simplify(ph_sub - (F*t**2*pp - sp.Rational(2, 3)*F**2*t**3)) == 0)

def norms(Fv, tv, w):
    L = max(60.0/w, 1e-12)*10
    P = np.linspace(-L, L, 400001); dP = P[1] - P[0]
    fh = np.exp(-(w*P)**2/2)          # fhat di una gaussiana larga w
    nf = np.sqrt(np.sum(fh**2)*dP)
    nfp = np.sqrt(np.sum((P*fh)**2)*dP)
    E = np.sqrt(np.sum(np.abs(1 - np.exp(1j*(Fv*tv**2*P - 2*Fv**2*tv**3/3)))**2*fh**2)*dP)
    return E/nf, nfp/nf
E1, d1 = norms(1.0, 1.0, 25.0)
old = 1.0*d1 + 1.0/6
new = 1.0*d1 + 2.0/3
check("A9(b2) stima vecchia violata (F=t=1, larghezza 25)", E1 > old, "%.4f > %.4f" % (E1, old))
check("A9(b2) stima corretta vale", E1 <= new + 1e-9, "%.4f <= %.4f" % (E1, new))
r = []
for tv in [0.3, 0.1, 0.03]:
    Ev, dv = norms(1.0, tv, 50.0/tv**2)   # larghezza ~ 1/t^2: il termine t^3 domina su t^2 ||f'||
    r.append(Ev/(tv**2*dv + 2*tv**3/3))
check("A9(a) costante 2/3 ottimale: rapporto -> 1", r[-1] > 0.95 and all(v <= 1 + 1e-9 for v in r),
      str([round(v, 4) for v in r]))

# 2. ENC-2: classe V = beta(t) x ha encoder puntuale + gauge con theta = id.
B = sp.Function('B')(t); Xi = sp.Function('Xi')(t); Ph = sp.Function('Ph')(t)
v = sp.exp(sp.I*k*(x - Xi) - sp.I*k**2*t)          # soluzione libera i v_t = -v_yy, y = x - Xi
u = sp.exp(-sp.I*B*x - sp.I*Ph)*v
beta = sp.diff(B, t)
resid = sp.I*sp.diff(u, t) + sp.diff(u, x, 2) - beta*x*u
resid = resid.subs({sp.Derivative(Xi, t): -2*B, sp.Derivative(Ph, t): B**2})
check("V = beta(t)x: u = e^{-iBx-iPhi} v(t, x-Xi), B'=beta, Xi'=-2B, Phi'=B^2", sp.simplify(resid/u) == 0)

# 3. ENC-7: coefficiente di f(-x) per K generico: B = -2 d/dx K(x,-x).
s = sp.symbols('s', real=True)
K = 1 + 2*x + 3*s + x*s + x**2 - s**2/2 + x**2*s       # nucleo generico, non di Goursat
f = 1 + x/3 + x**2 - x**3/5 + x**4/7 + x**5/11
fs = f.subs(x, s)
Tf = f + sp.integrate(K*fs, (s, -x, x))
lhs = -sp.diff(Tf, x, 2) - (-sp.diff(f, x, 2) + sp.integrate(K*(-sp.diff(fs, s, 2)), (s, -x, x)))
A = -2*sp.diff(K.subs(s, x), x)            # q = 0
Bc = -2*sp.diff(K.subs(s, -x), x)
C = sp.diff(K, s, 2) - sp.diff(K, x, 2)
rhs = A*f + Bc*f.subs(x, -x) + sp.integrate(C*fs, (s, -x, x))
check("U1: L_0 T f - T L_0 f = A f(x) + B f(-x) + int C f con B = -2 d/dx K(x,-x)",
      sp.expand(lhs - rhs) == 0)

# 4. ENC-6: osservazione in ogni punto: P(alpha, L_q)(x-x1)^M = c (x-x1)^{M-2d} + ordini superiori.
X = sp.symbols('X')                     # X = x - x1
x1 = sp.Rational(1, 3)
q = 2 - x + x**2/3
qX = sp.expand(q.subs(x, X + x1))
Lq = lambda g: sp.expand(-sp.diff(g, X, 2) + qX*g)
M = 7
h = X**M
P_coeffs = [5, -1, 3]                   # P(alpha, sigma) = 5 - sigma + 3 sigma^2, d = 2
acc = 0; g = h
for c_ in P_coeffs:
    acc += c_*g; g = Lq(g)
acc = sp.expand(acc)
low = min(sp.Poly(acc, X).monoms())[0]
lc = sp.Poly(acc, X).coeff_monomial(X**low)
expected = 3*(-1)**2*sp.factorial(M)/sp.factorial(M - 4)
check("T2(c') termine di ordine minimo (x-x1)^{M-2d} con coeff. p_d (-1)^d M!/(M-2d)!",
      low == M - 4 and lc == expected, "ordine %d, coeff %s" % (low, lc))

# 5. ENC-10: anello coniugato di Avron-Herbst ha coefficienti polinomiali in (t, x).
uu = sp.Function('u')
yv = sp.symbols('yv', real=True)
# v(t,y) = e^{iFt(y-Ft^2) + iF^2t^3/3} u(t, y - F t^2); Phi^{-1} d_t Phi u in coordinate x = y - Ft^2
vexpr = sp.exp(sp.I*F*t*(yv - F*t**2) + sp.I*F**2*t**3/3)*uu(t, yv - F*t**2)
dv = sp.diff(vexpr, t)
back = sp.simplify((dv/sp.exp(sp.I*F*t*(yv - F*t**2) + sp.I*F**2*t**3/3)).subs(yv, x + F*t**2))
U = uu(t, x)
cand = sp.diff(U, t) - 2*F*t*sp.diff(U, x) + sp.I*F*x*U - sp.I*F**2*t**2*U
check("NS2: Phi^{-1} d_t Phi = d_t - 2Ft d_x + iFx - iF^2t^2", sp.simplify(back.doit() - cand) == 0)
dvy = sp.diff(vexpr, yv)
backy = sp.simplify((dvy/sp.exp(sp.I*F*t*(yv - F*t**2) + sp.I*F**2*t**3/3)).subs(yv, x + F*t**2))
check("Phi^{-1} d_y Phi = d_x + iFt", sp.simplify(backy.doit() - (sp.diff(U, x) + sp.I*F*t*U)) == 0)

# 6. ENC-5(c): famiglia stretta, (C) fallisce: W_c manda cos(sqrt(lam)(x-x0)) e^{-i(lam+c)t}
#    in cos(sqrt(lam+c)(x-x0)) e^{-i(lam+c)t} (autofunzione di L_0, stessi dati di Cauchy).
lam, c = sp.symbols('lam c', positive=True)
w_in = sp.cos(sp.sqrt(lam)*x); w_out = sp.cos(sp.sqrt(lam + c)*x)
ok = (sp.simplify(-sp.diff(w_in, x, 2) + c*w_in - (lam + c)*w_in) == 0 and
      sp.simplify(-sp.diff(w_out, x, 2) - (lam + c)*w_out) == 0 and
      w_out.subs(x, 0) == w_in.subs(x, 0) and sp.diff(w_out, x).subs(x, 0) == sp.diff(w_in, x).subs(x, 0))
check("N1'(v): famiglia stretta, uscite non equivalenti per gauge (cos sqrt(lam) vs cos sqrt(lam+c))",
      ok and sp.simplify(w_in - w_out) != 0)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
