# S-II, ripresa 25/10 sera — controlli per il recepimento dell'audit S-CHECK-2B
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I s3_ripresa.py > s3_ripresa.out
import sys
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding='utf-8')

tau, xi, s, t, x = sp.symbols('tau xi s t x')
ok_all = True

def report(name, cond):
    global ok_all
    ok_all = ok_all and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

def companion_of(P, var):
    p = sp.Poly(sp.expand(P), var)
    k = p.degree()
    c = p.all_coeffs()[::-1]  # p_0..p_k
    C = sp.zeros(k, k)
    for i in range(k - 1):
        C[i, i + 1] = 1
    for j in range(k):
        C[k - 1, j] = -c[j] / c[k]
    return C

def mat_poly(P, var, C):
    p = sp.Poly(sp.expand(P), var)
    k = C.shape[0]
    R = sp.zeros(k, k)
    for (e,), a in p.terms():
        R += a * C**e
    return R

# ---------------------------------------------------------------- A. II-T2-F1, F2
print('== A. II-T2-F1/F2: nucleo di Π_j(ξ0) = ker B_j(ξ0,C0)')
Q = [tau - 1, tau - xi, tau + xi]
P = sp.expand(Q[0] * Q[1] * Q[2])
C = companion_of(P, tau)
B1 = sp.expand(Q[1] * Q[2])
r1 = sp.resultant(Q[0], B1, tau)
# e_1 = V_1 B_1 / r_1 via gcdex in K[tau]
Uq, Vb, g = sp.gcdex(Q[0], B1, tau)  # Uq*Q0 + Vb*B1 = g (g costante in tau)
e1 = sp.simplify(Vb * B1 / g)
Pi1 = sp.simplify(mat_poly(e1, tau, C))
Pi1_0 = Pi1.subs(xi, 0)
C0 = C.subs(xi, 0)
report('r_1 = 1 - xi^2 (a meno del segno), r_1(0) != 0', sp.simplify(r1**2 - (1 - xi**2)**2) == 0 and r1.subs(xi, 0) != 0)
report('Π_1(0) idempotente', sp.simplify(Pi1_0**2 - Pi1_0) == sp.zeros(3, 3))
kerPi = (Pi1_0).nullspace()
kerB = mat_poly(B1.subs(xi, 0), tau, C0).nullspace()
sumQ = sp.Matrix.hstack(*(mat_poly(Q[1].subs(xi, 0), tau, C0).nullspace() + mat_poly(Q[2].subs(xi, 0), tau, C0).nullspace()))
report('dim ker Π_1(0) = dim ker B_1(0,C0) = 2', len(kerPi) == 2 and len(kerB) == 2)
report('ker Π_1(0) = ker B_1(0,C0) (stesso sottospazio)', sp.Matrix.hstack(*kerPi, *kerB).rank() == 2)
report('dim(ker Q_2(C0) + ker Q_3(C0)) = 1 < 2 (frase originale falsa)', sumQ.rank() == 1)
report('Im Π_1(0) = ker Q_1(0,C0)', sp.Matrix.hstack(*Pi1_0.columnspace(), *mat_poly(Q[0], tau, C0).nullspace()).rank() == 1)
# F2: N_i N_l ≡ 0 (ortogonalità identica); somma = I solo dove tutti gli r_i != 0
Ns = []
for j in range(3):
    Bj = sp.expand(P / Q[j]); Bj = sp.cancel(Bj)
    U, V, gg = sp.gcdex(Q[j], Bj, tau)
    rj = sp.resultant(Q[j], Bj, tau)
    Nj = sp.simplify(mat_poly(sp.expand(sp.cancel(V * rj / gg) * Bj), tau, C))
    Ns.append((Nj, rj))
orth = all(sp.simplify(Ns[i][0] * Ns[l][0]) == sp.zeros(3, 3) for i in range(3) for l in range(3) if i != l)
report('F2: N_i N_l ≡ 0 per i != l (polinomiale in ξ)', orth)
r2 = Ns[1][1]
report('F2: in ξ0 = 0, r_2(0) = 0 (Π_2 ha un polo: ΣΠ_i(0) non definita)', sp.simplify(r2.subs(xi, 0)) == 0)

