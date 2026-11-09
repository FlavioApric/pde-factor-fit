# RT-R3a: polinomi del calore di Rosenbloom-Widder v_n(x,t)=n! sum_k x^(n-2k) t^k/(k!(n-2k)!)  (u_t=u_xx)
import sympy as sp
x,t=sp.symbols('x t',real=True); s=sp.symbols('s',positive=True)
def v(n,X,T): return sp.factorial(n)*sum(X**(n-2*k)*T**k/(sp.factorial(k)*sp.factorial(n-2*k)) for k in range(n//2+1))
G=sp.exp(-x**2/(4*s))/sp.sqrt(4*sp.pi*s)
print("heat eq residuals n<=6:",[sp.simplify(sp.diff(v(n,x,t),t)-sp.diff(v(n,x,t),x,2)) for n in range(7)])
ok=True
for n in range(6):
    for m in range(6):
        I=sp.simplify(sp.integrate(v(n,x,-s)*v(m,x,-s)*G,(x,-sp.oo,sp.oo)))
        exp_=(2*s)**n*sp.factorial(n) if n==m else 0
        if sp.simplify(I-exp_)!=0: ok=False; print("FAIL",n,m,I)
print("orthogonality int v_n(x,-s)v_m(x,-s)G_s dx = (2s)^n n! delta_nm  (n,m<6):",ok)
# Mehler: reproducing kernel of the resulting Hilbert space at time -s, check first terms numerically
print("v_n(x,-1/2)=He_n(x/?)... compare v_4(x,-1/2) with hermite_prob He_4(x)? ",sp.expand(v(4,x,-sp.Rational(1,2))), "|", sp.expand(sp.hermite_prob(4,x)) if hasattr(sp,'hermite_prob') else "n/a")
print("v_4(x,-1/4)*2^4 vs physicists' H_4:",sp.expand(2**4*v(4,x,-sp.Rational(1,4))),"|",sp.expand(sp.hermite(4,x)))
