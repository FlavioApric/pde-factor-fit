# F6-ENC: verifica Darboux/Crum per Poschl-Teller senza riflessione (solo verifica)
import sympy as sp
x, k, lam = sp.symbols('x k lambda')
f = sp.Function('f')(x)
L = lambda q, g: -sp.diff(g, x, 2) + q*g
A  = lambda g: sp.diff(g, x) - sp.tanh(x)*g      # A
Ad = lambda g: -sp.diff(g, x) - sp.tanh(x)*g     # A^dagger = W (encoder)
q1 = -2*sp.sech(x)**2
ok = []
r1 = sp.simplify((Ad(A(f)) - (L(0, f) + f)).rewrite(sp.exp)); ok.append(('AdA = L0+1', r1 == 0))
r2 = sp.simplify((A(Ad(f)) - (L(q1, f) + f)).rewrite(sp.exp)); ok.append(('AAd = Lq+1', r2 == 0))
r3 = sp.simplify((Ad(L(q1, f)) - L(0, Ad(f))).rewrite(sp.exp)); ok.append(('W Lq = L0 W', r3 == 0))
r4 = sp.simplify(Ad(sp.sech(x))); ok.append(('ker W = sech', r4 == 0))
# soluzione di Jost di PT mappata in onda piana
psi = (k - sp.I*sp.tanh(x))*sp.exp(-sp.I*k*x)   # = i*A e^{-ikx}, risolve L_q psi = k^2 psi
r5 = sp.simplify((L(q1, psi) - k**2*psi).rewrite(sp.exp)); ok.append(('psi sol PT', r5 == 0))
Wpsi = sp.simplify(Ad(psi).rewrite(sp.exp))
r6 = sp.simplify((L(0, Wpsi) - k**2*Wpsi).rewrite(sp.exp)); ok.append(('W psi libera', r6 == 0))
print('W psi =', sp.simplify(sp.factor(Wpsi.rewrite(sp.exp))))
# operatore commutante di ordine 3: B = A d A^dagger
B = lambda g: A(sp.diff(Ad(g), x))
r7 = sp.simplify((L(q1, B(f)) - B(L(q1, f))).rewrite(sp.exp)); ok.append(('[Lq,B]=0', r7 == 0))
# Crum n=2: q2 = -6 sech^2; A2 = d - 2tanh, A2^dag A2 = L_{q1} + 4, A2 A2^dag = L_{q2} + 4
A2  = lambda g: sp.diff(g, x) - 2*sp.tanh(x)*g
A2d = lambda g: -sp.diff(g, x) - 2*sp.tanh(x)*g
q2 = -6*sp.sech(x)**2
r8 = sp.simplify((A2d(A2(f)) - (L(q1, f) + 4*f)).rewrite(sp.exp)); ok.append(('A2d A2 = Lq1+4', r8 == 0))
r9 = sp.simplify((A2(A2d(f)) - (L(q2, f) + 4*f)).rewrite(sp.exp)); ok.append(('A2 A2d = Lq2+4', r9 == 0))
W2 = lambda g: Ad(A2d(g))   # encoder di ordine 2: L_{q2} -> L_0
r10 = sp.simplify((W2(L(q2, f)) - L(0, W2(f))).rewrite(sp.exp)); ok.append(('W2 Lq2 = L0 W2', r10 == 0))
# nucleo di W2: stati legati sech^2 (E=-4) e tanh*sech (E=-1)
r11 = sp.simplify(W2(sp.sech(x)**2)); r12 = sp.simplify(W2(sp.tanh(x)*sp.sech(x)).rewrite(sp.exp))
ok.append(('ker W2 = {sech^2, tanh sech}', r11 == 0 and r12 == 0))
# evoluzione: i u_t = L_q u => v = W u risolve i v_t = L_0 v (W non dipende da t): verifica su un modo
t = sp.symbols('t', real=True)
u = sp.exp(-sp.I*k**2*t)*psi
v = Ad(u)
r13 = sp.simplify((sp.I*sp.diff(v, t) - L(0, v)).rewrite(sp.exp)); ok.append(('Schrodinger dip. tempo', r13 == 0))
for name, val in ok: print(('OK  ' if val else 'FAIL'), name)
print('TOTALE', sum(v for _, v in ok), '/', len(ok))
