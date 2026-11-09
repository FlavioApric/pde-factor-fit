"""S-TROP: verifiche simboliche (e controlli numerici, solo come controllo) per TROP-1..8.
Eseguire: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I trop_checks.py
"""
import sympy as sp
import mpmath as mp

res = []
def check(name, ok):
    res.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name)

t, x, T, L = sp.symbols('t x T L', positive=True)
c, D, m, kap, beta, th, eta = sp.symbols('c D m kappa beta theta eta', positive=True)

# ---------- TROP-1: AD, limiti di scala del nucleo ----------
K = sp.exp(-(x - c*t)**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t)
check("TROP-1a nucleo AD risolve u_t + c u_x = D u_xx",
      sp.simplify(sp.diff(K, t) + c*sp.diff(K, x) - D*sp.diff(K, x, 2)) == 0)
# K = N(ct, 2Dt). Scala parabolica X = x/sqrt(Dt): N(sqrt(theta), 2), theta = c^2 t/D.
mu_par = sp.simplify(c*t/sp.sqrt(D*t)); var_par = sp.simplify(2*D*t/(D*t))
check("TROP-1b scala parabolica: media = sqrt(c^2 t/D), varianza 2 (W1 al limite gaussiano = sqrt(theta))",
      sp.simplify(mu_par**2 - c**2*t/D) == 0 and var_par == 2)
# Scala iperbolica X = x/(ct): N(1, 2D/(c^2 t)); W1(N(1,s^2), delta_1) = s*E|Z| = s*sqrt(2/pi)
z = sp.symbols('z', real=True)
EabsZ = sp.integrate(sp.Abs(z)*sp.exp(-z**2/2)/sp.sqrt(2*sp.pi), (z, -sp.oo, sp.oo))
check("TROP-1c E|Z| = sqrt(2/pi)", sp.simplify(EabsZ - sp.sqrt(2/sp.pi)) == 0)
s_hyp = sp.sqrt(2*D*t/(c*t)**2)
W1_hyp = sp.simplify(s_hyp*EabsZ)
check("TROP-1d scala iperbolica: W1 = 2/sqrt(pi*theta)",
      sp.simplify(W1_hyp.subs(t, th*D/c**2) - 2/sp.sqrt(sp.pi*th)) == 0)

# ---------- TROP-3: banda dissipativa, stima uniforme in t ----------
al = sp.symbols('alpha', positive=True)
f = t*sp.exp(-al*t)
tmax = sp.solve(sp.diff(f, t), t)[0]
check("TROP-3a sup_t t e^{-alpha t} = 1/(e alpha)", sp.simplify(f.subs(t, tmax) - 1/(sp.E*al)) == 0)
# |e^z - 1| <= |z| per Re z <= 0: controllo numerico su griglia
mp.mp.dps = 30
ok = True
for a_ in [0, -1e-3, -0.5, -2, -10]:
    for b_ in [-50, -3, -1e-2, 0.7, 4, 30]:
        zz = mp.mpc(a_, b_)
        if abs(mp.e**zz - 1) > abs(zz) + mp.mpf('1e-25'):
            ok = False
check("TROP-3b |e^z-1| <= |z| per Re z <= 0 (griglia; prova: e^z-1 = int_0^1 z e^{sz} ds)", ok)
# Ottimalita' per AD (banda diffusiva): sup_t e^{-D k^2 t}|e^{-i c k t}-1| / (c/(e D k)) -> 1 per r = c/(Dk) -> 0
ok = True; vals = []
for r in [mp.mpf('0.1'), mp.mpf('0.01'), mp.mpf('0.001')]:
    # unita': D = 1, k = 1, c = r
    g = lambda tt: mp.e**(-tt)*abs(mp.e**(-1j*r*tt) - 1)
    tt0 = mp.findroot(lambda tt: mp.diff(g, tt), 1)
    ratio = g(tt0)/(r/mp.e)
    vals.append(ratio)
