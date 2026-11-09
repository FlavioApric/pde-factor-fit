# S-CHECK-F8-VAR (27/10/2026) - audit di VAR-L2-cor: controlli INDIPENDENTI.
# (0) SymPy: per Dirichlet/Neumann/periodiche il termine di bordo f f' si annulla, quindi
#     ||f'||^2 = -<f, f''> <= ||f|| ||f''||: norma del grafo di H_0 equivalente alla norma H^2.
# (1) VAR-P11(e) su un modello di Galerkin (toro, V(t,x) = a(t) cos x, a in C^1): la soluzione
#     con dato in D(H_0) e' classica: rapporto incrementale -> -i(H_0 + V(t))u(t), con errore O(h^2),
#     e t -> ||u(t)||_{H^2} e' continua.
# (2) Portata (1): dato a supporto in J \ cl(omega): restrizione a omega nulla a t = 0, ma la
#     traiettoria su I x omega non e' nulla (coerente con l'iniettivita' sulle traiettorie).
# (3) Caso autonomo V = V(x), dato solo in L^2: g = int rho(s) U(s) psi0 ds sta in D(H) con
#     H g = -i int rho'(s) U(s) psi0 ds e ||H g|| <= ||rho'||_1 ||psi0|| (uniforme nel troncamento),
#     mentre ||H psi0|| cresce col troncamento. E' il passo chiave della chiusura di VAR-Q17 per V(x).
import sympy as sp
import numpy as np

ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond)
    print(("OK   " if cond else "FAIL ") + name)

# ---------- (0) termine di bordo ----------
x, l = sp.symbols('x ell', positive=True)
cs = sp.symbols('c0:7')
f = sum(c*x**i for i, c in enumerate(cs))
for name, unk, conds in [("Dirichlet", [cs[0], cs[1]], [f.subs(x, 0), f.subs(x, l)]),
                    ("Neumann", [cs[1], cs[2]], [sp.diff(f, x).subs(x, 0), sp.diff(f, x).subs(x, l)]),
                    ("periodiche", [cs[1], cs[2]], [f.subs(x, 0) - f.subs(x, l), sp.diff(f, x).subs(x, 0) - sp.diff(f, x).subs(x, l)])]:
    sol = sp.solve(conds, unk, dict=True)[0]
    fs = f.subs(sol)
    bt = sp.simplify((fs*sp.diff(fs, x)).subs(x, l) - (fs*sp.diff(fs, x)).subs(x, 0))
    ibp = sp.simplify(sp.integrate(sp.diff(fs, x)**2, (x, 0, l)) + sp.integrate(fs*sp.diff(fs, x, 2), (x, 0, l)))
    chk(f"(0) {name}: termine di bordo nullo e ||f'||^2 = -<f,f''>", bt == 0 and ibp == 0)

# ---------- modello di Galerkin sul toro (0, 2 pi) ----------
def galerkin(M):
    k = np.arange(-M, M + 1)
    H0 = np.diag(k.astype(float)**2)
    C = np.zeros((2*M + 1, 2*M + 1))           # moltiplicazione per cos x: k <-> k +- 1, peso 1/2
    for i in range(2*M):
        C[i, i + 1] = C[i + 1, i] = 0.5
    return k, H0, C

def expmh(Hm, tau):                             # exp(-i tau Hm), Hm hermitiana
    w, Q = np.linalg.eigh(Hm)
    return (Q*np.exp(-1j*tau*w)) @ Q.conj().T

def evolve(c0, H0, C, a, T, dt):               # Magnus del 4o ordine (due punti di Gauss)
    n = int(round(T/dt)); dt = T/n
    out = [c0.copy()]; c = c0.copy()
    g1, g2 = 0.5 - np.sqrt(3)/6, 0.5 + np.sqrt(3)/6
    for j in range(n):
        t = j*dt
        A1 = H0 + a(t + g1*dt)*C; A2 = H0 + a(t + g2*dt)*C
        # Omega = -i dt (A1+A2)/2 + (sqrt3/12) dt^2 [-iA2, -iA1]  =  -i * Heff * dt
        Heff = (A1 + A2)/2 + 1j*(np.sqrt(3)/12)*dt*(A2 @ A1 - A1 @ A2)
        c = expmh(Heff, dt) @ c
        out.append(c.copy())
    return np.array(out), dt

# ---------- (1) VAR-P11(e): soluzione classica ----------
M = 32
k, H0, C = galerkin(M)
a = lambda t: 1 + 0.5*np.sin(3*t)
rng = np.random.default_rng(7)
# dato liscio (coefficienti gaussiani): il test O(h^2) richiede k^2 h piccolo sui modi presenti
c0 = (rng.normal(size=2*M + 1) + 1j*rng.normal(size=2*M + 1))*np.exp(-k.astype(float)**2/20)
c0 /= np.linalg.norm(c0)
T, dt = 1.0, 1e-3
traj, dt = evolve(c0, H0, C, a, T, dt)
errs = {}
for h_steps in [20, 10, 5, 2]:
    h = h_steps*dt; e = 0.0
    for t in [0.3, 0.7]:
        j = int(round(t/dt))
        D = (traj[j + h_steps] - traj[j - h_steps])/(2*h)
        G = -1j*(H0 + a(t)*C) @ traj[j]
        e = max(e, np.linalg.norm(D - G)/np.linalg.norm(G))
    errs[h] = e
    print(f"   P11(e): h = {h:.3f}: errore relativo del rapporto incrementale = {e:.2e}")
