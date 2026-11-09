# S-CHECK-F10-B2 . controlli per S10B-P11 e per l'ipotesi (L-int).
# (a) identita' algebrica del termine alpha = 0 nella prova di P11, su un modello discreto:
#     ||sum_j chi f_j||^2 = sum_j ||chi f_j||^2 - <K0 f, f>,  (K0 f)_i = - sum_{j != i} P_i chi^2 P_j f_j .
# (b) (L-int) per trasporti con d_j = 0 sul triangolo T = {x, y > 0, x + y < 1}: norma di Hilbert-Schmidt di
#     P_i chi_0^2 P_j. Formula dell'audit: HS^2 = int_T chi_0^4 / (|sin th_ij| l_i(x) l_j(x)) dx, con l_i(x) la
#     lunghezza della corda per x in direzione n_i. Con chi_0 = indicatrice di {dist(x, vertici) > r}:
#     HS^2(r) finita per ogni r > 0 e ~ C log(1/r) per r -> 0 (la non compattezza sta solo ai vertici).
#     Controllo incrociato con proiettori discreti (medie su bande di corde).
import numpy as np
rng = np.random.default_rng(7)
ok = []
def rep(name, c):
    ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
# (a)
M, N = 60, 3
Ps = []
for j in range(N):
    Q, _ = np.linalg.qr(rng.standard_normal((M, 12))); Ps.append(Q @ Q.T)
chi2 = rng.uniform(0, 1, M)
worst = 0
for _ in range(20):
    f = [P @ rng.standard_normal(M) for P in Ps]
    lhs = np.sum((np.sqrt(chi2)*sum(f))**2)
    K0f = [-sum(Ps[i] @ (chi2*f[j]) for j in range(N) if j != i) for i in range(N)]
    rhs = sum(np.sum(chi2*fj**2) for fj in f) - sum(K0f[i] @ f[i] for i in range(N))
    worst = max(worst, abs(lhs - rhs)/lhs)
rep('(a) identita del termine alpha = 0 (errore relativo %.1e)' % worst, worst < 1e-12)
# (b)
V = np.array([[0., 0.], [1., 0.], [0., 1.]])
dirs = [np.array([1., 0.]), np.array([0., 1.]), np.array([1., 2.])/np.sqrt(5)]
def chord(p, e):
    # lunghezza della corda di T per i punti p (array n x 2) in direzione e
    lo = np.full(len(p), -np.inf); hi = np.full(len(p), np.inf)
    for (a, b, c) in [((1, 0), 0, 1), ((0, 1), 0, 1), ((-1, -1), -1, 1)]:   # a.x >= b
        a = np.array(a, float); ae = a @ e; ap = p @ a
        with np.errstate(divide='ignore', invalid='ignore'):
            s = (b - ap)/ae
        lo = np.where(ae > 0, np.maximum(lo, s), lo); hi = np.where(ae < 0, np.minimum(hi, s), hi)
    return hi - lo
def sample(n):
    u = rng.uniform(0, 1, (n, 2)); m = u.sum(1) > 1; u[m] = 1 - u[m]; return u
def hs2_integral(i, j, r, n=4_000_000):
    p = sample(n); d = np.min(np.linalg.norm(p[:, None, :] - V[None], axis=2), axis=1)
    chi = (d > r).astype(float)
    s = abs(dirs[i][0]*dirs[j][1] - dirs[i][1]*dirs[j][0])
    return 0.5*np.mean(chi/(s*chord(p, dirs[i])*chord(p, dirs[j])))
def hs2_discrete(i, j, r, nb=400, n=4_000_000):
    # proiettori discreti: medie di Monte Carlo sulle bande sottili di corde (nb bande per direzione)
    p = sample(n); d = np.min(np.linalg.norm(p[:, None, :] - V[None], axis=2), axis=1)
    chi2 = (d > r).astype(float)
    def band(e):
        sperp = p @ np.array([-e[1], e[0]]); edges = np.linspace(sperp.min(), sperp.max(), nb+1)
        return np.clip(np.digitize(sperp, edges) - 1, 0, nb-1)
    bi, bj = band(dirs[i]), band(dirs[j])
    ni = np.bincount(bi, minlength=nb).astype(float); nj = np.bincount(bj, minlength=nb).astype(float)
    Cij = np.zeros((nb, nb)); np.add.at(Cij, (bi, bj), chi2)
    with np.errstate(divide='ignore', invalid='ignore'):
        Hm = np.where((ni[:, None] > 0) & (nj[None] > 0), Cij**2/(ni[:, None]*nj[None]), 0.)
    return Hm.sum()
for (i, j) in [(0, 1), (0, 2), (1, 2)]:
    vals = [(r, hs2_integral(i, j, r)) for r in (0.2, 0.1, 0.05, 0.025, 0.0125)]
    incr = [vals[m+1][1] - vals[m][1] for m in range(len(vals)-1)]
    print('   (i,j)=(%d,%d) HS^2(r):' % (i, j), ', '.join('r=%.4g: %.3f' % v for v in vals))
    print('            incrementi per dimezzamento di r:', ', '.join('%.3f' % d for d in incr))
    # per (0,1) entrambe le direzioni sono parallele a lati del triangolo: a ogni vertice al piu' una delle due
    # corde degenera, e HS^2(r) converge per r -> 0 (incrementi dimezzati); per (0,2), (1,2) c'e' un vertice in cui
    # degenerano entrambe e la crescita e' logaritmica (incrementi quasi costanti).
    if (i, j) == (0, 1):
        crit = all(incr[m+1] < 0.6*incr[m] for m in range(len(incr)-1))
        lab = 'convergente per r -> 0 (nessun vertice con due corde degeneri)'
    else:
        crit = max(incr[1:])/min(incr[1:]) < 1.25
        lab = 'crescita ~ log(1/r) (incrementi quasi costanti)'
    rep('(b) (i,j)=(%d,%d): HS^2(r) finita per ogni r > 0, %s' % (i, j, lab),
        all(np.isfinite(v[1]) for v in vals) and crit)
    hd = hs2_discrete(i, j, 0.1)
    rep('(b) (i,j)=(%d,%d), r = 0.1: HS^2 discreto %.3f vs formula %.3f' % (i, j, hd, vals[1][1]),
        abs(hd - vals[1][1])/vals[1][1] < 0.1)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
