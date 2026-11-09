# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §17 (DM-δ-MINIMAX), compreso il kill-argument.
import sys
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

t, x, yv = sp.symbols('t x y', real=True)
eps, c0, x0, d0 = sp.symbols('epsilon c0 x0 delta0', positive=True)
# φ concreta: φ(y) = y² e^{−y²}·(normalizzata), φ(0) = 0, φ''(0) = 2 ≠ 0 (la troncatura C_c^∞ non cambia nulla vicino a 0)
phi = yv**2*sp.exp(-yv**2)
ok("§17 φ(0) = 0, φ''(0) ≠ 0, sup|φ| = e^{-1} ≤ 1", phi.subs(yv, 0) == 0 and sp.diff(phi, yv, 2).subs(yv, 0) == 2 and sp.N(sp.maximum(phi, yv, sp.Interval(-10, 10))) <= 1)
h = eps*phi.subs(yv, (x - x0)/eps**sp.Rational(1, 3))
for k in range(4):
    dk = sp.simplify(sp.diff(h, x, k).subs(x, x0 + eps**sp.Rational(1, 3)*yv))
    ok(f"§17 ∂_x^{k} h = ε^{{1−{k}/3}} φ^({k})", sp.simplify(dk - eps**(1 - sp.Rational(k, 3))*sp.diff(phi, yv, k)) == 0)
u1 = c0                       # costante, |u_1| = c0 ≥ 2δ_0
u2 = u1 + h
V = lambda u: (sp.I*sp.diff(u, t) + sp.diff(u, x, 2))/u
dV = sp.simplify((V(u2) - V(u1)).subs(x, x0))
ok("§17 V_{u_2} − V_{u_1} in x_0 = ε^{1/3}φ''(0)/u_1", sp.simplify(dV - eps**sp.Rational(1, 3)*2/c0) == 0)
# dato intermedio: ‖ũ − u_i‖ = ‖h‖/2 ≤ ε/2
ok("§17 ũ = u_1 + h/2 è ε-vicino a u_1 e u_2", sp.N(sp.maximum(phi, yv, sp.Interval(-10, 10))/2) <= 1)
# vincolo |u_2| ≥ δ_0: |u_2| ≥ c0 − ε ≥ δ_0 se c0 ≥ 2δ_0 e ε ≤ δ_0;  vincolo |u_2| ≤ M (derivata d'ordine 0) richiede c0 + ε ≤ M
# ⇒ serve M ≥ 2δ_0 + ε (fix D39: dichiarare M > 2δ_0, o M ≥ 4δ_0 come margine "derivate ≤ M/2")
ok("§17 D39: con u_1 ≡ 2δ_0 e ‖u_1‖ ≤ M/2 serve M ≥ 4δ_0 (ipotesi non scritta)", sp.solve(sp.Eq(2*d0, sp.Symbol('M', positive=True)/2), sp.Symbol('M', positive=True)) == [4*d0])

# limite superiore: rapporto ‖V_u − V_{u*}‖/ε^{1/3} sulla famiglia nitida u = 1 + a sin(kx), u* = 1, a = ε, k = (M/ε)^{1/3}
mp.mp.dps = 20
Mv = mp.mpf(1)
rat = []
for ev in [mp.mpf('1e-3'), mp.mpf('1e-5'), mp.mpf('1e-7')]:
    kk = (Mv/ev)**(mp.mpf(1)/3)
    # ‖V‖ = sup a k² |sin|/(1 + a sin) ≈ a k² = ε^{1/3}M^{2/3}
    Vn = max(abs(ev*kk**2*mp.sin(s)/(1 + ev*mp.sin(s))) for s in mp.linspace(0, 2*mp.pi, 2001))
    rat.append(float(Vn/ev**(mp.mpf(1)/3)))
print("    ‖ΔV‖/ε^{1/3} sulla famiglia sinusoidale:", rat)
ok("§17 la famiglia sinusoidale (derivate ≤ M) realizza anch'essa la scala ε^{1/3}", all(abs(r - 1) < 1e-2 for r in rat))
# kill-argument: un dato ε-vicino con |α| ≤ 3 limitate non permette di fare meglio di ε^{1/3} nemmeno usando u_t:
# h non dipende da t, quindi l'informazione temporale non aiuta (u_t identico per u_1 e u_2)
ok("§17 KA: h indipendente da t, ∂_t u_1 = ∂_t u_2 (l'osservazione in t non separa)", sp.diff(u2 - u1, t) == 0)

print(f"\n[c_dmdelta] {sum(c for _, c in RES)}/{len(RES)} OK")
