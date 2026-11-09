# S10-OPEN-C rev2: verifiche dei fix dell'audit AUDIT_S10-OPEN-C (C-1 ... C-24).
# Sono solo controlli: le prove della sezione «Recepimento dell'audit (rev2)» sono scritte a mano
# e non si appoggiano su questo calcolo.
import math
import random
import sys

import mpmath as mp
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

res = []


def ok(name, cond):
    res.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)


I = sp.I
t, x, s, y, z = sp.symbols('t x s y z', real=True)
dl, k, a, eps = sp.symbols('delta k a epsilon', real=True)

# ---------------------------------------------------------------------------
# Riduzione delle derivate in t con l'equazione libera i F_t + F_xx = 0, cioè F_t = i F_xx
U = sp.Function('u')(t, x)
P = sp.Function('p')(t, x)


def red_free(e, funcs=(U, P)):
    def is_td(d):
        return isinstance(d, sp.Derivative) and d.expr in funcs and dict(d.variable_count).get(t, 0) > 0

    def rep(d):
        vc = dict(d.variable_count)
        nt, nx = vc.get(t, 0), vc.get(x, 0)
        return I**nt*sp.Derivative(d.expr, (x, nx + 2*nt))

    e = sp.expand(e.doit())
    for _ in range(4):
        e = sp.expand(e.replace(is_td, rep).doit())
    return sp.simplify(e)


# ---------------------------------------------------------------------------
# C-15 (§11). Passo 2: u' = e^{iθ1}u, i u_t = -u_xx + (q0 + c)u, V' = V + δ.
th1 = sp.Function('theta1')(t)
th = sp.Function('theta')(t)
q0 = sp.Function('q0')(x)
cc = sp.Symbol('c', real=True)
V = q0 + cc
up = sp.exp(I*th1)*U
resid = I*sp.diff(up, t) - (-sp.diff(up, x, 2) + (V + dl)*up)
# sostituzione u_t = i u_xx - i V u (equazione di Schrödinger con V)
resid = sp.expand(resid.subs(sp.Derivative(U, t), I*sp.diff(U, x, 2) - I*V*U).doit())
ok("C-15 passo 2: residuo = (-θ1' - δ) e^{iθ1} u",
   sp.simplify(resid - (-sp.diff(th1, t) - dl)*sp.exp(I*th1)*U) == 0)

# Passo 4: w libera, w' = e^{iθ}w libera ⇒ residuo -θ' e^{iθ} w
W = sp.Function('w')(t, x)
wp = sp.exp(I*th)*W
r4 = red_free(I*sp.diff(wp, t) + sp.diff(wp, x, 2), funcs=(W,))
ok("C-15 passo 4: L_0(e^{iθ}w) = -θ' e^{iθ} w per w libera",
   sp.simplify(r4 + sp.diff(th, t)*sp.exp(I*th)*W) == 0)

# Il quoziente u'/u con fase lineare in t non dipende da x (controllo del sollevamento della fase)
uu = (x**2 + 2*I*t)
uup = sp.exp(I*(sp.Rational(3, 2) - 2*t))*uu
ok("C-15 lift: u'/u = e^{i(κ - δ t)} indipendente da x", sp.simplify(sp.diff(uup/uu, x)) == 0)

