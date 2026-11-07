# S10-OPEN-A, P1-Q7: controlli per il teorema di dilatazione (solo verifica).
import sympy as sp

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name)

s, e0 = sp.symbols('s epsilon0', nonzero=True)
# (1) Hankel dei momenti m_k = e0 s^{k+1}/(k+1): det = e0^n s^{n^2} det Hilb_n != 0
for n in range(1, 8):
    H = sp.Matrix(n, n, lambda i, j: e0*s**(i+j+1)/(i+j+1))
    Hilb = sp.Matrix(n, n, lambda i, j: sp.Rational(1, i+j+1))
    chk(f"Hankel n={n}: det = e0^n s^(n^2) det Hilb_n, det Hilb_n != 0",
        sp.simplify(H.det() - e0**n*s**(n*n)*Hilb.det()) == 0 and Hilb.det() != 0)
# (2) somme di p esponenziali formali: Hankel (p+1)x(p+1) identicamente nullo
for p in (1, 2, 3):
    q = sp.symbols(f'q0:{p}'); tau = sp.symbols(f'tau0:{p}')
    m = lambda k: sum(q[i]*tau[i]**k for i in range(p))
    H = sp.Matrix(p+1, p+1, lambda i, j: m(i+j))
    chk(f"rango <= p per p={p} (det Hankel (p+1) = 0)", sp.expand(H.det()) == 0)
# (3) Weyl A_1: sigma(Z) = Delta^{-1} Z Delta, (Delta g)(x) = g(x/mu): x -> mu x, d -> d/mu
x, mu = sp.symbols('x mu', positive=True)
Delta = lambda g: g.subs(x, x/mu)
Deltainv = lambda g: g.subs(x, mu*x)
conj = lambda op: (lambda g: Deltainv(op(Delta(g))))
dop = lambda g: sp.diff(g, x)
xop = lambda g: x*g
test = x**7 + 3*x**4 - x + 2
chk("sigma(d) = d/mu", sp.simplify(conj(dop)(test) - sp.diff(test, x)/mu) == 0)
chk("sigma(x) = mu x", sp.simplify(conj(xop)(test) - mu*x*test) == 0)
for a in (3, 4, 5):
    Xop = lambda g, a=a: x**a*sp.diff(g, x)
    chk(f"sigma(x^{a} d) = mu^{a-1} x^{a} d (alpha = {a-1}, beta = -1)",
        sp.simplify(conj(Xop)(test) - mu**(a-1)*x**a*sp.diff(test, x)) == 0)
# (4) riscalamento t = nu^alpha s: tempo X = nu^{-alpha} g(nu^alpha s), tempo Y = nu^{-beta} g(nu^alpha s), g in t C[[t]]
nu, t = sp.symbols('nu t')
alpha, beta = 2, -1
g = sum(sp.Rational(k+1, k+2)*t**k for k in range(1, 6))
gX = sp.expand(g.subs(t, nu**alpha*s)*nu**(-alpha))
gY = sp.expand(g.subs(t, nu**alpha*s)*nu**(-beta))
chk("tempo X: polinomio in nu", all(mm[0] >= 0 for mm in sp.Poly(gX, nu).monoms()))
chk("tempo Y: polinomio in nu con valutazione >= alpha - beta = 3", min(mm[0] for mm in sp.Poly(gY, nu).monoms()) >= alpha - beta)
# (5) caso alpha = 0 (algebra libera, Y -> mu^{-1} Y): tempo X indipendente da nu, tempo Y = nu g(s)
gX0 = sp.expand(g.subs(t, s)); gY0 = sp.expand(nu*g.subs(t, s))
chk("alpha = 0: tempo Y = nu * g(s)", sp.simplify(gY0 - nu*gX0) == 0)
print(f"{ok}/{tot} OK")
