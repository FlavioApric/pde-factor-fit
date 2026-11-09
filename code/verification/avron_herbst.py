# F6-ENC: Avron-Herbst. i u_t = -1/2 u_xx + F x u  <->  i v_t = -1/2 v_yy  (solo verifica)
# u = exp(S): residuo/u = i S_t + (S_xx + S_x^2)/2 - F x   (forma logaritmica: evita simplify costosi)
import sympy as sp
t, x, F, p = sp.symbols('t x F p', real=True)
ok = []
def resid_log(S, Vpot):
    return sp.cancel(sp.expand(sp.I*sp.diff(S, t) + (sp.diff(S, x, 2) + sp.diff(S, x)**2)/2 - Vpot))
phase = -sp.I*F*t*x - sp.I*F**2*t**3/6
y = x + F*t**2/2
Splane = sp.I*p*y - sp.I*p**2*t/2
ok.append(('onda piana libera -> F x', resid_log(phase + Splane, F*x) == 0))
Sg = -sp.log(1 + sp.I*t)/2 - y**2/(2*(1 + sp.I*t))
ok.append(('gaussiana libera -> F x', resid_log(phase + Sg, F*x) == 0))
ok.append(('controllo: senza fase fallisce', resid_log(Splane, F*x) != 0))
# le funzioni libere usate risolvono davvero la libera
yy = sp.symbols('yy', real=True)
ok.append(('onda piana libera ok', resid_log((sp.I*p*x - sp.I*p**2*t/2), 0) == 0))
ok.append(('gaussiana libera ok', resid_log(-sp.log(1 + sp.I*t)/2 - x**2/(2*(1 + sp.I*t)), 0) == 0))
for name, val in ok: print(('OK  ' if val else 'FAIL'), name)
print('TOTALE', sum(v for _, v in ok), '/', len(ok))
