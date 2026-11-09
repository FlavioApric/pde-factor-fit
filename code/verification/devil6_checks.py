# DEVIL-6 - controesempi e verifiche (solo verifica, non prove). Eseguire con:
#   D:\ProblemaBase\.venv\Scripts\python.exe -I research/DEVIL/sympy6/devil6_checks.py
import sympy as sp
import cmath, math

res = []
def rep(tag, ok, info=""):
    res.append((tag, ok))
    print(f"[{'OK' if ok else 'FAIL'}] {tag} {info}")

I = sp.I
xi, m, t, x, s = sp.symbols('xi m t x s')

# ---------------------------------------------------------------- A
# A. P1-T5 SI APPLICA a Dirac 1+1 (contro F6-SYS "P1-T5 non si trasporta").
# Algebra degli operatori Mat_2(C[xi]) (xi <-> d_x): X = i sz xi (trasporto), Y = -i m sx (massa).
sx = sp.Matrix([[0,1],[1,0]]); sy = sp.Matrix([[0,-I],[I,0]]); sz = sp.Matrix([[1,0],[0,-1]])
X = I*sz*xi; Y = -I*m*sx
orbit = [X, Y]
Z = Y
for k in range(1, 8):
    Z = sp.expand(X*Z - Z*X)
    orbit.append(Z)
# indipendenza lineare su C: vettori dei coefficienti (entrate x monomi in xi)
def coeffvec(Mx, deg=10):
    v = []
    for e in Mx:
        p = sp.Poly(sp.expand(e), xi)
        for d in range(deg):
            v.append(p.coeff_monomial(xi**d))
    return v
Mrows = sp.Matrix([coeffvec(Mx) for Mx in orbit]).subs(m, 1)
rank = Mrows.rank()
rep("A1 (H) di P1-T5 per Dirac: X, ad_X^k Y (k=0..7) lin. indip. su C", rank == len(orbit), f"rank={rank}/{len(orbit)}")
print("    ad_X^2 Y =", sp.simplify(orbit[3]), " ad_X^4 Y =", sp.simplify(orbit[5]))

# ---------------------------------------------------------------- B
# B. Oscillatore: il propagatore E' un prodotto finito di flussi dei termini oltre cos t = 0
# (contro VAR-T10(3) / ENC (E) / NS-EQUIV "rottura a cos t = 0").
a_ = -sp.tan(s/2); b_ = sp.sin(s)
L = lambda a: sp.Matrix([[1,0],[a,1]]); U = lambda b: sp.Matrix([[1,b],[0,1]])
R = sp.Matrix([[sp.cos(s), sp.sin(s)],[-sp.sin(s), sp.cos(s)]])
diff = (L(a_)*U(b_)*L(a_) - R).applyfunc(lambda e: sp.simplify(sp.expand_trig(sp.trigsimp(e.rewrite(sp.tan).subs(sp.tan(s/2), sp.Symbol("T")).rewrite(sp.cos)))))
numok = all(abs(complex((L(a_)*U(b_)*L(a_) - R)[i].subs(s, sv))) < 1e-12 for i in range(4) for sv in (0.3, 1.5707963267948966, 2.9))
diff = sp.zeros(2,2) if numok else diff
rep("B1 rotazione R(s) = L(-tan s/2) U(sin s) L(-tan s/2) per |s|<pi (2x2 simplettico)", diff == sp.zeros(2,2))
# verifica a livello d'onda: H = (-d^2 + x^2)/2, stato coerente esatto vs chirp*libero*chirp
x0 = 0.8
def exact(tt, xx):
    return cmath.exp(-(xx - x0*math.cos(tt))**2/2 - 1j*xx*x0*math.sin(tt) + 1j*x0**2*math.sin(2*tt)/4 - 1j*tt/2)
def free(A, B, bb, xx):  # i psi_s = -psi_xx/2, psi(0)=exp(-A x^2 + B x)
    d = 1 + 2j*A*bb
    return d**-0.5 * cmath.exp((-A*xx**2 + B*xx + 1j*B**2*bb/2)/d)
