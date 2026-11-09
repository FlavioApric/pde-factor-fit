# F4-INT — verifiche KdV (solo controllo, vincolo k3). Eseguire: .venv\Scripts\python.exe -I int_kdv.py
# Convenzione: u_t + 6 u u_x + u_xxx = 0, cioe' u_t = K1[u]; gerarchia con parte lineare -d^{2n+1}:
#   K0 = -u_x ; K1 = -(u_xxx + 6 u u_x) ; K2 = -(u_5x + 10 u u_xxx + 20 u_x u_xx + 30 u^2 u_x)  (Lax 5th order)
# N-solitone: u = 2 (log f)_xx, f = sum_mu prod A_ij^{mu_i mu_j} prod E_i^{mu_i}, E_i = exp(k_i x - k_i^3 t + c_i),
#   A_ij = ((k_i-k_j)/(k_i+k_j))^2. d_x = sum k_i E_i d/dE_i ; d_t (flusso K1) = sum -k_i^3 E_i d/dE_i.
# Predizione (INT-T1): sum_n d_n K_n[u] = 0  <=>  q_d(k_i^2) = 0 per ogni i, q_d(lam) = sum d_n lam^n.
import sympy as sp, itertools, random
random.seed(7)
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(("OK  " if cond else "FAIL"), name)

def soliton(ks):
    N = len(ks); E = sp.symbols(f'E1:{N+1}', positive=True)
    A = lambda i, j: sp.Rational((ks[i]-ks[j])**2, (ks[i]+ks[j])**2)
    f = 0
    for mu in itertools.product([0, 1], repeat=N):
        term = sp.Integer(1)
        for i in range(N):
            for j in range(i+1, N):
                if mu[i] and mu[j]: term *= A(i, j)
        for i in range(N): term *= E[i]**mu[i]
        f += term
    Dx = lambda p: sum(ks[i]*E[i]*sp.diff(p, E[i]) for i in range(N))
    Dt = lambda p: sum(-ks[i]**3*E[i]*sp.diff(p, E[i]) for i in range(N))
    return E, f, Dx, Dt

def jet_at(ks, pt, order=7):
    """Valori esatti in un punto (E_i razionali) di u, u_x..u_5x, u_t via ricorsione di Leibniz su f g' = f'."""
    E, f, Dx, Dt = soliton(ks)
    fd = [f]
    for _ in range(order+1): fd.append(sp.expand(Dx(fd[-1])))
    ft = [sp.expand(Dt(f))]
    for _ in range(3): ft.append(sp.expand(Dx(ft[-1])))
    F = [sp.Rational(p.subs(pt)) for p in fd]
    Ft = [sp.Rational(p.subs(pt)) for p in ft]
    g = [None]  # g[j] = d^j log f, j>=1
    for n in range(order+1):
        # f^{(n+1)} = sum_{j=0}^{n} C(n,j) f^{(n-j)} g^{(j+1)}
        acc = F[n+1] - sum(sp.binomial(n, j)*F[n-j]*g[j+1] for j in range(n))
        g.append(acc/F[0])
    r = []
    for n in range(3):
        acc = Ft[n] - sum(sp.binomial(n, j)*F[n-j]*r[j] for j in range(n))
        r.append(acc/F[0])
    u = [2*g[m+2] for m in range(6)]
    ut = 2*r[2]
    u0, u1, u2, u3, u4, u5 = u
    K0 = -u1; K1 = -(u3 + 6*u0*u1); K2 = -(u5 + 10*u0*u3 + 20*u1*u2 + 30*u0**2*u1)
    return dict(ut=ut, K0=K0, K1=K1, K2=K2)

def pts(N, n):
    return [{sp.Symbol(f'E{i+1}', positive=True): sp.Rational(random.randint(1, 19), random.randint(1, 19)) for i in range(N)} for _ in range(n)]

def zero_at_points(ks, coeffs, n=12):
    # combinazione lineare dei campi nulla in n punti razionali casuali (esatto nei punti; V-ex come identita')
    for pt in pts(len(ks), n):
        J = jet_at(ks, pt)
        if sum(c*J[k] for k, c in coeffs.items()) != 0: return False
    return True

def relation_dim(ks, names, n=12):
    M = sp.Matrix([[jet_at(ks, pt)[k] for k in names] for pt in pts(len(ks), n)])
    return len(names) - M.rank()

