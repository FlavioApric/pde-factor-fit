# S-CHECK-EX10 -- controllo indipendente di EX10-e-K (Maxwell, nucleo di Phi_u nella classe hamiltoniana)
# Classe: d_t psi = sum_j A_j d_j psi + B psi, psi = (E, B) in C^6, A_j, B in Mat_6.
# Parte lineare di Phi_u: (A, B) -> sum_j A_j d_j psi + B psi.  Su un'onda piana v e^{i(k.x - w t)}:
# (i sum_j k_j A_j + B) v = 0.  Riparametrizzo A'_j = i A_j: il nucleo e' quello di (sum k_j A'_j + B) v = 0 (rango invariato).
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import itertools

ok = []
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

# quaterne pitagoriche diverse da quelle dello script S10-INT
kv = [(2, 6, 9), (6, 6, 7), (3, 4, 12), (2, 10, 11), (1, 12, 12), (8, 9, 12),
      (12, 4, 3), (9, 2, 6), (6, 9, 2), (7, 4, 4), (-3, 4, 12), (2, -10, 11)]
def norm(k):
    n = sp.sqrt(sum(c*c for c in k)); assert n.is_Integer; return int(n)

def polarizations(k):
    # due vettori razionali indipendenti ortogonali a k
    cand = [cross(k, e) for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1])]
    basis = []
    for c in cand:
        M = sp.Matrix(basis + [c])
        if M.rank() == len(basis) + 1:
            basis.append(c)
        if len(basis) == 2: break
    return basis

def modes(ks, branches=(1, -1)):
    out = []
    for k in ks:
        w0 = norm(k)
        for s in branches:
            w = s * w0
            for E0 in polarizations(k):
                B0 = [sp.Rational(c, w) for c in cross(k, E0)]
                out.append((k, w, [sp.Rational(c) for c in E0] + B0))
    return out

# (0) le onde piane risolvono Maxwell (E_t = curl B, B_t = -curl E, div = 0): simboli -iw E = i k x B, -iw B = -i k x E
good = True
for (k, w, v) in modes(kv):
    E0, B0 = v[:3], v[3:]
    kxB, kxE = cross(k, B0), cross(k, E0)
    good &= all(sp.simplify(-w*E0[i] - kxB[i]) == 0 and sp.simplify(-w*B0[i] + kxE[i]) == 0 for i in range(3))
    good &= sum(k[i]*E0[i] for i in range(3)) == 0 and sum(k[i]*B0[i] for i in range(3)) == 0
ok.append(('(0) 48 onde piane (12 k nuovi x 2 rami x 2 polarizzazioni) risolvono Maxwell con i vincoli', good))

# incognite: A'_j (j=0,1,2) e B, ordinati
def idx_A(j, r, c): return 36*j + 6*r + c
def idx_B(r, c): return 108 + 6*r + c

def system_rows(md, sym=False):
    rows = []
    for (k, w, v) in md:
        for r in range(6):
            row = [QQ(0)] * 144
            for j in range(3):
                for c in range(6):
                    row[idx_A(j, r, c)] += QQ(k[j]) * QQ(v[c].p, v[c].q)
            for c in range(6):
                row[idx_B(r, c)] += QQ(v[c].p, v[c].q)
            rows.append(row)
    return rows

def sym_reduce(rows):
    # A'_j simmetriche: parametri a_{j,r<=c}; B libero
    params = []
    for j in range(3):
        for r in range(6):
            for c in range(r, 6):
                params.append(('A', j, r, c))
    for r in range(6):
        for c in range(6):
            params.append(('B', r, c))
    new = []
    for row in rows:
        nr = []
        for p in params:
            if p[0] == 'A':
                _, j, r, c = p
                val = row[idx_A(j, r, c)] + (row[idx_A(j, c, r)] if r != c else QQ(0))
            else:
                val = row[idx_B(p[1], p[2])]
            nr.append(val)
        new.append(nr)
    return new, params

def rank(rows):
    return DomainMatrix(rows, (len(rows), len(rows[0])), QQ).rank()

md = modes(kv)
R = system_rows(md)
rk = rank(R)
print('    classe generale, 12 k nuovi:', len(R), 'equazioni, 144 incognite, rango', rk)
ok.append(('(1) classe generale: rango 132 (nucleo 12) con 12 k nuovi', rk == 132))

