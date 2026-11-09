# R7-S2: KdV u_t + 6 u u_x + u_xxx = 0 ; u = 2 (log f)_xx ; N-solitoni di Hirota
import sympy as sp, itertools, random
x,t=sp.symbols('x t',real=True)
k=sp.symbols('k1:4',positive=True)
eta=[ki*x-ki**3*t for ki in k]
A=lambda i,j: ((k[i]-k[j])/(k[i]+k[j]))**2
def tau(N):
    f=0
    for mu in itertools.product([0,1],repeat=N):
        e=sum(mu[i]*eta[i] for i in range(N))
        c=sp.Mul(*[A(i,j) for i in range(N) for j in range(i+1,N) if mu[i] and mu[j]])
        f+=c*sp.exp(e)
    return f
def kdv(u): return sp.diff(u,t)+6*u*sp.diff(u,x)+sp.diff(u,x,3)
def hirota(f):  # (D_x D_t + D_x^4) f.f
    fx,ft=sp.diff(f,x),sp.diff(f,t)
    DxDt=2*(f*sp.diff(f,x,t)-fx*ft)
    Dx4=2*(f*sp.diff(f,x,4)-4*fx*sp.diff(f,x,3)+3*sp.diff(f,x,2)**2)
    return DxDt+Dx4
for N in (1,2):
    f=tau(N); u=2*sp.diff(sp.log(f),x,2)
    print(f"S2a N={N}: Hirota bilineare = 0:", sp.simplify(sp.expand(hirota(f)))==0, "; KdV residuo = 0:", sp.simplify(kdv(u))==0)
f3=tau(3)
H3=sp.powsimp(sp.expand(hirota(f3)));terms=sp.collect(H3,[sp.exp(a) for a in []],evaluate=False)
d={}
for term in sp.Add.make_args(H3):
    c,e=term.as_independent(x,t)
    d[e]=d.get(e,0)+c
print("S2b N=3: Hirota bilineare = 0 (coeff. per esponenziale):", all(sp.simplify(c)==0 for c in d.values()), "; #esponenziali distinti:", len(d))
# sfasamento 2-solitone (k1>k2): soliton 1 a t->+inf ha fase eta1+log A12
f2=tau(2); A12=A(0,1)
print("S2c A12 =", sp.factor(A12), "; shift posizione soliton veloce dx1 = -log(A12)/k1 > 0, lento dx2 = +log(A12)/k2 < 0")
# massa: int u dx = 2[(log f)_x]_{-inf}^{+inf} = 2(k1+k2) = somma delle masse singole -> int E_int dx = 0
lf=sp.diff(sp.log(f2),x)
lf=lf.subs({t:0,k[0]:2,k[1]:1}); Lp=sp.limit(lf,x,sp.oo); Lm=sp.limit(lf,x,-sp.oo)
print("S2d massa 2-solitone (k1=2,k2=1):", 2*(Lp-Lm), " = 2k1+2k2 = 6 => int E_int dx = 0")
# Lax pair: L=-D^2+u, P=-4D^3-6uD-3u_x ; L_t=[P,L] <=> KdV (forma u_t+6uu_x+u_xxx=0)
U=sp.Function('u')(x,t); w=sp.Function('w')(x)
Lop=lambda g: -sp.diff(g,x,2)+U*g
Pop=lambda g: -4*sp.diff(g,x,3)-6*U*sp.diff(g,x)-3*sp.diff(U,x)*g
comm=sp.expand(Pop(Lop(w))-Lop(Pop(w)))
print("S2e [P,L]w =", sp.simplify(comm), " ; quindi L_t=[P,L] <=> u_t = -6uu_x - u_xxx")
# Miura: u = -(v^2 + v_x) ; KdV[u] = -(2v + D)(mKdV[v]) con mKdV: v_t - 6 v^2 v_x + v_xxx
V=sp.Function('v')(x,t); um=-(V**2+sp.diff(V,x))
mk=sp.diff(V,t)-6*V**2*sp.diff(V,x)+sp.diff(V,x,3)
print("S2f Miura:", sp.simplify(kdv(um)+(2*V*mk+sp.diff(mk,x)))==0)
