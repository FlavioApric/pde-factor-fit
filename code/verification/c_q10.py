# S-CHECK-F10-C: controlli indipendenti per S10-OPEN-C §3 (VAR-Q10-EX).
import sys
import sympy as sp
import mpmath as mp
sys.stdout.reconfigure(encoding="utf-8")
RES = []
def ok(name, cond):
    RES.append((name, bool(cond))); print(("OK  " if cond else "FAIL"), name)

y, l, sv = sp.symbols('y l s', positive=True)
k = sp.Symbol('k', positive=True)

# D6: sup_s s^{-k} e^{-1/(2s²)} = k^{k/2} e^{-k/2} (y = s^{-2}: y^{k/2} e^{-y/2}, max in y = k)
hy = (k/2)*sp.log(y) - y/2
yc = sp.solve(sp.diff(hy, y), y)[0]
ok("D6 sup s^{-k}e^{-1/(2s²)}: punto critico y = k", sp.simplify(yc - k) == 0)
ok("D6 valore k^{k/2}e^{-k/2}", sp.simplify(sp.exp(hy.subs(y, yc)) - k**(k/2)*sp.exp(-k/2)) == 0)
# k^{k/2}e^{-k/2} ≤ C^k (k!)^{1/2}: rapporto^(1/k) limitato (Stirling), controllo k ≤ 200
rat = [float((mp.mpf(kk)**(kk/2)*mp.e**(-kk/2)/mp.sqrt(mp.factorial(kk)))**(1/mp.mpf(kk))) for kk in range(1, 201)]
ok("D6 (k^{k/2}e^{-k/2}/(k!)^{1/2})^{1/k} ≤ 1 per k ≤ 200", max(rat) <= 1.0)
# Cauchy: Re (1+ζ)^{-2} ≥ 1/2 per |ζ| ≤ 1/10 (campionamento fine del bordo e dell'interno)
mn = min(((1 + rr*mp.e**(1j*th))**-2).real for rr in [0.0, 0.05, 0.1] for th in mp.linspace(0, 2*mp.pi, 721))
ok("D6 Re(1+ζ)^{-2} ≥ 1/2 su |ζ| ≤ 0.1 (min ≈ %.4f)" % float(mn), mn >= 0.5)
# stima |g_0^{(k)}(s)| ≤ k!(θs)^{-k}e^{-1/(2s²)} con θ = 1/10, controllo numerico k ≤ 8
g0 = sp.exp(-1/sv**2)
good = True
for kk in range(0, 9):
    dk = sp.lambdify(sv, sp.diff(g0, sv, kk), 'mpmath')
    for ss in [0.05, 0.1, 0.2, 0.4, 0.8, 1.5, 3.0]:
        lhs = abs(dk(mp.mpf(ss)))
        rhs = mp.factorial(kk)*(mp.mpf(ss)/10)**(-kk)*mp.e**(-1/(2*mp.mpf(ss)**2))
        good &= lhs <= rhs
ok("D6 |g_0^{(k)}| ≤ k!(s/10)^{-k}e^{-1/(2s²)} (k ≤ 8, 7 punti)", good)

# D7: e^{-ℓ^{-4}/2} ≤ ℓ su (0,1]: log ℓ + ℓ^{-4}/2 ≥ 0, minimo in ℓ = 1 sul dominio
phi = sp.log(l) + l**-4/2
crit = sp.solve(sp.diff(phi, l), l)
ok("D7 punto critico di log ℓ + ℓ^{-4}/2 è ℓ = 2^{1/4} > 1 (quindi decrescente su (0,1])", len(crit) == 1 and sp.nsimplify(crit[0]**4) == 2)
ok("D7 valore in ℓ = 1: 1/2 > 0", phi.subs(l, 1) == sp.Rational(1, 2))
# sup_{ℓ} ℓ^{-k} e^{-ℓ^{-4}/2} = (k/(2e))^{k/4}  (w = ℓ^{-4}: w^{k/4}e^{-w/2}, max in w = k/2)
hw = (k/4)*sp.log(y) - y/2
wc = sp.solve(sp.diff(hw, y), y)[0]
ok("§3 passo 3: sup ℓ^{-k}e^{-ℓ^{-4}/2} = (k/(2e))^{k/4}", sp.simplify(sp.exp(hw.subs(y, wc)) - (k/(2*sp.E))**(k/4)) == 0)

# Leibniz per B(s) = g_0(s)g_0(1−s): Σ C(k,j) (j!(k−j)!)^{3/2} ≤ 2^k (k!)^{3/2}
good = all(sum(sp.binomial(kk, j)*(sp.factorial(j)*sp.factorial(kk - j))**sp.Rational(3, 2) for j in range(kk + 1)) <= 2**kk*sp.factorial(kk)**sp.Rational(3, 2) for kk in range(0, 30))
ok("§3 Leibniz: Σ_j C(k,j)(j!(k−j)!)^{3/2} ≤ 2^k(k!)^{3/2} (k < 30)", good)

# D8: ((k+j)!)^{7/4}/(2k)! con (k+j)! ≤ 2^{k+j}k!j!: termine ≤ const_j·(2^{7/4}A)^k/(k!)^{1/4}
good = all(sp.factorial(kk + j) <= 2**(kk + j)*sp.factorial(kk)*sp.factorial(j) for kk in range(25) for j in range(25))
ok("D8 (k+j)! ≤ 2^{k+j} k! j! (k, j < 25)", good)
good = all(sp.factorial(2*kk) >= sp.factorial(kk)**2 for kk in range(40))
ok("§3 (2k)! ≥ (k!)²", good)

# Tychonoff: residuo di L_0 sulla serie troncata = solo il termine di testa (verifica indipendente, ordine 9)
t, x = sp.symbols('t x', real=True)
g = sp.Function('g')
Kt = 9
u = sum((-sp.I)**kk*sp.diff(g(t), t, kk)*x**(2*kk)/sp.factorial(2*kk) for kk in range(Kt + 1))
res = sp.expand(sp.I*sp.diff(u, t) + sp.diff(u, x, 2))
ok("§3 serie di Tychonoff: L_0 u_K = i(−i)^K g^{(K+1)}x^{2K}/(2K)!", sp.simplify(res - sp.I*(-sp.I)**Kt*sp.diff(g(t), t, Kt + 1)*x**(2*Kt)/sp.factorial(2*Kt)) == 0)
ok("§3 u(t,0) = g(t)", u.subs(x, 0) == g(t))

# illustrazione: g_j su un gap (α, α+ℓ): piatta agli estremi (derivate → 0, k ≤ 3)
al, ll = sp.Rational(1, 3), sp.Rational(1, 3)
B = lambda z: sp.exp(-1/z**2)*sp.exp(-1/(1 - z)**2)
gj = sp.exp(-ll**-4)*B((t - al)/ll)
good = all(sp.limit(sp.diff(gj, t, kk), t, al, '+') == 0 and sp.limit(sp.diff(gj, t, kk), t, al + ll, '-') == 0 for kk in range(4))
ok("§3 g_j piatta agli estremi del gap (k ≤ 3)", good)

print(f"\n[c_q10] {sum(c for _, c in RES)}/{len(RES)} OK")
