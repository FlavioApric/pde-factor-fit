"""F4-LIFT s3 (controllo, V-ex).
 L1  Burgers: d/dt(u^k) = nu d_x^2(u^k) - nu k(k-1) u^{k-2} u_x^2 - k/(k+1) d_x(u^{k+1}): le potenze puntuali non chiudono
     (risposta a F4-ALG, domanda 1); le funzioni a k punti y_k = u(x1)...u(xk) chiudono (parte lineare = somma di Kronecker).
 L2  ODE x' = F(x): l'ideale (x - x*) e' D-stabile  <=>  F(x*) = 0 (Carleman centrato in x* troncabile <=> x* equilibrio).
 L3  modulo dei sollevati Ann_2(u) = {(Q0,Q1,Q2): Q0*1 + Q1 u + Q2 u^2 = 0}, |alpha| <= 2, per Burgers (nu = 1):
     1 fronte (onda viaggiante) vs 2 fronti: dimensione del nucleo del Gram (rango numerico ad alta precisione, solo controllo).
 L4  (iii) ker(tau - a(xi)) chiuso per prodotti sugli esponenziali <=> a(z1)+a(z2) = a(z1+z2): calore no (z1 z2 = 0), trasporto si'.
 L5  PDE u_t = u_xx + u^2: parentesi dei due campi (lineare, quadratico) generano campi quadratici nuovi u_x^2, u_xx^2 (algebra
     di Lie dei termini non finita); Burgers: [u_xx, -u u_x] = 2 u_x u_xx.
"""
import sympy as sp
import mpmath as mp
ok = []
t, x, nu = sp.symbols('t x nu')
u = sp.Function('u')(t, x)

# L1
for k in range(2, 6):
    ut = nu*sp.diff(u, x, 2) - u*sp.diff(u, x)
    lhs = sp.expand(k*u**(k-1)*ut)
    rhs = sp.expand(nu*sp.diff(u**k, x, 2) - nu*k*(k-1)*u**(k-2)*sp.diff(u, x)**2 - sp.Rational(k, k+1)*sp.diff(u**(k+1), x))
    ok.append(('L1 k=%d' % k, sp.simplify(lhs - rhs) == 0))
x1, x2 = sp.symbols('x1 x2')
w = sp.Function('w')
y2 = w(t, x1)*w(t, x2)
# per w soluzione di w_t = nu w_xx - w w_x : d_t y2 = nu(d_x1^2 + d_x2^2) y2 + (termine con y3 sulle diagonali)
wt = lambda X: nu*sp.diff(w(t, X), X, 2) - w(t, X)*sp.diff(w(t, X), X)
lhs = sp.expand(wt(x1)*w(t, x2) + w(t, x1)*wt(x2))
lin = sp.expand(nu*(sp.diff(y2, x1, 2) + sp.diff(y2, x2, 2)))
rest = sp.expand(lhs - lin)
ok.append(('L1 y2 chiude: resto = -(w w_x)(x1) w(x2) - w(x1)(w w_x)(x2) (traccia di y3)',
           sp.simplify(rest + w(t, x1)*sp.diff(w(t, x1), x1)*w(t, x2) + w(t, x1)*w(t, x2)*sp.diff(w(t, x2), x2)) == 0))

# L2
X, xs = sp.symbols('X xs')
f0, f1, f2, f3 = sp.symbols('f0:4')
F = f0 + f1*(X - xs) + f2*(X - xs)**2 + f3*(X - xs)**3
for N in range(0, 4):
    img = sp.expand(F*sp.diff((X - xs)**(N+1), X))
    rem = sp.rem(sp.Poly(img, X), sp.Poly((X - xs)**(N+1), X)).as_expr()
    ok.append(('L2 N=%d resto = (N+1) F(x*) (X-x*)^N' % N, sp.simplify(rem - (N+1)*f0*(X - xs)**N) == 0))

# L3
mp.mp.dps = 60
def burgers_from_phi(coeffs):
    T, Xs = sp.symbols('T Xs')
    phi = sum(c*sp.exp(a*Xs + a**2*T) for a, c in coeffs)
    U = sp.simplify(-2*sp.diff(phi, Xs)/phi)
    return T, Xs, U
