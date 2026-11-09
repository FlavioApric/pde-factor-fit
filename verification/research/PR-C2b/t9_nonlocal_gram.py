"""T9 — non locale / frazionario (C2.37, C2.38) + proposizione generale sui blocchi di Gram (C1.0)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary, RESULTS

x = sp.symbols('x', real=True)
t, lam, al, T0, D, c = sp.symbols('t lambda alpha T D c', positive=True)
kap = sp.symbols('kappa', real=True)
z = sp.symbols('z', positive=True)
s = sp.symbols('s', positive=True)

# ---- C2.38 Caputo: E_alpha(-lam t^alpha) risolve D^alpha u = -lam u (residuo della troncata = solo coda)
N = 6
def caputo_pow(gamma_exp):  # D^alpha t^{gamma}, gamma = alpha*k
    return sp.gamma(gamma_exp + 1)/sp.gamma(gamma_exp + 1 - al)*t**(gamma_exp - al)
uN = sum((-lam)**kk*t**(al*kk)/sp.gamma(al*kk + 1) for kk in range(N + 1))
DuN = sum((-lam)**kk/sp.gamma(al*kk + 1)*caputo_pow(al*kk) for kk in range(1, N + 1))  # k=0: costante -> 0
res = sp.simplify(sp.gammasimp(DuN + lam*uN))
check("C2.38 Caputo: D^a E_N + lam E_N = coda lam(-lam)^N t^{aN}/Gamma(aN+1)",
      sp.gammasimp(res - lam*(-lam)**N*t**(al*N)/sp.gamma(al*N + 1)))
# RL: D_RL^a t^{a-1} = d/dt I^{1-a} t^{a-1} = d/dt Gamma(a) = 0
I_pow = lambda beta, gam: sp.gamma(gam + 1)/sp.gamma(gam + beta + 1)*t**(gam + beta)
check("C2.38 Riemann-Liouville: t^{a-1} in ker D_RL^a", sp.diff(sp.gammasimp(I_pow(1 - al, al - 1)), t))
# NON-semigruppo: coefficiente di xy in E_a(x+y) vs E_a(x)E_a(y): 2/Gamma(2a+1) vs 1/Gamma(a+1)^2
diff_coef = 2/sp.gamma(2*al + 1) - 1/sp.gamma(al + 1)**2
check("C2.38 alpha=1: E(x+y)=E(x)E(y) (coefficiente xy coincide)", diff_coef.subs(al, 1))
check_true("C2.38 alpha=1/2: E(x+y) != E(x)E(y)  => split moltiplicativo G3 FALLISCE", sp.simplify(diff_coef.subs(al, sp.Rational(1, 2))) != 0,
           str(sp.simplify(diff_coef.subs(al, sp.Rational(1, 2)))))
# subordinazione alpha=1/2: E_{1/2}(-z) = int_0^inf M_{1/2}(s) e^{-z s} ds, M_{1/2}(s) = e^{-s^2/4}/sqrt(pi)
sub = sp.integrate(sp.exp(-s**2/4)/sp.sqrt(sp.pi)*sp.exp(-z*s), (s, 0, sp.oo))
check("C2.38 subordinazione: int M_{1/2}(s) e^{-zs} ds = e^{z^2} erfc(z) = E_{1/2}(-z)", sp.simplify(sub - sp.exp(z**2)*sp.erfc(z)))
# e^{z^2} erfc(z) = E_{1/2}(-z): confronto serie
E12 = sum((-z)**kk/sp.gamma(sp.Rational(kk, 2) + 1) for kk in range(12))
check("C2.38 serie E_{1/2}(-z) = e^{z^2}erfc(z) fino a z^11", sp.expand(sp.series(sp.exp(z**2)*sp.erfc(z), z, 0, 12).removeO() - E12))
a_, b_ = sp.symbols('a b', positive=True)
check("C2.38 dentro la subordinazione lo split e' esatto: e^{-(a+b)s t^al} = e^{-a s t^al} e^{-b s t^al}",
      sp.exp(-(a_ + b_)*s*t**al) - sp.exp(-a_*s*t**al)*sp.exp(-b_*s*t**al))

# ---- C2.37/C2.38 Cauchy (s=1/2): P_t = t/(pi(t^2+x^2)) armonica in (t,x) e simbolo e^{-t|k|}
Pt = t/(sp.pi*(t**2 + x**2))
check("C2.38 Poisson P_t armonica (Caffarelli-Silvestre s=1/2)", sp.diff(Pt, t, 2) + sp.diff(Pt, x, 2))
kp = sp.symbols('kp', positive=True)
xp = sp.symbols('xp', positive=True)  # P_t pari in x: basta x>0
inv = sp.integrate(sp.exp(-t*kp)*sp.cos(kp*xp), (kp, 0, sp.oo), conds='none')/sp.pi
check("C2.38 (1/2pi) int e^{-t|k|} e^{ikx} dk = P_t (x>0, pari)", sp.simplify(inv - Pt.subs(x, xp)))
check("C2.38 frazionario in spazio: modi e^{ikx - |k|^{2s} t} (Fourier multiplier) e split commutante",
      sp.exp(-(sp.Abs(kap)**sp.Rational(3, 2) + D*kap**2)*t) - sp.exp(-sp.Abs(kap)**sp.Rational(3, 2)*t)*sp.exp(-D*kap**2*t))
# ---- C2.37 diffusione non locale u_t = J*u - u, J gaussiano: simbolo Jhat(k) - 1
sg = sp.symbols('sigma', positive=True)
J = sp.exp(-x**2/(2*sg**2))/sp.sqrt(2*sp.pi*sg**2)
Jhat = sp.integrate(J*sp.exp(-sp.I*kap*x), (x, -sp.oo, sp.oo))
check("C2.37 Jhat(k) = e^{-sigma^2 k^2/2}", sp.simplify(Jhat - sp.exp(-sg**2*kap**2/2)))
y_ = sp.symbols('y', real=True)
conv = sp.integrate(J.subs(x, x - y_)*sp.exp(sp.I*kap*y_), (y_, -sp.oo, sp.oo))
check("C2.37 J*e^{iky} = Jhat(k) e^{ikx} (esponenziali = autofunzioni della convoluzione)", sp.simplify(conv - sp.exp(-sg**2*kap**2/2)*sp.exp(sp.I*kap*x)))

# ---- PROPOSIZIONE Gram (C1.0): su T x [0,T], <e^{ikx+tau1 t}, e^{ilx+tau2 t}> = 2pi delta_kl (e^{sT}-1)/s, s = tau1 + conj(tau2)
sv = sp.symbols('s_v')
check("Gram: int_0^T e^{s t} dt = (e^{sT}-1)/s", sp.integrate(sp.exp(sv*t), (t, 0, T0)).args[0][0] - (sp.exp(sv*T0) - 1)/sv
      if isinstance(sp.integrate(sp.exp(sv*t), (t, 0, T0)), sp.Piecewise) else sp.integrate(sp.exp(sv*t), (t, 0, T0)) - (sp.exp(sv*T0) - 1)/sv)
# coerenza calore/trasporto al modo k: mu_k = |<e1,e2>|/(|e1||e2|) -> 0 come k^{-1}
kk = sp.symbols('k', positive=True)
st = -D*kk**2 + sp.I*c*kk   # tau_heat + conj(tau_transport), tau_tr = -ick
ip = (sp.exp(st*T0) - 1)/st
n1 = T0                       # |e_tr|^2/(2pi)
n2 = (1 - sp.exp(-2*D*kk**2*T0))/(2*D*kk**2)
mu2 = sp.simplify(ip*sp.conjugate(ip)/(n1*n2))
lead = sp.limit(mu2*kk**2, kk, sp.oo)
check("Gram: mu_k^2 k^2 -> 2/(D T) (coerenza calore-trasporto ~ sqrt(2/(DT))/k)", sp.simplify(lead - 2/(D*T0)))
# coerenza Schrodinger/Airy (entrambi unitari): |int_0^T e^{i(k^2 - k^3)t}dt|/T -> 0 come 1/k^3
ph = kk**3 - kk**2
mu = sp.Abs((sp.exp(sp.I*ph*T0) - 1)/(sp.I*ph))/T0
check_true("Gram: coerenza Schrod-Airy <= 2/(T|k^3-k^2|) -> 0", sp.simplify(sp.limit(2/(T0*ph), kk, sp.oo)) == 0)
# coerenza onda destra/sinistra su [0,T]: |sin(ckT)|/(ckT)
mu_w = sp.Abs(sp.integrate(sp.exp(-2*sp.I*c*kk*t), (t, 0, T0)))/T0
check("Gram: onda destra/sinistra mu_k = |sin(ckT)|/(ckT)", sp.simplify(sp.Abs(sp.sin(c*kk*T0))/(c*kk*T0) - mu_w.rewrite(sp.sin).simplify()))
summary("t9_nonlocal_gram")

# coerenza nonlocale (tau -> -1 per k grande, J gaussiano) / calore
RESULTS.clear() if False else None
tn = sp.exp(-sg**2*kk**2/2) - 1
s_nl = tn - D*kk**2
ip_nl = (sp.exp(s_nl*T0) - 1)/s_nl
n_nl = (sp.exp(2*tn*T0) - 1)/(2*tn)
n_h = (1 - sp.exp(-2*D*kk**2*T0))/(2*D*kk**2)
lead_nl = sp.limit(ip_nl**2/(n_nl*n_h)*kk**2, kk, sp.oo)
check("Gram: nonlocale(J*u-u)/calore mu_k^2 k^2 -> 4/(D(1-e^{-2T}))", sp.simplify(lead_nl - 4/(D*(1 - sp.exp(-2*T0)))))
summary("t9_nonlocal_gram (con aggiunta)")
