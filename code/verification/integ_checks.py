# S4-INTEG: controlli simbolici/numerici (solo verifica, k3).
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I integ_checks.py
import sympy as sp, mpmath as mp, random, itertools
res = []
def chk(name, ok):
    res.append((name, bool(ok))); print(("OK  " if ok else "FAIL"), name, flush=True)

t, x, nu = sp.symbols('t x nu', real=True)

# ---------- ALG-P4: identita di Cole-Hopf ----------
phi = sp.Function('phi')(t, x)
u = -2*nu*sp.diff(phi, x)/phi
FB = sp.diff(u, t) + u*sp.diff(u, x) - nu*sp.diff(u, x, 2)
rhs = -2*nu*sp.diff((sp.diff(phi, t) - nu*sp.diff(phi, x, 2))/phi, x)
chk("ALG-P4 F_B(-2nu phi_x/phi) = -2nu d_x((phi_t - nu phi_xx)/phi)", sp.simplify(FB - rhs) == 0)

# ---------- ALG-P6: Miura ----------
v = sp.Function('v')(t, x)
U = -(v**2 + sp.diff(v, x))
KdV = lambda w: sp.diff(w, t) + 6*w*sp.diff(w, x) + sp.diff(w, x, 3)
mK = sp.diff(v, t) - 6*v**2*sp.diff(v, x) + sp.diff(v, x, 3)
chk("ALG-P6 KdV[-(v^2+v_x)] = -(2v+d_x) mKdV[v]", sp.simplify(KdV(U) + (2*v*mK + sp.diff(mK, x))) == 0)

# ---------- ALG-L1: [D, D_N] = 0 sul getto ----------
y = sp.symbols('y0:14')
def D(p): return sum(sp.diff(p, y[k])*y[k+1] for k in range(12))
def DN(p, N):
    out = 0; q = N
    for k in range(8):
        out += sp.diff(p, y[k])*q; q = D(q)
    return out
test = y[0]**2*y[2] + y[1]**3*y[0]
for name, N in [("Burgers", -y[0]*y[1] + nu*y[2]), ("KdV", -6*y[0]*y[1] - y[3])]:
    chk("ALG-L1 [D,D_N]=0 su polinomio di prova, " + name, sp.expand(D(DN(test, N)) - DN(D(test), N)) == 0)

# ---------- MODREL: primitivita della relazione di Burgers ----------
tau, xi = sp.symbols('tau xi')
chk("MODREL gcd(tau - nu xi^2, xi/2) = 1", sp.gcd(tau - nu*xi**2, xi) == 1)

# ---------- Hirota: determinante di Cauchy, Z, integrale ----------
N = 3
k = sp.symbols('k1:4', positive=True); E = sp.symbols('E1:4', positive=True)
A = lambda i, j: ((k[i]-k[j])/(k[i]+k[j]))**2
f = 0
for mu in itertools.product([0, 1], repeat=N):
    term = 1
    for i in range(N):
        if mu[i]: term *= E[i]
    for i in range(N):
        for j in range(i+1, N):
            if mu[i] and mu[j]: term *= A(i, j)
    f += term
C = sp.Matrix(N, N, lambda i, j: sp.sqrt(E[i]*E[j])*2*sp.sqrt(k[i]*k[j])/(k[i]+k[j]))
chk("Hirota f = det(I+C) (N=3, determinante di Cauchy)", sp.simplify(sp.expand((sp.eye(N)+C).det()) - sp.expand(f)) == 0)
p = [E[i]/(1+E[i]) for i in range(N)]
Z = 0
for mu in itertools.product([0, 1], repeat=N):
    term = 1
    for i in range(N): term *= p[i] if mu[i] else (1-p[i])
    for i in range(N):
        for j in range(i+1, N):
            if mu[i] and mu[j]: term *= A(i, j)
    Z += term
chk("Hirota Z = f/prod(1+E_i) = E_mu[prod A_ij^{mu_i mu_j}]", sp.simplify(Z - f/sp.prod([1+e for e in E])) == 0)

mp.mp.dps = 30
kv = [mp.mpf(1), mp.mpf('1.7'), mp.mpf('2.6')]; cv = [mp.mpf('0.3'), mp.mpf(-1), mp.mpf('0.5')]
def logZ(X):
    Ev = [mp.e**(kv[i]*X + cv[i]) for i in range(3)]
    fv = 0
    for mu in itertools.product([0, 1], repeat=3):
        term = mp.mpf(1)
        for i in range(3):
            if mu[i]: term *= Ev[i]
        for i in range(3):
            for j in range(i+1, 3):
                if mu[i] and mu[j]: term *= ((kv[i]-kv[j])/(kv[i]+kv[j]))**2
        fv += term
    return mp.log(fv) - sum(mp.log(1+e) for e in Ev)
