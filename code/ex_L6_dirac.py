"""S9-ALG, esempio L6: Dirac 1+1 libero (verifica V-ex, non una prova).
Convenzione: i psi_t = H psi, H = -i sigma_x d_x + m sigma_z  (alpha = sigma_x, beta = sigma_z).
(a) (i d_t - H)(i d_t + H) = -(d_t^2 - d_x^2 + m^2) I  (ogni componente risolve Klein-Gordon).
(b) psi := (i d_t + H)(f e_1), f = J0(m sqrt(t^2 - x^2)) soluzione KG non EP: psi risolve Dirac.
(c) classe hamiltoniana i psi_t = A psi_x + B psi (A, B incognite 2x2, 8 incognite):
    con psi di (b) il sistema lineare puntuale ha rango 8 (ID-ker, e la legge vera esiste: H-ex);
    con un'onda piana (dato EP) il rango e' 2: nessuna unicita'.
"""
import sympy as sp
import mpmath as mp

t, x = sp.symbols('t x', real=True)
m = sp.Integer(1)
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
ok = []

# (a) prodotto dei simboli (tau = d_t, xi = d_x commutano)
tau, xi = sp.symbols('tau xi')
Hs = -sp.I * sx * xi + m * sz
prod = (sp.I * tau * I2 - Hs) * (sp.I * tau * I2 + Hs)
target = -(tau**2 - xi**2 + m**2) * I2
ok.append(('(a) fattorizzazione Dirac -> KG', sp.simplify(prod - target) == sp.zeros(2)))

# (b) psi da una soluzione KG non EP
s = sp.sqrt(t**2 - x**2)
f = sp.besselj(0, m * s)
def Hop(v):
    return -sp.I * sx * sp.diff(v, x) + m * sz * v
F = sp.Matrix([f, 0])
psi = sp.I * sp.diff(F, t) + Hop(F)
res = sp.I * sp.diff(psi, t) - Hop(psi)
kg = sp.diff(f, t, 2) - sp.diff(f, x, 2) + m**2 * f
mp.mp.dps = 30
pts = [(2.3, 0.7), (3.1, -1.2), (1.7, 0.4), (4.0, 2.5)]
def num(e, a, b):
    return sp.N(e.subs({t: sp.Rational(str(a)), x: sp.Rational(str(b))}), 40)
kg_max = max(sp.Abs(num(kg, a, b)) for a, b in pts)
res_max = max(sp.Abs(num(r, a, b)) for r in res for a, b in pts)
ok.append(('(b) f risolve KG (num., |res| < 1e-20)', kg_max < 1e-20))
ok.append(('(b) psi risolve Dirac (num., |res| < 1e-20)', res_max < 1e-20))
print('    max |KG f| =', kg_max, ' max |Dirac psi| =', res_max)

# (c) rango del sistema per (A, B)
a = sp.symbols('a0:4'); b = sp.symbols('b0:4')
A = sp.Matrix(2, 2, a); B = sp.Matrix(2, 2, b)
unk = list(a) + list(b)
def rows_at(ps, a0, b0):
    eqs = sp.I * sp.diff(ps, t) - A * sp.diff(ps, x) - B * ps
    eqs = [e.subs({t: sp.Rational(str(a0)), x: sp.Rational(str(b0))}) for e in eqs]
    M = sp.Matrix([[sp.diff(e, u) for u in unk] for e in eqs])
    return M
Mbig = sp.Matrix.vstack(*[rows_at(psi, a0, b0) for a0, b0 in pts])
Mnum = mp.matrix([[complex(sp.N(Mbig[i, j], 30)) for j in range(8)] for i in range(Mbig.rows)])
sv = mp.svd_c(Mnum, compute_uv=False)
svl = sorted([float(abs(v)) for v in sv])
print('    valori singolari (dato non EP):', ['%.3e' % v for v in svl])
ok.append(('(c) dato non EP: rango 8 (sigma_min > 1e-6)', svl[0] > 1e-6))
# soluzione vera
true = {a[0]: 0, a[1]: -sp.I, a[2]: -sp.I, a[3]: 0, b[0]: 1, b[1]: 0, b[2]: 0, b[3]: -1}
eqs_true = (sp.I * sp.diff(psi, t) - A * sp.diff(psi, x) - B * psi).subs(true)
chk = max(sp.Abs(num(e, a0, b0)) for e in eqs_true for a0, b0 in pts)
ok.append(('(c) (A,B) = (-i sigma_x, m sigma_z) risolve il sistema', chk < 1e-20))

# onda piana: dato EP
k = sp.Rational(1, 2); om = sp.sqrt(k**2 + m**2)
Hk = sx * k + m * sz          # H e^{ikx} v = (sigma_x k + m sigma_z) v e^{ikx}
v = (Hk - (-om) * I2).columnspace()[0]   # autovettore con autovalore +om
v = sp.simplify(v)
pw = v * sp.exp(sp.I * (k * x - om * t))
ok.append(('(c) onda piana risolve Dirac', sp.simplify(sp.I * sp.diff(pw, t) - Hop(pw)) == sp.zeros(2, 1)))
Mpw = sp.Matrix.vstack(*[rows_at(pw, a0, b0) for a0, b0 in pts])
Mpwn = mp.matrix([[complex(sp.N(Mpw[i, j], 30)) for j in range(8)] for i in range(Mpw.rows)])
svp = sorted([float(abs(v)) for v in mp.svd_c(Mpwn, compute_uv=False)], reverse=True)
rank_pw = sp.simplify(Mpw).rank(simplify=True)
print('    valori singolari (onda piana):', ['%.3e' % v for v in svp])
ok.append(('(c) dato EP (onda piana): rango 2 < 8', rank_pw == 2))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
