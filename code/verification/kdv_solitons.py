"""PR-C2c / schede C2.45, C2.16, C2.44 (KdV, solitoni, Hirota, Miura, Lax) -- verifiche SymPy.
Convenzione A: u_t + 6 u u_x + u_xxx = 0.
"""
import sympy as sp
import mpmath as mp

x, t = sp.symbols('x t', real=True)

def kdv(u):
    return sp.diff(u, t) + 6*u*sp.diff(u, x) + sp.diff(u, x, 3)

def numzero(expr, subs_list, prec=30):
    """valuta |expr| in punti razionali; restituisce max"""
    return max(abs(sp.N(expr.subs(s), prec)) for s in subs_list)

# [K1] 1-solitone u = (c/2) sech^2( sqrt(c)/2 (x - c t - x0) )
c, x0 = sp.symbols('c x0', positive=True)
u1 = c/2*sp.sech(sp.sqrt(c)/2*(x - c*t - x0))**2
print('[K1] KdV[1-solitone] =', sp.simplify(kdv(u1).rewrite(sp.exp)))

# [K2] Hirota: u = 2 (log f)_xx, f = 1 + e^{eta1} + e^{eta2} + A12 e^{eta1+eta2}, eta_i = k_i x - k_i^3 t
k1, k2 = sp.symbols('k1 k2', positive=True)
e1 = sp.exp(k1*x - k1**3*t); e2 = sp.exp(k2*x - k2**3*t)
A12 = ((k1 - k2)/(k1 + k2))**2
f = 1 + e1 + e2 + A12*e1*e2
# forma bilineare (D_x D_t + D_x^4) f.f = 2[ f f_xt - f_x f_t + f f_xxxx - 4 f_x f_xxx + 3 f_xx^2 ]
fx = lambda n: sp.diff(f, x, n)
bil = f*sp.diff(f, x, t) - fx(1)*sp.diff(f, t) + f*fx(4) - 4*fx(1)*fx(3) + 3*fx(2)**2
print('[K2a] (D_xD_t + D_x^4) f.f /2 =', sp.simplify(sp.expand(bil)))
u2 = 2*sp.diff(sp.log(f), x, 2)
pts = [{x: sp.Rational(i, 3), t: sp.Rational(j, 7), k1: sp.Rational(3, 2), k2: sp.Rational(4, 5)} for i in range(-4, 5, 2) for j in (-3, 0, 2)]
print('[K2b] max |KdV[u_2sol]| su 15 punti =', numzero(kdv(u2), pts))
# il coefficiente A12 e' l'UNICO dato di interazione: con A12 generico il bilineare non si annulla
Ag = sp.symbols('A')
fg = 1 + e1 + e2 + Ag*e1*e2
bilg = sp.expand(fg*sp.diff(fg, x, t) - sp.diff(fg, x)*sp.diff(fg, t) + fg*sp.diff(fg, x, 4) - 4*sp.diff(fg, x)*sp.diff(fg, x, 3) + 3*sp.diff(fg, x, 2)**2)
sol = sp.solve(sp.Eq(sp.simplify(sp.expand(bilg).subs(t, 0).subs(x, 0)), 0), Ag)
print('[K2c] A che annulla il bilineare in (0,0):', [sp.factor(s) for s in sol], ' atteso', sp.factor(A12))

# [K3] sfasamento: lungo x = k1^2 t + xi (frame del solitone veloce, k1>k2), t -> +/- inf
xi = sp.symbols('xi', real=True)
u_on1 = u2.subs(x, k1**2*t + xi)
kv = {k1: sp.Rational(2), k2: sp.Rational(1)}
fn = sp.lambdify((xi, t), u_on1.subs(kv), 'mpmath')
mp.mp.dps = 40
# posizione del picco a t = +/-T
def peak(T):
    return mp.findroot(lambda s: mp.diff(lambda q: fn(q, T), s), 0.1 if T < 0 else 1.0, tol=1e-20)
for T in (-15, 15):
    print('[K3a] t =', T, ' picco solitone veloce a xi =', mp.nstr(peak(T), 12))
d_pred = sp.N(2/kv[k1]*sp.log((kv[k1] + kv[k2])/(kv[k1] - kv[k2])), 12)
print('[K3b] salto previsto Delta xi_1 = (2/k1) ln((k1+k2)/(k1-k2)) =', d_pred, '(in avanti)')
print('      [con eta1 = k1 x - k1^3 t il picco isolato e'' a xi=0 per t->-inf e a xi=-ln(A12)/k1 per t->+inf]')
print('      -ln(A12)/k1 =', sp.N(-sp.log(A12.subs(kv))/kv[k1], 12))