# ---------------------------------------------------------------------------
# C-17 (§12). Darboux: χ = Λφ = φ_x - (u_x/u)φ, W = uφ_x - u_xφ = uχ.
chi = sp.diff(P, x) - sp.diff(U, x)/U*P
Wr = U*sp.diff(P, x) - sp.diff(U, x)*P
ok("C-17 W = u χ", sp.simplify(Wr - U*chi) == 0)
lhs = red_free(sp.diff(P/U, t))
rhs1 = red_free(I*sp.diff(Wr, x)/U**2)
rhs2 = red_free(I*(sp.diff(chi, x) + sp.diff(U, x)/U*chi)/U)
ok("C-17 ∂_t(φ/u) = i W_x/u^2", sp.simplify(lhs - rhs1) == 0)
ok("C-17 i W_x/u^2 = i(χ_x + (u_x/u)χ)/u", sp.simplify(rhs1 - rhs2) == 0)
aa = sp.Function('a')(t)
La = red_free(I*sp.diff(aa*U, t) + sp.diff(aa*U, x, 2))
ok("C-17 L_0(a(t)u) = i a' u per u libera", sp.simplify(La - I*sp.diff(aa, t)*U) == 0)
# (i) a mano: L_0 χ = V_1 χ con V_1 = -2 ∂_x^2 log u
V1 = -2*sp.diff(sp.log(U), x, 2)
Lchi = red_free(I*sp.diff(chi, t) + sp.diff(chi, x, 2))
ok("C-17 (i) L_0 Λφ = V_1 Λφ (u, φ libere qualsiasi)", sp.simplify(Lchi - red_free(V1*chi)) == 0)
# Λf = u ∂_x(f/u)
F = sp.Function('f')(t, x)
ok("C-17 Λf = u ∂_x(f/u)", sp.simplify(sp.diff(F, x) - sp.diff(U, x)/U*F - U*sp.diff(F/U, x)) == 0)
# esempio: u = x^2 + 2it, χ = Λ(x^3 + 6itx), ψ dalla formula con c' = iκ
u0 = x**2 + 2*I*t
ph0 = x**3 + 6*I*t*x
ok("C-17 esempio: u0 e φ0 libere",
   sp.simplify(I*sp.diff(u0, t) + sp.diff(u0, x, 2)) == 0 and sp.simplify(I*sp.diff(ph0, t) + sp.diff(ph0, x, 2)) == 0)
chi0 = sp.simplify(sp.diff(ph0, x) - sp.diff(u0, x)/u0*ph0)
x0 = sp.Integer(1)
kap = sp.simplify(((sp.diff(chi0, x) + sp.diff(u0, x)/u0*chi0)/u0).subs(x, x0))
cfun = sp.integrate(I*kap, (t, 0, t))
xs = sp.Symbol('xs', positive=True)
psi = u0*(sp.integrate((chi0/u0).subs(x, xs), (xs, x0, x)) + cfun)
ok("C-17 esempio: ψ libera", sp.simplify(I*sp.diff(psi, t) + sp.diff(psi, x, 2)) == 0)
ok("C-17 esempio: Λψ = χ", sp.simplify(sp.diff(psi, x) - sp.diff(u0, x)/u0*psi - chi0) == 0)
ok("C-17 esempio: ψ - φ0 ∈ ℂ u0", sp.simplify(sp.diff((psi - ph0)/u0, x)) == 0 and
   sp.simplify(sp.diff((psi - ph0)/u0, t)) == 0)

# ---------------------------------------------------------------------------
# C-18: boost di Galileo, esempio reale dipendente da t
uG = (x - 2*k*t + a)*sp.exp(I*(k*x - k**2*t))
ok("C-18 u_G libera", sp.simplify(I*sp.diff(uG, t) + sp.diff(uG, x, 2)) == 0)
V1G = sp.simplify(-2*(sp.diff(uG, x, 2)/uG - (sp.diff(uG, x)/uG)**2))
ok("C-18 V_1 = 2/(x - 2kt + a)^2 (reale, dipende da t)", sp.simplify(V1G - 2/(x - 2*k*t + a)**2) == 0)

# ---------------------------------------------------------------------------
# C-19 (§13): lemma del cono, controllo numerico in N = 2 e N = 3
random.seed(1)


def phi2(yp):  # Lipschitz con costante ≤ 1.5
    return 0.5*abs(math.sin(3*yp)) - 0.2*yp


Lc = 1.5 + 0.2
good = True
for _ in range(20000):
    xp = random.uniform(-1, 1)
    xn = phi2(xp) + random.uniform(1e-9, 0.5)
    r = random.uniform(0, 1)
    ang = random.uniform(-math.atan(1/Lc), math.atan(1/Lc))
    zp, zn = r*math.sin(ang), r*math.cos(ang)
    if zn > Lc*abs(zp):
        good &= (xn + zn > phi2(xp + zp))
