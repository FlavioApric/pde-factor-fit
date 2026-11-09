# audit_s4term.py — S-CHECK-11, red team SymPy/numpy per S4-TERM (26/10/2026)
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_s4term.py > audit_s4term.out
import sys
sys.stdout.reconfigure(encoding='utf-8')
import sympy as sp
import numpy as np
from itertools import product

RES = []
import random
def iszero(e, n=6):
    e = sp.sympify(e)
    if e == 0:
        return True
    syms = sorted(e.free_symbols, key=str)
    rnd = random.Random(1)
    for _ in range(n):
        sub = {v: sp.Rational(rnd.randint(-97, 97), rnd.randint(13, 41)) for v in syms}
        val = complex(sp.N(e.subs(sub), 30))
        if abs(val) > 1e-18:
            return False
    return True
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL") + " | " + name + ((" | " + str(info)) if info else ""))

x, t, s, nu, eps, d, r, lam = sp.symbols('x t s nu epsilon d r lambda', real=True)
NJ = 16
U = sp.symbols('u0:%d' % NJ)

def Dtot(G):
    return sum(sp.diff(G, U[k]) * U[k + 1] for k in range(NJ - 1))
def Dk(G, k):
    for _ in range(k):
        G = Dtot(G)
    return G
def Dev(P, G):
    """derivazione evolutiva D_P G = sum_k dG/du_k * d^k P"""
    out = 0
    for k in range(NJ):
        g = sp.diff(G, U[k])
        if g != 0:
            out += g * Dk(P, k)
    return sp.expand(out)
def evalf_(G, f):
    sub = {U[k]: sp.diff(f, x, k) for k in range(NJ)}
    return sp.expand(G.subs(sub))

A = nu * U[2]; B = -U[0] * U[1]

# ---------- 1. S4T-T1: getto in t via parole, Burgers ----------
K = 4
def word_coeffs(Ts, K):
    """coefficiente di s^k/k! di E^add (somma parole non costanti)"""
    N = len(Ts)
    out = {}
    for k in range(2, K + 1):
        tot = 0
        for w in product(range(N), repeat=k):
            if len(set(w)) < 2:
                continue
            G = U[0]
            for n in reversed(w):  # D_{n1}...D_{nk} u0: applica prima l'ultima lettera
                G = Dev(Ts[n], G)
            tot += G
        out[k] = sp.expand(tot)
    return out
Wadd = word_coeffs([A, B], K)
c2 = sp.expand(Wadd[2] / 2)
check("T1(iii) [s^2]E^add Burgers = -nu(2u'u''+u u''')", sp.expand(c2 + nu * (2 * U[1] * U[2] + U[0] * U[3])) == 0)
c2_formula = sp.expand(sp.Rational(1, 2) * (Dev(A, B) + Dev(B, A)))
check("T1(i) [s^2] = 1/2 sum_{m!=n} T_n'[T_m]", sp.expand(c2 - c2_formula) == 0)
# omogeneità: coefficiente di s^k: termini nu^a con grado b+1, peso 2a+b, a+b=k, a,b>=1
def weight(mon):
    return sum(k * e for k, e in enumerate(sp.Poly(mon, *U).monoms()[0]))
ok_h = True
for k in range(2, K + 1):
    P = sp.Poly(Wadd[k], nu, *U)
    for mon, cf in P.terms():
        a = mon[0]; degs = mon[1:]
        deg = sum(degs); wt = sum(i * e for i, e in enumerate(degs))
        b = k - a
        if not (a >= 1 and b >= 1 and deg == b + 1 and wt == 2 * a + b):
            ok_h = False
check("T1(iii) omogeneità nu^a, grado b+1, peso 2a+b, a,b>=1 (k<=4)", ok_h)

# ---------- 1b. Controllo indipendente: Hopf–Cole + caratteristiche + calore (serie in t come liste; x tramite z = e^{ix}) ----------
def trunc(e, n=4, var=t):
    e = sp.expand(e)
    return sum(e.coeff(var, k) * var ** k for k in range(n + 1))
zv = sp.Symbol('z')
def dxz(g, k=1):
    for _ in range(k):
        g = sp.expand(sp.I * zv * sp.diff(g, zv))
    return g
