# Controllo (non metodo): limiti di scala del nucleo di u_t = D u_xx + b u_xxx
import sympy as sp
xi,t,y,s=sp.symbols('xi t y s',real=True)
D,b=sp.symbols('D b',positive=True)
a=-D*xi**2 - sp.I*b*xi**3     # simbolo di Fourier (u = e^{i xi x})
# t->inf, scala diffusiva xi = s/sqrt(t): t*a(s/sqrt t) -> -D s^2
print(sp.limit(t*a.subs(xi,s/sp.sqrt(t)),t,sp.oo))
# t->0, scala dispersiva xi = s/t^(1/3): t*a(s/t^(1/3)) -> -i b s^3
print(sp.limit(t*a.subs(xi,s/t**sp.Rational(1,3)),t,0,'+'))
# termine dominante per banda: vertici dell'inviluppo superiore di (k, log|a_k|), es. a=1e-2 xi + xi^2 + 1e-3 xi^3 + xi^4
import math
pts=[(1,math.log(1e-2)),(2,0.0),(3,math.log(1e-3)),(4,0.0)]
def upper_hull(P):
    H=[]
    for p in sorted(P):
        while len(H)>=2 and (H[-1][0]-H[-2][0])*(p[1]-H[-2][1])-(H[-1][1]-H[-2][1])*(p[0]-H[-2][0])>=0: H.pop()
        H.append(p)
    return H
print([k for k,_ in upper_hull(pts)])   # termine 3 non e' vertice -> mai dominante

# Output (python -I, 2026-10-22):
# -D*s**2
# -I*b*s**3
# [1, 2, 4]
