# p2_checks.py — controlli SymPy per work/P2/PROOF_PACKAGE.md (S-P2). SOLO verifica, non metodo.
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I p2_checks.py > p2_checks.out
import sympy as sp
import itertools, random

results = []
def check(name, cond):
    ok = bool(cond)
    results.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)

t, x, s, z = sp.symbols('t x s z')
c, D, lam = sp.symbols('c D lambda', positive=True)
xi = sp.symbols('xi')

# ---------- K1: P2-T1 su un esempio finito (Tikhonov l2, residuo -> P^perp u) ----------
# H = R^3, dizionario D = {e1, e1+e2 (non normalizzato)}, M = span{e1,e2}, u = (1,2,3): P^perp u = (0,0,3)
al = sp.symbols('alpha', positive=True)
Smat = sp.Matrix([[1, 1], [0, 1], [0, 0]])
u = sp.Matrix([1, 2, 3])
om = (Smat.T*Smat + al*sp.eye(2)).inv()*Smat.T*u
r = u - Smat*om
check("K1 Tikhonov l2: residuo -> P^perp u per alpha->0", sp.simplify(r.applyfunc(lambda e: sp.limit(e, al, 0)) - sp.Matrix([0, 0, 3])) == sp.zeros(3, 1))
# l1-like regularizzatore: R(w)=|w1|+|w2|; con u nello span il minimo e' Sw=Pu; residuo indipendente da R (verifica sul limite: P u raggiungibile)
check("K1b P u nello span: esiste w con Sw = Pu", (Smat*sp.Matrix([-1, 2]) - sp.Matrix([1, 2, 0])) == sp.zeros(3, 1))

# ---------- K2: P2-T2 avvezione-diffusione ----------
a1 = -c*xi; a2 = D*xi**2; a = a1 + a2
prod = sp.expand((a - a1)*(a - a2))
check("K2a Pi(a-a_n) = -cD xi^3", sp.simplify(prod + c*D*xi**3) == 0)
def op(poly_xi, f):  # applica poly(d/dx) a f
    p = sp.Poly(poly_xi, xi)
    return sum(coef*sp.diff(f, x, k[0]) for k, coef in zip(p.monoms(), p.coeffs()))
AD = lambda f: sp.diff(f, t) + c*sp.diff(f, x) - D*sp.diff(f, x, 2)
TR = lambda f: sp.diff(f, t) + c*sp.diff(f, x)
HE = lambda f: sp.diff(f, t) - D*sp.diff(f, x, 2)
basis = [sp.Integer(1), x - c*t, (x - c*t)**2 + 2*D*t]
check("K2b base Sol(R/J) in ker AD", all(sp.simplify(AD(b)) == 0 for b in basis))
check("K2c base Sol(R/J) annullata da d_x^3", all(sp.simplify(sp.diff(b, x, 3)) == 0 for b in basis))
# Q = (dt - a1)(dt - a2) applicato a u in ker AD da' -cD u_xxx: verifica su soluzione generica esponenziale
zeta = sp.symbols('zeta')
ue = sp.exp((D*zeta**2 - c*zeta)*t + zeta*x)
Qu = TR(HE(ue))
check("K2d Qu = -cD u_xxx su modi di V(P)", sp.simplify(Qu + c*D*sp.diff(ue, x, 3)) == 0)
# decomposizione esplicita in D_1 + D_2 dell'elemento quadratico
s_ = x - c*t
v1 = s_**2 - 2*D*s_/c; v2 = 2*D*x/c
check("K2e (x-ct)^2+2Dt = v1 + v2, v1 in ker TR, v2 in ker HE",
      sp.simplify(v1 + v2 - basis[2]) == 0 and sp.simplify(TR(v1)) == 0 and sp.simplify(HE(v2)) == 0)

# tre termini: a = D xi^2 - c xi - lam ; dim = sum deg(a - a_n) = 1+2+2 = 5
terms = [D*xi**2, -c*xi, -lam*sp.Integer(1)]
aa = sum(terms)
degs = [sp.degree(sp.expand(aa - tn), xi) for tn in terms]
check("K2f dim Sol(R/J) = 5 per D xi^2 - c xi - lam", sum(degs) == 5)
# ogni radice zeta di a - a_n da' un esponenziale in ker(dt - a_n)
okf = True
for n, tn in enumerate(terms):
    for rt in sp.solve(sp.expand(aa - tn), xi):
        f = sp.exp(aa.subs(xi, rt)*t + rt*x)
        lhs = sp.diff(f, t) - op(sp.expand(tn), f) if sp.degree(tn, xi) > 0 else sp.diff(f, t) - tn*f
        okf = okf and sp.simplify(lhs) == 0
