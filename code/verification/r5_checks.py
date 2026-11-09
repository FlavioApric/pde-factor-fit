"""R5 - controlli simbolici (SymPy) per REPORT.md. Eseguire con:
D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I r5_checks.py
Solo CONTROLLI di enunciati (vincolo k3), nessuna numerica come metodo."""
import sympy as sp

t, x, k, D, c, s, r = sp.symbols('t x k D c s r', real=True)
ok = lambda name, expr: print(f"[{'OK' if sp.simplify(expr) == 0 else 'FAIL'}] {name}")

# ---------- C1: heat + trasporto (commutanti) ----------
# A1 = D d^2/dx^2, A2 = -c d/dx ; test e^{kx} (autofunzioni comuni)
u0 = sp.exp(k*x)
S1 = lambda f, tt: f.subs(x, x) * 0 + sp.exp(D*k**2*tt) * sp.exp(k*x)  # e^{tA1} e^{kx}
u = sp.exp(D*k**2*t - c*k*t + k*x)                                      # e^{tA2}e^{tA1}e^{kx}
ok("C1a u=e^{tA1}e^{tA2}e^{kx} risolve u_t = D u_xx - c u_x", sp.diff(u, t) - D*sp.diff(u, x, 2) + c*sp.diff(u, x))
# soluzione fondamentale: nucleo del calore traslato
G = sp.exp(-(x - c*t)**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t)
ok("C1b G(t,x-ct) risolve advezione-diffusione", sp.diff(G, t) - D*sp.diff(G, x, 2) + c*sp.diff(G, x))
u1 = sp.exp(D*k**2*t + k*x); u2 = sp.exp(-c*k*t + k*x)
Eadd = u - u1 - u2 + u0
ok("C1c E_int^add = (S1-I)(S2-I)u0 (G3, bilineare)", Eadd - (sp.exp(D*k**2*t)-1)*(sp.exp(-c*k*t)-1)*u0)

# ---------- C2: complessita' N termini commutanti ----------
N = 5
z = sp.symbols('z1:%d' % (N+1))
prod = sp.Mul(*[1+zi for zi in z])
lhs = sp.expand(prod - 1 - sum(z))
esym = [sp.expand(sum(sp.Mul(*cmb) for cmb in __import__('itertools').combinations(z, kk))) for kk in range(N+1)]
ok("C2 Prod(1+z_n)-1-Sum z_n = Sum_{k>=2} e_k(z)  (2^N-N-1 monomi, valutabile in O(N))", lhs - sum(esym[2:]))
print("     numero monomi:", len(sp.Add.make_args(lhs)), "= 2^N-N-1 =", 2**N-N-1)

# ---------- C3: Zassenhaus/BCH al 2-3 ordine con simboli non commutativi ----------
X, Y = sp.symbols('X Y', commutative=False)
def expser(Z, n=4):
    return sum((Z**j)/sp.factorial(j) for j in range(n+1))
def tdeg_trunc(e, n):
    e = sp.expand(e)
    out = 0
    for term in sp.Add.make_args(e):
        cpart, _ = term.args_cnc()
        d = sp.degree(sp.Mul(*cpart), t) if cpart else 0
        if d <= n:
            out += term
    return out
comm = lambda a, b: a*b - b*a
C2 = -sp.Rational(1, 2)*comm(X, Y)
C3 = sp.Rational(1, 3)*comm(Y, comm(X, Y)) + sp.Rational(1, 6)*comm(X, comm(X, Y))
lhs = expser(t*(X+Y), 3)
rhs = expser(t*X, 3)*expser(t*Y, 3)*expser(t**2*C2, 1)*expser(t**3*C3, 1)
diff = tdeg_trunc(lhs - rhs, 3)
ok("C3 Zassenhaus e^{t(X+Y)} = e^{tX}e^{tY}e^{t^2 C2}e^{t^3 C3} + O(t^4)", diff)
# BCH 2o ordine: log(e^{tX}e^{tY}) = t(X+Y) + t^2/2 [X,Y] + O(t^3)
Z = t*(X+Y) + t**2/2*comm(X, Y)
ok("C3b BCH: e^{tX}e^{tY} = e^{t(X+Y)+t^2/2[X,Y]} + O(t^3)", tdeg_trunc(expser(t*X, 2)*expser(t*Y, 2) - expser(Z, 2), 2))

