# audit_opfun.py -- S-CHECK-14, red team indipendente sui claim OP-FUN (scritto da zero)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_opfun.py > audit_opfun.out
import itertools, math, cmath, random
import sympy as sp
from sympy import I, Rational as Q

RES = []
def check(name, cond, info=""):
    RES.append((name, bool(cond)))
    print(("[OK]  " if cond else "[FAIL]") + " " + name + ((" -- " + str(info)) if info != "" else ""))

t, x, tau, xi, s, lam, zeta = sp.symbols('t x tau xi s lambda zeta')

# ---------------- OPF-T1: r in (Q_j,B_j) cap C[xi], sigma in (Q_j,B_j) cap C[tau] ----------------
def elim(f, g):
    Gx = sp.groebner([f, g], tau, xi, order='lex')      # elimina tau -> ultimo elemento in C[xi]
    Gt = sp.groebner([f, g], xi, tau, order='lex')      # elimina xi  -> ultimo elemento in C[tau]
    rx = [p for p in Gx.exprs if not p.has(tau)]
    st = [p for p in Gt.exprs if not p.has(xi)]
    return rx, st
cases = {
 'trave (tau-i xi^2, tau+i xi^2)': (tau - I*xi**2, tau + I*xi**2),
 'calore x trasporto': (tau - xi**2, tau + xi),
 'non monico xi tau-1 vs tau-xi': (xi*tau - 1, tau - xi),
 'molteplicita (tau-xi)^2 vs tau+xi': ((tau - xi)**2, tau + xi),
 'grado 2 KG tau^2-xi^2-1 vs tau': (tau**2 - xi**2 - 1, tau),
 'non monico xi^2 tau-(1+xi) vs (tau-1)^3': (xi**2*tau - (1 + xi), (tau - 1)**3),
}
for nm, (f, g) in cases.items():
    rx, st = elim(f, g)
    check("T1 ideale contiene r(xi)!=0 e sigma(tau)!=0: " + nm, len(rx) > 0 and len(st) > 0 and all(p != 0 for p in rx + st),
          "r=%s ; sigma=%s" % (sp.factor(rx[-1]), sp.factor(st[-1])))
# certificati espliciti dichiarati nel package
f, g = tau - xi**2, tau + xi
check("T1 certificato calore x trasporto: xi+xi^2 = g-f", sp.expand(g - f - (xi + xi**2)) == 0)
check("T1 certificato: tau-tau^2 = f-(tau-xi) g", sp.expand(f - (tau - xi)*g - (tau - tau**2)) == 0)
f, g = tau - I*xi**2, tau + I*xi**2
check("T1 certificato trave: xi^2=(g-f)/(2i), tau=(f+g)/2", sp.expand((g - f)/(2*I) - xi**2) == 0 and sp.expand((f + g)/2 - tau) == 0)

# ---------------- OPF-L1 passo 3: primitiva di Volterra in t con dato indipendente da x ----------------
gam = sp.Function('gamma')
# sigma = tau^2 + 1: G_sigma(t) = sin t; w = int_{t*}^t sin(t-t') gamma(t') dt'
tp = sp.symbols('tp')
w = sp.Integral(sp.sin(t - tp)*sp.exp(2*tp), (tp, 0, t)).doit()
check("L1 passo 3: sigma(d_t)w = gamma (sigma=tau^2+1, gamma=e^{2t}) e w non dipende da x",
      sp.simplify(sp.diff(w, t, 2) + w - sp.exp(2*t)) == 0 and not w.has(x))
# stima EP: ||(t^l e^{mu t})^{(i)}|| <= C eta^i per eta>|mu|  (controllo numerico del rapporto)
mu = Q(3, 2); l = 3
vals = []
for i in [10, 20, 40, 80]:
    d = sp.diff(t**l*sp.exp(mu*t), t, i)
    vals.append(float(sp.Abs(d.subs(t, 1)))/float(2)**i)
check("L1 passo 3: derivate di t^3 e^{1.5t} crescono come eta^i con eta=2 (rapporto decrescente)", vals[-1] < vals[0], vals)

