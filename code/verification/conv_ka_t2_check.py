# KA CONV-T2: (1) lemma di evitamento: K0(m,L) finito, rango pieno righe |beta|>L,
# anche con g=e^{|z|^2} (punto (ii) superfluo); (2) riparazione corollario:
# v = q + eps t^{N-1} e^{|x|^2}, verifica Ann(v) ∩ R_{<=D} = (tau^N) ∩ R_{<=D}.
import itertools, sympy as sp
t,x=sp.symbols('t x')
def mids(n,K):
    return [a for k in range(K+1) for a in itertools.product(range(k+1),repeat=n) if sum(a)==k]
def jet(f,K):
    P=sp.series(f.subs({t:sp.Symbol('s')*t, x:sp.Symbol('s')*x}),sp.Symbol('s'),0,K+1).removeO()
    P=sp.expand(P.subs(sp.Symbol('s'),1)); poly=sp.Poly(P,t,x)
    return {g: poly.coeff_monomial(t**g[0]*x**g[1])*sp.factorial(g[0])*sp.factorial(g[1]) for g in mids(2,K)}
def rank_rows(j,m,K,L):
    cols=mids(2,m); rows=[b for b in mids(2,K-m) if sum(b)>L]
    if not rows: return 0,len(cols)
    M=sp.Matrix([[j[(a[0]+b[0],a[1]+b[1])] for a in cols] for b in rows]); return M.rank(),len(cols)
for (m,L) in [(1,0),(1,2),(2,1),(2,3)]:
    for name,g in [('|z|^{2(L+1)}e^{|z|^2}',(t**2+x**2)**(L+1)*sp.exp(t**2+x**2)),('e^{|z|^2}',sp.exp(t**2+x**2))]:
        for K in range(m+L+1,m+L+12):
            j=jet(g,K); r,c=rank_rows(j,m,K,L)
            if r==c: print(f"m={m} L={L} g={name}: K0={K} (rango {r}=dim R_<=m)"); break
        else: print(f"m={m} L={L} g={name}: non trovato K0 fino a {K}")
# (2) riparazione: N=3, q polinomio di grado <=1, v=q+ (1/2!) t^2 e^{x^2}; Ann(v) cap R_{<=D}
N=3; v=1+2*t-x+sp.Rational(1,2)*t**2*sp.exp(x**2); D=4; Kj=16
j=jet(v,Kj); cols=mids(2,D); rows=[b for b in mids(2,Kj-D)]
M=sp.Matrix([[j[(a[0]+b[0],a[1]+b[1])] for a in cols] for b in rows])
ns=M.nullspace()
print("dim N_{D,K}(v) =",len(ns)," atteso dim (tau^3) cap R_<=4 =",sum(1 for a in cols if a[0]>=N))
ok=all(all(vec[i]==0 for i,a in enumerate(cols) if a[0]<N) for vec in ns)
print("nucleo contenuto in span{tau^a xi^b: a>=3}:",ok)
