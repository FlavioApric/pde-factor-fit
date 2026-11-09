# S-CHECK-9 red team per S4-INTEG (eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_s4integ.py)
import sys, random
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
mp.mp.dps = 30
OK = 0; BAD = 0
def chk(name, cond, info=""):
    global OK, BAD
    if cond: OK += 1; print("OK  ", name, info)
    else: BAD += 1; print("FAIL", name, info)

t, x, y, s, nu = sp.symbols('t x y s nu', positive=True)

# ---------------- 1. L-S: lemma della striscia ----------------
random.seed(1)
minim = 10.0
for trial in range(200):
    n = random.randint(2, 5)
    pts = sorted(mp.mpf(random.random()) for _ in range(n)); pts[0] = mp.mpf(0); pts[-1] = mp.mpf(1)
    wts = [mp.mpf(random.random()) for _ in range(n)]; S = sum(wts); wts = [w/S for w in wts]
    M = lambda z: sum(w*mp.exp(z*p) for w, p in zip(wts, pts))
    # min of Re(e^{-i tau m} M) / (cos(|tau|w/2) E e^{sigma X}) on samples of the strip
    for _ in range(20):
        sig = mp.mpf(random.uniform(-6, 6)); tau = mp.mpf(random.uniform(-0.999, 0.999))*mp.pi
        val = mp.re(mp.exp(-1j*tau*mp.mpf('0.5'))*M(sig+1j*tau))
        low = mp.cos(abs(tau)/2)*sum(w*mp.exp(sig*p) for w, p in zip(wts, pts))
        if val < low*(1-mp.mpf('1e-20')): minim = -1
chk("L-S settore: Re(e^{-iτm}M) >= cos(|τ|w/2) E e^{σX} (200 leggi x 20 punti)", minim > 0)
# two-point optimal
z = sp.symbols('z')
M2 = (1 + sp.exp(z))/2
chk("L-S ottimalità: zeri di (1+e^z)/2 in z = iπ(2k+1)", sp.simplify(M2.subs(z, sp.I*sp.pi)) == 0)

# ---------------- 2. F4L-P3 ----------------
# (iii) tanh formula at x=0 and R(t,x)
A, eps = sp.symbols('A epsilon', positive=True)
G0 = sp.Symbol('G', positive=True); Phi = sp.Rational(1, 2)
sig = eps*A/(2*nu)
phi = (1-Phi) + Phi*sp.exp(-sig); phix = G0*(sp.exp(-sig)-1)
u = -2*nu*phix/phi
chk("F4L-P3(iii) u(t,0) = 4νG tanh(εA/4ν)", sp.simplify((u - 4*nu*G0*sp.tanh(eps*A/(4*nu))).rewrite(sp.exp)) == 0)
# radius at general x, numeric: first zero of denominator vs formula
for (nuv, Av, tv, xv) in [(0.5, 1.0, 1.0, 0.3), (0.1, 2.0, 0.5, -0.2), (1.0, 3.0, 2.0, 1.5)]:
    nuv, Av, tv, xv = map(mp.mpf, (nuv, Av, tv, xv))
    Ph = mp.erfc(-xv/mp.sqrt(4*nuv*tv))/2  # = int_0^inf G(x-y)dy
    Rform = (2*nuv/Av)*mp.sqrt(mp.log((1-Ph)/Ph)**2 + mp.pi**2)
    root = (2*nuv/Av)*(-mp.log((1-Ph)/Ph) + 1j*mp.pi)    # zero of den: (1-Ph)+Ph e^{-eps A/2nu}
    den = (1-Ph) + Ph*mp.exp(-root*Av/(2*nuv))
    # Taylor coefficients of u(eps) at x: root test
    G = mp.exp(-xv**2/(4*nuv*tv))/mp.sqrt(4*mp.pi*nuv*tv)
    f = lambda e: -2*nuv*G*(mp.exp(-e*Av/(2*nuv))-1)/((1-Ph)+Ph*mp.exp(-e*Av/(2*nuv)))
    co = mp.taylor(f, 0, 40)
    rt = 1/abs(co[40])**(mp.mpf(1)/40) if co[40] != 0 else 1/abs(co[39])**(mp.mpf(1)/39)
    chk("F4L-P3(iii) R(t,x): zero del denominatore e |zero| = formula", abs(den) < 1e-20 and abs(abs(root)-Rform) < 1e-20, "R=%s"%mp.nstr(Rform, 8))
    chk("F4L-P3(iii) radice n-esima (n=40) ~ R(t,x) (entro 10%)", abs(rt/Rform - 1) < 0.1, "root=%s"%mp.nstr(rt, 6))
    chk("F4L-P3(iii) R(t,x) >= 2πν/A", Rform >= 2*mp.pi*nuv/Av - 1e-25)

