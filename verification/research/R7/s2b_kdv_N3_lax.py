# R7-S2b: 3-solitone KdV via polinomi in E_i=exp(eta_i) (derivazioni esatte) + coppia di Lax
import sympy as sp, itertools
k=sp.symbols('k1:4',positive=True); E=sp.symbols('E1:4',positive=True)
Dx=lambda p: sp.expand(sum(k[i]*E[i]*sp.diff(p,E[i]) for i in range(3)))
Dt=lambda p: sp.expand(sum(-k[i]**3*E[i]*sp.diff(p,E[i]) for i in range(3)))
A=lambda i,j: ((k[i]-k[j])/(k[i]+k[j]))**2
f=0
for mu in itertools.product([0,1],repeat=3):
    c=sp.Mul(*[A(i,j) for i in range(3) for j in range(i+1,3) if mu[i] and mu[j]])
    f+=c*sp.Mul(*[E[i]**mu[i] for i in range(3)])
f=sp.expand(f)
fx=Dx(f); fxx=Dx(fx); fxxx=Dx(fxx); fxxxx=Dx(fxxx); ft=Dt(f); fxt=Dx(ft)
H=2*(f*fxt-fx*ft)+2*(f*fxxxx-4*fx*fxxx+3*fxx**2)
P=sp.Poly(sp.expand(H),*E)
print("S2b N=3 Hirota (D_xD_t+D_x^4)f.f = 0:", all(sp.simplify(sp.factor(c))==0 for c in P.coeffs()), "; monomi:", len(P.coeffs()))
# tau con solo coefficienti a coppie: f = sum_mu exp(sum mu_i eta_i + sum_{i<j} mu_i mu_j log A_ij); A123 = A12 A13 A23 (nessun termine a 3 corpi)
x,t=sp.symbols('x t'); u=sp.Function('u')(x,t); w=sp.Function('w')(x)
L=lambda g: -sp.diff(g,x,2)+u*g
for s,Pop in ((+1,lambda g: -4*sp.diff(g,x,3)+6*u*sp.diff(g,x)+3*sp.diff(u,x)*g),):
    c=sp.simplify(sp.expand(Pop(L(w))-L(Pop(w))))
    print("S2e Lax: L=-D^2+u, P=-4D^3+6uD+3u_x ; [P,L]w =", sp.factor(c), "=> L_t=[P,L] <=> u_t = 6uu_x - u_xxx ; con u -> -u: u_t+6uu_x+u_xxx=0")
