# S10-OPEN-B · controlli per [Hm] (leggi di conservazione di Gardner), solo verifica.
# Convenzione del progetto: u_t = K_1[u] = -(u_xxx + 6 u u_x).
# H1: identita di Miura-Gardner (convenzione +6uu_x)  u = w + e w_x - e^2 w^2  ⇒
#     u_t + 6 u u_x + u_xxx = (1 + e D - 2 e^2 w)(w_t + 6(w - e^2 w^2) w_x + w_xxx)   (simbolico)
# H2: w_n dalla ricorrenza w_0 = u, w_n = -D w_{n-1} + sum_{i+j=n-2} w_i w_j ; densita' conservate:
#     Euler(D_F w_n) = 0 per n <= 8 (D_F = derivazione evolutiva di KdV sui getti)
# H3: parte quadratica di w_{2n} ≡ (-1)^(n+1) y_{n-1}^2 modulo derivate totali (operatore di Eulero), n <= 5
# H4: ogni monomio di grado d >= 3 di w_{2n} ha peso 2n+2 (wt y_j = j+2)
import sympy as sp
ok = []
def rep(name, c): ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
# H1
t, x, e = sp.symbols('t x e')
w = sp.Function('w')(t, x)
U = w + e*sp.diff(w, x) - e**2*w**2
lhs = sp.diff(U, t) + 6*U*sp.diff(U, x) + sp.diff(U, x, 3)
G = sp.diff(w, t) + 6*(w - e**2*w**2)*sp.diff(w, x) + sp.diff(w, x, 3)
rhs = G + e*sp.diff(G, x) - 2*e**2*w*G
rep('H1 identita di Miura-Gardner', sp.expand(lhs - rhs) == 0)
# getti
M = 40
Y = sp.symbols('y0:%d' % M)
def D(p): return sp.expand(sum(sp.diff(p, Y[j])*Y[j+1] for j in range(M-1)))
def Dn(p, n):
    for _ in range(n): p = D(p)
    return p
F = -(Y[3] + 6*Y[0]*Y[1])          # u_t
def DF(p): return sp.expand(sum(sp.diff(p, Y[j])*Dn(F, j) for j in range(M-6) if p.has(Y[j])))
def euler(p):
    return sp.expand(sum((-1)**j*Dn(sp.diff(p, Y[j]), j) for j in range(M-6) if p.has(Y[j])))
wn = [Y[0]]
for n in range(1, 11):
    s = -D(wn[n-1]) + sum(wn[i]*wn[n-2-i] for i in range(0, n-1))
    wn.append(sp.expand(s))
good = all(euler(DF(wn[n])) == 0 for n in range(0, 9))
rep('H2 Euler(D_F w_n) = 0, n <= 8', good)
def wt(m): return sum((j+2)*e_ for j, e_ in enumerate(m))
g3 = g4 = True
for n in range(1, 6):
    P = sp.Poly(wn[2*n], *Y[:2*n+1])
    quad = sum(c*sp.Mul(*[Y[j]**e_ for j, e_ in enumerate(m)]) for m, c in zip(P.monoms(), P.coeffs()) if sum(m) == 2)
    if euler(quad - (-1)**(n+1)*Y[n-1]**2) != 0: g3 = False
    for m, c in zip(P.monoms(), P.coeffs()):
        if sum(m) >= 3 and wt(m) != 2*n+2: g4 = False
        if sum(m) == 1 and wt(m) != 2*n+2: g4 = False
rep('H3 parte quadratica di w_2n = (-1)^(n+1) y_(n-1)^2 mod derivate totali, n <= 5', g3)
rep('H4 omogeneita di peso 2n+2 dei monomi di w_2n, n <= 5', g4)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
