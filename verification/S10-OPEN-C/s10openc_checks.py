# S10-OPEN-C: verifiche SymPy/mpmath. Sono solo verifiche: nessuna prova del pacchetto si appoggia su questo calcolo.
import sympy as sp
import mpmath as mp
import sys
sys.stdout.reconfigure(encoding="utf-8")

res = []
def ok(name, cond):
    res.append((name, bool(cond)))
    print(("OK  " if cond else "FAIL"), name)

t, x, xi, m, tau, s, y = sp.symbols('t x xi m tau s y', real=True)
I = sp.I

# T1 Tychonoff: la serie troncata a K termini ha residuo pari al solo termine di testa
g = sp.Function('g')
K = 6
u = sum((-I)**k*sp.diff(g(t), t, k)*x**(2*k)/sp.factorial(2*k) for k in range(K+1))
r = sp.expand(I*sp.diff(u, t) + sp.diff(u, x, 2))
lead = sp.expand(I*(-I)**K*sp.diff(g(t), t, K+1)*x**(2*K)/sp.factorial(2*K))
ok("T1 Tychonoff: residuo = termine di testa", sp.simplify(r - lead) == 0)

# T2 sup_l l^{-k} exp(-l^{-4}) = (k/(4e))^{k/4}  (stima Gevrey 7/4 di VAR-Q10)
k_ = 7
lpos = sp.Symbol('l', positive=True)
h = -k_*sp.log(lpos) - lpos**(-4)
crit = sp.solve(sp.diff(h, lpos), lpos)
val = sp.exp(h.subs(lpos, crit[0]))
ok("T2 sup l^-k e^{-l^-4} = (k/4e)^{k/4}", sp.simplify(val - (sp.Rational(k_, 4)/sp.E)**sp.Rational(k_, 4)) == 0)

# T3 Dirac: e^{tA} = e^{iaσz} e^{ibσx} e^{iaσz} (numerico); A = X + mY, X = iξσz, Y = −iσx
mp.mp.dps = 30
good = True
for (XI, MM, TT) in [(0.7, 1.3, 0.4), (2.1, 0.5, 0.3), (-1.4, 0.8, 0.5), (0.3, 2.0, 0.2)]:
    A = mp.matrix([[1j*XI, -1j*MM], [-1j*MM, -1j*XI]])
    w = mp.sqrt(XI**2 + MM**2)
    b = -mp.asin(MM*mp.sin(w*TT)/w)
    a = mp.arg(mp.cos(w*TT) + 1j*XI*mp.sin(w*TT)/w)/2
    L = mp.expm(A*TT)
    Ra = mp.expm(mp.matrix([[1j*a, 0], [0, -1j*a]]))
    Rb = mp.expm(mp.matrix([[0, 1j*b], [1j*b, 0]]))
    d = mp.mnorm(L - Ra*Rb*Ra, 1)
    print("    Dirac residuo", mp.nstr(d, 3))
    good &= d < 1e-12
ok("T3 Euler ZXZ di Dirac (4 punti con ωt < π/2)", good)

# T4 g1 = a/ξ e g2 = −b/m hanno coefficienti polinomiali in (ξ, m) come serie in t
sz = sp.Matrix([[1, 0], [0, -1]]); sx = sp.Matrix([[0, 1], [1, 0]])
w2 = xi**2 + m**2
N = 6
ser_sin = sum((-1)**j*w2**j*t**(2*j+1)/sp.factorial(2*j+1) for j in range(N))   # sin(ωt)/ω
ser_tan = sp.series(sp.tan(s), s, 0, 2*N).removeO()
ser_tanw = sp.expand(sum(ser_tan.coeff(s, 2*j+1)*w2**j*t**(2*j+1) for j in range(N)))  # tan(ωt)/ω
def trunc_t(e, o):
    e = sp.expand(e); return sum(e.coeff(t, j)*t**j for j in range(o+1))
def compose(outer, inner, o=9):
    # outer(y) polinomio in y, inner = O(t): composizione troncata a t^o
    out = 0; pw = sp.Integer(1)
    for j in range(o+1):
        cj = outer.coeff(y, j)
        if cj != 0: out += cj*pw
        pw = trunc_t(pw*inner, o)
    return trunc_t(out, o)
