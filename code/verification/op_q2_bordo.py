# OP-ANA Q2 (P3-Q-bordo): controlli (NON prove) del Teorema OPA-T2.
# (1) Lemma del commutatore: d/dx S^D(s) f = S^N(s) f'  (SymPy, modi seno).
# (2) Identita' del nucleo K^N - K^D = 2 sum_j G_s(x+y-2jL) (numerico, theta di Jacobi).
# (3) Costanti del profilo: N_0 = sqrt(J/pi) (forma chiusa) e N_1 (quadratura in trasformata seno).
# (4) Serie modale ESATTA di P3-P1(b) per u0 = e_1 e u0 = x^2(1-x)^2 (L=c=D=1):
#     ||E(t)|| / t^{5/4+alpha/2}  ->  |c| N_alpha D^{alpha/2+1/4} sqrt(gamma_0^2+gamma_L^2).
import numpy as np, sympy as sp
from scipy.integrate import quad
from scipy.special import erfc

ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond)
    print(("[OK] " if cond else "[FAIL] ") + name, flush=True)

# (1) commutatore su (0,L): f = sum f_n e_n con f in H^1_0
x, L, s, D = sp.symbols('x L s D', positive=True)
for n in [1, 2, 3]:
    mu = n*sp.pi/L
    e = sp.sqrt(2/L)*sp.sin(mu*x); c_ = sp.sqrt(2/L)*sp.cos(mu*x)
    lhs = sp.diff(sp.exp(-D*mu**2*s)*e, x)                 # d/dx S^D(s) e_n
    rhs = sp.exp(-D*mu**2*s)*mu*c_                          # S^N(s) (e_n)'
    check(f"commutatore modo n={n}", sp.simplify(lhs - rhs) == 0)
# coefficiente in coseno di f' per f in H^1_0 generica (test: f = x^2(L-x))
f = x**2*(L - x)
for n in [0, 1, 2, 3]:
    cn = sp.integrate(sp.diff(f, x)*(sp.sqrt(2/L)*sp.cos(n*sp.pi*x/L) if n > 0 else 1/sp.sqrt(L)), (x, 0, L))
    fn = sp.integrate(f*sp.sqrt(2/L)*sp.sin(n*sp.pi*x/L), (x, 0, L)) if n > 0 else 0
    check(f"<f',c_{n}> = mu_n f_n  (f=x^2(L-x))", sp.simplify(cn - (n*sp.pi/L)*fn) == 0)

# (2) nucleo (L=1, D=1, s=0.01): somma modale vs immagini
Lv, sv = 1.0, 0.01
for (xv, yv) in [(0.1, 0.05), (0.5, 0.3), (0.95, 0.9)]:
    nmax = 400
    n = np.arange(1, nmax)
    KN = 1/Lv + (2/Lv)*np.sum(np.exp(-(n*np.pi/Lv)**2*sv)*np.cos(n*np.pi*xv/Lv)*np.cos(n*np.pi*yv/Lv))
    KD = (2/Lv)*np.sum(np.exp(-(n*np.pi/Lv)**2*sv)*np.sin(n*np.pi*xv/Lv)*np.sin(n*np.pi*yv/Lv))
    G = lambda z: np.exp(-z**2/(4*sv))/np.sqrt(4*np.pi*sv)
    img = 2*sum(G(xv + yv - 2*j*Lv) for j in range(-5, 6))
    check(f"K^N-K^D = 2 sum_j G(x+y-2jL) in (x,y)=({xv},{yv}): {KN-KD:.10f} vs {img:.10f}", abs(KN - KD - img) < 1e-10)

# (3) costanti del profilo
Jc = quad(lambda y: y**-3.5*(1 - np.exp(-y)*(1 + y))**2, 0, np.inf, limit=200)[0]
N0_closed = np.sqrt(Jc/np.pi)
def Zhat(k, beta_hat, alpha):
    # Z^(1)(k) = int_0^1 e^{-k^2(1-s)} s^{(alpha+1)/2} beta_hat(k sqrt s) ds
    return quad(lambda s: np.exp(-k**2*(1 - s))*s**((alpha + 1)/2)*beta_hat(k*np.sqrt(s)), 0, 1, limit=200)[0]
def beta_hat_from(beta):
    cache = {}
    def bh(kappa):
        if kappa < 1e-12: return 0.0
        key = round(kappa, 12)
        if key not in cache:
            cache[key] = np.sqrt(2/np.pi)*quad(beta, 0, np.inf, weight='sin', wvar=kappa, limlst=200)[0]
        return cache[key]
    return bh
beta0 = lambda w: erfc(w/2)                                         # alpha = 0
beta1 = lambda w: 2/np.sqrt(np.pi)*np.exp(-w**2/4) - w*erfc(w/2)    # alpha = 1
bh0 = lambda kap: np.sqrt(2/np.pi)*(1 - np.exp(-kap**2))/kap        # forma chiusa
bh0_num = beta_hat_from(beta0)
check("trasformata seno di erfc(w/2): forma chiusa vs quadratura", all(abs(bh0(k) - bh0_num(k)) < 1e-7 for k in [0.3, 1.0, 2.5]))
N0 = np.sqrt(quad(lambda k: Zhat(k, bh0, 0)**2, 0, np.inf, limit=200)[0])
check(f"N_0 (quadratura) = {N0:.6f} vs sqrt(J/pi) = {N0_closed:.6f} (J={Jc:.6f})", abs(N0 - N0_closed) < 1e-6)
bh1 = beta_hat_from(beta1)
N1 = np.sqrt(quad(lambda k: Zhat(k, bh1, 1)**2, 0, 40, limit=400)[0])
print(f"N_1 = {N1:.6f}", flush=True)

