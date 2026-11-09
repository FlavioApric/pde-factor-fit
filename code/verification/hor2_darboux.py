# F6-HOR · verifica: (a) encoder differenziale di Darboux per V con monodromia banale; (b) identificazione di L0 con V(x) libero
import sympy as sp, random
x,t,lam=sp.symbols('x t lambda')
f=sp.Function('f')
def L(V,g): return -sp.diff(g,x,2)+V*g
ok=True
# (a1) Poschl-Teller V=-2 sech^2 x, W = d/dx - tanh x : (-d2+V) W f = W (-d2) f  per f generica
for name,V,phi in [('Poschl-Teller -2sech^2',-2/sp.cosh(x)**2,sp.tanh(x)),('centrifugo 2/x^2',2/x**2,1/x)]:
    W=lambda g: sp.diff(g,x)-phi*g
    r=sp.simplify(sp.expand(L(V,W(f(x)))-W(L(0,f(x)))))
    print(f'intertwining [{name}]: residuo =',r); ok&=(r==0)
# (a2) stessa W manda soluzioni di i u_t = -u_xx (libera) in soluzioni con V (non autonomo ma V(x))
k1,k2=sp.Rational(1,2),sp.Rational(3,2)
v=sp.exp(sp.I*(k1*x-k1**2*t))+2*sp.exp(sp.I*(k2*x-k2**2*t))
V=-2/sp.cosh(x)**2; u=sp.diff(v,x)-sp.tanh(x)*v
r=sp.simplify((sp.I*sp.diff(u,t)+sp.diff(u,x,2)-V*u).rewrite(sp.exp))
print('Schrodinger dipendente dal tempo, u = W v: residuo =',r); ok&=(r==0)
# (b) identificazione di L0 in span{d2, d1, d3} con V(x) libero:  i u_t = L0 u + V(x) u
#     V = (i u_t - L0 u)/u deve essere indipendente da t  <=>  u(i u_tt - L0 u_t) - u_t (i u_t - L0 u) = 0  (lineare in L0)
c=sp.symbols('c1:4')
def L0(g): return c[0]*sp.diff(g,x,2)+c[1]*sp.diff(g,x)+c[2]*sp.diff(g,x,3)
def test(u,label):
    ut=sp.diff(u,t)
    E=u*(sp.I*sp.diff(u,t,2)-L0(ut))-ut*(sp.I*ut-L0(u))
    random.seed(3); rows=[]
    fE=[sp.lambdify((t,x),sp.diff(E,ci),'mpmath') for ci in c]
    f0=sp.lambdify((t,x),E.subs({ci:0 for ci in c}),'mpmath')
    import mpmath as mp
    A=[];b=[]
    for _ in range(8):
        tt,xx=random.uniform(-1,1),random.uniform(-2,2)
        A.append([complex(g(tt,xx)) for g in fE]); b.append(-complex(f0(tt,xx)))
    import numpy as np
    A=np.array(A);b=np.array(b)
    sv=np.linalg.svd(A,compute_uv=False)
    sol=np.linalg.lstsq(A,b,rcond=None)[0]
    print(f'[{label}] valori singolari del sistema lineare in (c1,c2,c3):',np.round(sv,8),' soluzione:',np.round(sol,8))
    return sv
sv=test(u,'u = W(due modi), V = -2sech^2')
ok&=(min(sv)>1e-6)   # identificazione unica attesa: L0 = -d2  (c1=-1)
# stato stazionario: u = W e^{i(kx-k^2 t)} separabile -> ogni L0 e' compatibile (V := E - L0 psi/psi): sistema degenere atteso
us=sp.diff(sp.exp(sp.I*(k1*x-k1**2*t)),x)-sp.tanh(x)*sp.exp(sp.I*(k1*x-k1**2*t))
sv2=test(us,'stato stazionario (un modo)')
ok&=(max(sv2)<1e-8)
print('ESITO','OK' if ok else 'FAIL')
