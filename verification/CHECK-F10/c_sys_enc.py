# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §8 (II-T2(b′)), §9 (SYS-MAXWELL), §10 (ENC-T2(c′)-P), §11 (ENC-Q4-S).
import sys, itertools, random
import sympy as sp
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

xi, tau = sp.symbols('xi tau')
# ---------- §8: proiettore spettrale su ker(A − ξ) lungo ker(A + ξ)(A + 2ξ), via basi saturate (metodo indipendente da B(A)/B(ξ))
A1 = sp.Matrix([[xi, 0, 0], [0, -xi, 1], [0, 0, -2*xi]])
A2 = sp.Matrix([[xi, 1, 0], [0, -xi, 0], [0, 0, -2*xi]])
def proj_bases(A):
    n = 3
    E = (A - xi*sp.eye(n)).nullspace()
    F = ((A + xi*sp.eye(n))*(A + 2*xi*sp.eye(n))).nullspace()
    # saturazione: moltiplico per il denominatore e divido per il gcd delle entrate (DVR in ξ = 0)
    def sat(v):
        v = sp.Matrix([sp.together(e) for e in v]); den = sp.lcm([sp.denom(e) for e in v]); v = (v*den).applyfunc(sp.expand)
        g = sp.gcd([e for e in v if e != 0]); return (v/g).applyfunc(sp.cancel)
    e = sp.Matrix.hstack(*[sat(v) for v in E]); f = sp.Matrix.hstack(*[sat(v) for v in F])
    EF = sp.Matrix.hstack(e, f)
    P = (sp.Matrix.hstack(e, sp.zeros(3, f.shape[1]))*EF.inv()).applyfunc(sp.cancel)
    return e, f, EF, P
for name, A in [("A_1", A1), ("A_2", A2)]:
    e, f, EF, P = proj_bases(A)
    d0 = sp.simplify(EF.det().subs(xi, 0)) if not sp.denom(sp.cancel(EF.det())).subs(xi, 0) == 0 else None
    pole = any(sp.denom(sp.cancel(x)).subs(xi, 0) == 0 for x in P)
    print(f"    {name}: det[e f](0) = {d0}, P = {P.tolist()}")
    if name == "A_1":
        ok("§8 A_1: det[e f](0) ≠ 0 e P senza polo (criterio (a))", d0 != 0 and not pole)
    else:
        ok("§8 A_2: det[e f](0) = 0 e P con polo (criterio (a))", d0 == 0 and pole)
    ok(f"§8 {name}: P idempotente, PA = AP", (P*P - P).applyfunc(sp.cancel) == sp.zeros(3) and (P*A - A*P).applyfunc(sp.cancel) == sp.zeros(3))
# rafforzamento: coniugando A_2 con una permutazione costante si ottiene A_2' con A_2'(0) = A_1(0) come MATRICE
S = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])   # e1→e2, e2→e3, e3→e1
A2p = S*A2*S.inv()
ok("§8 A_2' := S A_2 S^{-1} ha A_2'(0) = A_1(0) letteralmente", A2p.subs(xi, 0) == A1.subs(xi, 0))
ok("§8 A_2' ha lo stesso polinomio caratteristico di A_1", sp.expand(A2p.charpoly(tau).as_expr() - A1.charpoly(tau).as_expr()) == 0)
P2p = ((A2p + xi*sp.eye(3))*(A2p + 2*xi*sp.eye(3))/(6*xi**2)).applyfunc(sp.cancel)
ok("§8 A_2' ha ancora il polo (stessa A(ξ_0), stessa fattorizzazione, esito diverso)", any(sp.denom(x).has(xi) for x in P2p))

# ---------- §9 Maxwell
x1, x2, x3 = sp.symbols('xi1 xi2 xi3')
xv = sp.Matrix([x1, x2, x3])
Cx = sp.Matrix([[0, -x3, x2], [x3, 0, -x1], [-x2, x1, 0]])
ok("§9 C·v = ξ × v", (Cx*sp.Matrix(sp.symbols('v1 v2 v3')) - xv.cross(sp.Matrix(sp.symbols('v1 v2 v3')))).applyfunc(sp.expand) == sp.zeros(3, 1))
P = sp.zeros(8, 6)
P[0:3, 0:3] = tau*sp.eye(3); P[0:3, 3:6] = -Cx
P[3:6, 0:3] = Cx; P[3:6, 3:6] = tau*sp.eye(3)
P[6, 0:3] = xv.T; P[7, 3:6] = xv.T
ok("§9 det(τ²I + C²) = τ²(τ² − |ξ|²)² (blocchi commutanti)", sp.factor((tau**2*sp.eye(3) + Cx*Cx).det() - tau**2*(tau**2 - x1**2 - x2**2 - x3**2)**2) == 0)
ok("§9 rango di P su Frac(R) = 6", P.rank() == 6)
K = (P.T).nullspace()   # nucleo sinistro su Frac(R)
S1 = sp.Matrix([[x1, x2, x3, 0, 0, 0, -tau, 0]]); S2 = sp.Matrix([[0, 0, 0, x1, x2, x3, 0, -tau]])
Mspan = sp.Matrix.vstack(S1, S2, *[k.T for k in K])
ok("§9 il nucleo sinistro su Frac(R) ha dim 2 ed è generato da S_1, S_2", len(K) == 2 and Mspan.rank() == 2)
# Buchsbaum–Eisenbud (controllo indipendente dell'esattezza di 0 → R² → R^8 → R^6): ranghi 2 + 6 = 8 e
# l'ideale dei minori 2×2 di [S1;S2] ha radicale (τ, ξ), quindi profondità 4 ≥ 2; I_6(P) ≠ 0 ha profondità ≥ 1.
Smat = sp.Matrix.vstack(S1, S2)
minors2 = set(sp.expand(Smat[:, [i, j]].det()) for i, j in itertools.combinations(range(8), 2))
need = {tau**2, x1**2, x2**2, x3**2}
ok("§9 I_2(S) contiene τ², ξ_1², ξ_2², ξ_3² (radicale massimale omogeneo)", need <= minors2)
# profondità di I_6(P) ≥ 1: un minore non nullo, già visto. Quindi il complesso è esatto (BE), pd M_P ≤ 2 e,
# per Auslander–Buchsbaum, depth (M_P)_m ≥ 4 − 2 = 2 ≥ 1 in ogni m: Hom(k, M_P) = 0.
ok("§9 gcd delle entrate di S_1 (e di S_2) = 1 (passo 3, nucleo libero)", sp.gcd_list([x1, x2, x3, tau]) == 1)