# ---------- C4: caso nilpotente  A1 = d^2, A2 = x  (Zassenhaus finito) ----------
# e^{t(d^2+x)} = e^{t d^2} e^{t x} e^{-t^2 d} e^{-2t^3/3}  (commutatori: [d^2,x]=2d, C2=-d, C3=-2/3)
# applicato a e^{kx} da destra a sinistra:
f = sp.exp(k*x)
f = sp.exp(-sp.Rational(2, 3)*t**3)*f                 # scalare
f = f.subs(x, x - t**2)                               # e^{-t^2 d}: traslazione
f = sp.exp(t*x)*f                                     # moltiplicazione
kk = sp.expand(sp.log(sp.expand_power_exp(f)).diff(x)) if False else (k + t)  # nuovo numero d'onda
f = sp.exp(kk**2*t)*f                                 # e^{t d^2} su e^{(k+t)x}
ok("C4a formula Zassenhaus finita risolve u_t = u_xx + x u", sp.diff(f, t) - sp.diff(f, x, 2) - x*f)
ok("C4b coincide con exp(tx+t^3/3+k^2 t+k(x+t^2))", sp.simplify(sp.log(f) - (t*x + t**3/3 + k**2*t + k*(x + t**2))).expand(force=True))
# commutatori come operatori su funzione test g
g = sp.Function('g')(x)
dd = lambda h: sp.diff(h, x); D2 = lambda h: sp.diff(h, x, 2); M = lambda h: x*h
ok("C4c [d^2,x] = 2d", D2(M(g)) - M(D2(g)) - 2*dd(g))
ok("C4d [x,[d^2,x]] = -2 (scalare) e [d^2,[d^2,x]] = 0", (M(2*dd(g)) - 2*dd(M(g))) + 2*g)

# ---------- C5: Ornstein-Uhlenbeck  A1 = d^2, A2 = -x d  (Wei-Norman, algebra risolubile 2-dim) ----------
ok("C5a [d^2, x d] = 2 d^2", D2(x*dd(g)) - x*dd(D2(g)) - 2*D2(g))
h = (sp.exp(2*t) - 1)/2
uOU = sp.exp(h*(k*sp.exp(-t))**2 + k*sp.exp(-t)*x)    # e^{h d^2} e^{-t x d} e^{kx}
ok("C5b Wei-Norman e^{t(d^2-xd)} = e^{h(t)d^2}e^{-t x d}, h=(e^{2t}-1)/2, risolve OU", sp.diff(uOU, t) - sp.diff(uOU, x, 2) + x*sp.diff(uOU, x))
# Dyson su monomi: H0 = -x d (x^n -> e^{-nt}x^n), V = d^2 (x^n -> n(n-1)x^{n-2})
n = sp.Symbol('n', positive=True, integer=True)
first = n*(n-1)*sp.integrate(sp.exp(-(n-2)*(t-s))*sp.exp(-n*s), (s, 0, t))
exact = n*(n-1)*sp.exp(-n*t)*h
ok("C5c Dyson 1o ordine <x^{n-2}|u(t)> = n(n-1)e^{-(n-2)t}(1-e^{-2t})/2 = esatto", first - exact)
# esatto completo per n=4 e Dyson troncato a ordine 2 (termina: V nilpotente sul grado)
nn = 4
uex = sp.expand(sp.exp(-nn*t)*sum((h**j/sp.factorial(j))*sp.diff(x**nn, x, 2*j) for j in range(3)))
ok("C5d e^{t(d^2-xd)}x^4 risolve OU", sp.diff(uex, t) - sp.diff(uex, x, 2) + x*sp.diff(uex, x))
# E_int additivo per u0=x^4: u - e^{tA1}u0 - e^{tA2}u0 + u0
u1 = sp.expand(sum((t**j/sp.factorial(j))*sp.diff(x**nn, x, 2*j) for j in range(3)))
u2 = sp.exp(-nn*t)*x**nn
Eint = sp.simplify(uex - u1 - u2 + x**nn)
print("     E_int^add (OU, u0=x^4) =", sp.factor(sp.collect(sp.expand(Eint), x)))
# termine bilineare in t^2: deve coincidere con (t^2/2)([A1,A2]+...) -> coefficiente commutatore
ser = sp.series(Eint, t, 0, 3).removeO()
print("     serie in t fino a t^2:", sp.expand(ser))
# confronto con (t^2/2)(A1A2 + A2A1) x^4  (termine misto del 2o ordine di e^{t(A1+A2)})
A1 = lambda q: sp.diff(q, x, 2); A2 = lambda q: -x*sp.diff(q, x)
mixed = sp.expand(t**2/2*(A1(A2(x**4)) + A2(A1(x**4))))
ok("C5e coeff. t^2 di E_int^add = (t^2/2)(A1A2+A2A1)u0", sp.expand(ser) - mixed)

