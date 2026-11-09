# S-CHECK-COL: controlli simbolici indipendenti delle disuguaglianze di S10-COL.
import sympy as sp

ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(f"[{'OK' if cond else 'FAIL'}] {name}")

rho, w1n, L, r, z, Wp, delta, kap, d, s = sp.symbols('rho w1n L r z Wp delta kappa d s', nonnegative=True)

# L1(iii): |x1-p| < rho + rho(|w1| + rho/2) <= rho(2+|w1|) per 0<rho<=1
expr = rho*(2 + w1n) - (rho + rho*(w1n + rho/2))
chk("L1(iii) rho(2+|w1|) - [rho + rho(|w1|+rho/2)] = rho(1-rho/2) >= 0 per rho<=1",
    sp.simplify(expr - rho*(1 - rho/2)) == 0)

# L1(ii): con rho=min(r, lam r, r/lam): lam*rho <= r e rho/lam <= r
lam = sp.symbols('lam', positive=True)
okii = True
for lv in [sp.Rational(1, 7), sp.Rational(1, 2), 1, 3, 11]:
    rv = sp.Rational(2, 5)
    rh = min(rv, lv*rv, rv/lv)
    okii &= (lv*rh <= rv) and (rh/lv <= rv)
chk("L1(ii) lam*rho <= r e rho/lam <= r (campioni razionali)", okii)

# L2 / TB Passo 3: |y-p| < r + r(|z|+r) <= r(2+|z|) per r<=1
chk("L2 r(2+|z|) - [r + r(|z|+r)] = r(1-r)", sp.simplify(r*(2 + z) - (r + r*(z + r)) - r*(1 - r)) == 0)

# TB Passo 3: |u'| <= |W(p)| + r <= |W(p)|+1 => 1+|u'| <= 2+|W(p)|
up = sp.symbols('up', nonnegative=True)
# verifica diretta: differenza = delta*(1+Wp-up)/((1+up)(2+Wp)) >= 0
chk("TB P3 differenza = delta(1+|W(p)|-|u'|)/((1+|u'|)(2+|W(p)|))",
    sp.simplify(delta/(1 + up) - delta/(2 + Wp) - delta*(1 + Wp - up)/((1 + up)*(2 + Wp))) == 0)

# TB Passo 2: |x'+s w' - p'| < delta + t|w'| <= 2 delta per t <= delta/(1+|w'|)
wp = sp.symbols('wp', nonnegative=True)
chk("TB P2 delta + delta|w'|/(1+|w'|) - 2delta = -delta/(1+|w'|) <= 0",
    sp.simplify(delta + delta*wp/(1 + wp) - 2*delta + delta/(1 + wp)) == 0)

# TB Passo 1: (kappa - e) sqrt(1+G^2) >= kappa/2 per e <= kappa/2
G, e = sp.symbols('G e', nonnegative=True)
chk("TB P1 (kappa-e)sqrt(1+G^2) >= kappa/2 per 0<=e<=kappa/2 (minimo in G=0, e=kappa/2)",
    sp.simplify(((kap - e)*sp.sqrt(1 + G**2)).subs({G: 0, e: kap/2}) - kap/2) == 0)

# TB Passo 3, riga finale: x_n-g(x') + t u_n - t(u_n - kappa/2) >= t kappa/2
t, un, b0 = sp.symbols('t u_n b0', real=True)
chk("TB P3 b0 + t u_n - t(u_n-kappa/2) - t kappa/2 = b0", sp.simplify(b0 + t*un - t*(un - kap/2) - t*kap/2 - b0) == 0)

# TC(a) punti lontani: sigma1 - M t >= c t  <=> t <= sigma1/(M+c)
M, c, s1 = sp.symbols('M c sigma1', positive=True)
chk("TC(a) sigma1 - M t - c t = 0 in t = sigma1/(M+c)", sp.simplify((s1 - M*t - c*t).subs(t, s1/(M + c))) == 0)

# Oss 3.3: e_n . (-nu) = 1/sqrt(1+|Dg|^2), nu = (Dg,-1)/sqrt(1+|Dg|^2)
g1 = sp.symbols('g1', real=True)
nu = sp.Matrix([g1, -1])/sp.sqrt(1 + g1**2)
chk("Oss 3.3 e_n.(-nu) = 1/sqrt(1+g'^2)", sp.simplify(sp.Matrix([0, 1]).dot(-nu) - 1/sp.sqrt(1 + g1**2)) == 0)

# Kill K1: g(x) = x sin(log|x|): g'(x) = sin(log|x|) + cos(log|x|) per x != 0, range [-sqrt2, sqrt2]
x = sp.symbols('x', positive=True)
gx = x*sp.sin(sp.log(x))
chk("K1 g'(x) = sin(log x) + cos(log x) (x>0)", sp.simplify(sp.diff(gx, x) - sp.sin(sp.log(x)) - sp.cos(sp.log(x))) == 0)
xm = sp.symbols('xm', negative=True)
gm = xm*sp.sin(sp.log(-xm))
chk("K1 g'(x) = sin(log|x|) + cos(log|x|) (x<0)", sp.simplify(sp.diff(gm, xm) - sp.sin(sp.log(-xm)) - sp.cos(sp.log(-xm))) == 0)
th = sp.symbols('th', real=True)
chk("K1 sin+cos = sqrt2 sin(th+pi/4): range [-sqrt2, sqrt2]",
    sp.simplify(sp.sin(th) + sp.cos(th) - sp.sqrt(2)*sp.sin(th + sp.pi/4)) == 0)

print("ESITO:", "TUTTO OK" if ok else "FALLIMENTI")