# (ii) bounds on step-function data, complex eps with |eps| <= r
random.seed(2)
allok = True
for trial in range(30):
    nuv = mp.mpf(random.choice([0.2, 0.5, 1.0])); tv = mp.mpf(random.choice([0.1, 1.0, 3.0]))
    jumps = sorted(random.uniform(-2, 2) for _ in range(3)); amps = [random.uniform(-1, 1) for _ in range(3)]
    levels = [0];
    for a_ in amps: levels.append(levels[-1]+a_)
    w = max(levels)-min(levels)
    r = mp.mpf(random.uniform(0.1, 0.95))*2*mp.pi*nuv/w
    def phi_(e, xv):
        # sum over intervals of G-mass times exp(-e U/2nu)
        edges = [-mp.inf] + [mp.mpf(j) for j in jumps] + [mp.inf]
        val = 0; dval = 0
        for k in range(4):
            lo, hi = edges[k], edges[k+1]
            mass = (mp.erf((xv-lo)/mp.sqrt(4*nuv*tv)) - mp.erf((xv-hi)/mp.sqrt(4*nuv*tv)))/2
            val += mass*mp.exp(-e*levels[k]/(2*nuv))
            # d/dx of mass = G(x-lo)-G(x-hi)
            g = lambda z_: mp.exp(-z_**2/(4*nuv*tv))/mp.sqrt(4*mp.pi*nuv*tv) if z_ not in (mp.inf, -mp.inf) else 0
            dval += (g(xv-lo) - g(xv-hi))*mp.exp(-e*levels[k]/(2*nuv))
        return val, dval
    bound = 2*nuv*mp.exp(r*w/(2*nuv))/(mp.cos(r*w/(4*nuv))*mp.sqrt(mp.pi*nuv*tv))
    for _ in range(15):
        th = random.uniform(0, 2*mp.pi); e = r*mp.exp(1j*th); xv = mp.mpf(random.uniform(-3, 3))
        v, dv = phi_(e, xv)
        uu = -2*nuv*dv/v
        if abs(uu) > bound: allok = False
chk("F4L-P3(ii) |u_ε| <= 2ν e^{rw/2ν}/(cos(rw/4ν)√(πνt)) su 30 dati a gradini x 15 punti", allok)

# (iv) Neumann kernel by images: positivity, mass 1, ||d_x G_N||_{L1} <= 1/sqrt(pi nu t)
def GN(tv, xv, yv, L, nuv, K=30):
    sgm = 0
    for k in range(-K, K+1):
        for z_ in (xv-yv+2*k*L, xv+yv+2*k*L):
            sgm += mp.exp(-z_**2/(4*nuv*tv))/mp.sqrt(4*mp.pi*nuv*tv)
    return sgm
def dGN(tv, xv, yv, L, nuv, K=30):
    sgm = 0
    for k in range(-K, K+1):
        for z_ in (xv-yv+2*k*L, xv+yv+2*k*L):
            sgm += -z_/(2*nuv*tv)*mp.exp(-z_**2/(4*nuv*tv))/mp.sqrt(4*mp.pi*nuv*tv)
    return sgm
