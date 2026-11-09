# S-C1C2 · C12-C1 (la scomposizione per fattori non conserva H^m(Omega)) e C12-T3 (corde corte)
# f = d_t - d_x, g = d_t - d_x - 1 su Omega = (0,1)^2; coordinate (t, s = x + t), angolo (0,0): corda t in (0,s).
# u = G(s)(e^t - 1);  componenti uniche: u_1 = -G(s) in ker f,  u_2 = e^t G(s) in ker g.
# Esecuzione: D:\ProblemaBase\.venv\Scripts\python.exe -I c12_counterexample.py
from sympy import (symbols, exp, log, diff, integrate, simplify, oo, Function, limit, Rational,
                   factorial, Matrix, sqrt, series, S)
t, x, s, eps = symbols('t x s epsilon', positive=True)
PASS = 0; FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print('PASS', name)
    else: FAIL += 1; print('FAIL', name)

Fn = Function('Gf')
# 1) appartenenza al nucleo per G generica
u = Fn(x + t)*(exp(t) - 1)
fu = diff(u, t) - diff(u, x)
fgu = diff(fu, t) - diff(fu, x) - fu
check('C1 u in ker fg (G generica)', simplify(fgu) == 0)
check('C1 f u = e^t G(x+t) = u_2', simplify(fu - exp(t)*Fn(x + t)) == 0)
u1 = -Fn(x + t); u2 = exp(t)*Fn(x + t)
check('C1 u_1 in ker f', simplify(diff(u1, t) - diff(u1, x)) == 0)
check('C1 u_2 in ker g', simplify(diff(u2, t) - diff(u2, x) - u2) == 0)
check('C1 u = u_1 + u_2', simplify(u1 + u2 - u) == 0)

# 2) pesi sulla corda di lunghezza s: int_0^s (e^t-1)^2 dt ~ s^3/3, int_0^s e^{2t} dt ~ s
w3 = integrate((exp(t) - 1)**2, (t, 0, s)); w1 = integrate(exp(2*t), (t, 0, s))
check('C1 peso corda (e^t-1)^2 ~ s^3/3', limit(w3/s**3, s, 0) == Rational(1, 3))
check('C1 peso corda e^{2t} ~ s', limit(w1/s, s, 0) == 1)

# 3) scelta G_m(s) = s^{m-1} log s (m >= 1), G_0 = 1/s ; integrali vicino all'angolo s in (0,1)
def Gm(m):
    return 1/s if m == 0 else s**(m - 1)*log(s)
for m in range(0, 5):
    G = Gm(m)
    # u in H^m: int |G^{(j)}|^2 s ds < oo per j <= m-1 ; int |G^{(m)}|^2 s^3 ds < oo
    ok_u = True
    for j in range(0, m):
        val = integrate(diff(G, s, j)**2*s, (s, 0, 1))
        ok_u = ok_u and val.is_finite
    val_top = integrate(diff(G, s, m)**2*s**3, (s, 0, 1))
    ok_u = ok_u and val_top.is_finite
    # u_2 non in H^m: int |G^{(m)}|^2 s ds = oo
    val_bad = integrate(diff(G, s, m)**2*s, (s, 0, 1))
    check(f'C1 m={m}: u in H^m (integrali finiti)', ok_u)
    check(f'C1 m={m}: u_2 = e^t G notin H^m (int |G^(m)|^2 s ds = oo)', val_bad == oo)
    if m >= 1:
        check(f'C1 m={m}: G^(m) = (m-1)!/s', simplify(diff(G, s, m) - factorial(m - 1)/s) == 0)

# 4) C12-T3: autovalore minimo della Gram di {1, e^t} su una corda (0,l): ~ l^3/12 (degenera), Gram ~ l
l = symbols('l', positive=True)
Gr = Matrix([[integrate(1, (t, 0, l)), integrate(exp(t), (t, 0, l))],
             [integrate(exp(t), (t, 0, l)), integrate(exp(2*t), (t, 0, l))]])
detG = simplify(Gr.det()); trG = simplify(Gr.trace())
lam_min_approx = detG/trG   # lambda_min <= det/trace*... ; lambda_min ~ det/trace per l->0
check('T3 det Gram ~ l^4/12', limit(detG/l**4, l, 0) == Rational(1, 12))
check('T3 lambda_min ~ det/tr ~ l^3/24', limit(lam_min_approx/l**3, l, 0) == Rational(1, 24))

# 5) densita' (m=0): u_eps = G 1_{s>eps}(e^t-1) -> u in L^2: resto int_0^eps G^2 s^3/3 ds -> 0
rest = integrate((1/s)**2*s**3/3, (s, 0, eps))
check('T3/C2 resto di troncamento -> 0', limit(rest, eps, 0) == 0)

print(f'\nRISULTATO: {PASS} PASS, {FAIL} FAIL')
