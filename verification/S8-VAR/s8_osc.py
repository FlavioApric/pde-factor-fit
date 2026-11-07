# S8-VAR — VAR-T10 corretto. (a) Stark/Avron-Herbst: U(t) = e^{i theta} e^{-i p x} T_b U_0(t) esatto per ogni t.
# (b) Oscillatore H = -d^2 + x^2: parola chirp.libero.chirp. Matrici di Mobius sui parametri gaussiani,
#     decomposizione valida <=> sin 2t != 0 (anche a t = pi/4, caustica della lente in questa normalizzazione).
# (c) verifica operatoriale numerica: W(t) f = c(t) U(t) f con lo STESSO c per due f diversi.
import sympy as sp
import numpy as np
t, x, y, al, gam, s = sp.symbols('t x y alpha gamma s')
I = sp.I
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")
# (a)
Ff = sp.Function('F')(t); p = sp.Function('p')(t); b = sp.Function('b')(t); th = sp.Function('theta')(t)
phi = sp.Function('phi')
Y = x - b
psi = sp.exp(I*th)*sp.exp(-I*p*x)*phi(t, Y)
expr = I*sp.diff(psi, t) + sp.diff(psi, x, 2) - Ff*x*psi
expr = expr.subs({sp.diff(p, t): Ff, sp.diff(b, t): -2*p, sp.diff(th, t): -p**2})
yy = sp.Symbol('yy')
expr = expr.doit()
# usa l'equazione libera i phi_t = -phi_yy
expr = expr.replace(lambda e: isinstance(e, sp.Subs), lambda e: e.doit())
e2 = sp.simplify(expr.subs(sp.Derivative(phi(t, Y), t), I*sp.Derivative(phi(t, Y), (x, 2))))
ys = sp.Symbol('ys')
e3 = sp.simplify((expr / (sp.exp(I*th)*sp.exp(-I*p*x))).subs(x, ys + b))
e3 = e3.doit()
e3 = sp.simplify(e3.subs(sp.Derivative(phi(t, ys), t), I*sp.Derivative(phi(t, ys), (ys, 2))))
report("(a) Avron-Herbst: p'=F, b'=-2p, theta'=-p^2 => psi risolve i psi_t = -psi_xx + F(t) x psi", e3 == 0, str(e3)[:80])
# (b) Gaussiane exp(-alpha x^2/2)
N = sp.Function('N')(t); a_ = sp.Function('a')(t)
g = N*sp.exp(-a_*x**2/2)
osc = sp.simplify((I*sp.diff(g, t) + sp.diff(g, x, 2) - x**2*g)/g)
sol_a = sp.solve(sp.Poly(sp.expand(osc), x).coeffs()[0], sp.diff(a_, t))[0]
report("(b1) oscillatore: alpha' = 2i(1 - alpha^2)", sp.simplify(sol_a - 2*I*(1 - a_**2)) == 0)
free = sp.simplify((I*sp.diff(g, t) + sp.diff(g, x, 2))/g)
report("(b2) libero: alpha' = -2i alpha^2", sp.simplify(sp.solve(sp.Poly(sp.expand(free), x).coeffs()[0], sp.diff(a_, t))[0] + 2*I*a_**2) == 0)
C = lambda gg: sp.Matrix([[1, -2*I*gg], [0, 1]]); Fm = lambda ss: sp.Matrix([[1, 0], [2*I*ss, 1]])
Mo = sp.Matrix([[sp.cos(2*t), I*sp.sin(2*t)], [I*sp.sin(2*t), sp.cos(2*t)]])
G = sp.Matrix([[0, 2*I], [2*I, 0]])
report("(b3) exp(tG) = M_osc(t)", sp.simplify((G*t).exp() - Mo) == sp.zeros(2))
gs = (sp.cos(2*t) - 1)/(2*sp.sin(2*t)); ss = sp.sin(2*t)/2
report("(b4) M_osc = C(gam) F(s) C(gam), gam = (cos2t-1)/(2 sin2t), s = sin(2t)/2", sp.simplify(C(gs)*Fm(ss)*C(gs) - Mo) == sp.zeros(2))
# nessuna decomposizione C F C se sin 2t = 0 (l'entrata (2,1) di C F C e' 2is)
report("(b5) (C F C)_{21} = 2 i s: a t = pi/2 serve s = 0, e allora CFC e' triangolare != M(pi/2) = -I? (M(pi/2) = -I: s=0 e gam=0 la danno)",
       sp.simplify((C(gam)*Fm(s)*C(gam))[1, 0] - 2*I*s) == 0)
print("    nota: a t = pi/2, M = -I e' proiettivamente l'identita' (U(pi/2) = parita' a meno di fase): la parola degenera, ma U e' banale; il primo vero ostacolo della parola fissa e' sin 2t = 0.")
# (c) numerico, operatori
Np, Lb = 1024, 30.0
xs = np.linspace(-Lb, Lb, Np, endpoint=False); dx = xs[1]-xs[0]; ks = 2*np.pi*np.fft.fftfreq(Np, d=dx)
U0 = lambda tt, v: np.fft.ifft(np.exp(-1j*tt*ks**2)*np.fft.fft(v))
Ffft = np.fft.fft(np.eye(Np), axis=0); D2 = np.real(np.fft.ifft(-(ks**2)[:, None]*Ffft, axis=0))
Hm = -D2 + np.diag(xs**2); w, Q = np.linalg.eigh((Hm + Hm.T)/2)
Uex = lambda tt, v: Q @ (np.exp(-1j*tt*w)*(Q.T @ v))
f1 = (xs + xs**3)*np.exp(-xs**2); f2 = np.exp(-(xs - 1)**2/2 + 0.5j*xs)
okc = True; info = []
for tt in [0.3, np.pi/4, 1.3]:
    gv = (np.cos(2*tt) - 1)/(2*np.sin(2*tt)); sv = np.sin(2*tt)/2
    W = lambda v: np.exp(1j*gv*xs**2)*U0(sv, np.exp(1j*gv*xs**2)*v)
    c1 = np.vdot(Uex(tt, f1), W(f1))/np.vdot(f1, f1); c2 = np.vdot(Uex(tt, f2), W(f2))/np.vdot(f2, f2)
    e1 = np.max(np.abs(W(f1) - c1*Uex(tt, f1))); e2 = np.max(np.abs(W(f2) - c1*Uex(tt, f2)))
    okc &= abs(abs(c1) - 1) < 1e-8 and abs(c1 - c2) < 1e-8 and e1 < 1e-7 and e2 < 1e-7
    info.append(f"t={tt:.3f}: |c|={abs(c1):.10f}, err={max(e1, e2):.1e}")
report("(c) chirp(gam).libero(s).chirp(gam) = c(t) U(t), stesso c su due f (t = 0.3, pi/4, 1.3)", okc, "; ".join(info))
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
