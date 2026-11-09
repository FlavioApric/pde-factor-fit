"""F4-LIN trop_burgers.py -- tropical Cole-Hopf (RT-R7b): estimate of E_int in nu.
Setting: psi^nu = -2 nu log sum_i exp(-S_i/(2nu)),  S_i(t,x) = c_i x - c_i^2 t/2 - beta_i
         psi^0 = min_i S_i (Hopf-Lax / entropy potential), u^nu = psi^nu_x, u^0 = psi^0_x.
Checks:
 T1 u^nu solves Burgers_nu (N=3 symbolic);  each S_i solves psi_t + psi_x^2/2 = 0 (and nu psi_xx = 0)
 T2 softmax mixture identity u^nu = sum_i w_i c_i, w = softmax(-S/2nu)
 T3 log-sum-exp bound -2 nu log N <= psi^nu - psi^0 <= 0  (numerical grid check N=3,5)
 T4 two waves: ||u^nu - u^0||_{L1(R)} = 4 nu ln 2 (exact, symbolic), independent of the jump
 T5 two waves: ||u^nu - u^0||_{L2}^2 = 4 nu Delta (ln 2 - 1/2) (exact, symbolic)
 T6 scaling: E(y) = (Delta/2) F(Delta y/(4 nu)), F = tanh - sgn; ||E||_{Lp} ~ nu^{1/p}; ||E||_{H^1} infinite for nu -> 0 rate nu^{-1/2}
 T7 N=3 numerical: L1 defect at a time with 2 isolated shocks ~ 2 * 4 nu ln 2 (controllo)
 T8 shock positions = corner locus of the tropical polynomial min_i S_i; Rankine-Hugoniot speed (c_i+c_j)/2
 T9 additive E_int = u^nu - sum_i u_i (u_i = c_i) is O(1): not the right object
"""
import sympy as sp
import mpmath as mp

res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

t, x, y = sp.symbols('t x y', real=True)
nu, D = sp.symbols('nu Delta', positive=True)
cs = sp.symbols('c1:4', real=True)
bs = sp.symbols('b1:4', real=True)
S = [ci*x - ci**2*t/2 - bi for ci, bi in zip(cs, bs)]
Z = sum(sp.exp(-Si/(2*nu)) for Si in S)
psi = -2*nu*sp.log(Z)
uN = sp.diff(psi, x)
burg = sp.diff(uN, t) + uN*sp.diff(uN, x) - nu*sp.diff(uN, x, 2)
check('T1a u^nu (N=3) solves Burgers_nu', sp.simplify(burg) == 0)
check('T1b each S_i solves psi_t + psi_x^2/2 = 0', all(sp.simplify(sp.diff(Si, t) + sp.diff(Si, x)**2/2) == 0 for Si in S))
w = [sp.exp(-Si/(2*nu))/Z for Si in S]
check('T2 softmax mixture u^nu = sum w_i c_i', sp.simplify(uN - sum(wi*ci for wi, ci in zip(w, cs))) == 0)

# T3 numerical grid
def lse_check(cvals, bvals, nuv):
    worst_lo, worst_hi = 0.0, -1e9
    N = len(cvals)
    for tv in [0.0, 0.3, 1.0, 2.5]:
        for xv in [i*0.05 - 5 for i in range(201)]:
            Sv = [cc*xv - cc**2*tv/2 - bb for cc, bb in zip(cvals, bvals)]
            m = min(Sv)
            ps = m - 2*nuv*mp.log(sum(mp.e**(-(s - m)/(2*nuv)) for s in Sv))
            d = float(ps - m)
            worst_lo = min(worst_lo, d + 2*nuv*float(mp.log(N)))
            worst_hi = max(worst_hi, d)
    return worst_lo >= -1e-12 and worst_hi <= 1e-12
check('T3a LSE bound N=3 (nu=0.1)', lse_check([2.0, 0.5, -1.0], [0.0, 0.3, -0.2], 0.1))
check('T3b LSE bound N=5 (nu=0.01)', lse_check([3, 1.5, 0.2, -0.7, -2], [0, 0.4, 0.1, -0.3, 0.2], 0.01))