def evz(G, f):
    return sp.expand(G.subs({U[k]: dxz(f, k) for k in range(NJ)}))
def smul(a, b, n):
    return [sp.expand(sum(a[i] * b[k - i] for i in range(k + 1) if i < len(a) and k - i < len(b))) for k in range(n + 1)]
def sadd(*ss):
    n = max(len(q) for q in ss)
    return [sp.expand(sum(q[k] for q in ss if k < len(q))) for k in range(n)]
def sscale(a, c):
    return [sp.expand(c * q) for q in a]
def sshift(a, n):  # moltiplica per t
    return ([sp.Integer(0)] + list(a))[:n + 1]
def sdx(a, k=1):
    return [dxz(q, k) for q in a]
def heat_s(a, n):  # S_A(t) applicato a una serie a(t)
    out = [sp.Integer(0)] * (n + 1)
    for m in range(n + 1):
        term = [sp.Integer(0)] * m + [sp.expand(nu ** m * q / sp.factorial(m)) for q in sdx(a, 2 * m)]
        out = sadd(out, term[:n + 1])
    return out[:n + 1]
def compose_shift(a, alpha, n):  # a(t)(x + alpha(t)) = sum_j alpha^j d^j a / j!
    out = [sp.Integer(0)] * (n + 1); pw = [sp.Integer(1)] + [sp.Integer(0)] * n
    for j in range(n + 1):
        out = sadd(out, sscale(smul(pw, sdx(a, j), n), sp.Rational(1, sp.factorial(j))))
        pw = smul(pw, alpha, n)
    return out[:n + 1]
def transport_s(a, n):  # v = a(t)(x - t v)
    v = list(a[:n + 1]) + [sp.Integer(0)] * (n + 1 - len(a))
    for _ in range(n + 1):
        v = compose_shift(a, sshift(sscale(v, -1), n), n)
    return v
def sinv(a, n):
    inv = [sp.Integer(1) / a[0]] + [sp.Integer(0)] * n
    for k in range(1, n + 1):
        inv[k] = sp.expand(-sum(a[i] * inv[k - i] for i in range(1, k + 1) if i < len(a)) / a[0])
    return inv
def hopf_s(f, n):  # u = f - 2nu P_x/P, P = sum (nu t)^k R_{2k}/k!, phi0^(m) = phi0 R_m
    R = [sp.Integer(1)]
    for m in range(2 * n + 2):
        R.append(sp.expand(dxz(R[-1]) - f / (2 * nu) * R[-1]))
    P = [sp.expand(nu ** k * R[2 * k] / sp.factorial(k)) for k in range(n + 1)]
    q = smul(sdx(P), sinv(P, n), n)
    return sadd([f], sscale(q, -2 * nu))
def sval(a):
    return sp.expand(sum(c * t ** k for k, c in enumerate(a)))
NT = 4
u0f = sp.expand(eps * ((zv - 1 / zv) / (2 * sp.I) + (zv ** 2 + zv ** -2) / 4))
u_s = hopf_s(u0f, NT); h_s = heat_s([u0f], NT); v_s = transport_s([u0f], NT)
Eadd_s = sadd(u_s, sscale(h_s, -1), sscale(v_s, -1), [u0f])
ok = iszero(Eadd_s[0]) and iszero(Eadd_s[1])
for k in range(2, NT + 1):
    if not iszero(Eadd_s[k] - evz(Wadd[k], u0f) / sp.factorial(k)):
        ok = False; print("   diff at k=", k)
check("T1(i) getto E^add (parole) = Hopf–Cole − calore − caratteristiche + u0, t^0..t^4 (dato eps(sin x + cos2x/2))", ok)
ok = True
mu_ = sp.Symbol('mu_', positive=True)
for k in range(2, NT + 1):
    ck = Eadd_s[k]
    if not iszero(ck.subs(nu, mu_ * eps) - eps ** (k + 1) * ck.subs({nu: mu_, eps: 1})):
        ok = False
