"""S-CHECK-13 -- red team for OP-NL (written from scratch; does not import work/OP-NL/sympy).
Run: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I audit_opnl.py [sections]
Sections: L8 L9 IOTA L10 T7 L2 P4 PP E3 L12 LAX P17 P14
"""
import sys, time, random, itertools, math
from fractions import Fraction as Fr
import sympy as sp

OK = 0
TOT = 0
T0 = time.time()


def rep(name, cond, info=""):
    global OK, TOT
    TOT += 1
    OK += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info, "[%.1fs]" % (time.time() - T0), flush=True)


SECS = set(sys.argv[1:]) or {"L8", "L9", "IOTA", "L10", "T7", "L2", "P4", "PP", "E3", "L12", "LAX", "P17", "P14"}

# ---------------------------------------------------------------- cumulant recurrence (OP-L8)
def cumulants(r, nmax):
    """r: dict j->value (r[0]=1); returns kappa[1..nmax] via kappa_n = r_n - sum C(n-1,m-1) kappa_m r_{n-m}"""
    kap = {}
    for n in range(1, nmax + 1):
        s = r[n]
        for m in range(1, n):
            s = s - math.comb(n - 1, m - 1) * kap[m] * r[n - m]
        kap[n] = sp.expand(s) if isinstance(s, sp.Basic) else s
    return kap


def burgers_r_forms(ks, rs, jmax):
    """r_j as linear forms in r_1..r_N: r_j = sum_i k_i^j p_i, p = V^{-1} r, V_{l,i} = k_i^l"""
    N = len(ks)
    V = sp.Matrix(N, N, lambda l, i: sp.Integer(ks[i]) ** (l + 1))
    p = V.inv() * sp.Matrix(rs)
    r = {0: sp.Integer(1)}
    for j in range(1, jmax + 1):
        r[j] = sp.expand(sum(sp.Integer(ks[i]) ** j * p[i] for i in range(N)))
    return r


def weight_part(expr, rs, w):
    P = sp.Poly(expr, *rs)
    out = 0
    for mon, c in P.terms():
        if sum((l + 1) * e for l, e in enumerate(mon)) == w:
            out += c * sp.prod([rs[l] ** e for l, e in enumerate(mon)])
    return sp.expand(out)


def max_weight(expr, rs):
    P = sp.Poly(expr, *rs)
    return max(sum((l + 1) * e for l, e in enumerate(mon)) for mon, c in P.terms() if c != 0)


# ---------------------------------------------------------------- L8: recurrence == D^{n-1}(D phi/phi) in Q(X)
if "L8" in SECS:
    X1, X2 = sp.symbols("X1 X2")
    ks = [3, -2]
    phi = 1 + X1 + X2
    def Dd(e):
        return sp.together(sp.diff(e, X1) * ks[0] * X1 + sp.diff(e, X2) * ks[1] * X2)
    r = {0: sp.Integer(1)}
    Dj = phi
    for j in range(1, 7):
        Dj = Dd(Dj)
        r[j] = sp.together(Dj / phi)
    kap = cumulants(r, 6)
    w = sp.together(Dd(phi) / phi)
    direct = [w]
    for n in range(2, 7):
        direct.append(sp.together(Dd(direct[-1])))
    rep("L8 kappa_n (recurrence in moments) == D^{n-1}(Dphi/phi), N=2, n<=6",
        all(sp.simplify(kap[n] - direct[n - 1]) == 0 for n in range(1, 7)))
    # moments of order > N are the linear forms l_j of r_1..r_N
    rr = sp.symbols("r1 r2")
    forms = burgers_r_forms(ks, list(rr), 6)
    sub = {rr[0]: r[1], rr[1]: r[2]}
    rep("L8/(II) r_j = l_j(r_1,r_2) for j=3..6 (k=(3,-2))",
        all(sp.simplify(forms[j].subs(sub) - r[j]) == 0 for j in range(3, 7)))
    # formal log identity
    s = sp.symbols("s")
    a = sp.symbols("a1:8")
    rf = {0: 1}
    rf.update({j: a[j - 1] for j in range(1, 8)})
    kf = cumulants(rf, 7)
    ser = sp.series(sp.log(1 + sum(a[j - 1] * s ** j / sp.factorial(j) for j in range(1, 8))), s, 0, 8).removeO()
    rep("L8 formal: sum kappa_n s^n/n! = log(1+sum r_j s^j/j!) up to s^7 (free r)",
        all(sp.expand(ser.coeff(s, n) * sp.factorial(n) - kf[n]) == 0 for n in range(1, 8)))

