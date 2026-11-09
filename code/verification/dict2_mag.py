# dict2_mag.py — S-CHECK-F8-DICT, rev2: audit indipendente di DICT-MAG-NU (PROOF_PACKAGE §2.6, punto "Sistemi").
# Convenzione della legge: i u_t = -(nabla - iA)^2 u + V u, A e V reali.
# M1-M2: identita' generiche; M3: esempio stazionario con zeri; M4: esempio non stazionario con zeri;
# M5: n = 3; M6: rot B != 0 (campi magnetici diversi); M7 [nota]: con A statico la costruzione non basta.
import sys
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ok = tot = 0


def check(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  [" + info + "]" if info else ""))


t, x, y, z = sp.symbols("t x y z", real=True)


def mag2(u, A):
    """(nabla - iA)^2 u in 2D."""
    return (sp.diff(u, x, 2) + sp.diff(u, y, 2)
            - 2 * sp.I * (A[0] * sp.diff(u, x) + A[1] * sp.diff(u, y))
            - sp.I * (sp.diff(A[0], x) + sp.diff(A[1], y)) * u
            - (A[0] ** 2 + A[1] ** 2) * u)


# ---------- M1: identita' delle differenze, funzioni generiche ----------
a, b = sp.Function("a", real=True)(t, x, y), sp.Function("b", real=True)(t, x, y)
A0 = (sp.Function("A1", real=True)(t, x, y), sp.Function("A2", real=True)(t, x, y))
Bg = (sp.Function("B1", real=True)(t, x, y), sp.Function("B2", real=True)(t, x, y))
u = a + sp.I * b
gu = (sp.diff(u, x), sp.diff(u, y))
divB = sp.diff(Bg[0], x) + sp.diff(Bg[1], y)
dVu = (-2 * sp.I * (Bg[0] * gu[0] + Bg[1] * gu[1]) - sp.I * divB * u
       - (2 * (A0[0] * Bg[0] + A0[1] * Bg[1]) + Bg[0] ** 2 + Bg[1] ** 2) * u)
A1 = (A0[0] + Bg[0], A0[1] + Bg[1])
check("M1 (nabla-i(A+B))^2u - (nabla-iA)^2u = dV*u", sp.simplify(sp.expand(mag2(u, A1) - mag2(u, A0) - dVu)) == 0)

# ---------- M2: Im(dV) = -div(|u|^2 B)/|u|^2 ----------
rho2 = a ** 2 + b ** 2
num = sp.expand(dVu * (a - sp.I * b))  # dV * |u|^2
im_num = (num - num.subs(sp.I, -sp.I)) / (2 * sp.I)  # tutte le funzioni sono reali
divrhoB = sp.diff(rho2 * Bg[0], x) + sp.diff(rho2 * Bg[1], y)
check("M2 Im(dV)|u|^2 = -div(|u|^2 B)", sp.simplify(sp.expand(im_num + divrhoB)) == 0)

# bump C_c^infty in coordinate locali
def bump(r2):
    return sp.Piecewise((sp.exp(-1 / (1 - r2)), r2 < 1), (0, True))


def residual_check(label, U, A, V, chi, pts, three_d=False):
    rho2 = sp.expand(U * sp.conjugate(U))
    rho2 = sp.simplify(sp.re(sp.expand_complex(rho2)))
    B = (sp.diff(chi, y) / rho2, -sp.diff(chi, x) / rho2)
    Anew = (A[0] + B[0], A[1] + B[1])
    gU = (sp.diff(U, x), sp.diff(U, y))
    dB = sp.diff(B[0], x) + sp.diff(B[1], y)
    dV = (-2 * sp.I * (B[0] * gU[0] + B[1] * gU[1]) / U - sp.I * dB
          - 2 * (A[0] * B[0] + A[1] * B[1]) - (B[0] ** 2 + B[1] ** 2))
    old = sp.I * sp.diff(U, t) + mag2(U, A) - V * U
    new = sp.I * sp.diff(U, t) + mag2(U, Anew) - (V + dV) * U
    mo = mn = mi = 0
    for p in pts:
        s = dict(zip((t, x, y), p))
        mo = max(mo, abs(complex(sp.N(old.subs(s), 40))))
        mn = max(mn, abs(complex(sp.N(new.subs(s), 40))))
        mi = max(mi, abs(complex(sp.N(sp.im(dV).subs(s), 40))))
    check(label + " legge vecchia risolve", mo < 1e-25, "max = %.1e" % mo)
    check(label + " legge nuova (A+B, V+dV) risolve", mn < 1e-25, "max = %.1e" % mn)
    check(label + " dV reale", mi < 1e-25, "max |Im dV| = %.1e" % mi)
    bval = complex(sp.N(B[0].subs(dict(zip((t, x, y), pts[0]))), 30))
    check(label + " B non nullo", abs(bval) > 1e-8, "|B1| = %.3e" % abs(bval))
    return B, rho2


# ---------- M3: stazionario con zeri. u = e^{-iEt} sin x sin y, A = 0, V = E - 2 ----------
E = sp.Rational(3, 2)
U3 = sp.exp(-sp.I * E * t) * sp.sin(x) * sp.sin(y)
c = sp.pi / 2
r2 = (x - c) ** 2 + (y - c) ** 2  # disco di raggio 1 dentro (0, pi)^2, dove u != 0
chi3 = bump(r2) * (1 + x / 3)
pts3 = [(0, c + sp.Rational(1, 5), c - sp.Rational(3, 10)), (sp.Rational(7, 10), c - sp.Rational(1, 2), c + sp.Rational(2, 5)),
        (2, c + sp.Rational(3, 5), c + sp.Rational(1, 10))]
B3, rho3 = residual_check("M3", U3, (0, 0), E - 2, chi3, pts3)
check("M3 u ha zeri (x = 0)", sp.simplify(U3.subs(x, 0)) == 0)

# ---------- M4: non stazionario con zeri. Libera: u = e^{i(x-t)} + e^{i(2y-4t)}, A = 0, V = 0 ----------
U4 = sp.exp(sp.I * (x - t)) + sp.exp(sp.I * (2 * y - 4 * t))
r24 = (t ** 2 + x ** 2 + y ** 2) * 4  # bump nello spazio-tempo di raggio 1/2 attorno a 0, dove |u|^2 >= 2 + 2cos(3/2 * ...) > 0
chi4 = bump(r24)
pts4 = [(sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(-1, 10)), (sp.Rational(-1, 8), sp.Rational(1, 10), sp.Rational(1, 6)),
        (0, sp.Rational(-1, 4), sp.Rational(1, 5))]
B4, rho4 = residual_check("M4", U4, (0, 0), 0, chi4, pts4)
zero_pt = {t: 0, x: sp.pi, y: 0}
check("M4 u ha zeri (t=0, x=pi, y=0)", sp.simplify(U4.subs(zero_pt)) == 0)
# |u|^2 = 2 + 2cos(x - 2y + 3t) e' >= 2 + 2cos(3*0.5*sqrt(14)/... ) sul supporto: controllo diretto del minimo grossolano
check("M4 supporto di chi lontano dagli zeri", all(abs(x0 - 2 * y0 + 3 * t0) <= 3 < sp.pi for t0 in (-0.5, 0.5) for x0 in (-0.5, 0.5) for y0 in (-0.5, 0.5)),
      "|x - 2y + 3t| <= 3 < pi sul cubo che contiene la palla")

# ---------- M5: n = 3, B = rho^{-2}(d_y chi, -d_x chi, 0) ----------
rr = sp.Function("r", positive=True)(x, y, z)
ch = sp.Function("chi")(x, y, z)
B5 = (sp.diff(ch, y) / rr, -sp.diff(ch, x) / rr, 0)
div5 = sp.diff(rr * B5[0], x) + sp.diff(rr * B5[1], y) + sp.diff(rr * B5[2], z)
check("M5 n = 3: div(|u|^2 B) = 0", sp.simplify(div5) == 0)

# ---------- M6: rot B != 0 (non e' un gradiente: campo magnetico diverso, cfr. SYS-N3(c)) ----------
rot3 = sp.diff(B3[1], x) - sp.diff(B3[0], y)
vals = [abs(float(sp.N(rot3.subs(dict(zip((t, x, y), p))), 30))) for p in pts3]
check("M6 rot B != 0 in M3", max(vals) > 1e-6, "max |rot B| = %.3e" % max(vals))

# ---------- M7 [nota]: in M4 il B costruito dipende da t ----------
dtB = sp.diff(B4[0], t)
v = abs(float(sp.N(dtB.subs({t: sp.Rational(1, 10), x: sp.Rational(1, 5), y: sp.Rational(-1, 10)}), 30)))
check("M7 [nota] in M4 dB/dt != 0: serve A = A(t,x) nella classe", v > 1e-8, "|d_t B1| = %.3e" % v)

print(f"{ok}/{tot} PASS")