# [K4] E_int "ingenuo" u - u_1 - u_2 non -> 0 per t -> +inf (sfasamento); quello con fasi corrette si'
s1 = 2*sp.diff(sp.log(1 + e1), x, 2); s2 = 2*sp.diff(sp.log(1 + e2), x, 2)
d1 = sp.log(A12);
s1p = 2*sp.diff(sp.log(1 + sp.exp(k1*x - k1**3*t + d1)), x, 2)
s2p = 2*sp.diff(sp.log(1 + sp.exp(k2*x - k2**3*t + d1)), x, 2)
Ena = sp.lambdify((x, t), (u2 - s1 - s2).subs(kv), 'mpmath')
Eco = sp.lambdify((x, t), (u2 - s1p - s2).subs(kv), 'mpmath')  # t>0: veloce sfasato di +ln(1/A12)/k1, lento non sfasato in questa normalizzazione
for T in (0, 10, 20):
    L1n = mp.quad(lambda q: abs(Ena(q, T)), [-80 + 3*T, 3*T, 80 + 4*T])
    L1c = mp.quad(lambda q: abs(Eco(q, T)), [-80 + 3*T, 3*T, 80 + 4*T])
    print(f'[K4] t={T}: ||u-u1-u2||_L1 = {mp.nstr(L1n, 8)} ;  ||u-u1(shift)-u2||_L1 = {mp.nstr(L1c, 8)}')
# massa conservata: int u dx = 4(k1+k2)/2*... verifica additivita' della massa (invariante lineare)
m = sp.lambdify((x, t), u2.subs(kv), 'mpmath')
print('[K4b] massa int u dx (t=0) =', mp.nstr(mp.quad(lambda q: m(q, 0), [-60, 0, 60]), 12), ' somma masse singole 2(k1+k2) =', 2*(2 + 1))

# [K5] Miura: v soluzione mKdV v_t - 6 v^2 v_x + v_xxx = 0  =>  u = -(v^2 + v_x) ... verifica dell'identita'
v = sp.Function('v')(x, t)
mkdv = sp.diff(v, t) - 6*v**2*sp.diff(v, x) + sp.diff(v, x, 3)
uM = -(v**2 + sp.diff(v, x))
target = -(2*v*mkdv + sp.diff(mkdv, x))
print('[K5] KdV[-(v^2+v_x)] + (2v + d_x) mKdV[v] =', sp.simplify(sp.expand(kdv(uM) - target)))

# [K6] Lax pair per la convenzione A: L = -d^2 - u, B = -4 d^3 - 6 u d - 3 u_x ;  L_t = [B, L]  <=>  KdV
u = sp.Function('u')(x, t); psi = sp.Function('psi')(x)
D = lambda g, n=1: sp.diff(g, x, n)
Lop = lambda g: -D(g, 2) - u*g
Bop = lambda g: -4*D(g, 3) - 6*u*D(g) - 3*D(u)*g
comm = sp.expand(Bop(Lop(psi)) - Lop(Bop(psi)))
Lt = -sp.diff(u, t)*psi
print('[K6] ([B,L] - L_t) psi - KdV[u] psi =', sp.simplify((comm - Lt) - kdv(u)*psi), ' ; ([B,L]-L_t) psi + KdV[u] psi =', sp.simplify((comm - Lt) + kdv(u)*psi))

# [K7] potenziale senza riflessione: -psi'' - 2 sech^2(x) psi = k^2 psi ha psi = (ik - tanh x) e^{ikx} (Jost), R=0; stato legato kappa=1
k = sp.symbols('k')
psiJ = (sp.I*k - sp.tanh(x))*sp.exp(sp.I*k*x)
print('[K7] residuo Schrodinger sech^2:', sp.simplify((-sp.diff(psiJ, x, 2) - 2*sp.sech(x)**2*psiJ - k**2*psiJ).rewrite(sp.exp)))
print('     stato legato sech x con E=-1:', sp.simplify((-sp.diff(sp.sech(x), x, 2) - 2*sp.sech(x)**3 + sp.sech(x)).rewrite(sp.exp)))



