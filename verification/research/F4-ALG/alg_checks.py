# F4-ALG -- verifiche SymPy (solo controllo, non metodo). Eseguire con:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I alg_checks.py > alg_checks.out
import sympy as sp

t, x = sp.symbols('t x', positive=True)
nu, k, k1, k2 = sp.symbols('nu k k1 k2', positive=True)
results = []

def check(name, expr):
    ok = sp.simplify(expr) == 0
    results.append((name, ok))
    print(f"[{'OK' if ok else 'FAIL'}] {name}")
    return ok

D = lambda f, *v: sp.diff(f, *v)

# C1 nucleo del calore: soluzione del calore, NON EP (∂_x^k G/G polinomio di grado k), ma
#    relazione autonoma con coefficienti costanti nel x-getto: y^2 y_xxx - 3 y y_x y_xx + 2 y_x^3 = 0
G = t**sp.Rational(-1, 2) * sp.exp(-x**2/(4*t))
check("C1a heat kernel solves u_t = u_xx", D(G, t) - D(G, x, 2))
for kk in range(1, 6):
    q = sp.simplify(D(G, x, kk)/G)
    ok = sp.Poly(sp.expand(q), x).degree() == kk
    results.append((f"C1b deg(d_x^{kk}G/G) = {kk}", ok)); print(f"[{'OK' if ok else 'FAIL'}] C1b deg(d_x^{kk}G/G) = {kk}")
check("C1c (log G)_xxx = 0 as polynomial relation in x-jet", G**2*D(G, x, 3) - 3*G*D(G, x)*D(G, x, 2) + 2*D(G, x)**3)

# C2 Cole-Hopf: F_B(-2 nu phi_x/phi) = -2 nu d_x((phi_t - nu phi_xx)/phi), phi generica
phi = sp.Function('phi')(t, x)
u = -2*nu*D(phi, x)/phi
FB = lambda w: D(w, t) + w*D(w, x) - nu*D(w, x, 2)
check("C2 Cole-Hopf identity", FB(u) - (-2*nu*D((D(phi, t) - nu*D(phi, x, 2))/phi, x)))

# C3 Cole-Hopf del nucleo del calore (phi_t = nu phi_xx): u = x/t, risolve Burgers, u_xx = 0
Gn = t**sp.Rational(-1, 2) * sp.exp(-x**2/(4*nu*t))
check("C3a G_nu solves heat", D(Gn, t) - nu*D(Gn, x, 2))
uG = sp.simplify(-2*nu*D(Gn, x)/Gn)
check("C3b u = x/t", uG - x/t)
check("C3c u = x/t solves Burgers", FB(x/t))

# C4 shock: phi = 1 + E, E = exp(k x + nu k^2 t): relazione autonoma di Riccati in x
E = sp.exp(k*x + nu*k**2*t)
us = sp.simplify(-2*nu*D(1 + E, x)/(1 + E))
check("C4a shock solves Burgers", FB(us))
check("C4b Riccati: u_x = u^2/(2 nu) + k u", D(us, x) - (us**2/(2*nu) + k*us))
check("C4c traveling: u_t - nu k u_x = 0 (char. della simmetria in I(u); E costante su x = -nu k t)", D(us, t) - nu*k*D(us, x))

# C5 commutazione [D, D_N] = 0 sull'anello dei polinomi del x-getto (Burgers, KdV)
Y = sp.symbols('y0:12')
def Dx(p):  # derivazione totale in x: y_k -> y_{k+1}
    return sum(sp.diff(p, Y[i])*Y[i+1] for i in range(len(Y)-1))
def DN(p, N, order):  # campo evolutivo: y_k -> D^k N
    tot = 0
    Nk = N
    for i in range(order):
        tot += sp.diff(p, Y[i])*Nk
        Nk = Dx(Nk)
    return tot
for name, N in [("Burgers", -Y[0]*Y[1] + nu*Y[2]), ("KdV", -6*Y[0]*Y[1] - Y[3])]:
    p = Y[0]**2*Y[2] + 3*Y[1]**3 - Y[0]*Y[1]*Y[2]  # polinomio di prova di ordine 2
    lhs = sp.expand(Dx(DN(p, N, 4)))
    rhs = sp.expand(DN(Dx(p), N, 5))
    check(f"C5 [D, D_N] = 0 on test polynomial ({name})", lhs - rhs)

