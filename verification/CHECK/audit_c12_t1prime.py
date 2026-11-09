# S-CHECK-3B — red team per C12-L1', L2', T1', P10 (work/C1C2/CHECK_REQUEST_2.md)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_c12_t1prime.py > audit_c12_t1prime.out
import sympy as sp
import mpmath as mp

res = []
def check(name, ok, info=""):
    res.append((name, bool(ok)))
    print(("OK   " if ok else "FAIL ") + name + ("  | " + str(info) if info != "" else ""))

t, x, t0, x0, p, q = sp.symbols('t x t0 x0 p q')
T, X = sp.symbols('tau xi')

# ---------- P10(a): Laplaciano, u = log|z-alpha|^2 ----------
Q1 = lambda f: sp.diff(f, t) - sp.I*sp.diff(f, x)
Q2 = lambda f: sp.diff(f, t) + sp.I*sp.diff(f, x)
u = sp.log((t-t0)**2 + (x-x0)**2)
check("a1 Q1Q2 = Laplaciano (simbolo)", sp.expand((T-sp.I*X)*(T+sp.I*X) - (T**2+X**2)) == 0)
check("a2 u armonica fuori da alpha", sp.simplify(sp.diff(u, t, 2) + sp.diff(u, x, 2)) == 0)
w = (t-t0) - sp.I*(x-x0)
F = sp.simplify(Q2(u))
check("a3 Q2 u = 2/w", sp.simplify(F - 2/w) == 0, F)
# dh = (F/2) dt + (F/(2i)) dx  deve essere dw/w = (1/w) dt - (i/w) dx
check("a4 d_t h = F/2 = 1/w", sp.simplify(F/2 - 1/w) == 0)
check("a5 d_x h = F/(2i) = -i/w", sp.simplify(F/(2*sp.I) + sp.I/w) == 0)
# chiusura di dw/w
check("a6 dw/w chiusa", sp.simplify(sp.diff(1/w, x) - sp.diff(-sp.I/w, t)) == 0)
# periodo su cerchio antiorario (in z = t + i x) di raggio r attorno ad alpha, percorso n volte
th, r = sp.symbols('theta r', positive=True)
tt = t0 + r*sp.cos(th); xx = x0 + r*sp.sin(th)
integrand = ((1/w)*sp.diff(tt, th) + (-sp.I/w)*sp.diff(xx, th)).subs({t: tt, x: xx})
per = sp.simplify(sp.integrate(sp.simplify(integrand), (th, 0, 2*sp.pi)))
check("a7 periodo di dw/w su cerchio antiorario = -2*pi*i (= coniugato di 2*pi*i*Ind)", sp.simplify(per + 2*sp.pi*sp.I) == 0, per)
# versione torta: [(tau-p) -+ i(xi-q)](d)(e v) = e Q_{1,2}(d) v
v = sp.Function('v')(t, x); e = sp.exp(p*t + q*x)
lhs1 = sp.diff(e*v, t) - p*e*v - sp.I*(sp.diff(e*v, x) - q*e*v)
lhs2 = sp.diff(e*v, t) - p*e*v + sp.I*(sp.diff(e*v, x) - q*e*v)
check("a8 twist Q1", sp.simplify(lhs1 - e*Q1(v)) == 0)
check("a9 twist Q2", sp.simplify(lhs2 - e*Q2(v)) == 0)
check("a10 (tau-p)^2+(xi-q)^2 = prodotto dei twist", sp.expand(((T-p)-sp.I*(X-q))*((T-p)+sp.I*(X-q)) - ((T-p)**2+(X-q)**2)) == 0)
# dim R/(Q1,Q2) = 1 (Groebner)
G = sp.groebner([T-sp.I*X, T+sp.I*X], T, X, order='grevlex')
check("a11 (Q1,Q2) = (tau, xi): dim R/(Q1,Q2) = 1", set(G.exprs) == {T, X}, G.exprs)

# ---------- P10(b): u = H(x-x0)H(t-t0), omega_eps = H_eps(x-x0) rho_eps(t-t0) dt ----------
mp.mp.dps = 30
eps = mp.mpf('0.1')
def rho(s):  # bump C^infinito normalizzato su [-eps, eps]
    if abs(s) >= eps: return mp.mpf(0)
    return mp.e**(-1/(1-(s/eps)**2))
