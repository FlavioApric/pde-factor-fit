# R3 SymPy check s10 -- C4/A8 sul catalogo: somme vs prodotti, lemma di decomposizione, E_int.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
t, x, k, c, Dd = symbols('t x k c D', positive=True)
L1 = lambda u: diff(u, t) + c*diff(u, x)            # trasporto
L2p = lambda u: -Dd*diff(u, x, 2)                   # parte spaziale della diffusione
L = lambda u: L1(u) + L2p(u)                        # advezione-diffusione  dt + c dx - D dxx
G = exp(-(x - c*t)**2/(4*Dd*t))/sqrt(4*pi*Dd*t)
check('advection-diffusion: G(t, x-ct) in ker L (= S_heat S_transport)', L(G), (t, x, c, Dd))
u0 = exp(I*k*x); S1 = exp(I*k*(x - c*t)); S2 = exp(-Dd*k**2*t + I*k*x); S12 = exp(I*k*(x - c*t) - Dd*k**2*t)
check('full Fourier mode solves L', L(S12), (t, x, k, c, Dd))
Eint = S12 - (u0 + (S1 - u0) + (S2 - u0))
check('E_int = (S1-I)(S2-I)u0  (bilinear)', Eint - u0*(exp(-I*k*c*t) - 1)*(exp(-Dd*k**2*t) - 1), (t, x, k, c, Dd))
check('log-symbol additivity: dt log(u_hat/u0_hat) = -ikc - Dk^2', diff(sp.log(sp.exp(-I*k*c*t - Dd*k**2*t)), t) - (-I*k*c - Dd*k**2), (t, k, c, Dd))
# Decomposable solutions (Lemma R3-L1): a=(x-ct)^2 in ker L1, b=2Dt in ker(dt... ) ; here split L = L1 + L2' with b in ker L2'
a = (x - c*t)**2; b = 2*Dd*t
check('L1 a = 0', L1(a)); check("L2' b = 0", L2p(b)); check('L(a+b) = 0', L(a + b))
s = symbols('s'); al, be = symbols('alpha beta'); g = Function('g')
print("a = g(s), s=x-ct, with D g'' in span{1,s} (= ker L1 cap ker L2'):", sp.dsolve(sp.Eq(diff(g(s), s, 2), al + be*s), g(s)))
tau, xi = symbols('tau xi')
print('factor_list of symbol tau + c xi - D xi^2 (irreducible):', sp.factor_list(tau + c*xi - Dd*xi**2))
# Generic heat-like solution of L NOT decomposable: G(t,x-ct) - check that L2' G != 0 is not in ker L1 cap ker L2'
w = sp.simplify(L2p(G))
print('L2\' G (must lie in span{1,x-ct} for G to be decomposable):', sp.simplify(w/G))
mode = exp(I*k*x + (I*k**3 - Dd*k**2)*t)
check('diffusion+dispersion mode u_t = D u_xx - u_xxx', diff(mode, t) - Dd*diff(mode, x, 2) + diff(mode, x, 3), (t, x, k, Dd))
F, Hh = Function('F'), Function('H')
wv = F(x - c*t) + Hh(x + c*t)
check("wave = (dt - c dx)(dt + c dx): d'Alembert F(x-ct)+H(x+ct)", diff(wv, t, 2) - c**2*diff(wv, x, 2))
f = Function('f')(x)
check("[x dx, dxx] f = -2 f''  (non-commuting terms)", x*diff(diff(f, x, 2), x) - diff(x*diff(f, x), x, 2) + 2*diff(f, x, 2))
summary()