dlZ = lambda X: mp.diff(logZ, X)
I = 2*(dlZ(40) - dlZ(-40))
Eint0 = 2*mp.diff(logZ, 0, 2)
chk("Hirota INT-P6: int E_int dx = 2[(log Z)_x] ~ 0 (N=3, |.|<1e-12)", abs(I) < 1e-12)
chk("Hirota: E_int(0) != 0 per k distinti (N=3)", abs(Eint0) > 1e-3)
PA = mp.fprod([((kv[i]-kv[j])/(kv[i]+kv[j]))**2 for i in range(3) for j in range(i+1, 3)])
chk("Hirota: Z(+inf) = prod A_ij < 1", abs(mp.e**logZ(60) - PA) < 1e-15 and PA < 1)

# ---------- INT-T1(c): N-solitone multi-tempo e K_n ----------
def kdv_flows(uexpr, X):
    ux = [uexpr]
    for m in range(1, 6): ux.append(sp.diff(ux[m-1], X))
    K0 = -ux[1]
    K1 = -(ux[3] + 6*ux[0]*ux[1])
    K2 = -(ux[5] + 10*ux[0]*ux[3] + 20*ux[1]*ux[2] + 30*ux[0]**2*ux[1])
    return [K0, K1, K2]
X = sp.symbols('X', real=True); cs = sp.symbols('c1:3', real=True)
def soliton(kk):
    n_ = len(kk)
    Es = [sp.exp(kk[i]*X + cs[i]) for i in range(n_)]
    if n_ == 1: fq = 1 + Es[0]
    else: fq = 1 + Es[0] + Es[1] + ((kk[0]-kk[1])/(kk[0]+kk[1]))**2*Es[0]*Es[1]
    return 2*sp.diff(sp.log(fq), X, 2)
pts = [{X: sp.Rational(1, 3), cs[0]: sp.Rational(1, 5), cs[1]: sp.Rational(-2, 7)},
       {X: sp.Rational(-3, 4), cs[0]: sp.Rational(2, 3), cs[1]: sp.Rational(1, 2)}]
for kk in [(sp.Integer(1),), (sp.Integer(1), sp.Integer(2)), (sp.Rational(1, 2), sp.Rational(3, 2))]:
    uq = soliton(kk); Ks = kdv_flows(uq, X)
    for n in range(3):
        target = -sum(kk[j]**(2*n+1)*sp.diff(uq, cs[j]) for j in range(len(kk)))
        ok = all(abs(sp.N((Ks[n]-target).subs(pt), 40)) < 1e-30 for pt in pts)
        chk(f"INT-T1(c) K_{n}[u] = -sum_j k_j^(2n+1) d_cj u, k={kk}", ok)
kk = (sp.Integer(1), sp.Integer(2)); uq = soliton(kk); Ks = kdv_flows(uq, X)
d = [kk[0]**2*kk[1]**2, -(kk[0]**2+kk[1]**2), 1]
Kd = sum(d[n]*Ks[n] for n in range(3))
chk("INT-T1(c) Novikov: 4K0 - 5K1 + K2 = 0 sul 2-solitone k=(1,2)",
    all(abs(sp.N(Kd.subs({X: xx, cs[0]: sp.Rational(1, 3), cs[1]: sp.Rational(-1, 2)}), 40)) < 1e-30
        for xx in [sp.Integer(-2), sp.Rational(1, 7), sp.Rational(5, 2)]))
w1 = sp.diff(uq, cs[0]); w2 = sp.diff(uq, cs[1])
W = (w1*sp.diff(w2, X) - w2*sp.diff(w1, X)).subs({X: sp.Rational(1, 3), cs[0]: 0, cs[1]: 0})
chk("INT-T1(c) d_c1 u, d_c2 u linearmente indipendenti (Wronskiano != 0)", abs(sp.N(W, 30)) > 1e-6)

# ---------- F4LIN-T2 ----------
z = sp.symbols('z', positive=True); Dl = sp.symbols('Delta', positive=True); nup = sp.symbols('nup', positive=True)
chk("F4LIN-T2(ii) int_0^inf (1-tanh) = ln 2", sp.simplify(sp.integrate(1-sp.tanh(z), (z, 0, sp.oo)) - sp.log(2)) == 0)
I2 = sp.integrate((1-sp.tanh(z))**2, (z, 0, sp.oo))
chk("F4LIN-T2(ii) ||E||_L2^2 = 4 nu Delta (ln2 - 1/2)",
    sp.simplify((Dl**2/4)*(4*nup/Dl)*2*I2 - 4*nup*Dl*(sp.log(2) - sp.Rational(1, 2))) == 0)
