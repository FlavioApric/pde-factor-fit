# S4-ID — verifiche SymPy (solo CONTROLLO dei claim di PROOF_PACKAGE.md; mai metodo).
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I s4id_checks.py  > s4id_checks.out
# Aritmetica esatta su QQ (DomainMatrix); esponenziali E_i trattati come indeterminate formali
# (caso non risonante), derivazione D E_i = k_i E_i.
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from sympy import QQ
from jetrel import burgers_nshock, kdv_nsoliton
from reduction_checks import Psi, V_dk, H_Dk, kernel_dim

RES = []
def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(f"[{'OK' if cond else 'FAIL'}] {name} {info}", flush=True)

# ---------------------------------------------------------------- P1: [F] ∩ V_{d,k}
for name, n, cases in [('burgers', 2, [(2, 2, '=1'), (2, 3, '>=2'), (3, 2, '>=2')]),
                       ('fisher', 2, [(2, 2, '=1'), (2, 3, '>=2'), (3, 2, '>=2')]),
                       ('kdv', 3, [(2, 3, '=1'), (2, 4, '>=2'), (3, 3, '>=2')]),
                       ('kdvb', 3, [(2, 3, '=1')])]:
    psi = Psi(name)
    for d, k, exp in cases:
        kd = kernel_dim(V_dk(psi, d, k))
        ok = (kd == 1) if exp == '=1' else (kd >= 2)
        check(f"P1 {name} dim([F] cap V_(d={d},k={k})) {exp}", ok, f"(trovato {kd})")
psi = Psi('burgers', nu=sp.Rational(1, 3))
check("P1 burgers nu=1/3 dim([F] cap V_(2,2)) = 1", kernel_dim(V_dk(psi, 2, 2)) == 1)

# ---------------------------------------------------------------- L4: Hammerstein
psi = Psi('burgers')
for D, k in [(2, 2), (2, 3), (2, 4), (3, 3), (3, 4)]:
    kd = kernel_dim(H_Dk(psi, D, k))
    check(f"L4 [F_B] cap H_(D={D},ord<={k}) = R.F_B cap H", kd == (k-1)*k//2, f"(dim {kd})")

# ---------------------------------------------------------------- triangolarita' di psi (L2)
y = psi.y
for (a, b) in [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0)]:
    p = psi.theta(a, b)
    m = 2*a + b
    lead_ok = sp.expand(sp.diff(p, y[m])) == sp.Integer(1)**a and all(not p.has(y[j]) for j in range(m+1, 30))
    check(f"L2 psi(d_t^{a} d_x^{b} y) = nu^a y_{m} + (ordine < {m})  [nu=1]", lead_ok)

# ---------------------------------------------------------------- T2: N-shock di Burgers
def bell_R(ks):
    """R_N in variabili w_j: sum_{m=1}^{N+1} e_m r_m, r_{m+1} = D r_m + w0 r_m, r_0 = 1."""
    N = len(ks)
    w = sp.symbols('w0:%d' % (N+2))
    def Dw(p):
        return sp.expand(sum(sp.diff(p, w[j])*w[j+1] for j in range(N+1)))
    r = [sp.Integer(1)]
    for mm in range(N+1):
        r.append(sp.expand(Dw(r[-1]) + w[0]*r[-1]))
    z = sp.Symbol('z')
    poly = sp.Poly(sp.expand(z*sp.prod([z - sp.nsimplify(k) for k in ks])), z)
    e = {mm: poly.coeff_monomial(z**mm) for mm in range(N+2)}
    R = sp.expand(sum(e[mm]*r[mm] for mm in range(1, N+2)))
    return w, R

for ks in [(1,), (1, 3), (1, 3, 7), (2, -1, 5)]:
    N = len(ks)
    w, R = bell_R(ks)
    # w = phi_x/phi  <=> modello burgers con nu = -1/2 (u = -2 nu phi_x/phi = phi_x/phi)
    m = burgers_nshock(ks, nu=sp.Rational(-1, 2))
    P = m.jet(N)
    # R(w-jet) = 0 ? : sostituisce w_j = P_j/phi^{j+1}, moltiplica per phi^{(N+1)(N+1)}
    top = (N+1)*(N+1)
    tot = sp.Poly(0, *m.gens, domain=QQ)
    Rp = sp.Poly(R, *w[:N+1], domain=QQ)
    for mon, c in Rp.as_dict().items():
        term = sp.Poly(c, *m.gens, domain=QQ); wt = 0
        for j, ex in enumerate(mon):
            for _ in range(ex):
                term = term*P[j]; wt += j+1
        term = term*m.Q**(top - wt)
        tot += term
    check(f"T2(b) N={N} k={ks}: R_N(w,...,w^(N)) = 0 identicamente", tot.is_zero)
    check(f"T2(b) N={N}: R_N lineare in w_N con coeff. 1, grado {N+1}",
          sp.diff(R, w[N]) == 1 and sp.Poly(R, *w[:N+1]).total_degree() == N+1)
    if N <= 3:
        n0, _ = m.rel_dim(N+3, N-1) if N >= 2 else (None, None)
        if N >= 2:
            check(f"T2(a) N={N}: J cap Q[y0..y_(N-1)]_(deg<= {N+3}) = 0", n0 == 0, f"(dim {n0})")
        n1, _ = m.rel_dim(N, N)
        n2, _ = m.rel_dim(N+1, N)
        check(f"T2(b) N={N}: dim J cap A_(<=N,<=N) = 0 e dim J cap A_(<=N+1,<=N) = 1", n1 == 0 and n2 == 1, f"({n1},{n2})")