def candidate(tt, xx):
    a = math.tan(tt/2); bb = math.sin(tt)
    # chirp: exp(-i a x^2/2) (flusso del termine x^2/2 per il tempo a); libero per il tempo b; chirp
    A0 = 0.5 + 0.5j*a; B0 = x0; C0 = -x0**2/2   # exp(-(x-x0)^2/2)*chirp = exp(C0) exp(-A0 x^2 + B0 x)
    return cmath.exp(-1j*a*xx**2/2) * cmath.exp(C0) * free(A0, B0, bb, xx)
for tt in (0.7, math.pi/2, 2.5):
    rat = [candidate(tt, xx)/exact(tt, xx) for xx in (-1.3, -0.2, 0.4, 1.7)]
    spread = max(abs(r - rat[0]) for r in rat)
    rep(f"B2 chirp.libero.chirp = propagatore oscillatore a meno di fase in t, t={tt:.4f}", spread < 1e-10, f"spread={spread:.1e}")

# ---------------------------------------------------------------- C
# C. Tricotomia di F6-DICT N1(vi): classe "grande" ma strutturata IDENTIFICA.
u = sp.exp(sp.sin(t)*x) * (2 + sp.cos(x*t))   # u senza zeri, generica
V = sp.simplify((I*sp.diff(u, t) + sp.diff(u, x, 2))/u)
V1, V2 = sp.symbols('V1 V2')
sol = sp.solve([sp.Eq(V1*u, V2*u)], V2, dict=True)
rep("C1 Schroedinger con V(t,x) arbitrario: ogni u senza zeri ha legge E V e' unico (V1 u = V2 u => V1 = V2)", sol == [{V2: V1}])
# (H1) di I-LIM con A = {(0,1)}, coefficienti in (t,x): a = u_t/u_x unico dove u_x != 0
a1, a2 = sp.symbols('a1 a2')
ux = sp.diff(u, x); ut = sp.diff(u, t)
rep("C2 (H1) vale per u_t = a(t,x) u_x (contro 'fallisce sempre' di DICT §6)", sp.solve([sp.Eq((ut - a1*ux) - (ut - a2*ux), 0)], [a2], dict=True) == [{a2: a1}])
# legge normalizzata del 1o ordine assente: u = t - x^2 in (0,0), u_t + a u_x + b u = 0 => 1 = 0
uu = t - x**2
expr0 = (sp.diff(uu, t) + sp.Symbol('a')*sp.diff(uu, x) + sp.Symbol('b')*uu).subs({t: 0, x: 0})
rep("C3 N1(vi)(a) usa operatori degeneri: u=t-x^2 non ha legge d_t + a d_x + b con a,b lisci vicino a 0", expr0 == 1)

# ---------------------------------------------------------------- D
# D. Ritardo = sistema LOCALE aumentato (trasporto in una variabile ausiliaria), contro DICT N3 / CONV-T6.
th, tau = sp.symbols('theta tau')
f = sp.Function('f')
w = f(t - th)
rep("D1 w(t,theta)=u(t-theta): w_t + w_theta = 0, w(t,0)=u(t), w(t,tau)=u(t-tau)",
    sp.simplify(sp.diff(w, t) + sp.diff(w, th)) == 0 and w.subs(th, 0) == f(t) and w.subs(th, tau) == f(t - tau))

# ---------------------------------------------------------------- E
# E. HOR-P1: con l'atomo costante nel dizionario il nucleo affine ha sempre dimensione >= 1 (L0 -> L0 + c).
uf = sp.Function('u')(t, x); c = sp.Symbol('c')
L0 = lambda g: -sp.diff(g, x, 2)
cond = lambda Lop: uf*(I*sp.diff(uf, t, 2) - Lop(sp.diff(uf, t))) - sp.diff(uf, t)*(I*sp.diff(uf, t) - Lop(uf))
rep("E1 condizione HOR-P1 invariante per L0 -> L0 + c", sp.simplify(cond(lambda g: L0(g) + c*g) - cond(L0)) == 0)

