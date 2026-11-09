# R2 - verifica G2 (C4.2) su f=(d_t - d_x^2), g=(d_t + d_x); controesempio periodico.
import sympy as sp
t,x,tau,xi = sp.symbols('t x tau xi')
f = tau - xi**2          # heat
g = tau + xi             # transport
# 1) variety V(f) ∩ V(g) and ideal (f,g)
G = sp.groebner([f,g], tau, xi, order='lex')
print("Groebner (f,g):", G.exprs)
print("V(f)∩V(g):", sp.solve([f,g],[tau,xi],dict=True))
# 2) ker f ∩ ker g basis (exponentials e^{tau t+ xi x} at common points, multiplicity 1 each)
Df = lambda u: sp.diff(u,t)-sp.diff(u,x,2)
Dg = lambda u: sp.diff(u,t)+sp.diff(u,x)
for u in [sp.Integer(1), sp.exp(t-x)]:
    print("u=",u," f u=",sp.simplify(Df(u))," g u=",sp.simplify(Dg(u)))
# 3) u = t lies in ker(fg)
u = t
print("fg(t) =", Df(Dg(u)))
# on R^2: t = x + (t-x), x in ker f, t-x in ker g
print("decomp on R^2: f(x)=",Df(x)," g(t-x)=",Dg(t-x))
# general decomposition t = u1+u2 with u2=phi(x-t): solve ODE for phi
s=sp.symbols('s'); phi=sp.Function('phi')
u2 = phi(x-t); u1 = t-u2
ode = sp.simplify(Df(u1)).subs(x-t,s)
print("heat(u1) =", ode)
print("phi solutions:", sp.dsolve(sp.Eq(phi(s).diff(s,2)+phi(s).diff(s)+1,0)))
# 4) periodic in x (mode k=0): f_0=tau, g_0=tau, f_0 g_0 = tau^2.
#    ker f_0 + ker g_0 = constants (dim 1) but ker(f_0 g_0) = span{1,t} (dim 2)
k=sp.symbols('k',integer=True)
fk = f.subs(xi, sp.I*k); gk = g.subs(xi, sp.I*k)
print("f_k =",fk," g_k =",gk," Res_tau(f,g)(xi) =", sp.resultant(f,g,tau))
print("modes k with common root:", [kk for kk in range(-50,51) if sp.gcd(fk.subs(k,kk), gk.subs(k,kk)).has(tau)])
