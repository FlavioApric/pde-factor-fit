# S8-VAR — VAR-P8(c): Poschl-Teller V_l = -l(l+1) sech^2 x. Simbolico: fattorizzazioni H_j = A_j^+A_j - j^2,
# A_jA_j^+ - j^2 = H_{j-1}, A_j sech^j = 0, A_j^+ cosh^j = 0, funzioni di Jost. Numerico (spettrale, scatola periodica):
# U_1(t) = e^{it} P_0 + A^+ U_0(t)(H_0+1)^{-1} A confrontato con exp(-itH_1) da diagonalizzazione densa; idem l = 2.
import sympy as sp
import numpy as np
x, k = sp.symbols('x k', real=True)
I = sp.I
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")
f = sp.Function('f')(x)
def H(j, g): return -sp.diff(g, x, 2) - j*(j+1)*sp.sech(x)**2*g
def A(j, g): return sp.diff(g, x) + j*sp.tanh(x)*g
def Ad(j, g): return -sp.diff(g, x) + j*sp.tanh(x)*g
okF = True
for j in range(1, 5):
    okF &= sp.simplify((Ad(j, A(j, f)) - j**2*f - H(j, f)).rewrite(sp.exp)) == 0
    okF &= sp.simplify((A(j, Ad(j, f)) - j**2*f - H(j-1, f)).rewrite(sp.exp)) == 0
    okF &= sp.simplify(A(j, sp.sech(x)**j).rewrite(sp.exp)) == 0
    okF &= sp.simplify(Ad(j, sp.cosh(x)**j).rewrite(sp.exp)) == 0
report("H_j = A_j^+A_j - j^2, A_jA_j^+ - j^2 = H_{j-1}, ker A_j = sech^j, ker A_j^+ = cosh^j (j=1..4)", okF)
jost = Ad(1, sp.exp(I*k*x))
report("Jost: H_1 (tanh x - ik)e^{ikx} = k^2 (tanh x - ik) e^{ikx}", sp.simplify((H(1, jost) - k**2*jost).rewrite(sp.exp)) == 0)
report("||sech||^2 = 2", sp.integrate(4/(sp.exp(x) + sp.exp(-x))**2, (x, -sp.oo, sp.oo)) == 2)
report("H_1 sech = -sech (stato legato a -1)", sp.simplify((H(1, sp.sech(x)) + sp.sech(x)).rewrite(sp.exp)) == 0)

# numerico
N, Lb = 2048, 60.0   # scatola larga: con Lb = 40 a t = 2.5 compare un artefatto di bordo (errore ~4e-6 in x = -Lb)
xs = np.linspace(-Lb, Lb, N, endpoint=False); dx = xs[1]-xs[0]
ks = 2*np.pi*np.fft.fftfreq(N, d=dx)
def D(v): return np.fft.ifft(1j*ks*np.fft.fft(v))
def U0(tt, v): return np.fft.ifft(np.exp(-1j*tt*ks**2)*np.fft.fft(v))
def R0(v, z): return np.fft.ifft(np.fft.fft(v)/(ks**2 + z))
th = np.tanh(xs); sech = 1/np.cosh(xs)
Ffft = np.fft.fft(np.eye(N), axis=0); D2 = np.real(np.fft.ifft(-(ks**2)[:, None]*Ffft, axis=0))
H1m = -D2 - np.diag(2*sech**2); H2m = -D2 - np.diag(6*sech**2)
def Uex(Hm, tt, v):
    w, Q = np.linalg.eigh((Hm + Hm.T)/2)
    return Q @ (np.exp(-1j*tt*w)*(Q.T @ v))
psi = (1 + 0.5*xs)*np.exp(-(xs - 0.7)**2) * np.exp(0.8j*xs)
errs = []
for tt in [0.3, 1.0, 2.5]:
    P0 = sech*np.sum(sech*psi)*dx/2
    Aps = D(psi) + th*psi
    form = np.exp(1j*tt)*P0 + (-D(U0(tt, R0(Aps, 1.0))) + th*U0(tt, R0(Aps, 1.0)))
    ex = Uex(H1m, tt, psi)
    errs.append(np.max(np.abs(form - ex)))
report("U_1(t) = e^{it}P_0 + A^+U_0(t)(H_0+1)^{-1}A vs exp(-itH_1), t=0.3,1,2.5", max(errs) < 1e-8, f"err max = {max(errs):.2e}")
# l = 2: U_2(t) = e^{4it} P_{sech^2} + A_2^+ U_1(t)(H_1+4)^{-1} A_2, con U_1 dalla formula precedente e (H_1+4)^{-1} denso
def U1form(tt, v):
    P0 = sech*np.sum(sech*v)*dx/2; Av = D(v) + th*v; w = U0(tt, R0(Av, 1.0))
    return np.exp(1j*tt)*P0 + (-D(w) + th*w)
errs2 = []
s2 = sech**2; ns2 = np.sum(s2*s2)*dx
for tt in [0.4, 1.7]:
    A2p = D(psi) + 2*th*psi
    r = np.linalg.solve(H1m + 4*np.eye(N), A2p)
    w = U1form(tt, r)
    form = np.exp(4j*tt)*s2*np.sum(s2*psi)*dx/ns2 + (-D(w) + 2*th*w)
    errs2.append(np.max(np.abs(form - Uex(H2m, tt, psi))))
report("l=2: U_2 = e^{4it}P + A_2^+U_1(H_1+4)^{-1}A_2 vs exp(-itH_2)", max(errs2) < 1e-7, f"err max = {max(errs2):.2e}")
# E_int^add esplicito (A9): U_1 - U_0 - e^{-itV} + I, V = -2 sech^2; ordine t^2: (1/2)(A1A2+A2A1)
tt = 1e-3
Eadd = U1form(tt, psi) - U0(tt, psi) - np.exp(2j*tt*sech**2)*psi + psi
A1 = lambda v: 1j*np.real(np.fft.ifft(-(ks**2)*np.fft.fft(v))) if np.isrealobj(v) else 1j*np.fft.ifft(-(ks**2)*np.fft.fft(v))
A2 = lambda v: 2j*sech**2*v
pred = 0.5*tt**2*(A1(A2(psi)) + A2(A1(psi)))
report("E_int^add(t) = (t^2/2)(A_1A_2 + A_2A_1) + O(t^3) per Poschl-Teller", np.max(np.abs(Eadd - pred))/np.max(np.abs(pred)) < 1e-2,
       f"rel = {np.max(np.abs(Eadd - pred))/np.max(np.abs(pred)):.2e}")
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