# C6 KdV u_t + 6 u u_x + u_xxx = 0: 1-solitone, relazione stazionaria u_xx + 3u^2 - k^2 u = 0
KdV = lambda w: D(w, t) + 6*w*D(w, x) + D(w, x, 3)
u1 = k**2/2*sp.sech((k*x - k**3*t)/2)**2
check("C6a 1-soliton solves KdV", KdV(u1).rewrite(sp.exp))
check("C6b stationary (Novikov N=1): u_xx + 3u^2 - k^2 u = 0", (D(u1, x, 2) + 3*u1**2 - k**2*u1).rewrite(sp.exp))
check("C6c traveling: u_t + k^2 u_x = 0", (D(u1, t) + k**2*D(u1, x)).rewrite(sp.exp))

# C7 KdV 2-solitone (k1=1, k2=2): u = 2 d_x^2 log tau, tau = 1+E1+E2+A E1E2
K1, K2 = 1, 2
A = sp.Rational((K1-K2)**2, (K1+K2)**2)
E1 = sp.exp(K1*x - K1**3*t); E2 = sp.exp(K2*x - K2**3*t)
tau = 1 + E1 + E2 + A*E1*E2
u2 = 2*D(sp.log(tau), x, 2)
check("C7a 2-soliton solves KdV", sp.together(KdV(u2)))
G1 = D(u2, x, 2) + 3*u2**2
G2 = D(u2, x, 4) + 10*u2*D(u2, x, 2) + 5*D(u2, x)**2 + 10*u2**3
c1, c0 = -(K1**2 + K2**2), K1**2*K2**2
check("C7b Novikov N=2: G2 + c1 G1 + c0 u = 0 with c1=-(k1^2+k2^2), c0=k1^2 k2^2", sp.together(G2 + c1*G1 + c0*u2))
# trdeg: u, u_x, u_xx sono funzioni razionali di (E1, E2): Jacobiano rispetto a (a,b) di rango <= 2
a, b = sp.symbols('a b', positive=True)
taub = 1 + a + b + A*a*b
Dab = lambda f: K1*a*sp.diff(f, a) + K2*b*sp.diff(f, b)   # d_x su Q(a,b)
U0 = sp.together(2*Dab(Dab(sp.log(taub))))
U1 = sp.together(Dab(U0)); U2 = sp.together(Dab(U1))
J = sp.Matrix([[sp.diff(f, v) for v in (a, b)] for f in (U0, U1, U2)])
r = J.subs({a: sp.Rational(3, 7), b: sp.Rational(5, 11)}).rank()
results.append(("C7c rank Jacobian (u,u_x,u_xx)/(E1,E2) = 2 (=> algebraic dependence)", r == 2))
print(f"[{'OK' if r == 2 else 'FAIL'}] C7c rank Jacobian (u,u_x,u_xx)/(E1,E2) = {r} (<= 2 => u,u_x,u_xx alg. dipendenti su C)")

# C8 Miura (segno di KdV u_t+6uu_x+u_xxx): u = -(v^2 + v_x), mKdV M[v] = v_t - 6 v^2 v_x + v_xxx
v = sp.Function('v')(t, x)
uM = -(v**2 + D(v, x))
M = D(v, t) - 6*v**2*D(v, x) + D(v, x, 3)
check("C8 Miura: KdV[-(v^2+v_x)] = -(2v + d_x) mKdV[v]", KdV(uM) - (-(2*v*M + D(M, x))))

# C9 linearita: un'equazione lineare a fattori P = (tau-xi^2)(tau+xi) ha soluzioni u1+u2 (somma):
#    la scomposizione per fattori e' una SOMMA; per F = F1*F2 polinomiale (non lineare) una soluzione
#    analitica su un connesso annulla F1 oppure F2 (unione). Esempio: F = (u_t - u_xx)(u_t + u_x).
w1 = sp.exp(t + x); w2 = (x - t)**3
Pheat = lambda w: D(w, t) - D(w, x, 2); Ptr = lambda w: D(w, t) + D(w, x)
check("C9a linear: (d_t - d_x^2)(d_t + d_x)(w1 + w2) = 0", Pheat(Ptr(w1 + w2)))
ok = sp.simplify(Pheat(w1 + w2)*Ptr(w1 + w2)) != 0
results.append(("C9b nonlinear product F1(u)F2(u) != 0 for u = w1 + w2 (union, not sum)", ok))
print(f"[{'OK' if ok else 'FAIL'}] C9b nonlinear product F1(u)F2(u) != 0 for u = w1 + w2 (union, not sum)")

n_ok = sum(1 for _, o in results if o)
print(f"\nTOTALE: {n_ok}/{len(results)} OK")