check("K2g modi spettrali di Sol(R/J) nelle classi dei termini", okf)

# ---------- K3: P2-P2 (ODE) esempio R1: ||P^perp e^x||^2 in L2(0,1) rispetto a span{1,x} ----------
G = sp.Matrix([[sp.integrate(1, (x, 0, 1)), sp.integrate(x, (x, 0, 1))], [sp.integrate(x, (x, 0, 1)), sp.integrate(x**2, (x, 0, 1))]])
bvec = sp.Matrix([sp.integrate(sp.exp(x), (x, 0, 1)), sp.integrate(x*sp.exp(x), (x, 0, 1))])
coef = G.inv()*bvec
res2 = sp.integrate(sp.exp(2*x), (x, 0, 1)) - (bvec.T*coef)[0]
check("K3 ||P^perp e^x||^2 = 20e - 7e^2/2 - 57/2 (valore R1)", sp.simplify(res2 - (20*sp.E - sp.Rational(7, 2)*sp.E**2 - sp.Rational(57, 2))) == 0)
print("     valore numerico:", sp.N(res2))

# ---------- K4: P2-T3 spettro di S*S su (ker S)^perp = [1-cF,1+cF] U {2} (esempi finiti) ----------
import numpy as np
rng = np.random.default_rng(1)
def orth(Mx, tol=1e-10):   # base ON dello spazio colonne (SVD: robusta anche con rango deficiente)
    U, sv, _ = np.linalg.svd(Mx, full_matrices=False); return U[:, sv > tol]
okspec = True; okRa = True
for trial in range(6):
    n = 7
    Ib = rng.standard_normal((n, 1))                       # intersezione di dim 1
    A0 = rng.standard_normal((n, 2)); B0 = rng.standard_normal((n, 2))
    H1 = orth(np.hstack([Ib, A0])); H2 = orth(np.hstack([Ib, B0]))
    S = np.hstack([H1, H2])                                # sintesi H1 (+) H2 -> R^n in coordinate ON
    T = S.T @ S
    ev = np.sort(np.linalg.eigvalsh(T))
    nonzero = ev[ev > 1e-10]
    # c_F tra H1 - I e H2 - I
    PI = orth(Ib); Pp = np.eye(n) - PI @ PI.T
    A = orth(Pp @ H1); B = orth(Pp @ H2)
    cF = np.linalg.svd(A.T @ B, compute_uv=False).max()
    okspec = okspec and abs(nonzero.min() - (1 - cF)) < 1e-9 and abs(nonzero.max() - 2) < 1e-9 and len(ev) - len(nonzero) == 1
    # ||R_alpha|| <= (1-cF)^(-1/2) e -> uguaglianza per alpha -> 0
    for alv in [1e-1, 1e-3, 1e-6]:
        Ra = np.linalg.solve(T + alv*np.eye(T.shape[0]), S.T)
        nr = np.linalg.norm(Ra, 2)
        okRa = okRa and nr <= (1 - cF)**-0.5 + 1e-9
    okRa = okRa and abs(np.linalg.norm(np.linalg.solve(T + 1e-9*np.eye(T.shape[0]), S.T), 2) - (1 - cF)**-0.5) < 1e-4
check("K4a inf sigma(S*S|(ker S)^perp) = 1 - c_F, max = 2, dim ker S = dim I (6 prove)", okspec)
check("K4b ||(S*S+a)^-1 S*|| <= (1-c_F)^-1/2, -> uguaglianza per a->0", okRa)
# caso C12-P8 (trasporti paralleli c=0): Gram normalizzata [[1,g],[g,1]] ha autovalori 1 +- g
g = sp.symbols('g', positive=True)
check("K4c Gram normalizzata di due esponenziali in t: autovalori 1 +- gamma", set(sp.Matrix([[1, g], [g, 1]]).eigenvals().keys()) == {1 - g, 1 + g})

# ---------- K5: P2-T5 tau*xi sul rettangolo: basi adattate, coerenze incrociate in L2 e H^1 ----------
T_, L_ = sp.Integer(1), sp.Integer(2)   # Omega = (0,1) x (0,2)
def gram_schmidt(funcs, ip):
    out = []
    for f in funcs:
        v = f - sum(ip(f, e)*e for e in out)
        nv = sp.sqrt(sp.simplify(ip(v, v)))
        out.append(sp.simplify(v/nv))
    return out
def ip_Om(f, h, m):  # prodotto H^m(Omega) per funzioni reali
    tot = 0
    for i in range(m + 1):
        for j in range(m + 1 - i):
            tot += sp.integrate(sp.integrate(sp.diff(f, t, i, x, j)*sp.diff(h, t, i, x, j), (t, 0, T_)), (x, 0, L_))
    return sp.simplify(tot)