# ---------------- OPF-T2: Jordan e=3, formula sui sottoinsiemi ----------------
f0, f1, f2 = sp.symbols('f0 f1 f2')
a = zeta**2 + 3*zeta
u = sp.exp(t*a)*(f0 + t*f1 + t**2/2*f2)*sp.exp(zeta*x)
def L(v):  # (d_t - a(d_x)) su funzioni in e^{zeta x}: a(d_x) = d_x^2 + 3 d_x
    return sp.diff(v, t) - (sp.diff(v, x, 2) + 3*sp.diff(v, x))
check("T2 (d_t-a)^3 u = 0 per u = e^{ta}(f0+tf1+t^2f2/2)e^{zeta x}", sp.simplify(L(L(L(u)))) == 0)
check("T2 (d_t-a)^2 u != 0", sp.simplify(L(L(u))) != 0)
a1, a2 = sp.symbols('a1 a2')
Ne = sp.Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
Ts = [a1*sp.eye(3), a2*sp.eye(3), Ne]
def ex(M): return sp.simplify((s*M).exp())
F = sp.Matrix([f0, f1, f2])
Uexp = ex(sum(Ts, sp.zeros(3)))*F
lhs = Uexp - F - sum(((ex(T) - sp.eye(3))*F for T in Ts), sp.zeros(3, 1))
rhs = sp.zeros(3, 1)
for k in [2, 3]:
    for S in itertools.combinations(range(3), k):
        M = sp.eye(3)
        for n in S: M = M*(ex(Ts[n]) - sp.eye(3))
        rhs += M*F
check("T2 E^add = somma su |S|>=2 (termini a1 I, a2 I, N_3)", sp.simplify(lhs - rhs) == sp.zeros(3, 1))
check("T2 E^mult = 0 (prodotto dei flussi = flusso totale)", sp.simplify(ex(Ts[0])*ex(Ts[1])*ex(Ts[2]) - ex(sum(Ts, sp.zeros(3)))) == sp.zeros(3))
check("T2 componente 0: u(t)=e^{sa}(f0+s f1+s^2/2 f2)", sp.simplify(Uexp[0] - sp.exp(s*(a1 + a2))*(f0 + s*f1 + s**2/2*f2)) == 0)

# ---------------- OPF-P3: coefficiente di s^2 dell'errore di splitting ----------------
def E(i, j, k):
    M = sp.zeros(k); M[i-1, j-1] = 1; return M
def s2coef(Tlist, order):
    k = Tlist[0].shape[0]
    tot = sum(Tlist, sp.zeros(k))
    full = sp.eye(k) + s*tot + s**2/2*tot**2
    prod = sp.eye(k)
    for o in order:
        T = Tlist[o]; prod = prod*(sp.eye(k) + s*T + s**2/2*T**2)
    d = sp.expand(full - prod)
    return d.applyfunc(lambda e: sp.expand(e).coeff(s, 2))
def companion_terms(k, terms):  # terms: list of (l, coeff)
    N0 = sum((E(i, i+1, k) for i in range(1, k)), sp.zeros(k))
    Ts = [N0] + [-c*E(k, l+1, k) for (l, c) in terms]
    return Ts
# k=2, KG: c0 = -xi^2 + m^2 (due termini), telegrafo c1 = b, c0 = -xi^2
m2, b = sp.symbols('m2 b')
okall = True; info = []
for nm, k, terms in [('KG', 2, [(0, -xi**2), (0, m2)]), ('telegrafo', 2, [(1, b), (0, -xi**2), (0, m2)]),
                     ('k=3', 3, [(0, xi**3), (1, xi), (0, 5), (2, xi**2)])]:
    Ts = companion_terms(k, terms)
    for order in itertools.permutations(range(len(Ts))):
        C2 = s2coef(Ts, order)
        pos = {o: i for i, o in enumerate(order)}
        eps = sum(((1 if pos[0] < pos[n+1] else -1)*c for n, (l, c) in enumerate(terms) if l == 0), 0)
        if sp.expand(C2[k-2, 0] - eps/2) != 0 or sp.expand(eps) == 0:
            okall = False; info.append((nm, order))
