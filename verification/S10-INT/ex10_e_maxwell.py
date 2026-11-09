"""S10-INT, EX10-e: Maxwell nel vuoto (c = 1) come sistema 8x6 in psi = (E, B), R = C[tau, xi1, xi2, xi3].
Righe: tau E - xi x B, tau B + xi x E, xi.E, xi.B. Verifica V-ex, non una prova.
(1) sizigie, rango 6, minore tau^2 (tau^2 - |xi|^2)^2, onda in U_P.
(2) elicita' (Riemann-Silberstein): V P T = diag(P_F, P_G) con V, T costanti invertibili;
    U_1 + U_2 = R^{1x6} => N = 0 => Ext^1(N, A) = 0 su ogni Omega; U_1 cap U_2 = U_P.
(3) classe hamiltoniana d_t psi = sum_j A_j d_j psi + B psi (144 incognite), dato EP di onde piane:
    rango 132 = 144 - 12; il nucleo e' l'ambiguita' dei vincoli (w (x) div E, w' (x) div B).
(4) classe simmetrica (A_j = A_j^T, 63 + 36 = 99 incognite): rango 99, soluzione unica = Maxwell.
(5) dato EP: un operatore estraneo in Ann(psi) => mai ID-ann (come P4-T2).
Per l'indipendenza degli esponenziali distinti il sistema puntuale equivale a quello modo per modo.
"""
import sympy as sp
from sympy.polys.matrices import DomainMatrix

tau, x1, x2, x3 = sp.symbols('tau xi1 xi2 xi3')
xi = sp.Matrix([x1, x2, x3])
ok = []
def cross_mat(v):
    return sp.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
C = cross_mat(xi)                      # C w = xi x w
Z3 = sp.zeros(3); I3 = sp.eye(3)
P = sp.Matrix.vstack(sp.Matrix.hstack(tau * I3, -C),
                     sp.Matrix.hstack(C, tau * I3),
                     sp.Matrix.hstack(xi.T, sp.zeros(1, 3)),
                     sp.Matrix.hstack(sp.zeros(1, 3), xi.T))
# (1)
S1 = sp.Matrix.hstack(xi.T, sp.zeros(1, 3), sp.Matrix([[-tau]]), sp.Matrix([[0]]))
S2 = sp.Matrix.hstack(sp.zeros(1, 3), xi.T, sp.Matrix([[0]]), sp.Matrix([[-tau]]))
ok.append(('(1) sizigie S1 P = 0, S2 P = 0', sp.expand(S1 * P) == sp.zeros(1, 6) and sp.expand(S2 * P) == sp.zeros(1, 6)))
n2 = x1**2 + x2**2 + x3**2
ok.append(('(1) minore 6x6 = tau^2 (tau^2 - |xi|^2)^2: rango 6', sp.factor(P[:6, :].det() - tau**2 * (tau**2 - n2)**2) == 0))
box = tau**2 - n2
# box * e_E1 = tau*(riga E1) + (xi x riga B)_1 - xi1*(div E)
rowE = P[0:3, :]; rowB = P[3:6, :]; dE = P[6, :]
comb = tau * rowE + C * rowB - xi * dE
ok.append(('(1) box I_3 sulle E: tau(E-righe) + xi x (B-righe) - xi (div E) = box [I 0]',
           sp.expand(comb - sp.Matrix.hstack(box * I3, Z3)) == sp.zeros(3, 6)))
