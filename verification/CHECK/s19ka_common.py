import sympy as sp
from itertools import combinations

lam = sp.Symbol('lam')

def ysyms(M):
    return sp.symbols('y0:%d' % M)

def Dj(p, Y):
    # total derivative on jet polynomials
    return sp.expand(sum(sp.diff(p, Y[j]) * Y[j+1] for j in range(len(Y)-1)))

def weight_monomials(w, Y):
    # monomials in Y with wt y_j=j+2 of total weight w
    res = []
    def rec(i, rem, cur):
        if rem == 0:
            res.append(cur); return
        if i >= len(Y): return
        wi = i + 2
        e = 0
        while e*wi <= rem:
            rec(i+1, rem - e*wi, cur * Y[i]**e)
            e += 1
    rec(0, w, sp.Integer(1))
    return res

def gd_polys(n, Y):
    # g_0..g_n , dg_{j+1} = -1/4 (D^3 + 4 u D + 2 u_x) g_j, zero constants
    g = [sp.Integer(1)]
    u = Y[0]
    for j in range(n):
        gj = g[-1]
        rhs = sp.expand(-sp.Rational(1, 4) * (Dj(Dj(Dj(gj, Y), Y), Y) + 4*u*Dj(gj, Y) + 2*Y[1]*gj))
        mons = weight_monomials(2*(j+1), Y)
        cs = sp.symbols('c0:%d' % len(mons))
        ans = sum(c*m for c, m in zip(cs, mons))
        eqs = sp.Poly(Dj(ans, Y) - rhs, *Y).coeffs()
        sol = sp.solve(eqs, cs, dict=True)[0]
        g.append(sp.expand(ans.subs(sol).subs({c: 0 for c in cs})))
    return g

def build_UV(N, k, Y):
    kap = [ki**2/4 for ki in k]
    Ginf = sp.expand(sp.prod([lam + c for c in kap]))
    a = [Ginf.coeff(lam, N-j) for j in range(N+1)]
    g = gd_polys(N, Y)
    Gh = [sp.expand(sum(a[j-i]*g[i] for i in range(j+1))) for j in range(N+1)]
    U = sp.expand(sum(Gh[j]*lam**(N-j) for j in range(N+1)))
    V = sp.expand(sum(Dj(Gh[j], Y)/2*lam**(N-j) for j in range(1, N+1)))
    fk = sp.expand(lam*Ginf**2)
    return U, V, fk, g, Gh

def remainder_coeffs(U, V, fk, N):
    r = sp.rem(sp.expand(V**2 + fk), U, lam)
    r = sp.Poly(r, lam)
    return [sp.expand(r.coeff_monomial(lam**m)) for m in range(N)]
