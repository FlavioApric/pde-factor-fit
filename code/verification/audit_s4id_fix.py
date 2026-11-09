# audit_s4id_fix.py — S-CHECK-10: ricontrollo dei 3 FAIL di audit_s4id_part2.out (errori dello script, non dei claim?)
import sys, itertools, random
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
random.seed(7)
res=[]
def check(n,ok,info=""):
    res.append(bool(ok)); print(("OK   " if ok else "FAIL ")+n+("  | "+str(info) if info!="" else "")); sys.stdout.flush()
# (1) P7(iii): u_xx/u_x come funzione di u per il 1-shock, verifica con riscrittura in E e numerica
x,t,k,nu=sp.symbols('x t k nu',positive=True); Es=sp.Symbol('E',positive=True)
u=-2*nu*k*Es/(1+Es)            # funzione di E, con dE/dx = k E
dx=lambda f: sp.diff(f,Es)*k*Es
ux=sp.simplify(dx(u)); uxx=sp.simplify(dx(ux))
H=sp.simplify(uxx/ux)
for cand in [k+u/nu, -k-u/nu]:
    print("INFO u_xx/u_x - (%s) = %s" % (cand, sp.simplify(H-cand)))
ok = any(sp.simplify(H-c)==0 for c in [k+u/nu,-k-u/nu])
Ef=sp.exp(k*x+nu*k**2*t); uf=-2*nu*k*Ef/(1+Ef)
burg=sp.simplify((sp.diff(uf,t)+uf*sp.diff(uf,x)-nu*sp.diff(uf,x,2)).rewrite(sp.exp))
check("P7(iii) 1-shock: u_xx = H(u) u_x con H affine (globale) e u risolve Burgers", ok and burg==0, "H = %s, Burgers residuo = %s"%(H,burg))
# (2) T2(c): dim (R_N, D R_N) ∩ A_{<=N+1,<=N+1} calcolata direttamente dall'ideale, contro il valore misurato (3 per N=1, 4 per N=2)
Y=sp.symbols('y0:8'); w=sp.symbols('w0:8')
def Dx(p): return sp.expand(sum(sp.diff(p,Y[j])*Y[j+1] for j in range(7)))
def bell(m):
    B=[sp.Integer(1)]
    for _ in range(m): p=B[-1]; B.append(sp.expand(sum(sp.diff(p,w[j])*w[j+1] for j in range(7))+w[0]*p))
    return B
YB=bell(4); z=sp.Symbol('z'); nuv=sp.Rational(1,3)
def RN(ks):
    pol=sp.Poly(sp.expand(z*sp.prod([z-q for q in ks])),z)
    sub={w[j]:-Y[j]/(2*nuv) for j in range(7)}
    return sp.expand(sum(pol.coeff_monomial(z**m)*YB[m].subs(sub,simultaneous=True) for m in range(1,len(ks)+2)))
measured={1:3,2:4}
for ks in [[2],[1,3]]:
    N=len(ks); R=RN([sp.Integer(q) for q in ks]); DR=Dx(R); K=N+1; d=N+1
    vars_=Y[:K+1]
    # moltiplicatori di grado <= G
    G=3
    mons=[sp.prod(c) if c else sp.Integer(1) for e in range(G+1) for c in itertools.combinations_with_replacement(vars_,e)]
    gens=[sp.expand(m*R) for m in mons]+[sp.expand(m*DR) for m in mons]
    allm={}
    def vec(p):
        P=sp.Poly(p,*vars_); return {mm:c for mm,c in P.terms()}
    vs=[vec(g) for g in gens]
    keys=sorted(set().union(*[v.keys() for v in vs]),key=lambda m:(-sum(m),m))
    hi=[kk for kk in keys if sum(kk)>d]; lo=[kk for kk in keys if sum(kk)<=d]
    A=sp.Matrix([[v.get(kk,0) for v in vs] for kk in hi+lo])
    # combinazioni con parte di grado > d nulla: nucleo del blocco alto, poi rango dell'immagine nel blocco basso
    Ahi=A[:len(hi),:]; Alo=A[len(hi):,:]
    ns=Ahi.nullspace()
    img=sp.Matrix.hstack(*[Alo*v for v in ns]) if ns else sp.zeros(len(lo),1)
    dimI=img.rank()
    check("T2(c) N=%d: dim (R_N, D R_N)∩A_{<=N+1,<=N+1} (moltiplicatori di grado <= %d) = %d = dim J_u∩A_{<=N+1,<=N+1} misurato %d"%(N,G,dimI,measured[N]), dimI==measured[N])
print("== Totale fix: %d/%d OK"%(sum(res),len(res)))
