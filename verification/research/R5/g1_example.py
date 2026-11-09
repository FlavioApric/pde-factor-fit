import sympy as sp
tau, xi = sp.symbols('tau xi')
P1 = tau - xi**2; P2 = -xi
Gb = sp.groebner([P1+P2, sp.expand(P1*P2)], tau, xi, order='grevlex')
print("Groebner (P1+P2, P1P2):", Gb.exprs)
# standard monomials -> dim of quotient
from itertools import product
lead = [sp.Poly(g, tau, xi).monoms(order='grevlex')[0] for g in Gb.exprs]
std = [(a,b) for a,b in product(range(6), range(6)) if not any(a>=l[0] and b>=l[1] for l in lead)]
print("monomi standard:", std, "dim =", len(std))
