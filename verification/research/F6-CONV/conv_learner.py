# F6-CONV: verifica (V-ex) della regola "grado minimo" L* (CONV-T1) sul modello M2 (jet in p0=0).
# N_{m,K} = {Q in R_{<=m} : d^beta(Qu)(0)=0 per |beta| <= K-m};  uscita O_K = gcd(N_{m*,K}), m* = min{m : N_{m,K} != 0}.
import sympy as sp
t, x, s, tau, xi = sp.symbols('t x s tau xi')

def jets(u, K):
    ser = sp.series(u.subs({t: s*t, x: s*x}), s, 0, K+1).removeO()
    poly = sp.Poly(sp.expand(ser.subs(s, 1)), t, x)
    D = {}
    for a in range(K+1):
        for b in range(K+1-a):
            D[(a, b)] = poly.coeff_monomial(t**a*x**b)*sp.factorial(a)*sp.factorial(b)
    return D

def N_mK(D, m, K):
    mons = [(i, j) for i in range(m+1) for j in range(m+1-i)]
    rows = []
    for a in range(K-m+1):
        for b in range(K-m+1-a):
            rows.append([D[(a+i, b+j)] for (i, j) in mons])
    if not rows:
        return mons, [sp.eye(len(mons)).col(k) for k in range(len(mons))]
    return mons, sp.Matrix(rows).nullspace()

def learner(u, K, mmax=4):
    D = jets(u, K)
    for m in range(0, mmax+1):
        mons, ns = N_mK(D, m, K)
        if ns:
            polys = [sp.expand(sum(v[k]*tau**i*xi**j for k, (i, j) in enumerate(mons))) for v in ns]
            g = polys[0]
            for p in polys[1:]:
                g = sp.gcd(g, p)
            return m, len(ns), sp.factor(g)
    return None, 0, 'nessun Q di grado <= %d' % mmax

def run(name, u, Ks, mmax=4):
    print('==', name)
    for K in Ks:
        print('  K=%2d ->' % K, learner(u, K, mmax))

N = 3
run('(a) u=1+x^(N+2)e^{x^2}, N=3 (Ann=(tau); tasso non uniforme: uscita giusta solo da K>=N+3)',
    1 + x**(N+2)*sp.exp(x**2), range(2, 9), mmax=1)
run('(b) u=(t+1)/((t+1)^2+x^2) armonica (attesa tau^2+xi^2)', (t+1)/((t+1)**2+x**2), [3, 5, 7, 9])
run('(c) calore, 3 modi sum e^{-k^2 t}cos(kx) (attesa tau-xi^2 come elemento di grado minimo)',
    sum(sp.exp(-k**2*t)*sp.cos(k*x) for k in (1, 2, 3)), [4, 6, 8, 10])
run('(d) u=exp(t^2+x^2), Ann=0 (atteso: nessun Q di grado <=3, grado minimo -> infinito)',
    sp.exp(t**2+x**2), [6, 8, 10], mmax=3)