# (2) le 12 direzioni di vincolo stanno nel nucleo per OGNI soluzione (simbolico: sum_j w e_{E_j}^T d_j psi = w div E)
xs = sp.symbols('x1:4')
psi = [sp.Function('p%d' % i)(*xs) for i in range(6)]
w = sp.symbols('w1:7')
allok = True
for blk in (0, 3):
    acc = [0]*6
    for j in range(3):
        for r in range(6):
            acc[r] += w[r] * sp.diff(psi[blk + j], xs[j])
    div = sum(sp.diff(psi[blk + j], xs[j]) for j in range(3))
    allok &= all(sp.expand(acc[r] - w[r]*div) == 0 for r in range(6))
ok.append(('(2) sum_j (w e_{E_j}^T) d_j psi = w div E, idem per B: nucleo >= 12 per ogni dato di Maxwell', allok))

# (2') le 12 direzioni sono indipendenti e generano esattamente il nucleo numerico del punto (1)
dirs = []
for blk in (0, 3):
    for r in range(6):
        vec = [QQ(0)]*144
        for j in range(3):
            vec[idx_A(j, r, blk + j)] = QQ(1)
        dirs.append(vec)
Dm = DomainMatrix(dirs, (12, 144), QQ)
RM = DomainMatrix(R, (len(R), 144), QQ)
ok.append(('(2\') le 12 direzioni: rango 12 e R * dir = 0  =>  ker = span(dir) (dim 12 = 144 - 132)',
           Dm.rank() == 12 and (RM * Dm.transpose()).to_Matrix().is_zero_matrix))

# (3) prova per TUTTI i k: T(k) Pi(k) = 0 come identita' polinomiale, Pi(k) = |k|^2 I - diag(k k^T, k k^T)
k1, k2, k3 = sp.symbols('k1 k2 k3')
K = sp.Matrix([k1, k2, k3])
Aj = [sp.Matrix(6, 6, lambda r, c, j=j: sp.Symbol('a%d_%d_%d' % (j, r, c))) for j in range(3)]
Bm = sp.Matrix(6, 6, lambda r, c: sp.Symbol('b_%d_%d' % (r, c)))
unk = [s for M in Aj + [Bm] for s in M]
T = k1*Aj[0] + k2*Aj[1] + k3*Aj[2] + Bm
kk = K * K.T
Pi = (k1**2 + k2**2 + k3**2) * sp.eye(6) - sp.diag(kk, kk)
TP = (T * Pi).applyfunc(sp.expand)
eqs = []
for e in TP:
    eqs += sp.Poly(e, k1, k2, k3).coeffs()
Ms, _ = sp.linear_eq_to_matrix(eqs, unk)
rk_all = DomainMatrix.from_Matrix(Ms).convert_to(QQ).rank()
print('    identita\' polinomiale per tutti i k: rango', rk_all, 'su 144')
ok.append(('(3) per tutti i k (identita\' polinomiale): nucleo esattamente di dimensione 12', rk_all == 132))

# (3') forma esplicita: B = 0 e A'_j = w1 e_{E_j}^T + w2 e_{B_j}^T (risoluzione simbolica)
sol = sp.solve(eqs, unk, dict=True)[0]
Bsol = Bm.subs(sol)
free = set().union(*[M.subs(sol).free_symbols for M in Aj])
form_ok = Bsol.is_zero_matrix and len(free) == 12
# colonne non nulle di A'_j solo E_j e B_j, e colonna E_j uguale per j = 0,1,2 (stesso w1)
for j in range(3):
    Asj = Aj[j].subs(sol)
    for c in range(6):
        if c not in (j, 3 + j):
            form_ok &= all(Asj[r, c] == 0 for r in range(6))
A0, A1, A2 = [Aj[j].subs(sol) for j in range(3)]
form_ok &= all(sp.simplify(A0[r, 0] - A1[r, 1]) == 0 and sp.simplify(A0[r, 0] - A2[r, 2]) == 0 for r in range(6))
form_ok &= all(sp.simplify(A0[r, 3] - A1[r, 4]) == 0 and sp.simplify(A0[r, 3] - A2[r, 5]) == 0 for r in range(6))
ok.append(('(3\') nucleo per tutti i k: B = 0, A_j = w1 e_{E_j}^T + w2 e_{B_j}^T, 12 parametri liberi', form_ok))

# (4) quanti k servono: rango in funzione del numero di k (24 equazioni indipendenti al piu' per k)
ranks = [rank(system_rows(modes(kv[:n]))) for n in range(1, 8)]
print('    rango con n = 1..7 vettori k:', ranks)
ok.append(('(4) il rango 132 si raggiunge gia\' con 6 k (minimo 132/24 -> 6); con 5 k e\' < 132',
           ranks[5] == 132 and ranks[4] < 132))

