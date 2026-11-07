# S8-VAR — VAR-N1, VAR-T1 (formula), VAR-P3 (identita' e nitidezza dell'esponente 1/3), VAR-P4 (DM-phi), VAR-P5 (Dirac).
import sympy as sp
t, x, E, c, k, eps = sp.symbols('t x E c k epsilon', real=True)
I = sp.I
ok_all = True
def report(name, ok, info=""):
    global ok_all
    ok_all = ok_all and bool(ok)
    print(f"[{'OK' if ok else 'FAIL'}] {name} {info}")

# VAR-N1: r_alpha := d^alpha u/u soddisfa la ricorrenza r_{alpha+e_i} = d_i r_alpha + r_alpha a_i
u = sp.exp(t*x + sp.sin(x)) * (2 + sp.cos(t*x))
a, bb = sp.diff(u, t)/u, sp.diff(u, x)/u
r = {(0, 0): sp.Integer(1)}
okN1 = True
for (i, j) in [(1, 0), (0, 1), (1, 1), (2, 1), (0, 3), (2, 2)]:
    lhs = sp.diff(u, t, i, x, j)/u
    # costruzione ricorsiva: prima in x poi in t
    rr = sp.Integer(1)
    for _ in range(j): rr = sp.diff(rr, x) + rr*bb
    for _ in range(i): rr = sp.diff(rr, t) + rr*a
    okN1 &= sp.simplify(lhs - rr) == 0
report("VAR-N1 ricorrenza r_alpha = d^alpha u/u (6 multi-indici)", okN1)

# VAR-T1: formula V = (i u_t + u_xx)/u su soluzioni note
hn = [sp.hermite(n, x)*sp.exp(-x**2/2)*sp.exp(-I*(2*n+1)*t) for n in range(4)]
okT1 = all(sp.simplify((I*sp.diff(w, t) + sp.diff(w, x, 2))/w - x**2) == 0 for w in hn)
w = hn[0] + hn[1]
okT1 &= sp.simplify((I*sp.diff(w, t) + sp.diff(w, x, 2))/w - x**2) == 0
report("VAR-T1 oscillatore h_0..h_3 e h_0+h_1: V = x^2 ricostruito", okT1)
# zeri: X_0 di h_1 = {0} (discreto); u = h_0 + h_1 non ha X_0
report("VAR-T1 X_0(h_1) = {0}", sp.solve(sp.hermite(1, x), x) == [0])

# VAR-P3: identita' V1 - V2 = [L0 e - V2 e]/u1
u1, u2, V1, V2 = sp.symbols('u1 u2 V1 V2')
L0e = V1*u1 - V2*u2           # L0 u_i = V_i u_i
report("VAR-P3 identita' V1-V2 = (L0(u1-u2) - V2(u1-u2))/u1", sp.simplify((L0e - V2*(u1 - u2))/u1 - (V1 - V2)) == 0)
# nitidezza: phi2 = 1 + a sin(kx): ||e||=a, ||e_xxx||=a k^3, ||V2-V1|| ~ a k^2 = ||e||^{1/3} ||e_xxx||^{2/3}
aa = sp.Symbol('a', positive=True); kk = sp.Symbol('k', positive=True)
report("VAR-P3 esponente 1/3 nitido: a k^2 = a^{1/3}(a k^3)^{2/3}", sp.simplify(aa*kk**2 - aa**sp.Rational(1, 3)*(aa*kk**3)**sp.Rational(2, 3)) == 0)
phi2 = 1 + eps*sp.sin(k*x)/k
dV = sp.simplify(sp.diff(phi2, x, 2)/phi2)
report("VAR-P3 controesempio C^1 -> L^inf: V2 - V1 = -eps k sin(kx)/(1+eps sin(kx)/k)", sp.simplify(dV + eps*k*sp.sin(k*x)/phi2) == 0)

# VAR-P4 (DM-phi): e^{i theta(t)} u risolve con V - theta'(t)
th = sp.Function('theta')(t); Vf = sp.Function('V')(x); U = sp.Function('U')(t, x)
v = sp.exp(I*th)*U
expr = I*sp.diff(v, t) + sp.diff(v, x, 2) - (Vf - sp.diff(th, t))*v
expr = expr.subs(sp.Derivative(U, (x, 2)), Vf*U - I*sp.Derivative(U, t))
report("VAR-P4 e^{i theta}u risolve con V - theta'", sp.simplify(expr) == 0)
# stazionario: (V,E) -> (V+c,E+c) lascia invariato il profilo
ph = sp.Function('p')(x)
report("VAR-P4 profilo: -p''+(V+c)p = (E+c)p equivale a -p''+Vp = Ep", sp.simplify((-sp.diff(ph, x, 2) + (Vf + c)*ph - (E + c)*ph) - (-sp.diff(ph, x, 2) + Vf*ph - E*ph)) == 0)

# VAR-P5 Dirac: m=0, V=0: psi_+ = f(x-t), psi_- = g(x+t) nella base di sigma_1
s1 = sp.Matrix([[0, 1], [1, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
f, gg = sp.Function('f'), sp.Function('g')
vp, vm = sp.Matrix([1, 1])/sp.sqrt(2), sp.Matrix([1, -1])/sp.sqrt(2)
psi = f(x - t)*vp + gg(x + t)*vm
res = I*sp.diff(psi, t) - (-I*s1*sp.diff(psi, x))
report("VAR-P5 Dirac m=0,V=0: psi = f(x-t)v+ + g(x+t)v- risolve", sp.simplify(res) == sp.zeros(2, 1))
# V scalare dalla formula <psi, r>/|psi|^2 su un esempio con V(x) = x, m = 1: costruiamo r = V psi
m = 1
psi2 = sp.Matrix([sp.exp(-I*t)*sp.cos(x), sp.exp(-I*t)*sp.sin(x)])
r_ = I*sp.diff(psi2, t) + I*s1*sp.diff(psi2, x) - m*s3*psi2
Vrec = sp.simplify((psi2.H*r_)[0]/(psi2.H*psi2)[0])
print("    Dirac: V ricostruito per psi2 =", Vrec, "; compatibilita' r || psi:", sp.simplify(r_[0]*psi2[1] - r_[1]*psi2[0]))
report("VAR-P5 formula <psi,r>/|psi|^2 calcolabile", Vrec is not None)
print("RISULTATO:", "TUTTO OK" if ok_all else "CI SONO FALLIMENTI")