ok("C-19 cono x + {z_N > L|z'|} sopra il grafico (N = 2, 20000 campioni)", good)


def phi3(y1, y2):  # Lipschitz con costante ≤ 1 (norma euclidea): |∇| ≤ sqrt(0.5^2+0.5^2) < 1
    return 0.5*math.sin(y1) + 0.5*abs(y2)


L3 = 1.0
good = True
for _ in range(20000):
    x1, x2 = random.uniform(-1, 1), random.uniform(-1, 1)
    xn = phi3(x1, x2) + random.uniform(1e-9, 0.3)
    z1, z2 = random.uniform(-1, 1), random.uniform(-1, 1)
    zn = L3*math.hypot(z1, z2) + random.uniform(1e-9, 1)
    good &= (xn + zn > phi3(x1 + z1, x2 + z2))
ok("C-19 cono sopra il grafico (N = 3, 20000 campioni)", good)
Ls, rr = sp.symbols('L r', positive=True)
rho, ang = sp.symbols('rho alpha', positive=True)
area = sp.integrate(sp.integrate(rho, (rho, 0, rr)), (ang, -sp.atan(1/Ls), sp.atan(1/Ls)))
ok("C-19 |Γ(L, r)| = r^N |Γ(L, 1)| (N = 2: r^2 arctan(1/L))", sp.simplify(area - rr**2*sp.atan(1/Ls)) == 0)
# convessità: combinazione convessa di due punti del cono resta nel cono (N = 2)
good = True
for _ in range(5000):
    pts = []
    while len(pts) < 2:
        zp, zn = random.uniform(-1, 1), random.uniform(0, 1)
        if zn > Lc*abs(zp) and zp*zp + zn*zn < 1:
            pts.append((zp, zn))
    lam = random.random()
    mpp = (lam*pts[0][0] + (1 - lam)*pts[1][0], lam*pts[0][1] + (1 - lam)*pts[1][1])
    good &= (mpp[1] > Lc*abs(mpp[0]) and mpp[0]**2 + mpp[1]**2 < 1)
ok("C-19 Γ(L, h) convesso (5000 campioni)", good)

# ---------------------------------------------------------------------------
# C-1 (§1): Lemma C in dimensione 1 (A_0 = α scalare), derivata e dominio
al = sp.Symbol('alpha', positive=True)   # positivo per evitare i rami Piecewise di α = 0
r_ = sp.Symbol('r', real=True)
fr = sp.cos(3*r_) + r_**2
Fc = sp.integrate(sp.exp(al*(t - r_))*fr, (r_, 0, t))
Fp = sp.exp(al*t)*fr.subs(r_, 0) + sp.integrate(sp.exp(al*(t - r_))*sp.diff(fr, r_), (r_, 0, t))
ok("C-1 Lemma C: F' = T(t)f(0) + ∫T(t-r)f'(r)dr", sp.simplify(sp.diff(Fc, t) - Fp) == 0)
ok("C-1 Lemma C: A_0 F = F' - f", sp.simplify(al*Fc - (Fp - fr.subs(r_, t))) == 0)
# classica ⇒ mite: d/dr [T(t-r)v(r)] = T(t-r)(v' - A_0 v)
vf = sp.Function('v')(r_)
ok("C-1 d/dr[T(t-r)v(r)] = T(t-r)(v'(r) - A_0 v(r))",
   sp.simplify(sp.diff(sp.exp(al*(t - r_))*vf, r_) - sp.exp(al*(t - r_))*(sp.diff(vf, r_) - al*vf)) == 0)