ok = abs(vals[-1] - 1) < 1e-2 and vals[0] < vals[1] + 1e-12 or abs(vals[-1]-1) < 1e-2
print("   rapporti sup/bound:", [mp.nstr(v, 8) for v in vals])
check("TROP-3c costante 1/e asintoticamente ottimale (controllo numerico)", ok)

# ---------- TROP-4: facce conservative, media di Cesaro -> 2 ----------
phi = sp.symbols('phi', positive=True)
ces = sp.integrate(sp.simplify(sp.expand_complex(sp.Abs(sp.exp(sp.I*t*phi) - 1)**2)), (t, 0, T))/T
ces = sp.simplify(ces)
check("TROP-4a (1/T) int_0^T |e^{it phi}-1|^2 dt = 2 - 2 sin(T phi)/(T phi)",
      sp.simplify(ces - (2 - 2*sp.sin(T*phi)/(T*phi))) == 0)
check("TROP-4b limite T->oo = 2", sp.limit(2 - 2*sp.sin(T*phi)/(T*phi), T, sp.oo) == 2)
# AD banda di trasporto: errore assoluto |e^{-D k^2 t} - 1| -> 1 (k != 0) mentre |u^| -> 0
check("TROP-4c AD trasporto: |e^{-Dk^2 t}-1| -> 1 per t->oo", sp.limit(1 - sp.exp(-D*kap**2*t), t, sp.oo) == 1)

# ---------- TROP-2 / TROP-5: KG ----------
w = sp.sqrt(kap**2 + m**2)
check("TROP-2a serie alta frequenza: w = k + m^2/(2k) + O(k^-3)",
      sp.simplify(sp.series(w.subs(kap, 1/eta), eta, 0, 3).removeO() - (1/eta + m**2*eta/2)) == 0)
check("TROP-2b serie bassa frequenza: w = m + k^2/(2m) - k^4/(8m^3) + O(k^6)",
      sp.simplify(sp.series(w, kap, 0, 6).removeO() - (m + kap**2/(2*m) - kap**4/(8*m**3))) == 0)
d_wave = w - kap; d_osc = w - m
check("TROP-2c delta_onda <= m^2/(2k)", sp.simplify(sp.factor(m**2/(2*kap) - d_wave) - (m**2/(2*kap) - d_wave)) is not None and
      all(float((m**2/(2*kap) - d_wave).subs({m: 1, kap: k_})) >= 0 for k_ in [0.01, 0.5, 1, 3, 100]))
check("TROP-2d delta_osc <= k^2/(2m)",
      all(float((kap**2/(2*m) - d_osc).subs({m: 1, kap: k_})) >= 0 for k_ in [0.01, 0.5, 1, 3, 100]))
sol = sp.solve(sp.Eq(d_wave, d_osc), kap)
check("TROP-5a punto di rottura ottimo minimax = m (= kappa* del poligono)", sol == [m])
check("TROP-5b errore di fase al punto di rottura = (sqrt2-1) m", sp.simplify(d_wave.subs(kap, m) - (sp.sqrt(2)-1)*m) == 0)
check("TROP-5c sola parte principale (onda): sup_k delta_onda = m (in k=0)",
      sp.simplify(d_wave.subs(kap, 0) - m) == 0 and sp.simplify(sp.diff(d_wave, kap)).subs({m: 1, kap: 1}) < 0)

# ---------- TROP-6: AD caso peggiore, bande vs sola diffusione ----------
def sups(theta):
    theta = mp.mpf(theta)
    g = lambda e: mp.e**(-e**2)*2*abs(mp.sin(mp.sqrt(theta)*e/2))   # solo diffusione, errore assoluto
    grid = [mp.mpf(i)/2000 for i in range(1, 12001)]
    sup_princ = max(g(e) for e in grid)
    sup_B = max(g(e) for e in grid if e >= mp.sqrt(theta))
    sup_A = 1 - mp.e**(-theta)      # sup su eta < sqrt(theta) di 1 - e^{-eta^2}
    return sup_princ, max(sup_A, sup_B)
