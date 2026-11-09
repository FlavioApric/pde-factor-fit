# AUDIT del TRIAGE (CHECK-F10), voce S10B-V9: reimplementazione indipendente dei minoranti delta_N(K).
# Non importa nulla da tri_delta.py, s10b_delta.py, opf5c_*.  Primo p = 10^9+7 (diverso da 2^31-1 e 2147483629).
# Due generatori di punti di Z_0 (k = 0), entrambi riduzioni mod p di famiglie razionali su Q:
#  (S) strato principale S°_0 (parametrizzazione sigma di OPF5C-T1(b) a k = 0): U = prod(lambda + s_j^2),
#      V(-s_j^2) = s_j^(2N+1); getti y_0..y_{2N-1} = Psi_0^{-1}(U,V) per inversione triangolare dei polinomi di
#      Gelfand-Dickey; y_{2N} dal flusso di Mumford V' = (V^2+f)/U - (y_0+lambda)U.  Rigoroso mod L8 / L8'.
#  (W) Adler-Moser via funzione di Schur della partizione a scala (N,...,1) nei tempi dispari t_1 = x, t_3, ...:
#      costruzione diversa dalla ricorrenza di Adler-Moser usata dal triage.  Si controlla in ogni punto
#      l'identita' stazionaria 2GG''-G'^2+4(u+lambda)G^2 = 4 lambda^(2N+1) (=> getto in Z_0 e y_{2N} = Phi(0;.))
#      e che U = G(x0) sia squarefree (=> punto di S°_0).
# Uso: python audit_delta.py MODE N K d [seed]   MODE in {S, W, Wcheck}
import sys, random, itertools, time
import numpy as np
import sympy as sp

P = 1000000007
def inv(a): return pow(a % P, P - 2, P)

# ---------- polinomi di Gelfand-Dickey simbolici: R_0 = 1, R_1 = -y0/2, R_2 = y2/8 + 3 y0^2/8, ... ----------
def gd_polys(N, nvar):
    Y = sp.symbols('y0:%d' % nvar)
    def D(e):
        e = sp.expand(e)
        return sp.expand(sum(sp.diff(e, Y[j]) * Y[j + 1] for j in range(nvar - 1)))
    R = [sp.Integer(1)]
    for j in range(1, N + 1):
        acc = 0
        for a in range(0, j):
            b = j - 1 - a
            acc += 2 * R[a] * D(D(R[b])) - D(R[a]) * D(R[b]) + 4 * Y[0] * R[a] * R[b]
        for a in range(1, j):
            acc += 4 * R[a] * R[j - a]
        R.append(sp.expand(-sp.Rational(1, 8) * acc))
    return Y, R, D

def to_modp_poly(expr, Y):
    pol = sp.Poly(expr, *Y)
    out = []
    for mon, c in pol.terms():
        c = sp.Rational(c)
        out.append((mon, int(c.p) % P * inv(int(c.q)) % P))
    return out

def ev(pp, y):
    s = 0
    for mon, c in pp:
        t = c
        for i, e in enumerate(mon):
            if e: t = t * pow(y[i], e, P) % P
        s = (s + t) % P
    return s

# ---------- polinomi in lambda mod p (coefficienti dal grado 0) ----------
def pmul(A, B):
    r = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B): r[i + j] = (r[i + j] + a * b) % P
    return r
def pdivmod(A, B):
    A = A[:]; q = [0] * max(1, len(A) - len(B) + 1); ib = inv(B[-1])
    for i in range(len(A) - len(B), -1, -1):
        c = A[i + len(B) - 1] * ib % P; q[i] = c
        for j, b in enumerate(B): A[i + j] = (A[i + j] - c * b) % P
    return q, A[:len(B) - 1]