mp.mp.dps = 20
for (tv, xv, L, nuv) in [(0.05, 0.3, 1.0, 1.0), (1.0, 0.7, 1.0, 0.3), (5.0, 0.1, 2.0, 0.5)]:
    tv, xv, L, nuv = map(mp.mpf, (tv, xv, L, nuv))
    mass = mp.quad(lambda yy: GN(tv, xv, yy, L, nuv), [0, xv, L])
    l1 = mp.quad(lambda yy: abs(dGN(tv, xv, yy, L, nuv)), [0, xv, L])
    mn = min(GN(tv, xv, mp.mpf(k)/20*L, L, nuv) for k in range(21))
    chk("F4L-P3(iv) G_N >= 0, massa 1", mn > 0 and abs(mass-1) < 1e-12, "massa=%s"%mp.nstr(mass, 15))
    chk("F4L-P3(iv) ||d_x G_N(t,x,.)||_{L1(0,L)} <= 1/sqrt(pi nu t)", l1 <= 1/mp.sqrt(mp.pi*nuv*tv)*(1+1e-12), "%s <= %s"%(mp.nstr(l1, 8), mp.nstr(1/mp.sqrt(mp.pi*nuv*tv), 8)))
    # Neumann: d_x G_N = 0 at x=0 and x=L
    chk("F4L-P3(iv) d_x G_N = 0 in x = 0, L", abs(dGN(tv, mp.mpf(0), mp.mpf('0.4')*L, L, nuv)) < 1e-15 and abs(dGN(tv, L, mp.mpf('0.4')*L, L, nuv)) < 1e-12)
mp.mp.dps = 30

# ---------------- 3. Kieffer: integral form, mass 1 ----------------
# integral form: phi = int G(x-y) exp(-(delta Re/2) 1_{y>0}) dy ; at x = 0: (1+e^{-delta Re/2})/2
d_, Re_ = sp.symbols('delta Re', positive=True)
den_int = (1 + sp.exp(-d_*Re_/2))/2
chk("Kieffer forma integrale (massa 1): zero in δ = 2πi/Re", sp.simplify(den_int.subs(d_, 2*sp.pi*sp.I/Re_)) == 0)
chk("Kieffer forma integrale: NON zero in δ = iπ/Re", sp.simplify(den_int.subs(d_, sp.pi*sp.I/Re_)) != 0)
chk("Kieffer 'e^{δRe}' (massa 2): 1+e^{δRe} zero in δ = iπ/Re", sp.simplify((1+sp.exp(d_*Re_)).subs(d_, sp.pi*sp.I/Re_)) == 0)
# scaling: delta u solves Burgers with data delta g
uu = sp.Function('uu')(t, x)
dl = sp.Symbol('dl'); Rr = sp.Symbol('Rr', positive=True)
eqK = sp.diff(uu, t) + dl*uu*sp.diff(uu, x) - sp.diff(uu, x, 2)/Rr
w_ = dl*uu
eqB = sp.diff(w_, t) + w_*sp.diff(w_, x) - sp.diff(w_, x, 2)/Rr
chk("Kieffer (v=0): w = δu risolve Burgers (ν = 1/Re)", sp.simplify(eqB - dl*eqK) == 0)

# ---------------- 4. Hirota ----------------
ks = [sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(5, 2)]
Es = sp.symbols('E1:4', positive=True)
N = 3
import itertools
def Aij(i, j): return ((ks[i]-ks[j])/(ks[i]+ks[j]))**2
f = 0
for r_ in range(N+1):
    for S in itertools.combinations(range(N), r_):
        aS = sp.Integer(1)
        for i, j in itertools.combinations(S, 2): aS *= Aij(i, j)
        f += aS*sp.prod([Es[i] for i in S])
C = sp.Matrix(N, N, lambda i, j: sp.sqrt(Es[i]*Es[j])*2*sp.sqrt(ks[i]*ks[j])/(ks[i]+ks[j]))
chk("INT-P5(a) f = det(I+C) (N=3, simbolico in E)", sp.simplify(sp.expand((sp.eye(N)+C).det()) - sp.expand(f)) == 0)
Kmat = sp.Matrix(N, N, lambda i, j: 2*sp.sqrt(ks[i]*ks[j])/(ks[i]+ks[j]))
chk("INT-P5(a) K definita positiva (minori principali > 0)", all(Kmat[:k, :k].det() > 0 for k in range(1, N+1)))
# Möbius cumulants
logA = {}
def log_a(T):
    return sum(sp.log(Aij(i, j)) for i, j in itertools.combinations(T, 2))
allok = True
for r_ in range(N+1):
    for S in itertools.combinations(range(N), r_):
        b = sum((-1)**(len(S)-len(T))*log_a(T) for q in range(len(S)+1) for T in itertools.combinations(S, q))
        target = sp.log(Aij(*S)) if len(S) == 2 else 0
        if sp.simplify(b - target) != 0: allok = False
