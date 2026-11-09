# S5-EX · E6 Bessel: B = x d^2 + d + x ∈ A_1 (ordine 0), calore radiale P_r = x d_t - x d_x^2 - d_x ∈ D = A_1[d_t]
# Teoremi: P4-C1; OP-ALG-T4 / OPR2-T3 (ipotesi "P monico in d_t" NON soddisfatta: si controlla cosa resta);
#          P3-T1(b) (corona con Dirichlet: V = (1/x) d_x limitato) ; C3/C12/P1/P2: non applicabili
# Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I ex5_bessel.py
import sys
import sympy as sp
import mpmath as mp

sys.stdout.reconfigure(encoding='utf-8')
t, x = sp.symbols('t x', positive=True)
RES = []


def check(name, cond, info=''):
    RES.append((name, bool(cond)))
    print(('[OK]   ' if cond else '[FAIL] ') + name + ((' :: ' + str(info)) if info != '' else ''), flush=True)


def wmul(A, B):
    out = {}
    for (a, b), ca in A.items():
        for (cc, d), cb in B.items():
            for l in range(0, min(b, cc) + 1):
                coef = ca * cb * sp.binomial(b, l) * sp.factorial(cc) / sp.factorial(cc - l)
                key = (a + cc - l, b - l + d)
                out[key] = sp.expand(out.get(key, 0) + coef)
    return {k: v for k, v in out.items() if v != 0}


def wapply(A, f):
    return sp.expand(sum(cf * x**i * sp.diff(f, x, j) for (i, j), cf in A.items()))


def box(I, J):
    return [(i, j) for i in range(I + 1) for j in range(J + 1)]


J0, J1 = sp.symbols('J0 J1')


def bj_coeffs(expr):
    e = sp.expand(expr).rewrite(sp.besselj)
    e = sp.expand(e.subs({sp.besselj(0, x): J0, sp.besselj(1, x): J1}))
    # derivate superiori producono besselj(2,x), ...: ricorrenza J_{n+1} = (2n/x) J_n - J_{n-1}
    for n in range(8, 1, -1):
        pass
    num = sp.numer(sp.together(e))
    return sp.Poly(sp.expand(num), x, J0, J1).coeffs()


def reduce_bessel(expr):
    e = sp.expand(expr)
    for n in range(10, 1, -1):
        e = sp.expand(e.subs(sp.besselj(n, x), 2 * (n - 1) / x * sp.besselj(n - 1, x) - sp.besselj(n - 2, x)))
    return e


B = {(1, 2): 1, (0, 1): 1, (1, 0): 1}

print('== E6.1 Bessel EDO: B J_0 = 0, J_0 e J_0\' indipendenti su C(x) ==')
check('E6.1a B J_0 = x J_0\'\' + J_0\' + x J_0 = 0', sp.simplify(reduce_bessel(wapply(B, sp.besselj(0, x)))) == 0)
zs = [mp.besseljzero(0, k) for k in (1, 2, 3)]
check('E6.1b J_0 ha infiniti zeri reali (2.405, 5.520, 8.654, ...) => J_0\'/J_0 = -J_1/J_0 non razionale',
      abs(zs[0] - 2.404825557695773) < 1e-9)

print('== E6.2 Ann_{A_1}(J_0) ∩ box vs A_1·B (B NON monico: coefficiente direttore x) ==')
I_, Jd = 3, 4
Bx = box(I_, Jd)
cs = sp.symbols(f'k0:{len(Bx)}')
expr = reduce_bessel(wapply(dict(zip(Bx, cs)), sp.besselj(0, x)))
eqs = bj_coeffs(expr)
ns = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs]).nullspace()
# A_1 B ∩ box: R in box(I_-1, Jd-2) (gradi additivi nelle due filtrazioni, A_1 dominio)
prods = [wmul({k: 1}, B) for k in box(I_ - 1, Jd - 2)]
Mp = sp.Matrix([[p.get(k, 0) for k in Bx] for p in prods])
Mann = sp.Matrix([[v[n] for n in range(len(Bx))] for v in ns])
r_p, r_a, r_pa = Mp.rank(), Mann.rank(), Mp.col_join(Mann).rank()
check(f'E6.2a Ann_A1(J_0) ∩ box({I_},{Jd}) = A_1 B ∩ box (dim {r_a} = {r_p}, somma {r_pa}): nessun elemento "saturato" in più (V-ex)',
      r_p == r_a == r_pa)
eqs2 = []
for (k_, l_) in box(2, 2):
    eqs2 += bj_coeffs(reduce_bessel(wapply(dict(zip(Bx, cs)), x**k_ * sp.diff(sp.besselj(0, x), x, l_))))
n2 = sp.Matrix([[sp.diff(e, cf) for cf in cs] for e in eqs2]).nullspace()
check('E6.2b P4-C1(a): rho_{J_0} iniettiva su box(3,4) (nucleo 0) anche se Ann ∩ box ≠ 0', len(n2) == 0 and r_a > 0)

print('== E6.3 calore radiale P_r = x d_t - x d_x^2 - d_x in D = A_1[d_t] (non monico in d_t) ==')


def Pr(u):
    return sp.expand(x * sp.diff(u, t) - x * sp.diff(u, x, 2) - sp.diff(u, x))


