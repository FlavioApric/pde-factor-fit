"""R4 - verifiche simboliche (controllo, non metodo).
Esegui: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I r4_checks.py
"""
import sympy as sp

x, t, z, tau, xi = sp.symbols('x t z tau xi')
D = lambda f, k=1: sp.diff(f, x, k)

def ok(name, cond):
    print(f"[{'OK' if cond else 'FAIL'}] {name}")

# ---------- C1: Prony/Hankel sul jet in UN punto (L0) ----------
u = (1 + x)*sp.exp(2*x) + 3*sp.exp(-x)
N = 8
s = [sp.simplify(D(u, k).subs(x, 0)) for k in range(N)]
H = sp.Matrix(4, 4, lambda i, j: s[i+j])
ok("C1a rank Hankel 4x4 del jet in 0 = 3 = deg p_u", H.rank() == 3)
H3 = sp.Matrix(3, 4, lambda i, j: s[i+j])
ns = H3.nullspace()
ok("C1b nucleo Hankel 3x4 di dim 1", len(ns) == 1)
c = ns[0] / ns[0][3]
p = sp.Poly(sum(c[k]*z**k for k in range(4)), z)
ok("C1c polinomio di Prony = (z-2)^2 (z+1)", sp.expand(p.as_expr() - (z-2)**2*(z+1)) == 0)
Lu = sum(c[k]*D(u, k) for k in range(4))
ok("C1d p_u(D) u = 0", sp.simplify(Lu) == 0)

# ---------- C2: Gram del jet su [0,1], dizionario D^0..D^4 ----------
Phi = [D(u, k) for k in range(5)]
G = sp.Matrix(5, 5, lambda i, j: sp.integrate(sp.expand(Phi[i]*Phi[j]), (x, 0, 1)))
r = G.rank(simplify=True)
ok(f"C2 rank Gram = 3, dim ker = 5-3 = 2 (n=4, d=3) -> non identificabile (rank={r})", r == 3)

# ---------- C3: risolvente / Laplace (P4.2) ----------
Lap = sp.laplace_transform(u, x, z, noconds=True)
num, den = sp.fraction(sp.factor(sp.together(Lap)))
ok("C3 denominatore ridotto di Laplace(u) = p_u(z)",
   sp.simplify(sp.Poly(den, z).monic().as_expr() - sp.expand((z-2)**2*(z+1))) == 0)

# ---------- C4: sparsita' NON implica identificabilita' (messaggio a R1) ----------
v = sp.exp(x)
ok("C4 D^k - 1 annulla e^x per k=1..6 (infiniti annullatori 2-sparsi)",
   all(sp.simplify(D(v, k) - v) == 0 for k in range(1, 7)))

# ---------- C5: L2 evoluzione su T, a(d_x)=d_x^2 + d_x^3 (coeff. reali) ----------
def a_sym(poly, kappa):  # simbolo valutato in i*kappa
    return poly.subs(xi, sp.I*kappa)
a = xi**2 + xi**3
S = [1, -1]  # soluzione reale con un solo |kappa|
U = sum(sp.exp(a_sym(a, k)*t + sp.I*k*x) for k in S)
a2 = a + (xi**2 + 1)*(5*xi - 7)   # stesso valore in xi = +-i, grado 3, coeff. reali
def apply_evol(poly, f):
    pl = sp.Poly(poly, xi)
    return sp.diff(f, t) - sum(cf*sp.diff(f, x, m[0]) for m, cf in zip(pl.monoms(), pl.coeffs()))
ok("C5a |S u -S|=2 < n+1=4: due operatori reali di grado 3 diversi annullano U",
   sp.simplify(apply_evol(a, U)) == 0 and sp.simplify(apply_evol(a2, U)) == 0)
S2 = [1, -1, 2, -2]
U2 = sum(sp.exp(a_sym(a, k)*t + sp.I*k*x) for k in S2)
ok("C5b con |S u -S|=4 = n+1 l'operatore a2 NON annulla piu' U2",
   sp.simplify(apply_evol(a2, U2)) != 0)
# unicita' via interpolazione: sistema lineare per coeff. di grado <=3
cs = sp.symbols('c0:4')
gen = sum(cs[k]*xi**k for k in range(4))
eqs = [sp.expand(gen.subs(xi, sp.I*k) - a_sym(a, k)) for k in S2]
sol = sp.solve(eqs, cs, dict=True)
ok("C5c interpolazione su {±1,±2} restituisce a unicamente", len(sol) == 1 and sp.expand(gen.subs(sol[0]) - a) == 0)

# ---------- C6: L3, calore con 2 modi reali risolve anche u_tt+5u_t+4u=0 ----------
W = sp.exp(-t)*sp.cos(x) + sp.exp(-4*t)*sp.cos(2*x)
heat = sp.diff(W, t) - sp.diff(W, x, 2)
osc = sp.diff(W, t, 2) + 5*sp.diff(W, t) + 4*W
ok("C6a W risolve il calore", sp.simplify(heat) == 0)
ok("C6b W risolve anche u_tt + 5u_t + 4u = 0 (Z finito => Ann(u) 0-dimensionale)", sp.simplify(osc) == 0)
# complesso: e^{-t+ix}+e^{-4t+2ix} risolve u_t = 3i u_x + 2u (ordine 1!)
Wc = sp.exp(-t + sp.I*x) + sp.exp(-4*t + 2*sp.I*x)
ok("C6c modo complesso: u_t = 3i u_x + 2u", sp.simplify(sp.diff(Wc, t) - 3*sp.I*sp.diff(Wc, x) - 2*Wc) == 0)

# ---------- C7: Weyl algebra, u = exp(x^2) ----------
w = sp.exp(x**2)
L1 = lambda f: D(f) - 2*x*f
ok("C7a (D-2x) w = 0", sp.simplify(L1(w)) == 0)
ok("C7b x(D-2x) w = 0 (moltiplo sinistro polinomiale: stessa classe, grado maggiore)", sp.simplify(x*L1(w)) == 0)
ok("C7c (D^2 - 4x^2 - 2) w = 0 (ordine 2, moltiplo sinistro (D+2x)(D-2x))",
   sp.simplify(D(w, 2) - (4*x**2 + 2)*w) == 0)
# coefficienti C^infinito: u D - u' annulla qualsiasi u
g = sp.Function('g')(x)
ok("C7d g D - g' annulla qualsiasi g (non-identificabilita' strutturale a coeff. liberi)",
   sp.simplify(g*D(g) - D(g)*g) == 0)