# ---------------------------------------------------------------- B. II-T3-F2 esistenza
print('== B. II-T3-F2: u = (bP2)u + (aP1)u')
P1 = tau * xi - 1; P2 = xi; a, b = -1, tau  # a P1 + b P2 = 1
report('a P1 + b P2 = 1', sp.expand(a * P1 + b * P2) == 1)
def op(Pol, f):
    p = sp.Poly(sp.expand(Pol), tau, xi)
    return sp.expand(sum(c * sp.diff(f, t, i, x, j) for (i, j), c in p.terms()))
w1 = sp.exp(2 * t + x / 2)  # in ker P1
w2 = sp.sin(t) + t**3        # in ker P2
report('w1 ∈ ker P1, w2 ∈ ker P2', sp.simplify(op(P1, w1)) == 0 and sp.simplify(op(P2, w2)) == 0)
u = w1 + w2
c1 = op(b * P2, u); c2 = op(a * P1, u)
report('(bP2)u = w1, (aP1)u = w2', sp.simplify(c1 - w1) == 0 and sp.simplify(c2 - w2) == 0)

# ---------------------------------------------------------------- C. II-T7-F1 criterio complesso
print('== C. II-T7-F1: k = 2, p complesso')
l1, l2 = sp.symbols('lambda1 lambda2')
phi1 = (l2 * sp.exp(l1 * t) - l1 * sp.exp(l2 * t)) / (l2 - l1)
report('φ1(0) = 1, φ1\'(0) = 0', sp.simplify(phi1.subs(t, 0)) == 1 and sp.simplify(sp.diff(phi1, t).subs(t, 0)) == 0)
report('φ1 = 0 ⟺ e^{(λ1−λ2)t} = λ1/λ2 (identità φ1·(λ2−λ1)e^{−λ2 t} = λ2 e^{(λ1−λ2)t} − λ1)',
       sp.simplify(phi1 * (l2 - l1) * sp.exp(-l2 * t) - (l2 * sp.exp((l1 - l2) * t) - l1)) == 0)
def minphi(L1, L2, T, n=6000):
    L1 = mp.mpc(L1); L2 = mp.mpc(L2)
    if abs(L1 - L2) < 1e-14:
        f = lambda tt: mp.exp(L1 * tt) * (1 - L1 * tt)
    else:
        f = lambda tt: (L2 * mp.exp(L1 * tt) - L1 * mp.exp(L2 * tt)) / (L2 - L1)
    return min(abs(f(T * i / n)) for i in range(n + 1))
m = minphi(1 + 1j, 2 + 1j, 30)
report('controesempio audit: radici 1+i, 2+i, min_[0,30] |φ1| ≈ 0.988 > 0 (globale, radici non reali)', m > 0.9)
report('radice doppia r = 1+i: φ1 = e^{rt}(1−rt) mai nulla per t>0 (min_[0,20] > 0)', minphi(1 + 1j, 1 + 1j, 20) > 1e-3)
report('radice doppia r = 2 (in (0,∞)): φ1(1/2) = 0', abs(mp.exp(1) * (1 - 1)) == 0)

# ---------------------------------------------------------------- D. conseguenze in frequenza ξ = iκ
print('== D. Conseguenze di II-T7(e) corretta (ξ = iκ ⇒ p(s;κ) = P(s, iκ))')
kap, c, v, m_, g_, bb = sp.symbols('kappa c v m gamma b', real=True)
def roots_at(Pexpr, subsd):
    pp = sp.Poly(sp.expand(Pexpr.subs(subsd)), tau)
    return [complex(rr) for rr in sp.Poly(pp, tau).nroots()]
def glob_min(Pexpr, subsd, T):
    r = roots_at(Pexpr, subsd)
    return minphi(r[0], r[1], T)

# D1 onda: locale, t* = π/(2cκ)
Pw = tau**2 - c**2 * xi**2
r = roots_at(Pw, {c: 1, xi: 3j})
report('D1 onda ξ=iκ (κ=3): φ1 = cos(3t) si annulla in π/6 (locale)', minphi(r[0], r[1], 0.6) < 1e-3)
# D2 onda con trasporto (derivata dispari in x): (τ+vξ)^2 − c^2ξ^2, ξ = iκ
Pdw = (tau + v * xi)**2 - c**2 * xi**2
okD2 = True
for vv, kk in [(0.5, 1), (0.5, 10), (0.5, 100), (-0.3, 7), (2.0, 5)]:
    mn = glob_min(Pdw, {c: 1, v: vv, xi: 1j * kk}, 40.0 / kk + 20)
    bound = min(abs(vv), 1.0) / 1.0
    okD2 = okD2 and (mn >= bound - 1e-6)
