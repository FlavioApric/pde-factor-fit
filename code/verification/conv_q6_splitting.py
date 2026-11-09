# S8-CONV, CONV-Q6 / CONV-T8: errore globale di Lie e Strang al 1° ordine in eps nel quadro di P3-T3
# (A0 = D d_xx Dirichlet su (0,L), V = -c d_x).  Solo verifica: forma chiusa contro somma diretta, pendenze, L^inf.
import sympy as sp
import mpmath as mp
mp.mp.dps = 30
ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)

# (1) simbolico: forma chiusa del termine modale.  a = e^{l1 h}, b = e^{lm h}, Delta = l1 - lm, x = Delta h
h, Dl, n = sp.symbols('h Delta n', positive=True)
l1, lm = sp.symbols('lambda1 lambdam', real=True)
a = sp.exp(l1*h); b = sp.exp(lm*h)
F1 = (a - b)/(l1 - lm)
q = (a**n - b**n)/(a - b)
lie = (F1 - h*b)*q
strang = (F1 - h/2*(a + b))*q
xx = (l1 - lm)*h
phiL = 1/xx - 1/(sp.exp(xx) - 1)
phiS = 1/xx - sp.Rational(1, 2)*sp.coth(xx/2)
for name, expr, phi in [('Lie', lie, phiL), ('Strang', strang, phiS)]:
    target = (a**n - b**n)*h*phi
    val = {l1: -sp.Rational(3, 7), lm: -sp.Rational(29, 5), h: sp.Rational(1, 13), n: 9}
    check('forma chiusa %s (valore razionale)' % name, abs(sp.N((expr - target).subs(val), 40)) < 1e-30)
# geometric sum identity
kk = sp.symbols('k', integer=True, nonnegative=True)
val = {l1: -1.0, lm: -7.3, h: 0.01, n: 37}
direct = sum(sp.exp(lm*(val[n]-kk-1)*val[h] + l1*kk*val[h]).subs({lm: val[lm], l1: val[l1]}) for kk in range(val[n]))
check('somma geometrica q', abs(float(direct) - float(q.subs(val))) < 1e-10)
# (2) limiti e maggioranti di phi
X = sp.symbols('X', positive=True)
check('phi_L(0+) = 1/2', sp.limit(1/X - 1/(sp.exp(X)-1), X, 0) == sp.Rational(1, 2))
check('phi_S ~ -X/12 (serie)', sp.simplify(sp.series(1/X - sp.cosh(X/2)/(2*sp.sinh(X/2)), X, 0, 3).removeO() + X/12) == 0)
check('phi_S(inf) = -1/2', sp.limit(1/X - sp.coth(X/2)/2, X, sp.oo) == -sp.Rational(1, 2))
grid = [mp.mpf(10)**(-6 + 0.05*j) for j in range(240)]
fL = lambda X: 1/X - 1/mp.expm1(X)
fS = lambda X: 1/X - mp.coth(X/2)/2
check('0 < phi_L <= 1/2 e phi_L >= min(1,1/X)/4 (griglia)', all(0 < fL(X) <= 0.5 and fL(X) >= min(1, 1/X)/4 for X in grid))
check('-min(X/12,1/2) <= phi_S <= 0 (griglia)', all(-min(X/12, mp.mpf(1)/2) - 1e-25 <= fS(X) <= 0 for X in grid))
check('|phi_S| crescente (griglia)', all(abs(fS(grid[j+1])) >= abs(fS(grid[j])) for j in range(len(grid)-1)))
check('|phi_S(1)| = 0.0819...', abs(abs(fS(mp.mpf(1))) - 0.08197) < 1e-4)

# (3) numerica: L = c = D = 1, T = 1, u0 = e_1
Lc, cc, Dc, T = 1, 1, 1, 1
kap = Dc*mp.pi**2/Lc**2
lam = lambda m: -kap*m*m
def Vm1(m):
    return 0 if (m + 1) % 2 == 0 else -4*cc*m/(Lc*(m*m - 1))
def G(hh, kind, Mmax):
    out = []
    for m in range(2, Mmax + 1, 2):
        X = (lam(1) - lam(m))*hh
        phi = fL(X) if kind == 'L' else fS(X)
        out.append(Vm1(m)*(mp.e**(lam(1)*T) - mp.e**(lam(m)*T))*hh*phi)
    return out
