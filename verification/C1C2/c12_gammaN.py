# Ripresa 3 S-C1C2: controllo del controesempio N=3 (AUDIT_P2 O-1) per C12-P7(c).
# Tre rette in C^3: v1=(1,0,e)/sqrt(1+e^2), v2=(-1/2,sqrt3/2,0), v3=(-1/2,-sqrt3/2,0).
# S: C^3 -> C^3, S(a,b,c)=a v1+b v2+c v3; S*S = Gram G; gamma_3 = lambda_min(G) (S iniettiva per e != 0).
import sympy as sp
e = sp.symbols('e', positive=True)
v1 = sp.Matrix([1, 0, e]) / sp.sqrt(1 + e**2)
v2 = sp.Matrix([-sp.Rational(1, 2), sp.sqrt(3)/2, 0])
v3 = sp.Matrix([-sp.Rational(1, 2), -sp.sqrt(3)/2, 0])
V = [v1, v2, v3]
G = sp.Matrix(3, 3, lambda i, j: (V[i].T * V[j])[0])
ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond); print(("OK  " if cond else "FAIL"), name)
detG = sp.simplify(G.det())
chk("det G = 3e^2/(4(1+e^2))", sp.simplify(detG - 3*e**2/(4*(1 + e**2))) == 0)
pairs = [sp.simplify(sp.Abs((V[i].T*V[j])[0])) for i, j in ((0, 1), (0, 2), (1, 2))]
chk("c_F a coppie: 1/(2 sqrt(1+e^2)), 1/(2 sqrt(1+e^2)), 1/2 (tutte <= 1/2)",
    sp.simplify(pairs[0] - 1/(2*sp.sqrt(1 + e**2))) == 0 and sp.simplify(pairs[2] - sp.Rational(1, 2)) == 0)
lam = sp.symbols('lam')
cp = sp.expand((lam*sp.eye(3) - G).det())
for ev in [sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]:
    roots = sorted([sp.re(r) for r in sp.Poly(cp.subs(e, ev), lam).nroots(n=30)])
    g3 = roots[0]
    chk(f"e={ev}: gamma_3 = {sp.N(g3, 6)} ~ e^2/3 = {sp.N(ev**2/3, 6)}", abs(g3/(ev**2/3) - 1) < 0.05)
chk("traccia G = 3 e per e=0 autovalori {0,3/2,3/2}",
    sp.simplify(G.trace() - 3) == 0 and sorted(G.subs(e, 0).eigenvals().keys()) == [0, sp.Rational(3, 2)])
print(f"ESITO: {ok}/{tot}")