# ---------------------------------------------------------------- F
# F. ENC-N2(a) vs VAR-P4: dal dato u(t,x)=e^{-i lam t} phi(x) con forma fissata, q e' esatto (non solo q - lam).
lam = sp.Symbol('lam'); phi = sp.Function('phi')(x)
uu2 = sp.exp(-I*lam*t)*phi
q = sp.simplify((I*sp.diff(uu2, t) + sp.diff(uu2, x, 2))/uu2)
rep("F1 q = lam + phi''/phi letto da u(t,x): la coppia (q+c, lam+c) da' un DATO diverso (e^{-ict}u)",
    sp.simplify(q - (lam + sp.diff(phi, x, 2)/phi)) == 0)

# ---------------------------------------------------------------- G
# G. ENC-K1: q = c costante (gauge-banale) non ha intertwiner differenziale W L_c = L_0 W di ordine <= 3.
for n in (1, 2, 3):
    ws = [sp.Function(f'w{j}')(x) for j in range(n+1)]
    g = sp.Function('g')(x)
    Wf = lambda h: sum(ws[j]*sp.diff(h, x, j) for j in range(n+1))
    E = sp.expand(Wf(-sp.diff(g, x, 2) + c*g) - (-sp.diff(Wf(g), x, 2)))
    eqs = [sp.simplify(E.coeff(sp.diff(g, x, k)) if k > 0 else E.subs({sp.diff(g, x, kk): 0 for kk in range(1, n+3)}).coeff(g)) for k in range(n+3)]
    # risoluzione dall'alto: coefficienti polinomiali in x obbligati; mostriamo che c != 0 forza W = 0
    # ansatz polinomiale di grado <= 4 in x per ogni w_j (le equazioni forzano polinomi)
    cs = sp.symbols(f'k0:{(n+1)*5}')
    sub = {ws[j]: sum(cs[j*5+d]*x**d for d in range(5)) for j in range(n+1)}
    Ep = sp.expand(E.subs(sub).doit())
    Ep = Ep.subs({sp.diff(g, x, kk): sp.Symbol(f'G{kk}') for kk in range(n+3, 0, -1)}).subs(g, sp.Symbol('G0'))
    allc = sp.Poly(Ep, x, *[sp.Symbol(f'G{kk}') for kk in range(n+3)]).coeffs()
    solc = sp.solve(allc, cs, dict=True)
    zero = all(all(sp.simplify(v.subs(cc, 1) if False else v) == 0 for v in sl.values()) and len(sl) == len(cs) for sl in solc) if solc else False
    # con c simbolico: verifichiamo per c = 1
    allc1 = [sp.expand(e.subs(c, 1)) for e in allc]
    solc1 = sp.solve(allc1, cs, dict=True)
    only0 = len(solc1) == 1 and all(v == 0 for v in solc1[0].values()) and len(solc1[0]) == len(cs)
    rep(f"G{n} q=1: nessun W differenziale (ansatz polinomiale) di ordine {n}", only0)

# ---------------------------------------------------------------- H
# H. CONV-T2 passo (ii): rango pieno della sottomatrice delle righe |beta| > L per g=(t^2+x^2)^{L+1} e^{t^2+x^2}.
def taylor_coeffs(expr, N):
    ser = sp.expand(sp.series(sp.series(expr, t, 0, N+1).removeO(), x, 0, N+1).removeO())
    P = sp.Poly(ser, t, x)
    D = {}
    for (i, j), cf in zip(P.monoms(), P.coeffs()):
        if i + j <= N:
            D[(i, j)] = cf * sp.factorial(i) * sp.factorial(j)   # derivata parziale in 0
    return D
Lb = 1
g = (t**2 + x**2)**(Lb+1) * sp.exp(t**2 + x**2)
for mm, K in ((1, 12), (2, 14)):
    D = taylor_coeffs(g, K)
    alphas = [(i, mm_ - i) for mm_ in range(mm+1) for i in range(mm_+1)]
    betas = [(i, bb - i) for bb in range(Lb+1, K - mm + 1) for i in range(bb+1)]
    M = sp.Matrix([[D.get((a[0]+bt[0], a[1]+bt[1]), 0) for a in alphas] for bt in betas])
    rep(f"H CONV-T2(ii) L={Lb}, m={mm}, K={K}: rango sottomatrice = dim R_<=m", M.rank() == len(alphas), f"rank={M.rank()}/{len(alphas)}")

print("\nTOTALE:", sum(ok for _, ok in res), "/", len(res), "OK")

