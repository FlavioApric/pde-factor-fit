import sympy as sp
t,x,y=sp.symbols('t x y',real=True)
I=sp.I
print("== K1: N1(iii) senza L in Ann(u): u=e^t, N=2, n=1, L=tau+5")
tau,xi=sp.symbols('tau xi')
u=sp.exp(t)
# Ann(u) ∩ R_{<=1}: a+b*tau+c*xi applied: a u + b u_t + c u_x = (a+b) e^t
a,b,c=sp.symbols('a b c')
print(" condizione Ann:", sp.simplify((a*u+b*sp.diff(u,t)+c*sp.diff(u,x))/u), "=0 -> span{tau-1, xi}")
print(" (tau+5) applicato a u / u =", sp.simplify((sp.diff(u,t)+5*u)/u), "!= 0 -> tau+5 non in Ann(u): inclusione falsa")
print("== K2: (a') u=t, m=1, N=2: theta0*u + theta1*u_x = -u_t")
u=t
print(" in t=0: u=",u.subs(t,0)," u_x=",sp.diff(u,x)," -u_t=",-sp.diff(u,t)," -> nessuna legge: identificabile per vacuita'")
print("== K3: V reale, u=e^{-it}(x+x^2)")
u=sp.exp(-I*t)*(x+x**2)
r=sp.simplify((I*sp.diff(u,t)+sp.diff(u,x,2))/u)
print(" (iu_t+u_xx)/u =",r," Im =",sp.simplify(sp.im(r)))
print(" in x=0: u=",u.subs(x,0)," iu_t+u_xx=",sp.simplify((I*sp.diff(u,t)+sp.diff(u,x,2)).subs(x,0)))
print("== K4: esempio del testo u=e^{-it}(2+cos x)+itx/5")
u=sp.exp(-I*t)*(2+sp.cos(x))+I*t*x/5
r=(I*sp.diff(u,t)+sp.diff(u,x,2))/u
for p in [(0.3,0.7),(0.7,0.3)]:
    print(" (t,x)=",p," V=",sp.N(r.subs({t:p[0],x:p[1]})))
print("== K5: trasporto u=t+psi(x), psi'=0 su intervallo: u_x=0,u_t=1 -> nessuna legge")
print("== K6: Schrodinger magnetico 2D: u=rho e^{iS}, A=0; B a div nulla con div(rho^2 B)!=0")
rho=2+sp.cos(x); S=y
u=rho*sp.exp(I*S)
B=(sp.Integer(0),sp.Integer(1))  # div B=0
divB=sp.diff(B[0],x)+sp.diff(B[1],y)
lapA=lambda f,A: sp.diff(f,x,2)+sp.diff(f,y,2)-2*I*(A[0]*sp.diff(f,x)+A[1]*sp.diff(f,y))-I*(sp.diff(A[0],x)+sp.diff(A[1],y))*f-(A[0]**2+A[1]**2)*f
diff=sp.simplify((lapA(u,B)-lapA(u,(0,0)))/u)
print(" div B=",divB," [(grad-iB)^2-(grad)^2]u/u =",diff)
print(" Im =",sp.simplify(sp.im(sp.expand_complex(diff))),"  -> serve Delta V reale =",sp.simplify(sp.re(sp.expand_complex(diff))),"; con Im=0 ok per questo B")
B=(sp.sin(y),sp.Integer(0)) # div B=0, B.grad rho !=0
diff=sp.simplify((lapA(u,B)-lapA(u,(0,0)))/u)
print(" B=(sin y,0): div=",sp.diff(B[0],x)," Im della differenza/u =",sp.simplify(sp.im(sp.expand_complex(diff))))
print("   -> non nullo: nessun V reale compensa; div(rho^2 B)=",sp.simplify(sp.diff(rho**2*B[0],x)))
