# S8-VAR — VAR-P9 (E^mult non autonomo al 2o ordine), commutare a tempi uguali non basta (esatto),
# commutare a tempi diversi basta; VAR-P11 maggiorante di Dyson; VAR-P12 Floquet (esempio V = v(t)).
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")
A1 = lambda s: np.array([[0.3*s, 1.0], [-1.0 + 0.5*s**2, 0.2]], dtype=complex)
A2 = lambda s: np.array([[1j*np.cos(s), 0.4], [0.1*s, -0.7]], dtype=complex)
def prop(Af, tt):
    r = solve_ivp(lambda s, y: (Af(s) @ y.reshape(2, 2)).ravel(), [0, tt], np.eye(2, dtype=complex).ravel(), rtol=1e-12, atol=1e-14)
    return r.y[:, -1].reshape(2, 2)
def twotime(tt, n=400):
    gs, ws = np.polynomial.legendre.leggauss(60)
    tot = np.zeros((2, 2), complex)
    for g1, w1 in zip(gs, ws):
        s1 = (g1 + 1)*tt/2
        for g2, w2 in zip(gs, ws):
            s2 = (g2 + 1)*s1/2
            C = A2(s1) @ A1(s2) - A1(s2) @ A2(s1)
            tot += w1*w2*(tt/2)*(s1/2)*C
    return tot
errs = []
for tt in [0.1, 0.05, 0.025]:
    E = prop(lambda s: A1(s) + A2(s), tt) - prop(A1, tt) @ prop(A2, tt)
    errs.append(np.max(np.abs(E - twotime(tt))))
rates = [np.log2(errs[i]/errs[i+1]) for i in range(2)]
report("VAR-P9 E^mult - int int_{s1>s2}[A2(s1),A1(s2)] = O(t^3)", all(r > 2.7 for r in rates), f"ordini osservati {['%.2f' % r for r in rates]}")
# commutano a tempi uguali ma E^mult != 0: A1 = f(s)X, A2 = g(s)Y, f g = 0
X = np.array([[0, 1], [0, 0]], complex); Yy = np.array([[0, 0], [1, 0]], complex)
f = lambda s: 1.0 if s < 0.5 else 0.0; g = lambda s: 0.0 if s < 0.5 else 1.0
U = expm(0.5*Yy) @ expm(0.5*X); U1U2 = expm(0.5*X) @ expm(0.5*Yy)
report("commutare a tempi uguali non basta: E^mult = e^{Y/2}e^{X/2} - e^{X/2}e^{Y/2} != 0", np.max(np.abs(U - U1U2)) > 0.1, f"|E^mult| = {np.max(np.abs(U - U1U2)):.3f}")
# commutano a tempi diversi: A1(s) = a(s) X, A2(s) = b(s) X^2+... usiamo diagonali
B1 = lambda s: np.diag([np.sin(s), 2*s]).astype(complex); B2 = lambda s: np.diag([s**2, np.cos(3*s)]).astype(complex)
report("[A1(s),A2(r)] = 0 per ogni s,r => E^mult = 0", np.max(np.abs(prop(lambda s: B1(s)+B2(s), 1.3) - prop(B1, 1.3) @ prop(B2, 1.3))) < 1e-9)
# Floquet V = v(t): U(T) = e^{-i int v} U_0(T): il logaritmo limitato ha simbolo k^2 ridotto mod 2pi/T (discontinuo)
T = 1.0; ks = np.linspace(-6, 6, 13)
K = -(np.angle(np.exp(-1j*T*ks**2)))/T
report("VAR-P12: simbolo del K limitato = k^2 mod 2pi/T, non polinomiale", np.max(np.abs(K - ks**2)) > 1 and np.all(np.abs(K) <= np.pi/T + 1e-12))
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
