# S8-DICT — seconda serie di verifiche (solo verifica, non prove). Esecuzione:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-DICT/sympy/s8dict_checks2.py
import sympy as sp
import mpmath as mp
import numpy as np

RES = []
def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("OK  " if ok else "FAIL"), name, info)

t, x, s = sp.symbols('t x s', real=True)
rng = np.random.default_rng(7)

# F1 Lemma ND: D1 = d_x, D2 = x d_x sono dipendenti in ogni punto (forme sul getto proporzionali)
# ma indipendenti come operatori; w = x da' D1 w = 1, D2 w = x indipendenti.
w = x
M = sp.Matrix([[sp.diff(w, x).subs(x, xv), (x*sp.diff(w, x)).subs(x, xv)] for xv in [0, 1]])
check("F1 Lemma ND: D1=d_x, D2=x d_x, w=x, det[D_i w(y_k)] != 0", M.det() != 0, "det=%s" % M.det())

# F2 Lemma ND non lineare: Q1=u^2, Q2=u u_x, Q3=u_x^2 (indipendenti come polinomi nel getto)
# getti scelti in 3 punti distinti -> matrice di valutazione invertibile
jets = [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
Mq = np.array([[u0**2, u0*u1, u1**2] for (u0, u1) in jets])
check("F2 Lemma ND-NL: det[Q_i(j_k)] != 0 per getti in punti distinti", abs(np.linalg.det(Mq)) > 1e-12, "det=%.3f" % np.linalg.det(Mq))

# F3 Teorema A(iii): dati finiti ESATTI (M funzionali) non certificano il fit.
# Omega = (0,1)^2, livello {d_t, d_x^2} (calore), u = e^{-t} sin x ha fit; costruisco w in ker(l_1..l_M)
# come combinazione di M+1 bump a supporti disgiunti, e verifico: stessi dati, misfit (Gram > 0).
n = 241
g = np.linspace(0, 1, n); h = g[1] - g[0]
T_, X_ = np.meshgrid(g, g, indexing='ij')
def bump(cx, ct, r):
    rr2 = ((X_ - cx)**2 + (T_ - ct)**2)/r**2
    return np.where(rr2 < 1, (1 - rr2)**6, 0.0)
def dt(F): return np.gradient(F, h, axis=0)
def dxx(F): return np.gradient(np.gradient(F, h, axis=1), h, axis=1)
u = np.exp(-T_)*np.sin(X_)
Mfun = 3
ells = [T_**a*X_**b for (a, b) in [(0, 0), (1, 0), (1, 2)]]
centers = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)]
wk = [bump(cx, ct, 0.2) for (cx, ct) in centers]
L = np.array([[np.sum(e*wkk)*h*h for wkk in wk] for e in ells])   # M x (M+1)
gam = np.linalg.svd(L)[2][-1]                                      # nucleo
wsum = sum(gk*wkk for gk, wkk in zip(gam, wk))
v = u + 0.05*wsum
same = max(abs(np.sum(e*(v - u))*h*h) for e in ells)
inner = (slice(5, -5), slice(5, -5))
def gram_min(F):
    A = np.column_stack([dt(F)[inner].ravel(), dxx(F)[inner].ravel()])
    G = A.T @ A*h*h
    return np.linalg.eigvalsh(G)[0]/np.trace(G)
check("F3 Teorema A(iii): stessi dati esatti, u con fit, v con misfit", same < 1e-12 and gram_min(u) < 1e-6 and gram_min(v) > 1e-3,
      "diff dati=%.1e, lmin_rel(u)=%.1e, lmin_rel(v)=%.1e" % (same, gram_min(u), gram_min(v)))

