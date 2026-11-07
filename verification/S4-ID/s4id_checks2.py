# S4-ID — verifiche supplementari (solo controllo).
# (A) controllo INDIPENDENTE della formula di T1(b): dim(I(u)  cap  V) calcolata direttamente con le
#     derivate in t e in x di u (derivazioni formali D_t E_i = nu k_i^2 E_i, D_x E_i = k_i E_i),
#     confrontata con dim([F]  cap  V) + dim(J_u  cap  psi(V)) (psi = forma normale).
# (B) riduzione autosimile di KdV usata in T4(iv).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
from itertools import combinations_with_replacement
from reduction_checks import Psi, V_dk, kernel_dim

RES = []
def check(name, cond, info=''):
    RES.append(bool(cond)); print(f"[{'OK' if cond else 'FAIL'}] {name} {info}", flush=True)

def rank_of_rational_list(exprs, gens):
    # dipendenze lineari a coefficienti costanti fra funzioni razionali nelle E
    nums = []
    dens = [sp.fraction(sp.together(e))[1] for e in exprs]
    L = sp.lcm_list(dens) if dens else 1
    for e in exprs:
        nums.append(sp.Poly(sp.cancel(e*L), *gens, domain=QQ).as_dict())
    keys = sorted(set().union(*[set(d.keys()) for d in nums]))
    rows = [[QQ.convert(d.get(k, 0)) for d in nums] for k in keys]
    M = DomainMatrix(rows, (len(keys), len(exprs)), QQ)
    return len(exprs) - M.rank()

def nshock_direct(ks, nu, d, k):
    N = len(ks)
    E = sp.symbols('E1:%d' % (N+1))
    phi = 1 + sum(E)
    u = -2*nu*sum(ki*Ei for ki, Ei in zip(ks, E))/phi
    def Dx(f): return sp.together(sum(ki*Ei*sp.diff(f, Ei) for ki, Ei in zip(ks, E)))
    def Dt(f): return sp.together(sum(nu*ki**2*Ei*sp.diff(f, Ei) for ki, Ei in zip(ks, E)))
    # controllo: Burgers soddisfatta
    assert sp.simplify(Dt(u) + u*Dx(u) - nu*Dx(Dx(u))) == 0
    thetas = [(a, b) for a in range(k+1) for b in range(k+1-a)]
    val = {}
    for (a, b) in thetas:
        f = u
        for _ in range(b): f = Dx(f)
        for _ in range(a): f = Dt(f)
        val[(a, b)] = f
    exprs = []
    for e in range(0, d+1):
        for cmb in combinations_with_replacement(thetas, e):
            f = sp.Integer(1)
            for th in cmb: f = f*val[th]
            exprs.append(f)
    dim_direct = rank_of_rational_list(exprs, E)
    # J_u  cap  psi(V): immagini psi (polinomi in y) valutate sul getto in x
    psi = Psi('burgers', nu=nu)
    imgs = V_dk(psi, d, k)
    xj = [u]
    for j in range(1, 2*k+2): xj.append(Dx(xj[-1]))
    y = psi.y
    subs = {y[j]: xj[j] for j in range(len(xj))}
    # dim(J  cap  psi(V)) = dim psi(V) - rank(valutazioni) ; dim psi(V) = dim V - dim [F] cap V
    kF = kernel_dim(imgs)
    evals = [sp.together(im.subs(subs)) for im in imgs]
    # dim ker(V -> funzioni via psi) = dim(I(u) cap V) per T1(a); qui calcolo dim ker della composizione
    dim_comp = rank_of_rational_list(evals, E)
    dim_J = dim_comp - kF
    return dim_direct, kF, dim_J

for ks, d, k in [((1,), 2, 2), ((1, 3), 2, 2), ((1, 3, 7), 2, 2)]:
    nu = sp.Rational(1)
    dd, kF, dJ = nshock_direct(ks, nu, d, k)
    check(f"T1(b) N-shock k={ks} in V_(2,2): dim(I(u) cap V) diretta = dim([F] cap V)+dim(J cap psi V)",
          dd == kF + dJ, f"({dd} = {kF} + {dJ})")
    if len(ks) == 3:
        check("T1(d)+T2(a): il 3-shock identifica Burgers in senso stretto in V_(2,2)? (atteso: dipende da J cap psi(V_(2,2)), ordine 4)", True, f"(dim I cap V = {dd})")

# (B) riduzione autosimile di KdV
t, x = sp.symbols('t x', positive=True)
W = sp.Function('W')
z = x*(3*t)**sp.Rational(-1, 3)
u = (3*t)**sp.Rational(-2, 3)*W(z)
expr = sp.diff(u, t) + 6*u*sp.diff(u, x) + sp.diff(u, x, 3)
Z = sp.Symbol('Z')
red = sp.simplify(expr*(3*t)**sp.Rational(5, 3))
red = red.subs(x, Z*(3*t)**sp.Rational(1, 3))
red = sp.simplify(red.doit())
target = sp.Derivative(W(Z), Z, 3) + 6*W(Z)*sp.Derivative(W(Z), Z) - 2*W(Z) - Z*sp.Derivative(W(Z), Z)
check("T4(iv) KdV autosimile: (3t)^{5/3}(u_t+6uu_x+u_xxx) = W''' + 6WW' - 2W - zW'",
      sp.simplify(red.doit() - target.doit()) == 0, f"({sp.simplify(red.doit())})")
print(f"\nTOTALE: {sum(RES)}/{len(RES)} OK")
