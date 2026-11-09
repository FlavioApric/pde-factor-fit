# audit_opana.py — S-CHECK-15, red team indipendente per OP-ANA (OPA-T1/C1, OPA-L2/T2, OPA-T3/P3, OPA-P4)
# Scritto da zero (non usa gli script di work/OP-ANA). Solo controllo, non prova.
# Uso: D:\ProblemaBase\.venv\Scripts\python.exe -I audit_opana.py [sezioni]   (sezioni: A B C D E F G H; default tutte)
import sys, time, math
sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import mpmath as mp
from scipy import integrate, special, linalg

SECT = sys.argv[1] if len(sys.argv) > 1 else "ABCDEFGH"
NOK = [0, 0]
def check(name, ok, info=""):
    NOK[1] += 1
    if ok: NOK[0] += 1
    print(("OK  " if ok else "FAIL") + " | " + name + (" | " + info if info else ""), flush=True)

L = lambda z: 1.0 / (1.0 + np.exp(-z))

# ---------------------------------------------------------------- A: Burgers, Cole–Hopf indipendente
def burgers_case(name, u0, U0, du0, d2u0, d3u0, heat, t, nus, xs_guess):
    unorm = np.max(np.abs(u0(np.linspace(0, 2*np.pi, 4001))))
    def Phi(x, y): return U0(y) + (x - y)**2 / (2*t)
    def argmin_branch(x, a0):
        a = a0
        for _ in range(60):
            F = a + t*u0(a) - x; Fp = 1 + t*du0(a)
            a = a - F/Fp
        return a
    ygrid_c = np.linspace(-np.pi - t*unorm - 2, 3*np.pi + t*unorm + 2, 200001)
    def global_min(x):
        v = Phi(x, ygrid_c); i = np.argmin(v)
        return argmin_branch(x, ygrid_c[i])
    # shock location: Delta(x)=Phi(a+)-Phi(a-) = 0, by bisection using branches near xs_guess
    am = global_min(xs_guess - 0.3); ap = global_min(xs_guess + 0.3)
    def branches(x):
        return argmin_branch(x, am + (x - xs_guess + 0.3)*0), argmin_branch(x, ap)
    lo, hi = xs_guess - 0.3, xs_guess + 0.3
    for _ in range(100):
        mid = 0.5*(lo + hi)
        a_m = argmin_branch(mid, am); a_p = argmin_branch(mid, ap)
        D = Phi(mid, a_p) - Phi(mid, a_m)
        if D > 0: lo = mid
        else: hi = mid
    xs = 0.5*(lo + hi); a_m = argmin_branch(xs, am); a_p = argmin_branch(xs, ap)
    Jm = 1 + t*du0(a_m); Jp = 1 + t*du0(a_p); rho = 0.5*np.log(Jm/Jp); Dj = (a_p - a_m)/t
    # smooth integrals over a in (a_p, a_m + 2pi): dx = J da
    f_uv = lambda a: t*abs(d2u0(a))/(1 + t*du0(a))
    I_uv = integrate.quad(f_uv, a_p, a_m + 2*np.pi, limit=400, epsabs=1e-12)[0]
    def f_add(a):
        x = a + t*u0(a); J = 1 + t*du0(a)
        return abs(t*d2u0(a)/J**2 - t*d2u0(x))*J
    I_add = integrate.quad(f_add, a_p, a_m + 2*np.pi, limit=400, epsabs=1e-12)[0]
    layer = 4*np.log(2*np.cosh(rho/2))
    Luv, Ladd = I_uv + layer, I_add + layer
    print(f"[{name}] t={t} x_s={xs:.6f} a-={a_m:.6f} a+={a_p:.6f} J-={Jm:.5f} J+={Jp:.5f} rho={rho:.5f} D={Dj:.5f}")
    print(f"[{name}] predetto: smooth_uv={I_uv:.5f} smooth_add={I_add:.5f} layer={layer:.5f} Lambda_uv={Luv:.5f} Lambda_add={Ladd:.5f}")
    res = []
    for nu in nus:
        h = 0.0015 if nu >= 1e-3 else 0.001
        # x grid on [xs-2pi, xs] (periodic cell), fine near both ends (the shock)
        def side_grid():
            fine = np.linspace(0, 0.08, 4001)
            coarse = np.linspace(0.08, 2*np.pi - 0.08, 3001)[1:-1]
            g = np.concatenate([fine, coarse, 2*np.pi - fine[::-1]])
            return xs - 2*np.pi + g
        X = side_grid()
        # minimizer branch: for x in (xs-2pi, xs): continuous branch starting from a+ - 2pi to a-
        A = np.empty_like(X); a_cur = a_p - 2*np.pi
        for i, x in enumerate(X):
            a_cur = argmin_branch(x, a_cur); A[i] = a_cur
        uB = (X - A)/t
        uS = np.empty_like(X)
        for i, x in enumerate(X):
            y = np.arange(x - t*unorm - 1.5, x + t*unorm + 1.5, h)
            p = Phi(x, y); p = p - p.min()
            w = np.exp(-p/(2*nu))
            uS[i] = (x - np.trapezoid(w*y, y)/np.trapezoid(w, y))/t
        Eadd = uS - heat(X, nu) - uB + u0(X)
        n_uv = np.trapezoid(np.abs(uS - uB), X)/nu
        n_add = np.trapezoid(np.abs(Eadd), X)/nu
        res.append((nu, n_uv, n_add))
        print(f"[{name}] nu={nu:.1e}: ||u-v||_1/nu={n_uv:.5f}  ||Eadd||_1/nu={n_add:.5f}", flush=True)
    # Richardson in nu^(1/2) on the last two (remainder O(nu^{1/2}) expected from O(nu^{3/2}) terms)
    (n1, a1, b1), (n2, a2, b2) = res[-2], res[-1]
    # differenze successive dimezzate ⇒ resto O(nu) nel rapporto (cioè O(nu^2) nella norma): Richardson lineare
    ext_uv = 2*a2 - a1; ext_add = 2*b2 - b1
    print(f"[{name}] estrapolato (Richardson, resto ~nu): uv={ext_uv:.5f} add={ext_add:.5f}")
    check(f"OPA-T1 {name}: Lambda_uv (estrapolato entro 1e-3 rel., misura entro 1%)", abs(ext_uv - Luv)/Luv < 1e-3 and abs(a2 - Luv)/Luv < 1e-2, f"mis {a2:.5f} / estr {ext_uv:.5f} vs pred {Luv:.5f}")
    check(f"OPA-T1 {name}: Lambda_add (estrapolato entro 1e-3 rel., misura entro 1%)", abs(ext_add - Ladd)/Ladd < 1e-3 and abs(b2 - Ladd)/Ladd < 1e-2, f"mis {b2:.5f} / estr {ext_add:.5f} vs pred {Ladd:.5f}")
    return rho, Luv, Ladd

