# S-P3 ripresa audit 5: conferma (non nuova prova) dei calcoli di AUDIT_P3 su T6-vi e T6-1.
# Sui modi: a_i = valori dei simboli, u(t0+s) = e^{s a}, u0 = 1. Duhamel G_g f = w  <=>  w' = g w + f, w(0) = 0.
import sympy as sp
s, th, rho = sp.symbols('s theta rho')
N = 3
A = sp.symbols('a1:%d' % (N+1), nonzero=True)
a = sum(A)
u = lambda t: sp.exp(t*a)
z = lambda e: sp.simplify(sp.expand(e)) == 0
ok = []
w = [Ai*(sp.exp(s*a)-sp.exp(th*s*a))/a for Ai in A]          # u_theta^(i)
ok.append(('theta: w_i = G_theta (1-theta) a_i u (ODE)', all(z(sp.diff(wi,s)-th*a*wi-(1-th)*Ai*u(s)) and z(wi.subs(s,0)) for Ai,wi in zip(A,w))))
ok.append(('theta: esattezza S_theta u0 + sum w_i = u', z(sp.exp(th*s*a)+sum(w)-u(s))))
F = [Ai*sp.exp(rho*a)/a for Ai in A]                           # primitiva di a_i u
ok.append(('theta: quadratura int_{theta s}^{s} a_i u', all(z(Fi.subs(rho,s)-Fi.subs(rho,th*s)-wi) for Fi,wi in zip(F,w))))
ok.append(('theta: componenti dipendono da theta', not z(sp.diff(w[0],th))))
ok.append(('theta: equivarianza (w_i/a_i indipendente da i)', all(z(wi/Ai-w[0]/A[0]) for Ai,wi in zip(A,w))))
ok.append(('bilancio violato: d_s w_i = a_i u(s) - theta a_i u(theta s)', all(z(sp.diff(wi,s)-(Ai*u(s)-th*Ai*u(th*s))) for Ai,wi in zip(A,w))))
ok.append(('theta=0: bilancio termine per termine', all(z(sp.diff(wi.subs(th,0),s)-Ai*u(s)) and z(wi.subs({th:0,s:0})) for Ai,wi in zip(A,w))))
uj = [Ai*(sp.exp(s*a)-1)/a for Ai in A]
for i in range(N):
    Ei = uj[i]-(sp.exp(s*A[i])-1)
    rhs = A[i]*sum(uj[j] for j in range(N) if j != i)
    ok.append(('T6-1: E^(%d) = G_%d a_%d sum_{j!=%d} u^(j) (ODE)' % (i+1,i+1,i+1,i+1), z(sp.diff(Ei,s)-A[i]*Ei-rhs) and z(Ei.subs(s,0))))
for name, v in ok: print(('OK  ' if v else 'FAIL'), name)
print('TOTALE %d/%d OK' % (sum(v for _, v in ok), len(ok)))