hs = sorted(errs)
chk("(1) P11(e): rapporto incrementale -> -i(H_0+V(t))u, ordine ~2 in h",
    errs[hs[0]] < 2e-3 and errs[hs[-1]]/errs[hs[0]] > 50)
H2 = np.array([np.linalg.norm((1 + k.astype(float)**2)*c) for c in traj])
jump = np.max(np.abs(np.diff(H2)))
print(f"   ||u(t)||_H2 in [{H2.min():.4f}, {H2.max():.4f}], salto massimo su un passo {jump:.2e}")
chk("(1) t -> ||u(t)||_{H^2} continua e limitata", jump < 1e-2*H2.max())
chk("(1) unitarieta' (V reale): ||u(t)||_L2 costante", np.max(np.abs(np.linalg.norm(traj, axis=1) - 1)) < 1e-10)

# ---------- (2) portata: tempo fisso contro traiettoria ----------
M2 = 128
k2, H02, C2 = galerkin(M2)
Ng = 2048; xg = 2*np.pi*np.arange(Ng)/Ng
def bump(s, lo, hi):
    m, hw = (lo + hi)/2, (hi - lo)/2
    y = np.clip(1 - ((s - m)/hw)**2, 1e-300, None)
    return np.where((s > lo) & (s < hi), np.exp(-1/y), 0.0)
f0 = bump(xg, 3.5, 5.5)
fh = np.fft.fft(f0)/Ng                          # coefficienti di Fourier
c02 = np.concatenate([fh[-M2:], fh[:M2 + 1]])   # ordine k = -M2..M2
def to_grid(c):
    full = np.zeros(Ng, complex); full[:M2 + 1] = c[M2:]; full[-M2:] = c[:M2]
    return np.fft.ifft(full)*Ng
om = (xg > 0.5) & (xg < 1.5)
traj2, dt2 = evolve(c02, H02, C2, a, 0.5, 2e-3)
r0 = np.max(np.abs(to_grid(traj2[0])[om]))
rt = max(np.max(np.abs(to_grid(c)[om])) for c in traj2[::10])
print(f"   portata: max|u(0)| su omega = {r0:.1e}; max_t max|u(t)| su omega = {rt:.3e}")
chk("(2) restrizione a omega nulla a t = 0 ma traiettoria non nulla su I x omega", r0 < 1e-6 and rt > 1e4*r0)  # r0 = coda di Fourier del bump

# ---------- (3) caso autonomo, dato in L^2 ----------
def mollify_check(Mx):
    kx, H0x, Cx = galerkin(Mx)
    Hm = H0x + Cx                               # V(x) = cos x
    lam, Q = np.linalg.eigh(Hm)
    ind = ((xg > 1) & (xg < 2)).astype(float)   # dato a gradino: in L^2, non in H^1
    fhx = np.fft.fft(ind)/Ng
    cx = np.concatenate([fhx[-Mx:], fhx[:Mx + 1]])
    eps = 0.1
    s = np.linspace(-eps, eps, 4001); ds = s[1] - s[0]
    rho = bump(s, -eps, eps); rho /= np.sum(rho)*ds
    drho = np.gradient(rho, ds)
    ph = np.exp(-1j*np.outer(lam, s))
    w = ph @ rho*ds; wp = ph @ drho*ds          # rho^(lam), (rho')^(lam)
    b = Q.conj().T @ cx
    g = Q @ (w*b)
    Hg = Q @ (lam*w*b); rhs = Q @ (-1j*wp*b)
    rel = np.linalg.norm(Hg - rhs)/np.linalg.norm(Hg)
    bound = np.sum(np.abs(drho))*ds*np.linalg.norm(cx)
    return np.linalg.norm(Hg), bound, rel, np.linalg.norm(Hm @ cx)
res = {Mx: mollify_check(Mx) for Mx in [64, 128, 256]}
for Mx, (nHg, bd, rel, nHf) in res.items():
    print(f"   autonomo M={Mx}: ||Hg|| = {nHg:.4f} <= {bd:.4f};  |Hg - (-i int rho' U f)|/|Hg| = {rel:.1e};  ||H psi0|| = {nHf:.2f}")
chk("(3) H g = -i int rho' U psi0 ds", all(r[2] < 1e-6 for r in res.values()))
chk("(3) ||H g|| <= ||rho'||_1 ||psi0||, uniforme nel troncamento", all(r[0] <= r[1] for r in res.values())
    and abs(res[256][0] - res[128][0]) < 1e-3*res[256][0])
chk("(3) ||H psi0|| cresce col troncamento (psi0 non in D(H))", res[256][3] > 1.3*res[64][3])
print("TUTTO OK" if ok else "FALLITO")
