# S-CHECK-EX10 -- controllo indipendente di EX10-e-H (decomposizione di Maxwell per elicita')
# P in R^{8x6}: righe tau E - xi x B, tau B + xi x E, xi.E, xi.B  (R = C[tau, xi1, xi2, xi3]).
# F = E + iB, G = E - iB.  Q_1 = P + {G = 0}, Q_2 = P + {F = 0}.
import sympy as sp

ok = []
tau, x1, x2, x3 = sp.symbols('tau xi1 xi2 xi3')
xi = sp.Matrix([x1, x2, x3])
def Cmat(v):  # C(v) w = v x w
    return sp.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
C = Cmat(xi); I3 = sp.eye(3); Z3 = sp.zeros(3); z = sp.zeros(1, 3)
P = sp.Matrix(sp.BlockMatrix([[tau*I3, -C], [C, tau*I3], [xi.T, z], [z, xi.T]]))

# (1) livello delle funzioni: Maxwell <=> due equazioni di elicita' disaccoppiate (operatori veri, non simboli)
t, y1, y2, y3 = sp.symbols('t y1 y2 y3')
ys = (y1, y2, y3)
Ef = sp.Matrix([sp.Function('E%d' % i)(t, *ys) for i in range(3)])
Bf = sp.Matrix([sp.Function('B%d' % i)(t, *ys) for i in range(3)])
curl = lambda V: sp.Matrix([sp.diff(V[2], y2) - sp.diff(V[1], y3), sp.diff(V[0], y3) - sp.diff(V[2], y1),
                            sp.diff(V[1], y1) - sp.diff(V[0], y2)])
div = lambda V: sum(sp.diff(V[i], ys[i]) for i in range(3))
M1 = Ef.diff(t) - curl(Bf); M2 = Bf.diff(t) + curl(Ef)
Ff = Ef + sp.I*Bf; Gf = Ef - sp.I*Bf
HF = Ff.diff(t) + sp.I*curl(Ff); HG = Gf.diff(t) - sp.I*curl(Gf)
ok.append(('(1) F_t + i curl F = M1 + i M2,  G_t - i curl G = M1 - i M2,  div F/G = div E +- i div B',
           (HF - (M1 + sp.I*M2)).applyfunc(sp.expand).is_zero_matrix and
           (HG - (M1 - sp.I*M2)).applyfunc(sp.expand).is_zero_matrix and
           sp.expand(div(Ff) - div(Ef) - sp.I*div(Bf)) == 0))

# (2) V, T costanti costruiti qui: psi = T (F, G), V combina le righe
T = sp.Matrix(sp.BlockMatrix([[I3/2, I3/2], [I3/(2*sp.I), -I3/(2*sp.I)]]))
V = sp.zeros(8, 8)
V[0:3, 0:3] = I3; V[0:3, 3:6] = sp.I*I3          # righe E + i righe B
V[3:6, 0:3] = I3; V[3:6, 3:6] = -sp.I*I3         # righe E - i righe B
V[6, 6] = 1; V[6, 7] = sp.I                      # div E + i div B
V[7, 6] = 1; V[7, 7] = -sp.I
VPT = (V*P*T).applyfunc(sp.expand)
PF = sp.Matrix(sp.BlockMatrix([[tau*I3 + sp.I*C], [xi.T]]))
PG = sp.Matrix(sp.BlockMatrix([[tau*I3 - sp.I*C], [xi.T]]))
target = sp.zeros(8, 6)
target[0:3, 0:3] = PF[0:3, :]; target[6, 0:3] = PF[3, :]
target[3:6, 3:6] = PG[0:3, :]; target[7, 3:6] = PG[3, :]
ok.append(('(2) V, T costanti invertibili (det V = %s, det T = %s)' % (sp.simplify(V.det()), sp.simplify(T.det())),
           V.det() != 0 and T.det() != 0))
ok.append(('(2\') V P T = diag(P_F, P_G) a meno di permutazione delle righe', (VPT - target).is_zero_matrix))

# (3) N = 0: righe costanti di Q_1 (G = 0) e Q_2 (F = 0) nelle coordinate originali, rango 6 su C
rowG = sp.Matrix(sp.BlockMatrix([[I3, -sp.I*I3]]))   # G = E - iB
rowF = sp.Matrix(sp.BlockMatrix([[I3, sp.I*I3]]))    # F = E + iB
ok.append(('(3) [rowF; rowG] costante di rango 6: U_1 + U_2 contiene R^{1x6}, N = 0',
           sp.Matrix.vstack(rowF, rowG).rank() == 6))

