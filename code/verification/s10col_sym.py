# S10-COL: controlli simbolici delle identita' usate nella prova.
import sympy as sp

ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(f"[{'OK' if cond else 'FAIL'}] {name}")

# (S1) normale esterna del sopragrafico {y_n > g(y')} (n = 3 per concretezza):
#      nu = (grad g, -1)/sqrt(1+|grad g|^2); W.(-nu) * sqrt(1+|grad g|^2) = W_n - W'.grad g
g1, g2, W1, W2, W3 = sp.symbols('g1 g2 W1 W2 W3', real=True)
s = sp.sqrt(1 + g1**2 + g2**2)
nu = sp.Matrix([g1, g2, -1]) / s
W = sp.Matrix([W1, W2, W3])
chk("(S1) W.(-nu)*sqrt(1+|Dg|^2) = W_n - W'.Dg", sp.simplify((-W.dot(nu)) * s - (W3 - W1*g1 - W2*g2)) == 0)
chk("(S1b) |nu| = 1", sp.simplify(nu.dot(nu) - 1) == 0)
# nu e' ortogonale ai vettori tangenti (1,0,g1), (0,1,g2)
chk("(S1c) nu ortogonale al piano tangente",
    sp.simplify(nu.dot(sp.Matrix([1, 0, g1]))) == 0 and sp.simplify(nu.dot(sp.Matrix([0, 1, g2]))) == 0)

# (S2) Cauchy-Schwarz: |a| + L|b| <= sqrt(1+L^2) sqrt(a^2+b^2)  (a = q_n, b = |q'|)
a, b, L = sp.symbols('a b L', nonnegative=True)
expr = (1 + L**2) * (a**2 + b**2) - (a + L*b)**2
chk("(S2) (1+L^2)(a^2+b^2) - (a+Lb)^2 = (La-b)^2", sp.expand(expr - (L*a - b)**2) == 0)

# (S3) |(w - W(q)).(-Dg, 1)| <= |w - W(q)| sqrt(1+|Dg|^2): Cauchy-Schwarz (Lagrange)
d1, d2, d3 = sp.symbols('d1 d2 d3', real=True)
lhs = (d1**2 + d2**2 + d3**2) * (g1**2 + g2**2 + 1) - (-d1*g1 - d2*g2 + d3)**2
lag = (d1*g2 - d2*g1)**2 + (d1*1 + d3*g1)**2 + (d2*1 + d3*g2)**2
chk("(S3) identita' di Lagrange per Cauchy-Schwarz", sp.expand(lhs - lag) == 0)

# (S4) passo della scomposizione u = u1 + u2 nel Lemma 1 (somma nel cono)
w1, w2, u = sp.symbols('w1 w2 u', real=True)
u1 = w1 + (u - w1 - w2) / 2; u2 = w2 + (u - w1 - w2) / 2
chk("(S4) u1 + u2 = u, u1 - w1 = u2 - w2 = (u - w1 - w2)/2",
    sp.simplify(u1 + u2 - u) == 0 and sp.simplify(u1 - w1 - (u - w1 - w2)/2) == 0)

print("ESITO:", "TUTTO OK" if ok else "FALLIMENTI")
