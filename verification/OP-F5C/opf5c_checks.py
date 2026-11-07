# OP-F5C: controlli SymPy (solo controllo) dei lemmi di OPF5C-T1..T3 e delle costruzioni di OPF5C-P5.
import sympy as sp, pickle, random, itertools, sys
lam = sp.Symbol('lam')
ok_all = True
def rep(tag, ok):
    global ok_all
    ok_all &= bool(ok); print('[%s]' % tag, 'OK' if ok else 'FAIL'); sys.stdout.flush()
# (E1) identita' dei coefficienti usata in (STAR): e_{N+2} + e_{N+1}/2 = -t_{N+1}/(N+2) != 0,
#      con T_N = troncamento di (1+x)^(-1/2), T_N^2 (1+x) = 1 + sum_{j>N} e_j x^j.
x = sp.Symbol('x')
ok = True
for N in range(1, 13):
    t = [sp.binomial(sp.Rational(-1, 2), j) for j in range(N+3)]
    TN = sum(t[j]*x**j for j in range(N+1))
    E = sp.Poly(sp.expand(TN**2*(1+x)), x)
    e = lambda j: E.coeff_monomial(x**j)
    ok &= all(e(j) == 0 for j in range(1, N+1)) and e(0) == 1
    ok &= sp.simplify(e(N+2) + e(N+1)/2 + t[N+1]/(N+2)) == 0 and t[N+1] != 0
rep('E1 e_{N+2}+e_{N+1}/2 = -t_{N+1}/(N+2) != 0, N<=12', ok)
# (E2) verifica diretta di (STAR) per N <= 6 con c simbolico: nessun (U,V) in M_0 con s_1..s_{N+1} del potenziale costante.
c = sp.Symbol('c')
ok = True
for N in range(1, 7):
    a1 = (N+2)//2; b1 = (N+1)//2       # numero di u e di v fissati tra s_1..s_{N+1}
    us = sp.symbols('u1:%d' % (N+1)); vs = sp.symbols('v1:%d' % (N+1))
    fix = {us[j-1]: sp.binomial(sp.Rational(-1, 2), j)*c**j for j in range(1, a1+1)}
    fix.update({vs[j-1]: 0 for j in range(1, b1+1)})
    U = (lam**N + sum(us[j-1]*lam**(N-j) for j in range(1, N+1))).subs(fix)
    V = sum(vs[j-1]*lam**(N-j) for j in range(1, N+1)).subs(fix)
    r = sp.rem(sp.expand(V**2 + lam**(2*N+1)), sp.expand(U), lam)
    eqs = [q for q in sp.Poly(r, lam).all_coeffs() if q != 0]
    unk = [z for z in list(us)+list(vs) if z not in fix]
    G = sp.groebner(eqs + [c*sp.Symbol('w') - 1], *(unk + [sp.Symbol('w'), c]), order='grevlex') if unk else sp.groebner(eqs + [c*sp.Symbol('w') - 1], sp.Symbol('w'), c, order='grevlex')
    ok &= (G.exprs == [1])
rep('E2 (STAR) diretta: sistema incompatibile con c != 0, N<=6', ok)
# (E3) rango di Bezout pesato: fibra di Z_k su un punto casuale (k generico) ha lunghezza 2^N (N = 2, 3).
def fibre_len(N, kap, base):
    us = sp.symbols('u1:%d' % (N+1)); vs = sp.symbols('v1:%d' % (N+1))
    seq = []
    for j in range(N): seq += [us[j], vs[j]]
    fix = dict(zip(seq[:N], base))
    U = (lam**N + sum(us[j-1]*lam**(N-j) for j in range(1, N+1))).subs(fix)
    V = sum(vs[j-1]*lam**(N-j) for j in range(1, N+1)).subs(fix)
    f = lam*sp.Mul(*[(lam+q)**2 for q in kap])
    r = sp.rem(sp.expand(V**2 + f), sp.expand(U), lam)
    eqs = [q for q in sp.Poly(r, lam).all_coeffs() if q != 0]
    unk = [z for z in seq if z not in fix]
    G = sp.groebner(eqs, *unk, order='grevlex')
    lms = [sp.Poly(gg, *unk).monoms(order='grevlex')[0] for gg in G.exprs]
    bound = []
    for v in range(len(unk)):
        pure = [lm[v] for lm in lms if all((lm[i] > 0) == (i == v) for i in range(len(unk)))]
        if not pure: return None
        bound.append(min(pure))
    cnt = 0
    for e in itertools.product(*[range(bd) for bd in bound]):
        if not any(all(m <= q for m, q in zip(lm, e)) for lm in lms): cnt += 1
    return cnt
