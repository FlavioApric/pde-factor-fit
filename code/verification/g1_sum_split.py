# R2 - verifica G1 (C4.1/A8): L = L1 + L2, ker L ∩ (ker L1 + ker L2) = Sol(L1+L2, L1*L2) = Sol(L1+L2, L1^2)
import sympy as sp
t,x,tau,xi = sp.symbols('t x tau xi')
def dim_quotient(gens, vars_):
    G = sp.groebner(gens, *vars_, order='grevlex')
    # standard monomials (finite case): enumerate up to degree bound
    lead = [sp.Poly(g,*vars_).monoms(order='grevlex')[0] for g in G.exprs]
    std=[]
    for a in range(0,12):
        for b in range(0,12):
            if not any(a>=l[0] and b>=l[1] for l in lead): std.append((a,b))
    return G.exprs, std
def op(P, u):  # apply P(d_t,d_x) to u
    P = sp.Poly(sp.expand(P), tau, xi)
    return sp.expand(sum(c*sp.diff(u, t, m[0], x, m[1]) if (m[0] or m[1]) else c*u for m,c in zip(P.monoms(),P.coeffs())))
# Example A: heat split L1 = d_x^2, L2 = -d_t
L1, L2 = xi**2, -tau
I1 = [L1+L2, L1*L2]; I2=[L1+L2, L1**2]
print("A) GB(L1+L2,L1L2) =", sp.groebner(I1,tau,xi,order='grevlex').exprs, " GB(L1+L2,L1^2) =", sp.groebner(I2,tau,xi,order='grevlex').exprs)
G,std = dim_quotient(I1,(tau,xi)); print("   standard monomials:", std, " dim =", len(std))
sols = [sp.Integer(1), x, x**2+2*t, x**3+6*t*x]
for u in sols:
    print("   u=",u," Lu=",op(L1+L2,u)," L1L2 u=",op(L1*L2,u))
# generic heat solution e^{s^2 t + s x}, s != 0 : L1L2 u != 0  => not in ker L1 + ker L2
s=sp.symbols('s', nonzero=True); ug=sp.exp(s**2*t+s*x)
print("   generic: Lu=",sp.simplify(op(L1+L2,ug)), " L1L2 u=", sp.simplify(op(L1*L2,ug)))
# Example B: advection-diffusion split L1 = d_t - d_x^2 , L2 = c d_x  (c=1)
L1, L2 = tau - xi**2, xi
G,std = dim_quotient([L1+L2, L1*L2],(tau,xi))
print("B) GB =", G, " dim =", len(std), " V(L1)∩V(L2) =", sp.solve([L1,L2],[tau,xi],dict=True))
# Example C: non-coprime terms L1 = d_t d_x, L2 = d_x^2 : common factor xi -> infinite-dim
L1, L2 = tau*xi, xi**2
print("C) gcd(L1,L2) =", sp.gcd(L1,L2), " -> V(L1)∩V(L2) contains line xi=0 ; any a(t) lies in ker L1 ∩ ker L2 ∩ ker L:", op(L1+L2, sp.Function('a')(t)))
# Example D: three terms, L = d_t - d_x^2 - d_x (pairwise coprime ?)
Ls=[tau, -xi**2, -xi]
print("D) pairwise gcds:", [sp.gcd(Ls[i],Ls[j]) for i in range(3) for j in range(i+1,3)])
