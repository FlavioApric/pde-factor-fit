# F6-ENC: lens transform (Niederer). libera i v_s = -1/2 v_yy  ->  armonica i u_t = -1/2 u_xx + 1/2 x^2 u
# u(t,x) = cos(t)^(-1/2) exp(-i x^2 tan t / 2) v(tan t, x / cos t); verifica in forma logaritmica.
import sympy as sp
t, x, p, y0 = sp.symbols('t x p y0', real=True)
ok = []
def resid_log(S):
    r = sp.I*sp.diff(S, t) + (sp.diff(S, x, 2) + sp.diff(S, x)**2)/2 - x**2/2
    r = sp.expand(sp.expand_trig(r)).rewrite(sp.cos)
    return sp.simplify(sp.cancel(sp.together(r)))
def lensS(Sv):   # Sv(s,y): log di v
    return -sp.log(sp.cos(t))/2 - sp.I*x**2*sp.tan(t)/2 + Sv(sp.tan(t), x/sp.cos(t))
Splane = lambda s, yy: sp.I*p*yy - sp.I*p**2*s/2
ok.append(('onda piana libera -> armonica', resid_log(lensS(Splane)) == 0))
Sg = lambda s, yy: -sp.log(1 + sp.I*s)/2 - yy**2/(2*(1 + sp.I*s))
ok.append(('gaussiana libera -> armonica', resid_log(lensS(Sg)) == 0))
# nucleo libero -> nucleo di Mehler
SK0 = lambda s, yy: -sp.log(2*sp.pi*sp.I*s)/2 + sp.I*(yy - y0)**2/(2*s)
ok.append(('lens(nucleo libero) risolve armonica', resid_log(lensS(SK0)) == 0))
SM = -sp.log(2*sp.pi*sp.I*sp.sin(t))/2 + sp.I*((x**2 + y0**2)*sp.cos(t) - 2*x*y0)/(2*sp.sin(t))
ok.append(('formula di Mehler risolve armonica', resid_log(SM) == 0))
# differenza di fase lens(K0) - Mehler non dipende da x (stesso nucleo a meno di fattore in (t,y0))
d = sp.simplify(sp.diff(lensS(SK0) - SM, x).rewrite(sp.cos))
print('d/dx [log lens(K0) - log Mehler] =', d)
ok.append(('lens(K0) = Mehler * c(t,y0)', d == 0))
# immagine della gaussiana: stato fondamentale exp(-x^2/2) a meno di fase
dg = sp.simplify(sp.diff(lensS(Sg), x).rewrite(sp.cos) + x)
print('d/dx log lens(gauss) + x =', dg)
ok.append(('lens(gauss) = stato fondamentale * fase(t)', dg == 0))
for name, val in ok: print(('OK  ' if val else 'FAIL'), name)
print('TOTALE', sum(v for _, v in ok), '/', len(ok))