check("P3 entrata (k-1,1) del coeff. s^2 = (1/2) sum eps_n c_{0,n} != 0, tutti gli ordinamenti (KG, telegrafo, k=3)", okall, info)
# red team: termini NON monomiali distinti (c0 = 2 xi scritto xi + xi): esiste un ordinamento con entrata (k-1,1) nulla
Ts = companion_terms(2, [(0, xi), (0, xi)])
zero_entry = []; still_nonzero = []
for order in itertools.permutations(range(3)):
    C2 = s2coef(Ts, order)
    if sp.expand(C2[0, 0]) == 0:
        zero_entry.append(order); still_nonzero.append(C2 != sp.zeros(2))
check("P3 red team: con termini ripetuti (xi+xi) l'entrata (k-1,1) puo' annullarsi (ipotesi 'monomi distinti' usata davvero)",
      len(zero_entry) > 0, "ordinamenti=%s; coeff s^2 comunque !=0: %s" % (zero_entry, still_nonzero))
# commutatore esplicito [N0, E_{k,b}] = E_{k-1,b} - E_{k,b+1}
k = 3
N0 = E(1, 2, 3) + E(2, 3, 3)
check("P3 [N0,E_{k,1}] = E_{k-1,1} - E_{k,2} (k=3)", N0*E(3, 1, 3) - E(3, 1, 3)*N0 == E(2, 1, 3) - E(3, 2, 3))
# potenza: Q^2 con Q = tau^2 - xi (c0 di Q^2 = xi^2 != 0): stesso argomento
Qp = sp.expand((tau**2 - xi)**2)
check("C1/P3 per potenze: tau non divide Q^e (c0 = xi^2)", sp.Poly(Qp, tau).coeff_monomial(1) == xi**2)

# ---------------- OPF-P4 ----------------
N = 12
v = sum(x**n*t**(n+1)/(sp.factorial(n)*sp.factorial(n+1)) for n in range(N))
resid = sp.expand(sp.diff(v, x, t) - v)
check("P4(a) serie di Bessel: (d_x d_t - 1)v = O(troncamento), v(0,x)=0, d_t v(0,x)=1",
      all(sp.Poly(resid, x, t).degree(x) >= N-1 for _ in [0]) and v.subs(t, 0) == 0 and sp.diff(v, t).subs(t, 0) == 1)
# confronto numerico con l'integrale di contorno
def contour(tt, xx, z0=0.0, eps=1.0, M=4000, afun=lambda z: 1/z):
    acc = 0
    for kk in range(M):
        th = 2*math.pi*kk/M
        z = z0 + eps*cmath.exp(1j*th)
        acc += cmath.exp(z*xx + afun(z)*tt)*1j*eps*cmath.exp(1j*th)*(2*math.pi/M)
    return acc/(2j*math.pi)
val = contour(0.7, 0.4)
ser = float(sum(Q(4, 10)**n*Q(7, 10)**(n+1)/(sp.factorial(n)*sp.factorial(n+1)) for n in range(30)))
check("P4(a) integrale di contorno = serie (t=0.7,x=0.4)", abs(val - ser) < 1e-10, (val, ser))
# molteplicita mu=2: p1 = xi^2, p0 = 1 + xi : a = (1+z)/z^2, residuo di a e^{zx} in 0 = x + 1 (coeff x^{mu-1} != 0)
res = sp.residue((1 + zeta)/zeta**2*sp.exp(zeta*x), zeta, 0)
check("P4(a) mu=2: d_t v(t0,.) = Res(a e^{zeta x}) = 1 + x (polinomio non nullo, grado mu-1)", sp.expand(res - (1 + x)) == 0)
v2 = contour(0.0, 0.3, afun=lambda z: (1+z)/z**2)
check("P4(a) mu=2: v(t0,x)=0 numerico", abs(v2) < 1e-12, v2)
# classe K_K: EP con esponente in K appartiene a ker Q (Dirac) e la formula e^{sa}(d_x)
z0 = sp.Integer(3)
uK = sp.exp(z0*x + (1/z0)*t)
check("P4(b) K_K non vuota: e^{3x + t/3} in ker(d_x d_t - 1)", sp.simplify(sp.diff(uK, x, t) - uK) == 0)
# Runge esplicito: 1/zeta su |zeta-3|<=1 approssimata da polinomi (serie geometrica in (3-zeta)/3)
errs = []
for n in [5, 10, 20]:
    pn = sum((3 - zeta)**kk/3**(kk+1) for kk in range(n))
    e = max(abs(complex((1/zeta - pn).subs(zeta, 3 + cmath.exp(1j*th)))) for th in [2*math.pi*j/50 for j in range(50)])
    errs.append(e)
