# S8-CONV: verifica di CONV-L1/T1 (regola del grado minimo L*, modello DM2) e del passo (ii) di CONV-T2.
# Solo verifica su esempi (V-ex), aritmetica esatta.
import sympy as sp
t, x, s, tau, xi = sp.symbols('t x s tau xi')
ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name)

def jets(u, K):
    ser = sp.series(u.subs({t: s*t, x: s*x}), s, 0, K+1).removeO()
    poly = sp.Poly(sp.expand(ser.subs(s, 1)), t, x)
    return {(a, b): poly.coeff_monomial(t**a*x**b)*sp.factorial(a)*sp.factorial(b)
            for a in range(K+1) for b in range(K+1-a)}

def mons(m): return [(i, j) for i in range(m+1) for j in range(m+1-i)]
def M_mK(D, m, K, rowmin=-1):
    rows = [[D[(a+i, b+j)] for (i, j) in mons(m)]
            for a in range(K-m+1) for b in range(K-m+1-a) if a + b > rowmin]
    return sp.Matrix(rows) if rows else sp.zeros(0, len(mons(m)))
def N_mK(D, m, K):
    M = M_mK(D, m, K)
    return M.nullspace() if M.rows else [sp.eye(len(mons(m))).col(k) for k in range(len(mons(m)))]
def learner(D, K, mmax):
    for m in range(0, min(K, mmax)+1):
        ns = N_mK(D, m, K)
        if ns:
            ps = [sp.expand(sum(v[k]*tau**i*xi**j for k, (i, j) in enumerate(mons(m)))) for v in ns]
            g = ps[0]
            for p in ps[1:]:
                g = sp.gcd(g, p)
            g = sp.factor(g)
            lc = sp.Poly(g, tau, xi).coeffs()[0] if g.free_symbols else g
            return (m, sp.factor(g/lc))
    return ('inf', None)

# T1(6): u = 1 + x^(N+2) e^{x^2}: Ann = (tau), K* = N+2
for N in (2, 3, 4):
    u = 1 + x**(N+2)*sp.exp(x**2)
    Kmax = N + 5
    D = jets(u, Kmax)
    outs = [(K, learner({k: v for k, v in D.items() if sum(k) <= K}, K, 1)) for K in range(1, Kmax+1)]
    first = min(K for K, o in outs if o == (1, tau) and all(o2 == (1, tau) for K2, o2 in outs if K2 >= K))
    print('  N=%d uscite:' % N, outs)
    check('T1(6) N=%d: uscita tau esattamente da K = N+2 = %d' % (N, N+2), first == N + 2)
    distinct = len(set(o for K, o in outs))
    check('T1(5) N=%d: uscite distinte %d <= (d+1)(d+2)/2 = 3' % (N, distinct), distinct <= 3)

# armonica (Poisson): Ann = (tau^2+xi^2), d = 2
u = (t+1)/((t+1)**2 + x**2)
D = jets(u, 9)
outs = [learner({k: v for k, v in D.items() if sum(k) <= K}, K, 2) for K in range(1, 10)]
print('  Poisson:', outs)
check('T1(2) armonica: uscita tau^2+xi^2 da un K finito in poi', all(o == (2, sp.expand(tau**2 + xi**2)) for o in outs[-3:]))
check('T1(5) armonica: uscite distinte <= 6', len(set(outs)) <= 6)
# monotonia di m*
check('T1(5) m* non decrescente (armonica)', all((outs[i][0] if outs[i][0] != 'inf' else 99) <= (outs[i+1][0] if outs[i+1][0] != 'inf' else 99) for i in range(len(outs)-1)))

# CONV-T2 passo (ii): g = (t^2+x^2)^{L+1} e^{t^2+x^2}; righe |beta| > L di M_{m,K}(g) hanno rango pieno da un K0 in poi
for L in (0, 1):
    g = (t**2 + x**2)**(L+1)*sp.exp(t**2 + x**2)
    for m in (1, 2):
        Kmax = 2*L + m + 9
        D = jets(g, Kmax)
        K0 = None
        for K in range(m + L + 1, Kmax + 1):
            Dk = {k: v for k, v in D.items() if sum(k) <= K}
            M = M_mK(Dk, m, K, rowmin=L)
            if M.rows and M.rank() == len(mons(m)):
                K0 = K; break
        check('T2(ii) L=%d m=%d: rango pieno %d raggiunto a K0=%s' % (L, m, len(mons(m)), K0), K0 is not None)
        # le righe |beta|>L non vedono un polinomio p di grado <= L
        p = 3 + 2*t - x if L >= 1 else sp.Integer(5)
        Dp = jets(p + g, K0)
        check('T2(ii) L=%d m=%d: righe |beta|>L di p+g = righe di g' % (L, m), M_mK(Dp, m, K0, rowmin=L) == M_mK({k: v for k, v in D.items() if sum(k) <= K0}, m, K0, rowmin=L))
# Ann(g) = 0 fino al grado 3 (controllo): nessun Q di grado <= 3 nel nucleo a K grande
Dg = jets(sp.exp(t**2 + x**2)*(t**2+x**2), 12)
check('Ann(g) cap R_{<=3} = 0 (K=12)', all(not N_mK(Dg, m, 12) for m in range(0, 4)))
print('ESITO:', 'TUTTI PASS' if ok else 'QUALCHE FAIL')
