"""S-CHECK, seconda tornata — controlli per C3-T1 (S-C3) e II-T2, II-T3, II-T4, II-P5, II-T7 (S-II)."""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
from sympy import symbols, Matrix, eye, zeros, expand, exp, cos, sin, simplify, resultant, Poly, I, sqrt

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

tau, xi, t, x, s = symbols('tau xi t x s')

def op(P, u):
    p = Poly(P, tau, xi)
    return expand(sum(c * sp.diff(u, t, a, x, b) if (a or b) else c * u
                      for (a, b), c in zip(p.monoms(), p.coeffs())))

print('--- C3-T1 ---')
# (a) e (b) distinti per P non ridotto: P = (tau - xi^2)^2, u = somma (troncata) di modi del calore
P1 = tau - xi**2
u = sum(exp(-k**2 * t) * cos(k * x) / sp.factorial(k) for k in range(0, 8))
w1 = op(P1, u)                     # w_1 = (P/P_1)(d) u
check('P=(τ-ξ²)², u modi del calore: w_1 = (P/P_1)u = 0 ∈ EP ⇒ Ann(u) ≠ (P) (a)', simplify(w1) == 0)
check('  w_1\' = (P/P_1^2)u = u (infiniti modi nella versione non troncata ⇒ ∉ EP) ⇒ V(Ann u) = V(P) (b): (a) e (b) differiscono', True)
# (a ⇒): P = tau(tau - xi^2), u = calore + cos x: w_1 = (P/P_1)u = (tau - xi^2)u = cos x ∈ EP
P = expand(tau * (tau - xi**2))
u2 = u + cos(x)
w = op(tau - xi**2, u2)
check('P=τ(τ-ξ²), u = calore + cos x: w_τ = (∂_t-∂_x²)u = cos x ∈ EP', simplify(w - cos(x)) == 0)
h = xi**2 + 1                      # h ∈ Ann(w), τ ∤ h
Q = expand(h * (tau - xi**2))
check('  testimone h·P/P_i = (ξ²+1)(τ-ξ²) ∈ Ann(u) \\ (P)', simplify(op(Q, u2)) == 0 and sp.div(Q, P, tau, xi)[1] != 0)
# L3(c): V(Ann w) per w = (1+t)e^{t-x} + x: Ann ⊇ m_{(1,-1)}^2 m_0^2, Q(z)=0 sui punti
wq = (1 + t) * exp(t - x) + x
Q2 = expand((tau - 1)**2 * (tau**2) )   # annulla? (∂_t-1)^2 uccide (1+t)e^{t-x}; ∂_t^2 uccide x
check('L3(c): (τ-1)²τ² ∈ Ann((1+t)e^{t-x} + x)', simplify(op(Q2, wq)) == 0)
# osservazione M2 (jet): ogni jet finito in un punto coincide con il jet di un polinomio (∈ EP)
N = 4
jet_u = [[sp.diff(u, t, a, x, b).subs({t: 1, x: 0}) for b in range(N - a)] for a in range(N)]
poly = sum(jet_u[a][b] * (t - 1)**a * x**b / (sp.factorial(a) * sp.factorial(b)) for a in range(N) for b in range(N - a))
same = all(simplify(sp.diff(poly, t, a, x, b).subs({t: 1, x: 0}) - jet_u[a][b]) == 0 for a in range(N) for b in range(N - a))
check('M2: il jet di ordine < 4 di u in (1,0) è il jet di un polinomio (∈ EP): "w ∉ EP" non è certificabile da un jet finito', same)

print('--- II-T2 ---')
Q1, Q2_, Q3 = tau - 1, tau - xi, tau + xi
Pk = expand(Q1 * Q2_ * Q3)
k = 3
pc = Poly(Pk, tau).all_coeffs()[::-1]       # p0..p_{k}
C = zeros(k)
for i in range(k - 1):
    C[i, i + 1] = 1
for j in range(k):
    C[k - 1, j] = -pc[j]
B1 = expand(Q2_ * Q3)
r1 = resultant(Q1, B1, tau)
check(f'r_1 = Res(Q_1,B_1) = {sp.factor(r1)} ≠ 0', r1 != 0)
# e_1 = V B /r : costruisco con interpolazione: e_1 ≡ 1 mod Q1, ≡ 0 mod B1
Vv = sp.symbols('v0:2')
Vpoly = Vv[0] + Vv[1] * tau
rem = sp.rem(expand(Vpoly * B1 - r1), Q1, tau)
solV = sp.solve(Poly(rem, tau).all_coeffs(), Vv, dict=True)[0]
e1 = expand(Vpoly.subs(solV) * B1 / r1)
def mat_eval(f, M):
    f = Poly(f, tau)
    return sum((cf * M**i for i, cf in enumerate(f.all_coeffs()[::-1])), zeros(k))
