# S8-ENC — verifiche di ENC-T2 (contrazione pari), ENC-K0 (q = c senza intertwiner stretto),
# ENC-K1' (fattorizzazione di Darboux), ENC-P0' (lente: identita' a t = 0, cambia il tempo), stima di E^mult.
import sys
sys.stdout.reconfigure(encoding="utf-8")
import sympy as sp
import numpy as np

tau, xi, sg, S_ = sp.symbols('tau xi sigma s')
x, t = sp.symbols('x t', real=True)
res = []
def report(name, ok, extra=''):
    res.append((name, ok)); print(('OK  ' if ok else 'FAIL') + ' ' + name + ' ' + str(extra))

# ---------- ENC-T2: (Q) ∩ C[tau, xi^2] via eliminazione, confronto con lcm(Q, Q~) o xi*lcm
def even_part_ideal(Q):
    G = sp.groebner([Q, S_ - xi**2], xi, tau, S_, order='lex')
    return [g for g in G.exprs if not g.has(xi)]
def predicted(Q):
    Qt = Q.subs(xi, -xi)
    L = sp.lcm(Q, Qt)
    Lt = sp.expand(L.subs(xi, -xi))
    if sp.expand(Lt - L) == 0: gen = L
    else: gen = sp.expand(xi*L)
    return sp.expand(gen).subs(xi**2, S_) if True else None
for Q in [xi**2 + xi + tau, xi, xi*(tau + xi), tau + sp.I*xi, xi**3 + tau*xi + 1, (xi - 1)**2*(tau - xi)]:
    elim = even_part_ideal(sp.expand(Q))
    gen = sp.expand(predicted(sp.expand(Q)))
    gen_s = sp.expand(gen.subs(xi, sp.sqrt(S_)))
    ok = len(elim) == 1 and sp.simplify(sp.cancel(elim[0]/gen_s)).is_number
    report('ENC-T2 (Q)∩C[tau,xi^2] = generatore previsto, Q = %s' % Q, ok, (elim, gen_s))

# ---------- ENC-K0: W L_c = L_0 W (c != 0) non ha soluzioni polinomiali W != 0 di ordine <= 5
c = sp.Symbol('c', nonzero=True)
for n in range(0, 6):
    D = n + 3
    coeffs = []; ws = []
    for j in range(n+1):
        cs = sp.symbols('w%d_0:%d' % (j, D+1)); coeffs += cs
        ws.append(sum(cs[m]*x**m for m in range(D+1)))
    g = sp.Function('g')(x)
    W = lambda h: sum(ws[j]*sp.diff(h, x, j) for j in range(n+1))
    expr = sp.expand(W(-sp.diff(g, x, 2) + c*g) + sp.diff(W(g), x, 2))
    eqs = []
    for j in range(n+3):
        cj = expr.coeff(sp.diff(g, x, j)) if j > 0 else expr.subs({sp.diff(g, x, k): 0 for k in range(1, n+3)}).coeff(g)
        eqs += sp.Poly(sp.expand(cj), x).coeffs()
    sol = sp.solve(eqs, coeffs, dict=True)
    triv = all(all(v == 0 for v in s_.values()) and len(s_) == len(coeffs) for s_ in sol) if sol else False
    report('ENC-K0 q=c: nessun W polinomiale di ordine %d (grado <= %d) con W L_c = L_0 W' % (n, D), triv)
# modulo costanti: W = I soddisfa W L_c = (L_0 + c) W (banale) ; q = c - 2 sech^2: A^dag L_q = (L_0 + c) A^dag
g = sp.Function('g')(x)
q = c - 2*sp.sech(x)**2
Ad = lambda w: -sp.diff(w, x) - sp.tanh(x)*w
r = sp.simplify((Ad(-sp.diff(g, x, 2) + q*g) - (-sp.diff(Ad(g), x, 2) + c*Ad(g))).rewrite(sp.exp))
report('(E2\') q = c - 2 sech^2: A^dag L_q = (L_0 + c) A^dag', r == 0, r)

# ---------- ENC-K1': un W di ordine 2 con nucleo span{sech^2, tanh sech} (Crum, q = -6 sech^2) si fattorizza
q2 = -6*sp.sech(x)**2
phi1, phi2 = sp.sech(x)**2, sp.tanh(x)*sp.sech(x)
L2 = lambda h: -sp.diff(h, x, 2) + q2*h
# nucleo invariante e autovettori
report('K1\': L_q sech^2 = -4 sech^2', sp.simplify((L2(phi1) + 4*phi1).rewrite(sp.exp)) == 0)
report('K1\': L_q tanh sech = -1 tanh sech', sp.simplify((L2(phi2) + phi2).rewrite(sp.exp)) == 0)
# W monico di ordine 2 con nucleo {phi1, phi2}: W h = Wronskiano(phi1, phi2, h)/Wronskiano(phi1, phi2)
def wr(fs):
    return sp.Matrix([[sp.diff(f_, x, i) for f_ in fs] for i in range(len(fs))]).det()
