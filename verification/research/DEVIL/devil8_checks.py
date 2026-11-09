# DEVIL-8: verifiche SymPy (solo verifica, nessuna scoperta). Eseguire con
#   D:\ProblemaBase\.venv\Scripts\python.exe -I devil8_checks.py
import sympy as sp

t, x, y, a0, eps = sp.symbols('t x y a0 epsilon', real=True)
res = []
def check(name, ok, info=''):
    res.append(ok)
    print(('PASS ' if ok else 'FAIL ') + name + ((' :: ' + info) if info else ''))

# (A) Normalizzazione di VAR-6 / F5. i u_t = H u.
# H = -d^2 + x^2: x' = 2p, p' = -2x. H/2: x' = p, p' = -x.
def flow(w, m):
    # flusso classico x'' = -w^2 x con x' = m p
    return sp.Matrix([[sp.cos(w*t), m*sp.sin(w*t)/w], [-w*sp.sin(w*t)/m, sp.cos(w*t)]])
def lower(g): return sp.Matrix([[1, 0], [g, 1]])
def upper(b): return sp.Matrix([[1, b], [0, 1]])
for lab, w, m in [('H=-d2+x2', 2, 2), ('H/2', 1, 1)]:
    S = flow(w, m)
    a_, b_, c_, d_ = S
    dec = lower((d_-1)/b_) * upper(b_) * lower((a_-1)/b_)
    ok = sp.simplify(dec - S) == sp.zeros(2)
    first_zero = sp.nsolve(b_, t, 1.5 if w == 2 else 3.0)
    check(f'(A) chirp*libero*chirp per {lab}: identita valida dove b!=0; primo zero b(t) a t={first_zero:.6f}', ok)
check('(A) per H=-d2+x2 lo zero t=pi/2 coincide con cos t=0',
      sp.simplify(sp.sin(2*t).subs(t, sp.pi/2)) == 0 and sp.cos(sp.pi/2) == 0)
check('(A) per H/2 la rottura e a t=pi (|t|<pi di DEVIL-6 vale solo per H/2)',
      sp.sin(sp.pi) == 0 and sp.sin(sp.pi/2) != 0)

# (C) ENC2-4: per V=0 un rappresentante pseudo-conforme con theta != id.
a = a0/(1+4*a0*t)
u = (1+4*a0*t)**sp.Rational(-1, 2)*sp.exp(sp.I*a*x**2)
check('(C) a(t)=a0/(1+4a0 t) risolve a\'+4a^2=0', sp.simplify(sp.diff(a, t)+4*a**2) == 0)
check('(C) u=(1+4a0t)^(-1/2) e^{i a x^2} risolve i u_t = -u_xx (V=0)',
      sp.simplify(sp.I*sp.diff(u, t)+sp.diff(u, x, 2)) == 0)
theta = t/(1+4*a0*t)
check('(C) theta(t)=t/(1+4a0 t) != t per a0 != 0 (V=0 ha rappresentanti con theta != id)',
      sp.simplify(theta - t) != 0)

# (D) Avron-Herbst: V = beta(t) x si toglie con theta = id.
beta = sp.Function('beta')
B = sp.Function('B')      # B' = beta
s = sp.Function('s')      # traslazione
g = sp.Function('g')      # fase
U2 = sp.exp(sp.I*(-B(t)*x + g(t)))
# u = U2 * w(t, x - s(t)); w_t = i w_YY (libero)
w0, w1, w2, wt = sp.symbols('w0 w1 w2 wt')
ut = sp.diff(U2, t)*w0 + U2*(wt - sp.diff(s(t), t)*w1)
ux = sp.diff(U2, x)*w0 + U2*w1
uxx = sp.diff(U2, x, 2)*w0 + 2*sp.diff(U2, x)*w1 + U2*w2
Rexpr = sp.expand((sp.I*ut + uxx - beta(t)*x*U2*w0)/U2)
Rexpr = Rexpr.subs(wt, sp.I*w2)
Rexpr = Rexpr.subs(sp.diff(B(t), t), beta(t))
cond = sp.Poly(sp.expand(Rexpr), w0, w1, w2)
coeffs = {m: sp.simplify(cf) for m, cf in zip(cond.monoms(), cond.coeffs())}
c_w1 = coeffs.get((0, 1, 0), 0).subs(sp.diff(s(t), t), -2*B(t))
c_w0 = coeffs.get((1, 0, 0), 0).subs(sp.diff(g(t), t), -B(t)**2)
check('(D) Avron-Herbst: con B\'=beta, s\'=-2B, g\'=-B^2 il residuo si annulla (tempo invariato, theta=id)',
      sp.simplify(c_w1) == 0 and sp.simplify(c_w0) == 0 and coeffs.get((0, 0, 1), 0) == 0,
      f'coeff w1 -> {sp.simplify(c_w1)}, coeff w0 -> {sp.simplify(c_w0)}')

# (E) VAR-N1: in un anello chiuso per derivazione Ann(u) e sempre di rango massimo.
uu = sp.Function('u')(t, x)
check('(E) (d_t - u_t/u) u = 0 e (d_x - u_x/u) u = 0 per ogni u senza zeri',
      sp.simplify(sp.diff(uu, t) - sp.diff(uu, t)/uu*uu) == 0 and sp.simplify(sp.diff(uu, x) - sp.diff(uu, x)/uu*uu) == 0)

# (F) "identificabile" come ker Phi_u = 0 senza esistenza di una legge.
aa, bb = sp.symbols('a b')
uF = t + sp.sin(x)
Phi = aa*sp.diff(uF, x, 2) + bb*uF   # classe u_t = a u_xx + b u
ker = sp.solve([sp.expand(Phi).coeff(t, 1), sp.expand(Phi).subs(t, 0).coeff(sp.sin(x))], [aa, bb], dict=True)
law = sp.solve([sp.expand(Phi - sp.diff(uF, t)).coeff(t, 1),
                sp.expand(Phi - sp.diff(uF, t)).subs(t, 0).coeff(sp.sin(x)),
                sp.expand(Phi - sp.diff(uF, t)).subs({t: 0, sp.sin(x): 0})], [aa, bb], dict=True)
check('(F) u=t+sin x, classe u_t=a u_xx+b u: ker Phi_u = 0 ma nessuna legge esiste',
      ker == [{aa: 0, bb: 0}] and law == [], f'ker={ker}, leggi={law}')

# (H) SYS-S1-C: e^{1/(1-t)} non si estende come distribuzione oltre t=1.
for N in (5, 20):
    L = sp.limit(eps**(N+1)*sp.exp(1/(3*eps)), eps, 0, '+')
    check(f'(H) eps^{N+1} e^(1/(3 eps)) -> oo (nessuna stima d\'ordine {N})', L == sp.oo)

print(f'\nTOTALE: {sum(res)}/{len(res)} PASS')
