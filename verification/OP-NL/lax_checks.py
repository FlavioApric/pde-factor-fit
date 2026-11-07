"""OP-NL: Lax / zero-curvature identities used in PROOF_PACKAGE.md §4 (INT-T1(C=>), INT-T2(=>)).
KdV (u_t + 6 u u_x + u_xxx = 0, L = -d^2 - u): for n = 0..3 there is B_n = d^{2n+1} + lower, with coefficients
differential polynomials in u WITHOUT constant term, such that [B_n, L] = multiplication by c_n K_n[u],
c_n != 0, K_n the hierarchy of S4-INTEG (K_{n+1} = R K_n, R = d^2 + 4u + 2u_x d^{-1}).
NLS (AKNS U = [[-i z, q],[r, i z]]): for n = 0..3 there is V_n(z) = sum_m z^m V_{n,m}, V_n -> v_n z^n diag(-i,i)
(+ lower constant diagonal = 0) as q,r -> 0, with  U_t - V_x + [U,V] = 0  <=>  q_t = T_n, r_t = T_n^*.
Identities are checked for an ARBITRARY smooth u (resp. q, r): for these n they are proofs by computation."""
import sympy as sp
from itertools import combinations_with_replacement

x = sp.Symbol('x')
ok = 0
tot = 0


def report(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name, info, flush=True)


# ---------------- KdV ----------------
u = sp.Function('u')(x)
phi = sp.Function('phi')(x)


def L(f):
    return -sp.diff(f, x, 2) - u * f


def diff_monomials(weight, fn):
    """differential monomials in fn of total weight `weight` (wt fn = 2, wt d = 1), as sympy exprs"""
    out = []
    # partitions of weight into parts >= 2 (each part = 2 + derivative order)
    def parts(w, mx):
        if w == 0:
            yield []
            return
        for p in range(min(w, mx), 1, -1):
            for rest in parts(w - p, p):
                yield [p] + rest
    for pr in parts(weight, weight):
        e = sp.Integer(1)
        for p in pr:
            e *= sp.diff(fn, x, p - 2)
        out.append(e)
    return out


# hierarchy K_n by recursion: K_0 = -u_x, K_{n+1} = R K_n with d^{-1} via ansatz (exact derivative)
def antideriv(expr, weight):
    """find total-derivative primitive of expr among differential monomials of given weight"""
    mons = diff_monomials(weight, u)
    cs = sp.symbols('c0:%d' % len(mons))
    cand = sum(c * m for c, m in zip(cs, mons))
    eq = sp.expand(sp.diff(cand, x) - expr)
    # collect over derivatives of u
    derivs = [sp.diff(u, x, k) for k in range(weight + 3)]
    syms = sp.symbols('D0:%d' % len(derivs))
    eqs = sp.expand(eq.subs({derivs[k]: syms[k] for k in reversed(range(len(derivs)))}))
    sol = sp.solve(sp.Poly(eqs, *syms).coeffs(), cs, dict=True)
    assert sol, "no primitive"
    return cand.subs(sol[0]).subs({c: 0 for c in cs})


K = [-sp.diff(u, x)]
for n in range(3):
    Kn = K[-1]
    wt = 2 * n + 3  # weight of K_n (u has weight 2, K_n ~ d^{2n+1} u)
    prim = antideriv(Kn, wt - 1)
    K.append(sp.expand(sp.diff(Kn, x, 2) + 4 * u * Kn + 2 * sp.diff(u, x) * prim))
report("K_1 = -(u_xxx + 6 u u_x)", sp.expand(K[1] + sp.diff(u, x, 3) + 6 * u * sp.diff(u, x)) == 0)


def subs_syms(e, maxk):
    derivs = [sp.diff(u, x, k) for k in range(maxk)]
    pd = [sp.diff(phi, x, k) for k in range(maxk)]
    S = sp.symbols('U0:%d' % maxk)
    T = sp.symbols('P0:%d' % maxk)
    rep = {}
    for k in reversed(range(maxk)):
        rep[derivs[k]] = S[k]
        rep[pd[k]] = T[k]
    return sp.expand(e.subs(rep)), S, T