check("T1(iii) legge di scala: [t^k]E(eps, nu=mu*eps) = eps^{k+1}[t^k]E(1,mu)", ok)
fs = sp.expand(eps * (zv - 1 / zv) / (2 * sp.I))
Es_ = sadd(hopf_s(fs, 2), sscale(heat_s([fs], 2), -1), sscale(transport_s([fs], 2), -1), [fs])
check("T1 esempio u0=eps sin x: [t^2]E^add = 3/2 nu eps^2 sin2x", iszero(Es_[2] - sp.Rational(3, 2) * nu * eps ** 2 * (zv ** 2 - zv ** -2) / (2 * sp.I)))
SA_SB = heat_s(v_s, NT)
EAB_s = sadd(u_s, sscale(SA_SB, -1))
SB_SA = transport_s(h_s, NT)
EBA_s = sadd(u_s, sscale(SB_SA, -1))
pAB = evz(nu * U[1] * U[2], u0f)
check("T1(ii)-(iii) [t^2]E^mult_AB = nu u0'u0'' (composizione esplicita dei flussi)", iszero(EAB_s[2] - pAB))
check("T1(ii)-(iii) [t^2]E^mult_BA = -nu u0'u0''", iszero(EBA_s[2] + pAB))
def lie_prod(P1, P2, n):  # getto di e^{tD_{P2}} e^{tD_{P1}} u0 = phi1(phi2(w))
    out = []
    for k in range(n + 1):
        tot = 0
        for j in range(k + 1):
            i = k - j
            G = U[0]
            for _ in range(j):
                G = Dev(P1, G)
            for _ in range(i):
                G = Dev(P2, G)
            tot += G / (sp.factorial(i) * sp.factorial(j))
        out.append(sp.expand(tot))
    return out
LP = lie_prod(A, B, 3)
check("Lemma J(ii): getto di S_A(t)S_B(t)u0 = e^{tD_B}e^{tD_A}u0 (ordine di Gröbner), k<=3", all(iszero(evz(LP[k], u0f) - SA_SB[k]) for k in range(4)))
ok = True
for k in range(2, NT + 1):
    for E_ in (EAB_s, EBA_s):
        ck = E_[k]
        if not iszero(ck.subs(nu, 0)) or not iszero(sp.diff(ck, eps).subs(eps, 0)):
            ok = False
check("T1(ii): E^mult senza parole costanti (nessun termine nu^0, nessun termine eps^1), k<=4", ok)
# KdV-Burgers e Fisher
C = -d * U[3]
W3 = word_coeffs([A, C, B], 2)
c2kb = sp.expand(W3[2] / 2)
pred = sp.expand(-nu * (2 * U[1] * U[2] + U[0] * U[3]) - nu * d * U[5] + d / 2 * (2 * U[0] * U[4] + 5 * U[1] * U[3] + 3 * U[2] ** 2))
check("T1(iv) KdV–Burgers [s^2]E^add", sp.expand(c2kb - pred) == 0)
ex = evalf_(c2kb, eps * sp.sin(x))
predsin = -eps / 2 * (2 * d * nu * sp.cos(x) + 5 * d * eps * sp.cos(2 * x) - 3 * eps * nu * sp.sin(2 * x))
check("T4(i) KdVB u0=eps sin x", iszero(ex - predsin))
Rf = r * (U[0] - U[0] ** 2)
Wf = word_coeffs([A, Rf], 2)
check("T1(v) Fisher [s^2]E^add = r nu(u''-u'^2-2uu'')", sp.expand(Wf[2] / 2 - r * nu * (U[2] - U[1] ** 2 - 2 * U[0] * U[2])) == 0)
check("T1(v) Fisher [s^2]E^mult_AR = r nu u'^2", sp.expand(sp.Rational(1, 2) * (Dev(A, Rf) - Dev(Rf, A)) - r * nu * U[1] ** 2) == 0)

# ---------- 2. S4T-T2: forme chiuse lagrangiane vs getti, primo ordine in nu ----------
NT2 = 5
fz = sp.expand(eps * (zv - 1 / zv) / (2 * sp.I))  # eps sin x
alpha = [sp.Integer(0)] * (NT2 + 1)   # a(x) = x + alpha, alpha = -t f(x + alpha)
for _ in range(NT2 + 1):
    alpha = sshift(sscale(compose_shift([fz], alpha, NT2), -1), NT2)
