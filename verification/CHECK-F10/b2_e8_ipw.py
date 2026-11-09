# S-CHECK-F10-B2 . controlli per S10B-E8 / (R).
# I_PW := { p omogeneo : p(A kap^j cos(theta + j pi/2))_j = 0 per ogni A, kap, theta reali } (S4ID-P8).
# Parametrizzazione complessa (Zariski-densa, i punti reali formano una sottovarieta' totalmente reale di
# dimensione massima): y_j = B mu^j + C (-mu)^j, cioe' i getti delle soluzioni di v'' = mu^2 v.
# Controlli: (1) la parametrizzazione reale e quella complessa danno lo stesso test sugli esempi;
# (2) I_PW non contiene forme lineari non nulle (quindi in (R) la clausola "parte lineare nulla" e' ridondante);
# (3) esempi noti in I_PW (S4ID-P8) e non in I_PW (parte minima di Pi_1, parte lineare di Novikov);
# (4) la "forma iniziale" usata da P8 e' la componente omogenea di grado ORDINARIO minimo: ampiezza uniforme t^{-1/2}.
import sympy as sp
ok = []
def rep(name, c):
    ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
n = 6
y = sp.symbols('y0:%d' % (n+1))
A, kap, th, B, C, mu, t, k = sp.symbols('A kappa theta B C mu t k')
real_jet = {y[j]: A*kap**j*sp.cos(th + j*sp.pi/2) for j in range(n+1)}
cplx_jet = {y[j]: B*mu**j + C*(-mu)**j for j in range(n+1)}
def in_ipw_c(p): return sp.expand(p.subs(cplx_jet, simultaneous=True)) == 0
def in_ipw_r(p): return sp.simplify(sp.expand_trig(p.subs(real_jet, simultaneous=True))) == 0
ex_in = [y[0]*y[3] - y[1]*y[2], y[0]*y[4] - y[2]**2, y[1]*y[4] - y[2]*y[3]]
ex_out = [y[1]**2 - k**2*y[0]**2, y[4] - 5*y[2] + 4*y[0], y[0]**2 + y[1]**2]
for p in ex_in:
    rep('in I_PW: %s (reale %s, complesso %s)' % (p, in_ipw_r(p), in_ipw_c(p)), in_ipw_r(p) and in_ipw_c(p))
for p in ex_out:
    rep('non in I_PW: %s' % p, (not in_ipw_r(p)) and (not in_ipw_c(p)))
c = sp.symbols('c0:%d' % (n+1))
lin = sum(c[j]*y[j] for j in range(n+1))
eqs = sp.Poly(sp.expand(lin.subs(cplx_jet, simultaneous=True)), B, C, mu).coeffs()
s = sp.solve(eqs, c, dict=True)
rep('nessuna forma lineare non nulla in I_PW (ordine <= %d): soluzione %s' % (n, s), s == [{cj: 0 for cj in c}])
# (4) scaling radiativo: getto = t^{-1/2} (v + o(1)) con lo stesso fattore per ogni j, quindi
# G(t^{-1/2} v) = sum_e t^{-e/2} G_e(v): conta il grado ordinario, non un peso dipendente da j.
G = (y[0]*y[4] - y[2]**2) + y[0]**3 + y[1]*y[2]*y[3]
sc = sp.expand(G.subs({y[j]: t*y[j] for j in range(n+1)}, simultaneous=True))
low = sp.Poly(sc, t).terms()[-1]
rep('componente dominante per t -> 0 (ampiezza) = parte di grado ordinario minimo: %s' % sp.factor(low[1]),
    sp.expand(low[1] - (y[0]*y[4] - y[2]**2)) == 0 and low[0] == (2,))
rep('(R) non vuota come classe: G = (y0 y4 - y2^2) + termini di grado 3 ha parte lineare nulla e in(G) in I_PW',
    in_ipw_c(y[0]*y[4] - y[2]**2))
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
