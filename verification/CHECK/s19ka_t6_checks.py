import sympy as sp
x,t=sp.symbols('x t',real=True)
# 1) C^1 counterexample to L9(i): z'=g(z), g(z)=-z/(2 log(1/z)), z=exp(-sqrt x)
z=sp.symbols('z',positive=True)
g=-z/(2*sp.log(1/z))
gp=sp.simplify(sp.diff(g,z))
print("g' =",gp," limit z->0+:",sp.limit(gp,z,0,'+'), " g'/z^0.1 limit:",sp.limit(gp/z**sp.Rational(1,10),z,0,'+'))
X=sp.symbols('X',positive=True)
zz=sp.exp(-sp.sqrt(X))
print("ODE residual:",sp.simplify(sp.diff(zz,X)-g.subs(z,zz)))
print("x^n z ->0 (n=50):",sp.limit(X**50*zz,X,sp.oo))
# 2) 2-soliton satisfies Novikov relation with l(z)=(z^2-k1^2)(z^2-k2^2)
k1,k2=sp.Rational(1),sp.Rational(3,2)
e1=sp.exp(k1*x-k1**3*t); e2=sp.exp(k2*x-k2**3*t)
A=((k1-k2)/(k1+k2))**2
tau=1+e1+e2+A*e1*e2
u=2*sp.diff(sp.log(tau),x,2)
D=lambda f,n=1: sp.diff(f,x,n)
kdv=sp.diff(u,t)+6*u*D(u)+D(u,3)
G1=u; G2=D(u,2)+3*u**2; G3=D(u,4)+10*u*D(u,2)+5*D(u)**2+10*u**3
nov=G3-(k1**2+k2**2)*G2+k1**2*k2**2*G1
import random
for _ in range(4):
    xv,tv=random.uniform(-3,3),random.uniform(-1,1)
    print("kdv res",sp.N(kdv.subs({x:xv,t:tv})),"novikov res",sp.N(nov.subs({x:xv,t:tv})))