a_ser = compose(sp.series(sp.atan(y), y, 0, 10).removeO(), trunc_t(xi*ser_tanw, 9))/2
b_ser = -compose(sp.series(sp.asin(y), y, 0, 10).removeO(), trunc_t(m*ser_sin, 9))
g1 = trunc_t(a_ser/xi, 9); g2 = trunc_t(-b_ser/m, 9)
coeffs = [sp.expand(g1.coeff(t, j)) for j in range(10)] + [sp.expand(g2.coeff(t, j)) for j in range(10)]
ok("T4a g1, g2 ∈ ℚ[ξ,m][[t]] fino a t^9", all(c.is_polynomial(xi, m) for c in coeffs))
X = I*xi*sz; Y = -I*sx
def mexp(M, order=7):
    out = sp.eye(2); P = sp.eye(2)
    for j in range(1, order+1):
        P = trunc((P*M)/j, 8); out += P
    return out
def trunc(M, o=6): return M.applyfunc(lambda e: trunc_t(e, o))
lhs = trunc(mexp(t*(X + m*Y)))
rhs = trunc(trunc(mexp(g1*X))*trunc(mexp(g2*m*Y))*trunc(mexp(g1*X)))
ok("T4b identità formale e^{t(X+mY)} = e^{g1X}e^{g2mY}e^{g1X} fino a t^6", (lhs - rhs).applyfunc(sp.expand) == sp.zeros(2))

# T5 Maxwell: P 8×6, rango 6, due sizigie a supporti disgiunti
x1, x2, x3 = sp.symbols('xi1 xi2 xi3')
xv = sp.Matrix([x1, x2, x3])
Cx = sp.Matrix([[0, -x3, x2], [x3, 0, -x1], [-x2, x1, 0]])   # Cx·v = ξ×v
P = sp.zeros(8, 6)
P[0:3, 0:3] = tau*sp.eye(3); P[0:3, 3:6] = -Cx      # τE − ξ×B
P[3:6, 0:3] = Cx;            P[3:6, 3:6] = tau*sp.eye(3)  # τB + ξ×E
P[6, 0:3] = xv.T; P[7, 3:6] = xv.T                  # ξ·E, ξ·B
S1 = sp.Matrix([[x1, x2, x3, 0, 0, 0, -tau, 0]]); S2 = sp.Matrix([[0, 0, 0, x1, x2, x3, 0, -tau]])
ok("T5a Maxwell: S1·P = S2·P = 0", (S1*P).applyfunc(sp.expand) == sp.zeros(1, 6) and (S2*P).applyfunc(sp.expand) == sp.zeros(1, 6))
d6 = sp.factor(P[0:6, :].det())
print("    det righe 0..5 =", d6)
ok("T5b Maxwell: minore 6×6 ≠ 0, quindi rango 6 e nucleo sinistro di dim 2", d6 != 0)

# T6 II-T2(b′): proiettore spettrale su ker(A − ξ) lungo ker B(A), B = (τ+ξ)(τ+2ξ)
def proj_Q(A):
    n = A.shape[0]
    Bm = (A + xi*sp.eye(n))*(A + 2*xi*sp.eye(n))
    return (Bm/(6*xi**2)).applyfunc(sp.cancel)
A1 = sp.Matrix([[xi, 0, 0], [0, -xi, 1], [0, 0, -2*xi]])
A2 = sp.Matrix([[xi, 1, 0], [0, -xi, 0], [0, 0, -2*xi]])
P1, P2 = proj_Q(A1), proj_Q(A2)
print("    P(A1) =", P1.tolist(), "  P(A2) =", P2.tolist())
ok("T6a A1: proiettore senza polo", all(not sp.denom(e).has(xi) for e in P1))
ok("T6b A2: proiettore con polo in ξ = 0", any(sp.denom(e).has(xi) for e in P2))
ok("T6c P idempotente e commuta con A (entrambi)", all(((Pk*Pk - Pk).applyfunc(sp.cancel) == sp.zeros(3)) and ((Pk*Ak - Ak*Pk).applyfunc(sp.cancel) == sp.zeros(3)) for Pk, Ak in [(P1, A1), (P2, A2)]))
J1 = A1.subs(xi, 0).jordan_form()[1]; J2 = A2.subs(xi, 0).jordan_form()[1]
ok("T6d stessa forma di Jordan in ξ = 0", J1 == J2)
ok("T6e stesso polinomio caratteristico", sp.expand(A1.charpoly(tau).as_expr() - A2.charpoly(tau).as_expr()) == 0)

