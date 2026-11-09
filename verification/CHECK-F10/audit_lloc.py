# Audit S-CHECK-F10-B: verifica numerica (V-ex) di L-loc vicino a una SECONDA nascita di shock (Burgers viscoso,
# formula di Cole-Hopf con peso exp(-Phi_x(a)/2nu), Phi_x(a) = U0(a) + (x-a)^2/(2t)).
import numpy as np
from scipy.optimize import brentq, minimize_scalar
c2, ph = 0.45, 1.0
u0  = lambda a: np.sin(a) + c2*np.sin(2*a + ph)
U0  = lambda a: -np.cos(a) - c2/2*np.cos(2*a + ph)          # primitiva, periodica
du0 = lambda a: np.cos(a) + 2*c2*np.cos(2*a + ph)
d2u0 = lambda a: -np.sin(a) - 4*c2*np.sin(2*a + ph)
# minimi locali di u0'
g = np.linspace(0, 2*np.pi, 20001)
z = d2u0(g); mins = []
for i in range(len(g)-1):
    if z[i] < 0 <= z[i+1]:
        r = brentq(d2u0, g[i], g[i+1]); mins.append((du0(r), r))
mins.sort()
print('minimi locali di u0\' (valore, punto):', [(round(v, 6), round(r, 6)) for v, r in mins])
def minimizers(x, t, A):
    Phi = U0(A) + (x - A)**2/(2*t)
    return Phi
A = np.linspace(-4*np.pi, 6*np.pi, 400001)
for v, ab in mins:
    if v >= 0: continue
    tb = -1/v; xb = ab + tb*u0(ab)
    Phi = minimizers(xb, tb, A)
    i = np.argmin(Phi); m = Phi[i]
    far = np.abs(((A - ab + np.pi) % (2*np.pi)) - np.pi) > 0.25
    gap = Phi[far].min() - Phi[i] if far.any() else np.inf
    # gap reale: escludere solo l'intorno di ab nel rivestimento (A vicino ad ab, non ai traslati)
    near = np.abs(A - ab) < 0.25
    gap2 = Phi[~near].min() - Phi[near].min()
    print('nascita candidata a_b=%.6f t_b=%.6f x_b=%.6f: argmin=%.6f, margine eta0 (fuori |a-a_b|<0.25) = %.4g' % (ab, tb, xb, A[i], gap2))
# seconda nascita: quella con t_b maggiore e margine positivo
cands = [(-1/v, ab) for v, ab in mins if v < 0]
cands.sort()
tb, ab = cands[1]
xb = ab + tb*u0(ab)
print('seconda nascita: t_b=%.6f a_b=%.6f x_b=%.6f' % (tb, ab, xb))
def inner_L1(nu, t, rb=0.25, za=1.0):
    h = nu/6
    X = np.arange(xb - rb, xb + rb, h)
    da = min(np.sqrt(nu*t)/12, nu**0.25/40)
    Aw = np.arange(ab - za, ab + za, da)
    tot = 0.0
    for s in range(0, len(X), 400):
        Xs = X[s:s+400, None]
        Phi = U0(Aw)[None, :] + (Xs - Aw[None, :])**2/(2*t)
        j = np.argmin(Phi, axis=1)
        mn = Phi[np.arange(len(Xs)), j][:, None]
        w = np.exp(-(Phi - mn)/(2*nu))
        u = ((Xs - Aw[None, :])/t*w).sum(1)/w.sum(1)
        # minimizzante "entropico" raffinato con interpolazione parabolica
        jj = np.clip(j, 1, len(Aw)-2)
        f0, f1, f2 = Phi[np.arange(len(Xs)), jj-1], Phi[np.arange(len(Xs)), jj], Phi[np.arange(len(Xs)), jj+1]
        den = f0 - 2*f1 + f2
        off = np.where(np.abs(den) > 1e-300, 0.5*(f0 - f2)/den, 0.0)
        astar = Aw[jj] + np.clip(off, -1, 1)*da
        v = (Xs[:, 0] - astar)/t
        tot += np.abs(u - v).sum()*h
    return tot
for t in [tb, tb - 0.02, tb + 0.02]:
    for nu in [1e-3, 3e-4, 1e-4]:
        I = inner_L1(nu, t)
        d = abs(t - tb)
        pred = 2*nu*np.log(1/max(d, np.sqrt(nu)))
        print('t-t_b=%+.3f nu=%.0e: L1 interno = %.6e, 2nu log(1/max(d,sqrt nu)) = %.6e, (L1 - pred)/nu = %.4f' % (t - tb, nu, I, pred, (I - pred)/nu))
