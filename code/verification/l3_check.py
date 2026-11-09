# S5-FIX2: ricontrollo della cifra 1.8e-5 di F4LIN-T2(iii) (rilievo di S-CHECK-9 §5.2 L.7)
# configurazione di work/S4-INTEG/sympy/integ_checks.py: c=(2,0,-2), beta=(0,3,0), t=1, N=3, K=2
import mpmath as mp
mp.mp.dps = 40
c = [mp.mpf(2), mp.mpf(0), mp.mpf(-2)]; b = [mp.mpf(0), mp.mpf(3), mp.mpf(0)]; t = 1
S = lambda x: sorted(c[i]*x - c[i]**2*t/2 - b[i] for i in range(3))
# delta = inf_x (S_(3) - S_(1)): minimo su una griglia fine + punti angolosi
pts = [mp.mpf(k)/1000 for k in range(-5000, 5001)]
delta = min(S(x)[2] - S(x)[0] for x in pts)
print("delta =", mp.nstr(delta, 10), " (argmin vicino a x=0)")
def Dp(x, nv):
    s = [c[i]*x - c[i]**2*t/2 - b[i] for i in range(3)]; m = min(s); im = s.index(m)
    w = [mp.e**(-(si - m)/(2*nv)) for si in s]
    return sum(w[i]*c[i] for i in range(3))/sum(w) - c[im]
for nv in [mp.mpf('0.05'), mp.mpf('0.02'), mp.mpf('0.1')]:
    val = mp.quad(lambda x: abs(Dp(x, nv)), [-30, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 30])
    err = abs(val - 8*nv*mp.log(2))
    print(f"nu={nv}: L1={mp.nstr(val,15)} err={mp.nstr(err,6)} e^(-delta/2nu)={mp.nstr(mp.e**(-delta/(2*nv)),6)} "
          f"ratio={mp.nstr(err/mp.e**(-delta/(2*nv)),4)} e^(-delta/4nu)={mp.nstr(mp.e**(-delta/(4*nv)),6)} e^(-2/2nu)={mp.nstr(mp.e**(-2/(2*nv)),6)}")