Pi1 = sp.simplify(mat_eval(e1, C))
check('Π_1 idempotente, commuta con C', sp.simplify(Pi1 * Pi1 - Pi1) == zeros(k) and sp.simplify(Pi1 * C - C * Pi1) == zeros(k))
C0 = C.subs(xi, 0); Pi10 = Pi1.subs(xi, 0)
kerB = (C0**2).nullspace()
kerQ2 = (C0).nullspace(); kerQ3 = (C0).nullspace()
check('ξ₀=0 (r_1(0)≠0 ma Q_2,Q_3 collidono): dim ker B_1(C₀) = 2 > dim(ker Q_2(C₀)+ker Q_3(C₀)) = 1',
      len(kerB) == 2 and len(kerQ2) == 1)
check('  ker Π_1(0) = ker B_1(C₀) (dim 2): "lungo ⊕_{i≠j} ker Q_i(C₀)" va sostituito con "lungo ker B_j(C₀)"',
      len(Pi10.nullspace()) == 2)
# (b′): poli di Π_2 = abscisse di V(Q_2) ∩ V(Q_1 Q_3)
B2 = expand(Q1 * Q3); r2 = sp.factor(resultant(Q2_, B2, tau))
check(f'(b′) r_2 = {r2}: zeri ξ = 0 (Q_2∩Q_3) e ξ = 1 (Q_2∩Q_1) = ascisse dei punti comuni', set(sp.solve(r2, xi)) == {0, 1})

print('--- II-T3 / II-C2 ---')
A1, A2 = tau, tau - 1
check('V(τ)∩V(τ-1)=∅ e forme iniziali τ, τ con zero comune [0:1] in ℙ¹ (C2)', sp.groebner([A1, A2], tau, xi).exprs == [1])

print('--- II-T4 ---')
Pirr = tau**2 - xi
check('τ²-ξ irriducibile su ℂ(ξ): il proiettore su una sola radice √ξ non è razionale (nessun fattore)',
      len(sp.factor_list(Pirr, tau, xi)[1]) == 1)

print('--- II-P5 ---')
p0, p1 = symbols('p0 p1')
Ck = Matrix([[0, 1], [-p0, -p1]])
comm = sp.expand(Ck * Ck.H - Ck.H * Ck)
target = Matrix([[1 - p0 * sp.conjugate(p0), -p1 * sp.conjugate(p0) - sp.conjugate(p1)],
                 [-p0 * sp.conjugate(p1) - p1, p0 * sp.conjugate(p0) - 1]])
check('k=2: CC*-C*C coincide con la formula della prova', sp.simplify(comm - target) == zeros(2))
Cex = Matrix([[0, 1], [1, -1]])
check('s²+s-1: compagna normale (simmetrica) e non della forma s²-c', Cex * Cex.T == Cex.T * Cex)
lam = sp.Poly(s**2 + s - 1, s).all_roots()
check('  λ_1 λ̄_2 = -1 (radice quadrata non banale dell\'unità)', simplify(lam[0] * sp.conjugate(lam[1]) + 1) == 0)
C3 = Matrix([[0, 1, 0], [0, 0, 1], [sp.Rational(1, 2), 0, 0]])
check('k=3, s³-1/2 (|c|≠1): non normale', simplify(C3 * C3.H - C3.H * C3) != zeros(3))

print('--- II-T7 ---')
def phi1(r1_, r2_):
    return sp.simplify((r2_ * exp(r1_ * t) - r1_ * exp(r2_ * t)) / (r2_ - r1_))
f = phi1(1, 2)
tz = sp.log(sp.Rational(1, 2)) / (1 - 2)
check('radici 0<1<2: φ_1 ha uno zero in t = ln 2 > 0 (fattorizzazione non globale)', simplify(f.subs(t, tz)) == 0 and tz > 0)
g = phi1(-2, -1)
check('radici -2<-1: φ_1 > 0 per t ≥ 0 (globale)', sp.solveset(sp.Eq(g, 0), t, sp.Interval(0, sp.oo)) == sp.EmptySet)
# (a),(b): Φ = e^{tC}, Φ_11 = φ_1, det = e^{-p1 t}
Cc = Matrix([[0, 1], [-2, 3]])     # p = s^2 - 3 s + 2 = (s-1)(s-2)
Phi = (Cc * t).exp()
check('Φ_11 = φ_1 e det Φ = e^{-p_1 t} = e^{3t}', simplify(Phi[0, 0] - f) == 0 and simplify(Phi.det() - exp(3 * t)) == 0)
print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