def at_a(g):
    return compose_shift([g], alpha, NT2)
u1a = at_a(dxz(fz)); u2a = at_a(dxz(fz, 2))
Ja = sadd([sp.Integer(1)], sshift(u1a, NT2))
invJ = sinv(Ja, NT2)
iJ2 = smul(invJ, invJ, NT2); iJ3 = smul(iJ2, invJ, NT2)
E1add = sshift(sadd(smul(u2a, iJ2, NT2), [-dxz(fz, 2)]), NT2)
E1AB = sshift(sshift(smul(smul(u1a, u2a, NT2), iJ3, NT2), NT2), NT2)
E1BA = sscale(sshift(sshift(smul(smul(u1a, u2a, NT2), iJ2, NT2), NT2), NT2), -1)
uF = hopf_s(fz, NT2); hF = heat_s([fz], NT2); vF = transport_s([fz], NT2)
EaddF = sadd(uF, sscale(hF, -1), sscale(vF, -1), [fz])
EABF = sadd(uF, sscale(heat_s(vF, NT2), -1))
EBAF = sadd(uF, sscale(transport_s(hF, NT2), -1))
def nu1(e):
    return sp.expand(sp.diff(e, nu).subs(nu, 0))
check("T2 coefficiente di nu^1 di E^add = forma chiusa (t<=5, tutti gli eps; u0=eps sin x)", all(iszero(nu1(EaddF[k]) - E1add[k]) for k in range(NT2 + 1)))
check("T2 coefficiente di nu^1 di E^mult_AB = t^2 u'u''/J^3 (t<=5)", all(iszero(nu1(EABF[k]) - E1AB[k]) for k in range(NT2 + 1)))
check("T2 coefficiente di nu^1 di E^mult_BA = -t^2 u'u''/J^2 (t<=5)", all(iszero(nu1(EBAF[k]) - E1BA[k]) for k in range(NT2 + 1)))
for name, E_ in (("add", EaddF), ("AB", EABF), ("BA", EBAF)):
    c_nu2 = [sp.expand(sp.diff(c, nu, 2).subs(nu, 0) / 2) for c in E_]
    ok = all(iszero(c_nu2[k]) for k in range(3)) and all(iszero(sp.diff(c_nu2[k], eps).subs(eps, 0)) for k in range(NT2 + 1))
    check("T2 Passo 7: parte nu^2 di R^%s = O(t^3) e senza termine eps^1 (getto t<=5)" % name, ok)
delta = sshift(smul(u2a, iJ2, NT2), NT2)
vxx = sdx(vF, 2)
dt_delta = [sp.expand((k + 1) * delta[k + 1]) for k in range(NT2)]
res = sadd(dt_delta, sdx(smul(vF, delta, NT2), 1)[:NT2], sscale(vxx[:NT2], -1))
check("T2 Passo 4: delta = t u0''(a)/J^2 risolve delta_t+(v delta)_x = v_xx (serie t<=4)", all(iszero(q) for q in res))
check("T2 Passo 4: v_xx = u0''(a)/J^3 (serie t<=5)", all(iszero(q) for q in sadd(vxx, sscale(smul(u2a, iJ3, NT2), -1))))

# Passo 7: identità per hat w (simbolica con funzioni generiche)
X_, T_ = sp.symbols('X T')
uf, hf_, vf, df, u0g = [sp.Function(n)(T_, X_) for n in ('u', 'h', 'v', 'delta', 'dummy')]
u0x = sp.Function('u0')(X_)
rules = {sp.Derivative(uf, T_): nu * sp.diff(uf, X_, 2) - uf * sp.diff(uf, X_),
         sp.Derivative(hf_, T_): nu * sp.diff(hf_, X_, 2),
         sp.Derivative(vf, T_): -vf * sp.diff(vf, X_),
         sp.Derivative(df, T_): sp.diff(vf, X_, 2) - sp.diff(vf * df, X_)}