# ---------- generatore (S): strato principale ----------
class GenS:
    def __init__(self, N):
        self.N = N
        Y, R, D = gd_polys(N, 2 * N + 3)
        self.u = [to_modp_poly(R[j], Y) for j in range(1, N + 1)]            # u_j = g_j
        self.v = [to_modp_poly(D(R[j]) / 2, Y) for j in range(1, N + 1)]     # v_j = D g_j / 2
        self.vNp = to_modp_poly(D(D(R[N])) / 2, Y)                            # v_N' = D^2 g_N / 2
        # coefficienti direttori: g_j lineare in y_{2j-2}, D g_j/2 in y_{2j-1}, D^2 g_N/2 in y_{2N}
        self.cu = [sp.Rational(sp.expand(R[j]).coeff(Y[2 * j - 2], 1)) for j in range(1, N + 1)]
        self.cv = [sp.Rational(sp.expand(D(R[j]) / 2).coeff(Y[2 * j - 1], 1)) for j in range(1, N + 1)]
        self.cN = sp.Rational(sp.expand(D(D(R[N])) / 2).coeff(Y[2 * N], 1))
        for c in self.cu + self.cv + [self.cN]: assert c != 0
        self.Y = Y
    def point(self, K):
        N = self.N
        while True:
            s = [random.randrange(1, P) for _ in range(N)]
            mu = [(-x * x) % P for x in s]
            if len(set(mu)) == N: break
        U = [1]
        for m in mu: U = pmul(U, [(-m) % P, 1])          # prod (lambda - mu_j)
        nu = [pow(x, 2 * N + 1, P) for x in s]           # V(mu_j) = s_j^(2N+1), nu^2 + mu^(2N+1) = 0
        # interpolazione di Lagrange: V di grado < N
        V = [0] * N
        for j in range(N):
            num = [1]; den = 1
            for i in range(N):
                if i != j: num = pmul(num, [(-mu[i]) % P, 1]); den = den * (mu[j] - mu[i]) % P
            c = nu[j] * inv(den) % P
            for t in range(N): V[t] = (V[t] + c * num[t]) % P
        f = [0] * (2 * N + 1) + [1]
        r = pdivmod(padd(pmul(V, V), f), U)[1]
        assert all(x == 0 for x in r), 'U non divide V^2+f'
        # coordinate: U = lambda^N + sum u_j lambda^{N-j}; V = sum v_j lambda^{N-j}
        ut = [U[N - j] for j in range(1, N + 1)]; vt = [V[N - j] for j in range(1, N + 1)]
        y = [0] * (2 * N + 3)
        for j in range(1, N + 1):
            # risolvi y_{2j-2} da u_j, poi y_{2j-1} da v_j (forma triangolare)
            k = 2 * j - 2; y[k] = 0
            rest = ev(self.u[j - 1], y); c = self.cu[j - 1]
            y[k] = (ut[j - 1] - rest) * int(c.q) % P * inv(int(c.p)) % P
            k = 2 * j - 1; y[k] = 0
            rest = ev(self.v[j - 1], y); c = self.cv[j - 1]
            y[k] = (vt[j - 1] - rest) * int(c.q) % P * inv(int(c.p)) % P
        for j in range(1, N + 1):
            assert ev(self.u[j - 1], y) == ut[j - 1] and ev(self.v[j - 1], y) == vt[j - 1]
        if K >= 2 * N:
            assert K == 2 * N
            Q, rem = pdivmod(padd(pmul(V, V), f), U)
            rhs = padd(Q, [(-x) % P for x in pmul([y[0], 1], U)])   # (V^2+f)/U - (y0+lambda)U
            target = rhs[0]                                          # coefficiente di lambda^0 = v_N'
            y[2 * N] = 0; rest = ev(self.vNp, y); c = self.cN
            y[2 * N] = (target - rest) * int(c.q) % P * inv(int(c.p)) % P
            # consistenza: anche gli altri coefficienti del flusso devono valere (v_j' = v_{j}' calcolato dai getti)
        return y[:K + 1]

def padd(A, B):
    n = max(len(A), len(B)); return [((A[i] if i < len(A) else 0) + (B[i] if i < len(B) else 0)) % P for i in range(n)]

# ---------- generatore (W): Schur a scala ----------
def h_coeffs(x, ts, M):
    # sum_k h_k z^k = exp(x z + sum_j ts[j] z^(2j+3)), k = 0..M
    c = [0] * (M + 1); c[1] = x % P
    for j, t in enumerate(ts):
        e = 2 * j + 3
        if e <= M: c[e] = t
    h = [1] + [0] * M
    for k in range(1, M + 1):
        acc = 0
        for i in range(1, k + 1):
            if c[i]: acc = (acc + i * c[i] * h[k - i]) % P
        h[k] = acc * inv(k) % P
    return h

def det_mod(A):
    A = [r[:] for r in A]; n = len(A); d = 1
    for c in range(n):
        pr = next((i for i in range(c, n) if A[i][c]), None)
        if pr is None: return 0
        if pr != c: A[c], A[pr] = A[pr], A[c]; d = -d
        d = d * A[c][c] % P; iv = inv(A[c][c])
        for i in range(c + 1, n):
            if A[i][c]:
                f = A[i][c] * iv % P
                A[i] = [(a - f * b) % P for a, b in zip(A[i], A[c])]
    return d % P

