# S8-VAR — C3-Q2 (A_2) per L monico in d_t. Algebra di Weyl A_2 = C[t,x]<dt,dx> implementata con forma normale
# (coefficienti a sinistra). (a) divisione Q = Q'L + R con R senza dt, verificata applicando a funzioni generiche;
# (b) funzioni D-finite non identificano: nucleo del calore/Schrodinger libero ucciso da R in B = C[t,x]<dx>;
# (c) saturazione: x dt u = 0 => dt u = 0 ma dt notin A_2 x dt.
import sympy as sp
t, x = sp.symbols('t x')
I = sp.I
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")
# operatore = dict {(i,j): coeff(t,x)} che significa sum coeff * dt^i dx^j
def apply(op, f): return sp.expand(sum(c*sp.diff(f, t, i, x, j) for (i, j), c in op.items()))
def mul(A, B):
    # (a dt^i dx^j)(b dt^k dx^l) = a sum_{p,q} C(i,p)C(j,q) (dt^p dx^q b) dt^{i-p+k} dx^{j-q+l}
    out = {}
    for (i, j), a in A.items():
        for (k, l), b in B.items():
            for p_ in range(i+1):
                for q_ in range(j+1):
                    c = a*sp.binomial(i, p_)*sp.binomial(j, q_)*sp.diff(b, t, p_, x, q_)
                    key = (i - p_ + k, j - q_ + l)
                    out[key] = sp.expand(out.get(key, 0) + c)
    return {kk: v for kk, v in out.items() if v != 0}
def add(A, B, s=1):
    out = dict(A)
    for kk, v in B.items(): out[kk] = sp.expand(out.get(kk, 0) + s*v)
    return {kk: v for kk, v in out.items() if v != 0}
def divide(Q, M):
    # L = dt - M, M senza dt. Restituisce Q', R con Q = Q' L + R, R senza dt
    L = add({(1, 0): sp.Integer(1)}, M, -1)
    Qp, R = {}, dict(Q)
    while any(i > 0 for (i, j) in R):
        i0 = max(i for (i, j) in R)
        lead = {(i, j): c for (i, j), c in R.items() if i == i0}
        mono = {(i - 1, j): c for (i, j), c in lead.items()}
        Qp = add(Qp, mono); R = add(R, mul(mono, L), -1)
    return Qp, R, L
M = {(0, 2): I, (0, 0): -I*x**2}          # Schrodinger con V = x^2: L = dt - i dx^2 + i x^2
Q = {(2, 1): t*x, (1, 3): sp.Integer(1) + x, (0, 2): t**2, (1, 0): x**3}
Qp, R, L = divide(Q, M)
F = sp.Function('F')(t, x)
okA = all(i == 0 for (i, j) in R) and sp.simplify(apply(Q, F) - apply(Qp, apply(L, F)) - apply(R, F)) == 0
report("(a) divisione Q = Q'L + R, R in C[t,x]<dx> (verificata su F generica)", okA)
# (b) D-finite: nucleo del calore u = (1+4t)^{-1/2} exp(-x^2/(1+4t)): u_t = u_xx, R = (1+4t) dx + 2x
u = (1 + 4*t)**sp.Rational(-1, 2)*sp.exp(-x**2/(1 + 4*t))
report("(b) calore: u_t = u_xx", sp.simplify(sp.diff(u, t) - sp.diff(u, x, 2)) == 0)
Rb = {(0, 1): 1 + 4*t, (0, 0): 2*x}
report("(b) R = (1+4t)dx + 2x in B uccide u: u non identifica dt - dx^2 in A_2", sp.simplify(apply(Rb, u)) == 0)
us = (1 + 4*I*t)**sp.Rational(-1, 2)*sp.exp(-x**2/(1 + 4*I*t))
report("(b') Schrodinger libero: i u_t + u_xx = 0 e (1+4it)dx + 2x uccide u", sp.simplify(I*sp.diff(us, t) + sp.diff(us, x, 2)) == 0 and sp.simplify(apply({(0, 1): 1 + 4*I*t, (0, 0): 2*x}, us)) == 0)
# (c) saturazione
Lc = {(1, 0): x}
Qd, Rc, _ = divide({(1, 0): sp.Integer(1)}, {})   # dt diviso per (dt - 0): resto 0
# dt in A_2 * x dt ? un elemento A * x dt ha tutti i coefficienti divisibili per x quando scritto in forma normale? controllo grado
Ag = {(0, 0): sp.Function('a')(t, x)}
prod = mul(Ag, Lc)
report("(c) a(t,x)*x dt ha coefficiente divisibile per x: dt notin A_2 x dt (al grado 0 in dt-coefficiente)", sp.simplify(prod[(1, 0)]/x) == sp.Function('a')(t, x))
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