check("P4(b) Runge esplicito: errore uniforme su |zeta-3|=1 decresce", errs[0] > errs[1] > errs[2] and errs[2] < 1e-3, errs)

# ---------------- OPF-T5 / corollari / kill-argument ----------------
wf = sp.Function('w')
for nm, P, A, kap in [('trave', lambda T, X: T**2 + X**4, sp.diag(lam**2, lam), lam**4),
                      ('onda', lambda T, X: T**2 - 4*X**2, sp.diag(lam, lam), lam**2),
                      ('tau xi', lambda T, X: T*X, sp.diag(lam, lam), lam**2)]:
    z = sp.Matrix([tau, xi]); Az = A.T*z
    check("T5 (S) P(A^T z) = kappa P(z): " + nm, sp.expand(P(Az[0], Az[1]) - kap*P(tau, xi)) == 0)
# identita' P(d)(w o Phi) = kappa (P(d) w) o Phi con w generica (trave, Phi(y) = o + A(y-o))
o1, o2 = sp.symbols('o1 o2')
Ph = (o1 + lam**2*(t - o1), o2 + lam*(x - o2))
T_, X_ = sp.symbols('T_ X_')
W = wf(T_, X_)
comp = W.subs({T_: Ph[0], X_: Ph[1]})
lhs = sp.diff(comp, t, 2) + sp.diff(comp, x, 4)
rhs = lam**4*(sp.diff(W, T_, 2) + sp.diff(W, X_, 4)).subs({T_: Ph[0], X_: Ph[1]})
check("T5 identita' di catena per la trave con w generica", sp.simplify(lhs - rhs) == 0)
# (C) sul rettangolo per pesi diversi
random.seed(1)
ok = True
for _ in range(2000):
    L1, L2 = random.uniform(0.1, 3), random.uniform(0.1, 3)
    oo = (random.uniform(0, L1), random.uniform(0, L2)); l = random.uniform(0.5, 0.999)
    for (yt, yx) in [(0, 0), (L1, 0), (0, L2), (L1, L2)]:
        pt = oo[0] + l**2*(yt - oo[0]); px = oo[1] + l*(yx - oo[1])
        if not (0 < pt < L1 and 0 < px < L2): ok = False
check("T5 corollario (b): (C) vale sui rettangoli con o interno (2000 casi casuali)", ok)
# kill-argument T5: trave sul parallelogramma {0<t<Lp, t<x<t+1}: (C) per la famiglia diag(l^2,l) e qualche centro o?
def para_ok(Lp, l, o):
    V = [(0, 0), (0, 1), (Lp, Lp), (Lp, Lp + 1)]
    for (yt, yx) in V:
        pt = o[0] + l**2*(yt - o[0]); px = o[1] + l*(yx - o[1])
        if not (0 < pt < Lp and pt < px < pt + 1): return False
    return True
def exists_o(Lp, l, n=120):
    for i in range(1, n):
        for j in range(1, n):
            ot = Lp*i/n; ox = ot + j/n
            if para_ok(Lp, l, (ot, ox)): return True
    return False
check("KA-T5 (attacco verificato): trave su parallelogramma L=2, nessun centro o soddisfa (C) per lambda=0.99",
      not exists_o(2.0, 0.99), "")
check("KA-T5 controllo: L=0.5, esiste o con (C) (lambda=0.99)", exists_o(0.5, 0.99))
# onda (omogeneo) sullo stesso parallelogramma: (C) vale con A = l I, o interno
check("T5 corollario (a): onda su parallelogramma L=2, (C) con A=lI", all(
    (lambda p: 0 < p[0] < 2 and p[0] < p[1] < p[0] + 1)((1 + 0.99*(yt - 1), 1.5 + 0.99*(yx - 1.5)))
    for (yt, yx) in [(0, 0), (0, 1), (2, 2), (2, 3)]))