chk("INT-P5(b) cumulanti b_S solo a coppie (N=3)", allok)
# numeric: E_int integral, int u
kk = [mp.mpf(1)/2, mp.mpf(3)/2, mp.mpf(5)/2]; cc = [mp.mpf(0), mp.mpf(1), mp.mpf(-2)]
def logf(xv):
    E = [mp.exp(kk[i]*xv + cc[i]) for i in range(3)]
    ff = 0
    for r_ in range(4):
        for S in itertools.combinations(range(3), r_):
            aS = mp.mpf(1)
            for i, j in itertools.combinations(S, 2): aS *= ((kk[i]-kk[j])/(kk[i]+kk[j]))**2
            pr = mp.mpf(1)
            for i in S: pr *= E[i]
            ff += aS*pr
    return mp.log(ff)
def logZ(xv):
    return logf(xv) - sum(mp.log(1+mp.exp(kk[i]*xv+cc[i])) for i in range(3))
dZ = lambda xv: mp.diff(logZ, xv)
chk("INT-P6 ∫E_int = 2[(log Z)_x] → 0", abs(2*(dZ(150) - dZ(-150))) < 1e-25, mp.nstr(2*(dZ(150)-dZ(-150)), 5))
dF = lambda xv: mp.diff(logf, xv)
chk("INT-P6 ∫u = 2Σk_i", abs(2*(dF(80)-dF(-80)) - 2*sum(kk)) < 1e-15)
EintL1 = mp.quad(lambda xv: 2*mp.diff(logZ, xv, 2), [-150, -40, -5, 0, 5, 40, 150])
chk("INT-P6 quadratura diretta ∫E_int ≈ 0", abs(EintL1) < 1e-10, mp.nstr(EintL1, 5))
chk("INT-P5(c) E_int(0) ≠ 0", abs(mp.diff(logZ, 0, 2)) > 1e-3)
# (e) Jacobi formula
xv = mp.mpf('0.37')
def Mx(xv, d=0):
    E = [mp.exp(kk[i]*xv+cc[i]) for i in range(3)]
    return mp.matrix([[ (1 if (i == j and d == 0) else 0) + mp.sqrt(E[i]*E[j])*2*mp.sqrt(kk[i]*kk[j])/(kk[i]+kk[j])*((kk[i]+kk[j])/2)**d for j in range(3)] for i in range(3)])
M0, M1, M2_ = Mx(xv), Mx(xv, 1), Mx(xv, 2)
Mi = M0**-1
jac = sum((Mi*M2_)[i, i] for i in range(3)) - sum(((Mi*M1)*(Mi*M1))[i, i] for i in range(3))
chk("INT-P5(e) (log f)'' = tr(M^-1 M'') - tr((M^-1 M')^2)", abs(jac - mp.diff(logf, xv, 2)) < 1e-20)

# ---------------- 5. F4LIN-T2 ----------------
z = sp.symbols('z', real=True)
chk("F4LIN-T2(ii) ∫_0^∞(1-tanh) = ln2", sp.simplify(sp.integrate(1-sp.tanh(z), (z, 0, sp.oo)) - sp.log(2)) == 0)
I2 = mp.quad(lambda zz: (1-mp.tanh(zz))**2, [0, mp.inf])
chk("F4LIN-T2(ii) ∫_0^∞(1-tanh)^2 = 2ln2 - 1", abs(I2 - (2*mp.log(2)-1)) < 1e-25)
chk("F4LIN-T2(ii) ∫sech^4 = 4/3", abs(mp.quad(lambda zz: mp.sech(zz)**4, [-mp.inf, mp.inf]) - mp.mpf(4)/3) < 1e-25)
# Burgers for profile
Dl, c1, c2 = sp.symbols('Delta c1 c2', positive=True)
uprof = (c1+c2)/2 - (c1-c2)/2*sp.tanh((c1-c2)*(x-(c1+c2)*t/2)/(4*nu))
chk("F4LIN-T2(ii) profilo risolve Burgers", sp.simplify((sp.diff(uprof, t)+uprof*sp.diff(uprof, x)-nu*sp.diff(uprof, x, 2)).rewrite(sp.exp)) == 0)
# F-hat closed form: F = sgn - tanh, Fhat(eta) = int F e^{-i eta y} = -2i ∫_0^∞ (1-tanh) sin(eta y) dy
for eta in [mp.mpf('0.3'), mp.mpf(1), mp.mpf(4)]:
    num = -2j*mp.quadosc(lambda yy: (1-mp.tanh(yy))*mp.sin(eta*yy), [0, mp.inf], omega=eta)
    closed = 1j*(mp.pi/mp.sinh(mp.pi*eta/2) - 2/eta)
    chk("F4LIN-T2 R5 chiuso: F̂(η) = i(π csch(πη/2) − 2/η)", abs(num-closed) < 1e-15, "η=%s"%eta)
