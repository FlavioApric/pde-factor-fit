# S10-OPEN-A, P1-Q6: termini costanti. Controlli simbolici e numerici (solo verifica).
import sympy as sp
import mpmath as mp

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name)

s, z, D, r, c, k1, k2 = sp.symbols('s zeta D r c k1 k2')
# (1) reazione-diffusione u_t = D u_xx + r u: G_zeta(s) si fattorizza
a = D*z**2 + r
G = sp.exp(s*a) - sp.exp(s*D*z**2) - sp.exp(s*r) + 1
chk("RD: G = (e^{sDz^2}-1)(e^{sr}-1)", sp.simplify(sp.expand(G - (sp.exp(s*D*z**2)-1)*(sp.exp(s*r)-1))) == 0)

# (2) identita di riduzione sui dati esponenziali: termini non costanti a1 = D z^2, a2 = c z; costanti k1, k2
a1, a2 = D*z**2, c*z
ap = a1 + a2; kap = k1 + k2
u_t = sp.exp((ap+kap)*s)          # u(t)/u0 sul modo e^{zeta x}, s = t - t0
v_t = sp.exp(ap*s)                # v = e^{-s kappa} u
Eadd = u_t - 1 - (sp.exp(s*a1)-1) - (sp.exp(s*a2)-1) - (sp.exp(s*k1)-1) - (sp.exp(s*k2)-1)
Eprm = v_t - 1 - (sp.exp(s*a1)-1) - (sp.exp(s*a2)-1)
rhs = Eprm + (sp.exp(s*kap)-1)*v_t - (sp.exp(s*k1)-1) - (sp.exp(s*k2)-1)
chk("riduzione: E^add(u) = E'(v) + (e^{s kappa}-1)v(t) - sum_j (e^{s k_j}-1)v0", sp.simplify(Eadd - rhs) == 0)

# (3) un solo termine non costante: E' = 0 sui modi (P1-T2(i))
Eprm1 = sp.exp(a1*s) - 1 - (sp.exp(s*a1)-1)
chk("un solo termine non costante: E' = 0", sp.simplify(Eprm1) == 0)

# (4) numerico: R = ||E^add||_{L2}/||u||_{H1} su Omega = (0,1)x(0,1), dati e^{a t + zeta x}, zeta reale
mp.mp.dps = 30
def ratio(terms, consts, zeta, t0v):
    A = sum(f(zeta) for f in terms) + sum(consts)
    def Eabs2(t):
        sv = t - t0v
        g = mp.e**(A*sv) - 1 - sum(mp.e**(f(zeta)*sv)-1 for f in terms) - sum(mp.e**(k*sv)-1 for k in consts)
        return abs(mp.e**(A*t0v)*g)**2
    num = mp.quad(Eabs2, [0, 1])
    den = (1 + abs(A)**2 + abs(zeta)**2) * mp.quad(lambda t: mp.e**(2*mp.re(A)*t), [0, 1])
    return mp.sqrt(num/den)
heat = lambda zz: zz**2
adv = lambda zz: -zz
vals_RD = [ratio([heat], [2.0], zz, 0.0) for zz in (5, 10, 20, 40)]
vals_AD = [ratio([heat, adv], [2.0], zz, 0.0) for zz in (5, 10, 20, 40)]
print("   RD  (u_t = u_xx + 2u)        R:", [mp.nstr(v, 6) for v in vals_RD])
print("   ADR (u_t = u_xx - u_x + 2u)  R:", [mp.nstr(v, 6) for v in vals_AD])
chk("RD, t0 = 0: R limitato", max(vals_RD) < 10)
chk("ADR, t0 = 0: R cresce esponenzialmente", vals_AD[-1] > 1e6*vals_AD[0])
# t0 = 1/2: raggio reale; t0 = 1: serve Re a -> -inf con q^bot != a: zeta = rho e^{5 i pi/8} (Re zeta^2 < 0, Re zeta < 0)
for t0v, ph in ((0.5, mp.mpf(1)), (1.0, mp.e**(mp.mpc(0, 5)*mp.pi/8))):
    zs = (10, 40)
    vR = [ratio([heat], [2.0], ph*zz, t0v) for zz in zs]
    vA = [ratio([heat, adv], [2.0], ph*zz, t0v) for zz in zs]
    print(f"   t0={t0v}: RD", [mp.nstr(v, 5) for v in vR], " ADR", [mp.nstr(v, 5) for v in vA])
    chk(f"t0 = {t0v}: RD limitato, ADR illimitato", max(vR) < 10 and vA[1] > 1e3*vA[0])
print(f"{ok}/{tot} OK")
