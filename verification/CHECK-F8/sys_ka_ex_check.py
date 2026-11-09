import sympy as sp
x,t,y=sp.symbols('x t y',real=True)
# heat example: f(t,x)=int_0^1 exp(y^2 t + y x) dy ; check integrand-level identity
g=sp.exp(y**2*t+y*x)
print("heat integrand residual:", sp.simplify(sp.diff(g,t)-sp.diff(g,x,2)))
# nested primes n=1: M=R+R/(zeta). f=int_0^1 e^{yx}dy, image of (a,b): a(d)f + b
f=sp.integrate(sp.exp(y*x),(y,0,1))
f=sp.simplify(f)
print("f =",f)
# incomparable maximal primes: a*1 + b*e^x = 0 on (0,1) forces a=b=0 (Wronskian)
W=sp.Matrix([[1,sp.exp(x)],[0,sp.exp(x)]]).det()
print("Wronskian 1,e^x:",W)
# can a(d)f be constant for a=c0+c1 zeta+c2 zeta^2? solve a(d)f + b = 0 via series
c0,c1,c2,b=sp.symbols('c0 c1 c2 b')
expr=sp.integrate((c0+c1*y+c2*y**2)*sp.exp(y*x),(y,0,1))+b
ser=sp.series(expr,x,0,6).removeO()
eqs=[sp.expand(ser).coeff(x,k) for k in range(6)]
print("solutions:",sp.solve(eqs,[c0,c1,c2,b],dict=True))
