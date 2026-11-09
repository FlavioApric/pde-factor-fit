# S-CHECK-F8-CONV: controlli indipendenti su CONV-T1(5,6), CONV-T2 (lemma di evitamento), CONV-T5(3),
# CONV-MZ3 (entrambe le letture del criterio RT-S2d), CONV-R1 (esempi), CONV-B2 (conteggio D+1),
# CONV-P6(b) (Lambert), CONV-T6 (Poisson), CONV-D1(c), CONV-D2 (successione esatta su un esempio).
import itertools, math, sys
import sympy as sp
sys.stdout.reconfigure(encoding='utf-8')
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

t, x, y, z = sp.symbols('t x y z', real=True)
tau, xi = sp.symbols('tau xi')

def monos(m, nv=2):
    return [a for k in range(m+1) for a in itertools.product(range(k+1), repeat=nv) if sum(a) == k] if nv != 2 else \
           [(i, k-i) for k in range(m+1) for i in range(k+1)]

def jet(u, K, vars_=(t, x)):
    J = {}
    for k in range(K+1):
        for i in range(k+1):
            a = (i, k-i)
            J[a] = sp.diff(u, vars_[0], a[0], vars_[1], a[1]).subs({vars_[0]: 0, vars_[1]: 0})
    return J

def Nmat(J, m, K):
    cols = monos(m); rows = monos(K-m)
    return sp.Matrix([[J[(al[0]+be[0], al[1]+be[1])] for al in cols] for be in rows]), cols

def Lstar(J, K):
    for m in range(K+1):
        M, cols = Nmat(J, m, K)
        ns = M.nullspace()
        if ns:
            polys = [sp.expand(sum(v[i]*tau**cols[i][0]*xi**cols[i][1] for i in range(len(cols)))) for v in ns]
            g = polys[0]
            for p in polys[1:]:
                g = sp.gcd(g, p)
            g = sp.Poly(g, tau, xi)
            return m, (g.monic().as_expr() if g.total_degree() > 0 else sp.Integer(1))
    return None, None

# --- T1(6): u = 1 + x^{N+2} e^{x^2}: O_K = 1 per K <= N+1, = tau da N+2
for N in (1, 2, 3):
    u = 1 + x**(N+2)*sp.exp(x**2)
    J = jet(u, N+4)
    outs = [Lstar(J, K) for K in range(1, N+4)]
    good = all(o == (1, 1) for o in outs[:N+1]) and all(o == (1, tau) for o in outs[N+1:])
    print("N=%d uscite (m*,O_K) K=1..%d:" % (N, N+3), outs)
    check("T1(6) N=%d: K* = N+2" % N, good)

# --- T1(5): conteggio uscite distinte su un esempio con d = 2 (calore), tetto (d+1)(d+2)/2 = 6
u = sp.exp(-t)*sp.sin(x) + sp.exp(-4*t)*sp.cos(2*x) + x
J = jet(u, 9)
outs = [Lstar(J, K) for K in range(1, 10)]
print("calore+trasporto, uscite:", outs)
dist = len(set(o[1] for o in outs))
check("T1(5): uscite distinte <= 6 (esempio)", dist <= 6)
# monotonia lessicografica della coppia (m*, deg O_K)
pairs = [(o[0], sp.Poly(o[1], tau, xi).total_degree()) for o in outs]
check("T1(5): coppia (m*, deg O_K) non decrescente (esempio)", all(pairs[i] <= pairs[i+1] for i in range(len(pairs)-1)))

# --- T2, lemma di evitamento in n = 2: g = |z|^{2(L+1)} e^{|z|^2}; K0(m,L) e dipendenza del minore
def K0(m, L, Kmax=16):
    g = (t**2+x**2)**(L+1)*sp.exp(t**2+x**2)
    J = jet(g, Kmax)
    cols = monos(m)
    for K in range(m+L+1, Kmax+1):
        rows = [be for be in monos(K-m) if sum(be) > L]
        M = sp.Matrix([[J[(al[0]+be[0], al[1]+be[1])] for al in cols] for be in rows])
        if M.rank() == len(cols):
            # tutte le coordinate usate hanno ordine in (L, K]
            used = {sum(al)+sum(be) for al in cols for be in rows}
            return K, min(used) > L and max(used) <= K
    return None, False
