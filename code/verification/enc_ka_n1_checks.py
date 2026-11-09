import sympy as sp
t,x,c,lam,x0=sp.symbols('t x c lambda x0',real=True)
q=sp.Function('q')(x); u=sp.Function('u')(t,x); th=sp.Function('theta')(t)
S=lambda w,V: sp.I*sp.diff(w,t)+sp.diff(w,x,2)-V*w   # Schrodinger residual i w_t = -w_xx + V w
# (a) phase e^{i theta(t)} u: residual for potential q when u solves for q
w=sp.exp(sp.I*th)*u
res=sp.simplify(sp.expand(S(w,q)/sp.exp(sp.I*th)-S(u,q)))
print("(a) extra residual of e^{i th}u:",res, " -> e^{i th}u solves V=q - th'(t)")
# (b) e^{-ict} maps q-solutions to (q+c)-solutions
w2=sp.exp(-sp.I*c*t)*u
print("(b)",sp.simplify(sp.expand(S(w2,q+c)/sp.exp(-sp.I*c*t)-S(u,q))))
# (c) identification under DM-phi: (i w_t + w_xx)/w = q - th'
print("(c)",sp.simplify((sp.I*sp.diff(w,t)+sp.diff(w,x,2))/w - (sp.I*sp.diff(u,t)+sp.diff(u,x,2))/u))
# (d) strict family on q0=0, class {c}: u=e^{-i lam t}cos(sqrt(lam)(x-x0)) common (saturated) element.
k=sp.sqrt(lam); phi=sp.cos(k*(x-x0)); uu=sp.exp(-sp.I*lam*t)*phi
print("(d) uu solves V=0:",sp.simplify(S(uu,0)), "; e^{-ict}uu solves V=c:",sp.simplify(S(sp.exp(-sp.I*c*t)*uu,c)))
# strict W_c maps phi (eigenfn of L_c with eigenvalue lam+c, Cauchy data (1,0)) to free eigenfn same Cauchy data
out0=uu; outc=sp.exp(-sp.I*lam*t)*sp.cos(sp.sqrt(lam+c)*(x-x0))
ratio=sp.simplify(outc/out0)
print("(d) ratio W_c uu / W_0 uu =",ratio," depends on x ->",sp.diff(ratio,x)!=0)