Wop = lambda h: sp.simplify(wr([phi1, phi2, h])/wr([phi1, phi2]))
r = sp.simplify((Wop(L2(g)) - (-sp.diff(Wop(g), x, 2))).rewrite(sp.exp))
report('K1\': W (nucleo {sech^2, tanh sech}) intreccia L_q e L_0', sp.simplify(r) == 0, r)
# primo passo: A_1 = d - phi1'/phi1, q_1 = q - 2 (log phi1)''; resto W_1 = W / A_1 di ordine 1
A1 = lambda h: sp.diff(h, x) - sp.diff(phi1, x)/phi1*h
q1 = sp.simplify(q2 - 2*sp.diff(sp.log(phi1), x, 2))
report('K1\': q_1 = q - 2(log sech^2)\'\' = -2 sech^2', sp.simplify((q1 + 2*sp.sech(x)**2).rewrite(sp.exp)) == 0, q1)
psi = sp.simplify(A1(phi2))  # nucleo di W_1
A2 = lambda h: sp.diff(h, x) - sp.diff(psi, x)/psi*h
r = sp.simplify((Wop(g) - A2(A1(g))).rewrite(sp.exp))
report('K1\': W = A_2 A_1 (catena di Darboux)', sp.simplify(r) == 0, r)

# ---------- ENC-P0': lente (H = -1/2 d2 + 1/2 x^2): u = (cos t)^{-1/2} e^{-i x^2 tan t / 2} v(tan t, x / cos t)
tt, yy, aa = sp.symbols('tau y a', positive=True)
v = (1 + sp.I*tt)**sp.Rational(-1, 2)*sp.exp(-(yy - 1)**2/(2*(1 + sp.I*tt)))  # gaussiana libera traslata: i v_tau = -1/2 v_yy
report('P0\': v soluzione libera', sp.simplify(sp.I*sp.diff(v, tt) + sp.diff(v, yy, 2)/2) == 0)
u = sp.cos(t)**sp.Rational(-1, 2)*sp.exp(-sp.I*x**2*sp.tan(t)/2)*v.subs({tt: sp.tan(t), yy: x/sp.cos(t)}, simultaneous=True)
rr = sp.simplify((sp.I*sp.diff(u, t) + sp.diff(u, x, 2)/2 - x**2*u/2)/u)
report('P0\': la lente manda la soluzione libera in una dell\'oscillatore', sp.simplify(sp.trigsimp(rr)) == 0, rr)
report('P0\': a t = 0 la lente e\' l\'identita\' (M = I)', sp.simplify(u.subs(t, 0) - v.subs({tt: 0, yy: x})) == 0)

# ---------- stima di E^mult per V = cos x (verifica sul toro, FFT): ||E f|| <= (t^2/2)[(|V''| + 2t|V'|^2)||f|| + 2|V'| ||f'||]
Nn = 512; xs = np.linspace(0, 2*np.pi, Nn, endpoint=False); k = np.fft.fftfreq(Nn, d=1.0/Nn)
V = 2*np.cos(xs); Vp = 2.0; Vpp = 2.0  # sup|V'|, sup|V''|
f = np.exp(np.sin(xs)) * (1 + 0.3*np.cos(3*xs))
def U0(tv, h): return np.fft.ifft(np.exp(-1j*tv*k**2)*np.fft.fft(h))
# propagatore esatto in base di Fourier troncata: H = diag(k^2) + V (matrice), esponenziale via autodecomposizione
M = 64; kk = np.arange(-M, M+1)
Hm = np.diag(kk.astype(float)**2) + (np.eye(2*M+1, k=1) + np.eye(2*M+1, k=-1))  # 2cos x accoppia k, k+-1
w_, P_ = np.linalg.eigh(Hm)
def to_c(h):
    fh = np.fft.fft(h)/Nn; return np.array([fh[int(j) % Nn] for j in kk])
def from_c(cv):
    out = np.zeros(Nn, complex)
    for j, cj in zip(kk, cv): out += cj*np.exp(1j*j*xs)
    return out
fc = to_c(f)
norm = lambda h: np.sqrt(np.sum(np.abs(h)**2)*2*np.pi/Nn)
fprime = np.real(np.fft.ifft(1j*k*np.fft.fft(f)))
oks = []; info = []
for tv in [0.01, 0.05, 0.2, 0.5]:
    Uf = from_c(P_ @ (np.exp(-1j*tv*w_) * (P_.conj().T @ fc)))
    Lie = U0(tv, np.exp(-1j*tv*V)*f)
    E = norm(Uf - Lie)
    bound = tv**2/2*((Vpp + 2*tv*Vp**2)*norm(f) + 2*Vp*norm(fprime))
    lead = tv**2/2*norm(np.real(np.fft.ifft(-(1j*k)**2*np.fft.fft(V*f))) - V*np.real(np.fft.ifft(-(1j*k)**2*np.fft.fft(f))))
    oks.append(E <= bound); info.append((tv, round(E, 6), round(bound, 6), round(lead, 6)))
report('stima E^mult <= bound (V = 2cos x, toro)', all(oks), info)

print('\nTOTALE: %d/%d OK' % (sum(1 for _, o in res if o), len(res)))
