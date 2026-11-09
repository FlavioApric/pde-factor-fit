# OP-F5C: certificato esatto della condizione (C_N) per OP-K15.
# Livello k = 0 (f = lam^(2N+1)), coordinate di Mumford s = (u1, v1, u2, v2, ...),
# U = lam^N + sum u_j lam^(N-j), V = sum v_j lam^(N-j); M_0 : U | V^2 + lam^(2N+1).
# Fibra F_N: s_1..s_N fissati ai valori del potenziale costante c = 1
#   (u_j = binom(-1/2, j), v_j = 0). Restano N incognite, N equazioni.
# Si verifica: (i) F_N e' 0-dimensionale di lunghezza 2^N (base di Groebner, monomi standard);
#   (ii) il polinomio caratteristico chi di s_{N+1} su F_N e' squarefree;
#   (iii) chi(s_{N+1}^const) != 0.
# (ii)+(iii) = (C_N) del PROOF_PACKAGE (OPF5C-T3). Aritmetica esatta su Q.
import sympy as sp, sys, time, itertools
lam = sp.Symbol('lam')
def run(N, special=True, seed=1):
    t0 = time.time()
    import random; random.seed(seed)
    a = (N + 1)//2; b = N//2            # u_1..u_a e v_1..v_b fissati (primi N di s)
    us = sp.symbols('u1:%d' % (N+1)); vs = sp.symbols('v1:%d' % (N+1))
    fixed = {}
    for j in range(1, a+1): fixed[us[j-1]] = sp.binomial(sp.Rational(-1, 2), j) if special else sp.Rational(random.randint(-9, 9), random.randint(1, 5))
    for j in range(1, b+1): fixed[vs[j-1]] = sp.Integer(0) if special else sp.Rational(random.randint(-9, 9), random.randint(1, 5))
    U = lam**N + sum(us[j-1]*lam**(N-j) for j in range(1, N+1))
    V = sum(vs[j-1]*lam**(N-j) for j in range(1, N+1))
    U = U.subs(fixed); V = V.subs(fixed)
    r = sp.rem(sp.expand(V**2 + lam**(2*N+1)), sp.expand(U), lam)
    eqs = [e for e in sp.Poly(r, lam).all_coeffs() if e != 0]
    unk = [x for x in list(us)+list(vs) if x not in fixed]
    # s_{N+1}
    if N % 2 == 0:
        sN1 = us[N//2]; cval = sp.binomial(sp.Rational(-1, 2), N//2+1)
    else:
        sN1 = vs[(N+1)//2 - 1]; cval = sp.Integer(0)
    G = sp.groebner(eqs, *unk, order='grevlex')
    lms = [sp.Poly(g, *unk).monoms(order='grevlex')[0] for g in G.exprs]
    # monomi standard (insieme finito se 0-dim)
    def divides(m, e): return all(mi <= ei for mi, ei in zip(m, e))
    # zero-dim: per ogni variabile esiste un LM puro
    zerodim = all(any(all((lm[i] > 0) == (i == v) for i in range(len(unk))) for lm in lms) for v in range(len(unk)))
    std = []
    if zerodim:
        bound = [min(lm[v] for lm in lms if all((lm[i] > 0) == (i == v) for i in range(len(unk)))) for v in range(len(unk))]
        for e in itertools.product(*[range(bd) for bd in bound]):
            if not any(divides(lm, e) for lm in lms): std.append(e)
    dim = len(std)
    idx = {e: i for i, e in enumerate(std)}
    mon = lambda e: sp.Mul(*[x**k for x, k in zip(unk, e)])
    M = sp.zeros(dim, dim)
    for j, e in enumerate(std):
        _, rr = sp.reduced(sp.expand(sN1*mon(e)), G.exprs, *unk, order='grevlex')
        P = sp.Poly(rr, *unk)
        for m, c in zip(P.monoms(), P.coeffs()):
            M[idx[m], j] = c
    z = sp.Symbol('z')
    chi = M.charpoly(z).as_expr()
    chiP = sp.Poly(chi, z)
    sqf = sp.degree(sp.gcd(chiP, chiP.diff(z)), z) == 0
    val = chiP.eval(cval)
    print('[%s] ' % ('fibra speciale (1,0..0)' if special else 'fibra casuale %s' % list(fixed.values())), end='')
    print('N=%d: zero-dim=%s, lunghezza=%d (atteso 2^N=%d), chi squarefree=%s, chi(s_const)=%s (!=0: %s), tempo %.1fs'
          % (N, zerodim, dim, 2**N, sqf, sp.nsimplify(val) if dim < 9 else ('%.6e' % float(val)), val != 0, time.time()-t0))
    if special:
        ok = zerodim and dim == 2**N and val != 0
        print('[STAR_%d] (lunghezza 2^N, chi(s_const) != 0)' % N, 'OK' if ok else 'FAIL')
    else:
        ok = zerodim and dim == 2**N and sqf
        print('[SQF_%d] (lunghezza 2^N, chi squarefree)' % N, 'OK' if ok else 'FAIL')
    sys.stdout.flush()
    return ok
Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
Nmin = int(sys.argv[2]) if len(sys.argv) > 2 else 1
for N in range(Nmin, Nmax+1):
    run(N, special=True)
    run(N, special=False)