for n in range(4):
    order = 2 * n + 1
    unknowns = []
    coeffs = []
    for j in range(order - 1):  # b_j d^j, j = 0..2n-1 (no d^{2n} term)
        mons = diff_monomials(order - j, u)
        cs = sp.symbols('b%d_0:%d' % (j, len(mons))) if mons else ()
        unknowns += list(cs)
        coeffs.append(sum((c * m for c, m in zip(cs, mons)), sp.Integer(0)))
    cK = sp.Symbol('cK')
    def B(f):
        return sp.diff(f, x, order) + sum(coeffs[j] * sp.diff(f, x, j) for j in range(order - 1))
    comm = B(L(phi)) - L(B(phi)) - cK * K[n] * phi
    e, S, T = subs_syms(comm, 2 * order + 4)
    eqs = sp.Poly(e, *(list(S) + list(T))).coeffs()
    sol = sp.solve(eqs, unknowns + [cK], dict=True)
    good = bool(sol) and sol[0].get(cK, 0) != 0
    report("KdV: exists B_%d = d^%d + lower (no constant terms) with [B,L] = c K_%d, c != 0" % (n, order, n), good,
           "(c = %s)" % (sol[0].get(cK) if sol else None))

# ---------------- NLS / AKNS ----------------
z = sp.Symbol('z')
q = sp.Function('q')(x)
r = sp.Function('r')(x)
# flows of INT-T2 (componentwise, r = -conj(q)): T_0 = i q, T_1 = q_x, T_2 = i(q_xx - 2 q^2 r), T_3 = -(q_xxx - 6 q r q_x)
T = [sp.I * q, sp.diff(q, x), sp.I * (sp.diff(q, x, 2) - 2 * q ** 2 * r), -(sp.diff(q, x, 3) - 6 * q * r * sp.diff(q, x))]
Tr = [-sp.I * r, sp.diff(r, x), -sp.I * (sp.diff(r, x, 2) - 2 * r ** 2 * q), -(sp.diff(r, x, 3) - 6 * q * r * sp.diff(r, x))]
U = sp.Matrix([[-sp.I * z, q], [r, sp.I * z]])


def qr_monomials(weight):
    """monomials in q, r and derivatives, total weight (wt q = wt r = 1, d = 1)"""
    gens = []
    for k in range(weight):
        gens += [(sp.diff(q, x, k), k + 1), (sp.diff(r, x, k), k + 1)]
    out = []
    def rec(i, w, cur):
        if w == 0:
            out.append(cur)
            return
        for j in range(i, len(gens)):
            g, gw = gens[j]
            if gw <= w:
                rec(j, w - gw, cur * g)
    rec(0, weight, sp.Integer(1))
    return out


for n in range(4):
    unknowns = []
    V = sp.zeros(2, 2)
    for m in range(n + 1):
        wt = n - m  # coefficient of z^m has weight n - m
        for (a, b) in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            if wt == 0:
                if (a, b) in [(0, 0), (1, 1)]:
                    c = sp.Symbol('v%d_%d%d' % (m, a, b))
                    unknowns.append(c)
                    V[a, b] += c * z ** m
                continue
            mons = qr_monomials(wt)
            cs = sp.symbols('v%d_%d%d_0:%d' % (m, a, b, len(mons)))
            unknowns += list(cs)
            V[a, b] += sum(c * mm for c, mm in zip(cs, mons)) * z ** m
    Ut = sp.Matrix([[0, T[n]], [Tr[n], 0]])
    ZC = Ut - V.diff(x) + U * V - V * U
    eqs = []
    maxk = n + 4
    S = sp.symbols('Q0:%d' % maxk)
    R_ = sp.symbols('R0:%d' % maxk)
    rep = {}
    for k in reversed(range(maxk)):
        rep[sp.diff(q, x, k)] = S[k]
        rep[sp.diff(r, x, k)] = R_[k]
    for ent in ZC:
        e = sp.expand(ent.subs(rep))
        if e != 0:
            eqs += sp.Poly(e, *(list(S) + list(R_) + [z])).coeffs()
    sol = sp.solve(eqs, unknowns, dict=True)
    good = False
    info = ""
    if sol:
        Vs = V.subs(sol[0])
        free = [s for s in unknowns if s not in sol[0]]
        Vs = Vs.subs({s: 0 for s in free})
        V0 = sp.simplify(Vs.subs({q: 0, r: 0}).doit())
        lead = sp.expand(V0[0, 0])
        # V is defined up to adding scalar multiples of I (they commute with U): test the traceless part
        good = sp.simplify(V0[0, 1]) == 0 and sp.simplify(V0[1, 0]) == 0 and sp.Poly(sp.expand(V0[0, 0] - V0[1, 1]), z).degree() == n and sp.expand((V0[0, 0] - V0[1, 1]) - sp.Poly(sp.expand(V0[0, 0] - V0[1, 1]), z).LC() * z ** n) == 0
        info = "(V at q=r=0: diag(%s, %s))" % (V0[0, 0], V0[1, 1])
    report("NLS: zero-curvature V_%d exists, traceless part of V at q=r=0 = c z^%d diag(1,-1)" % (n, n), good, info)

print("TOTAL %d/%d OK" % (ok, tot))