# T7 VAR-Q18: C'' = −‖x‖²C, C(0) = 0, C'(0) = 1
nx = sp.Symbol('n', positive=True); Cf = sp.Function('C')
sol = sp.dsolve(sp.diff(Cf(t), t, 2) + nx**2*Cf(t), Cf(t), ics={Cf(0): 0, sp.diff(Cf(t), t).subs(t, 0): 1})
ok("T7 VAR-Q18: C(t) = sin(‖x‖t)/‖x‖", sp.simplify(sol.rhs - sp.sin(nx*t)/nx) == 0)

# T8 VAR-P12(d): monodromia dell'oscillatore con ω costante a tratti
w1 = sp.Symbol('w1', positive=True)
def seg(w, th): return sp.Matrix([[sp.cos(th), sp.sin(th)/w], [-w*sp.sin(th), sp.cos(th)]])
Mon = seg(5*w1, 5*sp.pi/2)*seg(w1, sp.pi/2)
ok("T8a tr M = −26/5", sp.simplify(Mon.trace() + sp.Rational(26, 5)) == 0)
ok("T8b det M = 1", sp.simplify(Mon.det() - 1) == 0)
tt = sp.Symbol('tt')
Mseg = seg(w1, 2*w1*tt)
ok("T8c il segmento risolve x' = 2p, p' = −2ω²x", (sp.diff(Mseg, tt) - sp.Matrix([[0, 2], [-2*w1**2, 0]])*Mseg).applyfunc(sp.simplify) == sp.zeros(2))

# T9 ENC-Q10 Darboux: u = x² + 2it libera, L = ∂x − ux/u, V1 = −2∂x² log u
uu = x**2 + 2*I*t
L0 = lambda f: I*sp.diff(f, t) + sp.diff(f, x, 2)
ok("T9a u libera", sp.simplify(L0(uu)) == 0)
V1 = -2*sp.diff(sp.log(uu), x, 2)
Lop = lambda f: sp.diff(f, x) - sp.diff(uu, x)/uu*f
frees = [x, sp.Integer(1), x**3 + 6*I*t*x, sp.exp(2*I*x - 4*I*t)]
ok("T9b le φ di prova sono libere", all(sp.simplify(L0(p)) == 0 for p in frees))
plus = all(sp.simplify(L0(Lop(p)) + V1*Lop(p)) == 0 for p in frees)
minus = all(sp.simplify(L0(Lop(p)) - V1*Lop(p)) == 0 for p in frees)
print("    segno: iχt + χxx + V1χ = 0:", plus, "   iχt + χxx − V1χ = 0:", minus)
ok("T9c intertwining L: soluzioni libere → soluzioni del modello V1 (un segno)", plus or minus)
sgn = 1 if plus else -1
LV = lambda f: L0(f) + sgn*V1*f
ok("T9d 1/u non risolve il modello V1", sp.simplify(LV(1/uu)) != 0)
print("    residuo di 1/u:", sp.factor(sp.simplify(LV(1/uu))))
ok("T9e u_x/u... nucleo: L u = 0", sp.simplify(Lop(uu)) == 0)
# encoder inverso: ψ = u[∫_{x0}^x χ/u + c(t)], c' = iκ, κ = (χx + (ux/u)χ)(t,x0)/u(t,x0)
phi = x**3 + 6*I*t*x; chi = sp.simplify(Lop(phi)); x0 = 1
xs = sp.Symbol('xs', real=True)
Iint = sp.integrate(sp.cancel(chi/uu).subs(x, xs), (xs, x0, x))
kap = sp.simplify(((sp.diff(chi, x) + sp.diff(uu, x)/uu*chi)/uu).subs(x, x0))
cfun = sp.integrate((I*kap).subs(t, s), (s, 0, t)) + (phi/uu).subs({x: x0, t: 0})
psi = sp.simplify(uu*(Iint + cfun))
print("    ψ − φ =", sp.simplify(psi - phi))
ok("T9f encoder inverso: Lψ = χ", sp.simplify(Lop(psi) - chi) == 0)
ok("T9g encoder inverso: ψ libera (formula di κ)", sp.simplify(L0(psi)) == 0)