# (5) kill sull'ipotesi "entrambi i rami": un solo ramo (w > 0) da' 12 equazioni per k invece di 24.
# Con 12 k il rango e' ancora 132 (l'ipotesi e' sufficiente, non necessaria); con 6 k no.
rk1 = rank(system_rows(modes(kv, branches=(1,))))
rk1_6 = rank(system_rows(modes(kv[:6], branches=(1,))))
print('    un solo ramo: 12 k -> rango', rk1, '; 6 k -> rango', rk1_6)
ok.append(('(5) un solo ramo: rango 132 con 12 k, < 132 con 6 k (i due rami servono all\'argomento, non al risultato)',
           rk1 == 132 and rk1_6 < 132))

# (6) classe simmetrica: nucleo 0 per i dati generici e per tutti i k
Rs, params = sym_reduce(R)
rks = rank(Rs)
print('    classe simmetrica, 12 k nuovi: incognite', len(params), ', rango', rks)
ok.append(('(6) classe simmetrica (99 incognite): rango 99, nucleo 0', len(params) == 99 and rks == 99))

# (6') la legge vera e' nella classe simmetrica e risolve il sistema affine (unicita' da (6))
eps = sp.LeviCivita
Atrue = []
for j in range(3):
    L = sp.Matrix(3, 3, lambda i, kk_: eps(i, j, kk_))
    Atrue.append(sp.Matrix(sp.BlockMatrix([[sp.zeros(3), L], [-L, sp.zeros(3)]])))
symm = all(M == M.T for M in Atrue)
aff = True
for (k, wv, v) in md:
    vv = sp.Matrix(v)
    lhs = -sp.I * wv * vv
    rhs = sp.I * sum((k[j] * Atrue[j] for j in range(3)), sp.zeros(6)) * vv
    aff &= (lhs - rhs).applyfunc(sp.simplify).is_zero_matrix
ok.append(('(6\') A_j = [[0, L_j], [-L_j, 0]] simmetriche, B = 0, risolvono d_t psi = sum A_j d_j psi sui 48 modi', symm and aff))

# (7) kill: "nella classe simmetrica il nucleo e' 0" NON vale per ogni dato di Maxwell: un solo k (entrambi i rami)
rk_s1 = rank(sym_reduce(system_rows(modes(kv[:1])))[0])
print('    classe simmetrica, un solo k: rango', rk_s1, 'su 99')
ok.append(('(7) kill: classe simmetrica con un solo k: nucleo != 0 (l\'enunciato vale solo per dati generici)', rk_s1 < 99))

# (7') per tutti i k anche la classe simmetrica: nucleo 0 (identita' polinomiale con A_j simmetriche)
subsym = {}
for j in range(3):
    for r in range(6):
        for c in range(r+1, 6):
            subsym[Aj[j][c, r]] = Aj[j][r, c]
eqs_s = [e.subs(subsym) for e in eqs]
unk_s = [s for s in unk if s not in subsym]
Ms2, _ = sp.linear_eq_to_matrix(eqs_s, unk_s)
rk_s_all = DomainMatrix.from_Matrix(Ms2).convert_to(QQ).rank()
ok.append(('(7\') per tutti i k, classe simmetrica: rango %d = %d incognite' % (rk_s_all, len(unk_s)),
           rk_s_all == len(unk_s) == 99))

# (8) osservazione di forma: l'unione (non lo span) dei K(k), k reali, NON e' C^6
# v = ((1, i, 0), (0, 0, 1)): k.E = 0 con k reale => k1 = k2 = 0; k.B = 0 => k3 = 0.
ks = sp.symbols('s1:4', real=True)
Ev = [1, sp.I, 0]; Bv = [0, 0, 1]
eqs8 = [sp.re(sum(ks[i]*Ev[i] for i in range(3))), sp.im(sum(ks[i]*Ev[i] for i in range(3))),
        sum(ks[i]*Bv[i] for i in range(3))]
s8 = sp.solve(eqs8, ks, dict=True)
ok.append(('(8) ((1,i,0),(0,0,1)) non sta in nessun K(k) con k reale != 0: "unione = C^6" va letto "span = C^6"',
           s8 == [{ks[0]: 0, ks[1]: 0, ks[2]: 0}]))

for name, v in ok:
    print('PASS' if v else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
