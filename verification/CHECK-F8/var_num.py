# S-CHECK-F8-VAR (27/10/2026) - controlli numerici INDIPENDENTI (metodo diverso da s8_pt / s8_osc):
# (A) VAR-P8(c): formula di Darboux per U_1 e U_2 (Poschl-Teller) contro uno split-step di Strang
#     a passo piccolo (nessuna diagonalizzazione densa di H).
# (B) VAR-T10(3)(iii): U(t) = c(t) C(gamma) F(s) C(gamma) per H = -d^2 + x^2 contro lo sviluppo
#     esatto in funzioni di Hermite; verifica |c| = 1 e lo stesso c su due dati diversi.
import numpy as np
from numpy.fft import fft, ifft, fftfreq
from math import factorial

ok = True
def chk(name, cond):
    global ok
    ok &= bool(cond); print(("OK   " if cond else "FAIL ") + name)

# ---------- (A) Poschl-Teller ----------
Lb, N = 60.0, 1024
xg = (np.arange(N) - N//2)*(Lb/N); k = 2*np.pi*fftfreq(N, d=Lb/N)
D = lambda f: ifft(1j*k*fft(f))
th, sech = np.tanh(xg), 1/np.cosh(xg)
free = lambda f, tt: ifft(np.exp(-1j*tt*k**2)*fft(f))
ip = lambda f, g: np.sum(np.conj(f)*g)*(Lb/N)
def Hmat(l):   # matrice spettrale densa di H_l (usata solo per risolvere (H_{l-1}+l^2) y = g)
    F = np.fft.fft(np.eye(N), axis=0); Fi = np.fft.ifft(np.eye(N), axis=0)
    K2 = Fi @ np.diag(k**2) @ F
    return K2 - np.diag(l*(l+1)*sech**2)
H1 = Hmat(1)
def U1(f, tt):
    Af = D(f) + th*f
    g = ifft(np.exp(-1j*tt*k**2)*fft(Af)/(1 + k**2))
    return -D(g) + th*g + np.exp(1j*tt)*ip(sech, f)*sech/ip(sech, sech)
def U2(f, tt):
    Af = D(f) + 2*th*f
    y = np.linalg.solve(H1 + 4*np.eye(N), Af)
    g = U1(y, tt)
    s2 = sech**2
    return -D(g) + 2*th*g + np.exp(4j*tt)*ip(s2, f)*s2/ip(s2, s2)
def strang(f, tt, l, dt=2e-4):
    V = -l*(l+1)*sech**2
    n = int(round(tt/dt)); dt = tt/n
    h = np.exp(-0.5j*dt*V); p = np.exp(-1j*dt*k**2)
    for _ in range(n):
        f = h*ifft(p*fft(h*f))
    return f
f0 = np.exp(-(xg - 2.0)**2)*np.exp(1j*1.5*xg) + 0.5*sech
for l, Uf in [(1, U1), (2, U2)]:
    for tt in [0.5, 1.5]:
        a, b = Uf(f0, tt), strang(f0, tt, l)
        err = np.max(np.abs(a - b))/np.max(np.abs(b))
        print(f"   PT l={l}, t={tt}: errore relativo formula vs Strang = {err:.2e}")
        chk(f"P8(c): l={l}, t={tt}", err < 1e-5)

# ---------- (B) oscillatore H = -d^2 + x^2 ----------
Lb2, N2 = 40.0, 1024
x2 = (np.arange(N2) - N2//2)*(Lb2/N2); k2 = 2*np.pi*fftfreq(N2, d=Lb2/N2)
nmax = 60
# funzioni di Hermite normalizzate (ricorrenza stabile)
Hf = np.zeros((nmax, N2)); Hf[0] = np.pi**-0.25*np.exp(-x2**2/2)
Hf[1] = np.sqrt(2)*x2*Hf[0]
for n in range(2, nmax):
    Hf[n] = np.sqrt(2/n)*x2*Hf[n-1] - np.sqrt((n-1)/n)*Hf[n-2]
dx2 = Lb2/N2
def Uex(f, tt):
    c = Hf @ f*dx2
    return (np.exp(-1j*tt*(2*np.arange(nmax) + 1))*c) @ Hf
def word(f, tt):
    gam = (np.cos(2*tt) - 1)/(2*np.sin(2*tt)); s = np.sin(2*tt)/2
    C = np.exp(1j*gam*x2**2)
    return C*ifft(np.exp(-1j*s*k2**2)*fft(C*f))
fa = np.exp(-(x2 - 1)**2)*(1 + 0j); fb = (x2**2)*np.exp(-x2**2/2 + 0.5j*x2)
for tt in [0.3, np.pi/4, 1.3]:
    ua, wa = Uex(fa, tt), word(fa, tt); ub, wb = Uex(fb, tt), word(fb, tt)
    ca = np.vdot(wa, ua)/np.vdot(wa, wa); cb = np.vdot(wb, ub)/np.vdot(wb, wb)
    ea = np.max(np.abs(ua - ca*wa)); eb = np.max(np.abs(ub - cb*wb))
    print(f"   osc t={tt:.4f}: |c|={abs(ca):.12f}, |c_a-c_b|={abs(ca-cb):.1e}, err={max(ea,eb):.1e}")
    chk(f"T10(3): t={tt:.4f}", abs(abs(ca) - 1) < 1e-8 and abs(ca - cb) < 1e-8 and max(ea, eb) < 1e-8)
# a t = pi/2 l'evoluzione e' -i * parita': nessuna parola (gamma diverge); a t = pi e' -I
P = Uex(fb, np.pi/2); refl = fb[(N2 - np.arange(N2)) % N2]
chk("T10: U(pi/2) f = -i f(-x) (parita')", np.max(np.abs(P + 1j*refl)) < 1e-8)
P = Uex(fb, np.pi); chk("T10: U(pi) f = -f (parola banale)", np.max(np.abs(P + fb)) < 1e-8)
print("TUTTO OK" if ok else "FALLITO")
