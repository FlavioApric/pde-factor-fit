# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §5 (VAR-P12(d) nella classe quadratica).
import sys, random
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

w = sp.Symbol('omega1', positive=True)
tau = sp.Symbol('tau', positive=True)
# Heisenberg per H = p² + ω²x²: ẋ = i[H,x] = 2p, ṗ = i[H,p] = −2ω²x. Verifico i commutatori su una funzione test.
x = sp.Symbol('x', real=True); f = sp.Function('f')
p = lambda g: -sp.I*sp.diff(g, x)
Hop = lambda g, om: p(p(g)) + om**2*x**2*g
comm_x = sp.I*(Hop(x*f(x), w) - x*Hop(f(x), w))
comm_p = sp.I*(Hop(p(f(x)), w) - p(Hop(f(x), w)))
ok("Heisenberg: i[H,x] = 2p", sp.simplify(comm_x - 2*p(f(x))) == 0)
ok("Heisenberg: i[H,p] = −2ω²x", sp.simplify(comm_p + 2*w**2*x*f(x)) == 0)
# fattore di un tratto: risolvo il sistema lineare con matrice esponenziale
G = lambda om: sp.Matrix([[0, 2], [-2*om**2, 0]])
seg = lambda om, d: sp.simplify((G(om)*d).exp())
tau1 = sp.pi/(4*w); tau2 = sp.pi/(4*w)          # come nel PP (τ_2 = π/(4ω_1), θ_2 = 2·5ω_1·τ_2 = 5π/2)
M1 = seg(w, tau1); M2 = seg(5*w, tau2)
M = sp.simplify(M2*M1)
print("    M =", M.tolist())
ok("§5 M = M_2M_1 = diag(−1/5, −5)", M == sp.diag(-sp.Rational(1, 5), -5))
ok("§5 tr M = −26/5 < −2, det M = 1", M.trace() == -sp.Rational(26, 5) and M.det() == 1)
ok("§5 l'ordine non conta per la traccia", sp.simplify((M1*M2).trace() - M.trace()) == 0)
# exp(sl_2(R)) ⊂ {tr > −2} ∪ {−I}: campionamento casuale + le tre famiglie in forma chiusa
a, b, c = sp.symbols('a b c', real=True)
Xi = sp.Matrix([[a, b], [c, -a]])
d2 = a**2 + b*c
# tr e^Ξ = 2cosh(√d2) se d2>0, 2 se d2=0, 2cos(√(−d2)) se d2<0
random.seed(1)
good = True
for _ in range(300):
    av, bv, cv = [random.uniform(-4, 4) for _ in range(3)]
    E = mp.expm(mp.matrix([[av, bv], [cv, -av]]))
    trv = E[0, 0] + E[1, 1]
    good &= (trv > -2 + 1e-12) or (mp.norm(E + mp.eye(2)) < 1e-8)
ok("§5 300 Ξ casuali in sl_2: tr e^Ξ > −2 (o e^Ξ = −I)", good)
# tr e^Ξ = −2 solo per ellittico con √(−d2) = π (mod 2π) e allora e^Ξ = −I (Cayley–Hamilton: e^Ξ = cos·I + sin·Ξ/√)
th = sp.Symbol('theta', positive=True)
ok("§5 Ξ ellittico: e^Ξ = cos θ I + (sin θ/θ)Ξ, quindi tr = −2 ⇒ θ = π ⇒ e^Ξ = −I",
   sp.simplify((sp.cos(sp.pi)*sp.eye(2) + sp.sin(sp.pi)/sp.pi*Xi) + sp.eye(2)) == sp.zeros(2))
# M² ha autovalori positivi distinti: log reale iperbolico
M2T = M*M
L = sp.diag(sp.log(sp.Rational(1, 25)), sp.log(25))
ok("§5 al periodo 2T: M² = e^Ξ con Ξ = diag(−log 25, log 25) ∈ sl_2", (L.exp() - M2T).applyfunc(sp.simplify) == sp.zeros(2) and L.trace() == 0)
# regolarizzazione: ω liscio vicino al gradino in L¹ ⇒ tr resta < −2 (numerico, mpmath odefun)
mp.mp.dps = 20
w1 = mp.mpf(1); T1 = mp.pi/(4*w1); T = 2*T1
for epsr in [mp.mpf('0.05'), mp.mpf('0.02')]:
    om = lambda tt, e=epsr: w1 + 4*w1*(1 + mp.tanh((tt - T1)/e))/2
    def mono():
        cols = []
        for y0 in ([1, 0], [0, 1]):
            sol = mp.odefun(lambda tt, Y: [2*Y[1], -2*om(tt)**2*Y[0]], 0, y0)
            cols.append(sol(T))
        return cols[0][0] + cols[1][1]
    trv = mono()
    print("    ε =", float(epsr), " tr M_ε =", mp.nstr(trv, 8))
    ok("§5 regolarizzazione tanh, ε = %s: tr < −2" % mp.nstr(epsr, 2), trv < -2)

print(f"\n[c_p12] {sum(c for _, c in RES)}/{len(RES)} OK")