if "A" in SECT:
    t0 = time.time()
    # sin x, t = 2
    burgers_case("sin", np.sin, lambda y: 1 - np.cos(y), np.cos, lambda y: -np.sin(y), lambda y: -np.cos(y),
                 lambda X, nu: np.exp(-nu*2.0)*np.sin(X), 2.0, [2e-3, 1e-3, 5e-4], np.pi)
    # asimmetrico: sin x + 0.3 cos 2x, t = 1.5
    u0 = lambda y: np.sin(y) + 0.3*np.cos(2*y)
    U0 = lambda y: 1 - np.cos(y) + 0.15*np.sin(2*y)
    du0 = lambda y: np.cos(y) - 0.6*np.sin(2*y)
    d2u0 = lambda y: -np.sin(y) - 1.2*np.cos(2*y)
    d3u0 = lambda y: -np.cos(y) + 2.4*np.sin(2*y)
    heat = lambda X, nu: np.exp(-nu*1.5)*np.sin(X) + 0.3*np.exp(-4*nu*1.5)*np.cos(2*X)
    # shock guess: locate jump of global minimizer
    tt = 1.5
    yy = np.linspace(-12, 18, 300001)
    xg = np.linspace(0, 2*np.pi, 2001); amin = np.array([yy[np.argmin(U0(yy) + (x - yy)**2/(2*tt))] for x in xg])
    jumps = np.where(np.diff(amin) > 0.2)[0]
    print("[asym] salti del minimizzante sulla griglia in x:", [round(float(xg[j]), 4) for j in jumps])
    check("OPA-T1 asym: un solo shock per periodo", len(jumps) == 1)
    xs_g = float(xg[jumps[0]])
    burgers_case("asym", u0, U0, du0, d2u0, d3u0, heat, tt, [2e-3, 1e-3, 5e-4], xs_g)
    print(f"[A] tempo {time.time()-t0:.0f}s", flush=True)