for (m, L) in ((0, 0), (1, 0), (1, 1), (2, 1)):
    K, dep = K0(m, L)
    print("m=%d L=%d: K0=%s" % (m, L, K))
    check("T2 lemma m=%d L=%d: K0 esiste e minore usa solo ordini in (L,K0]" % (m, L), K is not None and dep)
# il punto (ii) non serve: lo stesso K0 esiste per g0 = e^{|z|^2} (nessun annullamento in 0)
def K0g0(m, L, Kmax=16):
    J = jet(sp.exp(t**2+x**2), Kmax); cols = monos(m)
    for K in range(m+L+1, Kmax+1):
        rows = [be for be in monos(K-m) if sum(be) > L]
        M = sp.Matrix([[J[(al[0]+be[0], al[1]+be[1])] for al in cols] for be in rows])
        if M.rank() == len(cols):
            return K
check("T2: con g0 = e^{|z|^2} (senza (ii)) K0(1,1) esiste ugualmente", K0g0(1, 1) is not None)

# --- T5(3): p = t^d x^d (n=2): Ann(p) ∩ R_{<=d} = 0; Q0 tau^{d+1} annulla u+eps p
for d in (1, 2, 3):
    p = t**d*x**d
    cols = monos(d)
    vecs = [sp.Poly(sp.diff(p, t, a, x, b), t, x) for (a, b) in cols]
    allm = sorted({mm for v in vecs for mm in v.monoms()})
    M = sp.Matrix([[v.coeff_monomial(mm) for v in vecs] for mm in allm])
    check("T5(3) d=%d: Ann(t^d x^d) ∩ R_<=d = 0" % d, M.rank() == len(cols))
uh = (t+1)**sp.Rational(-1, 2)*sp.exp(-x**2/(4*(t+1)))
eps = sp.symbols('eps')
up = uh + eps*t**2*x**2
Q0tau3 = sp.diff(sp.diff(up, t) - sp.diff(up, x, 2), t, 3)
check("T5(3): (tau - xi^2) tau^{3} annulla u + eps t^2 x^2 (d=2)", sp.simplify(Q0tau3) == 0)

# --- MZ3: entrambe le letture di RT-S2d
a11, a22, a12, a21 = sp.symbols('a11 a22 a12 a21')
s, tt = sp.symbols('s tt', positive=True)
def mz(A):
    a11, a12, a21, a22 = A
    K = a12*sp.exp(tt*a22)*a21
    noise = a12*sp.exp(tt*a22)
    Pm = sp.diag(1, 0); AA = sp.Matrix([[a11, a12], [a21, a22]])
    comm = Pm*AA - AA*Pm
    return sp.simplify(K) == 0, sp.simplify(noise) == 0, comm == sp.zeros(2, 2)
r1 = mz((a11, 1, 0, a22)); r2 = mz((a11, 0, 1, a22))
print("a12=1,a21=0: memoria0, rumore0, comm0 =", r1)
print("a12=0,a21=1: memoria0, rumore0, comm0 =", r2)
check("MZ3: lettura 'memoria' -> controesempio a12=1,a21=0", r1[0] and not r1[2])
check("MZ3: a12=1,a21=0 NON confuta la lettura 'memoria+rumore' (rumore != 0)", not r1[1])
check("MZ3: lettura 'memoria+rumore' -> controesempio a12=0,a21=1", r2[0] and r2[1] and not r2[2])
# MZ2: equazione eliminata
A_ = sp.Matrix([[a11, a12], [a21, a22]])
check("MZ2: det(tau-A) = (tau-a11)(tau-a22)-a12 a21", sp.expand((tau*sp.eye(2)-A_).det() - ((tau-a11)*(tau-a22)-a12*a21)) == 0)

