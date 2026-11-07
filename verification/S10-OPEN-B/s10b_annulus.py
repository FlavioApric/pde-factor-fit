# S10-OPEN-B · controesempio alla densita' di OPF5B-T1 fuori dai convessi (solo verifica).
# Omega = (0,3)^2 \ [1,2]^2 (corona quadrata), P = d_x d_y, Q_1 = d_x, Q_2 = d_y.
# u = phi(x) psi(y), phi, psi in C^inf, phi = 0 su (-inf,1], 1 su [2,inf); idem psi.
# A1: u_xy = phi'(x) psi'(y) e' nullo su Omega (supporto in [1,2]^2): controllo su griglia.
# A2: Lambda(a+b) = 0 per a = a(y) (componenti orizzontali) e b = b(x) generiche: identita' simbolica sui 4 vertici
#     del rettangolo [x1,x2]x[y1,y2] con x1 < 1 < 2 < x2, y1 < 1 < 2 < y2 (lati interamente in Omega).
# A3: Lambda_avg(u) = 1 (quadratura numerica del funzionale mediato).
import sympy as sp, mpmath as mp
ok = []
def rep(n, c): ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + n)
def h(s): return mp.exp(-1/s) if s > 0 else mp.mpf(0)
def step(s):  # 0 per s <= 1, 1 per s >= 2, C^inf
    return h(s-1)/(h(s-1)+h(2-s))
def dstep(s): return mp.diff(step, s) if 1 < s < 2 else mp.mpf(0)
inO = lambda X, Y: 0 < X < 3 and 0 < Y < 3 and not (1 <= X <= 2 and 1 <= Y <= 2)
worst = 0
for i in range(1, 60):
    for j in range(1, 60):
        X, Y = mp.mpf(i)/20, mp.mpf(j)/20
        if inO(X, Y): worst = max(worst, abs(dstep(X)*dstep(Y)))
rep('A1 u_xy = 0 su Omega (griglia 59x59), max = %s' % mp.nstr(worst, 3), worst == 0)
x1, x2, y1, y2 = sp.symbols('x1 x2 y1 y2')
aL, aR = sp.Function('a'), sp.Function('b')
# a funzione di y sulle righe y1, y2 (righe connesse in Omega): a(x,y_i) = A(y_i) indipendente da x
A, B = sp.Function('A'), sp.Function('B')
Lam = lambda F: F(x2, y2) - F(x1, y2) - F(x2, y1) + F(x1, y1)
rep('A2 Lambda(A(y) + B(x)) = 0', sp.simplify(Lam(lambda X, Y: A(Y) + B(X))) == 0)
mp.mp.dps = 20
u = lambda X, Y: step(X)*step(Y)
# Lambda_avg: media sui vertici in quadratini di lato 0.2 centrati in (0.5,0.5),(2.5,0.5),(2.5,2.5),(0.5,2.5)
avg = lambda cx, cy: mp.quad(lambda X: mp.quad(lambda Y: u(X, Y), [cy-0.1, cy+0.1]), [cx-0.1, cx+0.1])/mp.mpf('0.04')
L = avg(2.5, 2.5) - avg(0.5, 2.5) - avg(2.5, 0.5) + avg(0.5, 0.5)
rep('A3 Lambda_avg(u) = %s' % mp.nstr(L, 12), abs(L - 1) < 1e-12)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