what = (uf - hf_) - (vf - u0x) - nu * (df - T_ * sp.diff(u0x, X_, 2))
lhs = sp.diff(what, T_) + sp.diff(vf * what, X_) - nu * sp.diff(what, X_, 2)
lhs = lhs.subs(rules)
e_ = uf - vf; rh = hf_ - u0x - nu * T_ * sp.diff(u0x, X_, 2)
rhs = nu ** 2 * sp.diff(df - T_ * sp.diff(u0x, X_, 2), X_, 2) - sp.diff(vf * rh, X_) - e_ * sp.diff(e_, X_)
check("T2 Passo 7: equazione di hat w (identità esatta)", sp.simplify(sp.expand(lhs - rhs)) == 0)
# Passo 7(1): d_x^2(delta - s u0'') con u0 -> lam*u0: coefficienti lam^0, lam^1 nulli; t^0,t^1 nulli
fl = lam * (sp.sin(x) + sp.cos(2 * x) / 2)
a_l = x
for _ in range(5):
    a_l = trunc(sp.expand(x - t * sum((a_l - x) ** j * sp.diff(fl, x, j) / sp.factorial(j) for j in range(5))), 4)
def at_al(g):
    return trunc(sp.expand(sum((a_l - x) ** j * sp.diff(g, x, j) / sp.factorial(j) for j in range(5))), 4)
Jl = trunc(1 + t * at_al(sp.diff(fl, x)), 4)
iJl = trunc(sp.series(1 / Jl, t, 0, 5).removeO(), 4)
gl = sp.expand(sp.diff(trunc(t * at_al(sp.diff(fl, x, 2)) * iJl ** 2, 4) - t * sp.diff(fl, x, 2), x, 2))
okq = all(iszero(gl.coeff(t, k)) for k in range(2)) and all(iszero(sp.expand(gl.coeff(t, k)).coeff(lam, j)) for k in range(5) for j in range(2))
check("T2 Passo 7(1): d^2(delta - s u0'') = O(s^2) e O(lam^2) (getto s<=4)", okq)

# ---------- 3. S4T-P3: costanti e limite numerico ----------
z = sp.symbols('z', positive=True)
for p, val in ((2, 3 * sp.sqrt(3) / 16), (3, 25 * sp.sqrt(5) / 216)):
    Mp = sp.maximum(z / (1 + z ** 2) ** p, z, sp.Interval(0, sp.oo))
    check("P3 M_%d = %s" % (p, val), sp.simplify(Mp - val) == 0)
# u0 = sin x: a* = pi, kappa = 1, t* = 1
aa = np.linspace(0, 2 * np.pi, 400001)
for eta in (1e-2, 1e-3, 1e-4):
    tt = 1 - eta
    J = 1 + tt * np.cos(aa); u2 = -np.sin(aa); u1 = np.cos(aa); X = aa + tt * np.sin(aa)
    Eadd1 = tt * (u2 / J ** 2 - (-np.sin(X)))
    EAB1 = tt ** 2 * u1 * u2 / J ** 3
    EBA1 = -tt ** 2 * u1 * u2 / J ** 2
    print("   P3 eta=%g: eta^1.5 sup|E1add|=%.5f eta^2.5 sup|E1AB|=%.5f eta^1.5 sup|E1BA|=%.5f" % (
        eta, eta ** 1.5 * np.abs(Eadd1).max(), eta ** 2.5 * np.abs(EAB1).max(), eta ** 1.5 * np.abs(EBA1).max()))
lim2 = float(3 * np.sqrt(3) / 16 * np.sqrt(2)); lim3 = float(25 * np.sqrt(5) / 216 * np.sqrt(2))
print("   P3 limiti previsti: %.5f, %.5f, %.5f" % (lim2, lim3, lim2))
eta = 1e-4; tt = 1 - eta; J = 1 + tt * np.cos(aa)
check("P3 numerico (sin x, eta=1e-4) entro 2%", abs(eta ** 1.5 * np.abs(tt * (-np.sin(aa) / J ** 2 + np.sin(aa + tt * np.sin(aa)))).max() / lim2 - 1) < 0.02
      and abs(eta ** 2.5 * np.abs(tt ** 2 * np.cos(aa) * np.sin(aa) / J ** 3).max() / lim3 - 1) < 0.02)

