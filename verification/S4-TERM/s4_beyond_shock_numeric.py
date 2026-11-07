# S4-TERM s4: NUMERICAL ILLUSTRATION ONLY (not a proof) of S4T-T2 / S4T-T3 on T with u0 = sin x (eps=1, t*=1).
# Hopf-Cole: u(t,x) = int ((x-y)/t) w(y) dy / int w(y) dy, w = exp(-Phi_x(y)/(2 nu)), Phi_x(y) = U0(y) + (x-y)^2/(2t), U0 = 1-cos y.
# Lax-Oleinik: v(t,x) = (x - a(t,x))/t, a = argmin Phi_x. Heat: e^{s nu d^2} f via Gaussian convolution.
import numpy as np
from math import erf, sqrt, pi
U0 = lambda y: 1 - np.cos(y)
u0 = lambda y: np.sin(y)
def viscous(t, xs, nu, Ly=12.0, ny=40001):
    out = np.empty_like(xs)
    for i, x in enumerate(xs):
        y = np.linspace(x - Ly, x + Ly, ny)
        Phi = U0(y) + (x - y)**2/(2*t)
        w = np.exp(-(Phi - Phi.min())/(2*nu))
        out[i] = np.trapezoid((x - y)/t*w, y)/np.trapezoid(w, y)
    return out
def inviscid(t, xs, Ly=12.0, ny=40001):
    out = np.empty_like(xs); amin = np.empty_like(xs)
    for i, x in enumerate(xs):
        y = np.linspace(x - Ly, x + Ly, ny)
        Phi = U0(y) + (x - y)**2/(2*t)
        a = y[np.argmin(Phi)]
        for _ in range(30):   # Newton refinement of the stationarity condition a + t sin a = x
            a = a - (a + t*np.sin(a) - x)/(1 + t*np.cos(a))
        amin[i] = a
        out[i] = (x - a)/t
    return out, amin
def heat(f_vals, xs, s_nu):   # periodic grid xs on [0,2pi)
    n = len(xs); k = np.fft.fftfreq(n, d=(xs[1]-xs[0]))*2*np.pi
    return np.real(np.fft.ifft(np.fft.fft(f_vals)*np.exp(-s_nu*k**2)))
n = 8192
xs = np.linspace(0, 2*np.pi, n, endpoint=False); dx = xs[1] - xs[0]
print("== before the shock, t = 0.5 (t* = 1): ||E^add||_inf / nu vs closed form nu-coefficient ==")
t = 0.5
for nu in (0.02, 0.01, 0.005):
    u = viscous(t, xs, nu); v, a = inviscid(t, xs); h = heat(u0(xs), xs, nu*t)
    Eadd = u - h - v + u0(xs)
    J = 1 + t*np.cos(a); E1 = t*(-np.sin(a)/J**2 - (-np.sin(xs)))
    print("nu=%.4f  sup|E^add|/nu = %.5f   sup|E1 closed form| = %.5f   sup|E^add - nu E1|/nu^2 = %.3f" %
          (nu, np.abs(Eadd).max()/nu, np.abs(E1).max(), np.abs(Eadd - nu*E1).max()/nu**2))
print("== beyond the shock, t = 2: shock at x0 = pi ==")
t = 2.0
v, a = inviscid(t, xs)
i0 = np.argmin(np.abs(xs - np.pi))
D = v[i0-3] - v[i0+3]
print("jump of S_B(t)u0 at pi ~ D = %.5f ; lower bound l(t)/t from {1+t cos a<0}: l = %.5f" % (D, 2*np.arccos(-1/t) - 0 if False else (2*(np.pi - np.arccos(-1/t)))/t))
for nu in (0.01, 0.0025, 0.000625):
    u = viscous(t, xs, nu); h = heat(u0(xs), xs, nu*t)
    Eadd = u - h - v + u0(xs)
    EAB = u - heat(v, xs, nu*t)
    vh, _ = inviscid(t, xs) if False else (None, None)
    print("nu=%.6f  sup|E^add| = %.4f (>= D/2 = %.4f)  sup|E^mult_AB| = %.4f  ||E^mult_AB||_L1/sqrt(nu) = %.4f (2D sqrt(t/pi) = %.4f)  ||E^add||_L1/nu = %.3f" %
          (nu, np.abs(Eadd).max(), D/2, np.abs(EAB).max(), np.abs(EAB).sum()*dx/np.sqrt(nu), 2*D*np.sqrt(t/np.pi), np.abs(Eadd).sum()*dx/nu))