random.seed(5)
ok = True
for N, kap in [(2, [sp.Rational(1, 4), 1]), (3, [sp.Rational(1, 4), 1, 4])]:
    base = [sp.Rational(random.randint(-7, 7), random.randint(1, 4)) for _ in range(N)]
    L = fibre_len(N, kap, base)
    print('   N=%d kappa=%s base(s_1..s_N)=%s: lunghezza fibra = %s (atteso %d)' % (N, kap, base, L, 2**N))
    ok &= (L == 2**N)
rep('E3 lunghezza della fibra = 2^N (k generico)', ok)
# (E4) costruzioni di OPF5C-P5: coefficiente di v_N in r_m (m>=1) = 2 v_{N-m}; D := v_1 r_{N-2} - v_2 r_{N-1} non dipende da v_N, e' != 0;
#      pesi: r_{N-1} peso 2N+4, D peso 2N+9 (in (k, y)); gradi in y: <= N+2, <= N+4.
g = [sp.sympify(s) for s in pickle.load(open('opf5c_gd.pkl', 'rb'))]
Y = sp.symbols('y0:%d' % 40)
def Dop(e, top): return sp.expand(sum(sp.diff(e, Y[m])*Y[m+1] for m in range(top)))
ok = True
for N in [2, 3, 4]:
    ks = sp.symbols('k1:%d' % (N+1)); kap = [kk**2/4 for kk in ks]
    us = sp.symbols('u1:%d' % (N+1)); vs = sp.symbols('v1:%d' % (N+1))
    U = lam**N + sum(us[j-1]*lam**(N-j) for j in range(1, N+1))
    V = sum(vs[j-1]*lam**(N-j) for j in range(1, N+1))
    f = lam*sp.Mul(*[(lam+q)**2 for q in kap])
    r = sp.Poly(sp.rem(sp.expand(V**2 + f), sp.expand(U), lam), lam)
    rm = lambda m: sp.expand(r.coeff_monomial(lam**m))
    for m in range(1, N):
        ok &= sp.expand(sp.diff(rm(m), vs[N-1]) - 2*vs[N-m-1]) == 0
    # passaggio alle coordinate y
    Ginf = sp.Poly(sp.Mul(*[(lam+q) for q in kap]), lam)
    a = [Ginf.coeff_monomial(lam**(N-j)) for j in range(N+1)]
    sub = {}
    for j in range(1, N+1):
        Gh = sp.expand(sum(a[j-i]*g[i] for i in range(j+1)))
        sub[us[j-1]] = Gh; sub[vs[j-1]] = sp.expand(Dop(Gh, 2*N)/2)
    F = sp.expand(rm(N-1).subs(sub))
    degF = sp.Poly(F, *Y[:2*N]).total_degree()
    print('   N=%d: deg_y r_{N-1} = %d (limite N+2 = %d), contiene y_{2N-1}: %s' % (N, degF, N+2, sp.diff(F, Y[2*N-1]) != 0))
    ok &= degF <= N+2 and F != 0
    if N >= 3:
        Dd = sp.expand(vs[0]*rm(N-2) - vs[1]*rm(N-1))
        ok &= sp.diff(Dd, vs[N-1]) == 0 and Dd != 0
        Dy = sp.expand(Dd.subs(sub))
        degD = sp.Poly(Dy, *Y[:2*N]).total_degree()
        noy = sp.diff(Dy, Y[2*N-1]) == 0
        print('   N=%d: D libero da v_N: %s; deg_y D = %d (limite N+4 = %d); D in C[y_0..y_{2N-2}]: %s' % (N, sp.diff(Dd, vs[N-1]) == 0, degD, N+4, noy))
        ok &= degD <= N+4 and noy and Dy != 0
rep('E4 costruzioni r_{N-1} (grado <= N+2) e D (grado <= N+4, senza y_{2N-1})', ok)
print('TOTALE:', 'OK' if ok_all else 'FAIL')
