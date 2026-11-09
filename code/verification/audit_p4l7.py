# S-CHECK-8: red team di P4-L7 (CHECK_REQUEST_2.md). Esecuzione: .venv\Scripts\python.exe -I audit_p4l7.py
import sys; sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
t, x, tau, xi, tp, xp = sp.symbols('t x tau xi tp xp')
RES = []
def chk(name, cond):
    RES.append((name, bool(cond))); print(('OK  ' if cond else 'FAIL'), name)

def apply_op(Q, f, vt, vx):
    Qp = sp.Poly(sp.expand(Q), tau, xi); out = 0
    for (i, j), c in Qp.terms():
        out += c*sp.diff(f, vt, i, vx, j)
    return sp.expand(out)
def QA(Q, AmT):
    z = AmT*sp.Matrix([tau, xi])
    return sp.expand(Q.subs({tau: z[0], xi: z[1]}, simultaneous=True))

# ---------- 1. convenzione: (Q(d)u)oA == Q^A(d')(uoA), Q^A(z') = Q(A^{-T} z')
ftest = sp.exp(2*t-3*x)*(1+t*x**2) + sp.sin(t+x**2)
for A in [sp.Matrix([[1, 2], [0, 1]]), sp.Matrix([[2, -1], [1, 3]]), sp.Matrix([[0, 1], [1, 0]]),
          sp.Matrix([[sp.Rational(1, 2), 1], [-1, 1]])]:
    AmT = A.T.inv()
    sub = {t: A[0, 0]*tp+A[0, 1]*xp, x: A[1, 0]*tp+A[1, 1]*xp}
    for Q in [tau**2-xi, tau*xi-1, (tau-xi)*(tau+xi), tau-xi**2, tau**3+xi*tau-2]:
        lhs = apply_op(Q, ftest, t, x).subs(sub, simultaneous=True)
        uA = ftest.subs(sub, simultaneous=True)
        rhs = apply_op(QA(Q, AmT), uA, tp, xp)
        chk(f"1 chain rule A={list(A)} Q={Q}", sp.simplify(lhs-rhs) == 0)
    # controllo negativo: con A invece di A^{-T} la formula fallisce in generale
    A0 = sp.Matrix([[2, -1], [1, 3]])
sub0 = {t: 2*tp-xp, x: tp+3*xp}
Qn = tau*xi-1
lhs0 = apply_op(Qn, ftest, t, x).subs(sub0, simultaneous=True)
rhs0 = apply_op(QA(Qn, sp.Matrix([[2, -1], [1, 3]])), ftest.subs(sub0, simultaneous=True), tp, xp)
chk("1 controllo negativo: sostituire A al posto di A^{-T} da' un risultato diverso", sp.simplify(lhs0-rhs0) != 0)

# ---------- 2. coefficiente di tau'^m in P^A = P_m(a,b); monicita' dei fattori
def lead_hom(P):
    Pp = sp.Poly(P, tau, xi); m = Pp.total_degree()
    return m, sum(c*tau**i*xi**j for (i, j), c in Pp.terms() if i+j == m)
def make_AmT(a, b):
    M = sp.Matrix([[a, 0], [b, 1]]) if a != 0 else sp.Matrix([[a, 1], [b, 0]])
    assert M.det() != 0
    return M
cases = {'tau^2-xi': tau**2-xi, '(tau-xi)(tau+xi)': (tau-xi)*(tau+xi), 'tau*xi-1': tau*xi-1,
         'calore tau-xi^2': tau-xi**2, '(tau-xi)^2(tau+xi)': (tau-xi)**2*(tau+xi),
         'xi^2*(tau*xi-1)': xi**2*(tau*xi-1), 'tau^2': tau**2, 'xi*(xi-tau^2)': xi*(xi-tau**2)}
norm = {}
for name, P in cases.items():
    m, Pm = lead_hom(P)
    ab = next((a, b) for a in range(0, 4) for b in range(-3, 4) if (a, b) != (0, 0) and Pm.subs({tau: a, xi: b}) != 0)
    AmT = make_AmT(*ab)
    chk(f"2 {name}: A^-T e1 = (a,b) = {ab}", list(AmT[:, 0]) == list(ab))
    PA = QA(P, AmT); Pt = sp.Poly(PA, tau)
    chk(f"2 {name}: deg_tau P^A = deg P = {m}", Pt.degree() == m)
    chk(f"2 {name}: coeff di tau'^m = P_m(a,b) = {Pm.subs({tau: ab[0], xi: ab[1]})}",
        sp.simplify(Pt.LC()-Pm.subs({tau: ab[0], xi: ab[1]})) == 0)
    Pn = sp.expand(PA/Pt.LC())
    c, facs = sp.factor_list(Pn, tau, xi)
    ok = all(sp.Poly(f, tau).LC().is_number and sp.Poly(f, tau).degree() == sp.Poly(f, tau, xi).total_degree() >= 1
             for f, e in facs)
    chk(f"2 {name}: P^A normalizzato = {Pn}; fattori {[(f, e) for f, e in facs]} monici in tau con deg_tau = deg >= 1", ok)
    norm[name] = (Pn, facs, AmT)