# (2) elicita'
Tm = sp.Matrix.vstack(sp.Matrix.hstack(I3 / 2, I3 / 2), sp.Matrix.hstack(I3 / (2 * sp.I), -I3 / (2 * sp.I)))  # (F,G) -> (E,B)
V = sp.zeros(8, 8)
V[0:3, 0:3] = I3; V[0:3, 3:6] = sp.I * I3            # E-righe + i B-righe
V[3:6, 0:3] = I3; V[3:6, 3:6] = -sp.I * I3           # E-righe - i B-righe
V[6, 6] = 1; V[6, 7] = sp.I; V[7, 6] = 1; V[7, 7] = -sp.I
VPT = sp.expand(V * P * Tm)
PF = sp.Matrix.vstack(tau * I3 + sp.I * C, xi.T)
PG = sp.Matrix.vstack(tau * I3 - sp.I * C, xi.T)
target = sp.zeros(8, 6)
target[0:3, 0:3] = PF[0:3, :]; target[3:6, 3:6] = PG[0:3, :]
target[6, 0:3] = xi.T; target[7, 3:6] = xi.T
ok.append(('(2) V, T costanti invertibili', V.det() != 0 and Tm.det() != 0))
ok.append(('(2) V P T = diag(P_F, P_G): F = E + iB, G = E - iB', sp.expand(VPT - target) == sp.zeros(8, 6)))
Kc = sp.Matrix.vstack(sp.Matrix.hstack(I3, -sp.I * I3), sp.Matrix.hstack(I3, sp.I * I3))
ok.append(('(2) righe costanti (I, -iI) e (I, iI): rango 6 => U_1 + U_2 = R^{1x6}, N = 0, Ext^1 = 0', Kc.rank() == 6))
# varieta' caratteristiche di P_F e P_G: entrambe il cono (stessa varieta', eppure N = 0)
ok.append(('(2) det(tau I + i C) = tau (tau^2 - |xi|^2) = det(tau I - i C): stessa varieta\'',
           sp.factor((tau * I3 + sp.I * C).det() - tau * box) == 0 and sp.factor((tau * I3 - sp.I * C).det() - tau * box) == 0))

# (3)-(4) onde piane, terne pitagoriche (|k| razionale)
R = sp.Rational
kv = [(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 3, 6), (3, 6, 2), (6, 2, 3), (1, 4, 8), (4, 8, 1),
      (8, 1, 4), (4, 4, 7), (-1, 2, 2), (2, -3, 6)]
modes = []
for kk in kv:
    k = sp.Matrix(kk); kn = sp.sqrt(k.dot(k))
    assert kn.is_rational
    pols = []
    for v in (sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])):
        E0 = k.cross(v)
        if E0 != sp.zeros(3, 1) and (not pols or sp.Matrix.hstack(*(pols + [E0])).rank() > len(pols)):
            pols.append(E0)
        if len(pols) == 2:
            break
    for w in (kn, -kn):
        for E0 in pols:
            B0 = k.cross(E0) / w
            modes.append((k, w, sp.Matrix.vstack(E0, B0)))
# ogni modo risolve Maxwell: con d_t -> -i w, d_j -> i k_j
Pk = lambda k, w: P.subs({tau: -sp.I * w, x1: sp.I * k[0], x2: sp.I * k[1], x3: sp.I * k[2]})
ok.append(('(3) %d onde piane, tutte soluzioni di Maxwell (vincoli inclusi)' % len(modes),
           all(sp.expand(Pk(k, w) * a) == sp.zeros(8, 1) for k, w, a in modes)))

from sympy.polys.domains import QQ_I
def g(v):
    return QQ_I.from_sympy(sp.nsimplify(v))
# indici: generale A_j[r,c] -> j*36 + r*6 + c, B[r,c] -> 108 + r*6 + c
def build_general():
    rows, rhs = [], []
    for k, w, a in modes:
        for r in range(6):
            row = [QQ_I.zero] * 144
            for j in range(3):
                for c in range(6):
                    row[j * 36 + r * 6 + c] = g(sp.I * k[j] * a[c])
            for c in range(6):
                row[108 + r * 6 + c] = g(a[c])
            rows.append(row); rhs.append([g(-sp.I * w * a[r])])
    return DomainMatrix(rows, (len(rows), 144), QQ_I), DomainMatrix(rhs, (len(rhs), 1), QQ_I)
Mg, bg = build_general()
rank_g = Mg.rank()
print('    classe generale: equazioni', Mg.shape[0], ', incognite 144, rango', rank_g, flush=True)
ok.append(('(3) classe generale: rango 132 = 144 - 12 (ID-ker fallisce per ogni dato di Maxwell)', rank_g == 132))
kcols = []
for w_idx in range(6):
    for blk in (0, 3):
        col = [QQ_I.zero] * 144
        for j in range(3):
            col[j * 36 + w_idx * 6 + blk + j] = QQ_I.one
        kcols.append(col)