# ---------------- OPF-P5 ----------------
tt_, ss_ = sp.symbols('tt ss', real=True)
l_ = sp.symbols('l', positive=True)
# t < s < t+1, 0<t<1  ==>  t < 1 + l(s-1) < t+1  per 0<l<1
ok = True
for _ in range(20000):
    T0 = random.uniform(1e-6, 1 - 1e-6); S0 = random.uniform(T0, T0 + 1); lv = random.uniform(1e-3, 1 - 1e-3)
    sv = 1 + lv*(S0 - 1)
    if not (T0 < sv < T0 + 1): ok = False
check("P5 Psi_lambda manda Omega' in se' (20000 punti)", ok)
check("P5 diseguaglianza 1+l(t-1) >= t  <=>  (1-t)(1-l) >= 0", sp.expand((1 + l_*(tt_ - 1) - tt_) - (1 - tt_)*(1 - l_)) == 0)
# corde annidate per rettangolo (0,T)x(0,Lr), d_t + c d_x, s = x - c t, c>0: annidate verso s* in [0, Lr - cT] sse Lr >= cT
def chord(sv, T, Lr, c):
    lo = max(0.0, -sv/c); hi = min(T, (Lr - sv)/c); return lo, hi
def nested(T, Lr, c, sstar, n=400):
    S = (-c*T, Lr)
    for i in range(1, n):
        s1 = S[0] + (S[1] - S[0])*i/n
        for lv in [0.3, 0.7, 0.95]:
            s2 = sstar + lv*(s1 - sstar)
            a1_, b1_ = chord(s1, T, Lr, c); a2_, b2_ = chord(s2, T, Lr, c)
            if not (a2_ <= a1_ + 1e-12 and b2_ >= b1_ - 1e-12): return False
    return True
check("P5 estensione: rettangolo T=1, L=2, c=1 (L>=cT): corde annidate verso s*=0.5", nested(1, 2, 1, 0.5))
check("P5 estensione: rettangolo T=1, L=0.5, c=1 (L<cT): nessun s* annidato",
      not any(nested(1, 0.5, 1, ss) for ss in [-0.9 + 0.1*k for k in range(15)]))

# ---------------- OPF-O1 ----------------
p, q, r, uu, k1, k2, A1, A2 = sp.symbols('p q r u k1 k2 A1 A2')
# simmetrie affini (con eventuale peso esponenziale e^{a.y}): d_t -> p tau + q xi + A1, d_x -> r tau + u xi + A2
heat = (p*tau + q*xi + A1) - (r*tau + uu*xi + A2)**2 - k1*(tau - xi**2)
tran = (p*tau + q*xi + A1) + (r*tau + uu*xi + A2) - k2*(tau + xi)
eqs = sp.Poly(heat, tau, xi).coeffs() + sp.Poly(tran, tau, xi).coeffs()
sols = sp.solve(eqs, [p, q, r, uu, k1, k2, A1, A2], dict=True)
sols = [so for so in sols if so.get(uu, uu) != 0 and so.get(p, p) != 0]
check("O1 senza peso (A1=A2=0): solo A=I", all(not (so.get(A1, A1) == 0 and so.get(A2, A2) == 0) or (so.get(p) == 1 and so.get(uu) == 1 and so.get(q) == 0 and so.get(r) == 0) for so in sols), sols)
check("O1 con peso esponenziale (obiezione KA): soluzioni = identita' + un'involuzione, nessuna famiglia -> id diversa dall'id",
      len(sols) == 2, sols)
# l'involuzione dell'attaccante: v = e^{t-x} w(t, 2t-x)
al_, be_ = sp.symbols('al be')
okinv = True
for Wt in [sp.exp(al_*T_ + be_*X_), T_**3*X_**2 + sp.sin(X_)*T_, sp.exp(T_)*sp.cos(2*X_)]:
    vv = sp.exp(t - x)*Wt.subs({T_: t, X_: 2*t - x})
    h1 = sp.simplify(sp.diff(vv, t) - sp.diff(vv, x, 2) - sp.exp(t - x)*(sp.diff(Wt, T_) - sp.diff(Wt, X_, 2)).subs({T_: t, X_: 2*t - x}))
    h2 = sp.simplify(sp.diff(vv, t) + sp.diff(vv, x) - sp.exp(t - x)*(sp.diff(Wt, T_) + sp.diff(Wt, X_)).subs({T_: t, X_: 2*t - x}))
    okinv = okinv and h1 == 0 and h2 == 0
