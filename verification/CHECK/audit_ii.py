"""S-CHECK-2B — red team per II-T2, II-T3 (+II-C2), II-T4, II-P5, II-T7 (fonte: work/II/CHECK_REQUEST.md)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
from sympy import symbols, Matrix, zeros, eye, expand, exp, cos, sin, simplify, resultant, Poly, I, sqrt, factor

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

tau, xi, t, x, s = symbols('tau xi t x s')

def companion(P):
    p = Poly(expand(P), tau)
    k = p.degree()
    c = p.all_coeffs()[::-1]
    C = zeros(k)
    for i in range(k - 1):
        C[i, i + 1] = 1
    for j in range(k):
        C[k - 1, j] = -c[j]
    return C

def mat_eval(f, M):
    f = Poly(expand(f), tau)
    k = M.shape[0]
    out = zeros(k)
    Mi = eye(k)
    for cf in f.all_coeffs()[::-1]:
        out += cf * Mi
        Mi = Mi * M
    return out

def bezout_V(Q, B):
    """U Q + V B = r = Res_tau(Q,B), con V di grado < deg Q in tau (coeff. in C[xi])."""
    r = resultant(Q, B, tau)
    d = Poly(Q, tau).degree()
    vs = symbols('v0:%d' % d)
    V = sum(vs[i] * tau**i for i in range(d))
    rem = sp.rem(expand(V * B - r), Q, tau)
    sol = sp.solve(Poly(rem, tau).all_coeffs(), vs, dict=True)[0]
    V = expand(V.subs(sol))
    U = sp.cancel((r - V * B) / Q)
    return r, U, V

def projector(Qs, j):
    P = expand(sp.prod(Qs))
    B = expand(sp.prod([q for i, q in enumerate(Qs) if i != j]))
    r, U, V = bezout_V(Qs[j], B)
    C = companion(P)
    N = mat_eval(expand(V * B), C).applyfunc(expand)
    return C, N, r, U, V, B

def pole_order(M, pt):
    m = 0
    for e in M:
        e = sp.cancel(e)
        den = sp.denom(e)
        m = max(m, sp.roots(Poly(den, xi)).get(pt, 0) if Poly(den, xi).degree() > 0 else 0)
    return m

print('=== II-T2 ===')
# Esempio del rilievo: Q = (τ-1)(τ-ξ)(τ+ξ), ξ0 = 0
Qs = [tau - 1, tau - xi, tau + xi]
C, N1, r1, U1, V1, B1 = projector(Qs, 0)
check('(a) U_1Q_1 + V_1B_1 = r_1 con U_1,V_1 ∈ C[ξ][τ]', simplify(U1 * Qs[0] + V1 * B1 - r1) == 0 and sp.cancel(U1).is_polynomial(tau, xi) and V1.is_polynomial(tau, xi))
check('    N_1 ∈ Mat_3(C[ξ])', all(sp.cancel(e).is_polynomial(xi) for e in N1))
Pi = [projector(Qs, j)[1] / projector(Qs, j)[2] for j in range(3)]
check('(b) generico: Π_j idempotenti ortogonali, somma I, commutano con C',
      all(simplify(Pi[a] * Pi[b] - (Pi[a] if a == b else zeros(3))) == zeros(3) for a in range(3) for b in range(3))
      and simplify(Pi[0] + Pi[1] + Pi[2] - eye(3)) == zeros(3)
      and all(simplify(p * C - C * p) == zeros(3) for p in Pi))
check('    N_i N_j = 0 identicamente (i≠j): ortogonalità vale in ogni ξ0 dove entrambi sono definiti',
      all(simplify(projector(Qs, a)[1] * projector(Qs, b)[1]) == zeros(3) for a in range(3) for b in range(3) if a != b))
C0 = C.subs(xi, 0); P10 = Pi[0].subs(xi, 0)
kerB = mat_eval(B1, C).subs(xi, 0).nullspace()
sumker = Matrix.hstack(*(mat_eval(Qs[1], C).subs(xi, 0).nullspace() + mat_eval(Qs[2], C).subs(xi, 0).nullspace()))
check('F1: ξ0=0, r_1(0) = %s ≠ 0, ma dim(ker Q_2(C0)+ker Q_3(C0)) = %d < dim ker B_1(C0) = %d = dim ker Π_1(0)'
      % (r1.subs(xi, 0), sumker.rank(), len(kerB)), r1.subs(xi, 0) != 0 and sumker.rank() == 1 and len(kerB) == 2 and len(P10.nullspace()) == 2)
check('    ker Π_1(0) = ker B_1(0,C0) (stesso sottospazio)', Matrix.hstack(*(P10.nullspace() + kerB)).rank() == 2)
check('    Σ_jΠ_j(0) non definito: r_2(0) = r_3(0) = 0', projector(Qs, 1)[2].subs(xi, 0) == 0 and projector(Qs, 2)[2].subs(xi, 0) == 0)
# (b′) poli: Π_j olomorfo in ξ0 ⟺ r_j(ξ0) ≠ 0 ; ordine del polo vs ordine di r_j
tests = [
    [tau, tau - xi**2],
    [tau - xi, tau + xi],
    [(tau - xi)**2, tau],
    [tau**2 - xi, tau - 1],
    [tau**2 - xi**3, tau],
    [tau - 1, tau - xi, tau + xi],
    [tau**2 + xi**2 - 1, tau - xi],
]
allpoles = True; report = []
for Q in tests:
    for j in range(len(Q)):
        Cq, Nq, rq, *_ = projector(Q, j)
        Piq = (Nq / rq).applyfunc(sp.cancel)
        zr = sp.roots(Poly(rq, xi)) if Poly(rq, xi).degree() > 0 else {}
        poles = set()
        for e in Piq:
            den = sp.denom(sp.cancel(e))
            if Poly(den, xi).degree() > 0:
                poles |= set(sp.roots(Poly(den, xi)).keys())
        allpoles = allpoles and poles == set(zr.keys())
        report.append((str(Q[j]), dict(zr), {p: pole_order(Piq, p) for p in zr}))
check("(b′) 7 famiglie, ogni j: insieme dei poli di Π_j = zeri di r_j", allpoles)
lt = all(all(po[p] <= zr[p] for p in zr) for _, zr, po in report)
check('    ordine del polo ≤ molteplicità dello zero di r_j (il claim non afferma uguaglianza)', lt)
for q, zr, po in report:
    print('        Q_j =', q, ' zeri di r_j (molt.):', zr, ' ordine polo:', po)
# (c) azione sui modi
Qc = [tau - 1, tau - xi, tau + xi]
Cc, Nc, rc, *_ = projector(Qc, 0)
v = lambda tt: Matrix([1, tt, tt**2])
xi0 = sp.Rational(1, 3)
Pi0 = (Nc / rc).subs(xi, xi0)
check('(c) ξ0 = 1/3: Π_1 v(1) = v(1), Π_1 v(±1/3) = 0',
      simplify(Pi0 * v(1) - v(1)) == zeros(3, 1) and simplify(Pi0 * v(xi0)) == zeros(3, 1) and simplify(Pi0 * v(-xi0)) == zeros(3, 1))
check('    ξ0 = 0 (collisione Q_2=Q_3, r_1(0)≠0): Π_1 v(1)=v(1), Π_1 v(0)=0', simplify(P10 * v(1) - v(1)) == zeros(3, 1) and simplify(P10 * v(0)) == zeros(3, 1))
# (d) azione sulle soluzioni e sul jet
u1 = exp(t) * sin(x); u2 = (t + x)**3; u3 = cos(x - t)
u = u1 + u2 + u3
def op(Pp, w):
    p = Poly(expand(Pp), tau, xi)
    return expand(sum(c * sp.diff(w, t, a, x, b) for (a, b), c in zip(p.monoms(), p.coeffs())))
check('    u_i ∈ ker Q_i', all(simplify(op(q, w)) == 0 for q, w in zip(Qc, [u1, u2, u3])))
lhs = op(expand(projector(Qc, 0)[4] * projector(Qc, 0)[5]), u)
check('(d) (V_1B_1)(∂)u = r_1(∂_x)u_1', simplify(lhs - op(rc, u1)) == 0)
J = lambda w: Matrix([w, sp.diff(w, t), sp.diff(w, t, 2)])
def matop(M, vec):
    return Matrix([sum(op(M[i, jj], vec[jj]) for jj in range(3)) for i in range(3)])
check('    N_1(∂_x)J(u) = r_1(∂_x)J(u_1)', simplify(matop(Nc, J(u)) - J(op(rc, u1))) == zeros(3, 1))
check('    r_1(∂_x) ha nucleo: (∂_x²-1)e^{t+x} = 0 con e^{t+x} ∈ ker Q_1∩ker Q_2: u_1 recuperato solo mod ker r_1(∂_x)',
      simplify(op(rc, exp(t + x))) == 0 and simplify(op(Qc[0], exp(t + x))) == 0 and simplify(op(Qc[1], exp(t + x))) == 0)

print('=== II-T3 / II-C2 ===')
pairs_disjoint = [(tau, tau - 1), (tau - xi**2, tau - xi**2 - 1), (tau * xi - 1, xi)]
for P1, P2 in pairs_disjoint:
    G = sp.groebner([P1, P2], tau, xi)
    # coefficienti di Bezout a P1 + b P2 = 1 via reduce sulla base
    a, b = symbols('a b')
    check(f'(i)⟺(ii) {P1}, {P2}: base di Gröbner = [1]', G.exprs == [1])
# E1 esplicito e verifica su soluzioni
P1, P2 = tau * xi - 1, xi
E1 = tau * xi            # (-1)P1 + τ P2 = 1  ⇒ E1 = τ P2
check('    identità -P1 + τP2 = 1', expand(-P1 + tau * P2) == 1)
w1 = exp(2 * t + x / 2) + exp(-t - x)      # ker(∂_t∂_x - 1)
w2 = t**3 + sin(t)                          # ker ∂_x
check('(iv) E1 = τξ: E1 w1 = w1 (w1∈ker P1), E1 w2 = 0 (w2∈ker P2)',
      simplify(op(P1, w1)) == 0 and simplify(op(E1, w1) - w1) == 0 and simplify(op(E1, w2)) == 0)
check('    esistenza: u = aP1 u + bP2 u con bP2 u ∈ ker P1, aP1 u ∈ ker P2 (u = w1+w2)',
      simplify(op(P1, op(E1, w1 + w2))) == 0 and simplify(op(P2, op(-P1, w1 + w2))) == 0)
# (iv)/(v) ⇒ (i): punto comune ⇒ esponenziale nell'intersezione dei nuclei
P1, P2 = tau, tau - xi**2
w = exp(0 * t + 0 * x)
check('(v)⇒(i): V(τ)∩V(τ-ξ²) = {(0,0)} ⇒ 1 ∈ ker P1 ∩ ker P2', op(P1, w) == 0 and op(P2, w) == 0)
# II-C2: forme di grado massimo
def sigma(P):
    p = Poly(P, tau, xi); d = p.total_degree()
    return sum(c * tau**m[0] * xi**m[1] for m, c in zip(p.monoms(), p.coeffs()) if sum(m) == d)
cz = True
for P1, P2 in pairs_disjoint:
    s1, s2 = sigma(P1), sigma(P2)
    r = resultant(s1.subs(xi, 1), s2.subs(xi, 1), tau) if True else None
    common = sp.gcd(s1, s2)
    cz = cz and Poly(common, tau, xi).total_degree() >= 1
check('II-C2: nelle 3 coppie disgiunte σ(P1), σ(P2) hanno un fattore lineare comune', cz)
P1, P2 = tau - xi**2, tau - xi**2 - xi
check('II-C2 viceversa falso: σ = -ξ² per entrambi (zero comune [1:0]) ma V∩V = {(0,0)} ≠ ∅',
      sigma(P1) == sigma(P2) and sp.groebner([P1, P2], tau, xi).exprs != [1])
check('II-C2 nota: "forma iniziale" = parte di grado MASSIMO; con la parte di grado minimo (τ e -1 per P1=τ, P2=τ-1) l\'enunciato fallisce',
      Poly(sp.gcd(tau, -1), tau).degree() == 0)

print('=== II-T4 ===')
def spectral_proj(C, P, Sroots):
    """Proiettore spettrale g(C) per il sottoinsieme Sroots di radici (in K̄) con interpolazione di Hermite."""
    rts = sp.roots(Poly(P, tau))
    k = Poly(P, tau).degree()
    gs = symbols('g0:%d' % k)
    g = sum(gs[i] * tau**i for i in range(k))
    eqs = []
    for rt, mu in rts.items():
        val = 1 if any(simplify(rt - s0) == 0 for s0 in Sroots) else 0
        for d in range(mu):
            eqs.append(sp.diff(g, tau, d).subs(tau, rt) - (val if d == 0 else 0))
    sol = sp.solve(eqs, gs, dict=True)[0]
    g = expand(g.subs(sol))
    return mat_eval(g, C).applyfunc(sp.simplify), g
# irriducibile: S = {√ξ}
P = tau**2 - xi
C = companion(P)
PiS, g = spectral_proj(C, P, [sqrt(xi)])
check('τ²-ξ, S={√ξ}: Π_S idempotente ma non razionale in ξ (contiene √ξ)', simplify(PiS * PiS - PiS) == zeros(2) and PiS.has(sqrt(xi)))
# non ridotto, S = {ξ} con molteplicità 2: Q_S = (τ-ξ)² ∈ K[τ]
P = expand((tau - xi)**2 * (tau + xi))
C = companion(P)
PiS, g = spectral_proj(C, P, [xi])
check('(τ-ξ)²(τ+ξ), S={ξ}: Π_S ∈ Mat_3(C(ξ))', all(sp.cancel(e).is_rational_function(xi) and not e.has(sqrt(xi)) for e in PiS))
gnum = sp.numer(sp.together(g - 1))
gg = sp.gcd(P, gnum)
check('    gcd(P, g-1) = (τ-ξ)² = Q_S (molteplicità piena, risposta alla domanda)', simplify(gg / (tau - xi)**2).free_symbols.isdisjoint({tau}))
ordg = 0
for d in range(4):
    if simplify(sp.diff(g - 1, tau, d).subs(tau, xi)) == 0:
        ordg = d + 1
    else:
        break
check(f'    ord_{{τ=ξ}}(g-1) = {ordg} ≥ μ = 2; ord_{{τ=-ξ}}(g-1) = 0', ordg >= 2 and simplify((g - 1).subs(tau, -xi)) != 0)
# (τ²-ξ)²: S = {√ξ} con μ=2 non razionale; S = {±√ξ} razionale
P = expand((tau**2 - xi)**2)
C = companion(P)
PiS, g = spectral_proj(C, P, [sqrt(xi)])
check('(τ²-ξ)², S={√ξ}: Π_S non razionale', PiS.has(sqrt(xi)))
# coerenza con II-T2: (τ-ξ)²(τ+ξ) con Q=(τ-ξ)², B=τ+ξ
Cq, Nq, rq, *_ = projector([(tau - xi)**2, tau + xi], 0)
P = expand((tau - xi)**2 * (tau + xi)); PiS, g = spectral_proj(companion(P), P, [xi])
check('    Π_S (Hermite) = N/r di II-T2', simplify(PiS - Nq / rq) == zeros(3))

print('=== II-P5 ===')
import random
random.seed(1)
def is_normal(M):
    D = (M * M.H - M.H * M).evalf()
    return max(abs(complex(e)) for e in D) < 1e-9
fam_ok = True
for _ in range(6):
    th = random.uniform(0, 6.28); rr = random.uniform(-3, 3)
    p0 = sp.exp(I * th); p1 = I * rr * sp.exp(I * th / 2)
    M = Matrix([[0, 1], [-p0, -p1]])
    fam_ok = fam_ok and is_normal(M) and abs(complex((sp.conjugate(p0) * p1 + sp.conjugate(p1)).evalf())) < 1e-12
check('k=2: famiglia p0 = e^{iθ}, p1 = i r e^{iθ/2} (r reale): sempre normale (6 campioni)', fam_ok)
# k=2 con radici: λ2 = -1/conj(λ1)
lam1 = 2 + I
lam2 = -1 / sp.conjugate(lam1)
p = expand((s - lam1) * (s - lam2))
pc = Poly(p, s).all_coeffs()
M = Matrix([[0, 1], [-pc[2], -pc[1]]])
check('k=2: λ1 = 2+i, λ2 = -1/λ̄1 (|λ1| ≠ 1): compagna normale', is_normal(M))
# k=3: tentativo di normale non della forma s^3-c
bad = False
for _ in range(20):
    rts = [complex(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(3)]
    pp = Poly(expand(sp.prod([s - sp.nsimplify(r_, rational=True) for r_ in rts])), s).all_coeffs()
    M = zeros(3)
    M[0, 1] = 1; M[1, 2] = 1
    for j in range(3):
        M[2, j] = -pp[3 - j]
    if is_normal(M):
        bad = True
check('k=3: 20 cubiche casuali, nessuna compagna normale (coerente con (3))', not bad)
w = sp.exp(2 * sp.pi * I / 3)
M = zeros(3); M[0, 1] = 1; M[1, 2] = 1; M[2, 0] = w   # s^3 - w, |w| = 1
check('k=3: s³ - e^{2πi/3}: normale', is_normal(M))
# Lagrange
lams = [1, 2, -1]
V = Matrix([[l**i for l in lams] for i in range(3)])
Vi = V.inv()
lag = all(simplify((Vi[a, :] * Matrix([1, s, s**2]))[0] - sp.interpolate([(lams[b], 1 if b == a else 0) for b in range(3)], s)) == 0 for a in range(3))
check('Lagrange: w_aᵀ v(s) = ℓ_a(s) (radici 1, 2, -1)', lag)
pl = expand(sp.prod([s - l for l in lams])); pcl = Poly(pl, s).all_coeffs()
Cl = zeros(3); Cl[0, 1] = 1; Cl[1, 2] = 1
for j in range(3):
    Cl[2, j] = -pcl[3 - j]
check('    Π_a = v(λ_a)w_aᵀ è il proiettore spettrale (idempotente, C Π_a = λ_a Π_a)',
      all(simplify((V[:, a] * Vi[a, :])**2 - V[:, a] * Vi[a, :]) == zeros(3) and simplify(Cl * V[:, a] * Vi[a, :] - lams[a] * V[:, a] * Vi[a, :]) == zeros(3) for a in range(3)))

print('=== II-T7 ===')
def phi1(l1, l2):
    return (l2 * exp(l1 * t) - l1 * exp(l2 * t)) / (l2 - l1)
# ERRORE (e) per coefficienti complessi
l1, l2 = 1 + I, 2 + I
f = phi1(l1, l2)
ratio = sp.simplify(l1 / l2)
check(f'(e) radici NON reali 1+i, 2+i (p complesso): φ_1 = 0 ⟺ e^{{-t}} = {ratio}, non reale ⇒ nessuno zero in t ≥ 0',
      sp.im(ratio) != 0 and simplify(f.subs(t, 0) - 1) == 0 and simplify(sp.diff(f, t).subs(t, 0)) == 0)
import math
fn = sp.lambdify(t, f, 'mpmath')
mn = min(abs(complex(fn(0.01 * i))) for i in range(0, 3001))
check(f'    controllo numerico: min_{{t∈[0,30]}} |φ_1| = {mn:.3e} > 0 (fattorizzazione LDU globale su [0,∞) con radici non reali)', mn > 1e-6)
pp = expand((s - l1) * (s - l2)); pc = Poly(pp, s).all_coeffs()
Cc = Matrix([[0, 1], [-pc[2], -pc[1]]])
Phi = (Cc * t).exp()
check('    Φ_11 = φ_1 per questa C complessa', simplify(Phi[0, 0] - f) == 0)
# radice doppia complessa
r0 = 1 + I
f2 = exp(r0 * t) * (1 - r0 * t)
check('(e) radice doppia 1+i: φ_1 = e^{rt}(1-rt) senza zeri reali (t = 1/r non reale)', sp.im(1 / r0) != 0)
# reali: verifica dei casi
cases = {(1, 2): True, (-2, -1): False, (-1, 2): False, (0, 3): False, (-3, 0): False}
cr = True
for (a_, b_), haszero in cases.items():
    g_ = phi1(a_, b_)
    zs = sp.solveset(sp.Eq(g_, 0), t, sp.Interval.open(0, sp.oo))
    cr = cr and ((zs != sp.EmptySet) == haszero)
check('(e) radici reali: zero in t>0 solo per 0<r1<r2 (5 casi, inclusi r=0)', cr)
# (d): coordinate di seconda specie in ordine arbitrario per k=3 (unipotenti inferiori)
a, b, c = symbols('a b c')
E = lambda i, j: Matrix(3, 3, lambda p, q: 1 if (p, q) == (i, j) else 0)
orders = [[(1, 0), (2, 0), (2, 1)], [(2, 1), (1, 0), (2, 0)], [(2, 0), (2, 1), (1, 0)], [(1, 0), (2, 1), (2, 0)]]
L = Matrix([[1, 0, 0], [symbols('l10'), 1, 0], [symbols('l20'), symbols('l21'), 1]])
good = True
for od in orders:
    prod_ = eye(3)
    for (i, j), g_ in zip(od, (a, b, c)):
        prod_ = prod_ * (eye(3) + g_ * E(i, j))
    sol = sp.solve([prod_[1, 0] - L[1, 0], prod_[2, 0] - L[2, 0], prod_[2, 1] - L[2, 1]], [a, b, c], dict=True)
    good = good and len(sol) == 1 and all(sp.Poly(v_, *L.free_symbols).is_polynomial if False else sp.simplify(v_).is_polynomial(*L.free_symbols) for v_ in sol[0].values())
check('(d) k=3: per 4 ordini, L ↦ (g_ij) è biiezione polinomiale (Borel, LAG 14.4)', good)
# onda di Fourier: p = s² + κ²  (κ=1): Δ1 = cos t, zero in π/2
check('(e) onda κ=1: Δ1 = φ_1 = cos t, primo zero π/2 (globale solo su [0,π/2))', simplify(phi1(I, -I) - cos(t)) == 0)

print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
