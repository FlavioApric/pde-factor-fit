# S-CHECK-F10-A: verifica indipendente di S10A-P1 (Laplaciano sull'anello) e del Passo 2' di S10A-T3
import sympy as sp
import random

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1
    if cond: ok += 1
    print(("OK   " if cond else "FAIL ") + name)

t, x, th = sp.symbols('t x theta', real=True)
z = t + sp.I*x; zb = t - sp.I*x

def flux(h, R=sp.Rational(3, 2)):
    # Phi(h) = int_gamma *dh,  *dh = -h_x dt + h_t dx, gamma = {|z| = R} antiorario
    ht, hx = sp.diff(h, t), sp.diff(h, x)
    tt, xx = R*sp.cos(th), R*sp.sin(th)
    integrand = (-hx*sp.diff(tt, th) + ht*sp.diff(xx, th)).subs({t: tt, x: xx}, simultaneous=True)
    return sp.simplify(sp.integrate(sp.simplify(integrand), (th, 0, 2*sp.pi)))

# (1) log|z|: flusso 2 pi
L = sp.log(t**2 + x**2)/2
chk("flusso di log|z| = 2 pi", sp.simplify(flux(L) - 2*sp.pi) == 0)
# (2) olomorfe e antiolomorfe monodrome: flusso 0
fl = [flux(sp.expand(z**n)) for n in (-3, -2, -1, 1, 2, 3)] + [flux(sp.expand(zb**n)) for n in (-2, -1, 2)]
chk("flusso di z^n, zbar^n (n != 0) = 0", all(sp.simplify(v) == 0 for v in fl))
# (3) *dz = -i dz: componenti (dt, dx) di *dz = (-(dz)_x, (dz)_t)
dz = (1, sp.I)                      # dz = dt + i dx
star = (-dz[1], dz[0])              # *(a dt + b dx) = -b dt + a dx
chk("*dz = -i dz", all(sp.simplify(star[k] + sp.I*dz[k]) == 0 for k in range(2)))
# (4) *d Re F = d Im F per F = log z (ramo locale): *d log|z| = d arg z
argz = sp.atan2(x, t)
st = (-sp.diff(L, x), sp.diff(L, t))
chk("*d log|z| = d arg z", all(sp.simplify(st[k] - sp.diff(argz, v)) == 0 for k, v in enumerate((t, x))))
# (5) Laurent: h = f + gbar + c log|z| ha flusso 2 pi c
c = sp.Symbol('c')
h = sp.expand(z**2 + 3/z) + sp.expand(zb**-2) + c*L
chk("flusso(f + gbar + c log|z|) = 2 pi c", sp.simplify(flux(h) - 2*sp.pi*c) == 0)
# (6) armonicita'
chk("log|z|, z^2 armoniche", all(sp.simplify(sp.diff(w, t, 2) + sp.diff(w, x, 2)) == 0 for w in (L, sp.expand(z**2))))
# (7) delta(Delta) = dim C[tau,xi]/(tau+i xi, tau-i xi) = 1
tau, xi = sp.symbols('tau xi')
G = sp.groebner([tau + sp.I*xi, tau - sp.I*xi], tau, xi, order='lex')
chk("delta(Laplaciano) = 1 (ideale = (tau, xi))", set(G.exprs) == {tau, xi})

# (8) Passo 2' di S10A-T3: dominio sopra-grafico lipschitziano phi(y1) = L|y1| - 0.3 sin(5 y1)
#     costante di Lipschitz <= Lc = L + 1.5; y0 sul grafico o sopra; y0 + eps e2 + q con |q| < r_eps
#     deve soddisfare y2 - phi(y1) > eps/2.
import math
random.seed(1)
Lp = 1.2; Lc = Lp + 1.5
phi = lambda u: Lp*abs(u) - 0.3*math.sin(5*u)
bad = 0
for _ in range(200000):
    eps = random.uniform(1e-3, 0.2)
    r = eps/(2*math.sqrt(1 + Lc**2))
    y1 = random.uniform(-1, 1); y2 = phi(y1) + random.choice([0.0, random.uniform(0, 0.1)])
    ang = random.uniform(0, 2*math.pi); rad = r*math.sqrt(random.random())*0.999999
    p1, p2 = y1 + rad*math.cos(ang), y2 + eps + rad*math.sin(ang)
    if not (p2 - phi(p1) > eps/2): bad += 1
chk(f"Passo 2': B(y0 + eps e, r_eps) nel sopra-grafico, margine > eps/2 (violazioni: {bad})", bad == 0)

print(f"{ok}/{tot} OK")