def theta_val(N, x, ts):
    h = h_coeffs(x, ts, 2 * N)
    lam = list(range(N, 0, -1))
    H = lambda k: h[k] if 0 <= k <= 2 * N else 0
    return det_mod([[H(lam[i] - i + j) for j in range(N)] for i in range(N)])

def interp_shift(N, x0, ts):
    # coefficienti di theta(x0 + h) in h, grado D = N(N+1)/2, per interpolazione su h = 0..D
    Dg = N * (N + 1) // 2
    xs = list(range(Dg + 1)); vals = [theta_val(N, x0 + a, ts) for a in xs]
    # Newton / sistema di Vandermonde
    M = [[pow(a, e, P) for e in range(Dg + 1)] + [v] for a, v in zip(xs, vals)]
    n = Dg + 1
    for c in range(n):
        pr = next(i for i in range(c, n) if M[i][c]); M[c], M[pr] = M[pr], M[c]
        iv = inv(M[c][c]); M[c] = [a * iv % P for a in M[c]]
        for i in range(n):
            if i != c and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % P for a, b in zip(M[i], M[c])]
    return [M[i][n] for i in range(n)]

def ser_mul(A, B, L):
    r = [0] * L
    for i in range(min(L, len(A))):
        if A[i]:
            for j in range(min(L - i, len(B))): r[i + j] = (r[i + j] + A[i] * B[j]) % P
    return r
def ser_der(A): return [(i * A[i]) % P for i in range(1, len(A))] + [0]

def u_series(c, L):
    # c = coefficienti di theta(x0+h); ritorna u(x0+h) = 2 (log theta)'' troncata a L termini
    M = L + 3
    c = (c + [0] * M)[:M]; c0 = inv(c[0]); s = [a * c0 % P for a in c]
    l = [0] * M
    for n in range(1, M):
        acc = n * s[n] % P
        for i in range(1, n): acc = (acc - i * l[i] * s[n - i]) % P
        l[n] = acc * inv(n) % P
    return [2 * (j + 2) * (j + 1) * l[j + 2] % P for j in range(L)]

class GenW:
    def __init__(self, N): self.N = N
    def raw(self):
        N = self.N
        while True:
            ts = [random.randrange(P) for _ in range(N - 1)]
            x0 = random.randrange(P)
            c = interp_shift(N, x0, ts)
            if c[0]: return c
    def point(self, K):
        c = self.raw(); L = K + 1
        u = u_series(c, L); y = []; fact = 1
        for j in range(L):
            if j: fact = fact * j % P
            y.append(u[j] * fact % P)
        return y
    def check(self):
        # identita' stazionaria a k = 0 come serie in h, e U(x0) squarefree
        N = self.N; L = 6 * N + 8
        c = self.raw(); u = u_series(c, L)
        R = [[1] + [0] * (L - 1)]
        for j in range(1, N + 1):
            acc = [0] * L
            for a in range(j):
                b = j - 1 - a
                t1 = ser_mul(R[a], ser_der(ser_der(R[b])), L)
                t2 = ser_mul(ser_der(R[a]), ser_der(R[b]), L)
                t3 = ser_mul(u, ser_mul(R[a], R[b], L), L)
                acc = [(x + 2 * p1 - p2 + 4 * p3) % P for x, p1, p2, p3 in zip(acc, t1, t2, t3)]
            for a in range(1, j):
                t = ser_mul(R[a], R[j - a], L); acc = [(x + 4 * q) % P for x, q in zip(acc, t)]
            R.append([(-x) * inv(8) % P for x in acc])
        # G(lambda) = sum_j R_j lambda^{N-j}; E = 2GG''-G'^2+4uG^2+4 lambda G^2 - 4 lambda^{2N+1}
        G = [R[N - e] for e in range(N + 1)]       # G[e] = coeff di lambda^e (serie in h)
        valid = L - 2 * (2 * N + 1) - 4           # ordini in h affidabili (ogni derivata ne consuma 1)
        E = {}
        for e1 in range(N + 1):
            for e2 in range(N + 1):
                A, B = G[e1], G[e2]
                t = [(2 * p - q + 4 * r) % P for p, q, r in zip(ser_mul(A, ser_der(ser_der(B)), L), ser_mul(ser_der(A), ser_der(B), L), ser_mul(u, ser_mul(A, B, L), L))]
                E[e1 + e2] = [(a + b) % P for a, b in zip(E.get(e1 + e2, [0] * L), t)]
                t = [4 * x % P for x in ser_mul(A, B, L)]
                E[e1 + e2 + 1] = [(a + b) % P for a, b in zip(E.get(e1 + e2 + 1, [0] * L), t)]
        E[2 * N + 1][0] = (E[2 * N + 1][0] - 4) % P
        bad = [(e, i) for e in E for i in range(max(valid, 1)) if E[e][i]]
        U = [R[N - e][0] for e in range(N + 1)]  # coefficienti di lambda^e in x0
        dU = [(e * U[e]) % P for e in range(1, N + 1)]
        g = U[:]; hpol = dU[:]
        while any(hpol):
            while hpol and hpol[-1] == 0: hpol.pop()
            if not hpol: break
            g, hpol = hpol, pdivmod(g, hpol)[1]
            while hpol and hpol[-1] == 0: hpol.pop()
        while g and g[-1] == 0: g.pop()
        squarefree = (len(g) == 1)
        return len(bad) == 0, valid, squarefree, U[0] != 0