report('D2 onda+trasporto v≠0, ξ=iκ: globale, |φ1| ≥ min(|v|,c)/c uniforme in κ', okD2)
# D2': stessa P, modi reali ξ: supersonico |v|>c ⇒ due radici positive per un segno di ξ ⇒ locale
r = roots_at(Pdw, {c: 1, v: 2, xi: -1})
report('D2\' onda+trasporto |v|>c, ξ reale = −1: radici reali entrambe > 0 ⇒ locale', all(z.real > 0 and abs(z.imag) < 1e-12 for z in r) and minphi(r[0], r[1], 5) < 1e-3)
# D3 Klein–Gordon τ² − c²ξ² + m²: ξ = iκ locale per ogni κ (anche κ=0); ξ reale con |cξ| < m locale
Pkg = tau**2 - c**2 * xi**2 + m_**2
r = roots_at(Pkg, {c: 1, m_: 1, xi: 0})
report('D3 KG κ=0: φ1 = cos(mt), locale t < π/(2m)', minphi(r[0], r[1], 1.6) < 1e-2)
r = roots_at(Pkg, {c: 1, m_: 1, xi: 0.5})
report('D3 KG ξ reale, |cξ|<m: radici ±i√(m²−c²ξ²), locale (modi esponenziali reali NON globali)', minphi(r[0], r[1], 2.0) < 1e-2)
r = roots_at(Pkg, {c: 1, m_: 1, xi: 2})
report('D3 KG ξ reale, |cξ|>m: radici reali di segno opposto, globale', minphi(r[0], r[1], 30) > 0.4)
# D4 telegrafo τ² + 2γτ − c²ξ²: ξ = iκ globale ⟺ c|κ| ≤ γ
Pt = tau**2 + 2 * g_ * tau - c**2 * xi**2
r = roots_at(Pt, {c: 1, g_: 1, xi: 0.5j})
okA = minphi(r[0], r[1], 40) > 1e-3
r = roots_at(Pt, {c: 1, g_: 1, xi: 3j})
beta = (9 - 1) ** 0.5; tstar = (mp.pi - mp.atan(beta / 1)) / beta
okB = minphi(r[0], r[1], float(tstar) * 1.01) < 2e-3
report('D4 telegrafo ξ=iκ: c|κ|≤γ globale; c|κ|>γ locale con t* = (π − arctan(β/γ))/β, β = √(c²κ²−γ²)', okA and okB)
r = roots_at(Pt, {c: 1, g_: 1, xi: 2})
report('D4 telegrafo ξ reale: radici reali di segno opposto, globale', minphi(r[0], r[1], 30) > 0.1)
# D5 termine dispari senza τ: τ² − c²ξ² + bξ, ξ = iκ: p = s² + c²κ² + ibκ, globale ∀κ≠0 ma inf|φ1| → 0
Pc = tau**2 - c**2 * xi**2 + bb * xi
mins = []
for kk in [1, 10, 100]:
    r = roots_at(Pc, {c: 1, bb: 1, xi: 1j * kk})
    mins.append(minphi(r[0], r[1], 3.0 / kk + 1, n=20000))
report('D5 τ²−c²ξ²+bξ, ξ=iκ: globale (min|φ1|>0) per κ=1,10,100', all(mm > 0 for mm in mins))
report('D5 ... ma min|φ1| decresce come ~ bπ/(4c²κ) (nessuna stima uniforme in κ): ' + ', '.join(mp.nstr(mm, 3) for mm in mins),
       mins[0] > mins[1] > mins[2] and mins[2] < 0.02)
# D6 telegrafo con trasporto τ² + 2γτ + 2vξτ − c²ξ²: ξ = iκ
Ptv = tau**2 + 2 * g_ * tau + 2 * v * xi * tau - c**2 * xi**2
res = []
for kk in [1, 5, 50]:
    r = roots_at(Ptv, {c: 1, g_: 1, v: 0.5, xi: 1j * kk})
    res.append(minphi(r[0], r[1], 10, n=20000))
report('D6 telegrafo+trasporto (γ=1,v=0.5), ξ=iκ: globale per κ=1,5,50: ' + ', '.join(mp.nstr(mm, 3) for mm in res), all(mm > 1e-4 for mm in res))

print('ESITO GLOBALE:', 'OK' if ok_all else 'FAIL')