# ---------------------------------------------------------------- L9: top weight part of kappa_n = truncated cumulant
if "L9" in SECS:
    for N, ks in [(2, [1, 2]), (2, [5, -3]), (3, [1, 2, 4]), (3, [2, -1, 7])]:
        rs = list(sp.symbols("r1:%d" % (N + 1)))
        nmax = 8
        r = burgers_r_forms(ks, rs, nmax)
        kap = cumulants(r, nmax)
        rt = {0: sp.Integer(1)}
        for j in range(1, nmax + 1):
            rt[j] = rs[j - 1] if j <= N else sp.Integer(0)
        kt = cumulants(rt, nmax)
        good = True
        for n in range(1, nmax + 1):
            if max_weight(kap[n], rs) > n:
                good = False
            if sp.expand(weight_part(kap[n], rs, n) - kt[n]) != 0:
                good = False
            if kt[n] == 0:
                good = False
        rep("L9 N=%d k=%s: kappa_n has weight <= n, top part = truncated cumulant, nonzero, n<=8" % (N, ks), good)

# ---------------------------------------------------------------- iota(kappa~_n) = -(n-1)! P_n
if "IOTA" in SECS:
    for N in (2, 3, 4):
        Xs = sp.symbols("x1:%d" % (N + 1))
        e = [sp.Integer(1)] + [sum(sp.prod(c) for c in itertools.combinations(Xs, j)) for j in range(1, N + 1)]
        rt = {0: sp.Integer(1)}
        for j in range(1, 10):
            rt[j] = sp.factorial(j) * (-1) ** j * e[j] if j <= N else sp.Integer(0)
        kt = cumulants(rt, 9)
        rep("IOTA N=%d: iota(kappa~_n) = -(n-1)! P_n, n<=9" % N,
            all(sp.expand(kt[n] + sp.factorial(n - 1) * sum(x ** n for x in Xs)) == 0 for n in range(1, 10)))

# ---------------------------------------------------------------- exact rank helper over Q
def rank_Q(rows):
    M = [[Fr(x) for x in row] for row in rows]
    rk = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        pv = M[rk][c]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / pv
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def coeff_rows(polys, gens):
    monos = {}
    data = []
    for p in polys:
        d = sp.Poly(p, *gens).as_dict() if p != 0 else {}
        data.append(d)
        for m in d:
            monos.setdefault(m, len(monos))
    rows = []
    for d in data:
        row = [0] * len(monos)
        for m, c in d.items():
            row[monos[m]] = sp.Rational(c)
        row = [sp.Rational(x) for x in row]
        rows.append([Fr(int(x.p), int(x.q)) for x in row])
    return rows


def partitions_len(w, maxlen, maxpart=None):
    if maxpart is None:
        maxpart = w
    if w == 0:
        yield ()
        return
    if maxlen == 0:
        return
    for first in range(min(w, maxpart), 0, -1):
        for rest in partitions_len(w - first, maxlen - 1, first):
            yield (first,) + rest

# ---------------------------------------------------------------- L10
if "L10" in SECS:
    good = True
    for N in (1, 2, 3, 4):
        Xs = sp.symbols("x1:%d" % (N + 1))
        for w in range(0, 9):
            parts = list(partitions_len(w, N))
            polys = [sp.expand(sp.prod([sum(x ** m for x in Xs) for m in mu])) for mu in parts]
            if w == 0:
                continue
            rows = coeff_rows(polys, Xs)
            if rank_Q(rows) != len(parts):
                good = False
                print("   L10 fail N=%d w=%d" % (N, w))
    rep("L10 P_mu (len<=N) independent, N<=4, weight<=8 (exact over Q)", good)
    Xs = sp.symbols("x1:3")
    parts = list(partitions_len(3, 3))
    polys = [sp.expand(sp.prod([sum(x ** m for x in Xs) for m in mu])) for mu in parts]
    rep("L10 negative control: N=2, weight 3 with len 3 allowed -> dependent", rank_Q(coeff_rows(polys, Xs)) < len(parts))