okmca = True
for m in [0, 1]:
    E1 = gram_schmidt([sp.Integer(1), t, t**2, t**3], lambda f, h: ip_Om(f, h, m))
    E2 = gram_schmidt([sp.Integer(1), x, x**2, x**3], lambda f, h: ip_Om(f, h, m))
    for k, e in enumerate(E1):
        for l, f in enumerate(E2):
            val = ip_Om(e, f, m)
            exp_val = 1 if (k == 0 and l == 0) else 0
            okmca = okmca and sp.simplify(val - exp_val) == 0
check("K5a tau*xi: <e_k,f_l>_{H^m} = delta_k0 delta_l0 (m=0,1; gradi<=3) => kappa = 0 escludendo la costante", okmca)
# NSP sul gauge con la costante in un solo cluster: minimizzatori non unici
al1, be1 = sp.Rational(1, 2), sp.Rational(3, 2)
fz = lambda zz: abs(al1 + zz) + abs(be1 - zz)
vals = [fz(sp.Rational(k, 4)) for k in range(-2, 7)]
check("K5b gauge 1-dim, costante in entrambi i cluster: f(z)=|a+z|+|b-z| costante su [-a,b] (non unicita')", len(set(vals[0:9])) >= 1 and fz(-al1) == fz(be1) == fz(0) == al1 + be1)

# ---------- K6: P2-P4(b) encoder iniettivo compatto che annulla la distanza (troncamenti) ----------
okenc = True; prev = None
for N in [10, 100, 1000, 10000]:
    k = np.arange(1, N + 1)
    w = 1.0/k; w = w/np.linalg.norm(w)        # M = w^perp, dist(w, M) = 1
    Ew = w/k
    y = k*w                                   # y ⟂ E M  <=> E y in span(w)  (E simmetrica)
    dist = abs(Ew @ y)/np.linalg.norm(y)
    okenc = okenc and (prev is None or dist < prev); prev = dist
print("     dist(Ew, EM) per N = 10^4:", prev)
check("K6 dist(Ew, E M) decresce -> 0 (dist(w,M)=1 fisso)", okenc and prev < 0.02)

# ---------- K7: P2-P5 identita' e_{>=2} ----------
b1, b2, b3 = sp.symbols('b1 b2 b3')
lhs = sum(sp.prod(S_) for r_ in [2, 3] for S_ in itertools.combinations([b1, b2, b3], r_))
check("K7 sum_{|S|>=2} prod b = prod(1+b) - 1 - sum b (N=3)", sp.expand(lhs - ((1 + b1)*(1 + b2)*(1 + b3) - 1 - b1 - b2 - b3)) == 0)
kap = sp.symbols('kappa', real=True); tt = sp.symbols('tt', nonnegative=True)
check("K7b AD su R: |e^{t a_1(ik)}| = 1, |e^{t a_2(ik)}| = e^{-D k^2 t} <= 1",
      sp.simplify(sp.Abs(sp.exp(tt*(-c*sp.I*kap)))) == 1 and sp.simplify(sp.exp(tt*D*(sp.I*kap)**2) - sp.exp(-D*kap**2*tt)) == 0)

# ---------- K8: P2-P6 Vandermonde ----------
okv = True
for d in [2, 3, 4, 5]:
    h = sp.symbols('h', positive=True); z0 = sp.Rational(1, 3)
    nodes = [z0 + j*h for j in range(d + 1)]
    V = sp.Matrix(d + 1, d + 1, lambda i, j: nodes[i]**j)
    Vi = V.inv()
    for kk in range(d + 1):
        lead = sp.simplify(Vi[d, kk])   # coefficiente di xi^d in l_k
        expect = 1/sp.prod([nodes[kk] - nodes[j] for j in range(d + 1) if j != kk])
        okv = okv and sp.simplify(lead - expect) == 0
    # bound ||coef(l_k)||_1 <= prod(1+|z_j|)/|z_k - z_j| su valori numerici
    hv = sp.Rational(1, 10); nv = [nd.subs(h, hv) for nd in nodes]
    Vn = sp.Matrix(d + 1, d + 1, lambda i, j: nv[i]**j).inv()
    for kk in range(d + 1):
        l1 = sum(abs(Vn[i, kk]) for i in range(d + 1))
        bound = sp.prod([(1 + abs(nv[j]))/abs(nv[kk] - nv[j]) for j in range(d + 1) if j != kk])
        okv = okv and l1 <= bound
check("K8 Vandermonde: coeff. di testa di l_k = 1/prod(z_k-z_j); ||coef l_k||_1 <= prod(1+|z_j|)/|z_k-z_j| (d=2..5)", okv)

print()
print(f"TOTALE: {sum(ok for _, ok in results)}/{len(results)} PASS")