# (4) U_1 cap U_2 = U_P: nelle coordinate (F, G) U_P = U_{P_F} (+) U_{P_G}, U_1 = U_{P_F} (+) R^3, U_2 = R^3 (+) U_{P_G}.
# Controllo esplicito di "U_P = somma diretta dei blocchi": ogni riga (r_F, 0) con r_F in U_{P_F} sta in U_P'
# (le righe di VPT sono generatori di U_P' = U_P T); verifica che le righe di VPT siano gia' a blocchi.
blk = all(VPT[i, 3:6] == sp.zeros(1, 3) for i in (0, 1, 2, 6)) and all(VPT[i, 0:3] == sp.zeros(1, 3) for i in (3, 4, 5, 7))
ok.append(('(4) generatori di U_P T a blocchi (righe solo-F e solo-G): U_P T = U_{P_F} (+) U_{P_G}, quindi U_1 cap U_2 = U_P', blk))

# (5) proiettori costanti: pi_1 = T diag(I,0) T^{-1}, pi_2 = T diag(0,I) T^{-1};  P pi_1 = W_1 P con W_1 costante
D1 = sp.diag(I3, Z3); D2 = sp.diag(Z3, I3)
pi1 = T*D1*T.inv(); pi2 = T*D2*T.inv()
W1 = V.inv()*sp.diag(sp.eye(3), sp.zeros(3), 1, 0)*V
W2 = V.inv()*sp.diag(sp.zeros(3), sp.eye(3), 0, 1)*V
# riordino: le righe di VPT sono (F-curl, G-curl, F-div, G-div): proiettore sulle righe F = diag(I3, 0, 1, 0)
c1 = (P*pi1 - W1*P).applyfunc(sp.expand).is_zero_matrix
c2 = (P*pi2 - W2*P).applyfunc(sp.expand).is_zero_matrix
ok.append(('(5) P pi_i = W_i P con W_i costanti: pi_i manda Sol(P) in Sol(P) su ogni Omega, in C^inf e D\'', c1 and c2))
ok.append(('(5\') pi_1 + pi_2 = I, pi_1 pi_2 = 0; G(pi_1 psi) = 0, F(pi_2 psi) = 0',
           (pi1 + pi2 - sp.eye(6)).is_zero_matrix and (pi1*pi2).is_zero_matrix and
           (rowG*pi1).applyfunc(sp.simplify).is_zero_matrix and (rowF*pi2).applyfunc(sp.simplify).is_zero_matrix))

# (6) stessa varieta' caratteristica
dF = sp.factor((tau*I3 + sp.I*C).det()); dG = sp.factor((tau*I3 - sp.I*C).det())
ok.append(('(6) det(tau I + i C) = det(tau I - i C) = %s' % dF,
           sp.expand(dF - tau*(tau**2 - x1**2 - x2**2 - x3**2)) == 0 and sp.expand(dF - dG) == 0))

# (7) kill: la scomposizione non e' banale -- onde circolari in Sol(Q_1) e Sol(Q_2), non nulle
# F = (1, i, 0) e^{i(z - t)} risolve F_t + i curl F = 0 (elicita' +), G = 0
zf = sp.exp(sp.I*(y3 - t))
Fw = sp.Matrix([1, sp.I, 0])*zf
ok.append(('(7) F = (1,i,0)e^{i(z-t)}: F_t + i curl F = 0, div F = 0 (Sol(Q_1) != 0); il coniugato complesso di elicita\' opposta in Sol(Q_2)',
           (Fw.diff(t) + sp.I*curl(Fw)).applyfunc(sp.simplify).is_zero_matrix and sp.simplify(div(Fw)) == 0 and
           (lambda Gw: (Gw.diff(t) - sp.I*curl(Gw)).applyfunc(sp.simplify).is_zero_matrix)(sp.Matrix([1, -sp.I, 0])*zf)))

# (8) kill: proiettori non costanti non servono e la scomposizione per segno di frequenza non e' polinomiale:
# su un'onda piana di elicita' +, entrambi i segni di omega compaiono (omega = +|k| e omega = -|k| con k -> -k)
Fw2 = sp.Matrix([1, sp.I, 0])*sp.exp(sp.I*(-y3 + t))   # k = -e3, omega = -1
ok.append(('(8) elicita\' + contiene sia omega = +1 sia omega = -1: elicita\' != segno della frequenza',
           (Fw2.diff(t) + sp.I*curl(Fw2)).applyfunc(sp.simplify).is_zero_matrix))

for name, v in ok:
    print('PASS' if v else 'FAIL', name)
print('%d/%d PASS' % (sum(1 for _, v in ok if v), len(ok)))
