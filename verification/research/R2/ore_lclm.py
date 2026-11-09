# R2 - caso coeff. variabili (anello di Ore K(x)[D]): ker(L1 L2) != ker L1 + ker L2 ; ker LCLM(L1,L2) = ker L1 + ker L2
import sympy as sp
x=sp.symbols('x'); y=sp.Function('y')
D=lambda u,n=1: sp.diff(u,x,n)
L1=lambda u: x*D(u)-u      # ker L1 = span{x}
L2=lambda u: D(u)          # ker L2 = span{1}
print("ker L1 check:", L1(x), "  ker L2 check:", L2(sp.Integer(1)))
# product L1 L2 = x D^2 - D
print("L1L2 y =", sp.expand(L1(L2(y(x)))))
print("ker(L1L2):", sp.dsolve(L1(L2(y(x)))))
print("is x in ker(L1L2)?  L1L2(x) =", L1(L2(x)))
# LCLM(L1,L2): monic order-2 operator D^2 + a D + b killing 1 and x -> a=b=0 -> D^2
a,b=sp.symbols('a b')
eqs=[ (D(f,2)+a*D(f)+b*f) for f in (sp.Integer(1), x)]
print("LCLM coefficients:", sp.solve(eqs,[a,b]), " -> LCLM = D^2, ker = span{1,x} = ker L1 + ker L2")
# L2 L1 = D(xD-1) = x D^2 : ker = span{1,x}, coincides (L2L1 is a left multiple of L1 and of L2)
print("L2L1 y =", sp.expand(L2(L1(y(x)))))
# D-finite closure: sum f+g with ord r,s -> ord <= r+s ; product -> ord <= r*s
f=sp.exp(x**2); g=sp.sin(x)
c0,c1,c2=sp.symbols('c0 c1 c2')
# find order-3 operator D^3 + p2 D^2 + p1 D + p0 annihilating f, g*1 (cos,sin) -> LCLM(D-2x, D^2+1)
p0,p1,p2=sp.symbols('p0 p1 p2')
eqs=[sp.simplify((D(h,3)+p2*D(h,2)+p1*D(h)+p0*h)/ (sp.exp(x**2) if h==f else 1)) for h in (f, sp.sin(x), sp.cos(x))]
sol=sp.solve(eqs,[p0,p1,p2],dict=True)[0]
print("LCLM(D-2x, D^2+1) = D^3 + (", sp.factor(sol[p2]),")D^2 + (",sp.factor(sol[p1]),")D + (",sp.factor(sol[p0]),")")
h=f+g
print("check on f+g:", sp.simplify(D(h,3)+sol[p2]*D(h,2)+sol[p1]*D(h)+sol[p0]*h))