yv = sp.symbols('y', real=True)
uprof = -(Dl/2)*sp.tanh(Dl*yv/(4*nup))
H1 = sp.integrate(sp.diff(uprof, yv)**2, (yv, -sp.oo, sp.oo))
chk("F4LIN-T2(ii) |u^nu|_H1^2 = Delta^3/(12 nu)", sp.simplify(H1 - Dl**3/(12*nup)) == 0)
c1, c2, b1, b2 = sp.symbols('c1 c2 b1 b2', real=True)
S1 = c1*x - c1**2*t/2 - b1; S2 = c2*x - c2**2*t/2 - b2
uv = sp.diff(-2*nu*sp.log(sp.exp(-S1/(2*nu)) + sp.exp(-S2/(2*nu))), x)
xs = (c1+c2)*t/2 + (b1-b2)/(c1-c2)
prof = (c1+c2)/2 - (c1-c2)/2*sp.tanh((c1-c2)*(x-xs)/(4*nu))
num = [{c1: 3, c2: -1, b1: sp.Rational(1, 2), b2: -1, t: sp.Rational(7, 5), x: sp.Rational(1, 3), nu: sp.Rational(1, 4)},
       {c1: 2, c2: sp.Rational(1, 2), b1: 0, b2: 1, t: 1, x: -2, nu: sp.Rational(1, 10)}]
chk("F4LIN-T2(ii) u^nu = profilo tanh", all(abs(sp.N((uv-prof).subs(pt), 30)) < 1e-25 for pt in num))
Bu = sp.diff(uv, t) + uv*sp.diff(uv, x) - nu*sp.diff(uv, x, 2)
chk("F4LIN-T2 u^nu risolve Burgers_nu", all(abs(sp.N(Bu.subs(pt), 30)) < 1e-25 for pt in num))
# (iii) N=3, K=2 a t=1: L1 = 8 nu ln2 + O(exp)
cl = [mp.mpf(2), mp.mpf(0), mp.mpf(-2)]; bl = [mp.mpf(0), mp.mpf(3), mp.mpf(0)]   # S1 = -3: inviluppo con 3 rette, rotture in X = -1/2, +1/2
def L1err(nv):
    def Dp(Xv):  # D' = u^nu - u^0 = sum w_i c_i - c_{argmin}
        S = [cl[i]*Xv - cl[i]**2/2 - bl[i] for i in range(3)]; m = min(S); im = S.index(m)
        w = [mp.e**(-(Si-m)/(2*nv)) for Si in S]; Wt = sum(w)
        return sum(w[i]*cl[i] for i in range(3))/Wt - cl[im]
    # rotture: S0=S1 in X=-1/2, S1=S2 in X=+1/2
    val = mp.quad(lambda Xv: abs(Dp(Xv)), [-20, -0.5, 0.5, 20])
    return val, abs(val - 8*nv*mp.log(2))
for nv in [mp.mpf('0.05'), mp.mpf('0.02')]:
    val, err = L1err(nv)
    chk(f"F4LIN-T2(iii) N=3,K=2,nu={nv}: L1={mp.nstr(val,10)}, |L1-8nu ln2|={mp.nstr(err,3)} <= exp(-delta/4nu)={mp.nstr(mp.e**(-2/(4*nv)),3)} (delta=2)", err <= mp.e**(-2/(4*nv)))

# ---------- F4L-P3 ----------
random.seed(7); worst = mp.inf
for trial in range(400):
    pr = [random.random() for _ in range(4)]; S_ = sum(pr); pr = [q/S_ for q in pr]
    for zr in mp.polyroots([pr[3], pr[2], pr[1], pr[0]]):   # atomi 0,1/3,2/3,1: z = e^{s/3}
        worst = min(worst, abs(mp.im(3*mp.log(zr))))         # Im s mod 6pi: il ramo principale da' |Im s|<=3pi
chk(f"F4L-P3 striscia: min |Im s| sugli zeri (400 leggi a 4 atomi su [0,1]) = {mp.nstr(worst,8)} >= pi", worst >= mp.pi - mp.mpf(10)**-20)
A_ = mp.mpf('1.3'); nv = mp.mpf('0.4'); tv = mp.mpf('0.7')
Gt = lambda Xv: mp.e**(-Xv**2/(4*nv*tv))/mp.sqrt(4*mp.pi*nv*tv)
def uCH(eps, Xv):
    Phi = mp.erfc(-Xv/(2*mp.sqrt(nv*tv)))/2; s_ = eps*A_/(2*nv)
    return -2*nv*Gt(Xv)*(mp.e**(-s_)-1)/((1-Phi) + Phi*mp.e**(-s_))
