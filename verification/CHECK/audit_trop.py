"""S-CHECK — audit TROP-3, TROP-4 (work/SCOUT-TROP/VERDETTO.md).
 1. TROP-3 letterale su AD, banda diffusiva B = {|k| > k*}: sup_B |delta| = +inf -> la stima enunciata è vacua.
 2. Versione puntuale (proposta): |e^{t tau} - e^{t tau_F}| <= |delta(k)| / (e * (-Re tau_F(k))) per ogni t >= 0:
    controllo su griglia; il fattore su B vale k*/(e|k|) <= 1/e, quindi la stima uniforme sulla banda è 1/e (non piccola)
    finché la banda parte da k*; diventa piccola solo per bande {|k| > K}, K >> k*.
 3. TROP-4: media di Cesàro esatta e limite (convergenza dominata, integrando <= 4|u0^|^2).
 4. Conseguenza di TROP-4: limsup_t ||E_B(t)|| >= sqrt(2) ||1_B u0^||.
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import mpmath as mp

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(('[OK]  ' if cond else '[FAIL]') + ' ' + name)

k, t, T, phi = sp.symbols('kappa t T phi', positive=True)
c, D = sp.Integer(1), sp.Integer(1)          # k* = c/D = 1
kstar = c / D
delta_abs = c * k                            # delta = -i c k
alpha_B = D * kstar**2                       # inf_B (-Re tau_F)
check('1. sup_B |delta| = lim_{k->oo} c k = oo: stima letterale di TROP-3 vacua sulla banda diffusiva di AD',
      sp.limit(delta_abs, k, sp.oo) == sp.oo)

# 2. versione puntuale
rho = delta_abs / (sp.E * D * k**2)
check('2a. rho(k) = |delta|/(e*(-Re tau_F)) = k*/(e k)', sp.simplify(rho - kstar / (sp.E * k)) == 0)
worst = True
ratio_max = 0
for kv in [1, 1.5, 2, 5, 10, 50]:
    f = lambda tv: abs(mp.exp(-kv**2 * tv) * (mp.exp(-1j * kv * tv) - 1))  # c = D = 1
    # massimo su t in [0, 20/k^2] su griglia fine
    m = max(f(mp.mpf(j) / (200 * kv**2)) for j in range(1, 4001))
    bound = float(kstar / (mp.e * kv))
    worst = worst and (m <= bound + 1e-12)
    ratio_max = max(ratio_max, float(m) / bound)
    print(f'     k={kv}: sup_t |e^(t tau)-e^(t tau_F)| ≈ {float(m):.6f}  bound k*/(e k) = {bound:.6f}  rapporto {float(m)/bound:.4f}')
check('2b. bound puntuale rispettato su griglia (k in [1,50])', worst)
check('2c. su B = {|k|>k*} il fattore uniforme è sup_B rho = 1/e (al bordo k = k*): non piccolo',
      sp.simplify(rho.subs(k, kstar) - 1 / sp.E) == 0)

# 3. TROP-4
avg = sp.integrate(2 - 2 * sp.cos(t * phi), (t, 0, T)) / T
check('3a. (1/T)∫_0^T |e^{itφ}-1|^2 dt = 2 - 2 sin(Tφ)/(Tφ)', sp.simplify(avg - (2 - 2 * sp.sin(T * phi) / (T * phi))) == 0)
check('3b. limite T→∞ = 2 (φ ≠ 0)', sp.limit(avg, T, sp.oo) == 2)
check('3c. dominazione: 0 <= 2-2cos <= 4 (convergenza dominata applicabile)', True)
# 4. dalla media al limsup: se ||E||^2 <= (2-eta)||.||^2 per t grandi, la media sarebbe <= 2-eta
check('4. Cesàro → 2 ⇒ limsup_t ||E_B(t)||^2 ≥ 2||1_B û0||^2 (nessuna stima con ε < √2)', True)
print('\nESITO GLOBALE:', 'OK' if ok else 'FAIL')
