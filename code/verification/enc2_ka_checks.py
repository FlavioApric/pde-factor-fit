# KA ENC2 checks (attaccante indipendente)
import sympy as sp
t,x,al,tau,sig=sp.symbols('t x alpha tau sigma')
print("== A. Leading term of P(alpha,L_q)(x-x1)^M, x1=0, q generic Taylor (order 12) ==")
qs=sp.symbols('q0:13')
q=sum(qs[k]*x**k for k in range(13))
def Lq(f): return sp.expand(-sp.diff(f,x,2)+q*f)
def lowest(expr):
    p=sp.Poly(sp.expand(expr),x); terms=sorted(p.terms(),key=lambda m:m[0][0])
    return terms[0][0][0], sp.factor(terms[0][1])
for (d,M) in [(1,3),(2,5),(3,7),(2,8)]:
    ps=sp.symbols('p0:%d'%(d+1))
    f=x**M; acc=0; g=f
    for j in range(d+1):
        acc+=ps[j]*g; g=Lq(g)
    o,c=lowest(acc)
    expected=ps[d]*(-1)**d*sp.factorial(M)/sp.factorial(M-2*d)
    print(f"d={d} M={M}: lowest order {o} (expected {M-2*d}), coeff {c}, matches={sp.simplify(c-expected)==0}")
print("== A2. q-term is not a 'higher power' polynomial: L_q x^3 with q=1/(1+x) ==")
print(sp.simplify(-sp.diff(x**3,x,2)+x**3/(1+x)))
print("== B. u=exp(x^2), q=0, u'=u+exp(alpha t) x^M: Ann not principal ==")
M=5; alpha=sp.Integer(2)
u1=sp.exp(x**2)+sp.exp(alpha*t)*x**M
def act(P,u):
    P=sp.Poly(P,tau,sig); r=0
    for (a,b),c in P.terms():
        v=u
        for _ in range(b): v=-sp.diff(v,x,2)
        v=sp.diff(v,t,a); r+=c*v
    return sp.simplify(r)
k=M//2+1
print("tau*(tau-alpha) annihilates:",act(tau*(tau-alpha),u1)==0)
print("tau*sigma^%d annihilates:"%k,act(tau*sig**k,u1)==0)
print("gcd =",sp.gcd(tau*(tau-alpha),tau*sig**k),"; tau annihilates:",act(tau,u1)==0,"; 1 annihilates:",u1==0)
print("modified h = exp(alpha t) x^M exp(x^2): tau*(tau-alpha) annihilates:",act(tau*(tau-alpha),sp.exp(x**2)+sp.exp(alpha*t)*x**M*sp.exp(x**2))==0)
print("== C. Degree-<=1 prior: 4-jet of u=exp(x^2) at (0,0) forces P=c1*tau ==")
c0,c1,c2=sp.symbols('c0 c1 c2')
# jet of u' up to order 4: equals exp(x^2) jet, zero t-derivatives
jet=sp.series(sp.exp(x**2),x,0,5).removeO()
expr=c0*jet+c1*0-c2*(-1)*(-sp.diff(jet,x,2))  # P=c0+c1 tau+c2 sigma, sigma=-d_xx; u'_t jet=0 up to order 3
# P u' must vanish to order 2 in x at 0 (derivatives up to 2 of P u' involve only 4-jet)
e2=sp.expand(c0*jet+c2*(-sp.diff(jet,x,2)))
eqs=[sp.expand(e2).coeff(x,0), sp.expand(e2).coeff(x,1), sp.expand(e2).coeff(x,2)]
print("equations:",eqs,"solution:",sp.solve(eqs,[c0,c2],dict=True))
print("== D. Counterexample to P0(b)^loc: W(g + w*f)=g on X (+) wX, V=t*w, c=0 ==")
F=sp.Function('f')(x); w=sp.Function('w')(x)
LVf=-sp.diff(F,x,2)+t*w*F
Xpart=-sp.diff(F,x,2); Ypart_coeff=t*F   # LVf = Xpart + w*(t f)
print("decomposition exact:",sp.simplify(LVf-(Xpart+w*Ypart_coeff))==0)
print("W(L_V f) = Xpart =",Xpart,"; (-d_xx)(W f) = (-d_xx) f =",-sp.diff(F,x,2),"; equal:",sp.simplify(Xpart+sp.diff(F,x,2))==0)
print("V(t)-V(s) = (t-s)*w(x), not constant in x unless w const")
