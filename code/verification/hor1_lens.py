# F6-HOR · verifica (non metodo): trasformazione di lente / Niederer (encoder puntuale che rimuove V = w^2 x^2/2)
# u(t,x) = cos(wt)^(-1/2) exp(-i w x^2 tan(wt)/2) v(tan(wt)/w, x/cos(wt)),  i v_s = -1/2 v_yy
# tesi: i u_t = -1/2 u_xx + 1/2 w^2 x^2 u
import sympy as sp, random
t,x=sp.symbols('t x',real=True); w=sp.Rational(7,5)
k1,k2,a=sp.Rational(3,2),sp.Rational(-2,3),sp.Rational(1,2)
S=sp.tan(w*t)/w; Y=x/sp.cos(w*t)
pref=sp.cos(w*t)**sp.Rational(-1,2)*sp.exp(-sp.I*w*x**2*sp.tan(w*t)/2)
tests={
 'due onde piane libere': sp.exp(sp.I*k1*Y-sp.I*k1**2*S/2)+3*sp.exp(sp.I*k2*Y-sp.I*k2**2*S/2),
 'gaussiana libera': (1+sp.I*S/a)**sp.Rational(-1,2)*sp.exp(-Y**2/(2*(a+sp.I*S))),
}
random.seed(1); ok=True
for name,v in tests.items():
    U=pref*v
    R=sp.I*sp.diff(U,t)+sp.Rational(1,2)*sp.diff(U,x,2)-sp.Rational(1,2)*w**2*x**2*U
    m=0; fR=sp.lambdify((t,x),R,"mpmath"); fU=sp.lambdify((t,x),U,"mpmath")
    for _ in range(6):
        pt={t:sp.Rational(random.randint(-50,50),100),x:sp.Rational(random.randint(-200,200),100)}
        m=max(m,abs(fR(float(pt[t]),float(pt[x]))/fU(float(pt[t]),float(pt[x]))))
    print(f'lente [{name}]: max |residuo/u| su 6 punti = {float(m):.2e}'); ok&=m<1e-10
# controllo di non banalita': la stessa u NON risolve l'equazione libera
U=pref*tests['gaussiana libera']; R0=sp.I*sp.diff(U,t)+sp.Rational(1,2)*sp.diff(U,x,2)
f0=sp.lambdify((t,x),R0/U,'mpmath'); print('controllo: |(i u_t + u_xx/2)/u| in (0.3,1.1) =',float(abs(f0(0.3,1.1))))
print('ESITO', 'OK' if ok else 'FAIL')
