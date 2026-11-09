# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §1 (VAR-P11(e)), §2 (VAR-Q18-CE), §4 (VAR-Q17).
import sys
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

t, r, s, n, h = sp.symbols('t r s n h', positive=True)

# ---- §1, Lemma C in dimensione finita: F(t) = ∫_s^t e^{(t-r)A} f(r) dr, A F = F' - f, F' = e^{(t-s)A} f(s) + ∫ e^{(t-r)A} f'(r) dr
A = sp.Matrix([[0, 1], [0, 0]])   # nilpotente: e^{tA} = I + tA, integrali elementari
f = sp.Matrix([sp.sin(r), r**2])
s0 = sp.Integer(0)
E = lambda tau: (A*tau).exp()
F = (E(t - r)*f).applyfunc(lambda e: sp.integrate(sp.simplify(e), (r, s0, t)))
F = F.applyfunc(sp.simplify)
Fp = F.diff(t)
Fp_formula = E(t - s0)*f.subs(r, s0) + (E(t - r)*f.diff(r)).applyfunc(lambda e: sp.integrate(sp.simplify(e), (r, s0, t)))
ok("§1 Lemma C: F' = T(t-s)f(s) + ∫T(t-r)f'(r)dr (matrice 2x2)", (Fp - Fp_formula).applyfunc(sp.simplify) == sp.zeros(2, 1))
ok("§1 Lemma C: A F = F' - f", (A*F - (Fp - f.subs(r, t))).applyfunc(sp.simplify) == sp.zeros(2, 1))

# ---- §2, VAR-Q18-CE: equazione mite componente per componente (con ‖x‖ = n)
Cf = sp.sin(n*t)/n
c = sp.cos(n*t)
first = sp.integrate(c.subs(t, r), (r, 0, t))          # coefficiente di T(t)x nella prima componente
ok("§2 prima componente: ∫_0^t c = C(t)", sp.simplify(first - Cf) == 0)
second = 1 - sp.integrate((Cf*n**2).subs(t, r), (r, 0, t))   # ⟨y(r), f(r)⟩ = C(r) n²
ok("§2 seconda componente: 1 − ∫⟨y,f⟩ = cos(nt)", sp.simplify(second - c) == 0)
# antiaggiunzione di B(t)(y,c) = (c f, −⟨y,f⟩) su un modello finito ℂ^3 ⊕ ℂ con f casuale
fv = sp.Matrix([1 + 2*sp.I, -1, sp.I/3])
Bm = sp.zeros(4, 4)
Bm[0:3, 3] = fv
Bm[3, 0:3] = -fv.H
ok("§2 B antiaggiunto (B^* = −B) sul modello finito", (Bm.H + Bm) == sp.zeros(4, 4))
# norma di B(t) − B(t'): sul modello, ‖ΔB‖ = ‖Δf‖ (≤ 2‖Δf‖ come in D5)
df = sp.Matrix([0.3, -0.1j, 0.2])
dB = sp.zeros(4, 4); dB[0:3, 3] = df; dB[3, 0:3] = -df.H
nrm = max(abs(complex(e)) for e in (dB.H*dB).eigenvals().keys())**0.5
ok("§2 ‖B(t)−B(t')‖ = ‖f(t)−f(t')‖ ≤ 2‖f(t)−f(t')‖", abs(nrm - float(sp.sqrt((df.H*df)[0]).evalf())) < 1e-12)
# modello infinito: H = L²(T), A = d/dθ, x = Σ_{k≥1} e^{ikθ}/k ∉ D(A): Σ k²|x_k|² = Σ 1 diverge,
# mentre C(t)T(t)x ha coefficienti C(t)e^{ikt}/k: stessa divergenza se C(t) ≠ 0
kk = sp.Symbol('k', positive=True, integer=True)
ok("§2 x = Σ e^{ikθ}/k: x ∈ L² ma ∉ D(d/dθ)", sp.summation(1/kk**2, (kk, 1, sp.oo)).is_finite and sp.summation(kk**2/kk**2, (kk, 1, sp.oo)) == sp.oo)

# ---- §4, gauge e lemma delle medie (termine di bordo)
xx = sp.Symbol('x', real=True)
V0 = sp.Function('V0'); v = sp.Function('v'); pt = sp.Function('pt')
psi_t = sp.exp(-sp.I*sp.Integral(v(s), (s, 0, t)))*pt(t, xx)
res = sp.I*sp.diff(psi_t, t) + sp.diff(psi_t, xx, 2) - (V0(xx) + v(t))*psi_t
# se pt risolve con V0: i pt_t = -pt_xx + V0 pt
res = res.subs(sp.Derivative(pt(t, xx), t), (-pt(t, xx).diff(xx, 2) + V0(xx)*pt(t, xx))/sp.I)
ok("§4 gauge: e^{-i∫v}ψ̃ risolve con V_0 + v", sp.simplify(sp.expand(res.doit())) == 0)
# A ∫_0^a e^{σA} k(σ) dσ = k(a)e^{aA} − k(0) − ∫ e^{σA}k'(σ)dσ (termine di bordo −k(0) quando k(0) = h(r) ≠ 0)
sig, a = sp.symbols('sigma a', positive=True)
kf = 1 + sig**2
lhs = A*(E(sig)*kf).applyfunc(lambda e: sp.integrate(e, (sig, 0, a)))
rhs = kf.subs(sig, a)*E(a) - kf.subs(sig, 0)*sp.eye(2) - (E(sig)*sp.diff(kf, sig)).applyfunc(lambda e: sp.integrate(e, (sig, 0, a)))
ok("§4 lemma delle medie: formula con termine di bordo k(0)", (lhs - rhs).applyfunc(sp.simplify) == sp.zeros(2))

print(f"\n[c_semigroup] {sum(c for _, c in RES)}/{len(RES)} OK")

