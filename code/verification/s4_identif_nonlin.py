# R7-S4: identificazione lineare nei parametri con dizionario non lineare (G7): ker del "Gram" esatto
# u_N-solitone KdV (u_t+6uu_x+u_xxx=0) come funzione razionale di E_i=exp(eta_i); relazioni lineari esatte tra i termini
import sympy as sp, itertools
def run(ks):
    N=len(ks); E=sp.symbols(f'E1:{N+1}',positive=True)
    Dx=lambda p: sp.together(sum(ks[i]*E[i]*sp.diff(p,E[i]) for i in range(N)))
    Dt=lambda p: sp.together(sum(-ks[i]**3*E[i]*sp.diff(p,E[i]) for i in range(N)))
    A=lambda i,j: sp.Rational((ks[i]-ks[j])**2,(ks[i]+ks[j])**2)
    f=sum(sp.Mul(*[A(i,j) for i in range(N) for j in range(i+1,N) if mu[i] and mu[j]])*sp.Mul(*[E[i]**mu[i] for i in range(N)]) for mu in itertools.product([0,1],repeat=N))
    lf=Dx(sp.log(f)); u=sp.together(2*Dx(lf))
    ux=Dx(u); uxx=Dx(ux); uxxx=Dx(uxx); ut=Dt(u)
    names=['u_t','u_x','u','u^2','u*u_x','u_xx','u_xxx']
    T=[ut,ux,u,u**2,u*ux,uxx,uxxx]
    c=sp.symbols(f'c0:{len(T)}')
    num=sp.numer(sp.together(sum(ci*Ti for ci,Ti in zip(c,T))))
    eqs=sp.Poly(sp.expand(num),*E).coeffs()
    Mx=sp.Matrix([[sp.diff(e,ci) for ci in c] for e in eqs])
    ns=Mx.nullspace()
    print(f"k={ks}: dim ker = {len(ns)}")
    for v in ns: print("   relazione:", " + ".join(f"({sp.nsimplify(vi)})*{n}" for vi,n in zip(v,names) if vi!=0))
run([1]); run([2,1])
