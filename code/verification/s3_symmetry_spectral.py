# R7-S3: simmetrie lineari, V(P), scala di Heisenberg, algebre di Lie dei termini, Wei-Norman, Carleman, normalita' compagna
import sympy as sp
x,t,s,tau,xi,lam=sp.symbols('x t s tau xi lambda')
# (a) Galilei del calore come mappa affine di V(P): (tau,xi)->(tau+2 s xi+s^2, xi+s) ; P o g = P
P=tau-xi**2
g=lambda Q: sp.expand(Q.subs({tau:tau+2*s*xi+s**2, xi:xi+s},simultaneous=True))
print("S3a heat: P o g_Galilei - P =", g(P)-P)
u=sp.Function('u')
v=sp.exp(s*x+s**2*t)*u(x+2*s*t,t)
res=sp.diff(v,t)-sp.diff(v,x,2)
print("S3a' T_g u risolve il calore se u lo risolve:", sp.simplify((res/sp.exp(s*x+s**2*t)).subs(sp.Derivative(u(x+2*s*t,t),t),0)) )  # stampato per ispezione
# controllo diretto con u esponenziale del calore
xi0=sp.symbols('xi0'); ue=sp.exp(xi0*x+xi0**2*t); ve=sp.exp(s*x+s**2*t)*ue.subs(x,x+2*s*t)
print("S3a'' T_g e^{xi0 x+xi0^2 t} = e^{(xi0+s)x+(xi0+s)^2 t}:", sp.simplify(ve-sp.exp((xi0+s)*x+(xi0+s)**2*t))==0)
# Airy P=tau+xi^3: affine g=(a tau+b xi+c, d xi+e) con P o g = kappa P -> solo scaling (+ nessuno shift)
a,b,c,d,e,kap=sp.symbols('a b c d e kappa')
PA=tau+xi**3
eqs=sp.Poly(sp.expand(PA.subs({tau:a*tau+b*xi+c, xi:d*xi+e},simultaneous=True)-kap*PA),tau,xi).coeffs()
print("S3b Airy: stabilizzatore affine:", sp.solve(eqs,[a,b,c,e,kap],dict=True))
# (c) scala di Heisenberg: X = x + t a'(D) commuta con D_t - a(D); polinomi X^n 1 = coeff. di Taylor di e^{s x + t a(s)}
def check(aD, name):
    w=sp.Function('w')(x,t)
    A=lambda g: sum(cf*sp.diff(g,x,i) for i,cf in enumerate(sp.Poly(aD,xi).all_coeffs()[::-1]))
    Ap=lambda g: sum(cf*sp.diff(g,x,i) for i,cf in enumerate(sp.Poly(sp.diff(aD,xi),xi).all_coeffs()[::-1]))
    X=lambda g: x*g+t*Ap(g)
    Lop=lambda g: sp.diff(g,t)-A(g)
    print(f"S3c {name}: [D_t-a(D), x+t a'(D)] w =", sp.simplify(sp.expand(Lop(X(w))-X(Lop(w)))))
    gen=sp.exp(s*x+t*aD.subs(xi,s)); p=sp.Integer(1); ok=True
    for n in range(1,6):
        p=sp.expand(X(p)); ok&= sp.expand(p-sp.diff(gen,s,n).subs(s,0))==0 and sp.expand(Lop(p))==0
    print(f"     polinomi X^n 1 (n<=5) = d^n/ds^n e^(sx+t a(s))|_0 e risolvono:", ok, "; es. X^3 1 =", p if False else sp.expand(X(X(X(sp.Integer(1))))))
check(xi**2,"calore"); check(-xi**3,"Airy"); check(xi**2-xi**3+3*xi,"a generico")
# (d) algebre di Lie dei termini (algebra di Weyl): [D^3,x^2] genera ordini crescenti
f=sp.Function('f')(x)
def op(expr):  # rappresenta operatori come funzioni
    return expr
D=lambda k: (lambda g: sp.diff(g,x,k)); M=lambda h: (lambda g: h*g)
br=lambda A,B: (lambda g: sp.expand(A(B(g))-B(A(g))))
def order(Op):
    r=sp.expand(Op(f)); return max([dd.derivative_count for dd in r.atoms(sp.Derivative)]+[0])
B1=br(D(3),M(x**2)); B2=br(D(3),B1); B3=br(D(3),br(M(x**2),B1))
print("S3d ordini: [D3,x2]:",order(B1),"[D3,[D3,x2]]:",order(B2),"[D3,[x2,[D3,x2]]]:",order(B3))
# span{D^2, x^2, xD+1/2} chiuso (sl2) ; span{D^3,D^2,D,x,1} chiuso (risolubile)
print("S3d' [D^2,x^2]f =", sp.expand(br(D(2),M(x**2))(f)), " = (4xD+2)f ; [D^3,x]f =", br(D(3),M(x))(f))
# (e) Wei-Norman/BCH esatto: e^{t(D^2+x)} = e^{t^3/3} e^{t x} e^{t^2 D} e^{t D^2} su e^{xi0 x}
lhs_alpha=sp.integrate((xi0+t)**2,(t,0,t)); lhs=sp.exp(lhs_alpha+(xi0+t)*x)  # soluzione di u_t=u_xx+xu, u0=e^{xi0 x}
print("S3e verifica lhs risolve u_t=u_xx+xu:", sp.simplify(sp.diff(lhs,t)-sp.diff(lhs,x,2)-x*lhs)==0)
r1=sp.exp(xi0**2*t+xi0*x); r2=r1.subs(x,x+t**2); rhs=sp.exp(t**3/3)*sp.exp(t*x)*r2
print("S3e e^{t(D^2+x)} = e^{t^3/3} e^{tx} e^{t^2 D} e^{t D^2}:", sp.simplify(lhs-rhs)==0)
# (f) Carleman per x'=-x+x^2: y_n'=-n y_n + n y_{n+1}, troncato a N -> somma parziale della serie in x0
x0=sp.symbols('x0'); N=4
ys=[sp.Function(f'y{n}')(t) for n in range(1,N+1)]
sol=[None]*N
sol[N-1]=x0**N*sp.exp(-N*t)
for n in range(N-1,0,-1):
    yn=sp.Function('Y')(t)
    ode=sp.Eq(yn.diff(t),-n*yn+n*sol[n]); sol[n-1]=sp.simplify(sp.dsolve(ode,yn,ics={yn.subs(t,0):x0**n}).rhs)
part=sum(x0**n*sp.exp(-t)*(1-sp.exp(-t))**(n-1) for n in range(1,N+1))
print("S3f Carleman N=4: y1 troncato = sum_{n<=4} x0^n e^{-t}(1-e^{-t})^{n-1}:", sp.simplify(sol[0]-part)==0)
exact=x0*sp.exp(-t)/(1-x0+x0*sp.exp(-t))
print("     soluzione esatta - serie geometrica:", sp.simplify(exact - x0*sp.exp(-t)/(1-x0*(1-sp.exp(-t))))==0, " => converge unif. in t>=0 sse |x0|<1")
# (g) compagna normale sse p = z^m - c (m=3)
a0,a1,a2=sp.symbols('a0 a1 a2')
C=sp.Matrix([[0,1,0],[0,0,1],[-a0,-a1,-a2]])
print("S3g C C^T - C^T C = 0 <=>", sp.solve(list(C*C.T-C.T*C),[a1,a2],dict=True), "(reali) e |a0|=1: rotazione ciclica")