# ---------- 3. CK formale con dati lambda_j e^{x^2}
E = sp.exp(x**2)
def ck_coeffs(P, lam, K):
    Pt = sp.Poly(P, tau); m = Pt.degree()
    p = [sp.expand(Pt.coeff_monomial(tau**j)) for j in range(m)]
    a = [sp.Integer(lam[j])*E for j in range(m)]
    for k in range(K-m+1):
        a.append(sp.expand(-sum(apply_op(p[l], a[k+l], t, x) for l in range(m))))
    return a
def jets(a, K):
    return {(k, b): sp.diff(a[k], x, b).subs(x, 0) for k in range(K+1) for b in range(K+1-k)}
def ann_dim_upper(J, K, d):
    mons = [(i, j) for i in range(d+1) for j in range(d+1-i)]
    rows = []
    for k in range(K-d+1):
        for b in range(K-d+1-k):
            rows.append([J[(k+i, b+j)] for (i, j) in mons])
    M = sp.Matrix(rows)
    return len(mons)-M.rank()
def ideal_dim(P, d):
    dp = sp.Poly(P, tau, xi).total_degree()
    return 0 if d < dp else (d-dp+1)*(d-dp+2)//2

for name, (Pn, facs, AmT) in norm.items():
    m = sp.Poly(Pn, tau).degree()
    Pt = sp.Poly(Pn, tau)
    chk(f"3 {name}: forma di Kovalevskaya deg p_j <= m-j",
        all(sp.Poly(Pt.coeff_monomial(tau**j), xi).degree() <= m-j for j in range(m)))
    Pis = [sp.expand(f/sp.Poly(f, tau).LC()) for f, e in facs]; Qis = [sp.expand(sp.cancel(Pn/f)) for f in Pis]
    L = sp.symbols(f'l0:{m}')
    excl = []
    for Pi, Qi in zip(Pis, Qis):
        chk(f"3 {name}: deg_tau Q_i < m per Q_i = {sp.factor(Qi)}", sp.Poly(Qi, tau).degree() < m)
        cj = [sp.Poly(Qi, tau).coeff_monomial(tau**j) for j in range(m)]
        r = sp.expand(sum(L[j]*cj[j] for j in range(m)))
        eqs = sp.Poly(r, xi).coeffs()
        Mk = sp.Matrix([[sp.diff(e, l) for l in L] for e in eqs])
        excl.append((str(sp.factor(Qi)), [str(e) for e in eqs]))
        chk(f"3 {name}: nucleo di lambda -> r_i proprio (codim {Mk.rank()} >= 1) per Q_i = {sp.factor(Qi)}", Mk.rank() >= 1)
    print("     insieme escluso = unione dei nuclei {lambda: tutte le eq. = 0}:", excl)
    lamg = [j+1+j**2 for j in range(m)]
    K = 7
    a = ck_coeffs(Pn, lamg, K)
    U = sum(a[k]*t**k/sp.factorial(k) for k in range(K+1))
    R = apply_op(Pn, U, t, x)
    Rt = sp.Poly(sp.expand(R*sp.exp(-x**2)), t)
    chk(f"3 {name}: lam = {lamg}: P(d)u = 0 in serie fino a t^{K-m}",
        all(sp.simplify(Rt.coeff_monomial(t**k)) == 0 for k in range(K-m+1)))
    J = jets(a, K)
    chk(f"3 {name}: jet di u in 0 razionali fino all'ordine {K}", all(v.is_rational for v in J.values()))
    for Pi, Qi in zip(Pis, Qis):
        w0 = sp.expand(apply_op(Qi, U, t, x).subs(t, 0))
        cj = [sp.Poly(Qi, tau).coeff_monomial(tau**j) for j in range(m)]
        r = sp.expand(sum(lamg[j]*cj[j] for j in range(m)))
        chk(f"3 {name}: w_i(0,.) = r_i^lam(d_x) e^(x^2), r_i^lam = {r}, Q_i = {sp.factor(Qi)}",
            sp.simplify(w0-apply_op(r, E, t, x)) == 0)
        ders = [sp.expand(sp.diff(w0, x, k)*sp.exp(-x**2)) for k in range(8)]
        Md = sp.Matrix([[sp.Poly(dd, x).coeff_monomial(x**n) for n in range(25)] for dd in ders])
        chk(f"3 {name}: r != 0 e 8 derivate di w_i(0,.) linearmente indipendenti", r != 0 and Md.rank() == 8)
    for d in range(1, 4):
        du = ann_dim_upper(J, K, d)
        chk(f"3 {name}: certificato: dim Ann∩R_<={d} <= {du} = dim (P)∩R_<={d} = {ideal_dim(Pn, d)}", du == ideal_dim(Pn, d))

