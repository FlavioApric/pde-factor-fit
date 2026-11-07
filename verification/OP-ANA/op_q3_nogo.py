# OP-ANA Q3 (P1-Q6): controlli (NON prove) di OPA-T3 / OPA-P3.
# log del rapporto  R(zeta)^2 = int_I |G(t-t0)|^2 e^{2 Re a t0} dt / ( (1+|zeta|)^{2mK} int_I e^{2 Re a t} dt )
# con G(s) = e^{s a} - sum_n e^{s a_n} + (N-1)  (dati esponenziali u = e^{a(zeta)t + zeta x}).
import mpmath as mp
mp.mp.dps = 30
ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond); print(("[OK] " if cond else "[FAIL] ") + name, flush=True)

def logR2(terms, zeta, t0, T=1.0, m=2):
    an = [p(zeta) for p in terms]; a = sum(an); N = len(an)
    K = 2  # grado massimo usato nei test
    G = lambda s: mp.e**(s*a) - sum(mp.e**(s*q) for q in an) + (N - 1)
    num = mp.quad(lambda t: abs(G(t - t0))**2*mp.e**(2*mp.re(a)*t0), mp.linspace(0, T, 41))
    den = mp.quad(lambda t: mp.e**(2*mp.re(a)*t), [0, T])
    return mp.log(num) - mp.log(den) - 2*m*K*mp.log(1 + abs(zeta))

# (1) Lemma di Fourier: sum_k e^{2 pi i e k/d} = 0 se d non divide e
fine = all(abs(sum(mp.e**(2j*mp.pi*e*k/d) for k in range(d))) < 1e-20 for d in range(2, 7) for e in range(1, 13) if e % d)
check("sum_k e^{2pi i e k/d} = 0 per d|e falso (d<=6, e<=12)", fine)

# (2) monomi di gradi distinti (AD: a1 = -c xi, a2 = D xi^2), direzione da Theta_+ / Theta_-, per t0 in {0, 0.5, 1}
AD = [lambda z: -z, lambda z: z**2]
for t0 in [0.0, 0.5, 1.0]:
    # t0 < T: Theta_+ (Re a -> +inf, a_2 = xi^2 sopra a): theta = 0;  t0 = T: Theta_- (cos2th<0, cos th<0): theta = 2pi/3
    th = 0.0 if t0 < 1 else 2*mp.pi/3
    vals = [logR2(AD, r*mp.e**(1j*th), t0) for r in [20, 80, 160]]
    check(f"AD, t0={t0}, theta={float(th):.3f}: log R^2 cresce (r=20,80,160: {[round(float(v),1) for v in vals]})", vals[0] < vals[1] < vals[2] and vals[2] > 10)
# tre monomi: a = i xi^3 + xi^2 - 2 xi  (dispersivo + diffusivo all'indietro + trasporto)
M3 = [lambda z: 1j*z**3, lambda z: z**2, lambda z: -2*z]
for t0 in [0.0, 1.0]:
    best = None
    for th in [k*mp.pi/24 + 0.01 for k in range(48)]:
        v = [logR2(M3, r*mp.e**(1j*th), t0, m=2) for r in [6, 12]]
        if v[1] > v[0] + 5: best = (th, v); break
    check(f"tre monomi (xi^3, xi^2, xi), t0={t0}: esiste una direzione con log R^2 crescente: {None if best is None else [float(x) for x in best[1]]}", best is not None)

# (3) eccezione proporzionale: a1 = theta a, a2 = (1-theta) a con a = xi^2
def prop(theta): return [lambda z: theta*z**2, lambda z: (1 - theta)*z**2]
# theta = 1/2: (TC) vale per ogni t0 -> rapporto limitato (polinomiale) lungo a(zeta) reale +- infinito
for t0 in [0.0, 0.5, 1.0]:
    vals = [logR2(prop(0.5), mp.sqrt(lam), t0, m=1) for lam in [100, 400, 1600]] + \
           [logR2(prop(0.5), 1j*mp.sqrt(lam), t0, m=1) for lam in [100, 400, 1600]]
    check(f"proporzionale theta=1/2, t0={t0}: log R^2 limitato (<= 5) su a=+-lambda: max {float(max(vals)):.2f}", max(vals) < 5)
# theta = 2 (l'altro termine ha -1): (TC) falsa -> illimitato
vals = [logR2(prop(2.0), mp.sqrt(lam), 0.0, m=1) for lam in [25, 100, 400]]
check(f"proporzionale theta=2, t0=0: log R^2 cresce: {[float(v) for v in vals]}", vals[0] < vals[1] < vals[2])
# theta = -0.3 / 1.3 con T=1: (TC) vale per t0 in [0.3/1.3, 1/1.3] = [0.2308, 0.7692]
def prop2(): return [lambda z: -0.3*z**2, lambda z: 1.3*z**2]
for t0, expect_bounded in [(0.5, False), (0.1, False)]:
    vals = [logR2(prop2(), mp.sqrt(lam), t0, m=1) for lam in [25, 100, 400]] + \
           [logR2(prop2(), 1j*mp.sqrt(lam), t0, m=1) for lam in [25, 100, 400]]
    grows = max(vals[0:3]) > 10 or max(vals[3:]) > 10
    check(f"theta=(-0.3,1.3), t0={t0}: illimitato atteso (theta=1.3>1): max log R^2 = {float(max(vals)):.1f}", grows)
def prop3(): return [lambda z: -0.3*z**2, lambda z: 0.6*z**2, lambda z: 0.7*z**2]   # somma 1, tutti <= 1
for t0, expect in [(0.5, "lim"), (0.1, "illim"), (0.9, "illim")]:
    vals = [logR2(prop3(), mp.sqrt(lam), t0, m=1) for lam in [25, 100, 400]] + \
           [logR2(prop3(), 1j*mp.sqrt(lam), t0, m=1) for lam in [25, 100, 400]]
    mx = float(max(vals))
    check(f"theta=(-0.3,0.6,0.7), t0={t0}: atteso {expect} (TC <=> t0 in [0.2308,0.7692]); max log R^2 = {mx:.1f}", (mx < 6) if expect == "lim" else (mx > 15))

# (4) classe (F) non proporzionale: a1 = xi^2, a2 = xi^2 + xi; curva a(zeta) = i y  (Re a = 0)
F = [lambda z: z**2, lambda z: z**2 + z]
def root(y, branch):
    # radici di 2 z^2 + z - i y = 0
    d = mp.sqrt(1 + 8j*y)
    return (-1 + (d if branch == 0 else -d))/4
for t0 in [0.0, 0.5, 1.0]:
    found = False
    for br in [0, 1]:
        for sgn in [1, -1]:
            v = [logR2(F, root(sgn*y, br), t0, m=2) for y in [1e4, 1e5, 1e6]]
            if v[0] < v[1] < v[2] and v[2] > 10: found = True
    check(f"classe (F) xi^2, xi^2+xi, t0={t0}: illimitato lungo a(zeta) in iR", found)
print(f"RISULTATO: {ok}/{tot} OK")