# C-5 (§4): termine di bordo  A_0 ∫_0^b k T y = k(b)T(b)y - k(0)y - ∫_0^b k' T y
bb = sp.Symbol('b', positive=True)
sg = sp.Symbol('sigma', real=True)
kk = 2 - sg + sg**3
lhs5 = al*sp.integrate(kk*sp.exp(al*sg), (sg, 0, bb))
rhs5 = kk.subs(sg, bb)*sp.exp(al*bb) - kk.subs(sg, 0) - sp.integrate(sp.diff(kk, sg)*sp.exp(al*sg), (sg, 0, bb))
ok("C-5 formula con termine di bordo -k(0)y", sp.simplify(lhs5 - rhs5) == 0)

# ---------------------------------------------------------------------------
# C-7 (§5): monodromia e regolarizzazione


def seg(om, tau):
    th_ = 2*om*tau
    return [[math.cos(th_), math.sin(th_)/om], [-om*math.sin(th_), math.cos(th_)]]


def mul(A, B):
    return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]


w1, w2 = 1.0, 5.0
tau1 = math.pi/(4*w1)
tau2 = math.pi/(4*w1)   # τ2 = τ1, come nell'enunciato
Mq = mul(seg(w2, tau2), seg(w1, tau1))
ok("C-7 M = M2 M1 = diag(-1/5, -5)",
   abs(Mq[0][0] + 0.2) < 1e-12 and abs(Mq[1][1] + 5) < 1e-12 and abs(Mq[0][1]) < 1e-12 and abs(Mq[1][0]) < 1e-12)
Tt = tau1 + tau2


def tr_reg(width, nst=40000):
    Mx = [[1.0, 0.0], [0.0, 1.0]]
    dt = Tt/nst
    for j in range(nst):
        tm = (j + 0.5)*dt
        om = w1 + (w2 - w1)*(math.tanh((tm - tau1)/width) + 1)/2
        Mx = mul(seg(om, dt), Mx)
    return Mx[0][0] + Mx[1][1]


trs = [tr_reg(wd) for wd in (0.05, 0.02, 0.005)]
print("    tracce regolarizzate:", [round(v, 4) for v in trs])
ok("C-7 regolarizzazioni lisce di ω: tr < -2 e → -26/5", all(v < -2 for v in trs) and abs(trs[-1] + 5.2) < 0.05)

# ---------------------------------------------------------------------------
# C-8 (§6): polinomi di Touchard
Z = sp.Symbol('Z')
fy = sp.exp(sp.exp(y))
Tk = sp.Integer(1)
good = True
for kk_ in range(0, 11):
    if kk_ > 0:
        Tk = sp.expand(Z*(Tk + sp.diff(Tk, Z)))
    q = sp.simplify(sp.diff(fy, y, kk_)/fy - Tk.subs(Z, sp.exp(y)))
    pol = sp.Poly(Tk, Z)
    good &= (q == 0 and pol.degree() == kk_ and pol.LC() == 1)
ok("C-8 f^{(k)} = f·T_k(e^y), T_k monico di grado k (k ≤ 10)", good)
uu8 = fy.subs(y, x + t)
ok("C-8 (∂_t - ∂_x)u = 0", sp.simplify(sp.diff(uu8, t) - sp.diff(uu8, x)) == 0)

# ---------------------------------------------------------------------------
# C-10 (§7): maggiorazione corretta nel Lemma E
mp.mp.dps = 20
good = True
for Q, dQ in [(lambda v: v**2, lambda v: 2*v), (lambda v: v**3 + v, lambda v: 3*v**2 + 1), (lambda v: 3*v, lambda v: 3)]:
    for X in (2, 5, 9):
        val = abs(mp.quad(lambda v: mp.expj(Q(v)), mp.linspace(X, 2*X, 400)))
        bnd = 1/abs(dQ(X)) + 1/abs(dQ(2*X)) + abs(mp.mpf(1)/dQ(2*X) - mp.mpf(1)/dQ(X))
        good &= val <= bnd + 1e-12
ok("C-10 |∫_X^{2X} e^{iQ}| ≤ 1/|Q'(X)| + 1/|Q'(2X)| + |1/Q'(2X) - 1/Q'(X)|", good)

