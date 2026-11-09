# dict3_r6f.py — S-CHECK-F8-DICT: controllo leggero di R6-T(f) (triangolarita' dei getti di W = I + V).
# V f(x) = int_{-x}^{x} H(x, s) f(s) ds (punto base x_0 = 0). Si verifica:
# T1: se j^{m-1} f(0) = 0 allora j^m(Vf)(0) = 0 (triangolarita' stretta in x_0), per m = 1..6;
# T2: in x_1 != x_0 il getto di Vf dipende da f lontano da x_1 (nessuna triangolarita' fuori da x_0);
# T3: la t-dipendenza: W agisce in x, quindi d_t commuta e la triangolarita' vale per i getti in (t, x_0).
import sys
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ok = tot = 0


def check(name, cond, info=""):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  [" + info + "]" if info else ""))


x, s, t = sp.symbols("x s t", real=True)
H = 1 + x * s + 3 * s ** 2 - x ** 3 + sp.sin(x + 2 * s)  # nucleo liscio generico


def V(f):
    return sp.integrate(sp.series(H * f.subs(x, s), s, 0, 12).removeO(), (s, -x, x))


for m in range(1, 7):
    f = s ** m * (1 + s + 2 * s ** 2)  # getto d'ordine m-1 nullo in 0
    f = f.subs(s, x)
    vf = sp.expand(V(f))
    jet = [sp.diff(vf, x, k).subs(x, 0) for k in range(m + 1)]
    check(f"T1 m={m}: j^{m}(Vf)(0) = 0 se j^{m-1}f(0) = 0", all(sp.simplify(j) == 0 for j in jet))

# T2: f a supporto lontano da x_1 = 1/2 ma dentro [-1/2, 1/2]: f = bump vicino a -0.4; Vf(0.5) != 0
import mpmath as mp
Hf = sp.lambdify((x, s), H, "mpmath")
def bumpf(z):
    r = (z + mp.mpf(2) / 5) * 20
    return mp.e ** (-1 / (1 - r ** 2)) if abs(r) < 1 else mp.mpf(0)
val = mp.quad(lambda z: Hf(mp.mpf(1) / 2, z) * bumpf(z), [-0.45, -0.4, -0.35])
check("T2 in x_1 = 1/2: (Vf)(x_1) != 0 con f nulla vicino a x_1", abs(val) > 1e-12, "valore = %.3e" % float(val))

# T3: f(t, x) = e^{t} x^m: d_t^k V f = V d_t^k f
m = 3
ft = sp.exp(t) * x ** m
lhs = sp.diff(sp.integrate(H * ft.subs(x, s), (s, -x, x)), t)
rhs = sp.integrate(H * sp.diff(ft, t).subs(x, s), (s, -x, x))
check("T3 d_t commuta con W", sp.simplify(lhs - rhs) == 0)
print(f"{ok}/{tot} PASS")
