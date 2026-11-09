# F6-VAR — verifica SymPy (solo controllo). Caso non autonomo V(t,x).
# (a) errore di splitting non autonomo al 2o ordine: U - U1 U2 = int int_{s1>s2} [A2(s1), A1(s2)] + O(t^3)
# (b) termini che commutano a tempi uguali ma non a tempi diversi: E^mult != 0
# (c) oscillatore (sl2, rappresentazione metaplettica 2x2): decomposizione di Gauss (chirp*dilatazione*libera)
#     della rotazione esiste sse cos t != 0  -> P1-P5 (non risolubile => solo locale) in forma esplicita
# (d) Magnus: exp(Om1+Om2+Om3) = U + O(t^5) per il sistema di Airy y'' = t y
import sympy as sp

t, s, s1, s2, s3 = sp.symbols('t s s1 s2 s3', real=True)
ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1; r = bool(cond); ok += r
    print(('OK  ' if r else 'FAIL'), name)

N = 5  # ordine di troncamento
def dyson(A, order=N):
    # U(t) = I + int_0^t A(s) U(s) ds, iterazione di Picard troncata in t
    U = sp.eye(A(t).shape[0])
    for _ in range(order + 1):
        integrand = (A(s)*U.subs(t, s)).applyfunc(sp.expand)
        U = sp.eye(A(t).shape[0]) + integrand.applyfunc(lambda e: sp.integrate(e, (s, 0, t)))
        U = U.applyfunc(lambda e: sp.series(e, t, 0, order + 1).removeO())
    return U.applyfunc(sp.expand)

def trunc(M, order):
    return M.applyfunc(lambda e: sp.expand(sp.series(sp.expand(e), t, 0, order).removeO()))

X = sp.Matrix([[0, 1], [0, 0]]); Y = sp.Matrix([[0, 0], [1, 0]]); Z = sp.Matrix([[1, 0], [0, -1]])
A1 = lambda tt: (1 + tt)*X + tt**2*Z
A2 = lambda tt: (2 - 3*tt)*Y
A = lambda tt: A1(tt) + A2(tt)
U = dyson(A, 3); U1 = dyson(A1, 3); U2 = dyson(A2, 3)
lhs = trunc(U - U1*U2, 3)
comm = lambda P, Q: P*Q - Q*P
inner = comm(A2(s1), A1(s2)).applyfunc(lambda e: sp.integrate(sp.integrate(e, (s2, 0, s1)), (s1, 0, t)))
rhs = trunc(inner, 3)
check('(a) E^mult = int int_{s1>s2}[A2(s1),A1(s2)] + O(t^3)', sp.simplify(lhs - rhs) == sp.zeros(2))
# coefficiente di t^2: (1/2)[A2(0),A1(0)] come nel caso autonomo
c2 = lhs.applyfunc(lambda e: sp.expand(e).coeff(t, 2))
check('(a) coefficiente t^2 = (1/2)[A2(0),A1(0)]', sp.simplify(c2 - comm(A2(0), A1(0))/2) == sp.zeros(2))

# (b) f = 1 su [0,1/2], g = 1 su [1/2,1]: f g = 0 (commutano a tempi uguali); propagatori esatti a t = 1
expm = lambda M: sp.simplify(M.exp())
Uex = expm(Y/2)*expm(X/2)        # prima agisce X (tempi [0,1/2]), poi Y
U1U2 = expm(X/2)*expm(Y/2)       # U1(1) U2(1): flussi dei singoli termini
check('(b) commutano a tempi uguali ma E^mult(1) != 0', sp.simplify(Uex - U1U2) != sp.zeros(2))

# (c) rotazione R(t) = exp(t(X - Y)) = L(chirp) D(dilatazione) Ushear(libera)
Rt = sp.Matrix([[sp.cos(t), sp.sin(t)], [-sp.sin(t), sp.cos(t)]])
check('(c) exp(t(X-Y)) = rotazione', sp.simplify(expm(t*(X - Y)) - Rt) == sp.zeros(2))
a, d, b = sp.symbols('a d b')
Lm = sp.Matrix([[1, 0], [a, 1]]); Dm = sp.Matrix([[d, 0], [0, 1/d]]); Um = sp.Matrix([[1, b], [0, 1]])
# (L D U)_{11} = d: quindi d = cos t e' forzato; con a = -tan t, b = tan t si ottiene R(t)
prod = (Lm*Dm*Um).subs({a: -sp.tan(t), d: sp.cos(t), b: sp.tan(t)})
check('(c) LDU esplicita con d = cos t, a = -tan t, b = tan t (valida sse cos t != 0)', sp.simplify(prod - Rt) == sp.zeros(2))
check('(c) (LDU)_11 = d (d = cos t forzato)', sp.simplify((Lm*Dm*Um)[0, 0] - d) == 0)
Rpi2 = Rt.subs(t, sp.pi/2)
check('(c) a t = pi/2 nessuna LDU', sp.solve(list(Lm*Dm*Um - Rpi2), [a, d, b], dict=True) == [])

# (d) Magnus per y'' = t y : Y' = A(t) Y, A = [[0,1],[t,0]]
Aa = lambda tt: sp.Matrix([[0, 1], [tt, 0]])
Ua = dyson(Aa, 5)
Om1 = Aa(s).applyfunc(lambda e: sp.integrate(e, (s, 0, t)))
Om2 = (comm(Aa(s1), Aa(s2))/2).applyfunc(lambda e: sp.integrate(sp.integrate(e, (s2, 0, s1)), (s1, 0, t)))
T3 = (comm(Aa(s1), comm(Aa(s2), Aa(s3))) + comm(Aa(s3), comm(Aa(s2), Aa(s1))))/6
Om3 = T3.applyfunc(lambda e: sp.integrate(sp.integrate(sp.integrate(e, (s3, 0, s2)), (s2, 0, s1)), (s1, 0, t)))
Om = Om1 + Om2 + Om3
E = sp.eye(2); P = sp.eye(2)
for k in range(1, 6):
    P = (P*Om)/k
    E = E + P
diffM = trunc(E - Ua, 5)
check('(d) Magnus Om1+Om2+Om3 riproduce il propagatore di Airy fino a O(t^5)', diffM == sp.zeros(2))
print(f'{ok}/{tot} OK')
