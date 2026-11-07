# OP-F5A — OPA-Q1: controllo numerico (NON prova) di OPF5A-T1.
# Burgers viscoso su T, u0 = sin x (t* = 1, a* = pi, u0'''(pi) = 1).
# e(t) := ||S(t)u0 - S_B(t)u0||_{L1}. Predizioni:
#   t = t*:              e = nu|log nu| + O(nu)            -> (e - nu|log nu|)/nu limitato
#   t < t*:              e <= nu*TV(log J)  (Kato, OPF5A-P1)  e = nu*min(TV log J, |log nu|) + O(nu)
#   t* < t <= t*+tau0:   e <= nu|log nu| + C nu
# u - v = (a - <y>)/t, <.> media di Hopf; integrazione nella variabile a (x = a + t sin a, dx = J da).
import numpy as np
from scipy.optimize import brentq

def mean_shift(x, a, t, nu, extra_right=0.0):
    # <y - a> per la misura exp(-(Phi_x(y) - Phi_x(a))/2nu), Phi_x(y) = 1 - cos y + (x-y)^2/(2t)
    J = 1 + t*np.cos(a)
    s = min(np.sqrt(2*nu*t/max(J, 1e-300)), (48*nu)**0.25)
    smin = np.sqrt(2*nu*t/(1+t))
    h = min(s, smin)/14
    lo, hi = a - 2.0, a + 2.0 + extra_right
    y = np.arange(lo, hi, h)
    z = y - a
    Phi = (1 - np.cos(y)) + (x - y)**2/(2*t)
    E = -(Phi - Phi.min())/(2*nu)
    w = np.exp(E)
    return np.sum(w*z)/np.sum(w)

def e_before(t, nu, n=2500):
    # t <= 1: X monotone; by odd symmetry e = 2 * int_0^pi |u - v| J da
    zs = np.concatenate([np.geomspace(1e-9, 1e-3, 600), np.linspace(1e-3, np.pi, n)[1:]])
    a = np.pi - zs
    f = np.empty_like(a)
    for i, ai in enumerate(a):
        x = ai + t*np.sin(ai)
        f[i] = abs(mean_shift(x, ai, t, nu))/t*(1 + t*np.cos(ai))
    return 2*np.trapezoid(f, zs)

def e_after(t, nu, n=2500):
    # t > 1: left branch a in [0, a-], a- = pi - b, b = t sin b; x in [0, pi]
    b = brentq(lambda b: b - t*np.sin(b), 1e-12, np.pi - 1e-12)
    am = np.pi - b
    zs = np.concatenate([np.geomspace(1e-10, 1e-3, 800), np.linspace(1e-3, am, n)[1:]])
    a = am - zs
    f = np.empty_like(a)
    for i, ai in enumerate(a):
        x = ai + t*np.sin(ai)
        f[i] = abs(mean_shift(x, ai, t, nu, extra_right=2*b + 0.5))/t*(1 + t*np.cos(ai))
    return 2*np.trapezoid(f, zs)

def TVlogJ(t):
    # TV of log J over a in [-pi, pi], t < 1: 2*(log(1+t) - log(1-t))
    return 2*np.log((1 + t)/(1 - t))

if __name__ == "__main__":
    print("(A) t = t* = 1:  (e - nu|log nu|)/nu deve restare limitato")
    for nu in (1e-3, 3e-4, 1e-4, 3e-5, 1e-5):
        e = e_before(1.0, nu)
        print(f"  nu={nu:.0e}: e/nu={e/nu:.4f}  |log nu|={abs(np.log(nu)):.4f}  (e-nu|log nu|)/nu={(e-nu*abs(np.log(nu)))/nu:.4f}")
    print("(B) t < t*: Kato e <= nu TV(log J); e/nu vs min(TV log J, |log nu|)")
    for t in (0.9, 0.99, 0.999):
        for nu in (1e-4, 1e-5):
            e = e_before(t, nu)
            print(f"  t={t}, nu={nu:.0e}: e/nu={e/nu:.4f}  TVlogJ={TVlogJ(t):.4f}  Kato ok={e <= nu*TVlogJ(t)}  min(..)={min(TVlogJ(t), abs(np.log(nu))):.4f}")
    print("(C) t > t*: e/nu - |log nu| (deve restare <= C)")
    for nu in (1e-4, 1e-5):
        for tau in (0.3*np.sqrt(nu), np.sqrt(nu), 4*np.sqrt(nu), 0.01, 0.05):
            e = e_after(1 + tau, nu)
            print(f"  nu={nu:.0e}, tau={tau:.2e}: e/nu={e/nu:.4f}  |log nu|={abs(np.log(nu)):.4f}  diff={e/nu-abs(np.log(nu)):.4f}")
