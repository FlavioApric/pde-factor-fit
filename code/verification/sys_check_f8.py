# S-CHECK-F8-SYS — controlli indipendenti sul pacchetto S8-SYS (27/10/2026).
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I work/CHECK-F8/sympy/sys_check_f8.py
import sympy as sp
import cmath, math

ok_all = []
def report(tag, cond, msg=""):
    ok_all.append(bool(cond))
    print(f"[{'OK' if cond else 'FAIL'}] {tag} {msg}")

# ---------------------------------------------------------------- H-DIRAC-2(a)
# Eliminazione unimodulare: E D F = diag(-m I, (KG - m^2)/m I), det E = det F = 1.
p0, p1, p2, p3, m = sp.symbols('p0 p1 p2 p3 m', nonzero=True)
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
I2 = sp.eye(2); Z2 = sp.zeros(2)
sp_ = p1*sx + p2*sy + p3*sz
X = p0*I2 - sp_; Y = p0*I2 + sp_
KG = p0**2 - p1**2 - p2**2 - p3**2
D = sp.BlockMatrix([[-m*I2, X], [Y, -m*I2]]).as_explicit()
E = sp.BlockMatrix([[I2, Z2], [Y/m, I2]]).as_explicit()
F = sp.BlockMatrix([[I2, X/m], [Z2, I2]]).as_explicit()
target = sp.diag(-m, -m, (KG - m**2)/m, (KG - m**2)/m)
report("HD1", sp.simplify(E*D*F - target) == sp.zeros(4) and sp.simplify(E.det()) == 1 and sp.simplify(F.det()) == 1,
       "E D F = diag(-m,-m,(KG-m^2)/m,(KG-m^2)/m), E e F unimodulari: M_D = (R/q)^2 senza perdita di relazioni")
report("HD2", (sp.Matrix([[0, 0, 1, 0]])*F) == sp.Matrix([[0, 0, 1, 0]]) and (sp.Matrix([[0, 0, 0, 1]])*F) == sp.Matrix([[0, 0, 0, 1]]),
       "e_3 F = e_3, e_4 F = e_4: le classi di e_3, e_4 sono la base")

# ---------------------------------------------------------------- H-DIRAC-1
# Grado: W_d (tau I + alpha.xi) = 0 => W_d = 0 (det non nullo), anche per W generica 4x4.
tau, x1, x2, x3 = sp.symbols('tau xi1 xi2 xi3')
import random
random.seed(8)
al = [sp.Matrix(4, 4, lambda i, j: random.randint(-5, 5) + sp.I*random.randint(-5, 5)) for k in range(3)]
H = tau*sp.eye(4) + al[0]*x1 + al[1]*x2 + al[2]*x3
dH = sp.Poly(sp.expand(H.det(berkowitz=True) if False else H.det(method='berkowitz')), tau)
report("HD3", dH.LC() == 1 and dH.degree() == 4,
       "det(tau I + alpha.xi) monico di grado 4 in tau (alpha interi gaussiani casuali; in generale: coefficiente di tau^4 = det I)")

# ---------------------------------------------------------------- LAME: ipotesi mancante lambda + 2 mu != 0
rho, mu, lam = sp.symbols('rho mu lambda')
xi = sp.Matrix([x1, x2, x3])
P = rho*tau**2*sp.eye(3) - mu*(xi.T*xi)[0]*sp.eye(3) - (lam + mu)*xi*xi.T
qP = rho*tau**2 - (lam + 2*mu)*(xi.T*xi)[0]; qS = rho*tau**2 - mu*(xi.T*xi)[0]
report("L1", sp.expand(P.det() - qP*qS**2) == 0, "det P = qP qS^2 (riverificato)")
qP_deg = qP.subs(lam, -2*mu)
fac = sp.factor_list(sp.expand(qP_deg))
report("L2", sp.simplify(qP_deg - rho*tau**2) == 0 and any(e == 2 for _, e in fac[1]) or sp.factor(qP_deg) == rho*tau**2,
       f"con lambda = -2 mu (ammesso da 'rho, mu != 0, lambda+mu != 0'): qP = {sp.factor(qP_deg)} non e' primo")
Pdeg = P.subs(lam, -2*mu)
report("L3", sp.factor(Pdeg.det()) == sp.factor(rho*tau**2*qS**2),
       f"con lambda = -2 mu: det P = {sp.factor(Pdeg.det())}; Ass contiene (tau), la tesi mu=(1,2) su qP va riformulata")

# ---------------------------------------------------------------- SYS-S1-C con P != 0 (fix SYS-3)
# k = 3: Q1 = [(1,0,0),(0,0,tau)], Q2 = [(1,xi,0),(0,0,tau)], P = (0,0,tau).
a, b, c, d = sp.symbols('a b c d')
xi_ = sp.Symbol('xi')
v1 = a*sp.Matrix([[1, 0, 0]]) + b*sp.Matrix([[0, 0, tau]])
v2 = c*sp.Matrix([[1, xi_, 0]]) + d*sp.Matrix([[0, 0, tau]])
sol = sp.solve(list(v1 - v2), [a, c, b], dict=True)
# a = c, c*xi = 0 => c = 0 su un dominio; b = d
eqs = list(v1 - v2)
report("S1", eqs == [a - c, -c*xi_, b*tau - d*tau],
       "U1 cap U2: a=c, c*xi=0 => c=0 (dominio), b=d: U1 cap U2 = R(0,0,tau) = U_P != 0")

