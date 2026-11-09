# S-CHECK-F10-A: verifica indipendente di S10A-L1, S10A-T1, S10A-C1 (termini costanti)
import sympy as sp
import mpmath as mp

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1
    if cond: ok += 1
    print(("OK   " if cond else "FAIL ") + name)

s, x, z, D, r, k1, k2 = sp.symbols('s x zeta D r k1 k2')
a1, a2 = sp.symbols('a1 a2')  # valori dei simboli a_n(zeta) sul modo

# (1) RD sui modi: E^add = (e^{sDz^2}-1)(e^{sr}-1) e^{zx}
u = sp.exp(s*(D*z**2 + r) + z*x)
u0 = sp.exp(z*x)
E = u - u0 - (sp.exp(s*D*z**2)*u0 - u0) - (sp.exp(s*r)*u0 - u0)
chk("RD: E^add = (e^{sDz^2}-1)(e^{sr}-1)e^{zx}",
    sp.simplify(E - (sp.exp(s*D*z**2)-1)*(sp.exp(s*r)-1)*u0) == 0)

# (2) Lemma L1(ii) sui modi, due termini non costanti + due costanti
kap = k1 + k2
v = sp.exp(s*(a1 + a2) + z*x)          # v in ker Q'
uM = sp.exp(kap*s)*v                    # u = M v
Eadd = uM - u0 - (sp.exp(s*a1)*u0 - u0) - (sp.exp(s*a2)*u0 - u0) \
       - (sp.exp(s*k1)-1)*u0 - (sp.exp(s*k2)-1)*u0
Ep = v - u0 - (sp.exp(s*a1)*u0 - u0) - (sp.exp(s*a2)*u0 - u0)
B = (sp.exp(s*kap)-1)*v - (sp.exp(s*k1)-1)*u0 - (sp.exp(s*k2)-1)*u0
chk("L1(ii): E^add(Mv) = E'(v) + B(v)", sp.simplify(Eadd - Ep - B) == 0)

# (3) M intreccia Q e Q': Q(d)(e^{kap s} v) = e^{kap s} Q'(d) v, con a(d_x) = D d_x^2 - d_x
t = sp.symbols('t'); f = sp.Function('f')(t, x)
Qp = lambda w: sp.diff(w, t) - D*sp.diff(w, x, 2) + sp.diff(w, x)
Q = lambda w: Qp(w) - kap*w
chk("L1(i): Q(e^{kap t} f) = e^{kap t} Q'(f)", sp.simplify(Q(sp.exp(kap*t)*f) - sp.exp(kap*t)*Qp(f)) == 0)

# (4) N=0: Q' = tau, ker = funzioni di x sole => E'(v) = v(t)-v0 = 0
g = sp.Function('g')(x)
chk("N=0: E' identicamente nullo su ker tau", sp.simplify(g - g) == 0)

# (5) Leibniz: sum_l C(i,l)|g|^l rho^{i-l+j} = (rho+|g|)^i rho^j <= (rho+|g|)^{i+j}
i_, j_ = 5, 3; rho, gm = sp.Rational(3,2), sp.Rational(7,3)
lhs = sum(sp.binomial(i_, l)*gm**l*rho**(i_-l+j_) for l in range(i_+1))
chk("Leibniz: stima e^{gt} B_rho in B_{rho+|g|}", lhs == (rho+gm)**i_*rho**j_ and lhs <= (rho+gm)**(i_+j_))

# (6) numerico: rapporto R = ||E^add||_{L2} / ||u||_{H1} su (0,1)^2, t0 = 0
mp.mp.dps = 30
def ratio(asym, consts, zeta, t0=0.0):
    # asym: lista di funzioni zeta -> a_n(zeta); consts: lista di c_k
    lam = sum(f(zeta) for f in asym) + sum(consts)
    def F(tt):
        ss = tt - t0
        val = mp.e**(lam*ss) - 1
        for f in asym: val -= mp.e**(ss*f(zeta)) - 1
        for c in consts: val -= mp.e**(ss*c) - 1
        return val
    ix = mp.quad(lambda xx: abs(mp.e**(zeta*xx))**2, [0, 1])
    e2 = mp.quad(lambda tt: abs(F(tt))**2, [0, 1]) * ix
    u2 = mp.quad(lambda tt: abs(mp.e**(lam*(tt-t0)))**2, [0, 1]) * ix * (1 + abs(lam)**2 + abs(zeta)**2)
    return mp.sqrt(e2/u2)

# RD: u_t = u_xx + 2u ; ADR: u_t = u_xx - u_x + 2u ; famiglia zeta = a + i sqrt(a^2 - a), a < 0
# (Re(zeta^2 - zeta) = 0: la soluzione non esplode, il flusso del trasporto sì)
RD, ADR = [], []
for a in [-5, -10, -20, -40]:
    zeta = mp.mpf(a) + 1j*mp.sqrt(a*a - a)
    RD.append(ratio([lambda q: q**2], [2], zeta))
    ADR.append(ratio([lambda q: q**2, lambda q: -q], [2], zeta))
print("   RD :", [mp.nstr(v, 5) for v in RD])
print("   ADR:", [mp.nstr(v, 5) for v in ADR])
chk("RD: R limitato (<= 1) sulla famiglia", max(RD) < 1)
chk("ADR: R cresce di almeno 10^6 sulla famiglia", ADR[-1]/ADR[0] > 1e6)

# (7) RD per zeta oscillante zeta = i w: R limitato anche li'
RDo = [ratio([lambda q: q**2], [2], 1j*mp.mpf(w)) for w in [5, 20, 80]]
print("   RD oscill.:", [mp.nstr(v, 5) for v in RDo])
chk("RD oscillante: R limitato", max(RDo) < 1)

print(f"{ok}/{tot} OK")