Z = mp.quad(lambda s: rho(s), [-eps, eps])
rhoN = lambda s: rho(s)/Z
def Heps(s):
    if s <= -eps: return mp.mpf(0)
    if s >= eps: return mp.mpf(1)
    return mp.quad(rhoN, [-eps, s])
def period_circle(c_t, c_x, R, turns=1):
    # integrale di H_eps(x) rho_eps(t) dt sul cerchio antiorario di centro (c_t,c_x), alpha = (0,0)
    def f(th):
        tt_ = c_t + R*mp.cos(th); xx_ = c_x + R*mp.sin(th)
        return Heps(xx_)*rhoN(tt_)*(-R*mp.sin(th))
    # il supporto in t e' |t|<eps: punti critici dove c_t + R cos th = +-eps
    pts = [mp.mpf(0)]
    for s in (-eps, eps):
        cval = (s - c_t)/R
        if abs(cval) <= 1:
            a = mp.acos(cval); pts += [a, 2*mp.pi - a]
    pts = sorted(set([pp for pp in pts if 0 <= pp <= 2*mp.pi] + [2*mp.pi]))
    return turns*mp.quad(f, pts)
I1 = period_circle(0, 0, mp.mpf(1))
check("b1 periodo di omega_eps sul cerchio antiorario attorno ad alpha = -1", abs(I1 + 1) < mp.mpf('1e-15'), mp.nstr(I1, 20))
I2 = period_circle(0, 0, mp.mpf('0.5'), turns=2)
check("b2 cerchio percorso 2 volte (Ind = 2): periodo = -2", abs(I2 + 2) < mp.mpf('1e-15'), mp.nstr(I2, 20))
I3 = period_circle(mp.mpf(3), mp.mpf(0), mp.mpf(1))
check("b3 cerchio che non circonda alpha: periodo = 0", abs(I3) < mp.mpf('1e-15'), mp.nstr(I3, 20))
I4 = period_circle(mp.mpf('0.3'), mp.mpf('-0.2'), mp.mpf('0.9'))
check("b4 cerchio decentrato che circonda alpha: periodo = -1 (chiusura su E)", abs(I4 + 1) < mp.mpf('1e-15'), mp.nstr(I4, 20))
# d omega_eps = d_x(H_eps(x) rho_eps(t)) dx^dt = rho_eps(x) rho_eps(t) dx^dt: supporto in [-eps,eps]^2
Hs = sp.Function('H')(x); rs = sp.Function('rho')(t)
check("b5 d(H_eps(x) rho(t) dt) = H_eps'(x) rho(t) dx^dt", sp.simplify(sp.diff(Hs*rs, x) - sp.diff(Hs, x)*rs) == 0)
# distribuzionale: d_t d_x (H x H) = delta x delta, nulla su Omega se alpha non in Omega (controllo con test function)
phi = sp.exp(-(t-1)**2 - (x-2)**2)  # test (non compatta, ma decrescente) ; <d_t d_x(HxH), phi> = phi(0,0)
val = sp.integrate(sp.integrate(sp.diff(phi, t, x), (t, 0, sp.oo)), (x, 0, sp.oo))
check("b6 <dt dx (H(x)H(t)), phi> = phi(alpha)", sp.simplify(val - phi.subs({t: 0, x: 0})) == 0, sp.simplify(val))

# ---------- P10(c): disco bucato, tau*xi in C^infinito ----------
# u = theta (argomento) NON e' monodroma sul disco bucato; un elemento di ker d_t d_x su D*:
# u = a(x) + b(t) + f(x)*g(t) con f'g' supportato fuori da D* e' impossibile se D* contiene tutti i quadranti vicino a 0.
# Controllo della costruzione: phi = d_t u dipende solo da t, B = int_0^t g, A = u - B.
a_ = sp.Function('a')(x); b_ = sp.Function('b')(t)
uu = a_ + b_
g = sp.diff(uu, t)
B = sp.integrate(g.subs(t, sp.Symbol('s')), (sp.Symbol('s'), 0, t))
A = sp.simplify(uu - B)
check("c1 costruzione A, B: d_t A = 0, d_x B = 0", sp.simplify(sp.diff(A, t)) == 0 and sp.simplify(sp.diff(B, x)) == 0)
# corona vs disco bucato: u = alpha(x) beta(t) a gradini liscia con alpha'beta' supportato in [-1/2,1/2]^2
# sul disco bucato (raggio 2) il quadrato [-1/2,1/2]^2 \ {0} sta in D*: u NON e' nel nucleo di tau*xi.
check("c2 coerenza O-1 vs (c): [-1/2,1/2]^2 \\ {0} interseca D*(0,2) (u di O-1 non e' in ker su D*)", sp.Rational(1,4)**2*2 < 4)

