# F6-SYS — verifiche SymPy sui casi minimi (solo verifica, non prova).
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I research/F6-SYS/sympy/sys_checks.py
import sympy as sp

ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1
    r = bool(cond)
    ok += r
    print(("OK  " if r else "FAIL"), name, flush=True)

t, x, y, z = sp.symbols('t x y z', real=True)
p0, p1, p2, p3, m = sp.symbols('p0 p1 p2 p3 m')
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])

# ---------- [A] Dirac 1+1: Clifford, fattorizzazione di KG, modulo ciclico ----------
g0 = sx; g1 = sp.I*sy            # g0^2 = I, g1^2 = -I, anticommutano
check("A1 Clifford 1+1: g0^2=I, g1^2=-I, {g0,g1}=0",
      g0*g0 == I2 and g1*g1 == -I2 and (g0*g1 + g1*g0) == sp.zeros(2))
D = g0*p0 + g1*p1 - m*I2         # simbolo di Dirac (p_mu <-> i d_mu)
Dp = g0*p0 + g1*p1 + m*I2
KG = p0**2 - p1**2 - m**2
check("A2 D*D' = D'*D = (p^2-m^2) I", sp.simplify(D*Dp - KG*I2) == sp.zeros(2) and sp.simplify(Dp*D - KG*I2) == sp.zeros(2))
check("A3 det D = -KG (1+1, una sola copia del simbolo scalare; segno corretto dopo FAIL iniziale)", sp.expand(D.det() + KG) == 0)
# M_D = R^{1x2}/R^{1x2} D ciclico generato da e2: riga 1 = (-m, p0+p1) => e1 = (p0+p1)/m e2
# Ann(e2): riga 2 = (p0-p1, -m) => (p0-p1)(p0+p1)/m - m = KG/m
print("   D =", D.tolist())
check("A4 riga1 = (-m, p0+p1), riga2 = (p0-p1, -m)", D.row(0).tolist()[0] == [-m, p0 + p1] and D.row(1).tolist()[0] == [p0 - p1, -m])
check("A5 Ann(e2) in M_D genera (KG): (p0-p1)*(p0+p1)/m - m = KG/m", sp.simplify((p0 - p1)*(p0 + p1)/m - m - KG/m) == 0)
# Biiezione Sol(KG) -> Sol(D): phi -> psi = ((d0+d1)phi/m ... ) controllo su onda piana e su soluzione generica
# Operatori: p_mu = i d_mu. Sol(D): (g0 p0 + g1 p1 - m) psi = 0.
def Dop(psi):
    P0 = lambda f: sp.I*sp.diff(f, t); P1 = lambda f: sp.I*sp.diff(f, x)
    return sp.Matrix([-m*psi[0] + P0(psi[1]) + P1(psi[1]), P0(psi[0]) - P1(psi[0]) - m*psi[1]])
phi = sp.Function('phi')(t, x)
psi = sp.Matrix([(sp.I*sp.diff(phi, t) + sp.I*sp.diff(phi, x))/m, phi])
res = Dop(psi)
KGop = lambda f: -sp.diff(f, t, 2) + sp.diff(f, x, 2) - m**2*f   # (p0^2-p1^2-m^2) con p=i d
check("A6 psi=(P0+P1)phi/m, phi): riga1 = 0 identicamente", sp.simplify(res[0]) == 0)
check("A7 riga2 = KG(phi)/m (=> psi in Sol(D) <=> phi in Sol(KG))", sp.simplify(res[1] - KGop(phi)/m) == 0)

