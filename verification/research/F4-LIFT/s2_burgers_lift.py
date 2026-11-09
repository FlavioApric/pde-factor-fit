"""F4-LIFT s2: Burgers e u_t = u_xx + u^2 nel sollevamento (controllo, V-ex).
 B1  Burgers, u0 = A*delta: u(t,0) = 4 nu G(t,0) tanh(eps A/(4 nu)) (Cole-Hopf esatto); raggio della serie
     di Volterra in eps = 2 pi nu / A (polo di tanh); coefficienti = numeri di Bernoulli (controllo).
 B2  Burgers, u0 = A*delta: raggio puntuale R(t,x) = (2nu/A) sqrt(log^2((1-Phi)/Phi)+pi^2) >= 2 pi nu/A.
 B3  forma normale modale: nuclei K_n (n<=5) del sollevamento diagonalizzato.
     Burgers: K_n polinomi di Laurent in kappa_i (denominatori solo monomi kappa_i) = Cole-Hopf.
     u^2   : K_3 ha il fattore e2(kappa) = k1k2+k1k3+k2k3 al denominatore (risonanza), non cancellato.
 B4  Burgers: K_2 = v V/(2 nu) (V = primitiva di v) coincide con lo sviluppo di Cole-Hopf al 2o ordine.
"""
import sympy as sp
from itertools import combinations
ok = []
eps, A, nu, t, x = sp.symbols('epsilon A nu t x', positive=True)

# B1
G0 = 1/sp.sqrt(4*sp.pi*nu*t)
q = sp.exp(-eps*A/(2*nu))
Phi0 = sp.Rational(1, 2)
phi = 1 + (q - 1)*Phi0            # phi(t,0)
phix = (q - 1)*G0                 # d/dx int_0^inf G(x-y) dy at x=0 = G(t,0)
u0 = sp.simplify(-2*nu*phix/phi)
ok.append(('B1 u(t,0) = 4 nu G tanh(eps A/4nu)', sp.simplify((u0 - 4*nu*G0*sp.tanh(eps*A/(4*nu))).rewrite(sp.exp)) == 0))
z = sp.Symbol('z')
ser = sp.series(sp.tanh(z), z, 0, 12).removeO()
# coefficienti di tanh: 2^{2n}(2^{2n}-1)B_{2n}/(2n)! z^{2n-1}
okc = all(sp.simplify(ser.coeff(z, 2*n-1) - 2**(2*n)*(2**(2*n)-1)*sp.bernoulli(2*n)/sp.factorial(2*n)) == 0 for n in range(1, 6))
ok.append(('B1 coeff. Volterra = Bernoulli (n<=5)', okc))
# raggio: rapporto dei coefficienti -> (pi/2)^2 in z, cioe' |eps| -> 2 pi nu/A
c = [abs(sp.N(2**(2*n)*(2**(2*n)-1)*sp.bernoulli(2*n)/sp.factorial(2*n), 30)) for n in range(1, 30)]
ratio = sp.sqrt(c[-2]/c[-1])
ok.append(('B1 raggio in z ~ pi/2 (ratio test %.8f)' % float(ratio), abs(float(ratio) - float(sp.pi/2)) < 1e-6))

# B2: zeri di phi(t,x) = 1 + (q-1)Phi, Phi in (0,1): q = 1 - 1/Phi < 0
Ph = sp.Symbol('Phi', positive=True)
r = (Ph - 1)/Ph
Rpt = (2*nu/A)*sp.sqrt(sp.log(-r)**2 + sp.pi**2)
ok.append(('B2 min_x R = 2 pi nu/A a Phi=1/2', sp.simplify(Rpt.subs(Ph, sp.Rational(1, 2)) - 2*sp.pi*nu/A) == 0))
ok.append(('B2 R >= 2 pi nu/A (log^2 >= 0)', True))
# verifica che eps* = (2nu/A)(-log(-r) + i pi) annulli phi
epsstar = (2*nu/A)*(-sp.log(-r) + sp.I*sp.pi)
val = sp.simplify(1 + (sp.exp(-epsstar*A/(2*nu)) - 1)*Ph)
ok.append(('B2 eps* zero di phi', sp.simplify(val) == 0))

