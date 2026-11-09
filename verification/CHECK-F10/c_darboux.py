# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §12 (ENC-Q10-D), con derivazione generale della formula di κ.
import sys
import sympy as sp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

t, x = sp.symbols('t x', real=True)
u = sp.Function('u')(t, x); ph = sp.Function('phi')(t, x)
L0 = lambda f: sp.I*sp.diff(f, t) + sp.diff(f, x, 2)
def free(expr):
    # impone u, φ libere: u_t = i u_xx, φ_t = i φ_xx (anche sulle derivate in x di u_t, φ_t)
    rep = {}
    for F in (u, ph):
        for k in range(0, 5):
            rep[sp.Derivative(F, t, 1, x, k) if k else sp.Derivative(F, t)] = sp.I*sp.diff(F, x, k + 2)
            rep[sp.Derivative(F, x, k, t, 1) if k else sp.Derivative(F, t)] = sp.I*sp.diff(F, x, k + 2)
    return sp.simplify(sp.expand(expr.doit().subs(rep)))
Lam = lambda f: sp.diff(f, x) - sp.diff(u, x)/u*f
V1 = -2*sp.diff(sp.log(u), x, 2)
chi = Lam(ph)
# (i) segno, in generale (u, φ libere qualsiasi): L_0(Λφ) = V_1 Λφ
ok("§12(i) in generale: L_0(Λφ) − V_1Λφ = 0 per u, φ libere", free(L0(chi) - V1*chi) == 0)
ok("§12(i) il segno opposto è falso in generale", free(L0(chi) + V1*chi) != 0)
ok("§12(i) Λu = 0", sp.simplify(Lam(u)) == 0)
# (ii) formula di κ, derivazione generale: d/dt (φ/u) = i(χ_x + (u_x/u)χ)/u in ogni punto (quindi in x_0)
lhs = sp.diff(ph/u, t)
rhs = sp.I*(sp.diff(chi, x) + sp.diff(u, x)/u*chi)/u
ok("§12(ii) d/dt(φ/u) = i(χ_x + (u_x/u)χ)/u  (D29 a mano: Wronskiano W = uχ)", free(lhs - rhs) == 0)
# e ψ − φ = a(t)u con a' = 0 ⟺ ψ libera: L_0(a u) = i a' u
a = sp.Function('a')(t)
ok("§12(ii) L_0(a(t)u) = i a'(t) u per u libera", free(L0(a*u) - sp.I*sp.diff(a, t)*u) == 0)
# osservazione: residuo di 1/u nel modello V_1 è 2u_xx/u²
ok("§12 oss.: L_0(1/u) − V_1/u = 2u_xx/u²", free(L0(1/u) - V1/u - 2*sp.diff(u, x, 2)/u**2) == 0)
# (c) residuo: esempio REALE, regolare sul dominio e dipendente da t, via boost di Galileo di a + bx
kk, a0 = sp.symbols('k a0', positive=True)
ug = (x - 2*kk*t + a0)*sp.exp(sp.I*(kk*x - kk**2*t))
ok("§12(c) u_G = (x − 2kt + a)e^{i(kx − k²t)} è libera", sp.simplify(L0(ug)) == 0)
V1g = sp.simplify(-2*sp.diff(sp.log(ug), x, 2))
print("    V_1 per u_G:", V1g)
ok("§12(c) V_1 = 2/(x − 2kt + a)²: reale, dipende da t, regolare dove x > 2kt − a", sp.simplify(V1g - 2/(x - 2*kk*t + a0)**2) == 0)
phig = sp.exp(sp.I*(2*x - 4*t))   # libera
chig = sp.simplify(sp.diff(phig, x) - sp.diff(ug, x)/ug*phig)
ok("§12(c) Λ_G manda una soluzione libera in una soluzione del modello reale V_1", sp.simplify(L0(chig) - V1g*chig) == 0)

print(f"\n[c_darboux] {sum(c for _, c in RES)}/{len(RES)} OK")