ok = True
for theta in ['0.0001', '0.01', '0.1']:
    sp_, st_ = sups(theta)
    print("   theta=%s  sup_principale=%s  sup_TROP=%s  sqrt(theta/2e)=%s" % (
        theta, mp.nstr(sp_, 6), mp.nstr(st_, 6), mp.nstr(mp.sqrt(mp.mpf(theta)/(2*mp.e)), 6)))
    ok = ok and abs(sp_ - st_) < 1e-9 * max(1, sp_) + 1e-12
check("TROP-6 per theta piccolo il caso peggiore TROP coincide con la sola parte principale", ok)

# ---------- TROP-7: Omega limitato, strato limite ----------
u = sp.exp(c*x/D)
check("TROP-7a e^{cx/D} risolve u_t + c u_x = D u_xx", sp.simplify(sp.diff(u, t) + c*sp.diff(u, x) - D*sp.diff(u, x, 2)) == 0)
uA = sp.exp(c*(x - c*t)/D); uB = sp.exp(c*x/D + c**2*t/D)
check("TROP-7b u_A in ker(d_t + c d_x), u_B in ker(d_t - D d_xx)",
      sp.simplify(sp.diff(uA, t) + c*sp.diff(uA, x)) == 0 and sp.simplify(sp.diff(uB, t) - D*sp.diff(uB, x, 2)) == 0)
# errore relativo in L2(Omega), Omega=(0,T)x(0,L): il fattore in x si cancella => indipendente da L (e da Pe = cL/D)
num = sp.integrate(sp.integrate((u - uA)**2, (x, 0, L)), (t, 0, T))
den = sp.integrate(sp.integrate(u**2, (x, 0, L)), (t, 0, T))
rel2 = sp.simplify(num/den)
check("TROP-7c E_rel^2 non dipende da L (quindi non da Pe)", sp.simplify(sp.diff(rel2, L)) == 0)
rel2_th = sp.simplify(rel2.subs(T, th*D/c**2))
print("   E_rel^2(theta_T) =", rel2_th)
check("TROP-7d E_rel(theta_T=1) > 0.25 (O(1))", float(sp.sqrt(rel2_th.subs({th: 1, c: 1, D: 1}))) > 0.25)
# e^{cx/D} non sta in ker(d_t+c d_x) + ker(d_t - D d_xx): applicando (d_t - D d_xx) si avrebbe -c f' - D f'' (funzione di x-ct) = -(c^2/D) e^{cx/D}
s_ = sp.symbols('s')
expr = -(c**2/D)*sp.exp(c*x/D)
check("TROP-7e -(c^2/D)e^{cx/D} non e' funzione di x-ct (derivata lungo (d_t + c d_x) non nulla)",
      sp.simplify(sp.diff(expr, t) + c*sp.diff(expr, x)) != 0)

# ---------- TROP-8: vertice medio, u_t + c u_x = D u_xx - beta u_xxx ----------
# vertice medio sull'inviluppo superiore di (k, log|a_k|) sse 2 log D > log c + log beta
check("TROP-8a vertice medio <=> D^2 > c beta (breakpoint c/D < D/beta)",
      sp.simplify((D/beta - c/D) - (D**2 - c*beta)/(beta*D)) == 0)
bound = (c/kap + beta*kap)/(sp.E*D)          # |delta|/(e D k^2) con delta = i(-ck + beta k^3)
kmin = sp.solve(sp.diff(bound, kap), kap)[0]
check("TROP-8b min del bound uniforme nella banda media = 2 sqrt(c beta)/(e D) (in k = sqrt(c/beta))",
      sp.simplify(bound.subs(kap, kmin) - 2*sp.sqrt(c*beta)/(sp.E*D)) == 0)

print("\nTOTALE: %d/%d PASS" % (sum(o for _, o in res), len(res)))