# T10 VAR-C3Q2 / Q12: u = f(x+t) è annullata da ∂t − ∂x
F = sp.Function('F')
ok("T10 (∂t − ∂x) f(x+t) = 0", sp.simplify(sp.diff(F(x+t), t) - sp.diff(F(x+t), x)) == 0)

# T11 DICT-Q3: u = exp(−1/x²) per x > 0, 0 altrove
ue = sp.exp(-1/x**2)
q = sp.simplify(sp.diff(ue, x, 2)/ue)
ok("T11a u''/u = 4/x^6 − 6/x^4", sp.simplify(q - (4/x**6 - 6/x**4)) == 0)
ok("T11b u''/u → +∞ per x → 0+", sp.limit(q, x, 0, '+') == sp.oo)
ok("T11c u^(k) → 0 per x → 0+ (k ≤ 4)", all(sp.limit(sp.diff(ue, x, k), x, 0, '+') == 0 for k in range(5)))

# T12 DICT-Q4: atomi di media D_i f = ψ_i ∫_0^1 f
psis = [sp.Integer(1), x, x**2]
mean = lambda f: sp.integrate(f, (x, 0, 1))
uq = sp.sin(2*sp.pi*x)
ok("T12a ∫u = 0 ⇒ D_i u = 0 per ogni i (fit)", mean(uq) == 0)
vq = x - sp.Rational(1, 2) + sp.cos(2*sp.pi*x)
ok("T12b un v con lo stesso dato ℓ(v) = 0 sta nel fit", mean(vq) == 0)
Gr = sp.Matrix(3, 3, lambda i, j: sp.integrate(psis[i]*psis[j], (x, 0, 1)))
ok("T12c atomi indipendenti come operatori (Gram dei ψ_i invertibile)", Gr.det() != 0)

# T13 DICT-U3d-v: k = 1/(1+t), μ = e^{−λ}dλ; interpolazione di Čebyšëv in λ su [0, Λ]
mp.mp.dps = 25
Tm = mp.mpf(1)
allok = True
for J in [4, 8, 12, 16]:
    Lam = 4*J/(mp.e**2*Tm)
    nodes = [Lam/2*(1 - mp.cos((2*j+1)*mp.pi/(2*J))) for j in range(J)]
    cs = []
    for j in range(J):
        lj = lambda l, j=j: mp.fprod([(l - nodes[i])/(nodes[j] - nodes[i]) for i in range(J) if i != j])
        cs.append(mp.quad(lambda l: lj(l)*mp.e**(-l), mp.linspace(0, Lam, 8)))
    kJ = lambda tt: mp.fsum(c*mp.e**(-l*tt) for l, c in zip(nodes, cs))
    err = mp.quad(lambda tt: abs(1/(1+tt) - kJ(tt)), mp.linspace(0, 1, 9))
    bound = 2*Tm*(Lam*Tm/4)**J/mp.factorial(J)*(1 - mp.e**(-Lam)) + mp.e1(Lam)
    print(f"    J={J:2d} Λ={float(Lam):6.3f} errL1={float(err):.3e} stima={float(bound):.3e}")
    allok &= err <= bound
ok("T13 errore L¹(0,1) ≤ 2T(ΛT/4)^J/J!·μ([0,Λ]) + τ_k(Λ)", allok)

# T14 DM-δ: scala del bump h = ε φ(x/ε^{1/3})
eps = sp.Symbol('epsilon', positive=True); phi_ = sp.exp(-y**2)
hb = eps*phi_.subs(y, x/eps**sp.Rational(1, 3))
ok("T14a h''' = φ'''(x/ε^{1/3}) = O(1)", sp.simplify(sp.diff(hb, x, 3).subs(x, eps**sp.Rational(1, 3)*y) - sp.diff(phi_, y, 3)) == 0)
ok("T14b h''(0) = ε^{1/3} φ''(0)", sp.simplify(sp.diff(hb, x, 2).subs(x, 0) - eps**sp.Rational(1, 3)*sp.diff(phi_, y, 2).subs(y, 0)) == 0)
ok("T14c sup|h| = ε", sp.simplify(hb.subs(x, 0) - eps) == 0)

print(f"\n{sum(c for _, c in res)}/{len(res)} OK")
