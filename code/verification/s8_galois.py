# S8-VAR — VAR-T2/T6: Airy irriducibile, oscillatore (soluzioni iperesponenziali solo per E = +-(2n+1), uniche),
# d^2 non identificato in C(x)[d] (x e' ucciso da x d - 1), criterio di ordine 2.
import sympy as sp
x, E = sp.symbols('x E')
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")

# Riccati: (d + w)(d - w) = d^2 - w' - w^2
w = sp.Function('w')(x); y = sp.Function('y')(x)
lhs = sp.diff(y, x, 2) - sp.diff(w*y, x)*0  # placeholder
fact = sp.expand(sp.diff(sp.diff(y, x) - w*y, x) + w*(sp.diff(y, x) - w*y))
report("(d+w)(d-w) y = y'' - (w'+w^2) y", sp.simplify(fact - (sp.diff(y, x, 2) - (sp.diff(w, x) + w**2)*y)) == 0)

# Airy: nessuna w razionale con w' + w^2 = x. Test di grado: parte polinomiale di grado m>=1 da' x^{2m}; m=0 limitata.
# Verifica esaustiva su un'ansatz w = p/q, deg p, deg q <= 3 (complemento al ragionamento sui poli nel PROOF_PACKAGE).
cs = sp.symbols('c0:4'); ds = sp.symbols('d0:3')
p = sum(cs[i]*x**i for i in range(4)); q = 1 + sum(ds[i]*x**(i+1) for i in range(3))
num = sp.expand(sp.diff(p, x)*q - p*sp.diff(q, x) + p**2 - x*q**2)
sol = sp.solve(sp.Poly(num, x).coeffs(), list(cs) + list(ds), dict=True)
report("Airy: nessuna soluzione razionale (ansatz deg <= 3)", len(sol) == 0, f"soluzioni trovate: {len(sol)}")

# Oscillatore: y = P e^{-x^2/2} => P'' - 2xP' + (E-1)P = 0 ; y = P e^{x^2/2} => P'' + 2xP' + (1+E)P = 0
P = sp.Function('P')(x)
y1 = P*sp.exp(-x**2/2)
e1 = sp.simplify((sp.diff(y1, x, 2) - (x**2 - E)*y1)*sp.exp(x**2/2))
report("oscillatore, ramo e^{-x^2/2}: equazione di Hermite", sp.simplify(e1 - (sp.diff(P, x, 2) - 2*x*sp.diff(P, x) + (E - 1)*P)) == 0)
y2 = P*sp.exp(x**2/2)
e2 = sp.simplify((sp.diff(y2, x, 2) - (x**2 - E)*y2)*sp.exp(-x**2/2))
report("oscillatore, ramo e^{+x^2/2}", sp.simplify(e2 - (sp.diff(P, x, 2) + 2*x*sp.diff(P, x) + (1 + E)*P)) == 0)
# unicita' della soluzione polinomiale di grado n per E = 2n+1 (ricorrenza dei coefficienti)
okU = True
for n in range(6):
    N = n + 4
    a = sp.symbols(f'a0:{N+1}')
    Pp = sum(a[i]*x**i for i in range(N+1))
    eq = sp.expand(sp.diff(Pp, x, 2) - 2*x*sp.diff(Pp, x) + 2*n*Pp)
    s = sp.solve(sp.Poly(eq, x).coeffs(), a, dict=True)
    # spazio delle soluzioni polinomiali di grado <= N: dimensione 1, generato da H_n
    free = set().union(*[set(v.free_symbols) for v in s[0].values()]) | (set(a) - set(s[0].keys()))
    okU &= len(free) == 1
    Hn = sp.hermite(n, x)
    okU &= sp.simplify(sp.diff(Hn, x, 2) - 2*x*sp.diff(Hn, x) + 2*n*Hn) == 0
report("oscillatore E=2n+1: soluzioni polinomiali = C*H_n (n=0..5)", okU)
# ramo e^{+x^2/2} per E = 2n+1 > 0: grado m richiede 2m+1+E = 0, impossibile
report("ramo e^{+x^2/2} impossibile per E = 2n+1 > 0", all((2*m + 1 + (2*n + 1)) != 0 for m in range(10) for n in range(10)))
# d^2 in C(x)[d]: ogni soluzione a + b x e' iperesponenziale; (x d - 1) x = 0
aa, bb = sp.symbols('a b')
report("d^2: (a+bx) d - b uccide a + b x (ordine 1)", sp.simplify((aa + bb*x)*sp.diff(aa + bb*x, x) - bb*(aa + bb*x)) == 0)
# ordine 2: u identifica L <=> u'/u non razionale. Airy Ai: Ai'/Ai non razionale (coerente con irriducibilita').
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