# ---------- rango mod p ----------
def rank_mod(M):
    M = M.copy() % P; rows, cols = M.shape; r = 0
    for c in range(cols):
        if r == rows: break
        nz = np.flatnonzero(M[r:, c])
        if nz.size == 0: continue
        pr = r + nz[0]
        if pr != r: M[[r, pr]] = M[[pr, r]]
        M[r] = (M[r] * inv(int(M[r, c]))) % P
        idx = r + 1 + np.flatnonzero(M[r + 1:, c])
        if idx.size:
            f = M[idx, c].reshape(-1, 1)
            M[idx] = (M[idx] - (f * M[r]) % P) % P
        r += 1
    return r

def weight_classes(K, d):
    byw = {}
    for tot in range(1, d + 1):
        for comb in itertools.combinations_with_replacement(range(K + 1), tot):
            w = sum(j + 2 for j in comb)
            byw.setdefault(w, []).append(comb)
    return byw

def evalcols(pts, monos):
    A = np.array(pts, dtype=np.int64)
    M = np.ones((len(pts), len(monos)), dtype=np.int64)
    for j, comb in enumerate(monos):
        col = np.ones(len(pts), dtype=np.int64)
        for v in comb: col = (col * A[:, v]) % P
        M[:, j] = col
    return M

def run(mode, N, K, d):
    t0 = time.time()
    gen = GenS(N) if mode == 'S' else GenW(N)
    byw = weight_classes(K, d); mx = max(len(v) for v in byw.values())
    pts = [gen.point(K) for _ in range(mx + 20)]
    tgen = time.time() - t0
    deficient = []
    for w in sorted(byw):
        ms = byw[w]; rk = rank_mod(evalcols(pts[:len(ms) + 20], ms))
        if rk < len(ms): deficient.append((w, len(ms) - rk, min(len(m) for m in ms)))
    # grado minimo di una relazione (se esiste) tra i pesi difettosi
    dmin = None
    for w, _, _ in deficient:
        ms = sorted(byw[w], key=len)
        for dd in range(1, d + 1):
            sub = [m for m in ms if len(m) <= dd]
            if sub and rank_mod(evalcols(pts[:len(sub) + 20], sub)) < len(sub):
                if dmin is None or dd < dmin[0]: dmin = (dd, w)
                break
    msg = ('%s N=%d K=%d d<=%d p=%d: classi=%d max=%d punti=%d; ' % (mode, N, K, d, P, len(byw), mx, len(pts)))
    msg += ('nessuna relazione omogenea pesata di grado <= %d' % d) if dmin is None else ('relazione di grado minimo %d (peso %d)' % dmin)
    msg += ' [gen %.1fs, tot %.1fs]' % (tgen, time.time() - t0)
    print(msg); sys.stdout.flush()

if __name__ == '__main__':
    mode = sys.argv[1]; N = int(sys.argv[2])
    random.seed(int(sys.argv[5]) if len(sys.argv) > 5 else 777)
    if mode == 'Wcheck':
        g = GenW(N); res = [g.check() for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 5)]
        print('Wcheck N=%d: identita stazionaria k=0 (ordini h verificati=%d) %s; U(x0) squarefree %s; U(0)!=0 %s'
              % (N, res[0][1], all(r[0] for r in res), all(r[2] for r in res), all(r[3] for r in res)))
    else:
        run(mode, N, int(sys.argv[3]), int(sys.argv[4]))