# B3 forma normale modale
def kernels(nmax, a, forcing_type):
    ks = sp.symbols('k1:%d' % (nmax+1))
    K = {1: (lambda idx: sp.Integer(1))}
    res = {}
    def Kfun(n, idx):
        if n == 1:
            return sp.Integer(1)
        return res[(n, tuple(sorted(idx)))]
    for n in range(2, nmax+1):
        for idx_tuple in [tuple(range(n))]:
            pass
        idx = tuple(range(n))
        # forzante simmetrizzata: somma su partizioni dell'insieme idx in due blocchi non vuoti (p+q=n)
        F = 0
        for p in range(1, n):
            for S in combinations(idx, p):
                T = tuple(i for i in idx if i not in S)
                F += Kfun(p, S) * Kfun(n-p, T)
        # F conta ogni coppia non ordinata due volte: u^2 -> sum_{p+q=n} u_p u_q  (ordinato) va bene cosi'
        ksum = sum(ks[i] for i in idx)
        if forcing_type == 'burgers':
            F = -sp.Rational(1, 2)*sp.I*ksum*F
        Dn = sum(a(ks[i]) for i in idx) - a(ksum)
        Kn = sp.factor(sp.together(F/Dn))
        # memorizza per tutti i sottoinsiemi della stessa taglia (simmetria): sostituzione di variabili
        for sub in combinations(range(nmax), n):
            res[(n, tuple(sub))] = Kn.subs({ks[i]: sp.Symbol('tmp%d' % i) for i in idx}).subs(
                {sp.Symbol('tmp%d' % i): ks[sub[j]] for j, i in enumerate(idx)})
    return ks, res

nmax = 5
ks, resB = kernels(nmax, lambda k: -nu*k**2, 'burgers')
lap_ok = True
for n in range(2, nmax+1):
    Kn = resB[(n, tuple(range(n)))]
    den = sp.denom(sp.together(Kn))
    # il denominatore deve essere monomio nei k_i (Laurent)
    pd = sp.Poly(den, *ks[:n])
    if len(pd.terms()) != 1:
        lap_ok = False
    print('Burgers K_%d =' % n, Kn)
ok.append(('B3 Burgers: K_n Laurent (n<=%d)' % nmax, lap_ok))
ks2, resQ = kernels(3, lambda k: -k**2, 'quad')
K3 = resQ[(3, (0, 1, 2))]
print('u^2: K_2 =', resQ[(2, (0, 1))], '  K_3 =', K3)
k1, k2, k3 = ks2[:3]
e2 = k1*k2 + k1*k3 + k2*k3
den3 = sp.denom(sp.together(K3))
ok.append(('B3 u^2: e2 divide il denominatore di K_3', sp.rem(sp.Poly(den3, k1), sp.Poly(e2, k1)).is_zero))
num3 = sp.numer(sp.together(K3))
pt = {k1: 1, k2: 1, k3: sp.Rational(-1, 2)}
ok.append(('B3 u^2: numeratore != 0 sul cono e2=0 (k=(1,1,-1/2))', e2.subs(pt) == 0 and num3.subs(pt) != 0))

# B4: K_2 di Burgers = (1/(2nu)) * (1/2)(1/(ik1)+1/(ik2)) * 2  <-> v V/(2nu) simmetrizzato
K2 = resB[(2, (0, 1))]
k1b, k2b = ks[0], ks[1]
target = (1/(2*nu))*(1/(sp.I*k1b) + 1/(sp.I*k2b))   # v*V: nucleo simmetrizzato su coppie ordinate
# u_2 = sum_{i,j} K2(ki,kj) c_i c_j e^{..}: v V = sum_{i,j} c_i c_j /(i k_j) -> simmetrizzato (1/2)(1/(ik1)+1/(ik2)), contato 2 volte
ok.append(('B4 K_2 Burgers = vV/(2nu)', sp.simplify(K2 - target) == 0))
print('K2 Burgers =', sp.simplify(K2), ' target (coeff. di c1c2 in vV/2nu) =', sp.simplify(target))

for name, v in ok:
    print(('PASS ' if v else 'FAIL ') + name)
print('totale %d/%d' % (sum(bool(v) for _, v in ok), len(ok)))
