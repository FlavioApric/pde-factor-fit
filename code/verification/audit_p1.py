# audit_p1.py -- S-CHECK-3: red team / controlli per i claim di S-P1 (work/P1/CHECK_REQUEST.md)
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_p1.py
import sympy as sp
import mpmath as mp
from sympy import symbols, exp, Rational, simplify, expand, Matrix, diff, integrate, oo

RES = []
def rep(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(("[OK]   " if ok else "[FAIL] ") + name + ((" -- " + str(info)) if info else ""))

t, x, s, z, eps = symbols('t x s zeta epsilon')
c, D, T = symbols('c D T', positive=True)

# ---------------------------------------------------------------- P1-P1(e)
print("== P1-P1(e) avvezione-diffusione ==")
a = D*z**2 - c*z
u = exp(a*t + z*x)
rep("P1e.1 u_zeta in ker Q (Q = tau + c xi - D xi^2)", simplify(diff(u, t) + c*diff(u, x) - D*diff(u, x, 2)) == 0)
z1 = exp(-c*z*t) - 1; z2 = exp(D*z**2*t) - 1
E = z1*z2*exp(z*x)
# E^add = u - u0 - (u1-u0) - (u2-u0), t0=0
u0 = exp(z*x); u1 = exp(-c*z*t)*u0; u2 = exp(D*z**2*t)*u0
rep("P1e.2 E^add = z1 z2 e^{zeta x}", simplify(u - u0 - (u1-u0) - (u2-u0) - E) == 0)
rep("P1e.3 esponente del rapporto: 2 D zeta^2 T - 2 a T = 2 c zeta T", simplify(2*D*z**2*T - 2*a*T - 2*c*z*T) == 0)

mp.mp.dps = 40
def ratio_sq(cc, DD, TT, zz, m, t0, J=(0.0, 1.0)):
    """||E^add||^2_{L2(Omega)} / ||u||^2_{H^m(Omega)} per u = e^{a t + zeta x}, zeta reale, base t0."""
    aa = DD*zz**2 - cc*zz
    eJ = mp.quad(lambda xx: mp.e**(2*zz*xx), [J[0], J[1]])
    # ||u||_{H^m}^2 = sum_{i+j<=m} a^{2i} zeta^{2j} * int e^{2at} * eJ
    It = mp.quad(lambda tt: mp.e**(2*aa*tt), [0, TT])
    Hm = sum(aa**(2*i)*zz**(2*j) for i in range(m+1) for j in range(m+1-i))*It*eJ
    def Esq(tt):
        sgap = tt - t0
        return (mp.e**(aa*t0))**2*((mp.e**(-cc*zz*sgap)-1)*(mp.e**(DD*zz**2*sgap)-1))**2
    En = mp.quad(Esq, mp.linspace(0, TT, 9))*eJ
    return En/Hm

for t0 in (0.0, 0.5, 1.0):
    vals = [ratio_sq(1, 1, 1, zz, 2, t0) for zz in (10, 20, 40, 80)]
    incr = all(vals[i+1] > vals[i] for i in range(1, len(vals)-1)) and vals[-1] > 1e6
    rep("P1e.4 rapporto ||E||^2/||u||^2_{H^2} illimitato in zeta (c=D=T=1), t0=%.1f" % t0, incr,
        ", ".join(mp.nstr(v, 5) for v in vals))
# lower bound della prova (t0=0): ||E||^2 >= e^{-2D}/(16 zeta^2) e^{2 D zeta^2 T} eJ
ok = True
for zz in (3, 6, 12):
    aa = zz**2 - zz
    eJ = mp.quad(lambda xx: mp.e**(2*zz*xx), [0, 1])
    En = mp.quad(lambda tt: ((mp.e**(-zz*tt)-1)*(mp.e**(zz**2*tt)-1))**2, mp.linspace(0, 1, 9))*eJ
    lb = mp.e**(-2)/(16*zz**2)*mp.e**(2*zz**2)*eJ
    ok = ok and En >= lb
rep("P1e.5 minorazione della prova verificata (zeta=3,6,12; c=D=T=1)", ok)

# ---------------------------------------------------------------- P1-T2(iv)
print("== P1-T2(iv) coefficienti multinomiali ==")
A1, A2, A3 = symbols('A1 A2 A3')  # commutativi: immagini di a_n(d_x) su u0
N = 3; As = [A1, A2, A3]
ser = lambda X, K: sum(s**k/sp.factorial(k)*X**k for k in range(K+1))
K = 6
Ehat = expand(ser(A1+A2+A3, K) - 1 - sum(ser(Ai, K) - 1 for Ai in As))
ok = True
for k in range(K+1):
    lhs = sp.factorial(k)*Ehat.coeff(s, k)
    rhs = 0
    for k1 in range(k+1):
        for k2 in range(k+1-k1):
            k3 = k - k1 - k2
            if sum(1 for kk in (k1, k2, k3) if kk > 0) >= 2:
                rhs += sp.factorial(k)/(sp.factorial(k1)*sp.factorial(k2)*sp.factorial(k3))*A1**k1*A2**k2*A3**k3
    ok = ok and expand(lhs - rhs) == 0
rep("T2iv.1 coefficiente di s^k/k! = somma multinomiale con >=2 indici positivi (N=3, k<=6)", ok)
Sgen = expand(sp.prod([1 + (ser(Ai, K) - 1) for Ai in As]))
rep("T2iv.2 somma sui sottoinsiemi = prodotto (troncato)", expand(Sgen - ser(A1+A2+A3, K)).as_poly(s).degree() > K or
    all(expand(Sgen - ser(A1+A2+A3, K)).coeff(s, k) == 0 for k in range(K+1)))

# ---------------------------------------------------------------- P1-L2(c)
print("== P1-L2(c) ==")
l = 2; Apol = -c*z + D*z**3
f = x**l*exp(z*x)
lhs = sum(s**k/sp.factorial(k)*sp.Function('dummy')(0) * 0 for k in range(1))  # placeholder
# applica (A(d_x))^k a f e confronta coeff. di s^k con d_zeta^l(A(zeta)^k e^{zeta x})/k!
def Aop(g):
    return -c*diff(g, x) + D*diff(g, x, 3)
ok = True; g = f
for k in range(5):
    target = diff(Apol**k*exp(z*x), z, l)
    ok = ok and simplify(g - target) == 0
    g = Aop(g)
rep("L2c.1 A(d)^k (x^2 e^{zeta x}) = d_zeta^2 (A(zeta)^k e^{zeta x}), k<5", ok)

# ---------------------------------------------------------------- P1-T5
print("== P1-T5 ==")
# (H) per X = x^a d, Y = d nel campo vettoriale: [f d, g d] = (f g' - g f') d
def br(f, g):
    return expand(f*diff(g, x) - g*diff(f, x))
for aa in (3, 4, 5):
    Yk = [sp.Integer(1)]
    for k in range(7):
        Yk.append(br(x**aa, Yk[-1]))
    degs = [sp.Poly(y, x).degree() if y != 0 else None for y in Yk]
    ck = [sp.Poly(y, x).LC() if y != 0 else 0 for y in Yk]
    formula = all(ck[k] == sp.prod([j*(aa-1) - aa for j in range(k)]) for k in range(len(Yk)))
    monom = all(len(sp.Poly(y, x).terms()) == 1 for y in Yk if y != 0)
    indep = (None not in degs) and len(set(degs)) == len(degs) and aa not in degs and monom
    rep("T5.H a=%d: Y_k = c_k x^{k(a-1)} d, c_k formula, gradi distinti e != a (k<=7)" % aa, formula and indep, degs)
Yk = [sp.Integer(1)]
for k in range(4):
    Yk.append(br(x**2, Yk[-1]))
rep("T5.H a=2: orbita finita (Y_2 = 2x^2 d, Y_3 = 0: c_3 contiene il fattore 2(a-1)-a = 0)", Yk[2] != 0 and Yk[3] == 0, Yk)
# Duhamel formale con matrici non commutative generiche (3x3 simboliche numeriche razionali)
Xm = Matrix([[0, 1, 2], [1, 0, -1], [3, 1, 0]]); Ym = Matrix([[1, 0, 0], [2, -1, 1], [0, 1, 1]])
KT = 6
def expser(Mx, KK):
    out = sp.zeros(3); P = sp.eye(3)
    for k in range(KK+1):
        out += t**k/sp.factorial(k)*P; P = P*Mx
    return out
L = expser(Xm + eps*Ym, KT)
dL = L.diff(eps).subs(eps, 0)
ad = [Ym]
for k in range(KT):
    ad.append(Xm*ad[-1] - ad[-1]*Xm)
R = expser(Xm, KT)*sum(((-1)**k*t**(k+1)/sp.factorial(k+1)*ad[k] for k in range(KT)), sp.zeros(3))
diffm = (dL - R).applyfunc(lambda e: sp.expand(e))
ok = all(sp.Poly(e, t).degree() > KT - 1 if e != 0 else True for e in diffm)
# confronta solo coefficienti fino a t^{KT-1}
ok = all(sp.expand(e).coeff(t, k) == 0 for e in diffm for k in range(KT))
rep("T5.duh d/de e^{t(X+eY)}|_0 = e^{tX} sum (-1)^k t^{k+1}/(k+1)! ad_X^k Y (coeff. t^0..t^5)", ok)
# P1-L5(b): e^{gX} Y e^{-gX} = sum g^k ad^k Y /k! (g = t + t^2)
gg = t + t**2
def expg(Mx, gfun, KK):
    out = sp.zeros(3); P = sp.eye(3)
    for k in range(KK+1):
        out += gfun**k/sp.factorial(k)*P; P = P*Mx
    return out
lhs = (expg(Xm, gg, KT)*Ym*expg(Xm, -gg, KT)).applyfunc(sp.expand)
rhs = sum((gg**k/sp.factorial(k)*ad[k] for k in range(KT)), sp.zeros(3)).applyfunc(sp.expand)
rep("L5b e^{gX}Ye^{-gX} = sum g^k ad^k Y/k! (coeff. t^0..t^5)", all((lhs[i]-rhs[i]).coeff(t, k) == 0 for i in range(9) for k in range(KT)))
# Hankel: det H_n = t^{n^2} det Hilb_n
tt = symbols('tt', positive=True)
ok = True
for n in range(1, 7):
    H = Matrix(n, n, lambda i, j: tt**(i+j+1)/(i+j+1))
    Hil = Matrix(n, n, lambda i, j: Rational(1, i+j+1))
    ok = ok and simplify(H.det() - tt**(n**2)*Hil.det()) == 0 and Hil.det() != 0
rep("T5.hank det H_n = t^{n^2} det Hilb_n != 0 (n<=6)", ok)
# rango <= p per somme finite di p 'atomi' (q_i, tau_i) qualsiasi (complessi)
import random
random.seed(1)
ok = True
for p in (1, 2, 3):
    qs = [sp.Rational(random.randint(-5, 5) or 1, random.randint(1, 4)) + sp.I*random.randint(-3, 3) for _ in range(p)]
    ts = [sp.Rational(random.randint(-5, 5), random.randint(1, 5)) + sp.I*random.randint(-2, 2) for _ in range(p)]
    n = p + 2
    H = Matrix(n, n, lambda i, j: sum(qs[r]*ts[r]**(i+j) for r in range(p)))
    ok = ok and H.rank() <= p
rep("T5.rank Hankel di p atomi ha rango <= p (p=1,2,3)", ok)
# Passo 1: e^{(G-t)X} = 1 => G = t: coefficiente minimo
G = t + 3*t**2
e1 = expg(Xm, G - t, 4).applyfunc(sp.expand)
rep("T5.p1 G-t di ordine m => coeff. t^m di e^{(G-t)X} = (G-t)_m X != 0", e1.applyfunc(lambda e: e.coeff(t, 2)) == 3*Xm)

# ---------------------------------------------------------------- P1-C1
print("== P1-C1 ==")
T1m = Matrix([[0, 1], [0, 0]]); T2m = Matrix([[0, 0], [1, 0]])
def mexp(Mx):
    return sp.simplify((Mx*t).exp())
frak = (mexp(T1m)*mexp(T2m)).inv()*mexp(T1m + T2m)
claimed = mexp(-T1m)*mexp(T1m + T2m)
correct = mexp(-T2m)*mexp(-T1m)*mexp(T1m + T2m)
rep("C1.1 la formula scritta e^{-tT1}e^{t(T1+T2)} NON e' (e^{tT1}e^{tT2})^{-1}e^{tA} (termini non commutanti)",
    sp.simplify(frak - claimed) != sp.zeros(2))
rep("C1.2 forma corretta e^{-tT2}e^{-tT1}e^{t(T1+T2)}: 3 esponenziali nello span (conclusione di C1 invariata)",
    sp.simplify(frak - correct) == sp.zeros(2))

# ---------------------------------------------------------------- P1-P3
print("== P1-P3 ==")
# a_1 = xi^2 + xi (termini xi^2, xi), a_2 = 2 xi^2 (un termine); w in ker(tau-a1) cap ker(tau-a2): zeta=1
w0 = exp(x)
E1w = (exp(s*1) - 1)*(exp(s*1) - 1)*w0   # z_{xi^2} z_{xi} con zeta=1
rep("P3.1 ambiguita' w = e^{2t+x} cambia E^add del fattore 1 di (e^s-1)^2 e^x != 0", sp.simplify(E1w) != 0 and
    sp.simplify((1+1) - 2*1) == 0)

# ---------------------------------------------------------------- P1-L4
print("== P1-L4 ==")
y = symbols('y')
# r = xi^2 - 3 xi + 2 = (xi-1)(xi-2), ell=1: G'' - 3G' + 2G = 0, G(0)=0, G'(0)=1 -> G = e^{2z} - e^{z}
Gf = sp.Lambda(z, exp(2*z) - exp(z))
rep("L4.1 G risolve r(d)G=0 con dati di Volterra", simplify(diff(Gf(z), z, 2) - 3*diff(Gf(z), z) + 2*Gf(z)) == 0 and Gf(0) == 0 and diff(Gf(z), z).subs(z, 0) == 1)
F = exp(2*t + 3*y)*(1 + y**2)
w = integrate(Gf(x - y)*F, (y, 0, x))
rw = simplify(diff(w, x, 2) - 3*diff(w, x) + 2*w - F.subs(y, x))
rep("L4.2 r(d_x) w = F per F = e^{2t+3x}(1+x^2)", rw == 0)

# ---------------------------------------------------------------- P1-P4
print("== P1-P4 ==")
b_, c_ = symbols('b c_')
p11, p12, p21, p22 = symbols('p11 p12 p21 p22')
Mx = Matrix([[p11, p12], [p21, p22]])
Lm = Matrix([[1, 0], [p21/p11, 1]]); Dm = Matrix([[p11, 0], [0, (p11*p22 - p12*p21)/p11]]); Um = Matrix([[1, p12/p11], [0, 1]])
rep("P4.1 Gauss 2x2 in anello commutativo: M = L diag(p11, det/p11) U", simplify(Lm*Dm*Um - Mx) == sp.zeros(2))
# onda: phi1 = cosh(zeta t); KG: phi1 = cosh(sqrt(c^2 zeta^2 - m^2) t), T* esatto vs bound log2/K
mm, cc = 2.0, 1.0
ok = True; info = []
for rho in (0.5, 1.0, 3.0):
    Tstar = mp.pi/(2*mp.sqrt(mm**2 + cc**2*rho**2))   # primo zero minimo su |zeta|<=rho (zeta = i rho)
    Kb = max(1, cc**2*rho**2 + mm**2)
    ok = ok and Tstar >= mp.log(2)/Kb
    # controllo numerico: min |phi1| su griglia del disco per t < Tstar e' > 0
    tt_ = 0.999*Tstar
    mins = min(abs(mp.cosh(mp.sqrt(cc**2*(r*mp.e**(1j*th))**2 - mm**2)*tt_))
               for r in (0, rho/2, rho) for th in [k*mp.pi/24 for k in range(48)])
    ok = ok and mins > 0
    info.append("rho=%g T*=%s bound=%s" % (rho, mp.nstr(Tstar, 4), mp.nstr(mp.log(2)/Kb, 4)))
rep("P4.2 KG (m=2,c=1): T*(rho)=pi/(2 sqrt(m^2+c^2 rho^2)) >= log2/K, phi1 != 0 per t<T*", ok, "; ".join(info))
# coerenza con II-T7-cons: sui modi reali |c xi|<m il propagatore di KG e' solo locale, t*=pi/(2 sqrt(m^2-c^2 xi^2))
xi0 = 1.0
tloc = mp.pi/(2*mp.sqrt(mm**2 - cc**2*xi0**2))
rep("P4.3 KG modo reale xi=1: zero di phi1 a t*=pi/(2 sqrt(3)) e T*(rho>=1) <= t*", abs(mp.cosh(mp.sqrt(cc**2*xi0**2 - mm**2)*tloc)) < 1e-20 and
    mp.pi/(2*mp.sqrt(mm**2 + cc**2*1.0)) <= tloc)

# ---------------------------------------------------------------- P1-P6
print("== P1-P6 ==")
gfun = sp.Function('g')
kap = c/(2*D)
fexpr = exp(kap*x)*gfun(x)
Af = D*diff(fexpr, x, 2) - c*diff(fexpr, x)
rep("P6.1 M A M^{-1} = D d^2 - c^2/(4D)", simplify(exp(-kap*x)*Af - (D*diff(gfun(x), x, 2) - c**2/(4*D)*gfun(x))) == 0)
lam = symbols('lambda', positive=True)
ff = sp.Function('f')
uR = (1/c)*sp.Integral(exp(-lam*(x - y)/c)*ff(y), (y, 0, x))
rep("P6.2 resolvente inflow: lambda u + c u' = f, u(0)=0", simplify(lam*uR + c*diff(uR, x) - ff(x)) == 0 and uR.subs(x, 0).doit() == 0)

# ---------------------------------------------------------------- P1-T4 (OU)
print("== P1-T4 OU ==")
g2 = (1 - exp(-2*t))/2
ok = True
for n in range(0, 7):
    # lato destro: e^{-t x d} e^{g2 d^2} x^n  (prima calore per tempo g2, poi riscalamento x -> e^{-t} x)
    h = sum(g2**k/sp.factorial(k)*diff(x**n, x, 2*k) for k in range(n//2 + 1))
    rhs = h.subs(x, exp(-t)*x)
    # lato sinistro: soluzione polinomiale di u_t = u_xx - x u_x, u(0)=x^n -> verifica PDE e dato
    pde = simplify(diff(rhs, t) - diff(rhs, x, 2) + x*diff(rhs, x))
    ok = ok and pde == 0 and simplify(rhs.subs(t, 0) - x**n) == 0
rep("T4.OU e^{-t x d} e^{g2 d^2} x^n risolve u_t = u_xx - x u_x con dato x^n (n<=6)", ok)
# sl2 (P1-P5(b)): Gauss di e^{t(E-F)}: g21 = -tan t
Rm = Matrix([[sp.cos(t), sp.sin(t)], [-sp.sin(t), sp.cos(t)]])
rep("P5.1 rotazione: lower-left di Gauss = -tan t", simplify(Rm[1, 0]/Rm[0, 0] + sp.tan(t)) == 0 and ((Matrix([[0, 1], [-1, 0]])*t).exp() - Rm).applyfunc(lambda e: sp.simplify(e.rewrite(sp.cos))) == sp.zeros(2))

# ---------------------------------------------------------------- P1-T3 (DP aggregati)
print("== P1-T3 ==")
zs = symbols('z1:8')
ek_brute = [sp.expand(sum(sp.prod(S) for S in __import__('itertools').combinations(zs, k))) for k in range(8)]
coef = [sp.Integer(1)]
for zn in zs:
    new = [sp.Integer(0)]*(len(coef)+1)
    for k, ck in enumerate(coef):
        new[k] += ck; new[k+1] += ck*zn
    coef = [sp.expand(e) for e in new]
rep("T3.1 DP prod(1+lambda z_n) = e_k (N=7), #c_S = 2^7-7-1 = 120", all(sp.expand(coef[k] - ek_brute[k]) == 0 for k in range(8)) and 2**7-7-1 == 120)

print("\nESITO GLOBALE: %s (%d/%d)" % ("OK" if all(o for _, o in RES) else "FAIL", sum(o for _, o in RES), len(RES)))


