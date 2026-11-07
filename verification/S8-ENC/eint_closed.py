# S8-ENC — verifica (non metodo) delle forme chiuse di E_int A9 per Schrodinger con V.
# H_0 = -d^2/dx^2 su R, U_0(t) = exp(-i t H_0), nucleo K0 = (4 pi i t)^(-1/2) exp(i (x-y)^2/(4t)).
import sympy as sp
import mpmath as mp

x, y, z = sp.symbols('x y z', real=True)
t, F = sp.symbols('t F', positive=True)
res = []
def report(name, ok, extra=''):
    res.append((name, ok)); print(('OK  ' if ok else 'FAIL') + ' ' + name + ' ' + str(extra))

K0 = (4*sp.pi*sp.I*t)**sp.Rational(-1, 2)*sp.exp(sp.I*(x-y)**2/(4*t))
# 1. K0 risolve i K_t = -K_xx
r = sp.simplify((sp.I*sp.diff(K0, t) + sp.diff(K0, x, 2))/K0)
report('K0 libero', r == 0, r)

# 2. Potenziale lineare V = F x: K_F = K0 * exp(-i F t (x+y)/2 - i F^2 t^3/12)
KF = K0*sp.exp(-sp.I*F*t*(x+y)/2 - sp.I*F**2*t**3/12)
r = sp.simplify((sp.I*sp.diff(KF, t) + sp.diff(KF, x, 2) - F*x*KF)/KF)
report('lineare: K_F risolve i K_t = (-d2 + F x) K', r == 0, r)
# simmetria (necessaria per un propagatore con V reale: K(t,x,y) = K(t,y,x))
report('lineare: simmetria x<->y', sp.simplify(KF - KF.subs({x: y, y: x}, simultaneous=True)) == 0)
# Strang: exp(-itV/2) U0 exp(-itV/2) ha nucleo K0*exp(-iFt(x+y)/2) => U = exp(-iF^2 t^3/12) * Strang
Strang = sp.exp(-sp.I*t*F*x/2)*K0*sp.exp(-sp.I*t*F*y/2)
r = sp.simplify(KF/Strang)
report('lineare: U = exp(-i F^2 t^3/12) * Strang (esatto)', sp.simplify(r - sp.exp(-sp.I*F**2*t**3/12)) == 0, r)
# Lie: U0 exp(-itV) ha nucleo K0*exp(-iFty); E^mult nucleo = K0*(exp(-iFt(x+y)/2 - iF^2t^3/12) - exp(-iFty))
Lie = K0*sp.exp(-sp.I*F*t*y)
r = sp.simplify((KF - Lie)/K0 - (sp.exp(-sp.I*F*t*(x+y)/2 - sp.I*F**2*t**3/12) - sp.exp(-sp.I*F*t*y)))
report('lineare: nucleo di E^mult_{0V}', r == 0)
# Avron-Herbst in forma operatoriale: U(t) f(x) = exp(-itFx - i F^2 t^3/3) (U0(t) f)(x + F t^2)
AH = sp.exp(-sp.I*t*F*x - sp.I*F**2*t**3/3)*K0.subs(x, x + F*t**2)
report('lineare: forma di Avron-Herbst del nucleo', sp.simplify(AH/KF) == 1, sp.simplify(AH/KF))