# ---------------------------------------------------------------- B: profilo logistico
if "B" in SECT:
    for rho in [0.0, -0.3035, 0.7, 2.0]:
        f = lambda z: abs((1.0 if z > 0 else 0.0) - 1/(1 + math.exp(-(z + rho))))
        val = 2*(integrate.quad(f, -60, 0, limit=200)[0] + integrate.quad(f, 0, 60, limit=200)[0])
        check(f"OPA-T1 strato: 2∫|H-L(z+rho)| = 4log(2cosh(rho/2)), rho={rho}", abs(val - 4*math.log(2*math.cosh(rho/2))) < 1e-8,
              f"{val:.10f} vs {4*math.log(2*math.cosh(rho/2)):.10f}")
    # forma con D: nu*D*∫|H - L(Dw/2+rho)|dw indipendente da D
    for Dv in [0.3, 1.9]:
        g = lambda w: abs((1.0 if w > 0 else 0.0) - 1/(1 + math.exp(-(Dv*w/2 + 0.5))))
        val = Dv*(integrate.quad(g, -400/Dv, 0, limit=300)[0] + integrate.quad(g, 0, 400/Dv, limit=300)[0])
        check(f"OPA-T1 strato indipendente da D (D={Dv})", abs(val - 4*math.log(2*math.cosh(0.25))) < 1e-7, f"{val:.9f}")
    # segno di rho: due pozzi gaussiani esatti con curvature J-/t, J+/t e livelli uguali: peso relativo = sqrt(J-/J+)
    Jm, Jp, tt, nu = 1.0298, 1.8895, 1.5, 1e-4
    zm = integrate.quad(lambda z: math.exp(-(Jm/tt)*z*z/2/(2*nu)), -1, 1)[0]
    zp = integrate.quad(lambda z: math.exp(-(Jp/tt)*z*z/2/(2*nu)), -1, 1)[0]
    check("OPA-T1 rho = log(Z+/Z-)... : log(Z+/Z-) = ½log(J-/J+)", abs(math.log(zp/zm) - 0.5*math.log(Jm/Jp)) < 1e-9,
          f"{math.log(zp/zm):.6f} vs {0.5*math.log(Jm/Jp):.6f}")

# ---------------------------------------------------------------- C: Lemma 2 (Laplace con resti)
if "C" in SECT:
    mp.mp.dps = 30
    for (p, q, r4) in [(1.0, 6.0, 3.0), (2.5, -1.3, 0.0), (0.7, 0.4, -0.5)]:
        psi = lambda z: p*z**2/2 + q*z**3/6 + r4*z**4/24
        dl = 0.25
        errs = []
        for eps in [1e-2, 3e-3, 1e-3, 3e-4]:
            I0 = mp.quad(lambda z: mp.e**(-psi(z)/eps), [-dl, 0, dl])
            I1 = mp.quad(lambda z: z*mp.e**(-psi(z)/eps), [-dl, 0, dl])
            mean = I1/I0
            pred = -eps*q/(2*p**2)
            errs.append(float(abs(mean - pred))/eps**1.5)
            i0r = float(I0/mp.sqrt(2*mp.pi*eps/p)) - 1
        check(f"Lemma 2(ii) p={p},q={q}: |<z>+eps q/2p^2| = O(eps^1.5)", max(errs[1:]) <= 1.5*errs[0] + 1e-9,
              "err/eps^1.5 = " + ", ".join(f"{e:.3g}" for e in errs))