check("O1/KA: l'involuzione pesata v=e^{t-x}w(t,2t-x) conserva entrambi i nuclei (vero, ma e' isolata)", okinv)

# ---------------- OPF-T4 ----------------
th = sp.atan2(x, t)
r2 = t**2 + x**2
check("T4 dtheta: theta_t = -x/r^2, theta_x = t/r^2", sp.simplify(sp.diff(th, t) + x/r2) == 0 and sp.simplify(sp.diff(th, x) - t/r2) == 0)
check("T4 log r^2 armonica", sp.simplify(sp.diff(sp.log(r2), t, 2) + sp.diff(sp.log(r2), x, 2)) == 0)
Q1 = lambda f: sp.diff(f, t) - I*sp.diff(f, x)
Q2 = lambda f: sp.diff(f, t) + I*sp.diff(f, x)
check("T4 Laplaciano: Q1(theta) monodroma = -i/(t+ix)?", sp.simplify(Q1(th) - (-I/(t + I*x))) == 0, sp.simplify(Q1(th)))
check("T4 Laplaciano: Q2(log r^2) = 2/(t - i x)", sp.simplify(Q2(sp.log(r2)) - 2/(t - I*x)) == 0)
# monodromia di Q_j(phi w_j) per tau xi: w=(1,-1): d_t theta, -d_x theta funzioni razionali (monodrome)
check("T4 tau xi: d_t(theta), d_x(-theta) razionali", sp.simplify(sp.diff(th, t)).is_rational_function(t, x) and sp.simplify(-sp.diff(th, x)).is_rational_function(t, x))
# funzioni angolo tagliate: alpha = atan2(x,t) (taglio {x=0,t<0}); beta = pi/2 + atan2(-t, x) (taglio {t=0,x<0})
alpha = lambda T, X: math.atan2(X, T)
beta = lambda T, X: math.pi/2 + math.atan2(-T, X)
ok_d = True; ok_step = True
random.seed(3)
for _ in range(3000):
    T0, X0 = random.uniform(-1, 1), random.uniform(-1, 1)
    if T0*T0 + X0*X0 < 1e-3 or abs(T0) < 1e-6 or abs(X0) < 1e-6: continue
    hh = 1e-6
    # derivate classiche fuori dai tagli = derivate di theta
    if abs((alpha(T0 + hh, X0) - alpha(T0 - hh, X0))/(2*hh) - (-X0/(T0*T0 + X0*X0))) > 1e-4: ok_d = False
    if abs((beta(T0, X0 + hh) - beta(T0, X0 - hh))/(2*hh) - (T0/(T0*T0 + X0*X0))) > 1e-4: ok_d = False
    dif = beta(T0, X0) - alpha(T0, X0)
    expected = 2*math.pi if (T0 < 0 and X0 < 0) else 0.0
    if abs(dif - expected) > 1e-9: ok_step = False
check("T4(e) alpha liscia in t lungo x=cost!=0, beta liscia in x lungo t=cost!=0, derivate = theta_t, theta_x", ok_d)
check("T4(e) u = beta - alpha = 2pi * 1_{t<0,x<0} (gradino, = C12-P10(b))", ok_step)
# controllo Fubini: lungo la retta x=c (c<0) alpha e' continua attraversando t<0 (nessun salto) -- il taglio sta su x=0
jumps = max(abs(alpha(T0 + 1e-4, -0.3) - alpha(T0, -0.3)) for T0 in [-0.9 + 0.01*k for k in range(180)])
check("T4(e) nessun salto di alpha lungo x=-0.3", jumps < 1e-3, jumps)
# generalizzazione a tensori non decomponibili (obiezione KA): linearita' della costruzione -- verifica su delta=2 simbolico
# P = tau*xi*(tau-xi)?? -> qui solo identita' lineare: sum_k phi_k n_{k,j} con sum_j n_{k,j}=0 => sum_j sum_k phi_k n_{k,j} = 0
ph1, ph2 = sp.symbols('phi1 phi2'); n = sp.Matrix([[1, -1, 0], [0, 1, -1]])
check("T4(iii) caso generale: sum_j sum_k phi_k n_{k,j} = 0 se ogni riga di n somma a 0",
      sp.expand(sum(ph1*n[0, j] + ph2*n[1, j] for j in range(3))) == 0)

