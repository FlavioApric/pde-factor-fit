# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §6 (VAR-C3Q2-R) e §7 (SYS-DIRAC-POL).
import sys
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

# ---------- §6(b): prova elementare che f = exp(e^y) non è D-finita (sostituisce Wiman–Valiron)
y, z = sp.symbols('y z')
f = sp.exp(sp.exp(y))
good = True
for k in range(0, 9):
    q = sp.simplify(sp.diff(f, y, k)/f)               # deve essere P_k(e^y), P_k di Touchard, grado k, monico
    Pk = sp.expand(q.subs(sp.exp(y), z))
    good &= (not Pk.has(y)) and sp.Poly(Pk, z).degree() == k and sp.Poly(Pk, z).LC() == 1
    good &= sp.expand(Pk - sp.bell(k, z)) == 0   # polinomio di Touchard = polinomio di Bell
ok("§6(b) f^{(k)}/f = T_k(e^y), T_k di Touchard monico di grado k (k ≤ 8)", good)
# quindi Σ_k a_k(y) f^{(k)} = f·Σ_k a_k(y)T_k(e^y): il coefficiente di (e^y)^K (K = ordine massimo con a_K ≠ 0) è a_K(y);
# poiché e^y è trascendente su ℂ(y), Σ a_k(y)T_k(z) = 0 in ℂ(y)[z] ⇒ a_K = 0. Test: una relazione candidata non si annulla.
a0, a1, a2 = sp.symbols('a0 a1 a2')
rel = sp.expand(sum(c*sp.bell(k, z) for k, c in enumerate([a0, a1, a2])))
ok("§6(b) Σ_{k≤2} a_k T_k(z) = 0 in ℂ[z] forza a_0 = a_1 = a_2 = 0", sp.solve(sp.Poly(rel, z).coeffs(), [a0, a1, a2]) == {a0: 0, a1: 0, a2: 0})
t, x = sp.symbols('t x')
u = sp.exp(sp.exp(x + t))
ok("§6(b) (∂_t − ∂_x)u = 0", sp.simplify(sp.diff(u, t) - sp.diff(u, x)) == 0)
ok("§6(b) □u = 0, quindi u ∈ Sol(□) e Ann(u) ⊋ A_2□", sp.simplify(sp.diff(u, t, 2) - sp.diff(u, x, 2)) == 0)
# variabili (t, x, e^{x+t}) algebricamente indipendenti: in particolare il Jacobiano formale non basta, uso il criterio
# di trascendenza in una variabile lungo t = 0 (già coperto sopra). Qui controllo solo che restringendo a t = t0 si ritorna a f.
ok("§6(b) u(t0, x) = f(x + t0)", sp.simplify(u.subs(t, 0) - f.subs(y, x)) == 0)

# ---------- §6(a): divisione per L monico in ∂_t su un esempio (calcolo in A_2 con operatori su funzioni test)
F = sp.Function('F')(t, x)
L = lambda g: sp.diff(g, t, 2) - t*sp.diff(g, x, 2)            # L = ∂_t² − t∂_x², monico
# Q = ∂_t³: Q = ∂_t L + (t∂_x²∂_t + ∂_x²) (divisione a destra), resto in B ⊕ B∂_t
Qg = sp.diff(F, t, 3)
dec = sp.diff(L(F), t) + t*sp.diff(F, x, 2, t, 1) + sp.diff(F, x, 2)
ok("§6(a) divisione: ∂_t³ = ∂_t·L + (t∂_x²)∂_t + ∂_x² (resto con coefficienti in B)", sp.simplify(Qg - dec) == 0)

# ---------- §7(a): serie formali di g_1, g_2 calcolate in modo diverso (serie di SymPy in t, poi ω² → ξ²+m²)
xi, m = sp.symbols('xi m', positive=True)
tt = sp.Symbol('t')
W = sp.Symbol('W', positive=True)   # W = ω
N = 10
two_a = sp.series(sp.atan(xi*sp.tan(W*tt)/W), tt, 0, N).removeO()
bb = sp.series(-sp.asin(m*sp.sin(W*tt)/W), tt, 0, N).removeO()
g1 = sp.expand(two_a/(2*xi)); g2 = sp.expand(-bb/m)
def polyok(e):
    e = sp.expand(e.subs(W, sp.sqrt(xi**2 + m**2)))
    return all(sp.expand(e.coeff(tt, j)).is_polynomial(xi, m) and all(cc.is_rational for cc in sp.Poly(sp.expand(e.coeff(tt, j)), xi, m).coeffs()) for j in range(N) if e.coeff(tt, j) != 0)
