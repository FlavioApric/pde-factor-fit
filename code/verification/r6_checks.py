# R6 - verifiche SymPy (Idea II). Eseguire: D:\ProblemaBase\.venv\Scripts\python.exe -I r6_checks.py
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
x, s, tau, xi, lam = sp.symbols('x s tau xi lambda')
D = lambda f, k: sp.diff(f, x, k)

def companion(coeffs):  # p = s^m + a_{m-1}s^{m-1}+...+a_0 ; coeffs=[a0..a_{m-1}]
    m = len(coeffs); C = sp.zeros(m)
    for i in range(m - 1): C[i, i + 1] = 1
    for j in range(m): C[m - 1, j] = -coeffs[j]
    return C

print("== CHECK 1: Smith form di sI-C(p) = diag(1,..,1,p) (via b: invariante completo) ==")
C = companion([2, -1, -2])  # p = s^3-2s^2-s+2 (coeffs a0..a2 = 2,-1,-2) = (s-1)(s+1)(s-2)
print(smith_normal_form(s * sp.eye(3) - C, domain=sp.QQ[s]))
a = sp.symbols('a0:3'); M = s * sp.eye(3) - companion(list(a))
print("det(sI-C_generico) =", sp.expand(M.det()))
minors2 = [M.extract([i, j], [k, l]).det() for i in range(3) for j in range(i + 1, 3) for k in range(3) for l in range(k + 1, 3)]
print("esiste minore 2x2 = +-1 (=> fattori invarianti 1,1,p su ogni anello commutativo):", any(sp.expand(m_**2 - 1) == 0 for m_ in minors2))

print("\n== CHECK 2: e^{xC}: prima riga = base di ker p(D), radici multiple (Jordan) ==")
C2 = companion([-4, 8, -5])  # p = s^3-5s^2+8s-4 = (s-1)(s-2)^2
Pj, Jj = C2.jordan_form()
def expJ(J):
    n=J.shape[0]; N=J-sp.diag(*[J[i,i] for i in range(n)]); E_=sp.zeros(n)
    for i in range(n):
        for j in range(n):
            E_[i,j]=sp.exp(J[i,i]*x)*sum((x**k/sp.factorial(k))*(N**k)[i,j] for k in range(n))
    return E_
E = sp.expand(Pj*expJ(Jj)*Pj.inv())
print('dE/dx - C E = 0:', sp.simplify(E.diff(x)-C2*E)==sp.zeros(3), ' E(0)=I:', sp.simplify(E.subs(x,0)-sp.eye(3))==sp.zeros(3)); row = [sp.expand(r) for r in E[0, :]]
print("prima riga e^{xC}:", row)
print("p(D) su ciascuna:", [sp.simplify(D(r, 3) - 5 * D(r, 2) + 8 * D(r, 1) - 4 * r) for r in row])
print("Jordan di C:", C2.jordan_form()[1], "(non derogatoria: un blocco per autovalore)")

print("\n== CHECK 3: proiettori spettrali di C (Hermite) e split di u, E_int=0 ==")
def proj(Cm, ev, allev):
    qa = sp.prod([(s - e)**m for e, m in allev.items() if e != ev])
    r = sp.invert(qa, (s - ev)**allev[ev], s); q = sp.Poly(sp.expand(r * qa), s)
    return sum((q.coeff_monomial(s**k) * Cm**k for k in range(q.degree() + 1)), sp.zeros(Cm.shape[0]))
ev = {1: 1, 2: 2}; P1 = proj(C2, 1, ev); P2 = proj(C2, 2, ev)
print("P1+P2=I:", sp.simplify(P1 + P2 - sp.eye(3)) == sp.zeros(3), " P1P2=0:", sp.simplify(P1 * P2) == sp.zeros(3), " P1^2=P1:", sp.simplify(P1 * P1 - P1) == sp.zeros(3))
Y0 = sp.Matrix(sp.symbols('y0:3')); u = (E * Y0)[0]
u1 = sp.expand((E * P1 * Y0)[0]); u2 = sp.expand((E * P2 * Y0)[0])
print("u1 =", u1); print("u2 =", u2); print("u-u1-u2 =", sp.simplify(u - u1 - u2))
print("(D-1)u1 =", sp.simplify(D(u1, 1) - u1), " (D-2)^2u2 =", sp.simplify(D(u2, 2) - 4 * D(u2, 1) + 4 * u2))

