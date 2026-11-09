# DEVIL-4 check 2: radius in eps of the TERM-ALONE inviscid flow e_B (needed by the A9 E_int)
# vs the t-uniform radius 2*pi*nu/osc(U0) claimed by F4L-P3 for the full Burgers flow.
# e_B: u = eps*sin(x0 - t*u). Lagrange inversion: [eps^n] u = (1/n) [w^(n-1)] sin(x0 - t w)^n.
# Numeric truncated power series (mpmath, 40 digits).
import mpmath as mp, random
mp.mp.dps = 40
x0 = mp.mpf(1)
NMAX = 40
def sin_series(tv, K):
    # sin(x0 - t w) = sum_k c_k w^k
    return [mp.sin(x0 + k*mp.pi/2) * (-tv)**k / mp.factorial(k) for k in range(K)]
def mul(a, b, K):
    return [mp.fsum(a[i]*b[k-i] for i in range(k+1)) for k in range(K)]
def coeffs(tv):
    s = sin_series(tv, NMAX)
    p = [mp.mpf(1)] + [mp.mpf(0)]*(NMAX-1)
    out = []
    for n in range(1, NMAX+1):
        p = mul(p, s, NMAX)
        out.append(p[n-1]/n)
    return out
print("t | root-test radius |a_n|^(-1/n) n=40, n=38 | t*radius")
for tv in [mp.mpf(0.5), mp.mpf(1), mp.mpf(2), mp.mpf(4)]:
    a = coeffs(tv)
    r40 = abs(a[39])**(-mp.mpf(1)/40); r38 = abs(a[37])**(-mp.mpf(1)/38)
    print(mp.nstr(tv,3), "|", mp.nstr(r40,6), mp.nstr(r38,6), "|", mp.nstr(tv*r40,6))
# DEVIL-4 check 3: F4L-P3 is the classical cumulant-strip lemma.
# Lemma: X with values in an interval of width w, any law: s -> log E e^{sX} analytic on |Im s| < pi/w,
# hence Taylor radius >= pi/w; equality for the symmetric two-point law (log cosh).
# Burgers: phi_eps = E_G[exp(-eps U0(Y)/2nu)], X = U0(Y), s = -eps/(2nu)  =>  radius |eps| >= 2 pi nu/osc(U0).
random.seed(4)
worst = mp.inf
for trial in range(300):
    p = [random.random() for _ in range(3)]; S = sum(p); p = [q/S for q in p]
    for z in mp.polyroots([p[2], p[1], p[0]]):        # atoms at 0, 1/2, 1 : z = e^{s/2}
        for k in range(-3, 4):
            worst = min(worst, abs(2*(mp.log(z) + 2j*mp.pi*k)))
print("min |zero| of E e^{sX} over 300 random 3-atom laws on [0,1]:", mp.nstr(worst, 10), " (pi =", mp.nstr(mp.pi, 10), ")")
print("symmetric two-point law 1/2+1/2e^s: zeros at s = i*pi*(2k+1), min |s| = pi  (the tanh case u0 = A*delta of F4L-P3)")