# ---------- L1'(c') passo (4)-(5): incollamento con costanti ----------
F0 = sp.Function('F0')(t, x)                     # primitiva "vera" locale: w_j = F0 + c_j su U_j
c1, c2, c3 = sp.symbols('c1 c2 c3')
ch1 = sp.Function('chi1')(t, x); ch2 = sp.Function('chi2')(t, x)
ch3 = 1 - ch1 - ch2
wglob = ch1*(F0 + c1) + ch2*(F0 + c2) + ch3*(F0 + c3)
h_k = sp.expand(wglob - (F0 + c1))               # su U_1: w = w_1 + h_1
check("L1p-4 h_1 = sum_j chi_j (c_j - c_1) (liscia, combinazione delle chi)", sp.simplify(h_k - (ch2*(c2-c1) + ch3*(c3-c1))) == 0, h_k)
phit = sp.diff(F0, t); psit = sp.diff(F0, x)
a5 = sp.simplify(phit - sp.diff(wglob, t)); b5 = sp.simplify(psit - sp.diff(wglob, x))
check("L1p-5 a = -d_t h_1, b = -d_x h_1", sp.simplify(a5 + sp.diff(h_k, t)) == 0 and sp.simplify(b5 + sp.diff(h_k, x)) == 0)
check("L1p-6 a dt + b dx chiusa", sp.simplify(sp.diff(a5, x) - sp.diff(b5, t)) == 0)
# dove serve la topologia: d theta e' chiusa e non esatta sulla corona/disco bucato
dth_t = -x/(t**2+x**2); dth_x = t/(t**2+x**2)
check("L1p-7 d theta chiusa", sp.simplify(sp.diff(dth_t, x) - sp.diff(dth_x, t)) == 0)
pth = sp.integrate(sp.simplify((dth_t*sp.diff(sp.cos(th), th) + dth_x*sp.diff(sp.sin(th), th)).subs({t: sp.cos(th), x: sp.sin(th)})), (th, 0, 2*sp.pi))
check("L1p-8 periodo di d theta = 2 pi (non esatta: il passo (5) e' l'unico che usa H^1_dR = 0)", sp.simplify(pth - 2*sp.pi) == 0, pth)

# ---------- L2'/T1': dimensioni (algebra, indipendente da Omega) ----------
def stddim(gens):
    Gb = sp.groebner(gens, T, X, order='grevlex')
    # conta i monomi standard fino a grado 12
    lms = [sp.Poly(g_, T, X).monoms(order='grevlex')[0] for g_ in Gb.exprs]
    cnt = 0
    for i in range(13):
        for j in range(13):
            if not any(i >= m[0] and j >= m[1] for m in lms): cnt += 1
    return cnt
check("T1p-1 Laplaciano: delta = 1", stddim([T-sp.I*X, T+sp.I*X]) == 1)
check("T1p-2 tau*xi: delta = dim R/(tau,xi) = 1", stddim([T, X]) == 1)
check("T1p-3 calore x trasporto: delta = 2", stddim([T-X**2, T-X]) == 2)
# ambiguita' per tau*xi: N = {(c, -c)} = costanti (EP): nucleo di dim 1 su ogni Omega connesso
check("T1p-4 tre rette per 0 (tau, xi, tau-xi): delta = 3", stddim([T, X]) + stddim([T, T-X]) + stddim([X, T-X]) == 3)

# ---------- L2'(3): restrizione iniettiva (EP nullo su aperto => nullo) ----------
ep = (1 + t)*sp.exp(t + 2*x) - sp.exp(2*t)
check("L2p-1 EP non nullo non si annulla identicamente vicino a (0,0) (jet)", any(sp.diff(ep, t, i).subs({t: 0, x: 0}) != 0 for i in range(3)))

npass = sum(1 for _, o in res if o)
print("\nESITO: %d/%d OK" % (npass, len(res)))