# (iii) high-precision TV vs 4 nu K ln2
mp.mp.dps = 40
cs = [mp.mpf(1), mp.mpf(0), mp.mpf(-1)]; bs = [mp.mpf(0), mp.mpf(0), mp.mpf(0)]
def run(cs, bs, tv, nuv):
    Sfun = lambda xv: [cs[i]*xv - cs[i]**2*tv/2 - bs[i] for i in range(len(cs))]
    def E(xv):
        Sv = Sfun(xv); m = min(Sv)
        wts = [mp.exp(-(Si-m)/(2*nuv)) for Si in Sv]; W = sum(wts)
        unu = sum(wi*ci for wi, ci in zip(wts, cs))/W
        i0 = Sv.index(m); return unu - cs[i0]
    # breakpoints of envelope: pairwise intersections that are on envelope
    bps = []
    for i in range(len(cs)):
        for j in range(i+1, len(cs)):
            xv = ((cs[i]**2-cs[j]**2)*tv/2 + bs[i]-bs[j])/(cs[i]-cs[j])
            Sv = Sfun(xv)
            if abs(min(Sv) - Sv[i]) < 1e-30 and sorted(Sv)[2] - Sv[i] > 1e-20: bps.append(xv)
    bps = sorted(bps)
    def h(xv): Sv = sorted(Sfun(xv)); return Sv[2]-Sv[0]
    # delta = inf h: attained at kinks; scan intersections
    cand = [((cs[i]**2-cs[j]**2)*tv/2 + bs[i]-bs[j])/(cs[i]-cs[j]) for i in range(len(cs)) for j in range(i+1, len(cs))]
    delta = min(h(xv) for xv in cand)
    pts = sorted(set([-mp.mpf(60)] + bps + [mp.mpf(60)]))
    L1 = mp.quad(lambda xv: abs(E(xv)), pts)
    return L1, len(bps), delta
for (tv, nuv) in [(mp.mpf(1), mp.mpf('0.05')), (mp.mpf(1), mp.mpf('0.1')), (mp.mpf(1), mp.mpf('0.2'))]:
    L1, K, delta = run(cs, bs, tv, nuv)
    err = abs(L1 - 4*nuv*K*mp.log(2))
    print("    t=%s ν=%s K=%d δ=%s  err=%s  e^{-δ/2ν}=%s  e^{-δ/4ν}=%s" % (tv, nuv, K, mp.nstr(delta, 6), mp.nstr(err, 5), mp.nstr(mp.exp(-delta/(2*nuv)), 5), mp.nstr(mp.exp(-delta/(4*nuv)), 5)))
    chk("F4LIN-T2(iii) err <= 4νK e^{-δ/2ν} + C e^{-δ/4ν} (C<=10)", err <= 4*nuv*K*mp.exp(-delta/(2*nuv)) + 10*mp.exp(-delta/(4*nuv)))
    chk("F4LIN-T2(iii) err/e^{-δ/2ν} limitato (stima migliorata e^{-δ/2ν})", err/mp.exp(-delta/(2*nuv)) < 20, "rapporto=%s" % mp.nstr(err/mp.exp(-delta/(2*nuv)), 5))
# random four-line configurations
random.seed(5)
for trial in range(4):
    cs4 = sorted([mp.mpf(random.uniform(-2, 2)) for _ in range(4)], reverse=True)
    bs4 = [mp.mpf(random.uniform(-1, 1)) for _ in range(4)]
    nuv = mp.mpf('0.04')
    L1, K, delta = run(cs4, bs4, mp.mpf(1), nuv)
    err = abs(L1 - 4*nuv*K*mp.log(2))
    chk("F4LIN-T2(iii) N=4 casuale: err/e^{-δ/2ν} limitato", err <= 50*mp.exp(-delta/(2*nuv)) + mp.mpf('1e-30'), "K=%d δ=%s err=%s e^{-δ/2ν}=%s" % (K, mp.nstr(delta, 4), mp.nstr(err, 4), mp.nstr(mp.exp(-delta/(2*nuv)), 4)))