# ---------------------------------------------------------------------------
# C-11, C-12 (§8)
xi, tau = sp.symbols('xi tau')
A1 = sp.Matrix([[xi, 0, 0], [0, -xi, 1], [0, 0, -2*xi]])
A2 = sp.Matrix([[xi, 1, 0], [0, -xi, 0], [0, 0, -2*xi]])
S = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])   # S e1 = e2, S e2 = e3, S e3 = e1
ok("C-12 S e1 = e2, S e2 = e3, S e3 = e1",
   S*sp.Matrix([1, 0, 0]) == sp.Matrix([0, 1, 0]) and S*sp.Matrix([0, 1, 0]) == sp.Matrix([0, 0, 1]))
A2p = S*A2*S.inv()
ok("C-12 A2'(0) = A1(0) come matrici", A2p.subs(xi, 0) == A1.subs(xi, 0))
ok("C-12 stesso polinomio caratteristico",
   sp.expand((tau*sp.eye(3) - A2p).det() - (tau*sp.eye(3) - A1).det()) == 0)


def proj(A):
    return sp.simplify((A + xi*sp.eye(3))*(A + 2*xi*sp.eye(3))/(6*xi**2))


P1, P2p = proj(A1), proj(A2p)
ok("C-12 P(A1) = diag(1,0,0), nessun polo", P1 == sp.diag(1, 0, 0))
ok("C-12 P(A2') ha un elemento 1/(2ξ) (polo)", any(sp.simplify(e - 1/(2*xi)) == 0 for e in P2p))
ok("C-12 P(A2') idempotente e commuta con A2'",
   sp.simplify(P2p*P2p - P2p) == sp.zeros(3) and sp.simplify(P2p*A2p - A2p*P2p) == sp.zeros(3))
# C-11 basi saturate per A2: F = ker B(A2), saturazione nel DVR in 0
Bm = (A2 + xi*sp.eye(3))*(A2 + 2*xi*sp.eye(3))
Em = (A2 - xi*sp.eye(3))
Fb = Bm.nullspace()
Eb = Em.nullspace()


def saturate(vs):
    out = []
    for v in vs:
        v = sp.simplify(v*sp.lcm([sp.fraction(sp.together(e))[1] for e in v]))
        while all(sp.simplify(e.subs(xi, 0)) == 0 for e in v):
            v = sp.simplify(v/xi)
        out.append(v)
    return sp.Matrix.hstack(*out)


Fs, Es = saturate(Fb), saturate(Eb)
ok("C-11 basi saturate: e(0), f(0) di rango pieno", Fs.subs(xi, 0).rank() == Fs.shape[1] and Es.subs(xi, 0).rank() == Es.shape[1])
ok("C-11 det[e f](0) = 0 per A2 (polo)", sp.simplify(sp.Matrix.hstack(Es, Fs).det().subs(xi, 0)) == 0)

# ---------------------------------------------------------------------------
# C-20 (§14): polinomio nodale di Čebyšëv e resto di Lagrange
good = True
for J in range(3, 10):
    Lam = 4.0
    nodes = [Lam/2*(1 + math.cos((2*j - 1)*math.pi/(2*J))) for j in range(1, J + 1)]
    mx = max(abs(math.prod(lv - nd for nd in nodes)) for lv in [Lam*i/4000 for i in range(4001)])
    good &= abs(mx - 2*(Lam/4)**J) < 1e-9*(Lam/4)**J + 1e-12
ok("C-20 max|Π(λ - λ_j)| = 2(Λ/4)^J (J = 3..9)", good)
good = True
for (Lam, T_, J) in [(4.0, 1.0, 6), (10.0, 0.7, 8), (3.0, 2.0, 5)]:
    nodes = [Lam/2*(1 + math.cos((2*j - 1)*math.pi/(2*J))) for j in range(1, J + 1)]
    for tt in (T_/3, T_):
        vals = [math.exp(-nd*tt) for nd in nodes]

        def pint(lv):
            sm = 0.0
            for i, ni in enumerate(nodes):
                li = 1.0
                for jx, nj in enumerate(nodes):
                    if jx != i:
                        li *= (lv - nj)/(ni - nj)
                sm += vals[i]*li
            return sm
        err = max(abs(math.exp(-lv*tt) - pint(lv)) for lv in [Lam*i/2000 for i in range(2001)])
        good &= err <= 2*(Lam*T_/4)**J/math.factorial(J)*(1 + 1e-9)
