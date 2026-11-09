# Verifica (non metodo) per P2-C2 (ripresa audit 4): N >= 3 sottospazi, gamma_N.
import sympy as sp
ok=0; tot=0
def chk(name, cond):
    global ok, tot
    tot+=1; ok+=bool(cond); print(("PASS " if cond else "FAIL ")+name)
e=sp.symbols('epsilon', positive=True)
v=[sp.Matrix([sp.cos(e)*sp.cos(2*sp.pi*k/3), sp.cos(e)*sp.sin(2*sp.pi*k/3), sp.sin(e)]) for k in range(3)]
# coseni a coppie (rette: c_F = |<v_i,v_j>|)
c=[sp.simplify((v[i].T*v[j])[0]) for i,j in [(0,1),(0,2),(1,2)]]
chk("C2a coseni a coppie = -cos^2/2 + sin^2", all(sp.simplify(ci-(-sp.cos(e)**2/2+sp.sin(e)**2))==0 for ci in c))
S=sp.Matrix.hstack(*v)
SSt=sp.simplify(S*S.T)
chk("C2b S S^T = diag(3/2 cos^2, 3/2 cos^2, 3 sin^2)", sp.simplify(SSt-sp.diag(sp.Rational(3,2)*sp.cos(e)**2,sp.Rational(3,2)*sp.cos(e)**2,3*sp.sin(e)**2))==sp.zeros(3))
# gamma_3 = lambda_min(S^T S) = lambda_min(S S^T) (S quadrata invertibile per eps in (0,pi/2))
for ev in [sp.Rational(1,10), sp.Rational(1,100), sp.Rational(1,1000)]:
    G=(S.T*S).subs(e,ev)
    lam=min(sp.N(x,30) for x in G.eigenvals())
    cF=abs(sp.N(c[0].subs(e,ev),30))
    chk(f"C2c eps={ev}: gamma_3={float(lam):.3e} = 3 sin^2 eps, c_F a coppie={float(cF):.4f} < 1/2", abs(lam-3*sp.sin(ev)**2)<1e-25 and cF<0.5)
# Gershgorin / norma di C: per tre rette c_nm = |c|, ||C|| = 2|c|; bound gamma >= 1-2|c|
for ev in [sp.Rational(1,10), sp.Rational(1,3), sp.Rational(1,2)]:
    G=(S.T*S).subs(e,ev); lam=min(sp.N(x,30) for x in G.eigenvals()); cc=abs(sp.N(c[0].subs(e,ev),30))
    chk(f"C2d eps={ev}: gamma_3 = {float(lam):.4f} >= 1 - ||C|| = {float(1-2*cc):.4f}", lam >= 1-2*cc-1e-25)
# caso generale casuale (numpy): N=4 sottospazi 2-dim di R^9 a intersezioni nulle; gamma_N >= 1-||C||
import numpy as np, itertools
rng=np.random.default_rng(1)
for trial in range(6):
    bases=[np.linalg.qr(rng.standard_normal((9,2)))[0] for _ in range(4)]
    N=len(bases); C=np.zeros((N,N))
    for i,j in itertools.permutations(range(N),2):
        C[i,j]=np.linalg.norm(bases[i].T@bases[j],2)
    Sf=np.hstack(bases); lam=np.linalg.eigvalsh(Sf.T@Sf).min(); nC=np.abs(np.linalg.eigvalsh(C)).max()
    chk(f"C2e prova {trial}: gamma_4={lam:.4f} >= 1-||C||={1-nC:.4f}", lam >= 1-nC-1e-12)
# somma diretta di blocchi eps_k -> 0: c_F a coppie sup = 1/2 (<1), gamma_3 = inf 3 sin^2 eps_k = 0
cs=[abs(-np.cos(2.0**-k)**2/2+np.sin(2.0**-k)**2) for k in range(1,30)]
gs=[3*np.sin(2.0**-k)**2 for k in range(1,30)]
chk(f"C2g blocchi: sup c_F a coppie = {max(cs):.6f} <= 1/2, inf gamma_3 -> {min(gs):.2e}", max(cs)<=0.5 and min(gs)<1e-15)
# N=2: gamma = 1 - c_F (coerenza con T3) per due rette
th=sp.Rational(3,10)
a=sp.Matrix([1,0]); b=sp.Matrix([sp.cos(th),sp.sin(th)])
G=sp.Matrix.hstack(a,b).T*sp.Matrix.hstack(a,b)
chk("C2f N=2: lambda_min = 1 - cos(theta)", abs(min(sp.N(x,30) for x in G.eigenvals())-sp.N(1-sp.cos(th),30))<1e-25)
print(f"\nTOTALE: {ok}/{tot} PASS")