chk("F4L-P3(ii) u(t,0) = 4 nu G tanh(eps A/4nu)", abs(uCH(mp.mpf('0.9'), 0) - 4*nv*Gt(0)*mp.tanh(mp.mpf('0.9')*A_/(4*nv))) < 1e-20)
co = mp.taylor(lambda e: uCH(e, 0), 0, 25)
r = abs(co[25])**(-mp.mpf(1)/25)
chk(f"F4L-P3(ii) radice dei coeff. n=25 ({mp.nstr(r,5)}) ~ 2pi nu/A ({mp.nstr(2*mp.pi*nv/A_,5)})", abs(r/(2*mp.pi*nv/A_) - 1) < 0.1)
# versione su (0,L), u=0 al bordo <-> phi_x=0 (Neumann): nucleo >=0 di massa 1
mp.mp.dps = 20
Lf = mp.mpf(1); nv = mp.mpf('0.05'); tv = mp.mpf('0.3')
def GN(Xv, Yv, M=30):
    return (1 + 2*sum(mp.e**(-nv*(n*mp.pi/Lf)**2*tv)*mp.cos(n*mp.pi*Xv/Lf)*mp.cos(n*mp.pi*Yv/Lf) for n in range(1, M)))/Lf
U0 = lambda Yv: mp.sin(2*mp.pi*Yv)  # u0 = 2pi cos(2pi y): U0(0)=U0(L)=0, osc = 2
Xp = mp.mpf('0.25')
nodes = [GN(Xp, Yv) for Yv in mp.linspace(0, 1, 101)]
chk("F4L-P3 Neumann: nucleo >= 0 nei nodi e massa 1", min(nodes) > -1e-12 and abs(mp.quad(lambda Yv: GN(Xp, Yv), [0, 1]) - 1) < 1e-12)
def phiN(eps): return mp.quad(lambda Yv: GN(Xp, Yv)*mp.e**(-eps*U0(Yv)/(2*nv)), [0, 0.25, 0.5, 0.75, 1])
bound = 2*mp.pi*nv/2
vals = [abs(phiN(a*bound + 1j*b*bound)) for a in [-2, 0, 2] for b in [-0.99, -0.5, 0.5, 0.99]]
chk(f"F4L-P3 Neumann: |phi_eps| > 0 su un campione della striscia |Im eps| < 2 pi nu/osc (min {mp.nstr(min(vals),4)})", min(vals) > 0)
# Kieffer et al.: forma integrale (massa 1, v=0) contro formula esplicita stampata
mp.mp.dps = 25
Re = mp.mpf(4); tv = mp.mpf(1)
def uK_int(dl, Xv):
    a = Xv/(2*mp.sqrt(tv/Re)); E_ = mp.erfc(a)            # 2*(1-Phi)
    Phi2 = 2 - E_                                         # 2*Phi, Phi=P(Y>0)
    G = mp.e**(-Xv**2*Re/(4*tv))/mp.sqrt(4*mp.pi*tv/Re)
    s_ = dl*Re/2
    phi_ = (E_ + Phi2*mp.e**(-s_))/2; phix = G*(mp.e**(-s_) - 1)
    return -2/(dl*Re)*phix/phi_
def uK_30(dl, Xv, ex):
    a = Xv/(2*mp.sqrt(tv/Re))
    return 2*(mp.e**(ex*dl*Re)-1)*mp.e**(-Xv**2/(4*tv/Re))/(dl*mp.sqrt(mp.pi*Re*tv)*(2+(mp.e**(ex*dl*Re)-1)*mp.erfc(a)))
d0 = mp.mpf('0.3'); X0 = mp.mpf('0.2')
ui = uK_int(d0, X0)
chk("Kieffer: forma integrale (massa 1) = formula esplicita con e^{delta Re/2}, NON con e^{delta Re}",
    abs(ui - uK_30(d0, X0, mp.mpf(1)/2)) < 1e-15 and abs(ui - uK_30(d0, X0, 1)) > 1e-4)
den = lambda dl: (mp.erfc(0) + (2-mp.erfc(0))*mp.e**(-dl*Re/2))/2
z0 = mp.findroot(den, mp.mpc(0.1, 1.5))
numz = mp.e**(-z0*Re/2) - 1
chk(f"Kieffer forma integrale, x=0: zero del denominatore delta = {mp.nstr(z0,8)} = 2 pi i/Re, numeratore != 0 (polo)", abs(z0 - 2j*mp.pi/Re) < 1e-15 and abs(numz) > 1)
print("\nTOTALE: %d/%d OK" % (sum(o for _, o in res), len(res)))
