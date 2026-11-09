# S8-VAR — verifica del lemma di Carleman (VAR-L1) e dell'esempio di Tychonoff (VAR-T1(d)).
# (a) identita' ||P_lam z||^2 = ||S z||^2 + ||A z||^2 + q(z) per z gaussiana complessa e phi generica
#     (phi_xt != 0, phi_xxxx != 0): verifica numerica per quadratura su griglia, derivate esatte (sympy).
# (b) disuguaglianza di Carleman per il peso della prova (grafico curvo, s = x - g(t)) su una bolla:
#     rapporto int e^{2 lam phi}|P0 w|^2 / (lam^3 int e^{2 lam phi}|w|^2) >= mu per lam grande.
# (c) serie di Tychonoff u = sum (-i)^k g^(k)(t) x^(2k)/(2k)!, g = exp(-1/t^2): residuo di i u_t + u_xx.
import sympy as sp
import numpy as np

t, x, lam = sp.symbols('t x lam', real=True)
I = sp.I
ok_all = True

def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and ok
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")

# ---------- (a) identita' ----------
phi = sp.Rational(3, 10)*x**2 + sp.Rational(1, 5)*x*t + sp.Rational(1, 10)*t**2*x + sp.Rational(1, 20)*x**4 - sp.Rational(1, 7)*t**2
z = (1 + sp.Rational(3, 10)*x + sp.Rational(1, 5)*I*t*x) * sp.exp(-(x**2 + t**2)/2 + sp.Rational(1, 2)*I*x*t + sp.Rational(1, 3)*I*x)
L = 2.0
fx, fxx, ft = sp.diff(phi, x), sp.diff(phi, x, 2), sp.diff(phi, t)
Sz = sp.diff(z, x, 2) + L**2*fx**2*z + I*sp.diff(z, t)
Az = -2*L*fx*sp.diff(z, x) - L*fxx*z - I*L*ft*z
zx = sp.diff(z, x)
qd = (4*L*fxx*sp.Abs(zx)**2 + 4*L*sp.diff(phi, x, t)*sp.im(zx*sp.conjugate(z))
      + (4*L**3*fx**2*fxx - L*sp.diff(phi, x, 4) + L*sp.diff(phi, t, 2))*sp.Abs(z)**2)
fS = sp.lambdify((t, x), Sz, 'numpy'); fA = sp.lambdify((t, x), Az, 'numpy'); fq = sp.lambdify((t, x), qd, 'numpy')
g = np.linspace(-9, 9, 1201); T, X = np.meshgrid(g, g, indexing='ij'); h = g[1]-g[0]
S_ = fS(T, X); A_ = fA(T, X)
lhs = np.sum(np.abs(S_ + A_)**2)*h*h
rhs = (np.sum(np.abs(S_)**2) + np.sum(np.abs(A_)**2) + np.sum(np.real(fq(T, X))))*h*h
report("(a) identita' P = S + A, ||Pz||^2 = ||Sz||^2+||Az||^2+q(z)", abs(lhs-rhs)/abs(lhs) < 1e-9, f"lhs={lhs:.12g} rhs={rhs:.12g}")
# controllo che il termine incrociato sia necessario (segno): senza di esso l'identita' fallisce
qd_wrong = qd - 8*L*sp.diff(phi, x, t)*sp.im(zx*sp.conjugate(z))
rhs_w = (np.sum(np.abs(S_)**2) + np.sum(np.abs(A_)**2) + np.sum(np.real(sp.lambdify((t, x), qd_wrong, 'numpy')(T, X))))*h*h
report("(a') col segno opposto del termine incrociato l'identita' fallisce", abs(lhs-rhs_w)/abs(lhs) > 1e-4)
# P_lam = e^{lam phi} P0 e^{-lam phi}: verifica simbolica su funzione generica
F = sp.Function('F')(t, x); lam_s = sp.Symbol('lam')
P0 = lambda f: I*sp.diff(f, t) + sp.diff(f, x, 2)
conj_ = sp.simplify(sp.exp(lam_s*phi)*P0(sp.exp(-lam_s*phi)*F))
SA = (sp.diff(F, x, 2) + lam_s**2*fx**2*F + I*sp.diff(F, t)) + (-2*lam_s*fx*sp.diff(F, x) - lam_s*fxx*F - I*lam_s*ft*F)
report("(a'') e^{lam phi} P0 e^{-lam phi} = S + A (simbolico)", sp.simplify(sp.expand(conj_ - SA)) == 0)

