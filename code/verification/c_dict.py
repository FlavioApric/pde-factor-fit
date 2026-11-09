# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §13 (DICT-ILIM-Hs), §14 (DICT-U3d-v), §15 (DICT-Q3-R), §16 (DICT-Q4-C).
import sys, math
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

# ---------- §13: algebra degli esponenti e nitidezza per scaling
s, N, j = sp.symbols('s N j', positive=True)
th = 2/(2*s + 2 + N)
ok("§13 θ(s + N/2) = 1 − θ", sp.simplify(th*(s + N/2) - (1 - th)) == 0)
thj = 1 - th*(j + N/2)
ok("§13 θ_j = 1 − θ(j + N/2) = 2(s+1−j)/(2s+2+N) = θ(s+1−j)", sp.simplify(thj - 2*(s + 1 - j)/(2*s + 2 + N)) == 0 and sp.simplify(thj - th*(s + 1 - j)) == 0)
# nitidezza: f = h·φ(x/ℓ): ‖f‖_{C^s} ~ hℓ^{-s}, ‖f‖_2 ~ hℓ^{N/2}, ‖f‖_{C^{s,1}} ~ hℓ^{-s-1}
ok("§13 esponente nitido: (N/2)θ − (s+1)(1−θ) = −s", sp.simplify((N/2)*th - (s + 1)*(1 - th) + s) == 0)
# Taylor con resto integrale (s = 2, N = 1) e stima |f − T_x| ≤ c_1 M r^{s+1}
x, y, sg = sp.symbols('x y sigma', real=True)
fx = sp.sin(3*x) + x**4
s2 = 2
Tx = sum(sp.diff(fx, x, k)*(y - x)**k/sp.factorial(k) for k in range(s2 + 1))
rem = (s2/sp.factorial(s2))*(y - x)**s2*sp.Integral((1 - sg)**(s2 - 1)*(sp.diff(fx, x, s2).subs(x, x + sg*(y - x)) - sp.diff(fx, x, s2)), (sg, 0, 1))
val = (fx.subs(x, y) - Tx - rem).subs({x: sp.Rational(1, 3), y: sp.Rational(7, 10)}).evalf(30)
ok("§13 passo 2: f(y) − T_x(y) = formula del resto (s = 2, N = 1)", abs(val) < 1e-25)
# disuguaglianza numerica su una famiglia di bump (N = 1, s = 1, Ω = (0,1)): rapporto limitato uniformemente in ℓ
mp.mp.dps = 20
ratios = []
for ell in [0.2, 0.1, 0.05, 0.02, 0.01]:
    bump = lambda z: mp.e**(-1/(1 - z**2)) if abs(z) < 1 else mp.mpf(0)
    f = lambda z, e=ell: bump((z - 0.5)/e)
    L2 = mp.sqrt(mp.quad(lambda z: f(z)**2, [0.5 - ell, 0.5, 0.5 + ell]))
    zs = [0.5 - ell + 2*ell*k/2000 for k in range(2001)]
    d1 = [mp.diff(f, z) for z in zs]
    C1 = max(max(abs(f(z)) for z in zs), max(abs(v) for v in d1))
    d2 = max(abs(mp.diff(f, z, 2)) for z in zs[::5])
    C11 = max(C1, d2)
    thv = 2/(2*1 + 2 + 1)
    ratios.append(float(C1/(L2**thv*C11**(1 - thv))))
print("    §13 rapporti ‖f‖_{C^1}/(‖f‖_2^θ‖f‖_{C^{1,1}}^{1−θ}):", [round(r, 3) for r in ratios])
ok("§13 rapporto limitato e non degenere per ℓ → 0 (θ = 2/5 nitido)", max(ratios) < 10 and min(ratios) > 0.05)

# ---------- §14: Čebyšëv, costanti, e un nucleo diverso da quello di S10 (k = t^{-1/2})
J = sp.Symbol('J', positive=True, integer=True)
good = all((sp.Integer(n)/sp.E**2)**n/sp.factorial(n) <= sp.exp(-n) for n in range(1, 60))
ok("§14 (J/e²)^J/J! ≤ e^{−J} (J < 60)", good)
# max del polinomio nodale di Čebyšëv su [0, Λ] = 2(Λ/4)^J
good = True
for Jn in [3, 6, 9]:
    Lam = mp.mpf(5)
    nodes = [Lam/2*(1 - mp.cos((2*i + 1)*mp.pi/(2*Jn))) for i in range(Jn)]
    mx = max(abs(mp.fprod([lam - nd for nd in nodes])) for lam in mp.linspace(0, Lam, 4001))
    good &= abs(mx - 2*(Lam/4)**Jn)/(2*(Lam/4)**Jn) < 1e-6
