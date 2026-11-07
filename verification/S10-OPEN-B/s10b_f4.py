# S10-OPEN-B · controlli per [F4-] (N-solitone di Hirota senza riflessione), solo verifica.
# F1: minori principali della matrice C_ij = 2 sqrt(k_i k_j)/(k_i+k_j) = prod_{i<j in S} ((k_i-k_j)/(k_i+k_j))^2  (N <= 4, simbolico)  [rev2: saltabile con argomento noF1]
# F2: regola dei segni sign rho(S) = prod_{j in S} (-1)^(j-1)  (kappa crescenti, N <= 6, esatto)
# F3: identita' rho(S) = prod_{j in S} d_j * prod_{i<j in S}((kappa_i-kappa_j)/(kappa_i+kappa_j))^2  (N <= 6, esatto)
# F4: W(phi_1..phi_N) = V * exp(-sum kappa x) * f_tilde  (N = 2, 3, numerico 40 cifre in 7 punti x)
# F5: L A = A L_0 su e^{ikx}: (-D^2 - u) psi = k^2 psi, psi = W(phi, e^{ikx})/W(phi)  (N = 2, 3; rev2: sostituzione esatta ed evalf a 60 cifre)
# F6: asintotica psi e^{-ikx} -> prod(ik - kappa_j) (x -> +inf), prod(ik + kappa_j) (x -> -inf)  (N = 2, 3, numerico)
import sympy as sp, itertools, mpmath as mp, sys
SKIP_F1 = 'noF1' in sys.argv   # rev2: 'python s10b_f4.py noF1' esegue solo F2-F6
ok = []
def rep(name, cond):
    ok.append(bool(cond)); print(('OK  ' if cond else 'FAIL') + ' ' + name)
# F1
for N in ([] if SKIP_F1 else range(1, 5)):
    k = sp.symbols('k1:%d' % (N+1), positive=True)
    good = True
    for r in range(1, N+1):
        for S in itertools.combinations(range(N), r):
            M = sp.Matrix(r, r, lambda a, b: 2*sp.sqrt(k[S[a]]*k[S[b]])/(k[S[a]]+k[S[b]]))
            lhs = sp.factor(M.det())
            rhs = sp.Mul(*[((k[i]-k[j])/(k[i]+k[j]))**2 for i, j in itertools.combinations(S, 2)])
            if sp.simplify(lhs - rhs) != 0: good = False
    rep('F1 minori di Cauchy N=%d' % N, good)
# F2, F3
for N in range(1, 7):
    kap = [sp.Rational(p, 3) for p in [1, 2, 4, 5, 7, 11, 13][:N]]   # crescenti
    d = [sp.Mul(*[(kap[j]+kap[l])/abs(kap[j]-kap[l]) for l in range(N) if l != j]) for j in range(N)]
    g2 = g3 = True
    for r in range(0, N+1):
        for S in itertools.combinations(range(N), r):
            s = [(1 if j in S else -1) for j in range(N)]   # esponenti s_j*kappa_j: +kappa se in S (semi e^{-kx} + eps c e^{kx})
            rho = sp.Mul(*[(s[j]*kap[j] - s[i]*kap[i])/(kap[i]-kap[j]) * (-1) for i, j in itertools.combinations(range(N), 2)])
            # rho(S) := V(s)/V(-1,...,-1), V(z) = prod_{i<j}(z_j - z_i)
            Vs = sp.Mul(*[(s[j]*kap[j] - s[i]*kap[i]) for i, j in itertools.combinations(range(N), 2)])
            V0 = sp.Mul(*[(-kap[j] + kap[i]) for i, j in itertools.combinations(range(N), 2)])
            rho = Vs / V0
            if sp.sign(rho) != sp.Mul(*[(-1)**j for j in S]): g2 = False   # j 0-based: (-1)^(j) = (-1)^((j+1)-1)
            rhs = sp.Mul(*[d[j] for j in S]) * sp.Mul(*[((kap[i]-kap[j])/(kap[i]+kap[j]))**2 for i, j in itertools.combinations(S, 2)])
            if sp.simplify(abs(rho) - rhs) != 0: g3 = False
    rep('F2 segni N=%d' % N, g2); rep('F3 modulo di rho N=%d' % N, g3)
