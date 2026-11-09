"""T8 — operatori composti (C2.12, C2.19, C2.23): banco di prova di E_int."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from _common import check, check_true, summary, quotient_dim

x, y = sp.symbols('x y', real=True)
t, D, c, a, kp = sp.symbols('t D c a kappa', positive=True)
xi, tau = sp.symbols('xi tau')
k = sp.symbols('k', real=True, nonzero=True)
u0 = sp.Function('u0')

# ---------- C2.12 avvezione-diffusione: termini commutanti -> split moltiplicativo esatto
AD = lambda u: sp.diff(u, t) + c*sp.diff(u, x) - D*sp.diff(u, x, 2)
G = sp.exp(-x**2/(4*D*t))/sp.sqrt(4*sp.pi*D*t)
check("C2.12 nucleo: G(x - ct, t) = S_tr(t) S_heat(t) delta", AD(G.subs(x, x - c*t)))
# sul modo e^{ikx}: S1 = e^{-ickt}, S2 = e^{-Dk^2 t}; e^{t(A1+A2)} = S1 S2
S1, S2 = sp.exp(-sp.I*c*k*t), sp.exp(-D*k**2*t)
exact = sp.exp(t*(-sp.I*c*k - D*k**2))
check("C2.12 e^{t(A1+A2)} = S1 S2 (commutano)", exact - S1*S2)
# decomposizione additiva: u = u0 + (S1-1)u0 + (S2-1)u0 + E_int, E_int = (S1-1)(S2-1)u0
Eint = (S1 - 1)*(S2 - 1)
check("G3 E_int = (S1-I)(S2-I)u0 (bilineare)", exact - (1 + (S1 - 1) + (S2 - 1) + Eint))
check_true("G3 E_int != 0 per k != 0, t > 0", sp.simplify(Eint) != 0)
# N=3 termini: 2^N - N - 1 = 4 termini d'interazione (inclusione-esclusione)
S3 = sp.exp(-sp.Symbol('r', positive=True)*t)
expansion = sum(sp.Mul(*[(S - 1) for S in sub]) for L_ in range(4)
                for sub in __import__('itertools').combinations([S1, S2, S3], L_))
check("G3 prodotto di 3 semigruppi = somma su 2^3 sottoinsiemi", sp.expand(S1*S2*S3 - expansion))
# dominio log-simbolo: d_t log u_hat = -i c k - D k^2 (lineare nei coefficienti)
lam1, lam2 = sp.symbols('lambda1 lambda2')
uhat = sp.exp(t*(-sp.I*c*k - D*k**2))*sp.Symbol('A')
check("G3 d_t log u_hat = somma dei simboli", sp.diff(sp.log(uhat), t) - (-sp.I*c*k - D*k**2))
# identificazione: due frequenze distinte k1,k2 -> sistema lineare 2x2 in (c, D) invertibile
k1, k2 = sp.symbols('k1 k2', nonzero=True, real=True)
M = sp.Matrix([[-sp.I*k1, -k1**2], [-sp.I*k2, -k2**2]])
check("G4 det = i k1 k2 (k2 - k1)  != 0 sse k1 != k2 (k_i != 0)", sp.factor(M.det()) - sp.I*k1*k2*(k2 - k1))

# telegrafo / onda smorzata u_tt + 2a u_t = c^2 u_xx
Tg = lambda u: sp.diff(u, t, 2) + 2*a*sp.diff(u, t) - c**2*sp.diff(u, x, 2)
rho = sp.sqrt(c**2*t**2 - x**2)
check("C2.12 telegrafo: e^{-at} I0((a/c) sqrt(c^2t^2-x^2))", Tg(sp.exp(-a*t)*sp.besseli(0, a/c*rho)))
w = sp.Function('w')
check("C2.12 u = e^{-at} w  =>  Tg(u) = e^{-at}(w_tt - c^2 w_xx - a^2 w) (KG a massa immaginaria)",
      Tg(sp.exp(-a*t)*w(t, x)) - sp.exp(-a*t)*(sp.diff(w(t, x), t, 2) - c**2*sp.diff(w(t, x), x, 2) - a**2*w(t, x)))
# forma a sistema (via b): A = A_w + A_d sul modo k, non commutano
Aw = sp.Matrix([[0, 1], [-c**2*k**2, 0]])
Ad = sp.Matrix([[0, 0], [0, -2*a]])
comm = Aw*Ad - Ad*Aw
check_true("II(b) [A_w, A_d] != 0 anche a coeff. costanti (riduzione compagna)", comm != sp.zeros(2, 2), str(comm))
# controllo numerico (non metodo): e^{t(Aw+Ad)} != e^{tAw}e^{tAd}
import mpmath as mp
vals = {c: 1, k: 1, a: sp.Rational(1, 2), t: 1}
E1 = mp.expm(mp.matrix((Aw + Ad).subs(vals).tolist()))
E2 = mp.expm(mp.matrix(Aw.subs(vals).tolist()))*mp.expm(mp.matrix(Ad.subs(vals).tolist()))
check_true("II(b) e^{A_w+A_d} != e^{A_w}e^{A_d} (controllo numerico)", mp.mnorm(E1 - E2) > 1e-3, f"||diff||={float(mp.mnorm(E1-E2)):.3f}")
# Cattaneo: memoria esponenziale -> telegrafo (link T9)
th = sp.symbols('theta', positive=True)
check("C2.12/C2.37 tau = khat(tau) xi^2 con khat = 1/(1+theta tau) <=> theta tau^2 + tau - xi^2 = 0",
      sp.simplify((tau - xi**2/(1 + th*tau))*(1 + th*tau) - (th*tau**2 + tau - xi**2)))

# ---------- C2.19 ordine superiore / fattorizzazione
# trave: tau^2 + xi^4 = (tau - i xi^2)(tau + i xi^2), intersezione (tau, xi^2) dim 2 -> {1, x}
check("C2.19 tau^2+xi^4 = (tau - i xi^2)(tau + i xi^2)", sp.expand((tau - sp.I*xi**2)*(tau + sp.I*xi**2)) - (tau**2 + xi**4))
check_true("C2.19 dim C[tau,xi]/(tau - i xi^2, tau + i xi^2) = 2", quotient_dim([tau - sp.I*xi**2, tau + sp.I*xi**2], [tau, xi]) == 2)
Beam = lambda u: sp.diff(u, t, 2) + sp.diff(u, x, 4)
SchP = lambda u: sp.diff(u, t) - sp.I*sp.diff(u, x, 2)
SchM = lambda u: sp.diff(u, t) + sp.I*sp.diff(u, x, 2)
for f_, nm in ((sp.Integer(1), "1"), (x, "x")):
    check_true(f"C2.19 {nm} in ker(S+) ∩ ker(S-)", SchP(f_) == 0 and SchM(f_) == 0)
check("C2.19 beam = S+ S-", sp.expand(SchP(SchM(sp.Function('f')(t, x))) - Beam(sp.Function('f')(t, x))))
up = sp.exp(sp.I*kp*x - sp.I*kp**2*t)  # in ker S+ ? S+: tau = i xi^2 -> xi = i kp: tau = -i kp^2
check("C2.19 modo e^{i k x - i k^2 t} in ker S+ e quindi in ker beam", SchP(up))
check("C2.19 ... e in ker beam", Beam(up))
# u_t + u_xxxx (iperdiffusione): modi e^{ikx - k^4 t}
check("C2.19 iperdiffusione e^{ikx - k^4 t}", sp.diff(sp.exp(sp.I*k*x - k**4*t), t) + sp.diff(sp.exp(sp.I*k*x - k**4*t), x, 4))
# biarmonica: r^2 log r ; Almansi u = h1 + (x^2+y^2) h2
Lap = lambda u: sp.diff(u, x, 2) + sp.diff(u, y, 2)
r2 = x**2 + y**2
check("C2.19 Delta^2 (r^2 log r) = 0 (r>0)", Lap(Lap(r2*sp.log(sp.sqrt(r2)))))
F, Gf, F2, G2 = [sp.Function(n_) for n_ in ('F', 'Gf', 'F2', 'G2')]
h1 = F(x + sp.I*y) + Gf(x - sp.I*y)
h2 = F2(x + sp.I*y) + G2(x - sp.I*y)
check("C2.19 Almansi: h1 + r^2 h2 biarmonica", Lap(Lap(h1 + r2*h2)))
check_true("C2.19 (tau^2+xi^2)^2 non ridotto: ker(Delta) ∩ ker(Delta) = ker Delta (infinito) -> serve Noether op. (r^2)",
           quotient_dim([(tau**2 + xi**2), (tau**2 + xi**2)**2], [tau, xi]) is None)

# ---------- tabella intersezioni dim C[tau,xi]/(P1,P2) per coppie del catalogo (PR-C2.4, G1)
r_ = sp.symbols('r', positive=True)
cat = {
    'trasporto': tau + c*xi, 'calore': tau - D*xi**2, 'Airy': tau + xi**3,
    'Schrod': tau - sp.I*xi**2, 'onda': tau**2 - c**2*xi**2, 'trave': tau**2 + xi**4,
    'KG': tau**2 - xi**2 + 1, 'Laplace': tau**2 + xi**2, 'reazione': tau - r_,
}
names = list(cat)
print("TABELLA dim C[tau,xi]/(P_i,P_j)  (None = infinita):")
for i in range(len(names)):
    row = []
    for j in range(i + 1, len(names)):
        dd = quotient_dim([cat[names[i]], cat[names[j]]], [tau, xi])
        row.append(f"{names[j]}={dd}")
    print(f"  {names[i]}: " + ", ".join(row))
okG1 = True
for i, p in enumerate(names):
    for q in names[i + 1:]:
        dd = quotient_dim([cat[p], cat[q]], [tau, xi])
        gcd1 = sp.gcd(cat[p], cat[q]).is_number
        okG1 &= (dd is not None) == bool(gcd1)
check_true("G1 dim finita  <=>  gcd(P_i,P_j)=1 (infinita solo per trasporto|onda, Schrod|trave: fattorizzazione)", okG1)

# ---------- C2.23 tipo misto
kk = sp.symbols('k_m', positive=True)
yy = sp.symbols('yy', positive=True)
u = sp.cos(kk*x)*sp.airyai(kk**sp.Rational(2, 3)*y)
check("C2.23 Tricomi y u_xx + u_yy = 0: cos(kx) Ai(k^{2/3} y)", y*sp.diff(u, x, 2) + sp.diff(u, y, 2))
u = sp.cos(kk*x)*sp.sqrt(yy)*sp.besseli(1, 2*kk*sp.sqrt(yy))
check("C2.23 Keldysh u_xx + y u_yy = 0: cos(kx) sqrt(y) I1(2k sqrt y)", sp.diff(u, x, 2) + yy*sp.diff(u, yy, 2))
summary("t8_composite")