print("\n== CHECK 4: Gram del jet: rango = ordine annullatore minimo; ker = multipli di p ==")
uu = sp.exp(x) + x * sp.exp(2 * x); Mo = 5
jet = [D(uu, k) for k in range(Mo + 1)]
# Gram = B^T Gb B con B = coordinate del jet nella base (e^x, e^{2x}, x e^{2x}) e Gb>0 (Gram della base, def. pos.)
# => rank Gram = rank B, ker Gram = ker B (esatto, senza integrali trascendenti)
basis = [sp.exp(x), sp.exp(2 * x), x * sp.exp(2 * x)]
cs = sp.symbols('k0:3')
B = sp.zeros(3, Mo + 1)
for k in range(Mo + 1):
    eqs = [sp.expand(jet[k] - sum(cs[i] * basis[i] for i in range(3))).subs(x, xv) for xv in [0, 1, 2]]
    sol = sp.solve(eqs, cs, dict=True)[0]
    for i in range(3): B[i, k] = sp.nsimplify(sp.simplify(sol[cs[i]]))
print("controllo ricostruzione jet:", all(sp.simplify(jet[k] - sum(B[i, k] * basis[i] for i in range(3))) == 0 for k in range(Mo + 1)))
print("rank Gram(jet ord 5) = rank B =", B.rank())
ker = B.nullspace(); print("dim ker =", len(ker))
p = sp.expand((s - 1) * (s - 2)**2)
for v in ker:
    poly = sum(sp.simplify(v[k]) * s**k for k in range(Mo + 1)); print("  rem(poly del ker, p) =", sp.simplify(sp.rem(sp.expand(poly), p, s)))
W = sp.Matrix(3, 3, lambda i, j: D(uu, i + j)); print("det Hankel-Wronski 3x3 != 0:", sp.simplify(W.det()) != 0)
W4 = sp.Matrix(4, 4, lambda i, j: D(uu, i + j)); print("det Hankel-Wronski 4x4 =", sp.simplify(W4.det()))
# D sul jet: nella base (u,u',u'') la derivata ha matrice compagna (trasposta)
print("u''' - (5u''-8u'+4u) =", sp.simplify(D(uu, 3) - (5 * D(uu, 2) - 8 * D(uu, 1) + 4 * uu)))

print("\n== CHECK 5: gauge Y=GZ cambia il pol. caratteristico (coeff. variabili) ==")
a0f = sp.Function('a0')(x); a1f = sp.Function('a1')(x)
A = sp.Matrix([[0, 1], [-a0f, -a1f]]); Gm = sp.Matrix([[1, 0], [x, 1]])
A2 = sp.simplify(Gm.inv() * A * Gm - Gm.inv() * Gm.diff(x))
print("A' =", A2)
print("charpoly A :", sp.factor(A.charpoly(lam).as_expr())); print("charpoly A':", sp.factor(A2.charpoly(lam).as_expr()))
Gd = sp.diag(1, sp.exp(x)); A3 = sp.simplify(Gd.inv() * A * Gd - Gd.inv() * Gd.diff(x))
print("gauge diag(1,e^x): tr A3 - tr A =", sp.simplify(A3.trace() - A.trace()), "(= -(log det G)')")
f = sp.Function('f')(x)
print("similitudine di Ore: (d-1/x)(x f) - x (d f) =", sp.simplify(sp.diff(x * f, x) - f - x * sp.diff(f, x)))

print("\n== CHECK 6: Jacobson/ciclicita: sistema y1'=y2, y2'=a y1+b y2 -> diag(1,L) ==")
y1 = sp.Function('y1')(x); af = sp.Function('a')(x); bf = sp.Function('b')(x)
y2 = sp.diff(y1, x)  # trasformazione unimodulare V=[[1,0],[d,1]]
print("riga1 =", sp.simplify(sp.diff(y1, x) - y2), " ; riga2 = L y1 =", sp.simplify(-af * y1 + sp.diff(y2, x) - bf * y2))

print("\n== CHECK 7: via (a) autovettori di forma binaria di grado m: m direzioni (C-S, n=2) ==")
X, Y = sp.symbols('X Y')
for m, f_ in [(3, X**3 + 3 * X**2 * Y - 2 * Y**3 + X * Y**2), (4, X**4 - 2 * X**3 * Y + 5 * X * Y**3 + Y**4 + X**2 * Y**2), (5, X**5 + X * Y**4 - 3 * Y**5 + 2 * X**3 * Y**2)]:
    eig = sp.Poly(sp.expand(X * sp.diff(f_, Y) - Y * sp.diff(f_, X)), X, Y)  # generatore rotazioni
    roots = sp.Poly(eig.as_expr().subs(Y, 1), X).nroots()
    print(f" m={m}: grado condizione = {eig.total_degree()} ; formula ((m-1)^2-1)/(m-2) = {((m-1)**2-1)//(m-2)} ; direzioni reali = {sum(1 for r in roots if abs(sp.im(r))<1e-12)}")

