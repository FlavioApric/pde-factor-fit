"""PR-C2c / scheda C2.33 (trave di Euler-Bernoulli, caso 1D) -- verifiche SymPy.
T = d_t^2 + c^2 d_x^4  (c^2 = EI/(rho A)).
"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
c, beta, Lb = sp.symbols('c beta L', positive=True)
tau, xi = sp.symbols('tau xi')

def EB(u):
    return sp.diff(u, t, 2) + c**2*sp.diff(u, x, 4)

# [E1] simbolo e fattorizzazione
P = tau**2 + c**2*xi**4
P1 = tau - sp.I*c*xi**2; P2 = tau + sp.I*c*xi**2
print('[E1a] P - P1*P2 =', sp.expand(P - P1*P2))
print('[E1b] V(P1) cap V(P2):', sp.solve([P1, P2], [tau, xi], dict=True))
u = sp.Function('u')(x, t)
S1 = lambda g: sp.diff(g, t) - sp.I*c*sp.diff(g, x, 2)
S2 = lambda g: sp.diff(g, t) + sp.I*c*sp.diff(g, x, 2)
print('[E1c] S1 S2 u - EB(u) =', sp.simplify(S1(S2(u)) - EB(u)), ';  [S1,S2]u =', sp.simplify(S1(S2(u)) - S2(S1(u))))
# ker(S1) cap ker(S2) = {d_t u = 0, d_x^2 u = 0} = span{1, x}: dimensione 2 (verifica G2 di NOTAZIONE)
a0, a1 = sp.symbols('a0 a1')
w = a0 + a1*x
print('[E1d] S1(a0+a1 x)=', S1(w), ' S2(a0+a1 x)=', S2(w))
# proiettori espliciti: per u in ker EB, u+ = (S2 u)/(2 i c d_x^2)... a livello di simbolo u^ = u+^ + u-^ con
#   u+^ = (tau + i c xi^2)/(2 i c xi^2) u^  su V(P1) ecc.; qui verifichiamo sui modi esponenziali:
kk = sp.symbols('kappa', real=True)
up = sp.exp(sp.I*kk*x - sp.I*c*kk**2*t)   # in ker S1 ?  S1 = d_t - i c d_x^2 -> -i c k^2 + i c k^2 = 0
um = sp.exp(sp.I*kk*x + sp.I*c*kk**2*t)
print('[E1e] S1(e+) =', sp.simplify(S1(up)), ' S2(e-) =', sp.simplify(S2(um)), ' EB(e+ + e-) =', sp.simplify(EB(up + um)))

# [E2] modi separati: X'''' = beta^4 X ; T'' + c^2 beta^4 T = 0 ; omega = c beta^2
basis = [sp.cos(beta*x), sp.sin(beta*x), sp.cosh(beta*x), sp.sinh(beta*x)]
print('[E2a] X\'\'\'\' - beta^4 X per la base:', [sp.simplify(sp.diff(b, x, 4) - beta**4*b) for b in basis])
W = sp.Matrix([[sp.diff(b, x, i) for b in basis] for i in range(4)])
print('[E2b] Wronskiano =', sp.simplify(W.det()))
om = c*beta**2
print('[E2c] EB(X(x) cos(omega t)) =', [sp.simplify(EB(b*sp.cos(om*t))) for b in basis])

# [E3] condizioni al bordo -> equazioni di frequenza
# appoggiata-appoggiata: X = X'' = 0 in 0, L
n = sp.symbols('n', integer=True, positive=True)
Xs = sp.sin(n*sp.pi*x/Lb)
print('[E3a] SS: X(0),X\'\'(0),X(L),X\'\'(L) =', [sp.simplify(e) for e in (Xs.subs(x, 0), sp.diff(Xs, x, 2).subs(x, 0), Xs.subs(x, Lb), sp.diff(Xs, x, 2).subs(x, Lb))])
# incastro-libero (mensola): X(0)=X'(0)=0, X''(L)=X'''(L)=0 -> det = 0 <=> 1 + cos(bL) cosh(bL) = 0
C = sp.symbols('C1:5')
X = sum(Ci*b for Ci, b in zip(C, basis))
eqs = [X.subs(x, 0), sp.diff(X, x).subs(x, 0), sp.diff(X, x, 2).subs(x, Lb), sp.diff(X, x, 3).subs(x, Lb)]
Mcl = sp.Matrix([[sp.diff(e, Ci) for Ci in C] for e in eqs])
dcl = sp.simplify(Mcl.det())
print('[E3b] mensola: det =', sp.factor(sp.simplify(dcl.rewrite(sp.exp)).rewrite(sp.cos)))
print('      det / (2 beta^6 (1+cos cosh)) =', sp.simplify((dcl/(2*beta**6*(1 + sp.cos(beta*Lb)*sp.cosh(beta*Lb)))).rewrite(sp.exp)))
bl = sp.nsolve(1 + sp.cos(x)*sp.cosh(x), x, 1.9)
print('      prima radice beta L =', sp.N(bl, 12), '(atteso 1.87510407)')
# libera-libera: det -> 1 - cos cosh = 0 (piu' 2 modi rigidi {1, x}: beta=0)
eqsff = [sp.diff(X, x, 2).subs(x, 0), sp.diff(X, x, 3).subs(x, 0), sp.diff(X, x, 2).subs(x, Lb), sp.diff(X, x, 3).subs(x, Lb)]
Mff = sp.Matrix([[sp.diff(e, Ci) for Ci in C] for e in eqsff])
print('      libera-libera: det / (1 - cos cosh) =', sp.simplify((Mff.det()/(1 - sp.cos(beta*Lb)*sp.cosh(beta*Lb))).rewrite(sp.exp)))

# [E4] nucleo fondamentale (spostamento iniziale delta, velocita' nulla), t>0:
#  G(x,t) = (8 pi c t)^(-1/2) [cos(x^2/(4ct)) + sin(x^2/(4ct))]  = Re-media dei due propagatori di Schrodinger
tp = sp.symbols('t', positive=True)
G = (8*sp.pi*c*tp)**sp.Rational(-1, 2)*(sp.cos(x**2/(4*c*tp)) + sp.sin(x**2/(4*c*tp)))
print('[E4a] EB(G) =', sp.simplify(sp.diff(G, tp, 2) + c**2*sp.diff(G, x, 4)))
Kp = (4*sp.pi*sp.I*c*tp)**sp.Rational(-1, 2)*sp.exp(sp.I*x**2/(4*c*tp))   # nucleo di e^{i c t d_x^2}
Km = sp.conjugate(Kp)
print('[E4b] S1(K+) =', sp.simplify(sp.diff(Kp, tp) - sp.I*c*sp.diff(Kp, x, 2)))
print('[E4c] G - (K+ + K-)/2 (numerico, x=0.7,t=0.3,c=1.3):', sp.N((G - (Kp + Km)/2).subs({x: 0.7, tp: 0.3, c: 1.3})))
print('[E4d] int G dx =', sp.simplify(sp.integrate(G.subs({c: 1, tp: 1}), (x, -sp.oo, sp.oo))), '(massa 1: G(.,t) -> delta)')

# [E5] relazione di dispersione e velocita' di gruppo
k = sp.symbols('k', positive=True)
w = c*k**2
print('[E5] omega =', w, '; v_fase =', sp.simplify(w/k), '; v_gruppo =', sp.diff(w, k), ' (= 2 v_fase: dispersione "anomala", Schrodinger-like)')

# [E6] Timoshenko (una equazione, sezione uniforme), w = e^{i(kx - Omega t)}:
#  E I w_xxxx + rho A w_tt - rho I (1 + E/(kG)) w_xxtt + rho^2 I/(kG) w_tttt = 0
rho, I_, A_, E_, kG = sp.symbols('rho I A E kG', positive=True)
W = sp.symbols('W')  # W = Omega^2
dispT = E_*I_*k**4 - rho*A_*W - rho*I_*(1 + E_/kG)*k**2*W + rho**2*I_/kG*W**2
disc = sp.discriminant(dispT, W)
print('[E6a] Timoshenko: quadratica in Omega^2; discriminante =', sp.factor(disc))
print('      discriminante - [ (rhoA + rhoI(1+E/kG)k^2)^2 - 4 rho^2 I^2 E k^4/kG ] =', sp.simplify(disc - ((rho*A_ + rho*I_*(1 + E_/kG)*k**2)**2 - 4*rho**2*I_**2*E_*k**4/kG)))
# limite I-> 0 (rotary inertia e taglio trascurati) => ramo flessionale Omega^2 -> (EI/(rho A)) k^4
Wsol = sp.solve(dispT, W)
low = [ws for ws in Wsol]
print('[E6b] ramo basso / (EI k^4/(rho A)) per k->0:', [sp.limit(ws/(E_*I_*k**4/(rho*A_)), k, 0) for ws in low])