# 3. Oscillatore H = -d2 + x^2 : Mehler, e chirp-libero-chirp per |t| < pi/2
s2 = sp.sin(2*t); c2 = sp.cos(2*t)
KM = (2*sp.pi*sp.I*s2)**sp.Rational(-1, 2)*sp.exp(sp.I*((x**2+y**2)*c2 - 2*x*y)/(2*s2))
r = sp.simplify((sp.I*sp.diff(KM, t) + sp.diff(KM, x, 2) - x**2*KM)/KM)
report('Mehler risolve i K_t = (-d2 + x^2) K', sp.simplify(sp.trigsimp(r)) == 0, r)
s = s2/2; a = sp.tan(t)/2
K0s = (4*sp.pi*sp.I*s)**sp.Rational(-1, 2)*sp.exp(sp.I*(x-y)**2/(4*s))
CFC = sp.exp(-sp.I*a*x**2)*K0s*sp.exp(-sp.I*a*y**2)
expo = sp.simplify(sp.expand(sp.log(sp.exp(1))*0 + (sp.I*(x-y)**2/(4*s) - sp.I*a*(x**2+y**2)) - sp.I*((x**2+y**2)*c2 - 2*x*y)/(2*s2)))
report('chirp(tan t/2) . U0(sin 2t/2) . chirp: esponente = Mehler', sp.simplify(sp.trigsimp(sp.expand_trig(expo))) == 0, expo)
# prefattore: (4 pi i s)^(-1/2) = (2 pi i sin2t)^(-1/2) identico per costruzione
# controllo numerico del prodotto alla caustica della lente t = pi/4 e a t = 1.3 (< pi/2)
for tv in [sp.pi/4, sp.Rational(13, 10)]:
    vals = [complex(sp.N((CFC/KM).subs({t: tv, x: xv, y: yv}))) for xv, yv in [(0.3, -0.7), (1.1, 0.4)]]
    report('chirp-libero-chirp = Mehler a t=%s' % tv, all(abs(v-1) < 1e-12 for v in vals), vals)

# 4. Poschl-Teller q = -2 sech^2: G_t = U0(t)(L0+1)^{-1}, nucleo con erfc
rr = sp.sqrt(sp.I*t)
G = sp.exp(sp.I*t)/4*(sp.exp(-z)*sp.erfc(rr - z/(2*rr)) + sp.exp(z)*sp.erfc(rr + z/(2*rr)))
K0z = (4*sp.pi*sp.I*t)**sp.Rational(-1, 2)*sp.exp(sp.I*z**2/(4*t))
e1 = sp.I*sp.diff(G, t) + sp.diff(G, z, 2)
e2 = -sp.diff(G, z, 2) + G - K0z
for name, e in [('G: i G_t = -G_zz', e1), ('G: (-d2+1) G = K0', e2)]:
    f = sp.lambdify((t, z), e, 'mpmath')
    vals = [abs(f(mp.mpf(tv), mp.mpf(zv))) for tv, zv in [(0.2, 0.5), (1.0, -1.3), (2.5, 3.0), (0.05, 0.1)]]
    report(name, max(vals) < 1e-12, [mp.nstr(v, 3) for v in vals])
# limite t -> 0+: G -> e^{-|z|}/2
fG = sp.lambdify((t, z), G, 'mpmath')
vals = [abs(fG(mp.mpf('1e-8'), mp.mpf(zv)) - mp.e**(-abs(zv))/2) for zv in [0.5, -1.2, 2.0]]
report('G(0+) = e^{-|z|}/2', max(vals) < 1e-6, [mp.nstr(v, 3) for v in vals])
# confronto con la definizione di Fourier (smorzata: t -> t - i eps non serve, integrale assolutamente convergente)
def Gfourier(tv, zv):
    g = lambda k: mp.e**(1j*k*zv - 1j*tv*k**2)/(1+k**2)
    return mp.quad(g, mp.linspace(-60, 60, 241))/(2*mp.pi) + 0  # code ~ 1/60: errore ~1e-2 trascurabile? usiamo coda analitica
# coda: |∫_{|k|>60}| <= 2/60 ; confronto con tolleranza 0.04
vals = [abs(Gfourier(tv, zv) - fG(mp.mpf(tv), mp.mpf(zv))) for tv, zv in [(0.5, 0.3), (1.5, -1.0)]]
report('G = integrale di Fourier (tolleranza coda 0.04)', max(vals) < 0.04, [mp.nstr(v, 3) for v in vals])

