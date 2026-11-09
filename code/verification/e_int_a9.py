# DEVIL-4 check 1: the A9 per-term E_int for Burgers vs the objects called "E_int" in Fase 4.
# u_t = A u + B(u), A = nu d_xx (diffusion), B(u) = -u u_x (transport). Data u0 = eps sin x on T.
# e_A = heat flow alone, e_B = inviscid flow alone (term alone), u = full flow.
# A9: E_int := u - e_A - e_B + u0  (so that u = u0 + (e_A-u0) + (e_B-u0) + E_int).
# F4-LIFT: E^NL := u - e_A.   F4-LIN: E^trop := u^nu - u^0 (full minus inviscid limit).
import sympy as sp
t, x, nu, eps = sp.symbols('t x nu epsilon', positive=True)
N = 3  # order in eps
# full solution by regular perturbation u = sum eps^n u_n
def heat_solve(forcing_coeffs):
    pass
u = [0, sp.exp(-nu*t)*sp.sin(x)]
# order 2: u2_t - nu u2_xx = -u1 u1_x
c = sp.Function('c')
rhs2 = sp.simplify(-u[1]*sp.diff(u[1], x))          # = -e^{-2 nu t} sin x cos x
# ansatz u2 = c(t) sin 2x
sol = sp.dsolve(sp.Eq(c(t).diff(t) + 4*nu*c(t), sp.simplify(rhs2/sp.sin(2*x))), c(t), ics={c(0): 0})
u2 = sp.simplify(sol.rhs)*sp.sin(2*x)
assert sp.simplify(sp.diff(u2, t) - nu*sp.diff(u2, x, 2) - rhs2) == 0
# inviscid alone: u = eps sin(x - t u)  -> series
ub = eps*sp.sin(x)
for _ in range(N):
    ub = sp.series(eps*sp.sin(x - t*ub), eps, 0, N+1).removeO()
ub2 = sp.expand(ub).coeff(eps, 2)
ea1 = sp.exp(-nu*t)*sp.sin(x)
# A9 E_int at order eps^2 (e_A has no eps^2 term, u0 has none):
Eint2 = sp.simplify(u2 - ub2)
ENL2 = u2
print("u2 (full, order eps^2)      =", sp.simplify(u2))
print("e_B order eps^2 (inviscid)  =", sp.simplify(ub2))
print("E_int^A9 order eps^2        =", sp.simplify(Eint2))
print("  small-t expansion         =", sp.series(sp.simplify(Eint2/sp.sin(2*x)), t, 0, 4))
print("E^NL order eps^2 (F4-LIFT)  =", sp.simplify(ENL2))
print("  small-t expansion         =", sp.series(sp.simplify(ENL2/sp.sin(2*x)), t, 0, 3))
# commutator check: BCH predicts E_int ~ (t^2/2)[A,B]u0 at leading order; [A,B]u = A B(u) - B'(u)[A u]
U = sp.Function('U')(x)
Bf = lambda w: -w*sp.diff(w, x)
Af = lambda w: nu*sp.diff(w, x, 2)
w0 = sp.sin(x)
# Lie derivative bracket for vector fields on function space: [A,B](w) = DB(w)[A w] - DA(w)[B w] (sign convention)
DB_Aw = -(Af(w0)*sp.diff(w0, x) + w0*sp.diff(Af(w0), x))
DA_Bw = Af(Bf(w0))
br = sp.simplify(DB_Aw - DA_Bw)
print("(t^2/2)*(DB[Aw]-DA[Bw]) at u0=sin x :", sp.simplify(br/2), "* t^2   (order eps^2)")
print("ratio leading coeff E_int / bracket  :", sp.simplify(sp.series(Eint2, t, 0, 3).removeO().coeff(t, 2) / (br/2)))
# additive E_int is governed by the symmetrised product (anticommutator) at order t^2:
anti = sp.simplify(DB_Aw + DA_Bw)
print("(t^2/2)*(DB[Aw]+DA[Bw]) at u0=sin x :", sp.simplify(anti/2), "* t^2")
print("CHECK leading E_int^A9 == (t^2/2)(DA[B]+DB[A]) :", sp.simplify(sp.series(Eint2, t, 0, 3).removeO().coeff(t, 2)*sp.sin(2*x)/sp.sin(2*x) - anti/2) == 0)
print("CHECK E^NL first order == t*B(u0) (term alone, no interaction):", sp.simplify(sp.series(ENL2, t, 0, 2).removeO().coeff(t, 1) - Bf(w0)) == 0)
print("large-t: E_int^A9/sin2x ~", sp.limit(Eint2/sp.sin(2*x)/t, t, sp.oo), "* t  (grows linearly: inviscid term-alone flow keeps steepening)")