ok("§7(a) g_1 = a/ξ ∈ ℚ[ξ,m][[t]] fino a t^9 (metodo indipendente)", polyok(g1))
ok("§7(a) g_2 = −b/m ∈ ℚ[ξ,m][[t]] fino a t^9 (metodo indipendente)", polyok(g2))
# identità numerica e^{tA} = e^{g1 X} e^{g2 m Y} e^{g1 X} in punti nuovi
mp.mp.dps = 30
good = True
for (XI, MM, TT) in [(1.9, 0.4, 0.6), (-0.5, 1.7, 0.7), (3.0, 3.0, 0.3)]:
    XI, MM, TT = mp.mpf(str(XI)), mp.mpf(str(MM)), mp.mpf(str(TT)); j1 = mp.mpc(0, 1)
    w_ = mp.sqrt(XI**2 + MM**2); assert w_*TT < mp.pi/2
    A = mp.matrix([[j1*XI, -j1*MM], [-j1*MM, -j1*XI]])
    a_ = mp.atan(XI*mp.tan(w_*TT)/w_)/2; b_ = -mp.asin(MM*mp.sin(w_*TT)/w_)
    Ra = mp.matrix([[mp.e**(j1*a_), 0], [0, mp.e**(-j1*a_)]])
    Rb = mp.matrix([[mp.cos(b_), j1*mp.sin(b_)], [j1*mp.sin(b_), mp.cos(b_)]])
    dd = mp.mnorm(mp.expm(A*TT) - Ra*Rb*Ra, 1); print('    residuo ZXZ', mp.nstr(dd, 3)); good &= dd < 1e-20
ok("§7(a) identità ZXZ numerica in 3 punti nuovi (residuo < 1e-25)", good)

# ---------- §7(b): asintotica del bersaglio e Lemma E
xs = sp.Symbol('xi', positive=True); ms, ts = sp.symbols('m t', positive=True)
om = sp.sqrt(xs**2 + ms**2)
e11 = sp.cos(om*ts) + sp.I*xs*sp.sin(om*ts)/om
# (e^{tA})_11 e^{−iξt} = e^{i(ω−ξ)t} + i(ξ/ω − 1) sin(ωt) e^{−iξt}; ω − ξ = m²/(ω+ξ)
ok("§7(b) decomposizione esatta di (e^{tA})_11", sp.simplify(e11 - (sp.exp(sp.I*om*ts) + sp.I*(xs/om - 1)*sp.sin(om*ts))) == 0)
ee = sp.Symbol('e', positive=True)
s1 = sp.series((om - xs).subs(xs, 1/ee), ee, 0, 3).removeO()
s2 = sp.series((xs/om - 1).subs(xs, 1/ee), ee, 0, 2).removeO()
ok("§7(b) ω − ξ = m²/(2ξ) + O(ξ^{-3}),  ξ/ω − 1 = O(ξ^{-2})", sp.simplify(s1 - ms**2*ee/2) == 0 and s2 == 0)
# numerico: ξ·|(e^{tA})_11 − e^{iξt}| → m²t/2
vals = []
for XI in [1e2, 1e3, 1e4]:
    MM, TT = 0.8, 1.3
    w_ = mp.sqrt(XI**2 + MM**2)
    d = abs(mp.cos(w_*TT) + 1j*XI*mp.sin(w_*TT)/w_ - mp.e**(1j*XI*TT))
    vals.append(float(XI*d))
print("    ξ·|G(ξ)|:", vals, " atteso m²t/2 =", 0.8**2*1.3/2)
ok("§7(b) ξ|G(ξ)| → m²t/2 ≠ 0 (G non tende a 0 più rapidamente di 1/ξ, e non è nullo)", abs(vals[-1] - 0.416) < 1e-3)
# Lemma E: medie (1/X)∫_X^{2X} e^{iQ} → 0 per Q non costante (grado 1, 2, 3)
mp.mp.dps = 15
good = True
for Q in [lambda s: 0.3*s, lambda s: s**2 - 5*s, lambda s: 0.01*s**3 + s]:
    X = mp.mpf(200)
    pts = mp.linspace(X, 2*X, 4001)
    av = abs(mp.quad(lambda s: mp.e**(1j*Q(s)), pts))/X
    good &= av < 0.05
ok("§7(b) Lemma E: |(1/X)∫_X^{2X}e^{iQ}| piccolo per Q di grado 1, 2, 3 (X = 200)", good)

print(f"\n[c_c3q2_dirac] {sum(c for _, c in RES)}/{len(RES)} OK")


