# F6-ENC: spostamento efficace per H_eps = -d^2/dx^2 + eps^{-1} V(x/eps), V 2pi-periodica a media nulla.
# In y = x/eps: H_eps = eps^{-2}(-d_y^2 + eps V(y)). Candidato: fondo dello spettro -> -<(d_y^{-1}V)^2>.
# Verifica numerica (base di Fourier, k = 0 = bordo inferiore della banda): solo controllo.
import numpy as np
def bottom(eps, Vhat, N=40):
    n = np.arange(-N, N+1)
    H = np.diag(n.astype(float)**2).astype(complex)
    for m, v in Vhat.items():
        for i, ni in enumerate(n):
            j = ni - m
            if -N <= j <= N:
                H[i, j + N] += eps*v
    return np.linalg.eigvalsh(H).min()/eps**2
cases = {
  'V=cos y':              ({1: .5, -1: .5}, 0.5),
  'V=cos y + 0.5 sin 2y': ({1: .5, -1: .5, 2: -.25j, -2: .25j}, 0.5 + 0.03125),
}
allok = True
for name, (Vhat, mean_sq) in cases.items():
    vals = [bottom(e, Vhat) for e in [0.2, 0.1, 0.05, 0.02]]
    print(name, 'eps^-2 E0 ->', np.round(vals, 6), ' atteso', -mean_sq)
    allok &= abs(vals[-1] + mean_sq) < 1e-2
print(('OK  ' if allok else 'FAIL'), 'shift efficace = -<(d^{-1}V)^2>')
# scala eps^0 V(x/eps) (ampiezza O(1)): il fondo tende a <V> = 0 (potenziale efficace nullo)
v = [np.linalg.eigvalsh(np.diag(np.arange(-40,41.)**2) + e*e*0.5*(np.eye(81,k=1)+np.eye(81,k=-1))).min()/e**2 for e in [0.1,0.05,0.02]]
print('ampiezza O(1): E0 ->', np.round(v, 6), '(atteso 0)')
print(('OK  ' if abs(v[-1]) < 1e-3 else 'FAIL'), 'ampiezza O(1): operatore efficace libero')