def gram_kernel_dim(coeffs, npts=40):
    T, Xs, U = burgers_from_phi(coeffs)
    assert sp.simplify(sp.diff(U, T) + U*sp.diff(U, Xs) - sp.diff(U, Xs, 2)) == 0
    alphas = [(i, j) for i in range(3) for j in range(3) if i + j <= 2]
    funcs = [sp.Integer(1)] + [sp.diff(U, T, i, Xs, j) if (i or j) else U for (i, j) in alphas] + \
            [sp.diff(U**2, T, i, Xs, j) if (i or j) else U**2 for (i, j) in alphas]
    fl = [sp.lambdify((T, Xs), f, 'mpmath') for f in funcs]
    import random
    random.seed(1)
    rows = []
    for _ in range(npts):
        tt, xx = mp.mpf(random.uniform(0.1, 1.0)), mp.mpf(random.uniform(-2, 2))
        rows.append([mp.mpf(f(tt, xx)) if not isinstance(f(tt, xx), int) else mp.mpf(f(tt, xx)) for f in fl])
    M = mp.matrix(rows)
    S = mp.svd_r(M, compute_uv=False)
    s = [S[i] for i in range(min(M.rows, M.cols))]
    smax = max(s)
    rank = sum(1 for v in s if v > smax*mp.mpf(10)**(-40))
    return len(funcs) - rank, len(funcs)
d1, n1 = gram_kernel_dim([(sp.Integer(0), 1), (sp.Integer(1), 1)])          # 1 fronte (onda viaggiante)
d2, n2 = gram_kernel_dim([(sp.Integer(0), 1), (sp.Integer(1), 1), (sp.Rational(-3, 2), 1)])  # 2 fronti
print('L3 dizionario di %d funzioni: dim nucleo 1 fronte = %d, 2 fronti = %d' % (n1, d1, d2))
ok.append(('L3 2 fronti: solo la relazione di Burgers (dim 1)', d2 == 1))
ok.append(('L3 1 fronte: relazioni in piu\' (simmetria + Riccati), dim > 1', d1 > 1))

# L4
z1, z2, c = sp.symbols('z1 z2 c')
heat = lambda z: z**2
transp = lambda z: -c*z
ok.append(('L4 calore: defetto di risonanza = -2 z1 z2', sp.expand(heat(z1) + heat(z2) - heat(z1 + z2) + 2*z1*z2) == 0))
ok.append(('L4 trasporto: additivo (ker chiuso per prodotti)', sp.expand(transp(z1) + transp(z2) - transp(z1 + z2)) == 0))

# L5 parentesi di campi evolutivi: [F,G] = D_G F - D_F G (derivate di Frechet), su getti
us = sp.symbols('u0:8')
def D(expr):  # derivata totale in x sui getti
    return sum(sp.diff(expr, us[i])*us[i+1] for i in range(7))
def frechet(Fx, G):  # D_F[G] = sum_k dF/du_k * D^k G
    res, Gk = 0, G
    for k in range(6):
        res += sp.diff(Fx, us[k])*Gk
        Gk = D(Gk)
    return sp.expand(res)
def bracket(Fx, G):
    return sp.expand(frechet(Fx, G) - frechet(G, Fx))
lin, quad = us[2], us[0]**2
b1 = bracket(quad, lin)
b2 = bracket(b1, lin)
print('L5 [u^2, u_xx] =', b1, '; [[u^2,u_xx],u_xx] =', b2)
ok.append(('L5 [u^2,u_xx] ~ u_x^2', sp.simplify(b1/us[1]**2).is_number))
ok.append(('L5 [[u^2,u_xx],u_xx] ~ u_xx^2', sp.simplify(b2/us[2]**2).is_number))
bb = bracket(-us[0]*us[1], us[2])
print('L5 Burgers [ -u u_x, u_xx ] =', bb)
ok.append(('L5 Burgers bracket = +-2 u_x u_xx', sp.simplify(bb**2 - 4*us[1]**2*us[2]**2) == 0))

for name, v in ok:
    print(('PASS ' if v else 'FAIL ') + name)
print('totale %d/%d' % (sum(bool(v) for _, v in ok), len(ok)))