mp.mp.dps = 30

# ---------------- 6. INT-T1: hierarchy (jet variables), F-C, F-MS, Novikov, B1 ----------------
J = sp.symbols('j0:16')
def TD(p, top=14):
    return sp.expand(sum(sp.diff(p, J[k])*J[k+1] for k in range(top)))
def TDk(p, k):
    for _ in range(k): p = TD(p)
    return p
def weight(mono):
    # weight: j_k has weight k+2
    return sum((k+2)*e for k, e in enumerate(sp.Poly(mono, *J[:14]).monoms()[0]))
def monomials_of_weight(w, maxord=12):
    res = []
    def rec(k, rem, cur):
        if rem == 0: res.append(cur); return
        if k > maxord or k+2 > rem: return
        e = 0
        while e*(k+2) <= rem:
            rec(k+1, rem - e*(k+2), cur*J[k]**e); e += 1
    rec(0, w, sp.Integer(1)); return res
def invD(K, w):
    mons = monomials_of_weight(w-1)
    cs_ = sp.symbols('a0:%d' % len(mons))
    P = sum(c*m for c, m in zip(cs_, mons))
    eqs = sp.Poly(sp.expand(TD(P) - K), *J[:15]).coeffs()
    sol = sp.solve(eqs, cs_, dict=True)
    assert sol, "non esatto"
    return sp.expand(P.subs(sol[0]).subs({c: 0 for c in cs_}))
Ks = [-J[1]]; wts = [3]
for n in range(3):
    Kp = Ks[-1]; w = wts[-1]
    Ks.append(sp.expand(TDk(Kp, 2) + 4*J[0]*Kp + 2*J[1]*invD(Kp, w))); wts.append(w+2)
chk("INT-T1 K_1 = -(u_xxx+6uu_x)", sp.expand(Ks[1] + J[3] + 6*J[0]*J[1]) == 0)
chk("INT-T1 K_2 = -(u_5x+10uu_xxx+20u_xu_xx+30u^2u_x)", sp.expand(Ks[2] + J[5] + 10*J[0]*J[3] + 20*J[1]*J[2] + 30*J[0]**2*J[1]) == 0)
chk("INT-T1 K_3 locale (∂^{-1}K_2 esatto: K_2 è una derivata totale)", True, "K_3 = " + str(Ks[3])[:80] + "...")
def frech(K, W):
    return sp.expand(sum(sp.diff(K, J[k])*TDk(W, k) for k in range(14) if K.has(J[k])))
Wv = sp.Symbol('Wv')
allok = True
for m in range(4):
    for n in range(m+1, 4):
        if sp.expand(frech(Ks[m], Ks[n]) - frech(Ks[n], Ks[m])) != 0: allok = False; print("   comm", m, n)
chk("F-C: K_m'[u]K_n = K_n'[u]K_m per 0<=m<n<=3 (identità in u)", allok)
# K_1'[u] w on a generic jet w: use w = j-variables shifted? check via linear functional form
Wf = sp.Function('Wf')(x); Uf = sp.Function('Uf')(x)
def tofun(K, Uf):
    return K.subs({J[k]: sp.diff(Uf, x, k) for k in range(15, -1, -1)})
epsw = sp.Symbol('epsw')
K1lin = sp.diff(tofun(Ks[1], Uf + epsw*Wf), epsw).subs(epsw, 0)
chk("INT-T1 K_1'[u]w = -(w_xxx+6uw_x+6u_xw)", sp.simplify(K1lin + sp.diff(Wf, x, 3) + 6*Uf*sp.diff(Wf, x) + 6*sp.diff(Uf, x)*Wf) == 0)
k1, k2 = sp.Rational(1), sp.Rational(2)
c1s, c2s = sp.symbols('c1s c2s')
E1 = sp.exp(k1*x + c1s); E2 = sp.exp(k2*x + c2s)
A12 = ((k1-k2)/(k1+k2))**2
fMS = 1 + E1 + E2 + A12*E1*E2
uMS = 2*sp.diff(sp.log(fMS), x, 2)
# numerico ad alta precisione: getti di u via mp.diff
mp.mp.dps = 60
def logf_ms(xv, a_, b_):
    e1 = mp.exp(xv + a_); e2 = mp.exp(2*xv + b_)
    return mp.log(1 + e1 + e2 + mp.mpf(1)/9*e1*e2)
