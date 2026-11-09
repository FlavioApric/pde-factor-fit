# F6-VAR — verifica SymPy (solo controllo).
# (a) Esempio di Landau (1902): fattorizzazioni di un LPDO in numero diverso di fattori irriducibili.
# (b) Algebra di Lie generata da d^2 e V(x): dimensione finita per V quadratico, crescita per V = x^3, e^x.
import sympy as sp

x, y = sp.symbols('x y')
f = sp.Function('f')(x, y)
ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1; r = bool(cond); ok += r
    print(('OK  ' if r else 'FAIL'), name)

Dx = lambda g: sp.diff(g, x)
Dy = lambda g: sp.diff(g, y)
Q = lambda g: Dx(g) + g                    # d_x + 1
S = lambda g: Dx(Dx(g)) + x*Dx(Dy(g)) + Dx(g) + (2 + x)*Dy(g)   # d_x^2 + x d_x d_y + d_x + (2+x) d_y

# Forma classica (Blumberg/Landau, v. Tsarev 2005, Grigoriev-Schwarz):
# L = Q Q P, P = d_x + x d_y ;  L = S Q, S = d_x^2 + x d_x d_y + d_x + (2+x) d_y (S irriducibile, Landau)
P = lambda g: Dx(g) + x*Dy(g)
L_a = sp.expand(Q(Q(P(f))))
L_b = sp.expand(S(Q(f)))
check('Landau: Q Q P = S Q (3 fattori irriducibili contro 2)', sp.simplify(L_a - L_b) == 0)
print('   L f =', L_a)

# S irriducibile nella classe dei fattori del primo ordine a coeff. polinomiali (controllo parziale):
# cerca S = (d_x + a d_y + b)(d_x + c d_y + e) con a,b,c,e polinomi di grado <= 1 in x,y
cs = sp.symbols('c0:12')
a = cs[0] + cs[1]*x + cs[2]*y; b = cs[3] + cs[4]*x + cs[5]*y
c = cs[6] + cs[7]*x + cs[8]*y; e = cs[9] + cs[10]*x + cs[11]*y
F1 = lambda g: Dx(g) + c*Dy(g) + e*g
F2 = lambda g: Dx(g) + a*Dy(g) + b*g
diff = sp.expand(F2(F1(f)) - S(f))
derivs = [f.diff(x, 2), f.diff(x, y), f.diff(y, 2), f.diff(x), f.diff(y), f]
eqs = []
for dd in derivs:
    coeff = sp.expand(diff.coeff(dd)) if dd != f else sp.expand(diff.subs({f.diff(x,2):0, f.diff(x,y):0, f.diff(y,2):0, f.diff(x):0, f.diff(y):0}).coeff(f))
    eqs += sp.Poly(coeff, x, y).coeffs()
sol = sp.solve(eqs, cs, dict=True)
check('S non fattorizza in due fattori del 1o ordine con coeff. polinomiali di grado<=1 (controllo PARZIALE; irriducibilita generale: Landau 1902)', sol == [])

# (b) Lie: operatori agenti su g(x)
g = sp.Function('g')(x)
def lie_dim(V, depth=3, K=14):
    dsym = sp.symbols('d0:%d' % K)
    def vec(E):
        r = sp.expand(E(g))
        for k in range(K-1, -1, -1):
            r = r.subs(sp.diff(g, x, k) if k > 0 else g, dsym[k])
        P = sp.Poly(sp.expand(r), x, *dsym)
        return {m: c for m, c in P.terms()}
    A = lambda h: sp.diff(h, x, 2)
    B = lambda h: sp.expand(V*h)
    elems = [A, B]; reps = [vec(A), vec(B)]
    def indep(reps):
        keys = sorted(set(k for r in reps for k in r))
        return sp.Matrix([[r.get(k, 0) for k in keys] for r in reps]).rank()
    for _ in range(depth):
        cur = list(elems)
        for X in cur:
            for Y in cur:
                C = (lambda X, Y: (lambda h: sp.expand(X(Y(h)) - Y(X(h)))))(X, Y)
                v = vec(C)
                if not v: continue
                if indep(reps + [v]) > len(reps):
                    reps.append(v); elems.append(C)
        if len(elems) > 10: break
    maxord = max(int(str(m)[0]) if False else max([i for i, e in enumerate(mon[1:]) if e] + [0]) for r in reps for mon in r)
    return len(elems), maxord

d2, o2 = lie_dim(x**2, depth=3)
print('   V=x^2: dim', d2, 'ordine max', o2)
check('V = x^2: algebra di dimensione finita (sl2 + centro: <= 4), ordine <= 2', d2 <= 4 and o2 <= 2)
d1, o1 = lie_dim(x, depth=3)
print('   V=x: dim', d1, 'ordine max', o1)
check('V = x: algebra di dimensione 4 {d^2, x, d, 1}', d1 == 4)
d3, o3 = lie_dim(x**3, depth=2)
d3b, o3b = lie_dim(x**3, depth=3)
print('   V=x^3: dim', d3, '(prof. 2),', d3b, '(prof. 3); ordine max', o3b)
check('V = x^3: crescita con la profondita (dim prof.2 > 4 e prof.3 > prof.2)', d3 > 4 and d3b > d3)
# funzioni: [f,[d^2,g]] = -2 f' g' : da V = x^3 si ottiene grado 2*3-2 = 4 > 3
fx = sp.expand(x**3*sp.diff(sp.diff(x**3*g, x, 2), x, 0))
h = sp.expand((lambda F, G: F*(sp.diff(G*g, x, 2)) - sp.diff(G*F*g, x, 2) - (G*sp.diff(F*g, x, 2) - F*G*sp.diff(g, x, 2))*0)(x**3, x**3))
c = sp.expand(x**3*(sp.diff(x**3*g, x, 2) - x**3*sp.diff(g, x, 2)) - (sp.diff(x**3*x**3*g, x, 2) - x**3*sp.diff(x**3*g, x, 2)))
check("[V,[d^2,V]] = -2 (V')^2 g = -18 x^4 g per V = x^3", sp.simplify(c + 18*x**4*g) == 0)

# nilpotenza per {d^2, x}: commutatori annidati di ordine 4 nulli
A = lambda h: sp.diff(h, x, 2); B = lambda h: x*h
com = lambda X, Y: (lambda h: sp.expand(X(Y(h)) - Y(X(h))))
gens = [A, B]
zero4 = True
for X in gens:
    for Y in gens:
        for Z in gens:
            for W in gens:
                if sp.expand(com(X, com(Y, com(Z, W)))(g)) != 0:
                    zero4 = False
check('{d^2, x}: tutti i commutatori annidati di lunghezza 4 sono nulli (nilpotente, Magnus termina)', zero4)
nz3 = any(sp.expand(com(X, com(Y, Z))(g)) != 0 for X in gens for Y in gens for Z in gens)
check('{d^2, x}: esiste un commutatore di lunghezza 3 non nullo (passo esattamente 3)', nz3)
print(f'{ok}/{tot} OK')