# ---------- 4. S4T-L2/T3: D per sin x, t=2; T3(iii) numerico con Hopf–Cole ----------
from scipy.optimize import brentq
from scipy.special import logsumexp, erfc
tt = 2.0
sstar = brentq(lambda q: q - tt * np.sin(q), 0.5, 3.0)
Dj = 2 * sstar / tt
print("   L2(d) sin x, t=2: a^+-pi = %.6f, D = %.6f, |I|/t = %.6f" % (sstar, Dj, 2 * (np.pi - np.arccos(-1 / tt)) / tt))
check("L2(d) D >= |I|/t (sin x, t=2): I = {1+2cos a<0}", Dj >= 2 * (np.pi - np.arccos(-1 / tt)) / tt - 1e-12)
check("T3(iii) int_0^inf Phi_N(-s) ds = 1/sqrt(2pi)", sp.simplify(sp.integrate(sp.erfc(s / sp.sqrt(2)) / 2, (s, 0, sp.oo)) - 1 / sp.sqrt(2 * sp.pi)) == 0)
check("T3(iii) sqrt2*D*sqrt t * 1/sqrt(2pi) = D sqrt(t/pi)", sp.simplify(sp.sqrt(2) / sp.sqrt(2 * sp.pi) - 1 / sp.sqrt(sp.pi)) == 0)
w_ = sp.symbols('w', positive=True)
check("T3(iii) int_0^1 e^{-w^2/4} dw >= e^{-1/4}", float(sp.integrate(sp.exp(-w_ ** 2 / 4), (w_, 0, 1))) >= float(sp.exp(-sp.Rational(1, 4))))
# Hopf–Cole numerico (vettorizzato): u(t,x) = (x - E_mu y)/t, mu ∝ exp(-Phi/2nu), Phi = U0(y) + (x-y)^2/2t, U0 = 1 - cos y
YG = np.linspace(-3.2, 3.2, 64001)  # offset y - x (|x - a| <= t||u0|| = 2)
def u_hc(xs, nu_, t_=tt):
    out = np.empty_like(xs)
    for i0 in range(0, len(xs), 50):
        xb = xs[i0:i0 + 50, None]; y = xb + YG[None, :]
        Phi = (1 - np.cos(y)) + (YG[None, :]) ** 2 / (2 * t_)
        lw = -Phi / (2 * nu_); lw -= lw.max(1, keepdims=True); w = np.exp(lw)
        out[i0:i0 + 50] = (xb[:, 0] - (w * y).sum(1) / w.sum(1)) / t_
    return out
def v_lo(xs, t_=tt):
    out = np.empty_like(xs)
    for i0 in range(0, len(xs), 50):
        xb = xs[i0:i0 + 50, None]; y = xb + YG[None, :]
        Phi = (1 - np.cos(y)) + (YG[None, :]) ** 2 / (2 * t_)
        out[i0:i0 + 50] = (xb[:, 0] - y[np.arange(y.shape[0]), Phi.argmin(1)]) / t_
    return out
ratios = []
for nu_ in (1e-2, 2.5e-3, 6.25e-4):
    sig = np.sqrt(2 * nu_ * tt)
    L = 14 * sig
    xs = np.linspace(np.pi - L, np.pi + L, 1201)
    zq = np.linspace(-7, 7, 1401); wq = np.exp(-zq ** 2 / 2); wq /= wq.sum()
    xg = np.linspace(np.pi - L - 7.5 * sig, np.pi + L + 7.5 * sig, 20001)
    vg = v_lo(xg)
    vv = np.interp((xs[:, None] + sig * zq[None, :]).ravel(), xg, vg).reshape(len(xs), len(zq))
    H = (vv * wq[None, :]).sum(1)
    E = u_hc(xs, nu_) - H
    l1 = np.trapezoid(np.abs(E), xs)
    ratios.append(l1 / np.sqrt(nu_))
    print("   T3(iii) nu=%g: sup|E^mult_AB| (finestra)=%.4f, L1(finestra)/sqrt(nu)=%.4f" % (nu_, np.abs(E).max(), l1 / np.sqrt(nu_)))
target = 2 * Dj * np.sqrt(tt / np.pi)
print("   T3(iii) 2D sqrt(t/pi) = %.4f" % target)
check("T3(iii) numerico: L1/sqrt(nu) crescente e sotto/vicino a 2D sqrt(t/pi) (entro 10%% all'ultimo nu)", ratios[0] < ratios[-1] and abs(ratios[-1] / target - 1) < 0.10)