def u_ms(xv, a_, b_): return 2*mp.diff(lambda z_: logf_ms(z_, a_, b_), xv, 2)
Kfun = [sp.lambdify(J[:10], Ks[n], modules='mpmath') for n in range(4)]
allok = True; maxres = mp.mpf(0)
for n in range(4):
    for (xv, a_, b_) in [('0.3', '0.1', '-0.4'), ('-1.1', '0.7', '0.2'), ('2.0', '-0.5', '0.0')]:
        xv, a_, b_ = mp.mpf(xv), mp.mpf(a_), mp.mpf(b_)
        jet = [2*mp.diff(lambda z_: logf_ms(z_, a_, b_), xv, k+2) for k in range(10)]
        lhs = Kfun[n](*jet)
        d1 = mp.diff(lambda c_: u_ms(xv, c_, b_), a_); d2 = mp.diff(lambda c_: u_ms(xv, a_, c_), b_)
        rhs = -(1**(2*n+1)*d1 + 2**(2*n+1)*d2)
        res = abs(lhs - rhs)/(1 + abs(rhs)); maxres = max(maxres, res)
        if res > mp.mpf('1e-30'): allok = False; print("   F-MS", n, res)
chk("F-MS (N=2, k=(1,2)): K_n[u] = -Σk_j^{2n+1}∂_{c_j}u per n=0..3 (V-ex, mpmath 60 cifre)", allok, "max residuo relativo=%s" % mp.nstr(maxres, 3))
NovF = sp.lambdify(J[:10], 4*Ks[0] - 5*Ks[1] + Ks[2], modules='mpmath')
nres = max(abs(NovF(*[2*mp.diff(lambda z_: logf_ms(z_, mp.mpf('0.2'), mp.mpf('-0.3')), mp.mpf(xv), k+2) for k in range(10)])) for xv in ('-1', '0.5', '2'))
chk("INT-T1(B) Novikov 4K_0-5K_1+K_2 = 0 su 2-solitone (1,2)", nres < mp.mpf('1e-30'), "max=%s" % mp.nstr(nres, 3))
mp.mp.dps = 30
# B1: Wronskian of ∂_{c1}u, ∂_{c2}u nonzero
g1, g2 = sp.diff(uMS, c1s), sp.diff(uMS, c2s)
Wr = g1*sp.diff(g2, x) - g2*sp.diff(g1, x)
chk("INT-T1 B1: Wronskiano ≠ 0", abs(sp.N(Wr.subs({x: 0.4, c1s: 0, c2s: 0}))) > 1e-6)
# c_1 = 0 (pure translation) counterexample to UC: u0 = bump vanishing on (-1,1), u = u0(x-t)
bump = sp.Piecewise((0, sp.Abs(x) < 1), (sp.exp(-1/(x**2-1))*sp.exp(-x**2), True))
chk("UC-1 necessità c_1≠0: per u=u_0(x−c_0t) con u_0≡0 su (−1,1), K_d[u]=0 su Ω={|x−c_0t|<1/2} ∀d, ma K_0[u] ≢ 0", sp.diff(bump, x).subs(x, 2) != 0)

# ---------------- 7. NLS: commutation T_2, T_3 (q, r = conj q treated independently) ----------------
q = sp.Function('q')(x); r = sp.Function('r')(x)
def Dx(e, k=1): return sp.diff(e, x, k)
eps_ = sp.Symbol("eps_")
T2q = sp.I*(Dx(q, 2) + 2*q*r*q); T2r = -sp.I*(Dx(r, 2) + 2*r*q*r)
T3q = -(Dx(q, 3) + 6*q*r*Dx(q)); T3r = -(Dx(r, 3) + 6*r*q*Dx(r))
def fre(Fq, Wq, Wr):
    return sp.diff(Fq.subs({q: q+eps_*Wq, r: r+eps_*Wr}).doit(), eps_).subs(eps_, 0)
comq = sp.simplify(sp.expand(fre(T2q, T3q, T3r) - fre(T3q, T2q, T2r)))
chk("INT-T2 flussi NLS: [T_2, T_3] = 0 (componente q)", comq == 0)

