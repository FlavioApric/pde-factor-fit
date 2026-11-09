# OP-F5C: verifica (V-ex) che l'N-solitone formale soddisfa 2GG''-G'^2+4(u+lam)G^2 = 4 lam G_inf(lam)^2
# (=> U | V^2 - R, R = -lam G_inf^2), con G = sum_j Ghat_j lam^(N-j), Ghat_j = sum_i a_{j-i} g_i, a_j = e_j(k_i^2/4).
import sympy as sp, pickle, itertools, sys
g = [sp.sympify(s) for s in pickle.load(open('opf5c_gd.pkl','rb'))]
y = sp.symbols('y0:%d' % 40)
lam = sp.Symbol('lam')
def check(ks, seed=0):
    N = len(ks)
    X = sp.symbols('X1:%d' % (N+1))
    A = {}
    f = 0
    for r in range(N+1):
        for S in itertools.combinations(range(N), r):
            aS = sp.Integer(1)
            for i, j in itertools.combinations(S, 2):
                aS *= sp.Rational(ks[i]-ks[j], ks[i]+ks[j])**2
            f += aS*sp.Mul(*[X[i] for i in S])
    def Dx(e):
        return sum(sp.diff(e, X[i])*ks[i]*X[i] for i in range(N))
    # punto numerico razionale (verifica esatta in un punto generico) + simbolico per N<=2
    u = 2*Dx(Dx(sp.log(f)))
    jets = [sp.together(u)]
    for j in range(2*N+3):
        jets.append(sp.together(Dx(jets[-1])))
    # valutazione esatta in punti razionali
    import random
    random.seed(seed)
    a = [sp.Integer(1)]
    kk = [sp.Rational(k)**2/4 for k in ks]
    Ginf = sp.expand(sp.Mul(*[(lam + q) for q in kk]))
    a = [Ginf.coeff(lam, N-j) for j in range(N+1)]
    ok = True
    for trial in range(3):
        pt = {X[i]: sp.Rational(random.randint(1, 9), random.randint(1, 9)) for i in range(N)}
        jv = {y[j]: jets[j].subs(pt) for j in range(2*N+3)}
        Gh = [sp.expand(sum(a[jj-i]*g[i] for i in range(jj+1)).subs(jv)) for jj in range(N+1)]
        Gp = [sp.expand(D1) for D1 in [sum(a[jj-i]*sum(sp.diff(g[i], y[m])*y[m+1] for m in range(2*N+1)) for i in range(jj+1)).subs(jv) for jj in range(N+1)]]
        Gpp_expr = []
        for jj in range(N+1):
            e = sum(a[jj-i]*g[i] for i in range(jj+1))
            e1 = sum(sp.diff(e, y[m])*y[m+1] for m in range(2*N+1))
            e2 = sum(sp.diff(e1, y[m])*y[m+1] for m in range(2*N+2))
            Gpp_expr.append(sp.expand(e2.subs(jv)))
        G = sum(Gh[jj]*lam**(N-jj) for jj in range(N+1))
        G1 = sum(Gp[jj]*lam**(N-jj) for jj in range(N+1))
        G2 = sum(Gpp_expr[jj]*lam**(N-jj) for jj in range(N+1))
        C = sp.expand(2*G*G2 - G1**2 + 4*(jv[y[0]] + lam)*G**2)
        ok &= sp.expand(C - 4*lam*Ginf**2) == 0
    return ok
for ks in [(1,), (3,), (1,2), (1,3), (2,5), (1,2,4), (1,3,7), (1,2,3,5)]:
    print('[NOV] k =', ks, ':', 'OK' if check(ks) else 'FAIL'); sys.stdout.flush()
