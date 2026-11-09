# TRIAGE (CHECK-F10): controllo indipendente dei limiti inferiori delta_N(K) (S10B-V9, OPF5C-Q1).
# Non usa opf5c_gd.pkl ne' s10b_delta.py. Due generatori di punti, entrambi riduzioni mod p di punti razionali:
#  (H) getti y_j = D^j u(0), u = 2 D^2 log f, f = sum_S a_S e^{(sum_{i in S} k_i) x} (Hirota, A_ij = ((ki-kj)/(ki+kj))^2),
#      k_i interi fissati (k fissato, non graduato): rango pieno mod p => nessuna relazione di grado <= d a quel k.
#  (AM) getti di u = 2 D^2 log theta_N (polinomi di Adler-Moser, livello k = 0, famiglia omogenea pesata):
#      rango pieno per ogni peso => nessuna relazione omogenea di grado <= d nulla sui getti AM.
#      (Vale come limite su Z_0 solo se i getti AM stanno nella chiusura dello strato principale di M_0: ipotesi.)
# Primo diverso da quello del pacchetto: p = 2^31 - 1.
import sys, random, itertools, time
import numpy as np
P = 2147483647
def inv(a): return pow(a % P, P - 2, P)

def series_log_jets(c, K):
    # c[n] = coefficienti di Taylor (gia' divisi per n!) di F(x0+h), n = 0..K+2; ritorna y_j = u^{(j)}(x0), u = 2(log F)''
    M = K + 3
    c0 = inv(c[0]); s = [x * c0 % P for x in c[:M]]
    # l = log s: l' s = s'  =>  n l_n = n s_n - sum_{i=1}^{n-1} i l_i s_{n-i}
    l = [0] * M
    for n in range(1, M):
        acc = n * s[n] % P
        for i in range(1, n): acc = (acc - i * l[i] * s[n - i]) % P
        l[n] = acc * inv(n) % P
    y = []; fact = 1
    for j in range(K + 1):
        if j > 0: fact = fact * j % P
        uj = 2 * (j + 2) * (j + 1) * l[j + 2] % P   # coeff. di h^j in u
        y.append(uj * fact % P)
    return y

def hirota_point(ks, K):
    N = len(ks)
    a = [random.randrange(1, P) for _ in range(N)]
    A = {}
    for i in range(N):
        for j in range(i + 1, N):
            A[i, j] = ((ks[i] - ks[j]) * inv(ks[i] + ks[j]) % P) ** 2 % P
    M = K + 3
    tau = [0] * M  # derivate n-esime in 0
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            w = 1
            for i in S: w = w * a[i] % P
            for i, j in itertools.combinations(S, 2): w = w * A[i, j] % P
            e = sum(ks[i] for i in S) % P
            pw = 1
            for n in range(M):
                tau[n] = (tau[n] + w * pw) % P; pw = pw * e % P
    fi = 1; c = []
    for n in range(M):
        if n > 0: fi = fi * inv(n) % P
        c.append(tau[n] * fi % P)
    return series_log_jets(c, K)

# --- polinomi mod p (coefficienti dal grado 0) ---
def pmul(A, B):
    r = [0] * (len(A) + len(B) - 1)
    for i, x in enumerate(A):
        if x:
            for j, z in enumerate(B): r[i + j] = (r[i + j] + x * z) % P
    return r
def pder(A): return [(i * A[i]) % P for i in range(1, len(A))] or [0]
def padd(A, B):
    n = max(len(A), len(B)); return [((A[i] if i < len(A) else 0) + (B[i] if i < len(B) else 0)) % P for i in range(n)]
def pscale(A, c): return [x * c % P for x in A]
def nullspace_mod(M):
    # M: lista di righe; ritorna base del nucleo
    M = [r[:] for r in M]; rows = len(M); cols = len(M[0]); piv = []; r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i][c]), None)
        if pr is None: continue
        M[r], M[pr] = M[pr], M[r]; iv = inv(M[r][c]); M[r] = [x * iv % P for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * z) % P for x, z in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]; basis = []
    for fc in free:
        v = [0] * cols; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-M[i][fc]) % P
        basis.append(v)
    return basis

def am_theta(N):
    # theta_0 = 1, theta_1 = x; theta_{n+1}' theta_{n-1} - theta_{n+1} theta_{n-1}' = (2n+1) theta_n^2
    th = [[1], [0, 1]]
    for n in range(1, N):
        d = (n + 1) * (n + 2) // 2
        tm, tn = th[n - 1], th[n]
        rhs = pscale(pmul(tn, tn), 2 * n + 1)
        # incognite c_0..c_{d-1} e c_d = 1: lineare
        L = len(tm) + d
        cols = []
        for i in range(d + 1):
            e = [0] * i + [1]
            col = padd(pmul(pder(e), tm), pscale(pmul(e, pder(tm)), P - 1))
            cols.append(col + [0] * (L - len(col)))
        rhs = rhs + [0] * (L - len(rhs))
        # sistema: sum_{i<d} c_i col_i = rhs - col_d ; nucleo dell'aumentata
        Mx = [[cols[i][r] for i in range(d)] + [(cols[d][r] - rhs[r]) % P] for r in range(L)]
        ns = nullspace_mod(Mx)
        # soluzioni con ultima coordinata 1; il nucleo omogeneo deve avere dim 1 (theta_{n-1})
        sol = [v for v in ns if v[-1]]
        assert len(ns) == 2 and sol, ('AM: dimensione inattesa', n, len(ns))
        hom = [v for v in ns if not v[-1]]
        v = sol[0]; iv = inv(v[-1]); part = [x * iv % P for x in v[:-1]] + [1]
        tau = random.randrange(P)
        if hom: part = padd(part, pscale(hom[0][:-1] + [0], tau))
        else:
            # entrambi i vettori hanno ultima coord != 0: combinazione per il nucleo omogeneo
            w0, w1 = ns; c = w0[-1] * inv(w1[-1]) % P
            h = [(x - c * z) % P for x, z in zip(w0, w1)]
            part = padd(part, pscale(h[:-1] + [0], tau))
        # verifica
        chk = padd(padd(pmul(pder(part), tm), pscale(pmul(part, pder(tm)), P - 1)), pscale(pmul(tn, tn), P - (2 * n + 1)))
        assert all(x == 0 for x in chk)
        th.append(part)
    return th[N]

