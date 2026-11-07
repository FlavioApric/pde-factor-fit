# OP-F5D: f di Hirota = Wronskiano (N=2,3); Crum: LA=A(-d^2), P=A d A^T commuta; Novikov; autofunzioni; Z-lemma N=1; semplicita' (1-solitone)
import sympy as sp, itertools
x=sp.symbols('x',real=True)
ok=0;tot=0
def chk(name,c):
    global ok,tot; tot+=1; ok+=bool(c); print(('OK  ' if c else 'FAIL'),name)
D=lambda e,k=1: sp.diff(e,x,k)
def wr(fs):
    n=len(fs); return sp.Matrix(n,n,lambda i,j: D(fs[j],i)).det()
def hirota(k,c):
    N=len(k); f=0
    for r_ in range(N+1):
        for S in itertools.combinations(range(N),r_):
            t=1
            for i,j in itertools.combinations(S,2): t*=((k[i]-k[j])/(k[i]+k[j]))**2
            for j in S: t*=sp.exp(k[j]*x+c[j])
            f+=t
    return f
def wr_form(k,c):
    N=len(k); ka=[kk/2 for kk in k]
    rho=[sp.prod([-(ka[a]+ka[b])/(ka[a]-ka[b]) for b in range(N) if b!=a]) for a in range(N)]
    s=[sp.exp(c[a])/rho[a] for a in range(N)]
    y=[sp.exp(-ka[a]*x)+s[a]*sp.exp(ka[a]*x) for a in range(N)]
    mu=[-kk for kk in ka]
    V0=sp.prod([mu[j]-mu[i] for i,j in itertools.combinations(range(N),2)])
    return y, sp.exp(sum(ka)*x)*wr(y)/V0
for N in (2,3):
    k=sp.symbols(f'k1:{N+1}',positive=True); c=sp.symbols(f'c1:{N+1}',real=True)
    y,F=wr_form(k,c)
    chk(f'f Hirota = e^(sum kappa x) Wr(y)/V0, N={N} (simbolico)', sp.simplify(sp.expand(F-hirota(k,c)))==0)
# Crum e Novikov su k=(1,2), c=(0,0) (esatto)
from importlib import util
k=[sp.Integer(1),sp.Integer(2)]; c=[sp.Integer(0),sp.Integer(1)]
y,F=wr_form(k,c)
u=sp.simplify(2*D(sp.log(hirota(k,c)),2))
phi=sp.Function('phi')(x)
W=wr(y)
Aop=lambda g: wr(y+[g])/W
Lop=lambda g: -D(g,2)-u*g
e=sp.simplify(Lop(Aop(phi))-Aop(-D(phi,2)))
chk('Crum: L A = A(-d^2), N=2', sp.simplify(e)==0)
# trasposta: A = sum a_j d^j ; A^T g = sum (-d)^j (a_j g)
Aphi=sp.expand(Aop(phi))
coef=[sp.simplify(Aphi.coeff(sp.Derivative(phi,(x,j)))) if j>0 else sp.simplify(Aphi.subs({sp.Derivative(phi,(x,jj)):0 for jj in range(1,4)}).coeff(phi)) for j in range(3)]
AT=lambda g: sum((-1)**j*D(coef[j]*g,j) for j in range(3))
P=lambda g: Aop(D(AT(g)))
comm=sp.simplify(P(Lop(phi))-Lop(P(phi)))
chk('P = A d A^T commuta con L, N=2', sp.simplify(comm)==0)
# Novikov: K_d[u]=0 con q_d = (l-1)(l-4) = 4 - 5l + l^2 (k_j^2 = 1,4)
v=sp.Function('v')(x)
K0=-D(u);K1=-(D(u,3)+6*u*D(u));K2=-(D(u,5)+10*u*D(u,3)+20*D(u)*D(u,2)+30*u**2*D(u))
nov=sp.simplify(4*K0-5*K1+K2)
chk('Novikov 4K0-5K1+K2 = 0 su u (N=2)', sp.simplify(nov)==0)
# autofunzioni A e^{-kappa_j x} in L^2 con autovalore -kappa_j^2
for j in range(2):
    kap=k[j]/2; g=sp.simplify(Aop(sp.exp(-kap*x)))
    chk(f'L(Ae^-kx) = -kappa^2 Ae^-kx, j={j+1}', sp.simplify(Lop(g)+kap**2*g)==0)
    chk(f'Ae^-kx -> 0 a +-inf, j={j+1}', sp.limit(g,x,sp.oo)==0 and sp.limit(g,x,-sp.oo)==0)
# Z-lemma N=1: P = A d A^T = alpha1 B1 + alpha0 B0 + beta (L-powers); B0=d, B1 = d^3 + (3/2)v d + (3/4)v'
k=[sp.Integer(2)];c=[sp.Integer(0)]
y,F=wr_form(k,c); W=wr(y); u=sp.simplify(2*D(sp.log(hirota(k,c)),2))
Aop=lambda g: wr(y+[g])/W
Aphi=sp.expand(Aop(phi)); a1=sp.simplify(Aphi.coeff(sp.Derivative(phi,x))); a0=sp.simplify(Aphi.subs(sp.Derivative(phi,x),0).coeff(phi))
AT=lambda g: -D(a1*g)+a0*g
Pp=sp.expand(sp.simplify(Aop(D(AT(phi)))))
B1=D(phi,3)+sp.Rational(3,2)*u*D(phi)+sp.Rational(3,4)*D(u)*phi
# P = -B1 + alpha0 d  (alpha0 da determinare)
rest=sp.simplify(Pp+B1)
al0=sp.simplify(rest.coeff(sp.Derivative(phi,x)))
chk('Z-lemma N=1: P + B1 = alpha0*d con alpha0 costante', sp.simplify(rest-al0*D(phi))==0 and sp.diff(al0,x)==0)
print('   alpha0 =',al0,' => q_d = alpha0*4^0 + (-1)*4^-1 l ~ l - 4 alpha0 ; atteso radice k^2=4:', sp.solve(al0-sp.Symbol('l')/4,sp.Symbol('l')))
# semplicita': 1-solitone v=2kap^2 sech^2(kap x): a'(i kap) = -i gamma int g^2 con g=1/(2cosh), gamma=1
kap=sp.symbols('kappa',positive=True); kk=sp.symbols('k')
a=(kk-sp.I*kap)/(kk+sp.I*kap)
lhs=sp.diff(a,kk).subs(kk,sp.I*kap); rhs=-sp.I*sp.integrate(1/(4*sp.cosh(kap*x)**2),(x,-sp.oo,sp.oo))
chk("a'(i kappa) = -i gamma int psi_+^2 (1-solitone)", sp.simplify(lhs-rhs)==0)
psi=sp.exp(sp.I*kk*x)*(kk+sp.I*kap*sp.tanh(kap*x))/(kk+sp.I*kap)
chk('psi_+ risolve -psi''-2kap^2 sech^2 psi = k^2 psi', sp.simplify(-D(psi,2)-2*kap**2/sp.cosh(kap*x)**2*psi-kk**2*psi)==0)
print(f'TOTALE {ok}/{tot}')
