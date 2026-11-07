# S8-SYS: verifiche simboliche e numeriche (solo verifica, nessuna prova).
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-SYS/sympy/s8sys_checks.py
import sympy as sp
import mpmath as mp

RES = []
def check(tag, cond, info=""):
    ok = bool(cond)
    RES.append((tag, ok))
    print(f"[{'OK' if ok else 'FAIL'}] {tag} {info}")

I = sp.I
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -I], [I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
xi, t, m, tau = sp.symbols('xi t m tau')

# ---------- [A] SYS-E: ipotesi (H) di P1-T5 in Mat_2(C[xi]) per Dirac 1+1 ----------
X = I*sz*xi; Y = -I*sx
Ys = [Y]
for k in range(9):
    Ys.append(sp.expand(X*Ys[-1] - Ys[-1]*X))
def vec(Mx, deg=12):
    v = []
    for e in Mx:
        p = sp.Poly(sp.expand(e), xi)
        v += [p.coeff_monomial(xi**d) for d in range(deg)]
    return v
Mrows = sp.Matrix([vec(X)] + [vec(Z) for Z in Ys[:9]])
check("A1 (H): X,Y_0..Y_8 linearmente indipendenti su C", Mrows.rank() == 10, f"rango {Mrows.rank()}/10")
ok = True
for k, Z in enumerate(Ys[:9]):
    base = sx if k % 2 == 0 else sy
    c = sp.simplify(Z[0, 1] / base[0, 1]) if base[0, 1] != 0 else None
    ok &= sp.simplify(Z - c*base) == sp.zeros(2) and sp.Poly(c, xi).degree() == k
check("A2 Y_k = c_k xi^k sigma_{x|y} (x per k pari, y per k dispari), c_k != 0", ok)
# chiusura nell'algebra torcita: base xi^{dispari} sz, xi^{pari} sx, xi^{dispari} sy
def in_twisted(Mx):
    a = sp.expand((Mx[0, 0] - Mx[1, 1]) / 2)    # coeff di sz
    b = sp.expand((Mx[0, 1] + Mx[1, 0]) / 2)    # coeff di sx
    c = sp.expand((Mx[1, 0] - Mx[0, 1]) / (2*I))  # coeff di sy
    tr = sp.expand(Mx[0, 0] + Mx[1, 1])
    par = lambda e, odd: all((d[0] % 2 == 1) == odd for d in sp.Poly(e, xi).monoms()) if e != 0 else True
    return tr == 0 and par(a, True) and par(b, False) and par(c, True)
gens = [X, Y]
basis = [xi**(2*j+1)*sz for j in range(3)] + [xi**(2*j)*sx for j in range(3)] + [xi**(2*j+1)*sy for j in range(3)]
ok = all(in_twisted(sp.expand(A*B - B*A)) for A in basis for B in basis)
check("A3 l'algebra torcita (sl2 x C[xi])^theta e' chiusa per commutatore (gradi bassi)", ok)
ok = all(in_twisted(Z) for Z in Ys[:9])
check("A4 tutti gli Y_k stanno nell'algebra torcita", ok)

# ---------- [B] Euler ZXZ con tempi dipendenti da xi ----------
def U_exact(tv, xv, mv):
    w = mp.sqrt(xv**2 + mv**2)
    A = mp.matrix([[1j*xv, -1j*mv], [-1j*mv, -1j*xv]])
    return mp.cos(w*tv)*mp.eye(2) + mp.sin(w*tv)/w*A
def ezx(a, b):
    Zf = lambda g: mp.matrix([[mp.e**(1j*g), 0], [0, mp.e**(-1j*g)]])
    Xf = mp.matrix([[mp.cos(b), 1j*mp.sin(b)], [1j*mp.sin(b), mp.cos(b)]])
    return Zf(a)*Xf*Zf(a)
def angles(tv, xv, mv):
    w = mp.sqrt(xv**2 + mv**2)
    b = -mp.asin(mv*mp.sin(w*tv)/w)
    z = mp.cos(w*tv) + 1j*xv*mp.sin(w*tv)/w
    a = mp.arg(z/mp.cos(b)) / 2
    return a, b
err = 0
for tv in [0.1, 0.7, 1.3, 2.9]:
    for xv in [-3.0, -0.4, 0.5, 2.0, 7.0]:
        a, b = angles(tv, xv, 1.0)
        err = max(err, mp.mnorm(ezx(a, b) - U_exact(tv, xv, 1.0), 1))
check("B1 e^{tA(xi)} = e^{ia sz} e^{ib sx} e^{ia sz} con a,b espliciti", err < 1e-12, f"err {float(err):.1e}")
bt = lambda tv, xv: -mp.asin(mp.sin(mp.sqrt(xv**2+1)*tv)/mp.sqrt(xv**2+1))
check("B2 b(t,xi) -> 0 per xi -> inf ma b(t,0) = -t != 0 (t=0.5): b non polinomiale in xi",
      abs(bt(0.5, 1e6)) < 1e-5 and abs(bt(0.5, 0) + 0.5) < 1e-12)
g1 = lambda tv, xv: angles(tv, xv, 1.0)[0] / xv
check("B3 g1 = a/xi -> tan(t)/2 per xi -> 0 (t=0.5)", abs(g1(0.5, 1e-7) - mp.tan(0.5)/2) < 1e-6)
tc = mp.pi/2
check("B4 a t = pi/(2m) g1 = a/xi diverge per xi -> 0 (blocco cardanico)", abs(g1(tc, 1e-4)) > 1e3 and abs(g1(tc, 1e-6)) > 1e5,
      f"g1(1e-4)={float(g1(tc,1e-4)):.2e}")

# ---------- [C] Dirac 3+1 (chirale), forma hamiltoniana ----------
p0, p1, p2, p3 = sp.symbols('p0 p1 p2 p3')
sig = [sx, sy, sz]
sp_ = p1*sx + p2*sy + p3*sz
Xc = p0*sp.eye(2) - sp_; Yc = p0*sp.eye(2) + sp_
KG = p0**2 - p1**2 - p2**2 - p3**2
check("C1 X Y = Y X = KG I_2", sp.expand(Xc*Yc - KG*sp.eye(2)) == sp.zeros(2) and sp.expand(Yc*Xc - KG*sp.eye(2)) == sp.zeros(2))
D = sp.BlockMatrix([[-m*sp.eye(2), Xc], [Yc, -m*sp.eye(2)]]).as_explicit()
Dp = sp.BlockMatrix([[m*sp.eye(2), Xc], [Yc, m*sp.eye(2)]]).as_explicit()
check("C2 D D' = D' D = (KG - m^2) I_4", sp.expand(D*Dp - (KG - m**2)*sp.eye(4)) == sp.zeros(4) and sp.expand(Dp*D - (KG - m**2)*sp.eye(4)) == sp.zeros(4))
check("C3 det D = (KG - m^2)^2", sp.factor(D.det() - (KG - m**2)**2) == 0)
# eliminazione: e_top = X e_bot / m  =>  relazione residua (Y X/m - m) = (KG-m^2)/m I_2
check("C4 Y X - m^2 I = (KG - m^2) I (M_D libero di rango 2 su R/(KG-m^2))", sp.expand(Yc*Xc - m**2*sp.eye(2) - (KG - m**2)*sp.eye(2)) == sp.zeros(2))
check("C5 KG - m^2 irriducibile su Q (m simbolo)", len(sp.factor_list(KG - m**2)[1]) == 1)
# forma hamiltoniana: coefficiente di p0 in D e' invertibile => L_H = G0^{-1} D ha p0*I
G0 = D.applyfunc(lambda e: sp.diff(e, p0))
LH = sp.expand(G0.inv()*D)
check("C6 forma hamiltoniana G0^{-1}D = p0 I + (lineare in p1..p3, costante)", sp.expand(LH.applyfunc(lambda e: sp.diff(e, p0))) == sp.eye(4)
      and all(sp.Poly(e, p0, p1, p2, p3).total_degree() <= 1 for e in LH if e != 0))
# Dirac 1+1 ciclico: D2 = [[-m, p0-p1],[p0+p1,-m]]
D2 = sp.Matrix([[-m, p0 - p1], [p0 + p1, -m]])
check("C7 Dirac 1+1: det = m^2 - (p0^2-p1^2), psi_1 = (p0-p1)psi_2/m", sp.expand(D2.det() - (m**2 - (p0**2 - p1**2))) == 0)

# ---------- [D] Lame n = 3 ----------
x1, x2, x3, lam, mu, rho = sp.symbols('xi1 xi2 xi3 lambda mu rho')
xv = sp.Matrix([x1, x2, x3]); n2 = x1**2 + x2**2 + x3**2
P = rho*tau**2*sp.eye(3) - mu*n2*sp.eye(3) - (lam + mu)*xv*xv.T
qP = rho*tau**2 - (lam + 2*mu)*n2; qS = rho*tau**2 - mu*n2
check("D1 det P = qP qS^2", sp.factor(P.det() - qP*qS**2) == 0)
check("D2 xi^T P = qP xi^T (div)", sp.expand(xv.T*P - qP*xv.T) == sp.zeros(1, 3))
Cx = sp.Matrix([[0, -x3, x2], [x3, 0, -x1], [-x2, x1, 0]])
check("D3 [xi]_x P = qS [xi]_x (rot)", sp.expand(Cx*P - qS*Cx) == sp.zeros(3))
check("D4 Helmholtz: |xi|^2 I = xi xi^T - [xi]_x^2", sp.expand(n2*sp.eye(3) - xv*xv.T + Cx*Cx) == sp.zeros(3))
# rango di P sulle due varieta' (punto generico): sostituisci tau^2
PS = sp.simplify(P.subs(tau**2, mu*n2/rho)); PP = sp.simplify(P.subs(tau**2, (lam + 2*mu)*n2/rho))
check("D5 rango P mod qS = 1 (mu_qS = 2), rango P mod qP = 2 (mu_qP = 1)", PS.rank() == 1 and PP.rank() == 2)
check("D6 qP, qS irriducibili, distinti per lam+mu != 0", len(sp.factor_list(qP)[1]) == 1 and len(sp.factor_list(qS)[1]) == 1 and sp.expand(qP - qS + (lam + mu)*n2) == 0)
check("D7 xi^T xi = |xi|^2 non in qS (Ass non contiene |xi|^2)", sp.rem(sp.Poly(n2, tau), sp.Poly(qS, tau)) != 0)

# ---------- [E] SYS-S1: controesempio su Omega a U ----------
a, b = sp.symbols('a b')
# U1 = R(1,0), U2 = R(1,xi): a(1,0) = b(1,xi) => b*xi = 0 => b = 0 => a = 0
sol = sp.solve([a - b, b*xi], [a, b], dict=True)
check("E1 U1 cap U2 = 0 (dunque P = 0, Sol(P) = A^2)", sol == [{a: 0, b: 0}])
check("E2 U1 + U2 = R(1,0) + R(0,xi): N = R/(xi) di lunghezza infinita", sp.Matrix([[1, 0], [1, xi]]).det() == xi)
tt = sp.symbols('t', real=True)
beta = 1  # per t in (3/4,1)
Iint = sp.integrate(beta/(1 - tt), (tt, sp.Rational(3, 4), tt))
check("E3 I(t) = int f dx = beta(t)/(1-t) -> +inf per t -> 1^-", sp.limit(1/(1 - tt), tt, 1, '-') == sp.oo)

# ---------- [F] SYS-N3: Schrodinger magnetico (stazionario e non) in 2D ----------
x, y, T = sp.symbols('x y T', real=True)
r = sp.Function('rho')(T, x, y); S = sp.Function('S')(T, x, y)
A1 = sp.Function('A1')(T, x, y); A2 = sp.Function('A2')(T, x, y); V = sp.Function('V')(T, x, y)
u = r*sp.exp(I*S)
def cov(f, j):  # (d_j - i A_j)
    return sp.diff(f, [x, y][j]) - I*[A1, A2][j]*f
H = -(cov(cov(u, 0), 0) + cov(cov(u, 1), 1)) + V*u
res = sp.expand(sp.simplify((I*sp.diff(u, T) - H) * sp.exp(-I*S)))
w1 = sp.diff(S, x) - A1; w2 = sp.diff(S, y) - A2
re_pred = -r*sp.diff(S, T) - (-sp.diff(r, x, 2) - sp.diff(r, y, 2) + r*(w1**2 + w2**2) + V*r)
im_pred = sp.diff(r, T) + (sp.diff(r**2*w1, x) + sp.diff(r**2*w2, y))/r
check("F1 i u_t = H_A u  <=>  {V = -S_t + Lap rho/rho - |w|^2, d_t rho^2 + 2 div(rho^2 w) = 0}",
      sp.simplify(res - (re_pred + I*im_pred)) == 0)
# famiglia: j -> j + rot(psi) lascia le due equazioni risolubili con lo stesso u; campo magnetico cambia
psi = sp.exp(-(x**2 + y**2)); rr = sp.exp(x/3)
k1, k2 = -sp.diff(psi, y), sp.diff(psi, x)
check("F2 div(rot psi) = 0", sp.simplify(sp.diff(k1, x) + sp.diff(k2, y)) == 0)
dB = sp.diff(-k2/rr**2, x) - sp.diff(-k1/rr**2, y)   # rot di delta A = -k/rho^2
check("F3 delta B = rot(-k/rho^2) != 0 (operatori non equivalenti di gauge)", sp.simplify(dB) != 0)

# ---------- [G] SYS-T0 ed esempio di SYS-EX (calore) ----------
s = sp.symbols('s'); xx = sp.symbols('x')
Pm = sp.Matrix([[s - 1, 1], [0, s - 2]])
aa, bb = 2, 3
uu = sp.Matrix([aa*sp.exp(xx) - bb*sp.exp(2*xx), bb*sp.exp(2*xx)])
act = lambda row, v: sum((sp.diff(v[j], xx) if row[j].has(s) else 0)*row[j].coeff(s, 1) + row[j].subs(s, 0)*v[j] for j in range(2))
ok = all(sp.simplify(act(Pm.row(i), uu)) == 0 for i in range(2))
check("G1 u = (a e^x - b e^{2x}, b e^{2x}) risolve [[s-1,1],[0,s-2]]", ok)
check("G2 Smith di [[s-1,1],[0,s-2]]: gcd minori 1x1 = 1, det = (s-1)(s-2)", sp.gcd_list(list(Pm)) == 1 and sp.factor(Pm.det()) == (s - 1)*(s - 2))
yv, tv_, xv_ = sp.symbols('y t x')
f = sp.Integral(sp.exp(yv**2*tv_ + yv*xv_), (yv, 0, 1))
heat = sp.diff(f.function, tv_) - sp.diff(f.function, xv_, 2)
check("G3 f = int_0^1 e^{y^2 t + y x} dy risolve f_t = f_xx (sezione s(y) = (y^2, y) di V(tau - xi^2))", sp.simplify(heat) == 0)

# ---------- [H] gauge: covarianza ----------
chi = sp.Function('chi')(x); Ax = sp.Function('Ax')(x); fz = sp.Function('f')(x)
lhs = sp.exp(-I*chi)*(sp.diff(sp.exp(I*chi)*fz, x) - I*(Ax + sp.diff(chi, x))*sp.exp(I*chi)*fz)
check("H1 e^{-i chi}(d - i(A + d chi)) e^{i chi} = d - i A", sp.simplify(lhs - (sp.diff(fz, x) - I*Ax*fz)) == 0)

n_ok = sum(o for _, o in RES)
print(f"\nTOTALE {n_ok}/{len(RES)} OK")