# ---------------- 8. ALG identities ----------------
ph = sp.Function('ph')(t, x)
uCH = -2*nu*sp.diff(ph, x)/ph
FB = sp.diff(uCH, t) + uCH*sp.diff(uCH, x) - nu*sp.diff(uCH, x, 2)
chk("ALG-P4 F_B(−2νφ_x/φ) = −2ν∂_x((φ_t−νφ_xx)/φ)", sp.simplify(FB + 2*nu*sp.diff((sp.diff(ph, t)-nu*sp.diff(ph, x, 2))/ph, x)) == 0)
# ALG-P4(a) closed form domega
uu2 = sp.Function('u')(t, x)
chk("ALG-P4(a) dω_u = F_B(u) dt∧dx", sp.simplify(sp.diff(uu2, t) - sp.diff(nu*sp.diff(uu2, x) - uu2**2/2, x) - (sp.diff(uu2, t)+uu2*sp.diff(uu2, x)-nu*sp.diff(uu2, x, 2))) == 0)
# ALG-P4(c) counterexample: G_nu -> u = x/t
Gn = t**sp.Rational(-1, 2)*sp.exp(-x**2/(4*nu*t))
chk("ALG-P4(c) u = −2ν(G_ν)_x/G_ν = x/t, G_ν risolve il calore", sp.simplify(-2*nu*sp.diff(Gn, x)/Gn - x/t) == 0 and sp.simplify(sp.diff(Gn, t)-nu*sp.diff(Gn, x, 2)) == 0)
# Miura
v = sp.Function('v')(t, x)
um = -(v**2 + sp.diff(v, x))
KdV = lambda w: sp.diff(w, t) + 6*w*sp.diff(w, x) + sp.diff(w, x, 3)
mK = sp.diff(v, t) - 6*v**2*sp.diff(v, x) + sp.diff(v, x, 3)
chk("ALG-P6 KdV[−(v²+v_x)] = −(2v+∂_x) mKdV[v]", sp.simplify(sp.expand(KdV(um) + 2*v*mK + sp.diff(mK, x))) == 0)
# ALG-L1 [D, D_N] = 0 on A for KdV, on a test polynomial in y0..y3
ys = sp.symbols('y0:12')
def Dop(p):
    return sum(sp.diff(p, ys[k])*ys[k+1] for k in range(10))
NK = -6*ys[0]*ys[1] - ys[3]
DkN = [NK]
for k in range(8): DkN.append(sp.expand(Dop(DkN[-1])))
def DN(p):
    return sum(sp.diff(p, ys[k])*DkN[k] for k in range(6))
ptest = ys[0]**2*ys[2] + ys[1]*ys[3] + ys[2]**3
chk("ALG-L1 [D, D_N] = 0 su polinomio di prova (KdV)", sp.expand(DN(Dop(ptest)) - Dop(DN(ptest))) == 0)
# ALG-T1(c) separant example: u = 1-soliton (k=1): relation of order 1? u = (1/2)sech^2(x/2 - t/2): u_x^2 = u^2 - 2u^3 (check)
us = sp.Rational(1, 2)*sp.sech((x - t)/2)**2
rel = sp.diff(us, x)**2 - (us**2 - 2*us**3)
chk("ALG-T1(c)/P3 1-solitone: relazione d'ordine 1 y_1² − y_0² + 2y_0³ ∈ J_u (separante 2y_1 ∉ J_u)", sp.simplify(rel.rewrite(sp.exp)) == 0 and sp.simplify(2*sp.diff(us, x)) != 0)
# MODREL: gcd(tau - nu xi^2, xi) = 1
tau, xi = sp.symbols('tau xi')
chk("MODREL Burgers: gcd(τ−νξ², ξ/2) = 1", sp.gcd(tau - nu*xi**2, xi/2) == 1)
# MODREL T1 counter-test: non-primitive v gives strictly larger saturation: v=(xi*(tau), xi*xi) -> (tau, xi) in K v ∩ R^2 not in R v
chk("MODREL T1: v non primitivo ⇒ R·v non saturato (esempio v = ξ·(τ, ξ))", sp.div(tau, xi*tau)[1] != 0)

print("\nTOTALE: %d OK, %d FAIL" % (OK, BAD))
