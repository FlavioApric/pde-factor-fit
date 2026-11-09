# S8-VAR — VAR-P8: (i) ad_{d^2}^j di un operatore di ordine k: coefficiente di d^{k+j} = 2^j c^{(j)};
# (ii) [f,[d^2,g]] = -2 f'g'; (iii) chiusura dell'algebra a 6 dimensioni per V quadratico;
# (iv) crescita dell'ordine/grado per V = x^3, e^x, sech^2 x (V lisci non polinomiali).
import sympy as sp
x = sp.Symbol('x'); F = sp.Function('F')(x)
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")
# operatori come dizionari {ordine: coefficiente}
def apply(op, f): return sum(c*sp.diff(f, x, k) for k, c in op.items())
def from_expr(e, maxo=12):
    # ricava i coefficienti di un operatore applicato a F
    e = sp.expand(e); op = {}
    for k in range(maxo, -1, -1):
        ck = sp.simplify(e.coeff(sp.Derivative(F, (x, k))) if k > 0 else e.subs({sp.Derivative(F, (x, j)): 0 for j in range(1, maxo+1)}).coeff(F))
        if ck != 0: op[k] = ck
    return op
def br(A, B): return from_expr(apply(A, apply(B, F)) - apply(B, apply(A, F)))
D2 = {2: sp.Integer(1)}
# (i)
c = sp.Function('c')(x)
P = {3: c, 1: sp.sin(x)}
okI = True; Q = P
for j in range(1, 4):
    Q = br(D2, Q)
    okI &= sp.simplify(Q.get(3 + j, 0) - 2**j*sp.diff(c, x, j)) == 0
report("(i) ad^j_{d^2}(c d^3 + ...) ha coefficiente di testa 2^j c^{(j)} (j=1..3)", okI)
# (ii)
f, g = sp.Function('f')(x), sp.Function('g')(x)
okII = sp.simplify(br({0: f}, br(D2, {0: g})).get(0, 0) + 2*sp.diff(f, x)*sp.diff(g, x)) == 0 and len(br({0: f}, br(D2, {0: g}))) == 1
report("(ii) [f,[d^2,g]] = -2 f' g'", okII)
# (iii) base dell'algebra per V quadratico
basis = [D2, {0: x**2}, {1: x, 0: sp.Rational(1, 2)}, {1: sp.Integer(1)}, {0: x}, {0: sp.Integer(1)}]
M = sp.Matrix([[sp.Poly(sum(B.get(k, 0)*sp.Symbol(f'e{k}') for k in range(3)), x, *sp.symbols('e0:3')).as_expr()] for B in basis])
def vec(op):
    # coordinate in base: coefficienti dei monomi x^a d^k con a<=2,k<=2
    v = []
    for k in range(3):
        pk = sp.Poly(sp.expand(op.get(k, 0)), x)
        for a in range(3): v.append(pk.coeff_monomial(x**a))
    return sp.Matrix(v)
Bm = sp.Matrix.hstack(*[vec(B) for B in basis])
okIII = True
for A in basis:
    for B in basis:
        C = br(A, B)
        if any(k > 2 or sp.Poly(sp.expand(cc), x).degree() > 2 for k, cc in C.items() if cc != 0): okIII = False; continue
        sol = Bm.gauss_jordan_solve(vec(C))
        okIII &= sol is not None
report("(iii) span{d^2, x^2, x d + 1/2, d, x, 1} chiuso per commutatori", okIII)
# (iv) crescita
def grow(V, steps=4):
    ords, degs = [], []
    f = {0: V}
    for _ in range(steps):
        f = br(f, br(D2, {0: V}))            # f -> -2 f' V'
        expr = sp.simplify(f.get(0, 0)); ords.append(expr)
    return ords
okIV = True
g3 = grow(x**3)
okIV &= [sp.Poly(e, x).degree() for e in g3] == [4, 5, 6, 7]
print("    V=x^3: gradi delle funzioni prodotte:", [sp.Poly(e, x).degree() for e in g3])
ge = grow(sp.exp(x), 3)
print("    V=e^x:", ge)
okIV &= all(sp.simplify(e / sp.exp((j + 2)*x)).is_constant() for j, e in enumerate(ge))
# V liscio non polinomiale: la funzione V non soddisfa V^{(m+1)} = 0 per nessun m: verifica per sech^2 (m <= 6)
Vpt = sp.sech(x)**2
okIV &= all(sp.simplify(sp.diff(Vpt, x, m)) != 0 for m in range(1, 8))
report("(iv) x^3: grado cresce; e^x: e^{kx} nuove; sech^2: nessuna derivata nulla", okIV)
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
