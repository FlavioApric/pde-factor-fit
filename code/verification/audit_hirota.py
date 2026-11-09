# Audit S-CHECK-F10-B: u = 2(log f)_xx con eta_j = k_j x - k_j^3 t + eta_j0 risolve u_t + 6 u u_x + u_xxx = 0 (N = 2, 3), mpmath.
import mpmath as mp, itertools
mp.mp.dps = 40
def make(k, e0):
    N = len(k)
    def f(x, t):
        s = 0
        for r in range(N+1):
            for S in itertools.combinations(range(N), r):
                a = mp.mpf(1)
                for i, j in itertools.combinations(S, 2): a *= ((k[i]-k[j])/(k[i]+k[j]))**2
                s += a*mp.exp(sum(k[i]*x - k[i]**3*t + e0[i] for i in S))
        return s
    return lambda x, t: 2*mp.diff(lambda z: mp.log(f(z, t)), x, 2)
worst = 0
for k, e0 in [((mp.mpf(1), mp.mpf(2)), (0.3, -0.7)), ((mp.mpf('0.8'), mp.mpf('1.7'), mp.mpf('2.9')), (0.1, 0.5, -1.2))]:
    u = make(k, e0)
    for (x, t) in [(-1.3, 0.2), (0.4, -0.5), (2.1, 0.9)]:
        ut = mp.diff(lambda s: u(x, s), t)
        ux = mp.diff(lambda z: u(z, t), x)
        uxxx = mp.diff(lambda z: u(z, t), x, 3)
        r = ut + 6*u(x, t)*ux + uxxx
        worst = max(worst, abs(r))
print(('OK  ' if worst < mp.mpf('1e-15') else 'FAIL') + ' Hirota N=2,3 risolve KdV (+6uu_x), residuo max = %s' % mp.nstr(worst, 3))