# ---------- 4. la genericita' serve
def bad(name, lam, Qi):
    Pn, facs, AmT = norm[name]; m = sp.Poly(Pn, tau).degree(); K = 8
    a = ck_coeffs(Pn, lam, K); U = sum(a[k]*t**k/sp.factorial(k) for k in range(K+1))
    W = apply_op(Qi, U, t, x)
    Wt = sp.Poly(sp.expand(W*sp.exp(-x**2)), t)
    zero = all(sp.simplify(Wt.coeff_monomial(t**k)) == 0 for k in range(K-m+1))
    chk(f"4 {name}: lam = {lam} nel nucleo => Q_i = {sp.factor(Qi)} annulla u (serie fino a t^{K-m}): Ann(u) != (P)", zero)
bad('tau^2', [1, 0], tau)
bad('(tau-xi)^2(tau+xi)', [0, 1, 0], sp.expand((3*tau-xi)*(3*tau+xi)/9))  # coordinate trasformate: P^A = (3tau-xi)(3tau+xi)^2/27
Pn = norm['(tau-xi)(tau+xi)'][0]
for lam in [[1, 0], [0, 1], [3, -7]]:
    a = ck_coeffs(Pn, lam, 3)
    U = sum(a[k]*t**k/sp.factorial(k) for k in range(4))
    for Qi in [3*tau-xi, 3*tau+xi]:  # fattori di P^A = tau^2 - xi^2/9
        w0 = sp.expand(apply_op(Qi, U, t, x).subs(t, 0))
        chk(f"4 (tau-xi)(tau+xi) [P^A = tau^2-xi^2/9]: lam = {lam}: w_i(0,.) != 0 per Q_i = {Qi} (unico lambda escluso: 0)", w0 != 0)
uc = (sp.exp((x+t)**2)+sp.exp((x-t)**2))/2
chk("4 onda: u = (e^{(x+t)^2}+e^{(x-t)^2})/2 risolve u_tt = u_xx con dati (e^{x^2}, 0)",
    sp.simplify(sp.diff(uc, t, 2)-sp.diff(uc, x, 2)) == 0 and sp.simplify(uc.subs(t, 0)-E) == 0 and sp.diff(uc, t).subs(t, 0) == 0)
chk("4 onda: (d_t+d_x)u = 2(x+t)e^{(x+t)^2} (non EP)", sp.simplify(sp.diff(uc, t)+sp.diff(uc, x)-2*(x+t)*sp.exp((x+t)**2)) == 0)

# ---------- 5. nota (b): calore
uh = t**sp.Rational(-1, 2)*sp.exp(-x**2/(4*t))
chk("5 calore: u = t^{-1/2}e^{-x^2/(4t)} risolve u_t = u_xx", sp.simplify(sp.diff(uh, t)-sp.diff(uh, x, 2)) == 0)
chk("5 calore: jet in (1,0) razionali fino all'ordine 4",
    all(sp.nsimplify(sp.diff(uh, t, i, x, j).subs({t: 1, x: 0})).is_rational for i in range(5) for j in range(5-i)))
print("     P^A calore normalizzato:", norm['calore tau-xi^2'][0], " A^-T:", list(norm['calore tau-xi^2'][2]))

# ---------- 6. Lettura con D (esempio della direzione utile)
a = ck_coeffs(tau**2, [1, 0], 6); J = jets(a, 6)
du = ann_dim_upper(J, 6, 2)
chk(f"6 tau^2, u = e^(x^2): dim{{jet-nulli}}∩R_<=2 = {du} > dim (tau^2)∩R_<=2 = 1 (testimone tau, D = 1)", du > 1)

print("\nTOTALE:", sum(ok for _, ok in RES), "/", len(RES))