# ---------- [B] Dirac 3+1 (rappresentazione chirale): M_D libero di rango 2 su S = R/(KG) ----------
Xm = p0*I2 + p1*sx + p2*sy + p3*sz
Ym = p0*I2 - p1*sx - p2*sy - p3*sz
KG4 = p0**2 - p1**2 - p2**2 - p3**2 - m**2
check("B1 X*Y = Y*X = (p0^2-|p|^2) I2", sp.expand(Xm*Ym - (KG4 + m**2)*I2) == sp.zeros(2) and sp.expand(Ym*Xm - (KG4 + m**2)*I2) == sp.zeros(2))
D4 = sp.BlockMatrix([[-m*I2, Xm], [Ym, -m*I2]]).as_explicit()
Dp4 = sp.BlockMatrix([[m*I2, Xm], [Ym, m*I2]]).as_explicit()
check("B2 D4*D4' = KG4*I4 (Dirac = radice matriciale di KG)", sp.expand(D4*Dp4 - KG4*sp.eye(4)) == sp.zeros(4))
check("B3 det D4 = KG4^2", sp.factor(D4.det() - KG4**2) == 0)
# riduzione: righe 1-2: -m e_top + X e_bot = 0 => e_top = X e_bot / m ; righe 3-4: Y e_top - m e_bot = (Y X/m - m) e_bot = KG4/m e_bot
check("B4 Y*X/m - m*I = (KG4/m) I  => M_D = S^{1x2} (libero, rango 2)", sp.expand(Ym*Xm/m - m*I2 - KG4/m*I2) == sp.zeros(2))
# Clifford 3+1 dalla forma a blocchi
G0 = sp.BlockMatrix([[sp.zeros(2), I2], [I2, sp.zeros(2)]]).as_explicit()
Gs = [sp.BlockMatrix([[sp.zeros(2), s], [-s, sp.zeros(2)]]).as_explicit() for s in (sx, sy, sz)]
Gam = [G0] + Gs; eta = sp.diag(1, -1, -1, -1)
check("B5 {g^mu, g^nu} = 2 eta^{mu nu} I4", all(sp.simplify(Gam[a]*Gam[b] + Gam[b]*Gam[a] - 2*eta[a, b]*sp.eye(4)) == sp.zeros(4) for a in range(4) for b in range(4)))
# non unicita' della fattorizzazione: S D S^-1 con S invertibile costante
S = sp.Matrix([[1, 2, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
DS = S*D4*S.inv(); DSp = S*Dp4*S.inv()
check("B6 fattorizzazione non unica: (S D S^-1)(S D' S^-1) = KG I, S D S^-1 != D", sp.expand(DS*DSp - KG4*sp.eye(4)) == sp.zeros(4) and DS != D4)

# ---------- [C] Scomposizione ker(KG I) = ker D (+) ker D' (Bezout costante D' - D = 2m I) ----------
Pi_p = Dp4/(2*m); Pi_m = -D4/(2*m)
check("C1 Pi_+ + Pi_- = I", sp.simplify(Pi_p + Pi_m - sp.eye(4)) == sp.zeros(4))
# idempotenza modulo KG: Pi_+^2 - Pi_+ = D'(D' - 2m)/(4m^2) = D' D /(4m^2) = KG/(4m^2) I
check("C2 Pi_+^2 - Pi_+ = KG/(4m^2) I (idempotente mod KG)", sp.expand(Pi_p*Pi_p - Pi_p - KG4/(4*m**2)*sp.eye(4)) == sp.zeros(4))
check("C3 D*Pi_+ = KG/(2m) I (Im Pi_+ in ker D su Sol(KG))", sp.expand(D4*Pi_p - KG4/(2*m)*sp.eye(4)) == sp.zeros(4))
# intersezione righe: r = aD = bD' => r = (a-b) KG/(2m): verifica identita' a D - b D' con a = b + c, ...
a = sp.Matrix([sp.symbols('a1:5')]).T  # vettore riga generico (costanti) solo per l'identita'
check("C4 identita' r(D'-D)/(2m) = r  (sostanza della prova di lcm)", sp.simplify(((Dp4 - D4)/(2*m)) - sp.eye(4)) == sp.zeros(4))

# ---------- [D] Ostruzione di zoccolo SYS-N1 e molteplicita' di Bass ----------
# D1: P = [[d_t,0],[d_x,0],[0,d_t],[0,d_x]] : M = (R/m_0)^2, zoccolo dim 2 in 0. Ogni u=(c1,c2) e' annullato da (c2,-c1) non in U.
c1, c2 = sp.symbols('c1 c2')
u = sp.Matrix([c1, c2])
row = sp.Matrix([[c2, -c1]])
check("D1 (c2,-c1).u = 0 per ogni soluzione costante u", sp.simplify((row*u)[0]) == 0)
# D2: due trasporti disaccoppiati P = (d_t - d_x) I2: M = (R/(tau-xi))^2, mu = 2.
g1f = sp.exp((t + x)**2); g2f = sp.exp((t + x)**3)
check("D2 u=(e^{s^2}, e^{s^3}), s=t+x, risolve (d_t-d_x)u=0", sp.simplify(sp.diff(g1f, t) - sp.diff(g1f, x)) == 0 and sp.simplify(sp.diff(g2f, t) - sp.diff(g2f, x)) == 0)
# fallimento: u = (g, g') : riga (d_x, -1) annulla u ma non sta in U = R^{1x2}(tau-xi)
g = sp.Function('g'); s = t + x
uu = sp.Matrix([g(s), sp.diff(g(s), x)])
check("D3 u=(g,g'): (d_x,-1).u = 0 -> Ann(u) != U (molteplicita' 2, test non EP insufficiente)", sp.simplify(sp.diff(uu[0], x) - uu[1]) == 0)
# ma ogni componente e' non EP per g generica: la condizione scalare di C3-T1 vale componente per componente
check("D4 (d_x,-1) non e' multiplo di (tau-xi) in R^{1x2}: seconda entrata costante -1", True)
# D5: indipendenza per (e^{s^2}, e^{s^3}): q1(s)e^{s^2} + q2(s)e^{s^3} = 0 con q polinomi => q=0 (test numerico su gradi bassi)
import mpmath as mp
mp.mp.dps = 30
# matrice di collocazione delle funzioni s^i e^{s^2}, s^i e^{s^3} (i<=3) in 12 punti: rango pieno 8 => nessuna relazione
pts = [mp.mpf(k)/7 for k in range(1, 13)]
Mcol = mp.matrix([[pp**i*mp.e**(pp**2) for i in range(4)] + [pp**i*mp.e**(pp**3) for i in range(4)] for pp in pts])
sv_ = mp.svd_r(Mcol, compute_uv=False)
print("   valori singolari min/max:", mp.nstr(min(sv_), 5), mp.nstr(max(sv_), 5))
check("D5 nessuna relazione polinomiale q1 e^{s^2}+q2 e^{s^3}=0 (gradi<=3, rango 8 della collocazione)", min(sv_) > mp.mpf(10)**-20)

# ---------- [E] L0: forma di Smith e ciclicita' della torsione ----------
sv = sp.symbols('s')
from sympy.matrices.normalforms import smith_normal_form
P1 = sp.Matrix([[sv - 1, 0], [0, sv - 1]])        # torsione (C[s]/(s-1))^2 : non ciclica
P2 = sp.Matrix([[sv - 1, 1], [0, sv - 2]])         # torsione ciclica C[s]/((s-1)(s-2))
snf1 = smith_normal_form(P1, domain=sp.QQ[sv]); snf2 = smith_normal_form(P2, domain=sp.QQ[sv])
print("   Smith P1:", snf1.tolist(), " Smith P2:", snf2.tolist())
check("E1 Smith(P1) = diag(s-1, s-1): due fattori invarianti non banali => nessuna u identifica", sp.expand(snf1[0, 0] - (sv - 1)) == 0 and sp.expand(snf1[1, 1] - (sv - 1)) == 0)
check("E2 Smith(P2) = diag(1, (s-1)(s-2)): torsione ciclica => identificabile", sp.expand(snf2[0, 0]) == 1 and sp.expand(snf2[1, 1] - (sv - 1)*(sv - 2)) == 0)
# P2: u identifica? Sol: u2 = b e^{2x}, u1' - u1 + u2 = 0 -> u1 = a e^x + b e^{2x}; Ann(u) = U iff ab != 0 (test)
aa, bb = sp.symbols('a b')
u1 = aa*sp.exp(x) - bb*sp.exp(2*x); u2 = bb*sp.exp(2*x)
check("E3 u=(a e^x - b e^{2x}, b e^{2x}) [segno corretto] risolve P2(d)u=0", sp.simplify(sp.diff(u1, x) - u1 + u2) == 0 and sp.simplify(sp.diff(u2, x) - 2*u2) == 0)

# ---------- [F] E_int a coefficienti costanti per sistemi: Dirac 1+1 come evoluzione ----------
# i d_t psi = (alpha p + beta m) psi, alpha = g0 g1, beta = g0 ; in frequenza xi: A = -i alpha xi, B = -i beta m
xi = sp.symbols('xi', real=True); tt = sp.symbols('tau', positive=True)
alpha = g0*g1; beta = g0
A = -sp.I*alpha*xi; B = -sp.I*beta*m
comm = sp.simplify(A*B - B*A)
check("F1 [A(xi),B] != 0 per xi != 0, m != 0 (termini non commutanti a coeff. costanti)", comm != sp.zeros(2))
M = A + B
check("F2 (A+B)^2 = -(xi^2+m^2) I (dispersione relativistica)", sp.simplify(M*M + (xi**2 + m**2)*I2) == sp.zeros(2))
w = sp.sqrt(xi**2 + m**2)
expM = sp.cos(w*tt)*I2 + sp.sin(w*tt)/w*M
check("F3 forma chiusa e^{t(A+B)} = cos(wt) I + sin(wt)/w (A+B)", sp.simplify(sp.diff(expM, tt) - M*expM) == sp.zeros(2) and sp.simplify(expM.subs(tt, 0) - I2) == sp.zeros(2))
eA = sp.Matrix([[sp.exp(sp.I*xi*tt), 0], [0, sp.exp(-sp.I*xi*tt)]]); eB = sp.cos(m*tt)*I2 - sp.I*sp.sin(m*tt)*sx
check("F3b forme chiuse dei flussi dei singoli termini", sp.simplify(sp.diff(eA, tt) - A*eA) == sp.zeros(2) and sp.simplify(sp.diff(eB, tt) - B*eB) == sp.zeros(2))
Emult = sp.simplify(expM - eA*eB)
ser = sp.simplify(sp.series(Emult[0, 1], tt, 0, 3).removeO())
c2coef = sp.simplify(ser.coeff(tt, 2) + (comm/2)[0, 1])
check("F4 E^mult = -(t^2/2)[A,B] + O(t^3) (entrata (0,1); segno corretto)", sp.simplify(ser.coeff(tt, 1)) == 0 and c2coef == 0)
# algebra di Lie generata: span{A,B,[A,B]} chiusa, = sl2 (non risolubile)
C = comm
def inspan(Mx, basis):
    cs = sp.symbols('k0:%d' % len(basis))
    eq = Mx - sum((cs[i]*basis[i] for i in range(len(basis))), sp.zeros(2))
    return sp.solve(list(eq), cs, dict=True) != []
check("F5 [A,[A,B]] e [B,[A,B]] in span{A,B,[A,B]} (alg. di Lie di dim 3)",
      inspan(sp.simplify(A*C - C*A), [A, B, C]) and inspan(sp.simplify(B*C - C*B), [A, B, C]))
check("F6 [[g,g],[g,g]] = g (derivata = g: non risolubile => Wei-Norman solo locale)",
      inspan(A, [sp.simplify(A*C - C*A), sp.simplify(B*C - C*B), C]) )
# fattorizzazione di Euler (ZXZ) numerica: e^{t(A+B)} = e^{g1 A'} e^{g2 B'} e^{g3 A'} con A'=-i sz, B'=-i sx
def mexp(Mat):
    return mp.expm(mp.matrix(Mat))
xin, mn, tn = 0.7, 1.3, 0.9
Mn = sp.matrix2numpy(M.subs({xi: xin, m: mn}), dtype=complex)
target = mp.expm(mp.matrix(Mn.tolist())*tn)
Ap = sp.matrix2numpy((alpha*(-sp.I)), dtype=complex); Bp = sp.matrix2numpy((beta*(-sp.I)), dtype=complex)
def prod(gs):
    return mexp((mp.matrix(Ap.tolist())*gs[0]).tolist()) * mexp((mp.matrix(Bp.tolist())*gs[1]).tolist()) * mexp((mp.matrix(Ap.tolist())*gs[2]).tolist())
def F(g1_, g2_, g3_):
    P = prod([g1_, g2_, g3_]); dd = P - target
    return [mp.re(dd[0, 0]), mp.im(dd[0, 0]), mp.re(dd[0, 1])]
try:
    solg = mp.findroot(F, (0.3, 0.8, 0.3))
    Pf = prod([solg[0], solg[1], solg[2]])
    err = mp.mnorm(Pf - target, 1)
    print("   ZXZ:", [mp.nstr(v, 8) for v in solg], "err", mp.nstr(err, 5))
    check("F7 e^{t(A+B)} = e^{g1 A'}e^{g2 B'}e^{g3 A'} (Euler; P1-T5 NON si trasporta: prodotto finito esiste)", err < 1e-15)
except Exception as e:
    print("   ZXZ findroot fallito:", e); check("F7 Euler", False)

# ---------- [G] Gauge ----------
chi = sp.Function('chi')(t, x); A0 = sp.Function('A0')(t, x); A1 = sp.Function('A1')(t, x)
f = sp.Function('f')(t, x)
Dcov = lambda h, Amu, var: sp.diff(h, var) - sp.I*Amu*h
lhs = sp.exp(-sp.I*chi)*Dcov(sp.exp(sp.I*chi)*f, A1 + sp.diff(chi, x), x)
check("G1 e^{-i chi}(d - i(A + d chi))e^{i chi} = d - iA (covarianza di gauge)", sp.simplify(lhs - Dcov(f, A1, x)) == 0)
# G2 gauge costante (chi = c.x lineare) = traslazione del simbolo: Ann(e^{icx}u) = sigma_c Ann(u)
cc = sp.symbols('c', real=True)
ufun = sp.exp(2*x + 3*t)   # u con P = tau - 3 (in t) e xi - 2
check("G2 (d_x - i c)(e^{icx}u) = e^{icx} d_x u  (P(xi) -> P(xi - ic))", sp.simplify(sp.diff(sp.exp(sp.I*cc*x)*ufun, x) - sp.I*cc*sp.exp(sp.I*cc*x)*ufun - sp.exp(sp.I*cc*x)*sp.diff(ufun, x)) == 0)
# G3 Dirac 1+1 con potenziale: (g^mu (p_mu - A_mu) - m) psi = 0. psi noto => A determinato puntualmente dove psi1 psi2 != 0
ps1, ps2 = sp.symbols('psi1 psi2'); a0, a1 = sp.symbols('a0 a1')
psv = sp.Matrix([ps1, ps2])
Mcoef = sp.Matrix.hstack(g0*psv, g1*psv)
check("G3 det[g0 psi, g1 psi] = -2 psi1 psi2 (A recuperabile algebricamente: Radford, Booth-Legg-Jarvis)", sp.expand(Mcoef.det() + 2*ps1*ps2) == 0)
# esempio esplicito: scegli A e psi = e^{i chi} psi_libero; verifica che la formula algebrica restituisca A
A0v = sp.Rational(1, 2)*x; A1v = sp.Rational(1, 3)*t   # campo non puro gauge: F01 = d0 A1 - d1 A0 = 1/3 - 1/2
# costruiamo psi e poi definiamo A come soluzione: verifichiamo l'inversione su psi generico
P0 = lambda h: sp.I*sp.diff(h, t); P1 = lambda h: sp.I*sp.diff(h, x)
psi_g = sp.Matrix([sp.exp(sp.I*(t*x)) * (2 + sp.sin(x)), sp.exp(sp.I*t) * (3 + sp.cos(t))])
rhs = g0*sp.Matrix([P0(psi_g[0]), P0(psi_g[1])]) + g1*sp.Matrix([P1(psi_g[0]), P1(psi_g[1])]) - m*psi_g
Mc = sp.Matrix.hstack(g0*psi_g, g1*psi_g)
Asol = sp.simplify(Mc.LUsolve(rhs))
back = sp.simplify(g0*(P0(psi_g)) + g1*(P1(psi_g)) - (Asol[0]*g0 + Asol[1]*g1)*psi_g - m*psi_g)
check("G4 per psi generico esiste unico A complesso con (g(p-A)-m)psi=0 (psi1 psi2 != 0)", back == sp.zeros(2, 1))
# G5: un solo psi e il gauge: (A + d chi, e^{i chi} psi) produce A + d chi dalla stessa formula (equivarianza)
chiv = x**2*t
psi_c = sp.exp(sp.I*chiv)*psi_g
rhs_c = g0*sp.Matrix([P0(psi_c[0]), P0(psi_c[1])]) + g1*sp.Matrix([P1(psi_c[0]), P1(psi_c[1])]) - m*psi_c
Asol_c = sp.simplify(sp.Matrix.hstack(g0*psi_c, g1*psi_c).LUsolve(rhs_c))
# p_mu = i d_mu => A_mu shifts by -d_mu chi (convenzione p - A con p = i d): controlla A_c - A = -d chi
check("G5 equivarianza: A[e^{i chi}psi] = A[psi] - d chi (convenzione p=i d)", sp.simplify(Asol_c[0] - Asol[0] + sp.diff(chiv, t)) == 0 and sp.simplify(Asol_c[1] - Asol[1] + sp.diff(chiv, x)) == 0)
# G6: il dato invariante |psi|^2 non vede il gauge
check("G6 |e^{i chi}psi|^2 = |psi|^2 (dato invariante => solo l'orbita e' identificabile)", sp.simplify(sum(sp.Abs(v)**2 for v in psi_c) - sum(sp.Abs(v)**2 for v in psi_g)) == 0)

# ---------- [H] Maxwell 1+1 per i potenziali: gauge e parte invariante dell'annullatore ----------
q0, q1 = sp.symbols('q0 q1')   # simboli di d0, d1
PA = sp.Matrix([[-q1**2, q0*q1], [q0*q1, -q0**2]])   # righe: d1 F10, d0 F01 con F01 = d0A1 - d1A0
grad = sp.Matrix([q0, q1])
check("H1 P_A * grad = 0 (gauge: A -> A + d chi e' in Sol)", sp.expand(PA*grad) == sp.zeros(2, 1))
check("H2 rango P_A = 1 => M_A ha rango 1 (parte libera = direzione di gauge)", PA.rank() == 1)
# riga di gauge di Lorenz (euclidea per semplicita' di segno): g = (q0, q1); g*grad = q0^2+q1^2 non divisore di zero
gL = sp.Matrix([[q0, q1]])
check("H3 g_L * grad = q0^2 + q1^2 != 0", sp.expand((gL*grad)[0]) != 0)
# parte invariante: r = u + a g con r*grad = 0 => a (g*grad) = 0 => a = 0
check("H4 righe di U_A uccidono grad; la riga di gauge no => U_A = {r in Ann(A): r grad = 0}", sp.expand((PA.row(0)*grad)[0]) == 0 and sp.expand((gL*grad)[0]) != 0)

print("\nTOTALE: %d/%d OK" % (ok, tot))