# F4 N3 su intervallo: ||(S_tau - H) f|| / ||f|| -> >= 1 per pacchetti d'onda ad alta frequenza,
# H = D delta + h*, h(t) = C e^{At} B (sistema finito-dimensionale causale, stato iniziale nullo)
T, tau = 4.0, 1.0
N = 40001
tt = np.linspace(0, T, N); dtt = tt[1] - tt[0]
def phi(tv): return np.where((tv > 0.5) & (tv < 1.4), np.sin(np.pi*(tv - 0.5)/0.9)**2, 0.0)
okF4 = True; worst = 10
for trial in range(5):
    A = rng.normal(size=(3, 3)); A = A - (np.max(np.linalg.eigvals(A).real) + 0.5)*np.eye(3)
    B = rng.normal(size=3); C = rng.normal(size=3); D = rng.normal()
    ev, V = np.linalg.eig(A); Vi = np.linalg.inv(V)
    hk = np.real(np.einsum('i,ij,tj,j->t', C, V, np.exp(np.outer(tt, ev)), Vi @ B))
    for om in [200.0, 400.0]:
        f = phi(tt)*np.exp(1j*om*tt)
        Sf = phi(tt - tau)*np.exp(1j*om*(tt - tau))
        Hf = D*f + np.convolve(hk, f)[:N]*dtt
        ratio = np.linalg.norm(Sf - Hf)/np.linalg.norm(f)
        worst = min(worst, ratio); okF4 = okF4 and ratio >= 1 - 2e-2
check("F4 N3 su (0,T): ||(S_tau - H)f||/||f|| >= 1 - o(1) per pacchetti ad alta frequenza", okF4, "min ratio=%.4f" % worst)

# F5 rappresentazione diffusiva esatta: k(t)=1/(1+t)=int e^{-lt} e^{-l} dl; (k*f)(t) = int w(t,l) e^{-l} dl
mp.mp.dps = 20
f = lambda sv: mp.cos(3*sv) + sv
tv = mp.mpf('1.3')
conv = mp.quad(lambda sv: f(sv)/(1 + tv - sv), [0, tv])
wfun = lambda l: mp.quad(lambda sv: mp.exp(-l*(tv - sv))*f(sv), [0, tv])
diff = mp.quad(lambda l: wfun(l)*mp.exp(-l), [0, 1, 10, mp.inf])
check("F5 diffusiva esatta per k=1/(1+t) (c.m.)", abs(conv - diff) < 1e-12, "diff=%.1e" % float(abs(conv - diff)))
# F5b convergenza L^1(0,T) delle somme di esponenziali (celle logaritmiche) per lo stesso k
def kJ_err(J):
    edges = np.concatenate([[0], np.exp(np.linspace(-6, 4, J))])
    lam_mid = np.sqrt(np.maximum(edges[:-1], 1e-300)*edges[1:]); lam_mid[0] = edges[1]/2
    wts = np.exp(-edges[:-1]) - np.exp(-edges[1:])
    tg = np.linspace(0, 5, 20001)
    kJ = (wts[None, :]*np.exp(-np.outer(tg, lam_mid))).sum(1)
    return np.trapezoid(np.abs(1/(1 + tg) - kJ), tg)
errs = [kJ_err(J) for J in [10, 40, 160]]
check("F5b L^1 convergenza per nucleo c.m. generico (nessuna velocita' dichiarata)", errs[0] > errs[1] > errs[2], str(["%.2e" % e for e in errs]))

# F6 Caffarelli-Silvestre: h(r) = r^{1-s} K_{1-s}(r) decrescente, h(0+) = 2^{-s} Gamma(1-s)
okF6 = True
for sv in [0.2, 0.5, 0.9]:
    hh = lambda r: r**(1 - sv)*mp.besselk(1 - sv, r)
    mp.mp.dps = 40; vals = [hh(mp.mpf(r)) for r in ['1e-100', '1e-3', '0.1', '1', '5']]  # r piccolo: correzione ~ r^{2(1-s)}
    okF6 = okF6 and all(vals[i] > vals[i + 1] for i in range(4)) and abs(vals[0]/(2**(-sv)*mp.gamma(1 - sv)) - 1) < 1e-8
check("F6 CS: h decrescente, h(0+) = 2^{-s} Gamma(1-s) (convergenza dominata del dato di Neumann)", okF6)

# F7 2-kink (cono di luce): residuo ~ 0 e rango 4 delle 5 funzioni atomo -> nucleo 1 (V-ex)
a1, a2 = sp.Rational(1, 2), sp.Rational(2, 1)
th1, th2 = a1*x + t/a1, a2*x + t/a2
best = None
for sgn in [1, -1]:
    for pref in [(a2 + a1)/(a2 - a1), (a2 - a1)/(a2 + a1)]:
        uk = 4*sp.atan(pref*(sp.exp(th1) + sgn*sp.exp(th2))/(1 - sgn*sp.exp(th1 + th2)))
        res = sp.lambdify((x, t), sp.diff(uk, x, t) - sp.sin(uk))
        r = max(abs(res(xv, tv)) for xv in [0.3, -0.7, 1.1] for tv in [0.2, -0.4, 0.9])
        if best is None or r < best[0]:
            best = (r, uk)