K = DomainMatrix([list(r) for r in zip(*kcols)], (144, 12), QQ_I)
ok.append(('(3) le 12 direzioni di vincolo stanno nel nucleo e sono indipendenti',
           (Mg * K).is_zero_matrix and K.rank() == 12))
def true_A(j):
    ej = sp.zeros(3, 1); ej[j] = 1
    Lj = cross_mat(ej)                 # (curl B) = sum_j L_j d_j B
    return sp.Matrix.vstack(sp.Matrix.hstack(Z3, Lj), sp.Matrix.hstack(-Lj, Z3))
At = [true_A(j) for j in range(3)]
ok.append(('(3) gli A_j veri sono simmetrici', all(a == a.T for a in At)))
tv = [g(At[j][r, c]) for j in range(3) for r in range(6) for c in range(6)] + [QQ_I.zero] * 36
TV = DomainMatrix([[v] for v in tv], (144, 1), QQ_I)
ok.append(('(3) (H-ex): la legge vera risolve il sistema', (Mg * TV - bg).is_zero_matrix))
# (4) classe simmetrica: S_j[r,c], r <= c (21 per j), poi B
sidx = {}
for j in range(3):
    for r in range(6):
        for c in range(r, 6):
            sidx[(j, r, c)] = len(sidx)
NS = len(sidx) + 36
def build_sym():
    rows, rhs = [], []
    for k, w, a in modes:
        for r in range(6):
            row = [QQ_I.zero] * NS
            for j in range(3):
                for c in range(6):
                    key = (j, min(r, c), max(r, c))
                    row[sidx[key]] += g(sp.I * k[j] * a[c])
            for c in range(6):
                row[len(sidx) + r * 6 + c] = g(a[c])
            rows.append(row); rhs.append([g(-sp.I * w * a[r])])
    return DomainMatrix(rows, (len(rows), NS), QQ_I), DomainMatrix(rhs, (len(rhs), 1), QQ_I)
Ms, bs = build_sym()
rank_s = Ms.rank()
print('    classe simmetrica: incognite', NS, ', rango', rank_s, flush=True)
ok.append(('(4) classe simmetrica: rango 99 = numero di incognite (ID-ker)', rank_s == NS == 99))
aug = Ms.hstack(bs)
ok.append(('(4) sistema compatibile (rango aumentato = 99)', aug.rank() == 99))
tvs = [QQ_I.zero] * NS
for (j, r, c), i in sidx.items():
    tvs[i] = g(At[j][r, c])
TVS = DomainMatrix([[v] for v in tvs], (NS, 1), QQ_I)
ok.append(('(4) soluzione unica = Maxwell (A_j veri, B = 0)', (Ms * TVS - bs).is_zero_matrix))
# (5) operatore estraneo r = prod_{k1 distinti}(d_1 - i k1) e_{E_1}: sul modo e^{i k.x} vale prod (i k_1 - i k1')
k1vals = sorted(set(k[0] for k, _, _ in modes))
fac = lambda kk1: sp.prod([sp.I * kk1 - sp.I * v for v in k1vals])
ok.append(('(5) r = prod (d_1 - i k_1) e_{E_1} annulla ogni modo del dato EP', all(fac(k[0]) * a[0] == 0 for k, w, a in modes)))
ktest = sp.Matrix([0, 3, 4]); Et = sp.Matrix([5, 0, 0])
at = sp.Matrix.vstack(Et, ktest.cross(Et) / 5)
ok.append(('(5) ... ma non un\'onda piana di Maxwell con k = (0,3,4), E_1 = 5: r non sta in U_P',
           sp.expand(Pk(ktest, 5) * at) == sp.zeros(8, 1) and fac(0) * at[0] != 0))

ok = [(n_, bool(v_)) for n_, v_ in ok]
for name, val in ok:
    print('PASS' if val else 'FAIL', name)
print('%d/%d PASS' % (sum(v for _, v in ok), len(ok)))