# --- 1-solitone, k = 2 ---
ks = [2]
check("1-sol: u_t = K1 (KdV)", zero_at_points(ks, {'ut': 1, 'K1': -1}))
check("1-sol: K1 - k^2 K0 = 0 (stazionario: traslazione = KdV, RT-R7c)", zero_at_points(ks, {'K1': 1, 'K0': -4}))
d = relation_dim(ks, ['ut', 'K0', 'K1']); check(f"1-sol: dim relazioni span{{u_t,K0,K1}} = 2 (ambiguita' H_1 = 1); trovato {d}", d == 2)
d = relation_dim(ks, ['ut', 'K0', 'K1', 'K2']); check(f"1-sol: dim relazioni span{{u_t,K0,K1,K2}} = 3 (ambiguita' H_2 = 2); trovato {d}", d == 3)
# --- 2-solitone ---
for ks in ([1, 2], [1, 3], [2, 5]):
    l1, l2 = ks[0]**2, ks[1]**2
    check(f"2-sol k={ks}: u_t = K1", zero_at_points(ks, {'ut': 1, 'K1': -1}))
    check(f"2-sol k={ks}: Novikov K2 - (k1^2+k2^2)K1 + k1^2k2^2 K0 = 0", zero_at_points(ks, {'K2': 1, 'K1': -(l1+l2), 'K0': l1*l2}))
    d = relation_dim(ks, ['ut', 'K0', 'K1']); check(f"2-sol k={ks}: dim relazioni span{{u_t,K0,K1}} = 1 (identifica in H_1); trovato {d}", d == 1)
    d = relation_dim(ks, ['ut', 'K0', 'K1', 'K2']); check(f"2-sol k={ks}: dim relazioni span{{u_t,K0,K1,K2}} = 2 (ambiguita' H_2 = 1); trovato {d}", d == 2)
# --- 3-solitone ---
ks = [1, 2, 3]
check("3-sol k=(1,2,3): u_t = K1", zero_at_points(ks, {'ut': 1, 'K1': -1}))
d = relation_dim(ks, ['ut', 'K0', 'K1', 'K2']); check(f"3-sol: dim relazioni span{{u_t,K0,K1,K2}} = 1 (identifica in H_2); trovato {d}", d == 1)

# --- Kay-Moses: f = det(I + C) a meno di un fattore che non cambia (log f)_xx ---
for ks in ([1, 2], [1, 2, 3]):
    N = len(ks); E = sp.symbols(f'E1:{N+1}', positive=True)
    # C_ij = sqrt(E_i E_j) * 2 sqrt(k_i k_j)/(k_i+k_j)  (forma simmetrica di Gram/Cauchy)
    s = sp.symbols(f's1:{N+1}', positive=True)  # s_i = sqrt(E_i)
    C = sp.Matrix(N, N, lambda i, j: s[i]*s[j]*2*sp.sqrt(ks[i]*ks[j])/(ks[i]+ks[j]))
    det = sp.expand((sp.eye(N) + C).det())
    _, fH, _, _ = soliton(ks)
    fH_s = sp.expand(fH.subs({sp.Symbol(f'E{i+1}', positive=True): s[i]**2 for i in range(N)}))
    check(f"Kay-Moses N={N}: det(I+C) = f di Hirota (identita' polinomiale)", sp.expand(det - fH_s) == 0)

# --- Forma 'Bernoulli/Ising' del tau: f / prod(1+E_i) = E_mu[ prod A_ij^{mu_i mu_j} ], mu_i ~ Bernoulli(p_i), p_i = E_i/(1+E_i)
ks = [1, 2, 3]; N = 3
E, f, Dx, Dt = soliton(ks)
p = [E[i]/(1+E[i]) for i in range(N)]
A = lambda i, j: sp.Rational((ks[i]-ks[j])**2, (ks[i]+ks[j])**2)
Z = 0
for mu in itertools.product([0, 1], repeat=N):
    w = sp.Integer(1)
    for i in range(N): w *= p[i] if mu[i] else (1-p[i])
    for i in range(N):
        for j in range(i+1, N):
            if mu[i] and mu[j]: w *= A(i, j)
    Z += w
check("tau/prod(1+E_i) = media di Bernoulli di exp(sum_{i<j} mu_i mu_j log A_ij) (N=3)",
      sp.simplify(Z - f/sp.Mul(*[(1+e) for e in E])) == 0)

# --- int E_int dx = 0 per ogni N: (log f)_x -> sum k_i per x->+inf, -> 0 per x->-inf; idem per prod(1+E_i)
# controllo simbolico N=3: lungo x con t fisso, E_i = a_i * X^{k_i}, X = e^x
X = sp.symbols('X', positive=True)
a = [sp.Rational(1, 3), sp.Rational(5, 2), sp.Rational(7, 4)]
sub = {E[i]: a[i]*X**ks[i] for i in range(N)}
lfx = sp.simplify((Dx(f)/f).subs(sub))
check("N=3: (log f)_x -> sum k_i = 6 per x->+inf", sp.limit(lfx, X, sp.oo) == 6)
check("N=3: (log f)_x -> 0 per x->-inf", sp.limit(lfx, X, 0) == 0)

print(f"\nTOTALE: {sum(OK)}/{len(OK)} OK")
