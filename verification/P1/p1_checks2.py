"""S-P1 controlli aggiuntivi dopo kill-argument (P1-P1(e)). Eseguire con .venv python -I."""
import sympy as sp
z, T, D, c, x, t = sp.symbols('zeta T D c x t', positive=True)
R = []
def check(n, b):
    R.append(b); print(f"[{'PASS' if b else 'FAIL'}] {n}")
# AD: a = -c xi + D xi^2, zeta reale > 0, t0 = 0
a1, a2 = -c*z, D*z**2
E = (sp.exp(a1*t)-1)*(sp.exp(a2*t)-1)            # fattore di e^{zeta x} in E_add(t)
u = sp.exp((a1+a2)*t)                             # fattore di e^{zeta x} in u(t)
# ||E||^2_{L2(I)} / sup_t |u|^2 e rapporto -> infinito: confronto dei tassi esponenziali
EL2 = sp.integrate(sp.exp(2*a2*t), (t, 0, T))     # termine dominante di |E|^2 per zeta grande (|z1|->1)
ratio = EL2 / sp.exp(2*(a1+a2)*T)                  # u e' crescente in t se D zeta > c
lim = sp.limit(sp.log(ratio)/z, z, sp.oo)
check("P1-P1(e) AD: log(||E||^2_{L2(I)}/max_t|u|^2)/zeta -> 2cT > 0 (rapporto esponenziale in zeta)", sp.simplify(lim - 2*c*T) == 0)
check("P1-P1(e) |z1| -> 1 per zeta -> +inf", sp.limit(sp.exp(a1*t)-1, z, sp.oo) == -1)
# attacco kill-argument: a1 = xi^2, a2 = -xi^2, modo e^{i k x}: E = (2-2cosh(s k^2))
k, s = sp.symbols('k s', positive=True)
Ek = (sp.exp(-s*k**2)-1)*(sp.exp(s*k**2)-1)
check("attacco: a1=xi^2, a2=-xi^2: E = 2-2cosh(s k^2)", sp.simplify((Ek-(2-2*sp.cosh(s*k**2))).rewrite(sp.exp)) == 0)
print(f"ESITO: {sum(R)}/{len(R)} PASS")