# T4, T5 two waves, symmetric frame: S1 - S2 = Delta * y (y = x - shock position), u jumps by Delta
# u^nu - u^0 = Delta*(sigmoid - Heaviside)-type; take u^nu = -(Delta/2) tanh(Delta y/(4nu)) + cbar, u^0 = -(Delta/2) sgn(y) + cbar
b = D/(4*nu)
E_pos = -(D/2)*(sp.tanh(b*y) - 1)   # y>0
L1 = 2*sp.integrate(sp.simplify(E_pos.rewrite(sp.exp)), (y, 0, sp.oo))
check('T4 L1 defect of one viscous shock = 4 nu ln 2', sp.simplify(L1 - 4*nu*sp.log(2)) == 0)
L2sq = 2*sp.integrate(sp.simplify((E_pos**2).rewrite(sp.exp)), (y, 0, sp.oo))
check('T5 L2^2 defect = 4 nu Delta (ln2 - 1/2)', sp.simplify(L2sq - 4*nu*D*(sp.log(2) - sp.Rational(1, 2))) == 0)
# confirm two-wave LSE gives exactly this tanh profile
c1, c2 = sp.symbols('cA cB', real=True)
S1 = c1*x - c1**2*t/2; S2 = c2*x - c2**2*t/2
u2 = sp.diff(-2*nu*sp.log(sp.exp(-S1/(2*nu)) + sp.exp(-S2/(2*nu))), x)
xs = (c1 + c2)*t/2
prof = (c1 + c2)/2 - (c1 - c2)/2*sp.tanh((c1 - c2)*(x - xs)/(4*nu))
check('T4b two-wave LSE = viscous shock profile ((c1+c2)/2 - (c1-c2)/2 tanh((c1-c2)(x-x_s)/4nu))',
      sp.simplify((u2 - prof).rewrite(sp.exp)) == 0)

# T6 scaling: d/dy of tanh profile: H^1 seminorm^2 = int (E')^2 = (Delta/2)^2 b^2 * 2 int sech^4 = ... ~ Delta^3/nu
z = sp.symbols("z", real=True)
I4 = sp.integrate(sp.simplify((sp.sech(z)**4).rewrite(sp.exp)), (z, -sp.oo, sp.oo))
print("     int sech^4 =", sp.nsimplify(sp.simplify(I4)))
H1sq = ((D/2)*b)**2 * sp.nsimplify(sp.simplify(I4)) / b
H1sq = sp.simplify(H1sq)
print('     |u^nu_x|_{L2}^2 (smooth part) =', H1sq)
check('T6 H^1 seminorm of E grows like nu^{-1/2} (squared ~ Delta^3/(nu))', sp.simplify(H1sq - D**3/(12*nu)) == 0)

# T7 N=3 numerical L1 defect (control)
mp.mp.dps = 30
def u_nu(xv, tv, cvals, bvals, nuv):
    Sv = [cc*xv - cc**2*tv/2 - bb for cc, bb in zip(cvals, bvals)]
    m = min(Sv)
    ws = [mp.e**(-(s - m)/(2*nuv)) for s in Sv]
    return sum(wi*cc for wi, cc in zip(ws, cvals))/sum(ws)
def u_0(xv, tv, cvals, bvals):
    Sv = [cc*xv - cc**2*tv/2 - bb for cc, bb in zip(cvals, bvals)]
    return cvals[Sv.index(min(Sv))]
cv, bv, tv = [2.0, 0.0, -2.0], [0.0, 1.0, 0.0], 0.1
for nuv in [0.02, 0.005]:
    f = lambda xv: abs(u_nu(xv, tv, cv, bv, nuv) - u_0(xv, tv, cv, bv))
    # shocks: S1=S2 -> 2x - 0.2 = -1 -> x=-0.4 ; S2=S3 -> -1 = -2x - 0.2 -> x = 0.4
    val = mp.quad(f, [-3, -0.4, 0.4, 3])
    ratio = val/(2*4*nuv*mp.log(2))
    print('     nu=%g  L1 defect=%s  ratio to 2*4nu ln2 = %s' % (nuv, mp.nstr(val, 10), mp.nstr(ratio, 10)))
check('T7 N=3, two isolated shocks: L1 defect / (8 nu ln2) -> 1 (nu=0.005 within 1e-6)', abs(ratio - 1) < 1e-6)

# T8 Rankine-Hugoniot: corner S_i = S_j moves with speed (c_i+c_j)/2
xs_sol = sp.solve(sp.Eq(S1, S2), x)[0]
check('T8 tropical corner S_i=S_j moves at (c_i+c_j)/2 (Rankine-Hugoniot)', sp.simplify(sp.diff(xs_sol, t) - (c1 + c2)/2) == 0)

# T9 additive E_int is O(1)
Eadd = u2 - (c1 + c2)
check('T9 additive E = u - (u1+u2) -> -c2 (resp. -c1) far from the shock: O(1)',
      sp.simplify(sp.limit(Eadd.subs({c1: 2, c2: -1, t: 0}), x, -sp.oo) - 1) == 0)

print('\nSUMMARY: %d/%d OK' % (sum(r for _, r in res), len(res)))
