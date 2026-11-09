# R1 controlli simbolici (coerenze di dizionari di nuclei, residuo indipendente dal regolarizzatore)
import sympy as sp, mpmath as mp
x,t=sp.symbols('x t',real=True)
s1,s2,lam,mu_=sp.symbols('sigma1 sigma2 lambda mu',positive=True)
a,b=sp.symbols('a b',real=True)
# 1) Coerenza tra gaussiane (atomi del nucleo del calore, sigma^2 = 2s)
g1=sp.exp(-(x-a)**2/(2*s1**2)); g2=sp.exp(-(x-b)**2/(2*s2**2))
ip=sp.simplify(sp.integrate(g1*g2,(x,-sp.oo,sp.oo)))
n1=sp.integrate(g1**2,(x,-sp.oo,sp.oo)); n2=sp.integrate(g2**2,(x,-sp.oo,sp.oo))
coh=sp.simplify(ip/sp.sqrt(n1*n2))
claim=sp.sqrt(2*s1*s2/(s1**2+s2**2))*sp.exp(-(a-b)**2/(2*(s1**2+s2**2)))
print("[1] gauss coherence:",coh," | claim diff =",sp.simplify(sp.log(coh)-sp.log(claim)))
r=sp.symbols('r',positive=True)
print("    same centre, s2=r*s1:",sp.simplify(claim.subs({a:0,b:0,s2:r*s1})),"= sqrt(sech(log r)) ?",
      sp.simplify(claim.subs({a:0,b:0,s2:r*s1})**2 - 1/sp.cosh(sp.log(r))).rewrite(sp.exp).simplify())
# 2) Coerenza tra esponenziali decrescenti in L2(0,inf)
e1=sp.exp(-lam*x); e2=sp.exp(-mu_*x)
c2=sp.simplify(sp.integrate(e1*e2,(x,0,sp.oo))/sp.sqrt(sp.integrate(e1**2,(x,0,sp.oo))*sp.integrate(e2**2,(x,0,sp.oo))))
print("[2] exp coherence:",c2," | minus sech(log(lam/mu)/2):",sp.simplify((c2-1/sp.cosh(sp.log(lam/mu_)/2)).rewrite(sp.exp)))
# 3) Gaussiana vs gaussiana evoluta da u_t+u_xxx=0 (Airy):  mu(t)=(1/int|g^|^2) int |g^(k)|^2 e^{i k^3 t} dk
def mu_num(sig,tt):
    f=lambda k: mp.exp(-sig**2*k**2)*mp.cos(k**3*tt)
    return mp.quad(f,[-mp.inf,0,mp.inf])/(mp.sqrt(mp.pi)/sig)
def mu_closed(sig,tt):
    bb=sig**2*(3*tt)**(-mp.mpf(2)/3)
    return 2*mp.sqrt(mp.pi)*sig*(3*tt)**(-mp.mpf(1)/3)*mp.exp(2*bb**3/3)*mp.airyai(bb**2)
for sig,tt in [(1,0.1),(1,1),(1,10),(0.5,3)]:
    print("[3] sigma=%s t=%s  numeric=%s closed=%s"%(sig,tt,mp.nstr(mu_num(sig,tt),12),mp.nstr(mu_closed(sig,tt),12)))
print("    large-t asymptotic 2*sqrt(pi)*sigma*Ai(0)*(3t)^(-1/3) at sigma=1,t=1e4:",
      mp.nstr(mu_closed(1,1e4),10), mp.nstr(2*mp.sqrt(mp.pi)*mp.airyai(0)*(3e4)**(-mp.mpf(1)/3),10))
# 4) Residuo indipendente dal regolarizzatore: L=D^2-1 scritto come somma di termini T1=D^2, T2=-1.
#    classi per termine: ker D^2 = span{1,x}; ker(-1)={0}. u=e^x in L2(0,1): dist(u, span{1,x}) > 0.
u=sp.exp(x); B=[sp.Integer(1),x]
G=sp.Matrix(2,2,lambda i,j: sp.integrate(B[i]*B[j],(x,0,1)))
h=sp.Matrix([sp.integrate(u*bb_,(x,0,1)) for bb_ in B])
c=G.solve(h); proj=c[0]+c[1]*x
res2=sp.simplify(sp.integrate((u-proj)**2,(x,0,1)))
print("[4] ||P_perp e^x||^2 on (0,1) =",res2,"=",sp.N(res2,12))
#    fattorizzazione (D-1)(D+1): classi e^x, e^-x -> residuo 0, Gram invertibile (split unico)
E=[sp.exp(x),sp.exp(-x)]
GE=sp.Matrix(2,2,lambda i,j: sp.integrate(E[i]*E[j],(x,0,1)))
print("    Gram{e^x,e^-x} det =",sp.simplify(GE.det()),"=",sp.N(GE.det(),8))
# 5) L2 (norma minima) vs L1 su dizionario ridondante: e1,e2 ONB di R^2, e3=(e1+e2)/sqrt2; u=e3
S=sp.Matrix([[1,0,1/sp.sqrt(2)],[0,1,1/sp.sqrt(2)]]); uu=sp.Matrix([1/sp.sqrt(2),1/sp.sqrt(2)])
w2=S.T*(S*S.T).inv()*uu
print("[5] min-l2 coeffs:",list(sp.simplify(w2)),"l1 norm",sp.nsimplify(sum(abs(v) for v in w2)),"vs sparse (0,0,1) l1=1")