# ---------- §10: P(∂_t, L_q)(e^{αt}f) = e^{αt} P(α, L_q) f per un P generico (q, f funzioni simboliche)
t, x, al = sp.symbols('t x alpha')
q = sp.Function('q')(x); fx = sp.Function('f')(x)
Lq = lambda g: -sp.diff(g, x, 2) + q*g
def applyP(coeffs, g):   # P = Σ c_{ij} τ^i σ^j
    out = 0
    for (i, j), cij in coeffs.items():
        h = g
        for _ in range(j): h = Lq(h)
        out += cij*sp.diff(h, t, i)
    return out
Pc = {(2, 0): 1, (1, 1): 3, (0, 3): -2, (0, 0): 5}
lhs = applyP(Pc, sp.exp(al*t)*fx)
rhs = sp.exp(al*t)*sum(cij*al**i*(lambda h: [h := Lq(h) for _ in range(j)] and h if j else h)(fx) for (i, j), cij in Pc.items())
ok("§10 P(∂_t, L_q)(e^{αt}f) = e^{αt}P(α, L_q)f", sp.simplify(sp.expand(lhs - rhs)) == 0)
# ordine e coefficiente di testa di p(L_q) = −2L_q³ + ...: costante (−2)(−1)³ = 2 davanti a f^{(6)}
p3 = sp.expand(Lq(Lq(Lq(fx))))
ok("§10 L_q³ ha ordine 6 e coefficiente di testa costante −1 (unicità di Cauchy applicabile)", p3.coeff(sp.diff(fx, x, 6)) == -1)
# passo 5 su polinomi: P_* = τ + σ² (esempio), α = 1: (τ − α) ∤ P_*, gcd = 1
Ps = tau + xi**2
ok("§10 scelta di α: P_*(α, σ) ≢ 0 e gcd(P_*, τ − α) = 1", sp.expand(Ps.subs(tau, 1)) != 0 and sp.gcd(Ps, tau - 1) == 1)

# ---------- §11: composizione di Volterra simmetrici e quasinilpotenza (discretizzazione)
random.seed(0); np.random.seed(0)
a = 1.0; Nn = 401
xs = np.linspace(-a, a, Nn); hgrid = xs[1] - xs[0]
def volterra_sym(kfun):
    M = np.zeros((Nn, Nn))
    for i, xx in enumerate(xs):
        for j, rr in enumerate(xs):
            if abs(rr) <= abs(xx) + 1e-12:
                M[i, j] = kfun(xx, rr)*hgrid*np.sign(xx if xx != 0 else 1)
    return M
K1 = volterra_sym(lambda x_, s_: np.cos(x_ + 2*s_)); K2 = volterra_sym(lambda x_, s_: 1 + x_*s_)
Comp = K1 @ K2
outside = max(abs(Comp[i, j]) for i in range(Nn) for j in range(Nn) if abs(xs[j]) > abs(xs[i]) + 1e-9)
ok("§11 D26: il composto di due Volterra simmetrici ha nucleo nullo per |r| > |x|", outside < 1e-12)
Vm = K1 + K2 + Comp
kn = np.abs(Vm).max()/hgrid
norms = []; Pw = np.eye(Nn)
for nn in range(1, 16):
    Pw = Vm @ Pw; norms.append(np.abs(Pw).sum(axis=1).max())
bound = [(2*kn*a)**nn/np.math.factorial(nn) if hasattr(np, 'math') else None for nn in range(1, 16)]
import math
bound = [(2*kn*a)**nn/math.factorial(nn) for nn in range(1, 16)]
ok("§11 ‖𝒱^n‖_∞ ≤ (2‖k‖a)^n/n! (n ≤ 15, discretizzato)", all(nv <= bv*1.05 for nv, bv in zip(norms, bound)))
ok("§11 raggio spettrale numerico ‖𝒱^15‖^{1/15} piccolo (quasinilpotenza)", norms[-1]**(1/15) < 0.5)
# passo 2: u' = e^{iθ_1}u con u ∈ 𝒮_{q0+c}, u' ∈ 𝒮_{q0+c'} ⇒ θ_1' = −δ
th = sp.Function('theta')(t); uu = sp.Function('u')(t, x); c, cp = sp.symbols('c cp', real=True)
q0 = sp.Function('q0')(x)
up = sp.exp(sp.I*th)*uu
res = sp.I*sp.diff(up, t) - (-sp.diff(up, x, 2) + (q0 + cp)*up)
res = res.subs(sp.Derivative(uu, t), (-sp.diff(uu, x, 2) + (q0 + c)*uu)/sp.I)
ok("§11 passo 2: residuo = (−θ' − (c' − c)) u'", sp.simplify(sp.expand(res - (-sp.diff(th, t) - (cp - c))*up)) == 0)

print(f"\n[c_sys_enc] {sum(c_ for _, c_ in RES)}/{len(RES)} OK")
