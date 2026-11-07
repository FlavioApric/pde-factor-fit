# enc_g8 — verifiche del recepimento post-Gate 8 (S8-ENC, 27/10/2026)
# 1. ENC2-4 / DIC3: per V = 0 il rappresentante pseudo-conforme risolve il sistema
#    T' = 1/rho^2, rho' = 4 a rho, a' + 4 a^2 = -alpha con alpha = 0 e ha theta != id.
# 2. Lo stesso rappresentante, come mappa puntuale piu' gauge, manda soluzioni libere
#    (i u_t = -u_xx, normalizzazione del progetto) in soluzioni libere: verifica su una
#    gaussiana libera esplicita.
# 3. ENC2-4: theta affine => rho costante => a = 0 => alpha = 0 (verifica simbolica).
# 4. ENC2-5 / POLE3: con polo z(t) = t, U = (1/2, 3/2) e' libero ai tempi 0 e 2,
#    ma il rettangolo [0, 2] x U contiene il polo (t = 1, x = 1).
import sys
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")
ok = 0
tot = 0


def check(name, cond):
    global ok, tot
    tot += 1
    ok += bool(cond)
    print(("OK  " if cond else "FAIL") + " " + name)


t, x, a0 = sp.symbols("t x a0", real=True)
tau, y = sp.symbols("tau y")

# 1. sistema DIC per alpha = 0
rho = 1 + 4 * a0 * t
a = a0 / rho
T = t / rho
alpha = 0
c1 = sp.simplify(sp.diff(T, t) - 1 / rho**2) == 0
c2 = sp.simplify(sp.diff(rho, t) - 4 * a * rho) == 0
c3 = sp.simplify(sp.diff(a, t) + 4 * a**2 + alpha) == 0
c4 = T.subs(t, 0) == 0 and sp.simplify(T - t) != 0
check("DIC3: pseudo-conforme risolve il sistema con alpha = 0 e theta != id", c1 and c2 and c3 and c4)

# 2. mappa puntuale + gauge su una gaussiana libera
v = lambda tt, yy: (1 + 4 * sp.I * tt) ** sp.Rational(-1, 2) * sp.exp(-yy**2 / (1 + 4 * sp.I * tt))
vres = sp.simplify(sp.I * sp.diff(v(tau, y), tau) + sp.diff(v(tau, y), y, 2))
found = None
for s in (1, -1):
    u = rho ** sp.Rational(-1, 2) * sp.exp(s * sp.I * a * x**2) * v(T, x / rho)
    res = sp.simplify((sp.I * sp.diff(u, t) + sp.diff(u, x, 2)) / u)
    if res == 0:
        found = s
check("gaussiana libera: v soluzione di i v_tau = -v_yy", vres == 0)
check("mappa u = rho^(-1/2) e^(+-i a x^2) v(T, x/rho) libera -> libera (segno %s)" % found, found is not None)

# 3. theta affine => alpha = 0
r = sp.Function("r")(t)
kk = sp.symbols("k", positive=True)
# T' = 1/rho^2 costante = kk => rho = kk^(-1/2) costante => a = rho'/(4 rho) = 0 => alpha = -(a' + 4a^2) = 0
rho_c = kk ** sp.Rational(-1, 2)
a_c = sp.diff(rho_c, t) / (4 * rho_c)
alpha_c = -(sp.diff(a_c, t) + 4 * a_c**2)
check("theta affine => rho costante => a = 0 => alpha = 0", sp.simplify(a_c) == 0 and sp.simplify(alpha_c) == 0)

# 4. POLE3
z = lambda tt: tt
U = (sp.Rational(1, 2), sp.Rational(3, 2))
free_ends = all(not (U[0] < z(tt) < U[1]) for tt in (0, 2))
crosses = U[0] < z(1) < U[1]
check("POLE3: U libero ai tempi 0 e 2, il polo lo attraversa a t = 1", free_ends and crosses)

print("%d/%d OK" % (ok, tot))