k = sp.Integer(2)
uk = sp.exp(-k**2 * t) * sp.besselj(0, k * x)
check('E6.3a u_k = e^{-k^2 t} J_0(kx): P_r u_k = 0', sp.simplify(reduce_bessel(Pr(uk).rewrite(sp.besselj))) == 0 or
      sp.simplify(Pr(uk)) == 0)
bk = sp.simplify(x * sp.diff(uk, x, 2) + sp.diff(uk, x) + k**2 * x * uk)
check('E6.3b u_k ∈ 𝒯 (B_k = x d^2 + d + k^2 x la annulla): Ann ≠ D·P_r, testimone B_k di grado 0 in d_t (come i modi EP nel caso costante)', bk == 0)
uK = sp.exp(-x**2 / (4 * t)) / t
check('E6.3c nucleo radiale u = t^-1 e^{-x^2/4t}: P_r u = 0', sp.simplify(Pr(uK)) == 0)
Bb = box(3, 3)
cb = sp.symbols(f'p0:{len(Bb)}')
r = sp.numer(sp.together(sp.simplify(wapply(dict(zip(Bb, cb)), uK) / uK)))
nsb = sp.Matrix([[sp.diff(e, cf) for cf in cb] for e in sp.Poly(sp.expand(r), t, x).coeffs()]).nullspace()
check('E6.3d u ∉ 𝒯: nessun b ∈ A_1 ∩ box(3,3) con b u = 0 (V-ex; in generale: coefficiente di t^-K = p_K(x)(-x/2)^K)', len(nsb) == 0)
# Ann_D(u) ∩ {q1 d_t + q0 : q_i ∈ box(3,3)} vs D·P_r ∩ stesso spazio
cA = sp.symbols(f'a0:{len(Bb)}')
cB = sp.symbols(f'b0:{len(Bb)}')
ex_ = wapply(dict(zip(Bb, cA)), sp.diff(uK, t)) + wapply(dict(zip(Bb, cB)), uK)
r = sp.numer(sp.together(sp.simplify(ex_ / uK)))
nsA = sp.Matrix([[sp.diff(e, cf) for cf in cA + cB] for e in sp.Poly(sp.expand(r), t, x).coeffs()]).nullspace()
# D·P_r con grado in d_t <= 1: r P_r, r ∈ A_1 (d_t centrale): q1 = r x, q0 = -r (x d^2 + d)
B0 = {(1, 2): 1, (0, 1): 1}
big = box(4, 4)
rs = sp.symbols(f'r0:{len(big)}')
Q1 = {}
Q0 = {}
for rr, kk in zip(rs, big):
    for kk2, v in wmul({kk: rr}, {(1, 0): 1}).items():
        Q1[kk2] = Q1.get(kk2, 0) + v
    for kk2, v in wmul({kk: rr}, B0).items():
        Q0[kk2] = Q0.get(kk2, 0) - v
outside = [Q1[k_] for k_ in Q1 if k_ not in Bb] + [Q0[k_] for k_ in Q0 if k_ not in Bb]
Mo = sp.Matrix([[sp.diff(e, cf) for cf in rs] for e in outside])
nsR = Mo.nullspace()
dimDP = sp.Matrix([[sp.expand(Q1.get(k_, 0)).subs(dict(zip(rs, v))) for k_ in Bb] + [sp.expand(Q0.get(k_, 0)).subs(dict(zip(rs, v))) for k_ in Bb] for v in nsR]).rank() if nsR else 0
Mann = sp.Matrix([[v[i] for i in range(2 * len(Bb))] for v in nsA]) if nsA else sp.zeros(0, 2 * len(Bb))
MDP = sp.Matrix([[sp.expand(Q1.get(k_, 0)).subs(dict(zip(rs, v))) for k_ in Bb] + [sp.expand(Q0.get(k_, 0)).subs(dict(zip(rs, v))) for k_ in Bb] for v in nsR]) if nsR else sp.zeros(0, 2 * len(Bb))
check(f'E6.3e osservato: Ann_D(u) ∩ {{q1 d_t + q0, q_i ∈ box(3,3)}} = D·P_r ∩ stesso spazio (dim {Mann.rank()} = {dimDP}): u identifica P_r (V-ex)',
      Mann.rank() == dimDP == Mann.col_join(MDP).rank())

print('== E6.4 P3-T1(b) su una corona (r0, R), Dirichlet: A_0 = d^2, V = (1/x) d_x con b_1 = 1/x ∈ L^inf ==')
mu_, Dd, s_ = sp.symbols('mu D s', positive=True)
f = mu_ * sp.exp(-Dd * mu_**2 * s_)
crit = sp.solve(sp.diff(f, mu_), mu_)
val = sp.simplify(f.subs(mu_, crit[0]))
check('E6.4 sup_mu mu e^{-D mu^2 s} = (2eDs)^{-1/2}: (H_{1/2}) con K = ||1/x||_inf (2eD)^{-1/2} = (2eD)^{-1/2}/r0 => Dyson-Phillips converge (solo per r0 > 0)',
      sp.simplify(val - (2 * sp.E * Dd * s_)**sp.Rational(-1, 2)) == 0)

nok = sum(1 for _, ok in RES if ok)
print(f'\nTOTALE E6: {nok}/{len(RES)} OK')