# T2(c)-congettura K1: nessuna relazione di grado <= N a ordine > N (V-ex)
m2 = burgers_nshock((1, 3))
for K in [3, 4, 5, 6]:
    n, _ = m2.rel_dim(2, K)
    check(f"K1 (V-ex) Burgers N=2: dim J cap A_(<=2,<= {K}) = 0", n == 0)
m3 = burgers_nshock((1, 3, 7))
for K in [4, 5]:
    n, _ = m3.rel_dim(3, K)
    check(f"K1 (V-ex) Burgers N=3: dim J cap A_(<=3,<= {K}) = 0", n == 0)

# Jacobiano in E = 0 (prova di T2(a)/T3(a)): det (k_i^{j+1}) e det(2 k_i^{j+2})
for ks in [(1, 3), (1, 2, 4)]:
    N = len(ks)
    for label, model in [('Burgers', burgers_nshock(ks, nu=sp.Rational(-1, 2))), ('KdV', kdv_nsoliton(ks))]:
        P = model.jet(N-1)
        cpow = model.c
        fun = [sp.Poly(P[j], *model.gens).as_expr()/model.Q.as_expr()**(j+cpow) for j in range(N)]
        J = sp.Matrix(N, N, lambda j, i: sp.diff(fun[j], model.E[i]))
        detE0 = sp.simplify(J.subs({e: 0 for e in model.E}).det())
        check(f"T2(a)/T3(a) Jacobiano {label} N={N} k={ks} in E=0 non nullo", detE0 != 0, f"(det = {detE0})")

# ---------------------------------------------------------------- T3: KdV N-solitoni
k1 = kdv_nsoliton((1,))
check("T3 KdV N=1: J cap A_(<=2,<=1) = 0, J cap A_(<=3,<=1) dim 1", k1.rel_dim(2, 1)[0] == 0 and k1.rel_dim(3, 1)[0] == 1)
rels = k1.kernel(3, 1)
yy = sp.symbols('y0:4')
target = yy[1]**2 - yy[0]**2 + 2*yy[0]**3
check("T3 KdV N=1: la relazione d'ordine 1 e' y1^2 - k^2 y0^2 + 2 y0^3 (k=1)",
      len(rels) == 1 and sp.simplify(rels[0]/target).is_number)
k2 = kdv_nsoliton((1, 2))
check("T3 KdV N=2 (k=1,2): J cap A_(<=3,<=3) = 0", k2.rel_dim(3, 3)[0] == 0)
check("T3 KdV N=2 (k=1,2): J cap A_(<=4,<=3) != 0 (dim 2)", k2.rel_dim(4, 3)[0] == 2)
check("T3 KdV N=2 (k=1,2): J cap A_(<=3,<=4) dim 3 (Novikov integrata, grado 3)", k2.rel_dim(3, 4)[0] == 3)
# il calcolo d=7,8 a ordine 2 e' in explore2_k2b.out (grado minimo 8)

# ---------------------------------------------------------------- MON-1 (1-shock)
m1 = burgers_nshock((sp.Rational(1),), nu=sp.Rational(1))
monos = [(2,), (1,), (0, 1)]   # y2, y1, y0 y1
n, _ = m1.rel_dim(None, 2, monos=monos)
check("MON-1 1-shock: relazione in span{y2, y1, y0 y1} (nu, f' non identificati)", n == 1)
m2b = burgers_nshock((1, 3), nu=sp.Rational(1))
monos = [(2,), (1,), (0, 1), (0, 0, 1), (0, 0, 0, 1)]
n, _ = m2b.rel_dim(None, 2, monos=monos)
check("MON-1 2-shock: nessuna relazione in span{y2, y1, y0 y1, y0^2 y1, y0^3 y1}", n == 0)

# ---------------------------------------------------------------- INT-Q1: onde piane
A, kap, th, x = sp.symbols('A kappa theta x')
pw = A*sp.cos(kap*x + th)
jet = [sp.diff(pw, x, j) for j in range(6)]
Y = sp.symbols('y0:6')
def ev(p):
    return sp.simplify(sp.expand_trig(p.subs({Y[j]: jet[j] for j in range(6)})))
check("Q1 y0 y3 - y1 y2 in I_PW", ev(Y[0]*Y[3] - Y[1]*Y[2]) == 0)
check("Q1 y0 y4 - y2^2 in I_PW", ev(Y[0]*Y[4] - Y[2]**2) == 0)
check("Q1 parte minima della relazione del 1-solitone (y1^2 - k^2 y0^2) non in I_PW", ev(Y[1]**2 - Y[0]**2) != 0)
check("Q1 parte lineare di Novikov N=2 (y4 - 5 y2 + 4 y0) non in I_PW", ev(Y[4] - 5*Y[2] + 4*Y[0]) != 0)
# forma lineare sum c_j y_j su A cos(kx+th): A kap^j cos(th + j pi/2); righe per th in {0, pi/2}, kap = 1..5
rows = []
for kv in range(1, 6):
    for thv in [0, sp.pi/2]:
        rows.append([kv**j*sp.cos(thv + j*sp.pi/2) for j in range(5)])
check("Q1 nessuna forma lineare non nulla (ordine<=4) in I_PW", sp.Matrix(rows).rank() == 5)

# ---------------------------------------------------------------- T4(ii): soglia di conteggio
from math import comb
def Dstar(n, a, b):
    c = b*(n+1) + max(a-b, 0)
    return (n+1)*c**n - n, c
for (n, a, b) in [(1, 1, 1), (2, 1, 1), (3, 2, 2)]:
    D, c = Dstar(n, a, b)
    check(f"T4(ii) conteggio n={n},a={a},b={b}: binom(D*+n+1,n+1) > binom(c D*+n,n)",
          comb(D+n+1, n+1) > comb(c*D+n, n), f"(D*={D}, c={c})")

print(f"\nTOTALE: {sum(1 for _, ok in RES if ok)}/{len(RES)} OK")
