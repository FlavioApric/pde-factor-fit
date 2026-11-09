# KA check of CONV-T1(6) and dimension remark: compute N_{m,K}, m*(K), O_K from jets.
import itertools, sympy as sp
from functools import reduce

def monos(nv, m):
    return [a for d in range(m+1) for a in itertools.product(range(d+1), repeat=nv) if sum(a)==d]

def run(u, vars_, Kmax, label):
    nv=len(vars_); Y=sp.symbols('Y0:%d'%nv)
    jet={}
    for a in monos(nv,Kmax):
        e=u
        for v,k in zip(vars_,a): e=sp.diff(e,v,k)
        jet[a]=sp.nsimplify(e.subs({v:0 for v in vars_}))
    out=[]
    for K in range(0,Kmax+1):
        mstar=None
        for m in range(0,K+1):
            A=monos(nv,m); B=monos(nv,K-m)
            M=sp.Matrix([[jet[tuple(x+y for x,y in zip(a,b))] for a in A] for b in B])
            ns=M.nullspace()
            if ns:
                polys=[sp.expand(sum(c*sp.Mul(*[Y[i]**a[i] for i in range(nv)]) for c,a in zip(v,A))) for v in ns]
                g=reduce(sp.gcd,polys)
                g=sp.Poly(g,*Y).monic().as_expr() if sp.Poly(g,*Y).total_degree()>0 else 1
                out.append((K,m,g)); mstar=m; break
        if mstar is None: out.append((K,None,None))
    print(label, out)

t,x,y=sp.symbols('t x y')
for N in range(0,4):
    run(1+x**(N+2)*sp.exp(x**2),[t,x],N+4,'n=2 N=%d (Y0=tau,Y1=xi):'%N)
for N in range(0,2):
    run(1+x**(N+2)*sp.exp(x**2),[t,x,y],N+4,'n=3 ORIGINAL N=%d:'%N)
    run(1+x**(N+2)*sp.exp(x**2+y**2),[t,x,y],N+5,'n=3 REPAIRED N=%d:'%N)