# ---------- 5. S4T-C1: ad^k e simboli ----------
def adk(P, Q, k):
    out = Q
    for _ in range(k):
        out = sp.expand(Dev(P, out) - Dev(out, P))  # caratteristica di [D_P, D_out]
    return out
ok = all(sp.expand(adk(A, B, k) - (-1) ** (k + 1) * (2 * nu) ** k * U[k] * U[k + 1]) == 0 for k in range(5))
check("C1(c) Burgers: char(ad_X^k Y) = (-1)^{k+1}(2nu)^k u_k u_{k+1}, k<=4", ok)
ok = all(sp.expand(adk(A, Rf, k) - (-r * (-2 * nu) ** k * U[k] ** 2)) == 0 for k in range(1, 5))
check("C1(c) Fisher: Q_k = -r(-2nu)^k u_k^2, k=1..4 (Q_0 != Y: Y ha anche la parte r u)", ok)
# KdVB: simbolo rho^k q_B
x1, x2 = sp.symbols('xi1 xi2')
def sym_quad(Q):
    """simbolo simmetrico di un polinomio quadratico sum c u_i u_j"""
    P = sp.Poly(Q, *U); out = 0
    for mon, cf in P.terms():
        idx = [i for i, e in enumerate(mon) for _ in range(e)]
        i, j = idx
        out += cf * (x1 ** i * x2 ** j + x1 ** j * x2 ** i) / 2
    return sp.expand(out)
AK = nu * U[2] - d * U[3]
rho = x1 * x2 * (3 * d * (x1 + x2) - 2 * nu)
qB = -(x1 + x2) / 2
ok = all(sp.expand(sym_quad(adk(AK, B, k)) - sp.expand(rho ** k * qB)) == 0 for k in range(4))
check("C1(c) KdV–Burgers: simbolo di ad^k = rho^k q_B, k<=3", ok)
# (a) [D_P,D_Q] = D_{D_PQ-D_QP} su test
Pt = U[0] ** 2 * U[1] + U[2]; Qt = U[1] * U[3] - U[0] ** 3; Gt = U[0] * U[2] ** 2 + U[1]
check("C1(a) [D_P,D_Q]G = D_{D_PQ-D_QP}G (test)", sp.expand(Dev(Pt, Dev(Qt, Gt)) - Dev(Qt, Dev(Pt, Gt)) - Dev(sp.expand(Dev(Pt, Qt) - Dev(Qt, Pt)), Gt)) == 0)
# indipendenza lineare (H) per KdVB fino a k=4 (rango)
chars = [AK, B] + [adk(AK, B, k) for k in range(1, 5)]
monos = sorted({m for c in chars for m in sp.Poly(c, nu, d, *U).as_dict().keys()})
# trattiamo nu,d come numeri generici
subsnd = {nu: sp.Rational(3, 7), d: sp.Rational(-5, 11)}
vecs = []
allm = set()
for c in chars:
    allm |= set(sp.Poly(sp.expand(c.subs(subsnd)), *U).as_dict().keys())
allm = sorted(allm)
M = sp.Matrix([[sp.Poly(sp.expand(c.subs(subsnd)), *U).as_dict().get(m, 0) for m in allm] for c in chars])
check("C1(d) KdVB: X, Y, ad^1..ad^4 linearmente indipendenti (nu=3/7, d=-5/11)", M.rank() == len(chars))

# ---------- 6. S4T-T4(iii): delta_d ----------
c_, q2, q3 = sp.symbols('c q2 q3')  # c=u0'(a), q2=u0''(a), q3=u0'''(a)
Jt = 1 + t * c_
dd = (1 / Jt) * (-t * q3 * (1 + Jt) / (2 * Jt ** 2) + t ** 2 * q2 ** 2 * (2 + Jt) / (2 * Jt ** 3))
# d/dt(delta J) = -J v_xxx, v_xxx(t,X) = q3/J^4 - 3 t q2^2/J^5
check("T4(iii) delta_d: d/dt(delta_d J) = -J v_xxx, delta_d(0)=0",
      sp.simplify(sp.diff(dd * Jt, t) + Jt * (q3 / Jt ** 4 - 3 * t * q2 ** 2 / Jt ** 5)) == 0 and sp.simplify(dd.subs(t, 0)) == 0)
