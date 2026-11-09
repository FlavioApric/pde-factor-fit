# F6-ENC: operatore di trasformazione simmetrico (tipo Marchenko/Levitan) per q costante = c.
# T f(x) = f(x) + int_{-x}^{x} K(x,s) f(s) ds,  K_xx - K_ss = c K,  K(x,x) = c x/2,  K(x,-x) = 0.
# Candidato (corretto dopo il 1o run: fattore 1/4): K(x,s) = c (x+s)/4 * 2 I_1(w)/w,  w = sqrt(c (x^2 - s^2)).
# Verifiche numeriche (mpmath): equazione di Goursat, condizioni, e T e^{iks} = soluzione con q=c
# avente gli stessi dati di Cauchy in 0 (cos(mu x) + i k sin(mu x)/mu, mu = sqrt(k^2 - c)).
import mpmath as mp
mp.mp.dps = 30
ok = []
def K(x, s, c):
    w2 = c*(x*x - s*s)
    if w2 == 0:
        g = mp.mpf(1)
    else:
        w = mp.sqrt(w2)
        g = 2*mp.besseli(1, w)/w
    return c*(x + s)/4*g
worst = 0
for c in [mp.mpf('0.7'), mp.mpf('-1.3'), mp.mpf('2.1')]:
    for (x, s) in [(mp.mpf('0.9'), mp.mpf('0.2')), (mp.mpf('1.4'), mp.mpf('-0.5')), (mp.mpf('0.5'), mp.mpf('0.1'))]:
        Kxx = mp.diff(lambda X: K(X, s, c), x, 2)
        Kss = mp.diff(lambda S: K(x, S, c), s, 2)
        worst = max(worst, abs(Kxx - Kss - c*K(x, s, c)))
ok.append(('Goursat K_xx-K_ss=cK (max res %s)' % mp.nstr(worst, 5), worst < mp.mpf('1e-15')))
c = mp.mpf('0.7'); x = mp.mpf('1.1')
ok.append(('K(x,x)=cx/2', abs(K(x, x, c) - c*x/2) < 1e-25))
ok.append(('K(x,-x)=0', abs(K(x, -x, c)) < 1e-25))
worst = 0
for c in [mp.mpf('0.7'), mp.mpf('-1.3')]:
    for k in [mp.mpf('0.4'), mp.mpf('2.3')]:
        mu = mp.sqrt(k*k - c)
        for x in [mp.mpf('0.6'), mp.mpf('1.5')]:
            Tf = mp.exp(1j*k*x) + mp.quad(lambda s: K(x, s, c)*mp.exp(1j*k*s), [-x, x])
            target = mp.cos(mu*x) + 1j*k*mp.sin(mu*x)/mu
            worst = max(worst, abs(Tf - target))
ok.append(('T e^{iks} = sol. con q=c, stessi dati in 0 (max err %s)' % mp.nstr(worst, 5), worst < mp.mpf('1e-15')))
# intertwining su una funzione NON soluzione (nessuna condizione al bordo): f(s) = s^3 + exp(s/2)
c = mp.mpf('0.7')
f = lambda s: s**3 + mp.exp(s/2)
f2 = lambda s: 6*s + mp.exp(s/2)/4
T = lambda g, X: g(X) + mp.quad(lambda s: K(X, s, c)*g(s), [-X, X])
worst = 0
for x in [mp.mpf('0.5'), mp.mpf('1.2')]:
    lhs = -mp.diff(lambda X: T(f, X), x, 2) + c*T(f, x)   # L_q T f
    rhs = T(lambda s: -f2(s), x)                           # T L_0 f
    worst = max(worst, abs(lhs - rhs))
ok.append(('L_q T f = T L_0 f per f generica (max err %s)' % mp.nstr(worst, 5), worst < mp.mpf('1e-10')))
for name, val in ok: print(('OK  ' if val else 'FAIL'), name)
print('TOTALE', sum(v for _, v in ok), '/', len(ok))