def am_point(N, K):
    th = am_theta(N)
    while True:
        x0 = random.randrange(P)
        # Taylor di theta(x0 + h): coefficienti c_n = theta^{(n)}(x0)/n!
        c = []; cur = th[:]; fi = 1
        for n in range(K + 3):
            if n > 0: fi = fi * inv(n) % P
            val = 0
            for co in reversed(cur): val = (val * x0 + co) % P
            c.append(val * fi % P); cur = pder(cur)
        if c[0]: return series_log_jets(c, K)

def rank_mod(M):
    M = M.copy(); rows, cols = M.shape; r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        pr = r + nz[0]
        if pr != r: M[[r, pr]] = M[[pr, r]]
        M[r, c:] = (M[r, c:] * inv(int(M[r, c]))) % P
        below = r + 1 + np.nonzero(M[r + 1:, c])[0]
        if len(below):
            f = M[below, c].reshape(-1, 1)
            M[below, c:] = (M[below, c:] - (f * M[r, c:]) % P) % P
        r += 1
        if r == rows: break
    return r

def monomials(nv, d):
    out = []
    for tot in range(d + 1):
        for comb in itertools.combinations_with_replacement(range(nv), tot):
            e = [0] * nv
            for i in comb: e[i] += 1
            out.append(tuple(e))
    return out

def evalmat(pts, mons, d):
    pts = np.array(pts, dtype=object)
    npts, nv = len(pts), len(mons[0])
    pw = [[[1] * npts] for _ in range(nv)]
    for v in range(nv):
        for e in range(1, d + 1):
            pw[v].append([pw[v][e - 1][i] * int(pts[i][v]) % P for i in range(npts)])
    pwa = [[np.array(x, dtype=np.int64) for x in pw[v]] for v in range(nv)]
    M = np.ones((npts, len(mons)), dtype=np.int64)
    for j, m in enumerate(mons):
        col = np.ones(npts, dtype=np.int64)
        for v, e in enumerate(m):
            if e: col = (col * pwa[v][e]) % P
        M[:, j] = col
    return M

def run_hirota(ks, K, d):
    t0 = time.time(); mons = monomials(K + 1, d)
    pts = [hirota_point(ks, K) for _ in range(len(mons) + 15)]
    M = evalmat(pts, mons, d); rk = rank_mod(M)
    print('HIROTA N=%d k=%s K=%d d<=%d: monomi=%d rango=%d nullita=%d [%.1fs]' % (len(ks), ks, K, d, len(mons), rk, len(mons) - rk, time.time() - t0)); sys.stdout.flush()

def run_am(N, K, d):
    t0 = time.time(); mons = monomials(K + 1, d)
    wt = lambda m: sum((j + 2) * e for j, e in enumerate(m))
    byw = {}
    for m in mons:
        if sum(m) > 0: byw.setdefault(wt(m), []).append(m)
    mx = max(len(v) for v in byw.values())
    pts = [am_point(N, K) for _ in range(mx + 15)]
    bad = []
    for w in sorted(byw):
        ms = byw[w]; M = evalmat(pts[:len(ms) + 15], ms, d); rk = rank_mod(M)
        if rk < len(ms): bad.append((w, len(ms) - rk, min(sum(m) for m in ms)))
    if bad:
        # grado minimo di una relazione: ripeti con gradi crescenti sui pesi difettosi
        dmin = None
        for w, _, _ in bad:
            ms = sorted(byw[w], key=sum)
            for dd in range(1, d + 1):
                sub = [m for m in ms if sum(m) <= dd]
                if not sub: continue
                M = evalmat(pts[:len(sub) + 15], sub, d)
                if rank_mod(M) < len(sub):
                    if dmin is None or dd < dmin[0]: dmin = (dd, w)
                    break
        print('AM N=%d K=%d d<=%d: max classe=%d; relazioni trovate, grado minimo %d (peso %d) [%.1fs]' % (N, K, d, mx, dmin[0], dmin[1], time.time() - t0))
    else:
        print('AM N=%d K=%d d<=%d: max classe=%d; nessuna relazione omogenea di grado <= %d [%.1fs]' % (N, K, d, mx, d, time.time() - t0))
    sys.stdout.flush()

if __name__ == '__main__':
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 20261027)
    mode = sys.argv[1]
    if mode == 'small':
        for N, ks in [(1, [1]), (2, [1, 2]), (3, [1, 2, 4]), (4, [1, 2, 3, 5])]:
            run_hirota(ks, 2 * N, N); run_hirota(ks, 2 * N, N + 1)
        for N in [1, 2, 3, 4]:
            run_am(N, 2 * N, N + 1)
    elif mode == 'h5': run_hirota([1, 2, 3, 5, 7], 10, 5)
    elif mode == 'am5': run_am(5, 10, 6)
    elif mode == 'am58': run_am(5, 8, 9)
    elif mode == 'am59': run_am(5, 9, 7)
    elif mode == 'am4_5': run_am(4, 5, 9)
    elif mode == 'am6': run_am(6, 12, 6)
    elif mode == 'am611': run_am(6, 11, 7)
    elif mode == 'am58lb': run_am(5, 8, 8)
