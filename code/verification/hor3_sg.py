# F6-HOR · verifica: non linearita' non polinomiali (sine-Gordon, Liouville) rese polinomiali da w = e^{iu} / soluzione generale di Liouville
import sympy as sp, random, numpy as np
x,t=sp.symbols('x t',real=True)
ok=True
a1,a2=sp.Rational(1,2),sp.Rational(2,1)
th=lambda a: a*x+t/a
# kink di u_xt = sin u
u1=4*sp.atan(sp.exp(th(a1)))
# 2-kink (forma di Hirota): tan(u/4) = g/f
g=sp.exp(th(a1))+sp.exp(th(a2)); A12=((a1-a2)/(a1+a2))**2; fH=1-A12*sp.exp(th(a1)+th(a2))
u2=4*sp.atan(g/fH)
for sgn in (-1,1):
    _f=1+sgn*A12*sp.exp(th(a1)+th(a2)); _u=4*sp.atan(g/_f); _R=sp.lambdify((t,x),sp.diff(_u,x,t)-sp.sin(_u),"mpmath")
    random.seed(11); _m=max(abs(_R(random.uniform(-1,1),random.uniform(-2,2))) for _ in range(6))
    print(f"prova segno f = 1 {sgn:+d}*A12*e^(th1+th2): max|residuo| = {float(_m):.1e}")
    if _m<1e-10: u2=_u
for name,u in [('kink',u1),('2-kink',u2)]:
    R=sp.diff(u,x,t)-sp.sin(u); fR=sp.lambdify((t,x),R,'mpmath')
    random.seed(5); m=max(abs(fR(random.uniform(-1,1),random.uniform(-2,2))) for _ in range(6))
    print(f'sine-Gordon u_xt = sin u [{name}]: max|residuo| = {float(m):.1e}'); ok&=m<1e-10
    w=sp.exp(sp.I*u)
    P=2*(w*sp.diff(w,x,t)-sp.diff(w,x)*sp.diff(w,t))-(w**3-w)
    fP=sp.lambdify((t,x),P,'mpmath'); m=max(abs(fP(random.uniform(-1,1),random.uniform(-2,2))) for _ in range(6))
    print(f'  forma polinomiale 2(w w_xt - w_x w_t) = w^3 - w con w=e^(iu): max|residuo| = {float(m):.1e}'); ok&=m<1e-10
# Liouville u_xt = e^u : e^u = 2 F'(x) G'(t)/(F+G)^2 (soluzione generale, linearizzazione di tipo Wiener)
F=sp.exp(x)+x**3/10+2; G=sp.sin(t)+t+3
u=sp.log(2*sp.diff(F,x)*sp.diff(G,t)/(F+G)**2)
R=sp.simplify(sp.diff(u,x,t)-sp.exp(u)); print('Liouville, soluzione generale: residuo =',R); ok&=(R==0)
# identificazione su dizionario D = {u_xt, sin u, u_xx, u_tt, u}: dimensione del nucleo di Gram (campionamento)
def kerdim(u,label):
    D=[sp.diff(u,x,t),sp.sin(u),sp.diff(u,x,2),sp.diff(u,t,2),u]
    fs=[sp.lambdify((t,x),d,'mpmath') for d in D]
    random.seed(7); M=[]
    for _ in range(25):
        tt,xx=random.uniform(-1.5,1.5),random.uniform(-1.5,1.5); M.append([float(fz(tt,xx)) for fz in fs])
    s=np.linalg.svd(np.array(M),compute_uv=False); s=s/s[0]
    k=int(sum(s<1e-9)); print(f'[{label}] valori singolari normalizzati {np.array2string(s,precision=2)} -> dim nucleo = {k}'); return k
k1=kerdim(u1,'kink'); k2=kerdim(u2,'2-kink')
ok&=(k1>=2 and k2==1)
print('ESITO','OK' if ok else 'FAIL')