# ---------- (b) Carleman per il peso della prova ----------
s_ = sp.Symbol('s')
gfun = sp.Rational(3, 10)*sp.sin(t)          # grafico curvo x = g(t), g in C^inf
b, a, mu, kap = 1.0, 1.0, 0.25, 1.0          # mu = 1/(4b): phi_x in [-3/2,-1/2]
phiw = -(x - gfun) + mu*(x - gfun)**2 - kap*t**2
r2 = (t/a)**2 + ((x - gfun)/b)**2
wexpr = sp.Piecewise((sp.exp(-1/(1 - r2))*(1 + I*x*t + sp.Rational(1, 2)*x), r2 < 1), (0, True))
P0w = I*sp.diff(wexpr, t) + sp.diff(wexpr, x, 2)
fw = sp.lambdify((t, x), wexpr, 'numpy'); fP = sp.lambdify((t, x), P0w, 'numpy'); fph = sp.lambdify((t, x), phiw, 'numpy')
gt = np.linspace(-1, 1, 801); gx = np.linspace(-1.4, 1.4, 1121)
T2, X2 = np.meshgrid(gt, gx, indexing='ij')
with np.errstate(all='ignore'):
    W = np.nan_to_num(fw(T2, X2)); PW = np.nan_to_num(fP(T2, X2)); PH = fph(T2, X2)
ratios = []
for lv in [5, 10, 20, 40, 80]:
    wt = np.exp(2*lv*PH)
    ratios.append(np.sum(wt*np.abs(PW)**2)/(lv**3*np.sum(wt*np.abs(W)**2)))
# soglia della prova: lam^2 >= (sup|phi_tt| + sup phi_xt^2/(2 mu))/mu
phtt = sp.lambdify((t, x), sp.diff(phiw, t, 2), 'numpy')(T2, X2); phxt = sp.lambdify((t, x), sp.diff(phiw, x, t), 'numpy')(T2, X2)
lam0 = np.sqrt((np.max(np.abs(phtt)) + np.max(phxt**2)/(2*mu))/mu)
print("    rapporti (lam=5,10,20,40,80):", ["%.3f" % r for r in ratios], " lam0 della prova = %.2f" % lam0)
report("(b) Carleman: rapporto >= mu = 1/4 per lam >= lam0", all(r >= mu for r, lv in zip(ratios, [5, 10, 20, 40, 80]) if lv >= lam0))

# ---------- (c) Tychonoff ----------
gT = sp.exp(-1/t**2)
K = 14
uT = sum((-I)**k*sp.diff(gT, t, k)*x**(2*k)/sp.factorial(2*k) for k in range(K+1))
res = sp.expand(I*sp.diff(uT, t) + sp.diff(uT, x, 2))
lastterm = (-I)**(K+1)*sp.diff(gT, t, K+1)*x**(2*K)/sp.factorial(2*K)*I  # i*d/dt del termine K non compensato
report("(c) residuo della serie troncata = solo il termine di coda", sp.simplify(res - sp.expand(I*(-I)**K*sp.diff(gT, t, K+1)*x**(2*K)/sp.factorial(2*K))) == 0)
val = complex(sp.N(uT.subs({t: sp.Rational(1, 2), x: sp.Rational(1, 2)}), 30))
report("(c') u(1/2,1/2) != 0 (u non identicamente nulla per t>0)", abs(val) > 1e-6, f"u={val:.6g}")
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
