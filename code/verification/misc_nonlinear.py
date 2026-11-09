"""PR-C2c / verifiche brevi per schede C2.15, C2.24, C2.44, C2.45, C2.47, C2.40, C2.41."""
import sympy as sp

x, t = sp.symbols('x t', real=True)
v = sp.symbols('v', real=True)

# [M1] sine-Gordon kink: u_tt - u_xx + sin u = 0, |v|<1
g = 1/sp.sqrt(1 - v**2)
uk = 4*sp.atan(sp.exp(g*(x - v*t)))
r = sp.diff(uk, t, 2) - sp.diff(uk, x, 2) + sp.sin(uk)
print('[M1] sine-Gordon kink residuo (numerico, v=0.3):', max(abs(sp.N(r.subs({v: sp.Rational(3, 10), x: a, t: b}))) for a in (-1, 0, 2) for b in (0, 1)))

# [M2] NLS focalizzante i u_t + u_xx/2 + |u|^2 u = 0 : u = a sech(a x) e^{i a^2 t/2}
a = sp.symbols('a', positive=True)
un = a*sp.sech(a*x)*sp.exp(sp.I*a**2*t/2)
print('[M2] NLS bright soliton:', sp.simplify((sp.I*sp.diff(un, t) + sp.diff(un, x, 2)/2 + a**2*sp.sech(a*x)**2*un).rewrite(sp.exp)))

# [M3] Fisher-KPP u_t = u_xx + u(1-u): onda di Ablowitz-Zeppetella u = (1 + C e^{z/sqrt6})^{-2}, z = x - 5t/sqrt6
C = sp.symbols('C', positive=True)
z = x - 5*t/sp.sqrt(6)
uf = (1 + C*sp.exp(z/sp.sqrt(6)))**-2
print('[M3] Fisher-KPP Ablowitz-Zeppetella:', sp.simplify(sp.diff(uf, t) - sp.diff(uf, x, 2) - uf*(1 - uf)))

# [M4] Burgers inviscido u_t + u u_x = 0: soluzione implicita u = F(x - u t) (caratteristiche/odografo)
F = sp.Function('F')
U = sp.Function('U')(x, t)
Gimp = U - F(x - U*t)
Ux = -sp.diff(Gimp, x)/sp.diff(Gimp, U).subs(sp.Derivative(U, x), 0) if False else None
# derivazione implicita: U_x = F'/(1+tF'), U_t = -U F'/(1+tF')
Fp = sp.symbols('Fp')
Ux_ = Fp/(1 + t*Fp); Ut_ = -U*Fp/(1 + t*Fp)
print('[M4] U_t + U U_x =', sp.simplify(Ut_ + U*Ux_), ' ; blow-up di U_x quando 1 + t F\' = 0  =>  t* = -1/min F\'')

# [M5] blow-up ODE/PDE omogenea: u_t = u_xx + u^2, u(0)=u0 costante -> u = u0/(1 - u0 t), T* = 1/u0
u0 = sp.symbols('u0', positive=True)
ub = u0/(1 - u0*t)
print('[M5] u_t - u_xx - u^2 =', sp.simplify(sp.diff(ub, t) - sp.diff(ub, x, 2) - ub**2))

# [M6] Fokker-Planck di Ornstein-Uhlenbeck p_t = (x p)_x + D p_xx: nucleo gaussiano con media x0 e^{-t}, varianza D(1-e^{-2t})
D, x0 = sp.symbols('D x0', positive=True)
s2 = D*(1 - sp.exp(-2*t))
p = sp.exp(-(x - x0*sp.exp(-t))**2/(2*s2))/sp.sqrt(2*sp.pi*s2)
print('[M6] OU Fokker-Planck:', sp.simplify(sp.diff(p, t) - sp.diff(x*p, x) - D*sp.diff(p, x, 2)))

# [M7] Feynman-Kac con potenziale lineare V = b x : u_t = u_xx/2 - b x u ; u = E[exp(-int_0^t b(x+W_s)ds) f(x+W_t)]
#      per f = 1: u = exp(-b x t + b^2 t^3/6)  (int W ds ~ N(0, t^3/3))
b = sp.symbols('b', real=True)
uFK = sp.exp(-b*x*t + b**2*t**3/6)
print('[M7] Feynman-Kac (V=bx, f=1):', sp.simplify(sp.diff(uFK, t) - sp.diff(uFK, x, 2)/2 + b*x*uFK))

# [M8] Vlasov libero / trasporto cinetico f_t + v f_x = 0 : f = g(x - v t, v)
gfun = sp.Function('g')
fk = gfun(x - v*t, v)
print('[M8] trasporto libero cinetico:', sp.simplify(sp.diff(fk, t) + v*sp.diff(fk, x)))

# [M9] acustica (Eulero compressibile linearizzato) rho_t + rho0 w_x = 0, w_t + c^2/rho0 rho_x = 0 -> invarianti di Riemann
rho0, cs = sp.symbols('rho0 c', positive=True)
fp, fm = sp.Function('fp'), sp.Function('fm')
rr = fp(x - cs*t) + fm(x + cs*t); ww = cs/rho0*(fp(x - cs*t) - fm(x + cs*t))
print('[M9] acustica 1D:', sp.simplify(sp.diff(rr, t) + rho0*sp.diff(ww, x)), sp.simplify(sp.diff(ww, t) + cs**2/rho0*sp.diff(rr, x)))

# [M10] Stefan a una fase (Neumann): T = A erf(x/(2 sqrt t)) ... interfaccia s(t)=2 lam sqrt(t); verifica equazione del calore
lam = sp.symbols('lam', positive=True)
T = sp.erf(x/(2*sp.sqrt(t)))
print('[M10] Stefan: T_t - T_xx =', sp.simplify(sp.diff(T, t) - sp.diff(T, x, 2)), '; fronte s=2 lam sqrt(t) (lam da eq. trascendente lam e^{lam^2} erf(lam) = St/sqrt(pi))')