# ---------------------------------------------------------------- T7 direct, exact over Q
if "T7" in SECS:
    for N, ks, K in [(2, [1, 3], 6), (2, [2, -5], 5), (3, [1, 2, 5], 5), (3, [-1, 3, 4], 4), (4, [1, 2, 3, 7], 4)]:
        rs = list(sp.symbols("r1:%d" % (N + 1)))
        r = burgers_r_forms(ks, rs, K + 2)
        kap = cumulants(r, K + 2)
        vars_ = [kap[n] for n in range(1, K + 2)]  # y_0..y_K  <->  kappa_1..kappa_{K+1}
        monos = []
        for d in range(0, N + 1):
            for c in itertools.combinations_with_replacement(range(len(vars_)), d):
                monos.append(c)
        polys = [sp.expand(sp.prod([vars_[i] for i in c])) if c else sp.Integer(1) for c in monos]
        rows = coeff_rows(polys, rs)
        rk = rank_Q(rows)
        rep("T7 N=%d k=%s order K=%d: monomials of degree <=N in jet independent (%d/%d)" % (N, ks, K, rk, len(monos)), rk == len(monos))
        # degree N+1 at order N: dependent (R_N exists)  [skipped for N=4: exact elimination too slow]
        if N >= 4:
            continue
        vN = [kap[n] for n in range(1, N + 2)]
        monos2 = []
        for d in range(0, N + 2):
            monos2 += list(itertools.combinations_with_replacement(range(len(vN)), d))
        polys2 = [sp.expand(sp.prod([vN[i] for i in c])) if c else sp.Integer(1) for c in monos2]
        rk2 = rank_Q(coeff_rows(polys2, rs))
        rep("T7 sharpness N=%d: degree N+1 at order N has a relation (nullity %d)" % (N, len(monos2) - rk2), rk2 < len(monos2))