ok("C-20 errore di interpolazione ≤ 2(ΛT/4)^J/J!", good)
good = all((math.e*Lm/(4*J))**J <= math.exp(-J) * (1 + 1e-12) for Lm in (1.0, 3.0) for J in range(max(1, math.ceil(math.e**2*Lm/4)), 60))
ok("C-20 (eΛT/(4J))^J ≤ e^{-J} per J ≥ e^2ΛT/4 (T = 1)", good)

# ---------------------------------------------------------------------------
# C-24 (§17)
c0 = sp.Symbol('c0', positive=True)
ph = sp.Function('varphi')
x0s = sp.Symbol('x0', real=True)
ep = sp.Symbol('epsilon', positive=True)
h = ep*ph((x - x0s)/ep**sp.Rational(1, 3))
u2 = c0 + h
Vd = (sp.diff(u2, x, 2))/u2   # V_{u2} - V_{u1}, u1 = c0 costante (u_t = 0)
Vd0 = sp.simplify(Vd.subs(x, x0s).doit().subs(ph(0), 0))
ok("C-24 V_{u2} - V_{u1} in x0 = ε^{1/3}φ''(0)/u1",
   sp.simplify(Vd0 - ep**sp.Rational(1, 3)*sp.Subs(sp.Derivative(ph(z), (z, 2)), z, 0)/c0) == 0)
Mv, d0 = 3.0, 1.0
yy = sp.Symbol('yy', real=True)
phi0 = yy**2*sp.exp(1 - 1/(1 - yy**2))
ders = [sp.lambdify(yy, sp.diff(phi0, yy, j), 'math') for j in range(4)]
grid = [-1 + 2*i/4000 for i in range(1, 4000)]
mxd = max(max(abs(dj(v)) for v in grid) for dj in ders)
cs = min(1.0, (Mv - d0)/2)/mxd
u1 = (Mv + d0)/2
eps0 = (Mv - d0)/4
good = True
for e_ in (eps0, eps0/10, eps0/1000):
    for v in grid[::7]:
        hval = e_*cs*ders[0](v)
        good &= (d0 <= abs(u1 + hval) <= Mv)
        for j in (1, 2, 3):
            good &= abs(e_**(1 - j/3)*cs*ders[j](v)) <= Mv
ok("C-24 u2 = (M+δ0)/2 + h ∈ 𝒰(M, δ0) per ε ≤ (M-δ0)/4 (M = 3, δ0 = 1)", good)
ok("C-24 φ''(0) ≠ 0 e φ(0) = 0 per la bump scelta", abs(ders[2](0.0)) > 0 and ders[0](0.0) == 0)

# ---------------------------------------------------------------------------
# C-23 (§16): esistenza di test duali, esempio finito (funzionali indipendenti ⇒ matrice invertibile)
xv = sp.Symbol('xv')
dists = [lambda f: sp.integrate(f, (xv, 0, 1)), lambda f: sp.integrate(xv*f, (xv, 0, 1)), lambda f: f.subs(xv, sp.Rational(1, 2))]
tests = [sp.Integer(1), xv, xv**2]
Mt = sp.Matrix(3, 3, lambda i, j: dists[i](tests[j]))
ok("C-23 tre distribuzioni indipendenti: det(⟨D_i, φ_j⟩) ≠ 0 su test polinomiali", Mt.det() != 0)

nok = sum(1 for _, c in res if c)
print(f"\nTotale: {nok}/{len(res)} OK")
sys.exit(0 if nok == len(res) else 1)
