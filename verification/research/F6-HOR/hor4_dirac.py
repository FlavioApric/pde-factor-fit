# F6-HOR · verifica: Dirac 1+1 libero e con gauge; varieta' caratteristica (Fitting) = Klein-Gordon doppia; proiettori di energia non razionali
import sympy as sp
t,x,m,tau,xi=sp.symbols('t x m tau xi')
g0=sp.Matrix([[1,0],[0,-1]]); g1=sp.Matrix([[0,1],[-1,0]])  # gamma^0=sigma3, gamma^1=i sigma2
ok=True
cl=[sp.simplify(g0*g0-sp.eye(2)),sp.simplify(g1*g1+sp.eye(2)),sp.simplify(g0*g1+g1*g0)]
print('Clifford (1,1):',[c==sp.zeros(2) for c in cl]); ok&=all(c==sp.zeros(2) for c in cl)
# simbolo: i gamma^mu d_mu - m  ->  -(gamma^0 tau + gamma^1 xi) - m  con d_t->-i tau? usiamo d_t -> i tau, d_x -> i xi
Sym=sp.I*(g0*sp.I*tau+g1*sp.I*xi)-m*sp.eye(2)
d=sp.factor(Sym.det()); print('det simbolo Dirac 2x2 =',d)
ok&=sp.simplify(d-(m**2+tau**2-xi**2))==0 or sp.simplify(d+(tau**2-xi**2-m**2))==0
# (i g.d + m)(i g.d - m) = -(box + m^2) I : KG*I sta nel modulo generato dalle righe di Dirac
S2=sp.I*(g0*sp.I*tau+g1*sp.I*xi)+m*sp.eye(2)
print('(Dirac+)(Dirac-) =',sp.simplify(S2*Sym)); 
# gauge: psi' = e^{i chi} psi risolve Dirac con A' = A + d chi; il simbolo principale non cambia
chi=sp.Function('chi')(t,x); psi=sp.Matrix([sp.Function('p1')(t,x),sp.Function('p2')(t,x)])
A0,A1=sp.Function('A0')(t,x),sp.Function('A1')(t,x)
def D(ps,a0,a1): return sp.I*(g0*(ps.diff(t)-sp.I*a0*ps)+g1*(ps.diff(x)-sp.I*a1*ps))-m*ps
r=sp.simplify(D(sp.exp(sp.I*chi)*psi,A0+chi.diff(t),A1+chi.diff(x))-sp.exp(sp.I*chi)*D(psi,A0,A1))
print('covarianza di gauge: residuo =',r.T); ok&=(r==sp.zeros(2,1))
# proiettori di energia: H(xi) = alpha xi + beta m, alpha=g0*g1, beta=g0 ; Lambda_pm = (1 +- H/E)/2, E = sqrt(xi^2+m^2)
al=g0*g1; be=g0; H=al*xi+be*m; E=sp.sqrt(xi**2+m**2)
print('H^2 =',sp.simplify(H*H))
Lp=(sp.eye(2)+H/E)/2
print('Lambda+ idempotente:',sp.simplify(Lp*Lp-Lp)==sp.zeros(2),' entrate non razionali in xi:',[sp.simplify(e) for e in Lp])
ok&=sp.simplify(Lp*Lp-Lp)==sp.zeros(2)
print('ESITO','OK' if ok else 'FAIL')
