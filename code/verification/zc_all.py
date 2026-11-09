# OP-F5D: (ZC) per ogni n (n<=5) via serie W, A^2+BC=1; flussi T_n=-2^n B_{n+1}; riduzione r=-conj(q)
import sympy as sp
x,z=sp.symbols('x zeta'); q=sp.Function('q')(x); r=sp.Function('r')(x)
D=lambda e,k=1: sp.diff(e,x,k)
ok=0;tot=0
def chk(name,c):
    global ok,tot; tot+=1; ok+=bool(c); print(('OK  ' if c else 'FAIL'),name)
M=8
A=[sp.Integer(1)];B=[sp.Integer(0)];C=[sp.Integer(0)]
for m in range(0,M):
    B.append(sp.expand(sp.I/2*(D(B[m])+2*q*A[m])))
    C.append(sp.expand(-sp.I/2*(D(C[m])-2*r*A[m])))
    mm=m+1
    s=sum(A[i]*A[mm-i] for i in range(1,mm))+sum(B[i]*C[mm-i] for i in range(0,mm+1))
    A.append(sp.expand(-s/2))
for m in range(0,M):
    chk(f'A_{m}x = qC_m - rB_m', sp.expand(D(A[m])-q*C[m]+r*B[m])==0)
U=sp.Matrix([[-sp.I*z,q],[r,sp.I*z]])
for n in range(0,6):
    V=sp.zeros(2,2)
    for m in range(0,n+1):
        V+=z**(n-m)*sp.Matrix([[A[m],B[m]],[C[m],-A[m]]])
    R=(V.diff(x)-(U*V-V*U)).applyfunc(sp.expand)
    target=sp.Matrix([[0,-2*sp.I*B[n+1]],[2*sp.I*C[n+1],0]]).applyfunc(sp.expand)
    chk(f'V_{n,x}-[U,V_n] = offdiag(-2iB_(n+1), 2iC_(n+1)) indip. da zeta', (R-target).applyfunc(sp.expand)==sp.zeros(2,2))
# confronto con T_n del progetto (r=-conj q): q,qb indipendenti
qb=sp.Function('qb')(x)
red=lambda e: sp.expand(e.subs(r,-qb).doit())
T={0:sp.I*q,1:D(q),2:sp.I*(D(q,2)+2*q*qb*q),3:-(D(q,3)+6*q*qb*D(q))}
chk('T_0 = +-(-B_1)', sp.expand(red(-B[1])+T[0])==0)
for n in (1,2,3):
    chk(f'T_{n} = -2^n B_(n+1)', sp.expand(red(-2**n*B[n+1])-T[n])==0)
# riduzione: con r=-conj q, C_m = conj(B_m), A_m reale. Verifica simbolica con q=a+ib reali
a=sp.Function('a')(x); b=sp.Function('b')(x)
for m in range(1,M):
    Bm=sp.expand(B[m].subs(r,-(a-sp.I*b)).subs(q,a+sp.I*b).doit())
    Cm=sp.expand(C[m].subs(r,-(a-sp.I*b)).subs(q,a+sp.I*b).doit())
    Am=sp.expand(A[m].subs(r,-(a-sp.I*b)).subs(q,a+sp.I*b).doit())
    cj=lambda e: sp.expand(e.xreplace({sp.I:-sp.I}))
    chk(f'riduzione m={m}: C=conj(B), A reale', sp.expand(Cm-cj(Bm))==0 and sp.expand(Am-cj(Am))==0)
# senza termine costante per m>=1
for m in range(1,M):
    s0={q:0,r:0}
    chk(f'W_{m} senza termine costante', all(sp.expand(e.subs({sp.Derivative(q,(x,k)):0 for k in range(1,20)}).subs({sp.Derivative(r,(x,k)):0 for k in range(1,20)}).subs(s0))==0 for e in (A[m],B[m],C[m])))
print(f'TOTALE {ok}/{tot}')