# nucleo di U_q: K_q = e^{it}/2 sech x sech y + (d_x - tanh x)(d_y - tanh y) G(t, x-y)
Gxy = G.subs(z, x - y)
Kq = sp.exp(sp.I*t)/2*sp.sech(x)*sp.sech(y) + (sp.diff(sp.diff(Gxy, y) - sp.tanh(y)*Gxy, x) - sp.tanh(x)*(sp.diff(Gxy, y) - sp.tanh(y)*Gxy))
eq = sp.I*sp.diff(Kq, t) + sp.diff(Kq, x, 2) + 2*sp.sech(x)**2*Kq
f = sp.lambdify((t, x, y), eq, 'mpmath')
vals = [abs(f(mp.mpf(a_), mp.mpf(b_), mp.mpf(c_))) for a_, b_, c_ in [(0.3, 0.2, -0.5), (1.0, 1.5, 0.7), (2.0, -0.8, 2.2)]]
report('PT: K_q risolve i K_t = (-d2 - 2 sech^2) K', max(vals) < 1e-10, [mp.nstr(v, 3) for v in vals])
fK = sp.lambdify((t, x, y), Kq, 'mpmath')
vals = [abs(fK(mp.mpf(a_), mp.mpf(b_), mp.mpf(c_)) - fK(mp.mpf(a_), mp.mpf(c_), mp.mpf(b_))) for a_, b_, c_ in [(0.3, 0.2, -0.5), (1.0, 1.5, 0.7)]]
report('PT: simmetria K_q(x,y) = K_q(y,x)', max(vals) < 1e-12, [mp.nstr(v, 3) for v in vals])
# completezza a t = 0: A (L0+1)^{-1} A^dag f + P_b f = f
fx = lambda u: mp.e**(-u**2)*(1+u)
dfx = lambda u: mp.e**(-u**2)*(1 - 2*u*(1+u))
Adag_f = lambda u: -dfx(u) - mp.tanh(u)*fx(u)
def h(u):   # (L0+1)^{-1} A^dag f = 1/2 e^{-|u-v|} * A^dag f
    return mp.quad(lambda v: mp.e**(-abs(u-v))/2*Adag_f(v), [-12, u, 12])
def dh(u):
    return mp.quad(lambda v: -mp.sign(u-v)*mp.e**(-abs(u-v))/2*Adag_f(v), [-12, u, 12])
cb = mp.quad(lambda v: mp.sech(v)*fx(v), [-12, 12])
vals = []
for u in [-1.0, 0.0, 0.4, 1.7]:
    lhs = dh(u) - mp.tanh(u)*h(u) + mp.sech(u)*cb/2
    vals.append(abs(lhs - fx(u)))
report('PT: A(L0+1)^{-1}A^dag + P_b = I (su f test)', max(vals) < 1e-10, [mp.nstr(v, 3) for v in vals])
# stato legato: L_q sech = -sech
L = lambda g: -sp.diff(g, x, 2) - 2*sp.sech(x)**2*g
report('PT: L_q sech = -sech', sp.simplify((L(sp.sech(x)) + sp.sech(x)).rewrite(sp.exp)) == 0)
# A^dag L_q = L_0 A^dag (encoder differenziale, A^dag = -d - tanh)
g = sp.Function('g')(x)
Ad = lambda w: -sp.diff(w, x) - sp.tanh(x)*w
r = sp.simplify((Ad(L(g)) - (-sp.diff(Ad(g), x, 2))).rewrite(sp.exp))
report('PT: A^dag L_q = L_0 A^dag', r == 0, r)

# 5. sviluppo di A9 al 2o ordine: E^mult = (t^2/2)[L0,V] + O(t^3); E^add = -(t^2/2){L0,V} + O(t^3)
# controllo simbolico con serie di matrici formali non commutative
A_, B_ = sp.symbols('L0 V', commutative=False)
def expser(X, n=3):
    return sum(((-sp.I*t)**k/sp.factorial(k))*X**k for k in range(n+1))
U = expser(A_+B_); U0 = expser(A_); UV = expser(B_)
Em = sp.expand(U - U0*UV); Ea = sp.expand(U - U0 - UV + 1)
c2m = sp.expand(Em).coeff(t, 2); c2a = sp.expand(Ea).coeff(t, 2)
report('A9: coeff t^2 di E^mult = (1/2)[L0,V]', sp.expand(c2m - (A_*B_ - B_*A_)/2) == 0, c2m)
report('A9: coeff t^2 di E^add = -(1/2){L0,V}', sp.expand(c2a + (A_*B_ + B_*A_)/2) == 0, c2a)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