print("\n== CHECK 8: separabilita per direzioni: odeco (rotazione) vs Waring (GL2), cubica binaria ==")
th, l1, l2 = sp.symbols('theta l1 l2')
v = sp.cos(th) * X + sp.sin(th) * Y; w = -sp.sin(th) * X + sp.cos(th) * Y
fo = sp.Poly(sp.expand(l1 * v**3 + l2 * w**3), X, Y)
cc = [fo.coeff_monomial(X**3), fo.coeff_monomial(X**2 * Y) / 3, fo.coeff_monomial(X * Y**2) / 3, fo.coeff_monomial(Y**3)]
odeco_eq = lambda c0, c1, c2, c3: c0 * c2 + c1 * c3 - c1**2 - c2**2
print(" eq. odeco c0c2+c1c3-c1^2-c2^2 su forma odeco:", sp.simplify(odeco_eq(*cc)))
for cvec in ([1, 1, 0, 1], [2, 3, 5, 9]):
    fq = cvec[0]*X**3 + 3*cvec[1]*X**2*Y + 3*cvec[2]*X*Y**2 + cvec[3]*Y**3
    print(" forma", fq, ": eq. odeco =", odeco_eq(*cvec))
    # Apolarita/Sylvester: f = sum al_i (X + k_i Y)^3 <=> c_j = sum al_i k_i^j : PRONY sulla catalecticante (=Hankel)
    Hk = sp.Matrix([[cvec[0], cvec[1], cvec[2]], [cvec[1], cvec[2], cvec[3]]])
    qv = Hk.nullspace()[0]; z = sp.symbols('z'); qz = sp.expand(qv[0] + qv[1] * z + qv[2] * z**2)
    ks = sp.solve(qz, z); al, be = sp.symbols('al be')
    sol = sp.solve([al + be - cvec[0], al * ks[0] + be * ks[1] - cvec[1]], [al, be], dict=True)[0]
    rec = sp.expand(sol[al] * (X + ks[0] * Y)**3 + sol[be] * (X + ks[1] * Y)**3)
    print("   catalecticante", Hk.tolist(), "rank", Hk.rank(), "; q(z) =", qz, "; disc =", sp.discriminant(qz, z), "; k =", ks, "; residuo Waring =", sp.simplify(rec - fq), "; 1+k1k2 =", sp.simplify(1 + ks[0]*ks[1]))
q4 = [1, 2, 0, -1, 3]; H4 = sp.Matrix(3, 3, lambda i, j: q4[i + j]); print(" quartica: catalecticante 3x3 rank =", H4.rank(), "=> Waring >= 3")

print("\n== CHECK 9: compagna normale? ==")
cr = sp.symbols('c', real=True)
Cn = companion([-cr, 0]); print(" [C,C^T] per p=s^2-c:", sp.simplify(Cn * Cn.T - Cn.T * Cn))
Cg2 = companion([2, -3]); print(" [C,C^T] per p=s^2-3s+2:", Cg2 * Cg2.T - Cg2.T * Cg2)
V = sp.Matrix([[1, 1], [1, 2]])
print(" C V = V diag(1,2), V Vandermonde:", Cg2 * V == V * sp.diag(1, 2), "; duali = righe di V^-1 =", V.inv().tolist())
print(" f(C) = sum f(l_a) v_a w_a^T con f=exp(x.):", sp.simplify(sp.expand(V*sp.diag(sp.exp(x),sp.exp(2*x))*V.inv()) - sum((sp.exp(x * l) * V[:, i] * V.inv()[i, :] for i, l in enumerate([1, 2])), sp.zeros(2))) == sp.zeros(2))

print("\n== CHECK 10: via (b) PDE: U_t = C(xi)U ; discriminante in tau = punti di Jordan ==")
Ptx = tau**2 + 2 * xi * tau + xi**4; Cx = companion([xi**4, 2 * xi])
print(" charpoly C(xi) =", sp.expand(Cx.charpoly(tau).as_expr()), " ; Disc_tau =", sp.factor(sp.discriminant(Ptx, tau)))
for x0 in [0, 1, 2]:
    print(f"  xi={x0}: Jordan =", Cx.subs(xi, x0).jordan_form()[1].tolist())

print("\n== CHECK 11: lemma odeco cubica binaria: c0c2+c1c3-c1^2-c2^2 = al*be*(k1-k2)^2*(1+k1*k2) ==")
al, be, k1, k2 = sp.symbols('al be k1 k2')
cj = [al * k1**j + be * k2**j for j in range(4)]
print(" differenza =", sp.factor(sp.expand(cj[0]*cj[2] + cj[1]*cj[3] - cj[1]**2 - cj[2]**2 - al*be*(k1-k2)**2*(1+k1*k2))))
print(" fattorizzazione =", sp.factor(sp.expand(cj[0]*cj[2] + cj[1]*cj[3] - cj[1]**2 - cj[2]**2)))