# ---------------------------------------------------------------- D: OPA-C1 forma chiusa e divergenza
if "D" in SECT:
    for t in [1.2, 2.0, 3.7]:
        b = float(mp.findroot(lambda b: b - t*mp.sin(b), 2.0 if t > 1.5 else 1.0))
        closed = 2*math.log((1 + t)/(1 - t*math.cos(b)))
        quad = integrate.quad(lambda a: t*abs(math.sin(a))/(1 + t*math.cos(a)), -(math.pi - b), math.pi - b, points=[0], limit=300)[0]
        check(f"OPA-C1 forma chiusa t={t}", abs(closed - quad) < 1e-9, f"{closed:.8f} vs {quad:.8f}; 1-t cos b={1-t*math.cos(b):.4f}>0")
    for t in [1.1, 1.01, 1.001, 1.0001]:
        b = float(mp.findroot(lambda b: b - t*mp.sin(b), math.sqrt(6*(t - 1))))
        closed = 2*math.log((1 + t)/(1 - t*math.cos(b)))
        print(f"[D] t={t}: Lambda_smooth={closed:.5f}  2log(1/(t-1))={2*math.log(1/(t-1)):.5f}  diff={closed-2*math.log(1/(t-1)):.2e}")
    check("OPA-C1 ⇒ Λ_smooth(t) - 2log(1/(t-1)) → 0 (divergenza dimostrabile dalla forma chiusa)", abs(closed - 2*math.log(1/(t-1))) < 1e-3)
    # g(t) = arccos(-1/t)+sqrt(t^2-1) > pi per t>1
    check("OPA-C1 F(a_c) > pi per t>1", all(math.acos(-1/t) + math.sqrt(t*t - 1) > math.pi for t in [1.0001, 1.5, 3, 10]))

# ---------------------------------------------------------------- E: OPA-L2 (commutatore, nucleo, integrale del nucleo)
if "E" in SECT:
    Lq, D = 1.0, 1.0
    M = 4000; n = np.arange(1, M + 1); mu = n*np.pi/Lq
    xg = np.linspace(0, Lq, 2001)
    f = lambda x: x*(Lq - x)*(2 - x)          # f in H^1_0, f'(0),f'(L) != 0
    fp = lambda x: (Lq - x)*(2 - x) - x*(2 - x) - x*(Lq - x)
    s = 1e-3
    # sine coeffs of f, cosine coeffs of f' by quadrature
    xx = np.linspace(0, Lq, 40001)
    fn = np.array([np.trapezoid(f(xx)*np.sqrt(2/Lq)*np.sin(m*xx), xx) for m in mu[:400]])
    gn = np.array([np.trapezoid(fp(xx)*np.sqrt(2/Lq)*np.cos(m*xx), xx) for m in mu[:400]])
    g0 = np.trapezoid(fp(xx), xx)/np.sqrt(Lq)
    check("OPA-L2(a) <f',c_n> = mu_n f_n, <f',c_0> = 0", np.max(np.abs(gn - mu[:400]*fn)) < 1e-6 and abs(g0) < 1e-8,
          f"max err {np.max(np.abs(gn - mu[:400]*fn)):.2e}")
    # (c) kernel = images; and integral of kernel vs erfc formula
    G = lambda sg, z: np.exp(-z**2/(4*sg))/np.sqrt(4*np.pi*sg)
    for s in [1e-3, 0.05, 0.5]:
        x0, y0 = 0.13, 0.71
        modal = 1/Lq + (2/Lq)*np.sum(np.exp(-D*mu**2*s)*np.cos(mu*(x0 + y0)))
        imgs = 2*sum(G(D*s, x0 + y0 - 2*j*Lq) for j in range(-40, 41))
        check(f"OPA-L2(c) nucleo K^N-K^D = 2Σ_j G (s={s})", abs(modal - imgs) < 1e-8*max(1, abs(imgs)), f"{modal:.10f} vs {imgs:.10f}")
        # integral in y: exact value is 1 - S^D(s)1(x)
        SD1 = np.sum(np.exp(-D*mu**2*s)*np.sqrt(2/Lq)*np.sin(mu*x0)*(np.sqrt(2/Lq)*(1 - np.cos(mu*Lq))/mu))
        exact = 1 - SD1
        erf_form = special.erfc(x0/(2*np.sqrt(D*s))) + special.erfc((Lq - x0)/(2*np.sqrt(D*s)))
        print(f"[E] s={s}: ∫k_s dy = 1 - S^D1 = {exact:.10f}; erfc(x/2√Ds)+erfc((L-x)/2√Ds) = {erf_form:.10f}")
        check(f"OPA-L2(c) ∫k_s dy ≤ erfc+erfc (s={s}) [usato in T2(i)]", exact <= erf_form + 1e-12)
        if s == 0.5:
            check("OPA-L2(c) uguaglianza ∫k_s dy = erfc+erfc (attesa FALSA per s non piccolo: rilievo L2-1)",
                  abs(exact - erf_form) > 1e-2, f"differenza {erf_form - exact:.4f}")

