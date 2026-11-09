# S-CHECK-F10-B2 . controllo su P3-a: un minimo locale di u_0' con valore critico 0 non e' spostato dalle
# perturbazioni psi_i del Passo 1 (che agiscono solo sui candidati m_i con u_0'(m_i) < 0), e una perturbazione
# C^r arbitrariamente piccola lo rende negativo, creando un tempo candidato t = 1/delta arbitrariamente grande.
# Esempio: u_0' = -cos x - cos 2x (media nulla, u_0 = -sin x - sin(2x)/2 periodica).
#   punti critici di u_0': x = 0 (min, valore -2: candidato t = 1/2), x = pi (min, valore 0), x = +-arccos(-1/4) (max).
import numpy as np
ok = []
def rep(name, c):
    ok.append(bool(c)); print(('OK  ' if c else 'FAIL') + ' ' + name)
up = lambda x: -np.cos(x) - np.cos(2*x)
upp = lambda x: np.sin(x) + 2*np.sin(2*x)
uppp = lambda x: np.cos(x) + 4*np.cos(2*x)
rep('x = pi: punto critico di u_0\' con valore %.3g e u_0\'\'\' = %.3g > 0 (minimo locale non degenere)' % (up(np.pi), uppp(np.pi)),
    abs(upp(np.pi)) < 1e-14 and abs(up(np.pi)) < 1e-14 and uppp(np.pi) > 0)
rep('x = 0: candidato, valore %.3g, tempo t = %.3g' % (up(0), -1/up(0)), up(0) == -2 and uppp(0) > 0)
# bump del Passo 1 attorno a m = 0: psi(x) = x chi(x), chi = 1 su |x| <= rho, supporto in |x| < 2 rho
rho = 0.3
def chi(x):
    s = np.clip((np.abs(x) - rho)/rho, 0, 1)
    h = lambda z: np.where(z > 0, np.exp(-1/np.maximum(z, 1e-300)), 0.)
    return h(1 - s)/(h(1 - s) + h(s))
xs = np.linspace(-np.pi, np.pi, 200001)
eps = 1e-3
pert = up(xs) + eps*np.gradient(xs*chi(xs), xs)       # u_0' + eps psi'
i_pi = np.argmin(np.abs(xs - np.pi)); i_0 = np.argmin(np.abs(xs))
rep('dopo il bump in m = 0: valore in 0 spostato di %.3g, valore in pi invariato (%.3g)' % (pert[i_0] - up(0), pert[i_pi]),
    abs(pert[i_0] - up(0) - eps) < 1e-6 and abs(pert[i_pi]) < 1e-12)
for delta in (1e-2, 1e-4, 1e-6):
    # perturbazione C^r piccola: -delta (1 + cos x)/2 ... media non nulla; si usa -delta*(cos x)*... con media nulla:
    # w(x) = -delta * (1 - cos(x - pi))/2 + delta/2 = delta*cos(x - pi)/2 ... valore in pi: -delta/2
    w = lambda x: delta*np.cos(x - np.pi)/2*(-1)          # media nulla, w(pi) = -delta/2, w'(pi) = 0
    val = up(np.pi) + w(np.pi)
    rep('delta = %.0e: perturbazione di norma C^r ~ %.0e porta il valore in pi a %.1e, nuovo candidato t = %.3g'
        % (delta, delta/2, val, -1/val), val < 0 and -1/val > 1/delta)
print('TOTALE: %d/%d OK' % (sum(ok), len(ok)))