ok("§14 D33: max|ω_J| su [0,Λ] = 2(Λ/4)^J (J = 3, 6, 9)", good)
xv = sp.Symbol('xv', positive=True)
gfun = lambda v: (1 - mp.e**(-v)) - (1 - mp.e**-1)*min(v, 1)
ok("§14 (1 − e^{−λT})/λ ≥ (1 − e^{−1})min(T, 1/λ) (campionamento)", min(gfun(mp.mpf(v)/100) for v in range(1, 2000)) >= -1e-30)
# k = t^{-1/2}: μ = λ^{-1/2}/Γ(1/2) dλ, τ_k(Λ) = 2Λ^{-1/2}/Γ(1/2), T = 1
mp.mp.dps = 25
T = mp.mpf(1); beta = mp.mpf('0.5')
allok = True; out = []
for Jn in [4, 8, 12]:
    Lam = 4*Jn/(mp.e**2*T)
    nodes = [Lam/2*(1 - mp.cos((2*i + 1)*mp.pi/(2*Jn))) for i in range(Jn)]
    dens = lambda lam: lam**(beta - 1)/mp.gamma(beta)
    cs = []
    for i in range(Jn):
        li = lambda lam, i=i: mp.fprod([(lam - nodes[q])/(nodes[i] - nodes[q]) for q in range(Jn) if q != i])
        cs.append(mp.quad(lambda lam: li(lam)*dens(lam), [0] + sorted(nodes) + [Lam]))
    kJ = lambda tt: mp.fsum(c*mp.e**(-lam*tt) for lam, c in zip(nodes, cs))
    err = mp.quad(lambda tt: abs(tt**(-beta) - kJ(tt)), [0, mp.mpf('1e-8'), mp.mpf('1e-4'), mp.mpf('0.01'), mp.mpf('0.1'), 1])
    mk = 2*mp.sqrt(Lam)/mp.gamma(beta)              # μ([0,Λ])
    tau_k = Lam**(beta - 1)/((1 - beta)*mp.gamma(beta))
    bnd = 2*T*(Lam*T/4)**Jn/mp.factorial(Jn)*mk + tau_k
    out.append((Jn, float(err), float(bnd)))
    allok &= err <= bnd
print("    §14 k = t^{-1/2}: (J, errL1, stima (ii))", out)
ok("§14 stima (ii) verificata su k = t^{-1/2} (J = 4, 8, 12)", allok)
ok("§14 τ_k(Λ) per t^{-β}: ∫_Λ^∞ λ^{β−2}/Γ(β) = Λ^{β−1}/((1−β)Γ(β))",
   sp.simplify(sp.integrate(sp.Symbol('l', positive=True)**(sp.Rational(1, 2) - 2), (sp.Symbol('l', positive=True), sp.Symbol('L', positive=True), sp.oo)) - sp.Symbol('L', positive=True)**(-sp.Rational(1, 2))/(sp.Rational(1, 2))) == 0)

# ---------- §15: u = e^{−1/x²} per x > 0
xx = sp.Symbol('x', positive=True)
ue = sp.exp(-1/xx**2)
V = sp.simplify(sp.diff(ue, xx, 2)/ue)
ok("§15 V = u''/u = 4/x^6 − 6/x^4 su x > 0", sp.simplify(V - (4/xx**6 - 6/xx**4)) == 0)
ok("§15 V → +∞ per x → 0⁺ (nessuna V ∈ L^∞_loc, né continua)", sp.limit(V, xx, 0, '+') == sp.oo)
ok("§15 u piatta in 0: u^{(k)}(0⁺) = 0 per k ≤ 6 (quindi θ = 0 è soluzione formale)", all(sp.limit(sp.diff(ue, xx, k), xx, 0, '+') == 0 for k in range(7)))

# ---------- §16: atomi di media D_i f = ψ_i ∫_0^1 f, rango 1; ker D = ker ℓ
z = sp.Symbol('z', real=True)
psis = [1, z, z**2]
mean = lambda f: sp.integrate(f, (z, 0, 1))
Dop = lambda c, f: sum(ci*pi for ci, pi in zip(c, psis))*mean(f)
c = (2, -1, 3)
tests = [sp.sin(5*z), z**3, sp.exp(z), sp.cos(z)]
imgs = [sp.simplify(Dop(c, f)/ (2 - z + 3*z**2)) for f in tests]
ok("§16 Σc_iD_i ha rango 1 (immagine ⊂ span{Σc_iψ_i})", all(sp.simplify(im).is_constant() for im in imgs))
v = z - sp.Rational(1, 2)
ok("§16 v con ∫v = 0: D_iv = 0 per ogni i (fit), quindi nessun misfit con quel dato", all(sp.simplify(pi*mean(v)) == 0 for pi in psis))
w = sp.Integer(1)
ok("§16 con ∫w ≠ 0 i D_iw = ψ_i∫w sono indipendenti (misfit esiste fuori da Z)", sp.Matrix([[sp.integrate(pi*qj, (z, 0, 1)) for qj in psis] for pi in psis]).det() != 0 and mean(w) != 0)

print(f"\n[c_dict] {sum(c_ for _, c_ in RES)}/{len(RES)} OK")
