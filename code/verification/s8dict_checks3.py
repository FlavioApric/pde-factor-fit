# S8-DICT, verifiche per il recepimento dell'audit (27/10/2026).
# R1: fix DICT-4, discretizzazione di Bernstein con nodo lambda = 0 trattato esattamente.
# R2: N1(vi) FALSO, controesempio u = t + x nella classe u_t = a(t,x) u_x.
# R3: non unicita' magnetica (DA AUDITARE): B = |u|^{-2} grad^perp chi rende reale delta V.
import sympy as sp
import mpmath as mp

ok = 0
tot = 0


def check(name, cond, info=""):
    global ok, tot
    tot += 1
    if cond:
        ok += 1
    print(("OK  " if cond else "FAIL") + " " + name + ("  " + info if info else ""))


# ---------- R1: k(t) = 1 + 1/(1+t), mu = delta_0 + e^{-lambda} d lambda ----------
mp.mp.dps = 30
T = 5.0


def kJ_err(Lam, J, eps0):
    # nodo esatto in 0 con peso 1; celle uniformi su [eps0, Lam] con peso mu'(I_i)
    edges = [eps0 + (Lam - eps0) * i / J for i in range(J + 1)]
    nodes = [(edges[i] + edges[i + 1]) / 2 for i in range(J)]
    w = [mp.e ** (-edges[i]) - mp.e ** (-edges[i + 1]) for i in range(J)]

    def kJ(t):
        return 1 + sum(wi * mp.e ** (-li * t) for wi, li in zip(w, nodes))

    def k(t):
        return 1 + 1 / (1 + t)

    return mp.quad(lambda t: abs(k(t) - kJ(t)), [0, 0.5, T])


errs = [kJ_err(L, J, e0) for (L, J, e0) in [(10, 20, 1e-1), (20, 80, 1e-2), (40, 320, 1e-3)]]
check("R1 errore L1 decrescente con nodo in 0", errs[0] > errs[1] > errs[2],
      "errori = " + ", ".join(mp.nstr(e, 3) for e in errs))
check("R1 errore finale < errore iniziale / 20", errs[2] < errs[0] / 20, mp.nstr(errs[2], 3))


# senza nodo in 0 (versione precedente): l'errore resta >= T
def err_no_zero(Lam, J, eps0):
    edges = [eps0 + (Lam - eps0) * i / J for i in range(J + 1)]
    nodes = [(edges[i] + edges[i + 1]) / 2 for i in range(J)]
    w = [mp.e ** (-edges[i]) - mp.e ** (-edges[i + 1]) for i in range(J)]
    return mp.quad(lambda t: abs(1 + 1 / (1 + t) - sum(wi * mp.e ** (-li * t) for wi, li in zip(w, nodes))), [0, 0.5, T])


e_nz = err_no_zero(40, 320, 1e-3)
check("R1 senza nodo in 0 l'errore e' circa T", e_nz > 0.9 * T, mp.nstr(e_nz, 4))

# ---------- R2: N1(vi) controesempio ----------
t, x = sp.symbols("t x", real=True)
u = t + x
a = sp.simplify(sp.diff(u, t) / sp.diff(u, x))
check("R2 legge a = 1 risolve u_t = a u_x", sp.simplify(sp.diff(u, t) - a * sp.diff(u, x)) == 0, "a = " + str(a))
check("R2 A_u = -u_x mai nulla (ker Phi_u = 0)", sp.diff(u, x) == 1)

# ---------- R3: non unicita' magnetica ----------
X, Y = sp.symbols("X Y", real=True)
U = (2 + sp.cos(X)) * sp.exp(sp.I * Y) * (1 + sp.Rational(1, 3) * sp.sin(X + 2 * Y) * sp.I)
chi = sp.exp(-(X ** 2 + Y ** 2)) * sp.cos(X - Y)
rho2 = sp.simplify(U * sp.conjugate(U))
B = (sp.diff(chi, Y) / rho2, -sp.diff(chi, X) / rho2)
divrhoB = sp.simplify(sp.diff(rho2 * B[0], X) + sp.diff(rho2 * B[1], Y))
check("R3 div(|u|^2 B) = 0", divrhoB == 0)
A0 = (sp.sin(Y), X ** 2)  # potenziale reale qualsiasi
gradU = (sp.diff(U, X), sp.diff(U, Y))
divB = sp.diff(B[0], X) + sp.diff(B[1], Y)
dV = (-2 * sp.I * (B[0] * gradU[0] + B[1] * gradU[1]) / U - sp.I * divB
      - 2 * (A0[0] * B[0] + A0[1] * B[1]) - (B[0] ** 2 + B[1] ** 2))
f_im = sp.lambdify((X, Y), sp.im(sp.expand_complex(dV)), "mpmath")
pts = [(sp.Rational(3, 10), sp.Rational(-7, 10)), (sp.Rational(11, 10), sp.Rational(2, 5)), (sp.Rational(-9, 10), sp.Rational(13, 10)), (2, sp.Rational(-3, 2))]
mx = max(abs(f_im(px, py)) for px, py in pts)
check("R3 Im(delta V) = 0 nei punti di prova", mx < 1e-20, "max |Im| = " + mp.nstr(mx, 3))


# identita' delle differenze: H(A+B, V+dV)u - H(A,V)u = 0, con (nabla - iA)^2
def mag(Avec):
    return (sp.diff(U, X, 2) + sp.diff(U, Y, 2)
            - 2 * sp.I * (Avec[0] * gradU[0] + Avec[1] * gradU[1])
            - sp.I * (sp.diff(Avec[0], X) + sp.diff(Avec[1], Y)) * U
            - (Avec[0] ** 2 + Avec[1] ** 2) * U)


A1 = (A0[0] + B[0], A0[1] + B[1])
diff_expr = -(mag(A1) - mag(A0)) + dV * U
f_d = lambda px, py: sp.N(diff_expr.subs({X: px, Y: py}), 50)
mxd = max(abs(complex(f_d(px, py))) for px, py in pts)
check("R3 H(A+B,V+dV)u = H(A,V)u", mxd < 1e-20, "max = " + mp.nstr(mxd, 3))
B_nonzero = abs(sp.lambdify((X, Y), B[0], "mpmath")(0.3, -0.7)) > 1e-6
check("R3 B non nullo", B_nonzero)

print(f"{ok}/{tot} OK")