# (4) serie modale esatta (P3-P1(b), P3-T3(i)), L=c=D=1, kappa = pi^2
def E_norm(t, cn, M=6000):
    kap = np.pi**2
    N = len(cn); n = np.arange(1, N + 1); m = np.arange(1, M + 1)
    lam_n = -kap*n**2; lam_m = -kap*m**2
    mm, nn = np.meshgrid(m, n, indexing='ij')
    V = np.where((mm + nn) % 2 == 1, -4*mm*nn/(mm**2 - nn**2 + ((mm + nn) % 2 == 0)), 0.0)
    dl = lam_n[None, :] - lam_m[:, None]; w = t*dl
    em = np.exp(lam_m[:, None]*t); en = np.exp(lam_n[None, :]*t)
    safe = np.where(np.abs(w) < 1e-3, 1.0, dl)
    T = np.where(np.abs(w) < 1e-3, t*em*(w/2 + w**2/6 + w**3/24), (en - em)/safe - t*em)
    Em = (V*T) @ cn
    return np.sqrt(np.sum(Em**2))
# e_1
pred0 = 1*N0_closed*1*np.sqrt(2)*(np.pi*np.sqrt(2))   # |c| N0 D^{1/4} sqrt(g0^2+gL^2), g0=|gL|=pi*sqrt(2)
for t in [1e-3, 1e-4, 1e-5]:
    r = E_norm(t, np.array([1.0]))/t**1.25
    print(f"e_1: t={t:.0e} ||E||/t^(5/4) = {r:.6f}  (predetto {pred0:.6f})", flush=True)
check("e_1: costante = 2*sqrt(J)*pi^{1/2} (audit S-CHECK-5) = |c| N_0 * 2 pi", abs(pred0 - 2*np.sqrt(Jc)*np.sqrt(np.pi)) < 1e-9)
check("e_1: rapporto a t=1e-5 entro 1% dal predetto", abs(E_norm(1e-5, np.array([1.0]))/1e-5**1.25/pred0 - 1) < 1e-2)
# x^2(1-x)^2: coefficienti in seno esatti (forma chiusa SymPy), calcolo a blocchi.
# NB: ogni troncamento modale ha u''(0)=0 e pendenza residua ~1/N: si usano t >= 1e-4 con N=3000
# e si estrapola r(t) = r0 + r1 t^{1/2} + r2 t (correzione attesa di ordine t^{1/2}, beta=1).
def cn_x2(N):
    n = np.arange(1, N + 1, dtype=float); sg = (-1.0)**n
    return 2*np.sqrt(2)*(-12*sg + np.pi**2*n**2*(sg - 1) + 12)/(np.pi**5*n**5)
def E_norm_blocks(t, cn, M=8000, B=500):
    kap = np.pi**2; N = len(cn); n = np.arange(1, N + 1)
    lam_n = -kap*n**2; en = np.exp(lam_n*t)
    tot = 0.0
    for m0 in range(1, M + 1, B):
        m = np.arange(m0, min(m0 + B, M + 1)); lam_m = -kap*m**2
        mm, nn = np.meshgrid(m, n, indexing='ij')
        V = np.where((mm + nn) % 2 == 1, -4*mm*nn/(mm**2 - nn**2 + ((mm + nn) % 2 == 0)), 0.0)
        dl = lam_n[None, :] - lam_m[:, None]; w = t*dl
        em = np.exp(lam_m[:, None]*t)
        safe = np.where(np.abs(w) < 1e-3, 1.0, dl)
        T = np.where(np.abs(w) < 1e-3, t*em*(w/2 + w**2/6 + w**3/24), (en[None, :] - em)/safe - t*em)
        tot += np.sum(((V*T) @ cn)**2)
    return np.sqrt(tot)
cn = cn_x2(3000)
pred1 = 1*N1*1*np.sqrt(2**2 + 2**2)    # alpha=1, gamma_0 = 2, |gamma_L| = 2
ts = np.array([3e-3, 1e-3, 3e-4, 1e-4]); rs = []
for t in ts:
    r = E_norm_blocks(t, cn)/t**1.75; rs.append(r)
    print(f"x^2(1-x)^2: t={t:.0e} ||E||/t^(7/4) = {r:.6f}  (predetto limite {pred1:.6f})", flush=True)
A = np.vstack([np.ones_like(ts), np.sqrt(ts), ts]).T
r0, r1, r2 = np.linalg.lstsq(A, np.array(rs), rcond=None)[0]
print(f"estrapolazione r0 + r1 sqrt(t) + r2 t: r0 = {r0:.5f}, r1 = {r1:.3f}, r2 = {r2:.3f}")
check("x^2(1-x)^2: limite estrapolato entro 2% da |c| N_1 sqrt(8)", abs(r0/pred1 - 1) < 2e-2)
print(f"RISULTATO: {ok}/{tot} OK")