# ---------------- S5-L2 ----------------
import numpy as np
def proj(B):
    Qm, _ = np.linalg.qr(B); return Qm @ Qm.T
e1, e2, e3 = np.eye(3)
c = e1 + e2 + 2*e3
H1p, H2p, H3p = e1.reshape(3, 1), e2.reshape(3, 1), (c/np.linalg.norm(c)).reshape(3, 1)
Ps = [proj(H1p), proj(H2p), proj(H3p)]
Cp = np.array([[0 if i == j else np.linalg.norm(Ps[i] @ Ps[j], 2) for j in range(3)] for i in range(3)])
nC = np.linalg.norm(Cp, 2)
# H1=span{e1,e3}, H2=span{e2,e3}, H3=span{c}: F1=F2=span{e3}, F3=0; relazioni: dim = 2+2+1-3 = 2; generate dalle intersezioni: 1
Bfull = np.column_stack([e1, e3, e2, e3, c])
dim_rel = 5 - np.linalg.matrix_rank(Bfull)
check("S5-L2(v) CONTROESEMPIO astratto: relazione non generata dalle intersezioni a coppie ma ||C'|| < 1",
      dim_rel == 2 and nC < 1, "dim relazioni=%d (a coppie: 1), ||C'||=%.4f (=1/sqrt3)" % (dim_rel, nC))
# esempio del package tau, xi, tau-xi su (0,1)^2 in H^1: le proiezioni sulle costanti sono la media (funzionale comune) -> parti H' sommano a 0
X_, T__ = sp.symbols('X T')
mean = lambda f: sp.integrate(sp.integrate(f, (X_, 0, 1)), (T__, 0, 1))
y = [X_, T__, -(X_ + T__)]
yp = [yi - mean(yi) for yi in y]
check("S5-L2(v) esempio tau,xi,tau-xi: parti H'_j della relazione sommano a 0 (quindi ||C'||>=1 in quell'esempio)",
      sp.simplify(sum(yp)) == 0 and all(sp.simplify(yi) != 0 for yi in yp))
# tre rette a 120 gradi
v3 = [np.array([math.cos(2*math.pi*k/3), math.sin(2*math.pi*k/3)]) for k in range(3)]
C3 = np.array([[0 if i == j else abs(v3[i] @ v3[j]) for j in range(3)] for i in range(3)])
check("S5-L2 tre rette a 120 gradi: ||C|| = 1", abs(np.linalg.norm(C3, 2) - 1) < 1e-12)
# lemma (iii): A(X)+F=Y con F finita => A(X) chiuso -- controllo di dimensioni sul caso finito (banale) omesso

# ---------------- OPF-P6 / P7 ----------------
d = [0.0, 1.0, 2.5]
def gram(al, be):
    G = np.zeros((3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            s_ = d[i] + d[j]
            G[i, j] = (be - al) if s_ == 0 else (math.exp(s_*be) - math.exp(s_*al))/s_
    return G
mins = [np.linalg.eigvalsh(gram(0, Lc)).min() for Lc in [1.0, 0.5, 0.1]]
check("P6 Gram di esponenziali definita positiva su corde, degenera solo per lunghezza -> 0", all(m > 0 for m in mins) and mins[2] < mins[0], mins)
# P7: idempotenti che commutano (oblique) su tensori
rng = np.random.default_rng(0)
def oblique(nn, kk):
    Bm = rng.standard_normal((nn, kk)); Cm = rng.standard_normal((kk, nn))
    return Bm @ np.linalg.inv(Cm @ Bm) @ Cm
pa = np.kron(oblique(4, 2), np.eye(5)); pb = np.kron(np.eye(4), oblique(5, 3))
Em = pa + pb - pa @ pb
check("P7 E = pi_A+pi_B-pi_A pi_B idempotente e rank = dim(im pi_A + im pi_B)",
      np.allclose(Em @ Em, Em) and np.linalg.matrix_rank(Em) == np.linalg.matrix_rank(np.column_stack([pa, pb])))

print("\nTOTALE: %d/%d OK" % (sum(1 for _, b in RES if b), len(RES)))