def l2(v): return mp.sqrt(sum(z*z for z in v))
def linf(v, hh):
    xs = [mp.mpf(j)/4000 for j in range(1, 400)]   # vicino al bordo x=0, dove vive lo strato
    return max(abs(sum(v[i]*mp.sqrt(2)*mp.sin((2*i + 2)*mp.pi*xv) for i in range(len(v)))) for xv in xs)
# confronto con somma diretta passo per passo (n piccolo)
hh = mp.mpf(1)/20; nn = 20
for kind in ('L', 'S'):
    cf = G(hh, kind, 60)
    dr = []
    for m in range(2, 61, 2):
        a_, b_ = mp.e**(lam(1)*hh), mp.e**(lam(m)*hh)
        F1n = (a_ - b_)/(lam(1) - lam(m))
        loc = F1n - (hh*b_ if kind == 'L' else hh/2*(a_ + b_))
        dr.append(Vm1(m)*loc*sum(mp.e**(lam(m)*(nn-k-1)*hh + lam(1)*k*hh) for k in range(nn)))
    check('forma chiusa = somma diretta (%s, n=20)' % kind, max(abs(cf[i]-dr[i]) for i in range(len(cf))) < 1e-20)
print('pendenze log-log (h -> h/4):')
res = {}
for kind in ('L', 'S'):
    prev = None
    for e in range(2, 7):
        hh = mp.mpf(4)**(-e)
        Mmax = int(40/mp.sqrt(hh)) + 50
        v = G(hh, kind, Mmax)
        nrm = l2(v)
        if prev is not None:
            sl = mp.log(prev/nrm)/mp.log(4)
            print('  %s  h=4^-%d  ||G||_L2=%s  pendenza=%s' % (kind, e, mp.nstr(nrm, 8), mp.nstr(sl, 6)))
            res[(kind, e)] = sl
        prev = nrm
check('Lie: pendenza L2 -> 1', abs(res[('L', 6)] - 1) < 0.02)
check('Strang: pendenza L2 -> 5/4', abs(res[('S', 6)] - 1.25) < 0.02)
# costante di Lie: ||G||/h -> (1/2) (sum V^2 (e^{l1T}-e^{lmT})^2)^{1/2}
CL = mp.sqrt(sum(Vm1(m)**2*(mp.e**(lam(1)*T) - mp.e**(lam(m)*T))**2 for m in range(2, 200001, 2)))/2
hh = mp.mpf(4)**(-6); v = G(hh, 'L', int(40/mp.sqrt(hh)) + 50)
print('  Lie: ||G||/h = %s, C_L = %s' % (mp.nstr(l2(v)/hh, 8), mp.nstr(CL, 8)))
v5 = G(hh*4, 'L', int(40/mp.sqrt(hh*4)) + 50); r6 = abs(l2(v)/hh/CL - 1); r5 = abs(l2(v5)/(4*hh)/CL - 1)
print('  errore relativo h=4^-5: %s, h=4^-6: %s, rapporto %s (atteso ~ 4^(1/2) = 2: coda dei modi m > h^(-1/2))' % (mp.nstr(r5, 4), mp.nstr(r6, 4), mp.nstr(r5/r6, 4)))
check('Lie: ||G||/h -> C_L con correzione relativa O(h^(1/2))', r6 < 0.03 and 1.8 < r5/r6 < 2.2)
# L^inf di Strang (V-ex): pendenza
prev = None
for e in (3, 4, 5):
    hh = mp.mpf(4)**(-e); v = G(hh, 'S', int(30/mp.sqrt(hh)) + 50)
    ni = linf(v, hh)
    if prev is not None:
        print('  Strang L^inf h=4^-%d  pendenza=%s' % (e, mp.nstr(mp.log(prev/ni)/mp.log(4), 5)))
        last = mp.log(prev/ni)/mp.log(4)
    prev = ni
check('[V-ex] Strang: pendenza L^inf vicino a 1', abs(last - 1) < 0.1)
print('ESITO:', 'TUTTI PASS' if ok else 'QUALCHE FAIL')