# F4, F5, F6
x = sp.Symbol('x', real=True)
def build(N):
    kap = [sp.Rational(p, 2) for p in [1, 3, 4][:N]]
    c = [sp.Rational(q, 5) for q in [3, 7, 2][:N]]
    eps = [(-1)**j for j in range(N)]
    phi = [sp.exp(-kap[j]*x) + eps[j]*c[j]*sp.exp(kap[j]*x) for j in range(N)]
    W = sp.Matrix(N, N, lambda a, b: sp.diff(phi[b], x, a)).det()
    V0 = sp.Mul(*[(-kap[j] + kap[i]) for i, j in itertools.combinations(range(N), 2)])
    d = [sp.Mul(*[(kap[j]+kap[l])/abs(kap[j]-kap[l]) for l in range(N) if l != j]) for j in range(N)]
    ft = 0
    for r in range(0, N+1):
        for S in itertools.combinations(range(N), r):
            ft += sp.Mul(*[c[j]*d[j]*sp.exp(2*kap[j]*x) for j in S]) * sp.Mul(*[((kap[i]-kap[j])/(kap[i]+kap[j]))**2 for i, j in itertools.combinations(S, 2)])
    return kap, phi, W, V0, ft
for N in (2, 3):
    kap, phi, W, V0, ft = build(N)
    mp.mp.dps = 40
    dW = sp.lambdify(x, W - V0*sp.exp(-sum(kap)*x)*ft, 'mpmath')
    sc = sp.lambdify(x, V0*sp.exp(-sum(kap)*x)*ft, 'mpmath')
    worst4 = max(abs(dW(mp.mpf(xx))/sc(mp.mpf(xx))) for xx in ('-3', '-1.5', '-0.4', '0', '0.7', '1.8', '3.2'))
    rep('F4 Wronskiano = V e^{-sum kappa x} f~ (N=%d), max err rel = %s' % (N, mp.nstr(worst4, 3)), worst4 < mp.mpf(10)**-30)
    u = 2*sp.diff(sp.log(ft), x, 2)
    kk = sp.Symbol('k')
    E = sp.exp(sp.I*kk*x)
    WE = sp.Matrix(N+1, N+1, lambda a, b: sp.diff((phi+[E])[b], x, a)).det()
    psi = WE / W
    res = -sp.diff(psi, x, 2) - u*psi - kk**2*psi
    mp.mp.dps = 40
    g = sp.lambdify((x, kk), psi*sp.exp(-sp.I*kk*x), 'mpmath')
    # rev2: F5 con sostituzione esatta (x, k razionali) ed evalf a 60 cifre; lambdify introduceva un errore ~1e-15
    # indipendente dalla precisione (s10b_f4_f5check.out)
    worst = max(abs(sp.N(res.subs({x: sp.Rational(xx), kk: sp.Rational(kv)}), 60)) / abs(sp.N(psi.subs({x: sp.Rational(xx), kk: sp.Rational(kv)}), 60))
                for xx in ('-13/10', '1/5', '21/10') for kv in ('7/10', '19/10'))
    rep('F5 (-D^2-u)psi = k^2 psi (N=%d), max|res|/|psi| = %s' % (N, sp.N(worst, 3)), worst < sp.Rational(1, 10**40))
    kv = mp.mpf('0.9')
    plus = mp.fprod([1j*kv - kk_ for kk_ in [mp.mpf(sp.Rational(q)) for q in kap]])
    minus = mp.fprod([1j*kv + kk_ for kk_ in [mp.mpf(sp.Rational(q)) for q in kap]])
    e1 = abs(g(mp.mpf(40), kv) - plus); e2 = abs(g(mp.mpf(-40), kv) - minus)
    rep('F6 asintotica ai due estremi (N=%d): %s, %s' % (N, mp.nstr(e1, 3), mp.nstr(e2, 3)), e1 < 1e-10 and e2 < 1e-10)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
