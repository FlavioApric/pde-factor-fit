# F6-ENC: controllo indipendente dell'intertwining (il run precedente ha dato errore esattamente 0, sospetto).
# Stampa lhs e rhs separati; derivata seconda per differenze centrali esplicite.
import mpmath as mp
mp.mp.dps = 40
def K(x, s, c):
    w2 = c*(x*x - s*s)
    g = mp.mpf(1) if w2 == 0 else 2*mp.besseli(1, mp.sqrt(w2))/mp.sqrt(w2)
    return c*(x + s)/4*g
c = mp.mpf('0.7')
f = lambda s: mp.cos(3*s) + s**4 - 2*s + mp.exp(s)       # nessuna condizione al bordo
f2 = lambda s: -9*mp.cos(3*s) + 12*s**2 + mp.exp(s)
T = lambda g, X: g(X) + mp.quad(lambda s: K(X, s, c)*g(s), [-X, 0, X])
h = mp.mpf('1e-8'); bad = 0
for x in [mp.mpf('0.4'), mp.mpf('0.9'), mp.mpf('1.3')]:
    Tpp = (T(f, x + h) - 2*T(f, x) + T(f, x - h))/h**2
    lhs = -Tpp + c*T(f, x)
    rhs = T(lambda s: -f2(s), x)
    print('x =', x, ' L_q T f =', mp.nstr(lhs, 15), '  T L_0 f =', mp.nstr(rhs, 15), '  diff =', mp.nstr(lhs - rhs, 5))
    bad = max(bad, abs(lhs - rhs))
# controllo negativo: con il nucleo sbagliato (fattore 1/2) l'intertwining deve fallire
K2 = lambda x, s: 2*K(x, s, c)
T2 = lambda g, X: g(X) + mp.quad(lambda s: K2(X, s)*g(s), [-X, 0, X])
x = mp.mpf('0.9')
d2 = -(T2(f, x + h) - 2*T2(f, x) + T2(f, x - h))/h**2 + c*T2(f, x) - T2(lambda s: -f2(s), x)
print('controllo negativo (nucleo x2): diff =', mp.nstr(d2, 5))
print(('OK  ' if bad < mp.mpf('1e-6') else 'FAIL'), 'intertwining L_q T = T L_0 (max diff %s)' % mp.nstr(bad, 5))
print(('OK  ' if abs(d2) > mp.mpf('1e-3') else 'FAIL'), 'controllo negativo fallisce come atteso')
