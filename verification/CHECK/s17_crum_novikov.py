# S-CHECK-17: controllo V-ex leggero per OPF5D-L6/T3 e [F4-] (N = 2, 3), senza exp simbolici.
# Tutte le funzioni sono razionali in e = exp(x); d/dx agisce come D = e d/de.
# Convenzioni del progetto: L = -d^2 - v, K_0 = -v', K_{n+1} = K_n'' + 4 v K_n + 2 v' a_n, a_n = antiderivata senza costante.
import sympy as sp
from math import comb

e = sp.symbols('e', positive=True)
k = sp.symbols('k')
res = []
def ok(name, cond):
    res.append((name, bool(cond))); print(('OK  ' if cond else 'FAIL') + ' ' + name, flush=True)

def D(f, n=1):
    for _ in range(n):
        f = sp.together(e*sp.diff(f, e))
    return f
def z(f):
    return sp.simplify(sp.factor(sp.together(f))) == 0

# operatori differenziali: dict ordine -> coefficiente
def compose(P, Q):
    R = {}
    for i, a in P.items():
        for j, b in Q.items():
            for l in range(i+1):
                c = sp.together(comb(i, l)*a*D(b, l))
                R[i-l+j] = sp.together(R.get(i-l+j, 0) + c)
    return R
def add(P, Q, s=1):
    R = dict(P)
    for j, b in Q.items():
        R[j] = sp.together(R.get(j, 0) + s*b)
    return R
def is_zero_op(P):
    return all(z(c) for c in P.values())
def transpose(P):
    # (a d^j)^T = (-d)^j o a
    R = {}
    for j, a in P.items():
        R = add(R, compose({j: sp.Integer((-1)**j)}, {0: a}))
    return R

def wronskian(fs):
    n = len(fs)
    M = sp.Matrix(n, n, lambda i, j: D(fs[j], i))
    return sp.together(M.det())

def run(kappas, label):
    N = len(kappas)
    # autofunzioni di L0 = -d^2 a -kappa^2: alternanza cosh/sinh (Crum, potenziale regolare)
    phis = []
    for j, kap in enumerate(kappas):
        s = 1 if j % 2 == 0 else -1
        phis.append((e**kap + s*e**(-kap))/2)
    W = wronskian(phis)
    v = sp.together(2*D(D(sp.log(W))))
    v = sp.factor(v)
    # Crum: A f = W(phi_1..phi_N, f)/W(phi_1..phi_N): coefficiente di d^j = cofattore
    n = N + 1
    A = {}
    for j in range(n):
        # sviluppo lungo l'ultima colonna: entrata (j, n-1) = D^j f
        M = sp.Matrix(n, n-1, lambda i, c: D(phis[c], i))
        minor = M.copy(); minor.row_del(j)
        cof = (-1)**(j + n - 1) * minor.det()
        A[j] = sp.together(cof/W)
    ok(f'{label}: A monico di ordine N', z(A[N]-1))
    L = {2: sp.Integer(-1), 0: -v}
    L0 = {2: sp.Integer(-1)}
    ok(f'{label}: intreccio di Crum L A = A L0 (L6)', is_zero_op(add(compose(L, A), compose(A, L0), -1)))
    # gerarchia
    vp = D(v)
    K = [-vp]; a = [-v]
    for m in range(N):
        Kn = sp.together(D(K[-1], 2) + 4*v*K[-1] + 2*vp*a[-1])
        K.append(Kn)
        # antiderivata senza costante: verifichiamo solo a_1 esplicito
        if m == 0:
            a.append(-(D(v, 2) + 3*v**2))
            ok(f'{label}: a_1 = -(v\'\'+3v^2) e\' antiderivata di K_1', z(D(a[1]) - K[1]))
        elif m == 1:
            # a_2 dalla T1: a_2 = 2*16*f_3; qui si usa la forma chiusa standard
            a2 = -(D(v, 4) + 10*v*D(v, 2) + 5*D(v)**2 + 10*v**3)
            ok(f'{label}: a_2 antiderivata di K_2', z(D(a2) - K[2]))
            a.append(a2)
    # Novikov: q_{d*} = prod (lambda - 4 kappa^2)
    lam = sp.symbols('lam')
    q = sp.Poly(sp.prod([lam - 4*kp**2 for kp in kappas]), lam)
    Kd = sum(q.coeff_monomial(lam**i)*K[i] for i in range(N+1))
    ok(f'{label}: Novikov K_d*[v] = 0 con q = prod(lam - 4 kappa_j^2) (T3)', z(Kd))
    # Ambiguita' minima: nessuna relazione di grado < N (determinante di Gram/indipendenza dei K_0..K_{N-1} in punti)
    pts = [sp.Rational(3, 2) + sp.Rational(i, 3) for i in range(N)]
    Mk = sp.Matrix(N, N, lambda i, j: K[j].subs(e, pts[i]))
    ok(f'{label}: K_0..K_(N-1) linearmente indipendenti (nessuna relazione di grado < N)', sp.simplify(Mk.det()) != 0)
    # P = A d A^T commuta con L e ha coefficiente direttore 1
    P = compose(compose(A, {1: sp.Integer(1)}), transpose(A))
    ok(f'{label}: P = A d A^T monico di ordine 2N+1', z(P[2*N+1]-1) and all(z(P.get(j, 0)) for j in range(2*N+2, 2*N+4)))
    ok(f'{label}: [P, L] = 0', is_zero_op(add(compose(P, L), compose(L, P), -1)))
    # senza riflessione: A e^{ikx} = e^{ikx} * p(k,x), limiti a +-inf = prod(ik -+ kappa) (convenzione Crum)
    sym = sum(A[j]*(sp.I*k)**j for j in range(N+1))
    lim_p = sp.expand(sp.limit(sym, e, sp.oo))
    lim_m = sp.expand(sp.limit(sym, e, 0))
    tp = sp.expand(sp.prod([sp.I*k - kp for kp in kappas])); tm = sp.expand(sp.prod([sp.I*k + kp for kp in kappas]))
    ok(f'{label}: simbolo di A -> prod(ik - kappa_j) a +inf', sp.simplify(lim_p - tp) == 0)
    ok(f'{label}: simbolo di A -> prod(ik + kappa_j) a -inf (T = prod (k+i kappa)/(k-i kappa), R = 0)', sp.simplify(lim_m - tm) == 0)
    return v, W

v2, W2 = run([1, 2], 'N=2 (kappa=1,2)')
# [F4-] N = 2: f di Hirota con k_j = 2 kappa_j: f = 1 + c1 E + c2 E^2 + ((k1-k2)/(k1+k2))^2 c1 c2 E^3, E = e^2
E = e**2
c1, c2 = sp.symbols('c1 c2', positive=True)
f = 1 + c1*E**1 + c2*E**2 + sp.Rational(1, 9)*c1*c2*E**3
vH = sp.together(2*D(D(sp.log(f))))
sol = sp.solve([sp.numer(sp.together(vH - v2)).subs(e, sp.Rational(1, 2)), sp.numer(sp.together(vH - v2)).subs(e, 2)], [c1, c2], dict=True)
good = [s for s in sol if all(val.is_positive for val in s.values())]
okH = bool(good) and z(vH.subs(good[0]) - v2)
ok('N=2: v di Crum = 2 d^2 log f (Hirota, k_j = 2 kappa_j) per opportune fasi c1,c2>0 ([F4-] N=2)', okH)
print('fasi', good, flush=True)

run([1, 2, 3], 'N=3 (kappa=1,2,3)')
n_ok = sum(1 for _, b in res if b)
print(f'TOTAL {n_ok}/{len(res)} OK')