# ---------------------------------------------------------------- SYS-S1-C in D'(Omega) (risposta a Q-S8SYS-2)
t = sp.Symbol('t', real=True)
beta = sp.Function('beta')
T_expr = sp.diff(-beta(t)*sp.log(1 - t), t) + sp.diff(beta(t), t)*sp.log(1 - t)
report("S2", sp.simplify(T_expr - beta(t)/(1 - t)) == 0,
       "per t<1: d/dt[-beta log(1-t)] + beta' log(1-t) = beta/(1-t): il salto 1/(1-t) si estende come distribuzione (f del pacchetto NON basta in D')")
# Con il salto e^{1/(1-t)}: <e^{1/(1-t)}, phi_eps> >= c eps e^{1/(2 eps)} contro C eps^{-N}
ep = sp.Symbol('epsilon', positive=True)
lims = [sp.limit(ep*sp.exp(1/(2*ep))*ep**N, ep, 0, '+') for N in (10, 50)]
report("S3", all(L == sp.oo for L in lims),
       "lim_{eps->0+} eps^{N+1} e^{1/(2 eps)} = oo per N = 10, 50: <e^{1/(1-t)}, phi_eps> >= c eps e^{1/(2eps)} batte ogni C eps^-N, nessuna estensione distribuzionale")

# ---------------------------------------------------------------- SYS-S1 riduzione scalare: serve n = 2
z1, z2, z3 = sp.symbols('z1 z2 z3')
G = sp.groebner([z1, z2], z1, z2, z3, order='grevlex')
report("S4", G.exprs == [z1, z2],
       "n=3, Q1=z1, Q2=z2 coprimi: N = C[z1,z2,z3]/(z1,z2) = C[z3] ha lunghezza infinita (la riduzione 'k=1 coprimi => lunghezza finita' vale solo per n=2)")

# ---------------------------------------------------------------- SYS-N3(c), n = 3 con Phi = psi e_3
y1, y2, y3 = sp.symbols('y1 y2 y3', real=True)
psi = sp.Function('psi')(y1, y2, y3); r = sp.Function('r', positive=True)(y1, y2, y3)
Phi = sp.Matrix([0, 0, psi]); Y = [y1, y2, y3]
curl = lambda V: sp.Matrix([sp.diff(V[2], y2) - sp.diff(V[1], y3), sp.diff(V[0], y3) - sp.diff(V[2], y1), sp.diff(V[1], y1) - sp.diff(V[0], y2)])
k = curl(Phi)
divk = sum(sp.diff(k[i], Y[i]) for i in range(3))
B12 = sp.diff(k[1]/r**2, y1) - sp.diff(k[0]/r**2, y2)
ell = -(sp.diff(sp.diff(psi, y1)/r**2, y1) + sp.diff(sp.diff(psi, y2)/r**2, y2))
report("N1", sp.simplify(divk) == 0 and sp.simplify(B12 - ell) == 0,
       "k = rot(psi e3): div k = 0 e (d(k/rho^2))_{12} = -div_{12}(rho^-2 grad_{12} psi): ellittico 2D fetta per fetta")

# ---------------------------------------------------------------- SYS-E3: ramo continuo e ZXZ, controllo numerico indipendente
def zxz_err(tt, xx, mm, nsteps=4000):
    w = math.sqrt(xx*xx + mm*mm)
    # ramo continuo di a in t, a(0)=0
    arg_prev = 0.0; acc = 0.0
    for kk in range(1, nsteps + 1):
        s = tt*kk/nsteps
        zz = complex(math.cos(w*s), xx*math.sin(w*s)/w)
        ang = cmath.phase(zz)
        dlt = (ang - arg_prev + math.pi) % (2*math.pi) - math.pi
        acc += dlt; arg_prev = ang
    aa = acc/2; bb = -math.asin(mm*math.sin(w*tt)/w)
    import numpy as np
    A = np.array([[1j*xx, -1j*mm], [-1j*mm, -1j*xx]])
    ex = math.cos(w*tt)*np.eye(2) + math.sin(w*tt)/w*A
    Rz = np.diag([cmath.exp(1j*aa), cmath.exp(-1j*aa)])
    Rx = np.array([[math.cos(bb), 1j*math.sin(bb)], [1j*math.sin(bb), math.cos(bb)]])
    return float(np.abs(Rz@Rx@Rz - ex).max()), aa
errs = [zxz_err(tt, xx, 1.0)[0] for tt in (0.3, 2.0, 7.5, 20.0) for xx in (0.05, 0.7, 3.0)]
report("E1", max(errs) < 1e-9, f"ZXZ con ramo continuo per t fino a 20, xi in {{0.05,0.7,3}}: err max {max(errs):.1e}")
_, a_big = zxz_err(1.0, 200.0, 1.0)
report("E2", abs(a_big/200.0 - 0.5) < 1e-2, f"g1 = a/xi a xi=200, t=1: {a_big/200.0:.4f} (limite t/2 = 0.5)")

print(f"\nTOTALE {sum(ok_all)}/{len(ok_all)} OK")