# ---------------------------------------------------------------- F: OPA-T2 costanti e serie modale indipendente
def B_alpha(alpha, k):
    k = np.asarray(k, dtype=float)
    if alpha == 0: return -np.expm1(-k**2)/k
    if alpha == 1: return (2*k/np.sqrt(np.pi) - 2*special.dawsn(k)/np.sqrt(np.pi))/k**2
    if alpha == 2: return (2*k**2 + 2*np.expm1(-k**2))/k**3
def N_alpha(alpha):
    def Zhat(k):
        return integrate.quad(lambda s: np.exp(-k*k*(1 - s))*s**((alpha + 1)/2)*B_alpha(alpha, k*np.sqrt(s)), 0, 1, limit=200, epsabs=1e-14)[0]
    val = integrate.quad(lambda k: Zhat(k)**2, 1e-9, np.inf, limit=400, epsabs=1e-14)[0]
    return math.sqrt(2/np.pi*val)
if "F" in SECT:
    t0 = time.time()
    J = integrate.quad(lambda y: y**-3.5*(-np.expm1(-y) - y*np.exp(-y))**2, 0, np.inf, limit=400, epsabs=1e-14)[0]
    N0, N1, N2 = N_alpha(0), N_alpha(1), N_alpha(2)
    print(f"[F] J={J:.6f} sqrt(J/pi)={math.sqrt(J/math.pi):.6f}  N0={N0:.6f} N1={N1:.6f} N2={N2:.6f}")
    check("OPA-T2 N0 = sqrt(J/pi) = 0.234005", abs(N0 - math.sqrt(J/math.pi)) < 1e-6 and abs(N0 - 0.234005) < 2e-6)
    check("OPA-T2 N1 = 0.162622", abs(N1 - 0.162622) < 2e-6, f"{N1:.7f}")
    Cs = 1.6*math.sqrt(2*(2 - math.sqrt(2))/math.sqrt(math.pi))
    check("OPA-T2(i) C_* = (8/5)(2(2-√2)/√π)^{1/2} ≈ 1.30 (tabella: 1.31, maggiorante)", abs(Cs - 1.3008) < 1e-3, f"{Cs:.5f}")
    # modal E^{mult,(1)} on (0,1), c=D=1
    def Emodal(u, t, M):
        n = np.arange(1, M + 1); lam = (n*np.pi)**2
        m_ = n[:, None]; k_ = n[None, :]
        with np.errstate(divide='ignore', invalid='ignore'):
            V = np.where((m_ + k_) % 2 == 1, -4.0*m_*k_/(m_**2 - k_**2), 0.0)
            lm = lam[:, None]; ln = lam[None, :]
            phi = np.where(m_ != k_, (np.exp(-ln*t) - np.exp(-lm*t))/(lm - ln), 0.0)
        Wm = (V*(phi - t*np.exp(-lm*t))) @ u[:M]
        return np.linalg.norm(Wm)
    M = 3000; nn = np.arange(1, M + 1)
    # e1
    u = np.zeros(M); u[0] = 1.0
    pred = 2*np.pi*N0
    vals = [Emodal(u, t, M)/t**1.25 for t in [1e-3, 1e-4, 1e-5]]
    check("OPA-T2 e1: ||E||/t^{5/4} → 2πN0 = 1.47030", abs(vals[-1] - pred)/pred < 2e-3, ", ".join(f"{v:.5f}" for v in vals) + f" vs {pred:.6f}")
    # x^2(1-x)^2 : sine coefficients exact
    un = np.where(nn % 2 == 1, np.sqrt(2)*(48 - 4*(np.pi*nn)**2)/(nn*np.pi)**5, 0.0)   # SymPy: 2(24-2π²n²)/(πn)^5, n dispari
    xx = np.linspace(0, 1, 20001); chk = np.trapezoid(xx**2*(1 - xx)**2*np.sqrt(2)*np.sin(3*np.pi*xx), xx)
    check("coeff. seno di x²(1-x)² = √2(48-4π²n²)/(nπ)^5 (n dispari)", abs(chk - un[2]) < 1e-9, f"{chk:.3e} vs {un[2]:.3e}")
    ts = [3e-3, 1e-3, 3e-4, 1e-4]
    vals = [Emodal(un, t, M)/t**1.75 for t in ts]
    A_ = np.vstack([np.ones(4), np.sqrt(ts), ts]).T; coef = np.linalg.lstsq(A_, np.array(vals), rcond=None)[0]
    pred = N1*math.sqrt(8)
    check("OPA-T2 x²(1-x)²: ||E||/t^{7/4} → N1√8 = 0.45996 (estrapolazione r0+r1√t+r2 t)", abs(coef[0] - pred)/pred < 3e-3,
          ", ".join(f"{v:.5f}" for v in vals) + f" → {coef[0]:.5f} vs {pred:.5f}")
    # k = 3: sin(pi x) - sin(3 pi x)/3 ; u0'(0)=u0'(1)=0, u0'''(0)=8π^3, u0'''(1)=-8π^3
    u = np.zeros(M); u[0] = 1/np.sqrt(2); u[2] = -1/(3*np.sqrt(2))
    ts = [1e-3, 3e-4, 1e-4, 3e-5]
    vals = [Emodal(u, t, M)/t**2.25 for t in ts]
    pred = N2*math.sqrt(2)*8*np.pi**3/2
    A_ = np.vstack([np.ones(4), ts]).T; coef = np.linalg.lstsq(A_, np.array(vals), rcond=None)[0]
    check("OPA-T2(iii) k=3: ||E||/t^{9/4} → N2·√2·8π³/2! (D^{5/4}=1)", abs(vals[-1] - pred)/pred < 5e-3,
          ", ".join(f"{v:.4f}" for v in vals) + f" (estr. {coef[0]:.4f}) vs {pred:.4f}")
    # (i) uniform bound check
    xs_ = np.linspace(0, 1, 100001)
    d1 = np.max(np.abs(2*xs_*(1 - xs_)*(1 - 2*xs_)))
    ok = all(Emodal(un, t, M) <= Cs*d1*t**1.25 for t in [1e-1, 1e-2, 1e-3, 1e-4])
    check("OPA-T2(i) ||E|| ≤ C_*||u0'||_∞ t^{5/4} su x²(1-x)² e su e1", ok and all(Emodal(np.eye(M)[0], t, M) <= Cs*math.sqrt(2)*np.pi*t**1.25 for t in [1e-1, 1e-2, 1e-3]))
    print(f"[F] tempo {time.time()-t0:.0f}s", flush=True)

