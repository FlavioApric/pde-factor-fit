"""S10-INT, EX10-a: Dirac libero 1+1, m = 1 != 0 (verifica V-ex, non una prova).
Convenzione (ALGORITMO_ESTESO 9.1): i psi_t = H psi, H = -i sigma_x d_x + m sigma_z.
Classe hamiltoniana K_H: i psi_t = A psi_x + B psi, A, B in Mat_2(C), 8 incognite.
Dato EP: somma di onde piane psi_j = v_j exp(i(k_j x - w_j t)), w_j = +-sqrt(k_j^2 + m^2).
Per l'indipendenza lineare degli esponenziali distinti su ogni aperto, il sistema
puntuale su Omega equivale al sistema modo per modo (i k A + B) v = w v (2 equazioni per modo).
"""
import sympy as sp
import mpmath as mp

t, x = sp.symbols('t x', real=True)
m = sp.Integer(1)
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
ok = []

def Hop(v):
    return -sp.I * sx * sp.diff(v, x) + m * sz * v

# modi con w razionale (terne pitagoriche): k^2 + 1 = w^2
R = sp.Rational
modes = [(R(3, 4), +1), (R(4, 3), -1), (R(5, 12), +1), (R(12, 5), -1)]
def mode(k, sgn):
    w = sgn * sp.sqrt(k**2 + m**2)
    Hk = sx * k + m * sz                      # H e^{ikx} v = Hk v e^{ikx}
    v = (Hk - w * I2).nullspace()[0]
    v = sp.simplify(v / v[0]) if v[0] != 0 else v
    return k, w, v, v * sp.exp(sp.I * (k * x - w * t))

M = [mode(k, s) for k, s in modes]
ok.append(('(0) ogni onda piana risolve Dirac',
           all(sp.simplify(sp.I * sp.diff(p, t) - Hop(p)) == sp.zeros(2, 1) for _, _, _, p in M)))
ok.append(('(0) w razionali (dato EP esatto)', all(w.is_rational for _, w, _, _ in M)))

a = sp.symbols('a0:4'); b = sp.symbols('b0:4')
A = sp.Matrix(2, 2, a); B = sp.Matrix(2, 2, b)
unk = list(a) + list(b)
def rows(k, w, v):
    eqs = (sp.I * k * A + B) * v - w * v
    return sp.Matrix([[sp.diff(e, u) for u in unk] for e in eqs]), sp.Matrix([-e.subs({u: 0 for u in unk}) for e in eqs])

def system(sel):
    Ms, rs = zip(*[rows(k, w, v) for (k, w, v, _) in sel])
    return sp.Matrix.vstack(*Ms), sp.Matrix.vstack(*rs)

ranks = []
for nmod in (1, 2, 3, 4):
    Mat, rhs = system(M[:nmod])
    ranks.append(Mat.rank())
print('    rango del sistema con 1, 2, 3, 4 modi:', ranks)
ok.append(('(1) un solo modo: rango 2 su 8 (ID-ker fallisce, dim ker = 6)', ranks[0] == 2))
ok.append(('(1) rango 2n per n = 1..4 modi generici', ranks == [2, 4, 6, 8]))
Mat, rhs = system(M)
sol = Mat.gauss_jordan_solve(rhs)
params = sol[1]
true = sp.Matrix([0, -sp.I, -sp.I, 0, 1, 0, 0, -1])     # A = -i sigma_x, B = m sigma_z
ok.append(('(2) 4 modi: soluzione unica (nessun parametro libero)', params.shape[0] == 0))
ok.append(('(2) la soluzione unica e\' (A, B) = (-i sigma_x, m sigma_z): vale (H-ex)',
           sp.simplify(sol[0] - true) == sp.zeros(8, 1)))

# non generico: due modi allo stesso k (rami +-): rango 4
k0 = R(3, 4)
Mng = [mode(k0, +1), mode(k0, -1)]
Mat2, _ = system(Mng)
ok.append(('(3) stesso k, entrambi i rami: rango 4 < 8', Mat2.rank() == 4))

# controllo puntuale numerico (come S9-ALG): dato = somma dei 4 modi, righe in 6 punti
psi = sum((p for _, _, _, p in M), sp.zeros(2, 1))
psi1 = M[0][3]
pts = [(0.3, 0.7), (1.1, -1.2), (1.7, 0.4), (2.0, 2.5), (0.6, -0.4), (2.6, 1.9)]
mp.mp.dps = 30
def pointwise(ps):
    out = []
    for t0, x0 in pts:
        eqs = sp.I * sp.diff(ps, t) - A * sp.diff(ps, x) - B * ps
        eqs = [e.subs({t: sp.Rational(str(t0)), x: sp.Rational(str(x0))}) for e in eqs]
        for e in eqs:
            row = []
            for u in unk:
                c = sp.N(sp.diff(e, u), 35)
                row.append(mp.mpc(str(sp.re(c)), str(sp.im(c))))
            out.append(row)
    return mp.matrix(out)
sv4 = sorted(float(abs(s)) for s in mp.svd_c(pointwise(psi), compute_uv=False))
sv1 = sorted(float(abs(s)) for s in mp.svd_c(pointwise(psi1), compute_uv=False))
print('    valori singolari puntuali, 4 modi:', ['%.2e' % s for s in sv4])
print('    valori singolari puntuali, 1 modo :', ['%.2e' % s for s in sv1])
ok.append(('(4) puntuale, 4 modi: sigma_min > 1e-3 (rango 8)', sv4[0] > 1e-3))
ok.append(('(4) puntuale, 1 modo: 6 valori singolari < 1e-20 (rango 2)', sum(s < 1e-20 for s in sv1) == 6))

# H-DIRAC-ann non vale per dati EP: operatore estraneo in Ann(psi)
dx = lambda f: sp.diff(f, x)
def extr(f):
    g = f
    for k, _, _, _ in M:
        g = dx(g) - sp.I * k * g
    return g
ok.append(('(5) prod_j (d_x - i k_j) I annulla il dato EP a 4 modi', sp.simplify(extr(psi)) == sp.zeros(2, 1)))
kz, wz, vz, pz = mode(sp.Integer(0), +1)
ok.append(('(5) ... ma non annulla l\'onda piana k = 0 (che risolve Dirac): non sta in U_P',
           sp.simplify(extr(pz)) != sp.zeros(2, 1)))

# passo 6: il simbolo KG e\' irriducibile su Q(i): nessuna scomposizione per fattori
tau, xi = sp.symbols('tau xi')
fl = sp.factor_list(tau**2 - xi**2 + m**2, extension=sp.I)
ok.append(('(6) tau^2 - xi^2 + m^2 irriducibile su Q(i)', len(fl[1]) == 1 and fl[1][0][1] == 1))
Hs = -sp.I * sx * xi + m * sz
ok.append(('(6) (i tau - H)(i tau + H) = -(tau^2 - xi^2 + m^2) I',
           sp.simplify((sp.I * tau * I2 - Hs) * (sp.I * tau * I2 + Hs) + (tau**2 - xi**2 + m**2) * I2) == sp.zeros(2)))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