# v_xxx lagrangiano: derivata di q2/J^3 rispetto ad a divisa per J (con c'=q2, q2'=q3)
aa_ = sp.symbols('a'); cf_ = sp.Function('c')(aa_)
vxx_l = sp.diff(cf_, aa_) / (1 + t * cf_) ** 3
vxxx_l = sp.diff(vxx_l, aa_) / (1 + t * cf_)
vxxx_l = vxxx_l.subs(sp.diff(cf_, aa_, 2), q3).subs(sp.diff(cf_, aa_), q2).subs(cf_, c_)
check("T4(iii) v_xxx(t,X) = u0'''/J^4 - 3t u0''^2/J^5", sp.simplify(vxxx_l - (q3 / Jt ** 4 - 3 * t * q2 ** 2 / Jt ** 5)) == 0)

# ---------- 7. S4T-P5 Fisher ----------
zz = sp.symbols('zz')
Lf = zz * sp.exp(r * t) / (1 - zz + zz * sp.exp(r * t))
check("P5 L(t,z) risolve L_t = rL(1-L), L(0,z)=z", sp.simplify(sp.diff(Lf, t) - r * Lf * (1 - Lf)) == 0 and sp.simplify(Lf.subs(t, 0) - zz) == 0)
check("P5 d_z L(t,0) = e^{rt}", sp.simplify(sp.diff(Lf, zz).subs(zz, 0) - sp.exp(r * t)) == 0)

# ---------- 8. S4T-P6: ordine eps^2 ----------
k1, k2 = sp.symbols('k1 k2', integer=True, nonzero=True)
def bracket(kl, km):
    Kk = kl + km
    return (sp.exp(-nu * (kl ** 2 + km ** 2) * t) - sp.exp(-nu * Kk ** 2 * t)) / (2 * nu * kl * km) - t
br = sp.series(bracket(k1, k2), t, 0, 4).removeO()
check("P6 bracket = -nu t^2 (k_l^2+k_lk_m+k_m^2) + O(t^3)", sp.simplify(br.coeff(t, 2) + nu * (k1 ** 2 + k1 * k2 + k2 ** 2)) == 0 and sp.simplify(br.coeff(t, 1)) == 0)
# confronto con il getto indipendente (Hopf–Cole) all'ordine eps^2, dato eps(sin x + cos 2x /2)
modes = {1: -sp.I / 2, -1: sp.I / 2, 2: sp.Rational(1, 4), -2: sp.Rational(1, 4)}
E2 = 0
for kl, cl in modes.items():
    for km, cm in modes.items():
        Kk = kl + km
        if Kk == 0:
            continue
        E2 += (-sp.I * Kk / 2) * cl * cm * zv ** Kk * bracket(kl, km)
E2s = sp.series(E2, t, 0, NT + 1).removeO()
ok = all(iszero(sp.expand(E2s).coeff(t, k) - sp.expand(sp.diff(Eadd_s[k], eps, 2).subs(eps, 0) / 2)) for k in range(NT + 1))
check("P6 E^add_[2] (formula) = parte eps^2 del getto Hopf–Cole, t<=4", ok)
# DEVIL-4: u0 = eps sin x
modes1 = {1: -sp.I / 2, -1: sp.I / 2}
E2b = 0
for kl, cl in modes1.items():
    for km, cm in modes1.items():
        if kl + km != 0:
            E2b += (-sp.I * (kl + km) / 2) * cl * cm * sp.exp(sp.I * (kl + km) * x) * bracket(kl, km)
E2b = sp.simplify(sp.expand_complex(E2b))
print("   P6 u0=eps sin x: E^add_[2] =", sp.simplify(E2b))
check("P6 sin: [t^2] = 3/2 nu sin 2x", iszero(sp.series(E2b, t, 0, 3).removeO().coeff(t, 2) - sp.Rational(3, 2) * nu * sp.sin(2 * x)))

print("\nTOTALE: %d/%d OK" % (sum(o for _, o in RES), len(RES)))