# ---------------------------------------------------------------- G: OPA-L5, OPA-L4/T3, OPA-P3
def logR2(a_list, t0, T, zeta, m, K):
    # log of ratio lower bound of OPA-L3: num = ∫_I |G(t-t0)|^2 e^{2Re a t0}, den = (1+|ζ|)^{2mK} ∫_I e^{2Re a t}
    mp.mp.dps = 50
    a = sum(f(zeta) for f in a_list)
    N = len(a_list)
    def G(s): return mp.e**(s*a) - sum(mp.e**(s*f(zeta)) for f in a_list) + (N - 1)
    num = mp.quad(lambda t: abs(G(t - t0))**2*mp.e**(2*mp.re(a)*t0), mp.linspace(0, T, 9))
    den = (1 + abs(zeta))**(2*m*K)*mp.quad(lambda t: mp.e**(2*mp.re(a)*t), [0, T])
    return float(mp.log(num/den))
if "G" in SECT:
    rng = np.random.default_rng(15)
    th = np.linspace(0, 2*np.pi, 20001)
    bad = 0
    for _ in range(300):
        d = int(rng.integers(1, 6)); e = int(rng.integers(1, 9))
        al = complex(*rng.normal(size=2)); be = complex(*rng.normal(size=2))
        if e == d and rng.random() < 0.3: be = abs(rng.normal())*al   # eccezione
        A_ = np.real(al*np.exp(1j*d*th)); Bv = np.real(be*np.exp(1j*e*th))
        nonempty = np.any((A_ > 1e-9) & (Bv < -1e-9)) and np.any((A_ < -1e-9) & (Bv > 1e-9))
        exc = (e == d and abs((be/al).imag) < 1e-12 and (be/al).real > 0)
        if nonempty == exc: bad += 1
    check("OPA-L5 Θ± non vuoti ⟺ non eccezione (300 casi casuali, campionamento)", bad == 0, f"discordanze {bad}")
    T = 1.0
    # monomi: AD (a1 = -c ξ ... qui a1 = ξ, a2 = ξ^2), tre monomi (iξ^3, ξ^2, -2ξ): crescita lungo un raggio scelto
    for lab, al, Kd in [("AD ξ, ξ²", [lambda z: z, lambda z: z**2], 2), ("iξ³, ξ², −2ξ", [lambda z: 1j*z**3, lambda z: z**2, lambda z: -2*z], 3)]:
        for t0 in [0.0, 0.5, 1.0]:
            best = None
            for thv in np.linspace(0.05, 2*np.pi - 0.05, 12):
                vals = [logR2(al, t0, T, complex(r*np.cos(thv), r*np.sin(thv)), 1, Kd) for r in (16.0, 32.0, 64.0)]
                if best is None or vals[-1] > best[-1]: best = vals
            check(f"OPA-T3(b) {lab}, t0={t0}: log R² cresce (m=1, K=d, r=16,32,64)", best[2] > best[1] > best[0] and best[2] > 5, ", ".join(f"{v:.1f}" for v in best))
    # proporzionali: a = ξ^2, a_n = θ_n a  (κ_n = 0)
    def prop_growth(thetas, t0):
        al = [(lambda th_: (lambda z: th_*z**2))(th_) for th_ in thetas]
        out = []
        for lam in [-400.0, -100.0, 100.0, 400.0]:
            zeta = complex(np.sqrt(lam), 0) if lam > 0 else complex(0, np.sqrt(-lam))
            out.append(logR2(al, t0, T, zeta, 1, 2))   # peso H^1: (1+|ζ|)^{2mK}, m=1, K=2
        return out
    for thetas, t0, expect_bounded in [((0.5, 0.5), 0.0, True), ((0.5, 0.5), 1.0, True), ((2.0, -1.0), 0.5, False),
                                       ((-0.3, 1.3), 0.5, False), ((-0.3, 0.6, 0.7), 0.5, True), ((-0.3, 0.6, 0.7), 0.1, False), ((-0.3, 0.6, 0.7), 0.9, False)]:
        v = prop_growth(thetas, t0)
        mu_ = [abs(x) for x in thetas if x < 0]
        tc = all((0 < x <= 1) for x in thetas if x > 0) and all(m*T/(1 + m) <= t0 <= T/(1 + m) for m in mu_)
        bounded = max(v) < 5
        check(f"OPA-P3 θ={thetas}, t0={t0}: (TC)={tc}; rapporto L2/L2 limitato={bounded}", tc == expect_bounded and bounded == expect_bounded,
              ", ".join(f"{x:.1f}" for x in v))

