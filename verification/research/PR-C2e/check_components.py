# PR-C2e: controllo simbolico dei nuclei "generatore singolo" usati in components_matrix.md
import sympy as sp
t,x,c,D,k,a=sp.symbols('t x c D k a',positive=True)
f=sp.Function('f'); g=sp.Function('g')
res={}
# transport: u_t + c u_x = 0, u=g(x-ct)
u=g(x-c*t); res['transport g(x-ct)']=sp.simplify(sp.diff(u,t)+c*sp.diff(u,x))
# heat: u_t - D u_xx = 0, Gaussian
u=sp.exp(-x**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t); res['heat Gaussian']=sp.simplify(sp.diff(u,t)-D*sp.diff(u,x,2))
# Airy dispersion: u_t + u_xxx = 0, K=(3t)^(-1/3) Ai(x/(3t)^(1/3))
s=(3*t)**sp.Rational(1,3); u=sp.airyai(x/s)/s; res['Airy kernel']=sp.simplify(sp.diff(u,t)+sp.diff(u,x,3))
# Schroedinger: i u_t + u_xx = 0, Fresnel kernel
u=sp.exp(sp.I*x**2/(4*t))/sp.sqrt(4*sp.pi*sp.I*t); res['Fresnel kernel']=sp.simplify(sp.I*sp.diff(u,t)+sp.diff(u,x,2))
# wave: d'Alembert
u=f(x-c*t)+g(x+c*t); res['wave dAlembert']=sp.simplify(sp.diff(u,t,2)-c**2*sp.diff(u,x,2))
# reaction: u_t - a u = 0
u=sp.exp(a*t)*f(x); res['reaction']=sp.simplify(sp.diff(u,t)-a*u)
# mixed d_t d_x: ker = A(t)+B(x)
u=f(t)+g(x); res['mixed dtdx']=sp.diff(u,t,x)
# telegraph/damped wave mode: u_tt + 2a u_t - c^2 u_xx = 0 with u=e^{-a t} v, v Klein-Gordon-type
v=sp.Function('v')(t,x); u=sp.exp(-a*t)*v
expr=sp.diff(u,t,2)+2*a*sp.diff(u,t)-c**2*sp.diff(u,x,2)
res['telegraph -> KG (residual/e^{-at})']=sp.simplify(sp.expand(expr*sp.exp(a*t))-(sp.diff(v,t,2)-c**2*sp.diff(v,x,2)-a**2*v))
# Euler-Bernoulli beam mode: u_tt + u_xxxx = 0, u = cos(k^2 t) sin(k x)
u=sp.cos(k**2*t)*sp.sin(k*x); res['beam mode']=sp.simplify(sp.diff(u,t,2)+sp.diff(u,x,4))
# commutators in Weyl algebra
h=sp.Function('h')(x)
res['[d_x, x]h - h']=sp.simplify(sp.diff(x*h,x)-x*sp.diff(h,x)-h)
res['[d_x^2, x]h - 2h_x']=sp.simplify(sp.diff(x*h,x,2)-x*sp.diff(h,x,2)-2*sp.diff(h,x))
# Mehler (harmonic oscillator u_t = u_xx - x^2 u): ground mode e^{-t} e^{-x^2/2}
u=sp.exp(-t)*sp.exp(-x**2/2); res['oscillator ground mode']=sp.simplify(sp.diff(u,t)-sp.diff(u,x,2)+x**2*u)
# Burgers via Cole-Hopf: u=-2nu phi_x/phi, phi heat solution
nu=sp.symbols('nu',positive=True); phi=1+sp.exp(-x/(2*nu)+t/(4*nu))  # phi_t = nu phi_xx
res['phi heat']=sp.simplify(sp.diff(phi,t)-nu*sp.diff(phi,x,2))
u=-2*nu*sp.diff(phi,x)/phi; res['Burgers via Cole-Hopf']=sp.simplify(sp.diff(u,t)+u*sp.diff(u,x)-nu*sp.diff(u,x,2))
# KdV soliton u_t + 6 u u_x + u_xxx = 0
u=k**2/2*sp.sech(k/2*(x-k**2*t))**2; res['KdV soliton']=sp.simplify((sp.diff(u,t)+6*u*sp.diff(u,x)+sp.diff(u,x,3)).rewrite(sp.exp))
for kk,vv in res.items(): print(f"{kk:40s} residual = {vv}")

# --- aggiunte: fattorizzazioni e algebre di Lie dei termini ---
tau,xi=sp.symbols('tau xi')
print("beam   tau^2+xi^4 =", sp.factor(tau**2+xi**4, extension=sp.I))
print("Laplace tau^2+xi^2 =", sp.factor(tau**2+xi**2, extension=sp.I))
print("wave   tau^2-c^2 xi^2 =", sp.factor(tau**2-c**2*xi**2))
print("telegraph tau^2+2a tau-c^2xi^2 irreducible over Q(a,c):", sp.factor(tau**2+2*a*tau-c**2*xi**2))
print("KG tau^2-xi^2+m^2:", sp.factor(tau**2-xi**2+k**2, extension=sp.I))
# beam: Schroedinger kernels solve the beam equation
u=sp.exp(sp.I*x**2/(4*t))/sp.sqrt(4*sp.pi*sp.I*t)   # solves u_t = i u_xx
print("Fresnel kernel in ker(beam):", sp.simplify(sp.diff(u,t,2)+sp.diff(u,x,4)))
# sl(2): A=d_x^2, B=x^2, C=x d_x + 1/2
A=lambda w: sp.diff(w,x,2); B=lambda w: x**2*w; C=lambda w: x*sp.diff(w,x)+w/2
com=lambda P,Q,w: sp.expand(P(Q(w))-Q(P(w)))
print("[A,B]-4C =", sp.simplify(com(A,B,h)-4*C(h)))
print("[C,A]+2A =", sp.simplify(com(C,A,h)+2*A(h)))
print("[C,B]-2B =", sp.simplify(com(C,B,h)-2*B(h)))
# Heisenberg-type: d_x^2 and x : [d_x^2,x]=2d_x, [d_x,x]=1 -> closes on {d_x^2, d_x, x, 1}