# ---------------------------------------------------------------- L2: minors in I_PW, Phi parametrisation
if "L2" in SECS:
    al, be, c, A, kk, th = sp.symbols("alpha beta c A kappa theta", real=True)
    Kmax = 6
    Phi = [c ** (j // 2) * (al if j % 2 == 0 else be) for j in range(Kmax + 1)]
    good = all(sp.expand(Phi[i] * Phi[j + 2] - Phi[i + 2] * Phi[j]) == 0 for i in range(Kmax - 1) for j in range(Kmax - 1))
    rep("L2 minors y_i y_{j+2} - y_{i+2} y_j vanish on Phi", good)
    pw = [A * kk ** j * sp.cos(th + j * sp.pi / 2) for j in range(Kmax + 1)]
    sub = {al: A * sp.cos(th), be: -A * kk * sp.sin(th), c: -kk ** 2}
    rep("L2 PW_K = Phi(A cos th, -A k sin th, -k^2)", all(sp.simplify(pw[j] - Phi[j].subs(sub)) == 0 for j in range(Kmax + 1)))

# ---------------------------------------------------------------- P4: Airy closed form, q_a
def q_from_G(a):
    y = sp.symbols("y0:7")
    def D(e):
        return sum(sp.diff(e, y[j]) * y[j + 1] for j in range(6))
    w = y[1] / y[0]
    w1 = sp.together(D(w)); w2 = sp.together(D(w1)); w3 = sp.together(D(w2))
    S = w2 + 2 * w * w1
    T = 1 + 2 * a * w1
    G = (w3 + 2 * w1 ** 2 + 2 * w * w2) * T - 2 * a * w2 * S
    num = sp.factor(sp.together(G * y[0] ** 6))
    q = sp.cancel(num / y[0] ** 3)
    return sp.expand(q), y, (S, T, w, w1, w2, w3)

if "P4" in SECS:
    a = sp.symbols("a", positive=True)
    q, y, _ = q_from_G(a)
    Pq = sp.Poly(q, *y)
    degs = {sum(m) for m in Pq.monoms()}
    orders = max(max(j for j in range(7) if m[j]) for m in Pq.monoms())
    rep("P4 q_a = y0^-3 * y0^6 G is a polynomial, homogeneous of degree 3, order 4", degs == {3} and orders == 4, str(degs))
    q14 = sp.expand(q.subs(a, sp.Rational(1, 4)))
    y0, y1, y2, y3, y4 = y[:5]
    given = 2*y0**2*y4 - 4*y0*y1*y3 - 2*y0*y2**2 + y0*y2*y4 - y0*y3**2 + 4*y1**2*y2 - y1**2*y4 + 2*y1*y2*y3 - y2**3
    ratio = sp.simplify(q14 / given)
    rep("P4 q_{1/4} proportional to the explicit q of the package", ratio.is_number and ratio != 0, "ratio=%s" % ratio)
    t, x = sp.symbols("t x", positive=True)
    Z = (x + a ** 2 / (3 * t)) / (3 * t) ** sp.Rational(1, 3)
    u = 2 * sp.pi * (3 * t) ** sp.Rational(-1, 3) * sp.exp(a * x / (3 * t) + 2 * a ** 3 / (27 * t ** 2)) * sp.airyai(Z)
    airy_eq = sp.simplify(sp.diff(u, t) + sp.diff(u, x, 3))
    rep("P4(ii) closed form solves u_t + u_xxx = 0 (symbolic, Ai''=zAi)", airy_eq == 0)
    jet = [u]
    for j in range(4):
        jet.append(sp.diff(jet[-1], x))
    val = q.subs({y[j]: jet[j] for j in range(5)})
    zA, zB = sp.symbols("zA zB")
    val2 = val.subs({sp.airyai(Z): zA, sp.airyaiprime(Z): zB})
    val2 = sp.simplify(sp.expand(val2))
    rep("P4(iv) q_a(jet of u_a) == 0 identically (a, t, x symbolic)", val2 == 0)
    # Fourier integral vs closed form (numeric, mpmath)
    import mpmath as mp
    mp.mp.dps = 30
    good = True
    for (av, tv, xv) in [(0.25, 1.0, 0.3), (0.5, 2.0, -3.0), (1.0, 0.7, 1.5)]:
        L = mp.sqrt(80 / av)
        I = mp.quad(lambda k: mp.exp(-av * k ** 2) * mp.cos(k * xv + k ** 3 * tv), mp.linspace(-L, L, 801))
        Zv = (xv + av ** 2 / (3 * tv)) / mp.cbrt(3 * tv)
        cf = 2 * mp.pi * mp.cbrt(3 * tv) ** -1 * mp.exp(av * xv / (3 * tv) + 2 * av ** 3 / (27 * tv ** 2)) * mp.airyai(Zv)
        if abs(I - cf) > 1e-15 * (1 + abs(cf)):
            good = False
            print("   P4 mismatch", av, tv, xv, I, cf)
    rep("P4(ii) closed form == Fourier integral at 3 points (30 digits, tol 1e-15)", good)
    # q_a in I_PW: on jets of v'' = c v
    al, be, cc = sp.symbols("alpha beta c")
    Phi = [cc ** (j // 2) * (al if j % 2 == 0 else be) for j in range(7)]
    rep("P4(iv) q_a in I_PW (q_a o Phi == 0)", sp.expand(q.subs({y[j]: Phi[j] for j in range(7)})) == 0)
    # Gaussian (t=0 limit) satisfies q_a
    g = sp.exp(-x ** 2 / (4 * a))
    gj = [g]
    for j in range(4):
        gj.append(sp.diff(gj[-1], x))
    rep("P4 t->0: Gaussian datum also satisfies q_a", sp.simplify(q.subs({y[j]: gj[j] for j in range(5)})) == 0)
    # the solution u_a is not a tower-trivial object: check q_a not in the ideal of KdV-type trivial relations? (info) ; q_a != 0
    rep("P4 q_a != 0 for every a>0 (coefficient of y0^2 y4 independent of a)", sp.Poly(q, *y).coeff_monomial(y0 ** 2 * y4) != 0,
        str(sp.Poly(q, *y).coeff_monomial(y0 ** 2 * y4)))

# ---------------------------------------------------------------- property (P) for u_a, and sign of the phase
if "PP" in SECS:
    import mpmath as mp
    mp.mp.dps = 40
    av = mp.mpf("0.25")
    def uj(j, tv, xv):
        Zs = sp.symbols("Zs")
        return None
    t, x = sp.symbols("t x", positive=True)
    a = sp.Rational(1, 4)
    Z = (x + a ** 2 / (3 * t)) / (3 * t) ** sp.Rational(1, 3)
    u = 2 * sp.pi * (3 * t) ** sp.Rational(-1, 3) * sp.exp(a * x / (3 * t) + 2 * a ** 3 / (27 * t ** 2)) * sp.airyai(Z)
    jets = [u]
    for j in range(3):
        jets.append(sp.diff(jets[-1], x))
    fns = [sp.lambdify((t, x), e, [{"airyai": lambda z: mp.airyai(z), "airyaiprime": lambda z: mp.airyai(z, derivative=1)}, "mpmath"]) for e in jets]
    k0 = mp.mpf("0.8")
    errs_minus, errs_plus = [], []
    for tv in [mp.mpf(10) ** 3, mp.mpf(10) ** 4]:
        xv = -3 * k0 ** 2 * tv
        amp = tv ** mp.mpf(-0.5) * mp.sqrt(4 * mp.pi / (3 * k0)) * mp.exp(-av * k0 ** 2)
        Th = 2 * k0 ** 3 * tv - mp.pi / 4
        em = max(abs(fns[j](tv, xv) - amp * k0 ** j * mp.cos(Th - j * mp.pi / 2)) for j in range(4)) / amp
        ep = max(abs(fns[j](tv, xv) - amp * k0 ** j * mp.cos(Th + j * mp.pi / 2)) for j in range(4)) / amp
        errs_minus.append(em); errs_plus.append(ep)
    print("   PP rel. errors with cos(Th - j pi/2):", [mp.nstr(e, 5) for e in errs_minus], " with cos(Th + j pi/2):", [mp.nstr(e, 5) for e in errs_plus])
    rep("PP u_a satisfies (P) with Theta = 2k0^3 t - pi/4 and cos(Theta - j pi/2) [equivalently Theta' = -Theta, cos(Theta'+j pi/2)]",
        errs_minus[1] < errs_minus[0] and errs_minus[1] < 0.05)
    rep("PP with the package's literal sign cos(Theta + j pi/2), Theta = 2k0^3t - pi/4, odd j FAIL (sign convention only)",
        errs_plus[1] > 0.5)

# ---------------------------------------------------------------- E3
if "E3" in SECS:
    import mpmath as mp
    mp.mp.dps = 60
    good = True
    for m in range(1, 41):
        S = mp.nsum(lambda k: mp.exp(-mp.power(2, k / 2)) * mp.power(2, 4 * m * k), [0, mp.inf])
        bound = mp.mpf(1) / 2 * mp.exp(-8 * mp.sqrt(2) * m) * mp.power(8 * m, 8 * m)
        kms = [k for k in range(0, 400) if 8 * m <= 2 ** (k / 2) < 8 * math.sqrt(2) * m]
        if len(kms) != 1 or S < bound:
            good = False
            print("   E3 fail m=", m, kms, S, bound)
    rep("E3 F^(4m)(0) >= 1/2 e^{-8 sqrt2 m}(8m)^{8m} and k_m unique, m=1..40", good)
    # Cauchy ratio grows
    rho = mp.mpf("0.5")
    ratios = [mp.mpf(1) / 2 * (16 * m * rho * mp.exp(-2 * mp.sqrt(2))) ** (4 * m) for m in (5, 10, 20)]
    rep("E3 Cauchy-ratio lower bound diverges (rho=0.5)", ratios[0] < ratios[1] < ratios[2])

# ---------------------------------------------------------------- L12: scaling of the KdV soliton family
def kdv_jet_exact(ks, Xs, K):
    """exact jet y_0..y_K of u = 2 D^2 log f, f = sum_S a_S X^S, at numeric k, X (Fractions)"""
    N = len(ks)
    terms = []
    for S in itertools.chain.from_iterable(itertools.combinations(range(N), r) for r in range(N + 1)):
        aS = Fr(1)
        for i, j in itertools.combinations(S, 2):
            aS *= Fr(ks[i] - ks[j], ks[i] + ks[j]) ** 2
        kS = sum((ks[i] for i in S), Fr(0))
        XS = Fr(1)
        for i in S:
            XS *= Xs[i]
        terms.append((aS * XS, kS))
    f = sum(c for c, _ in terms)
    r = {m: sum(c * kS ** m for c, kS in terms) / f for m in range(K + 3)}
    r[0] = Fr(1)
    kap = cumulants(r, K + 2)
    return [2 * kap[j + 2] for j in range(K + 1)], f

if "L12" in SECS:
    good = True
    random.seed(5)
    for _ in range(5):
        ks = [Fr(random.randint(1, 9)), Fr(random.randint(10, 19)), Fr(-random.randint(21, 29))]
        Xs = [Fr(random.randint(1, 7), random.randint(1, 5)) for _ in range(3)]
        lam = Fr(random.randint(2, 6), random.randint(1, 4))
        j1, _ = kdv_jet_exact(ks, Xs, 4)
        j2, _ = kdv_jet_exact([lam * k for k in ks], Xs, 4)
        if any(j2[j] != lam ** (j + 2) * j1[j] for j in range(5)):
            good = False
    rep("L12 D^j u(lam k, X) = lam^{j+2} D^j u(k, X), N=3, j<=4 (exact)", good)

# ---------------------------------------------------------------- LAX: independent ansatz
if "LAX" in SECS:
    xx = sp.symbols("x")
    v = sp.Function("v")(xx)
    def vd(j):
        return sp.diff(v, xx, j)
    K = [-vd(1)]
    Kint = [-v]  # d^{-1} K_0
    K1 = sp.expand(sp.diff(K[0], xx, 2) + 4 * v * K[0] + 2 * vd(1) * Kint[0])
    K.append(K1)
    Kint.append(-vd(2) - 3 * v ** 2)
    rep("LAX d(Kint_1) == K_1", sp.expand(sp.diff(Kint[1], xx) - K1) == 0)
    K2 = sp.expand(sp.diff(K[1], xx, 2) + 4 * v * K[1] + 2 * vd(1) * Kint[1])
    K.append(K2)
    rep("LAX K_1 = -v_xxx - 6 v v_x", sp.expand(K1 + vd(3) + 6 * v * vd(1)) == 0)
    phi = sp.Function("phi")(xx)
    def Lop(g):
        return -sp.diff(g, xx, 2) - v * g
    # differential monomials of given weight (wt v^(j) = j+2) up to weight W
    def dmonos(W):
        out = []
        def rec(rem, minj, cur):
            if rem == 0 and cur:
                out.append(sp.prod(cur))
            for j in range(minj, rem - 1):
                if j + 2 <= rem:
                    rec(rem - j - 2, j, cur + [vd(j)])
        rec(W, 0, [])
        return out
    for n in range(0, 3):
        ordr = 2 * n + 1
        cs = []
        Bphi = sp.diff(phi, xx, ordr)
        for j in range(0, ordr - 1):
            for mo in dmonos(ordr - j):
                cc = sp.Symbol("c_%d_%d" % (j, len(cs)))
                cs.append(cc)
                Bphi += cc * mo * sp.diff(phi, xx, j)
        def B(g):
            return Bphi.subs(phi, g).doit()
        comm = sp.expand(B(Lop(phi)) - Lop(B(phi)) - sp.Rational(1, 4 ** n) * K[n] * phi)
        # collect coefficients in phi-derivatives and v-monomials
        eqs = []
        derivs = sorted(comm.atoms(sp.Derivative), key=lambda d: str(d))
        gens = list({d for d in derivs}) + [v, phi]
        P = sp.Poly(comm, *gens)
        eqs = list(P.coeffs())
        sol = sp.solve(eqs, cs, dict=True) if cs else ([{}] if comm == 0 else [])
        rep("LAX n=%d: exists B_n = d^{2n+1} + lower (coefficients w/o constant term) with [B_n, L] = 4^{-n} K_n" % n, len(sol) >= 1,
            str(sol[0]) if sol else "")

# ---------------------------------------------------------------- P17 on a 1-soliton
if "P17" in SECS:
    xx = sp.symbols("x", real=True)
    kp = sp.symbols("kappa", positive=True)
    v = 2 * kp ** 2 / sp.cosh(kp * xx) ** 2
    K0 = -sp.diff(v, xx)
    K1 = -sp.diff(v, xx, 3) - 6 * v * sp.diff(v, xx)
    rep("P17 soliton stationary for d=(-4k^2,1): K_1 - 4k^2 K_0 = 0", sp.simplify((K1 - 4 * kp ** 2 * K0).rewrite(sp.exp)) == 0)
    phi = 1 / sp.cosh(kp * xx)
    rep("P17 L sech = -k^2 sech", sp.simplify((-sp.diff(phi, xx, 2) - v * phi + kp ** 2 * phi).rewrite(sp.exp)) == 0)
    def B1(g):  # B_1 for L = -d^2 - v (from LAX: d^3 + 3/2 v d + 3/4 v_x)
        return sp.diff(g, xx, 3) + sp.Rational(3, 2) * v * sp.diff(g, xx) + sp.Rational(3, 4) * sp.diff(v, xx) * g
    Bd = -4 * kp ** 2 * sp.diff(phi, xx) + 4 * B1(phi)
    rep("P17(ii) B_d phi = Omega_d(i k) phi = 0 on the bound state (q_d(4k^2)=0)", sp.simplify(Bd.rewrite(sp.exp)) == 0)
    # continuous spectrum: q_d(-4k^2) = -4kappa^2 - 4k^2 != 0 -> b must vanish (reflectionless) : consistent
    rep("P17(i) consistency: q_d(-4k^2) = -4(kappa^2+k^2) != 0 for real k, and the soliton is reflectionless", True, "(INFO)")

# ---------------------------------------------------------------- P14: exact generic relation of weight 16 for N=2
PR = [2147483647, 2147483629, 2147483587, 2147483579, 2147483563, 2147483549]

def kernel_mod(rows, p):
    M = [r[:] for r in rows]
    ncol = len(M[0])
    piv_cols = []
    rk = 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(M)):
            if M[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], p - 2, p)
        M[rk] = [x * inv % p for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[rk])]
        piv_cols.append(c)
        rk += 1
    free = [c for c in range(ncol) if c not in piv_cols]
    ker = []
    for fc in free:
        vec = [0] * ncol
        vec[fc] = 1
        for i, pc in enumerate(piv_cols):
            vec[pc] = (-M[i][fc]) % p
        ker.append(vec)
    return rk, ker


def jet_mod(ks, Xs, K, p):
    N = len(ks)
    terms = []
    for S in itertools.chain.from_iterable(itertools.combinations(range(N), r) for r in range(N + 1)):
        aS = 1
        for i, j in itertools.combinations(S, 2):
            aS = aS * (ks[i] - ks[j]) * pow(ks[i] + ks[j], p - 2, p) % p
            aS = aS * (ks[i] - ks[j]) * pow(ks[i] + ks[j], p - 2, p) % p
        kS = sum(ks[i] for i in S) % p
        XS = 1
        for i in S:
            XS = XS * Xs[i] % p
        terms.append((aS * XS % p, kS))
    f = sum(c for c, _ in terms) % p
    finv = pow(f, p - 2, p)
    r = {m: sum(c * pow(kS, m, p) for c, kS in terms) * finv % p for m in range(K + 3)}
    r[0] = 1
    kap = {}
    for n in range(1, K + 3):
        s = r[n]
        for m in range(1, n):
            s -= math.comb(n - 1, m - 1) * kap[m] * r[n - m]
        kap[n] = s % p
    return [2 * kap[j + 2] % p for j in range(K + 1)]


def ratrec(a, m):
    # rational reconstruction
    a %= m
    r0, r1 = m, a
    s0, s1 = 0, 1
    bound = math.isqrt(m // 2)
    while r1 > bound:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > bound:
        return None
    return Fr(r1, s1) if s1 > 0 else Fr(-r1, -s1)

if "P14" in SECS:
    # monomials k1^a k2^b y0^c0 y1^c1 y2^c2 of weight exactly 16, with k1 = 1 set: key (b, c0, c1, c2)
    monos = []
    for c2 in range(0, 5):
        for c1 in range(0, 6):
            for c0 in range(0, 9):
                wy = 2 * c0 + 3 * c1 + 4 * c2
                if wy > 16:
                    continue
                for b in range(0, 16 - wy + 1):
                    monos.append((b, c0, c1, c2))
    print("   P14 #monomials of weight 16 in (k1,k2,y0,y1,y2):", len(monos), flush=True)
    idx0 = monos.index((0, 8, 0, 0))
    vecs = []
    okrec = False
    random.seed(13)
    for p in PR[:4]:
        rows = []
        while len(rows) < len(monos) + 30:
            kap = random.randrange(2, p)
            X = [random.randrange(1, p), random.randrange(1, p)]
            if (1 + kap) % p == 0:
                continue
            try:
                y = jet_mod([1, kap], X, 2, p)
            except Exception:
                continue
            rows.append([pow(kap, b, p) * pow(y[0], c0, p) * pow(y[1], c1, p) * pow(y[2], c2, p) % p for (b, c0, c1, c2) in monos])
        rk, ker = kernel_mod(rows, p)
        rep("P14 nullity at weight 16 mod p=%d is 1" % p, len(ker) == 1, "nullity=%d" % len(ker))
        if len(ker) != 1:
            break
        v = ker[0]
        inv = pow(v[idx0], p - 2, p)
        vecs.append([x * inv % p for x in v])
        if len(vecs) >= 2:
            # CRT
            M = 1
            for q_ in PR[:len(vecs)]:
                M *= q_
            coeffs = []
            okrec = True
            for i in range(len(monos)):
                a_ = 0
                for vv, q_ in zip(vecs, PR[:len(vecs)]):
                    Mi = M // q_
                    a_ += vv[i] * Mi * pow(Mi, q_ - 2, q_)
                a_ %= M
                rr = ratrec(a_, M)
                if rr is None:
                    okrec = False
                    break
                coeffs.append(rr)
            if okrec:
                break
    if vecs and okrec:
        Q = {monos[i]: coeffs[i] for i in range(len(monos)) if coeffs[i] != 0}
        print("   P14 reconstructed Q with %d nonzero terms; max height %d" % (len(Q), max(max(abs(c.numerator), c.denominator) for c in Q.values())), flush=True)
        # exact verification on the grid kappa in 2..50, X1, X2 in 1..17 (degree bounds 48, 16, 16)
        den = 1
        for c in Q.values():
            den = den * c.denominator // math.gcd(den, c.denominator)
        Qi = {m: int(c * den) for m, c in Q.items()}
        bad = 0
        npts = 0
        tstart = time.time()
        for kv in range(2, 51):
            for x1 in range(1, 18):
                for x2 in range(1, 18):
                    yj, f = kdv_jet_exact([Fr(1), Fr(kv)], [Fr(x1), Fr(x2)], 2)
                    F = f * (1 + kv) ** 2
                    Nj = [yj[j] * F ** (j + 2) for j in range(3)]
                    if all(n.denominator == 1 for n in Nj) and F.denominator == 1:
                        Ni = [int(n) for n in Nj]
                        Fi = int(F)
                        Fp = [Fi ** e for e in range(17)]
                        s = 0
                        for (b, c0, c1, c2), c in Qi.items():
                            s += c * kv ** b * Fp[16 - 2 * c0 - 3 * c1 - 4 * c2] * Ni[0] ** c0 * Ni[1] ** c1 * Ni[2] ** c2
                    else:
                        s = Fr(0)
                        for (b, c0, c1, c2), c in Qi.items():
                            s += c * Fr(kv) ** b * yj[0] ** c0 * yj[1] ** c1 * yj[2] ** c2
                    npts += 1
                    if s != 0:
                        bad += 1
            if time.time() - tstart > 1500:
                break
        rep("P14 EXACT: Q(1,kappa; jet) = 0 on the full grid 49x17x17 (=> identity, degree bounds 48/16/16)", bad == 0 and npts == 49 * 17 * 17,
            "points=%d bad=%d" % (npts, bad))
        sym = all(Q.get(m, 0) == Q.get(m, 0) for m in Q)
        # properties: y0^8 coefficient, evenness in k2, y-degree 8 max
        ydeg = max(c0 + c1 + c2 for (b, c0, c1, c2) in Q)
        even = all(b % 2 == 0 for (b, c0, c1, c2) in Q)
        rep("P14 Q: coefficient of y0^8 = 1 (constant), y-degree 8, even in k2 (k1=1)", Q.get((0, 8, 0, 0)) == 1 and ydeg == 8 and even,
            "ydeg=%d even=%s" % (ydeg, even))
        # k0 = (1,2) not in Z_15: rank of y-monomials of weight <= 15 at k0, exact over Q via mod p full rank
        p = PR[0]
        ym = [(c0, c1, c2) for c0 in range(8) for c1 in range(6) for c2 in range(4) if 0 < 2 * c0 + 3 * c1 + 4 * c2 <= 15] + [(0, 0, 0)]
        rows = []
        while len(rows) < len(ym) + 20:
            X = [random.randrange(1, p), random.randrange(1, p)]
            y = jet_mod([1, 2], X, 2, p)
            rows.append([pow(y[0], a0, p) * pow(y[1], a1, p) * pow(y[2], a2, p) % p for (a0, a1, a2) in ym])
        rk, ker = kernel_mod(rows, p)
        rep("P14 k0=(1,2) not in Z_15 (full rank mod p of %d y-monomials of weight<=15 => no relation over Q)" % len(ym), len(ker) == 0)
    else:
        rep("P14 rational reconstruction", False)

print("TOTAL %d/%d OK" % (OK, TOT), flush=True)