# --- R1: f=xi, g=tau su I x T: ker(tau xi) = ker xi + ker tau (u_tx = 0 => A(t)+B(x))
A_f, B_f = sp.Function('A'), sp.Function('B')
w = A_f(t) + B_f(x)
check("R1: A(t)+B(x) in ker(tau xi)", sp.diff(w, t, x) == 0)
# esempio R2: f = tau - xi^2, g = tau + xi; r(xi) = f - g = -xi(xi+1); risonanze k in Z con r(ik)=0
r = sp.expand((tau - xi**2) - (tau + xi))
Z = [k for k in range(-20, 21) if r.subs(xi, sp.I*k) == 0]
check("R1 esempio R2: Z = {0}", Z == [0])
f0, g0 = (tau - xi**2).subs(xi, 0), (tau + xi).subs(xi, 0)
check("R1 esempio R2: k=0 risonante, deg gcd = 1", sp.degree(sp.gcd(f0, g0), tau) == 1)
# testimone u = t
check("R1: u=t in ker(fg)", sp.diff(sp.diff(t, t) + sp.diff(t, x), t) - sp.diff(sp.diff(t, t) + sp.diff(t, x), x, 2) == 0)

# --- B2: ogni ∂^gamma compare al piu' D+1 volte in sum_alpha ||∂^alpha e||^2_{H^1}
for Dd, n0 in ((2, 2), (3, 2), (2, 3)):
    from collections import Counter
    cnt = Counter()
    alphas = [a for k in range(n0+1) for a in itertools.product(range(k+1), repeat=Dd) if sum(a) == k]
    for a in alphas:
        cnt[a] += 1
        for j in range(Dd):
            b = list(a); b[j] += 1; cnt[tuple(b)] += 1
    check("B2: molteplicita' max = %d <= D+1 = %d (D=%d,n0=%d)" % (max(cnt.values()), Dd+1, Dd, n0), max(cnt.values()) <= Dd+1)

# --- P6(b): Lambert, a = W0(-sigma k^2)/sigma soddisfa a = -k^2 e^{-sigma a}
import mpmath as mp
okL = True
for sig in (0.5, 1.0, 2.0):
    for kk in (0.1, 0.3, 0.5):
        if kk >= (sig*math.e)**-0.5: continue
        aa = mp.lambertw(-sig*kk**2, 0).real/sig
        okL &= abs(aa + kk**2*mp.e**(-sig*aa)) < 1e-12
check("P6(b): identita' di Lambert", okL)

# --- T6: Poisson, rami tau = i xi e tau = -i xi, prodotto tau^2 + xi^2
k = sp.symbols('k', real=True)
check("T6 Poisson: (tau - i xi)(tau + i xi) = tau^2 + xi^2", sp.expand((tau - sp.I*xi)*(tau + sp.I*xi)) == tau**2 + xi**2)
check("T6 Poisson ramo k>0: tau=-k, xi=ik soddisfa tau - i xi = 0", sp.simplify(-k - sp.I*(sp.I*k)) == 0 or sp.simplify(-k - sp.I*sp.I*k) == 0)

# --- D1(c): w = f(t+x1), (tau - xi1) w = 0, xi2 w = 0
x1, x2 = sp.symbols('x1 x2', real=True)
F = sp.Function('f')
ww = F(t + x1)
check("D1(c): (∂t-∂x1) w = 0 e ∂x2 w = 0", sp.simplify(sp.diff(ww, t) - sp.diff(ww, x1)) == 0 and sp.diff(ww, x2) == 0)

# --- D2: (Q1) ∩ (Q2) = (Q1 Q2) per Q1 = tau - xi^2, Q2 = tau + xi (Groebner dell'intersezione)
Q1, Q2 = tau - xi**2, tau + xi
ss = sp.symbols('ss')
Gb = sp.groebner([ss*Q1, (1-ss)*Q2], ss, tau, xi, order='lex')
inter = [g for g in Gb.exprs if not g.has(ss)]
check("D2: (Q1)∩(Q2) = (Q1 Q2) (esempio)", len(inter) == 1 and sp.simplify(sp.cancel(inter[0]/(Q1*Q2))).is_number)

print("TUTTI PASS" if all(OK) else "ALCUNI FAIL", "(%d/%d)" % (sum(OK), len(OK)))