# ---------------------------------------------------------------- H: OPA-P4 (ε = 1), serie modale + trasporto con inflow
if "H" in SECT:
    t0_ = time.time()
    Lq, c, D = 1.0, 1.0, 1.0
    M = 700; n = np.arange(1, M + 1); lam = D*(n*np.pi)**2
    m_ = n[:, None]; k_ = n[None, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        V = np.where((m_ + k_) % 2 == 1, -4.0*c*m_*k_/(m_**2 - k_**2), 0.0)
    A = -np.diag(lam) + V
    xx = np.linspace(0, Lq, 200001)
    basis = lambda f: np.array([np.trapezoid(f*np.sqrt(2)*np.sin(mm*np.pi*xx), xx) for mm in n])
    u0 = xx*(1 - xx)
    u = basis(u0)
    res = []
    for t in [3e-2, 1e-2, 3e-3, 1e-3]:
        St = linalg.expm(t*A) @ u
        S2 = np.where(xx > c*t, (xx - c*t)*(1 - (xx - c*t)), 0.0)
        S0S2 = np.exp(-lam*t)*basis(S2)
        Emult = St - S0S2
        with np.errstate(divide='ignore', invalid='ignore'):
            lm = lam[:, None]; ln = lam[None, :]
            phi = np.where(m_ != k_, (np.exp(-ln*t) - np.exp(-lm*t))/(lm - ln), 0.0)
        E1 = (V*(phi - t*np.exp(-lm*t))) @ u
        r = np.linalg.norm(Emult - E1)/t**1.5
        res.append((t, np.linalg.norm(Emult)/t**1.25, np.linalg.norm(E1)/t**1.25, r))
        print(f"[H] t={t:.0e}: ||E^mult||/t^1.25={res[-1][1]:.5f} ||E^(1)||/t^1.25={res[-1][2]:.5f} ||E^mult-E^(1)||/t^1.5={r:.4f}", flush=True)
    N0 = 0.234005
    check("OPA-P4 ||E^mult - E^(1)|| = O(t^{3/2}) (rapporto limitato)", max(x[3] for x in res) < 3*min(x[3] for x in res) + 1e-9,
          ", ".join(f"{x[3]:.3f}" for x in res))
    check("OPA-P4 ||E^mult||/t^{5/4} → N0√2 = 0.33093 (correzione O(t^{1/4}))", abs(res[-1][1] - N0*math.sqrt(2)) < 0.05,
          ", ".join(f"{x[1]:.4f}" for x in res))
    # stima di ‖∂S^D(r)‖ ≤ (2eDr)^{-1/2}
    rr = 1e-3; mus = n*np.pi
    check("OPA-P4 sup_μ μe^{-Dμ²r} ≤ (2eDr)^{-1/2}", np.max(mus*np.exp(-D*mus**2*rr)) <= (2*np.e*D*rr)**-0.5)
    print(f"[H] tempo {time.time()-t0_:.0f}s", flush=True)

print(f"\nTOTALE: {NOK[0]}/{NOK[1]} OK")