# ---------- C6: sl(2) non risolubile: fattorizzazione solo locale ----------
E = sp.Matrix([[0, 1], [0, 0]]); F = sp.Matrix([[0, 0], [1, 0]]); H = sp.Matrix([[1, 0], [0, -1]])
for name, Mtx, a_ in [("E+F (iperbolico)", E+F, sp.tanh(t)), ("E-F (rotazione)", E-F, sp.tan(t))]:
    lhs = sp.simplify((t*Mtx).exp())
    sgn = 1 if name.startswith("E+F") else -1
    # ansatz e^{aE} e^{bH} e^{cF}: risolto in forma chiusa
    a, b, cc = sp.symbols('a b cc')
    rhs = (a*E).exp()*(b*H).exp()*(cc*F).exp()
    sol = sp.solve([sp.Eq(rhs[1, 1], lhs[1, 1]), sp.Eq(rhs[0, 1]*sp.exp(b), lhs[0, 1]*sp.exp(b))], [a, b, cc], dict=True)
    print(f"     sl2 {name}: e^tM =", lhs.tolist(), "; a(t) atteso =", a_)
    ok(f"C6 {name}: a(t)=M01/M11 = {a_}", sp.simplify(lhs[0, 1]/lhs[1, 1] - a_))

# ---------- C7: Duhamel per l'errore di Lie (matrici generiche 2x2 non commutanti) ----------
A = sp.Matrix([[0, 1], [0, 0]]); B = sp.Matrix([[0, 0], [1, 0]])
lhs = (t*A).exp()*(t*B).exp() - (t*(A+B)).exp()
W = lambda q: (q*A).exp()*(q*B).exp()
integrand = W(s)*((-s*B).exp()*A*(s*B).exp() - A)*((t-s)*(A+B)).exp()
rhs = integrand.applyfunc(lambda e: sp.integrate(sp.simplify(e.rewrite(sp.exp)), (s, 0, t)))
ok("C7 Duhamel: e^{tA}e^{tB}-e^{t(A+B)} = int_0^t e^{sA}e^{sB}(e^{-sB}Ae^{sB}-A)e^{(t-s)(A+B)}ds", sp.simplify((lhs - rhs).applyfunc(lambda e: sp.simplify(e.rewrite(sp.exp)))).norm())

# ---------- C8: G1 su esempio (coeff. costanti) ----------
tau, xi = sp.symbols('tau xi')
P1 = tau - xi**2; P2 = -xi  # L1 = d_t - d_x^2, L2 = -d_x  (L = L1+L2 avvezione-diffusione)
sol = sp.solve([P1 + P2, P1*P2], [tau, xi], dict=True)
print("     C8 V(P1+P2) cap V(P1 P2) =", sol, "(= V(P1,P2): finita)")

# ---------- C9: algebra generata da d^2 e x^3 e' infinito-dimensionale ----------
def comm_op(P, Q, h): return P(Q(h)) - Q(P(h))
X3 = lambda q: x**3*q
c1 = sp.expand(comm_op(X3, D2, g))
print("     [x^3, d^2] g =", c1)
Q = lambda q: x**2*sp.diff(q, x)   # componente x^2 d
ok("C9 [x^k, x^{k-1}d] = -k x^{2k-2} per k=3", sp.expand(comm_op(X3, Q, g) + 3*x**4*g))