r2, uk = best
fl = [sp.lambdify((x, t), e_) for e_ in [sp.diff(uk, x, t), sp.sin(uk), sp.diff(uk, x, 2), sp.diff(uk, t, 2), uk]]
pts = [(xv, tv) for xv in np.linspace(-1.5, 1.5, 13) for tv in np.linspace(-1.5, 1.5, 13)]
Mat = np.array([[float(np.real(F(*p))) for F in fl] for p in pts])
Mat = Mat[np.all(np.isfinite(Mat), axis=1)]
sv5 = np.linalg.svd(Mat, compute_uv=False)
rank = int(np.sum(sv5 > 1e-8*sv5[0]))
check("F7 2-kink: residuo sine-Gordon ~ 0, rango 4 => nucleo 1 (identifica nel dizionario a 5 atomi; V-ex)", r2 < 1e-9 and rank == 4,
      "res=%.1e sv=%s" % (r2, np.array2string(sv5, precision=2)))

# F8 corollario Holder s=0, N=1 su [0,1]: ||f||_inf <= max(2 Lip^{1/3} ||f||_2^{2/3}, 2 sqrt2 ||f||_2)
okF8 = True
xs = np.linspace(0, 1, 20001)
for trial in range(300):
    k = rng.integers(1, 30); c0 = rng.uniform(0, 1); amp = rng.normal()
    fv = amp*np.exp(-k*np.abs(xs - c0)) + rng.normal()*0.01*np.sin(k*xs)
    lip = np.max(np.abs(np.diff(fv))/np.diff(xs)); l2 = np.sqrt(np.trapezoid(fv**2, xs))
    okF8 = okF8 and np.max(np.abs(fv)) <= max(2*lip**(1/3)*l2**(2/3), 2*np.sqrt(2)*l2) + 1e-9
check("F8 interpolazione L^2-Lip -> L^inf (costante esplicita, N=1)", okF8)

# F9 NS-L1: esponenziali commensurabili, u_xt = e^u - e^{2u}; w = e^u: w w_xt - w_x w_t = w^3 - w^4
uf = sp.Function('u')(x, t)
W = sp.exp(uf)
lhs = W*sp.diff(W, x, t) - sp.diff(W, x)*sp.diff(W, t) - (W**3 - W**4)
check("F9 NS-L1: polinomializzazione con esponenti commensurabili", sp.simplify(lhs - W**2*(sp.diff(uf, x, t) - sp.exp(uf) + sp.exp(2*uf))) == 0)

# F10 N1(iii): serve N >= 2. N = 3: C(n+3,3) - C(n+2,3) = C(n+2,2) -> inf; N = 1: differenza costante = d
nn, dd = sp.symbols('n d', positive=True, integer=True)
e3 = sp.binomial(nn + 3, 3) - sp.binomial(nn + 2, 3) - sp.binomial(nn + 2, 2)
e1 = (nn + 1) - (nn - dd + 1) - dd
check("F10 N1(iii): conteggi per N=3 (cresce) e N=1 (costante)", sp.simplify(sp.expand_func(e3)) == 0 and sp.simplify(e1) == 0)

# F11 teorema di rango: K = 3 atomi (d_x, 1, d_t), theta = rho x e (prodotto vettoriale) e' nel nucleo
uu = sp.exp(t)*sp.cos(x) + x**2*t
rho = sp.Matrix([sp.diff(uu, x), uu, sp.diff(uu, t)])
e = sp.Matrix([1, 2, 3])
th = rho.cross(e)
check("F11 rango: K>=2 => nucleo puntuale non banale (theta = rho x e)", sp.simplify(th.dot(rho)) == 0 and th != sp.zeros(3, 1))

print("\nTOTALE: %d/%d OK" % (sum(1 for _, o in RES if o), len(RES)))
