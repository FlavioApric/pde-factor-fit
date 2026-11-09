# R3 SymPy check s12 -- C2.7d (breve, ▲): V V_x  ->  Burgers u_t + u u_x = nu u_xx  ->  Cole-Hopf u = -2 nu phi_x/phi
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
t, x, nu, k = symbols('t x nu k', positive=True)
phi = Function('phi')(t, x)
u = -2*nu*diff(phi, x)/phi
burg = diff(u, t) + u*diff(u, x) - nu*diff(u, x, 2)
heat = diff(phi, t) - nu*diff(phi, x, 2)
# identita': Burgers[u] = -2 nu d_x( heat[phi]/phi )
check('Burgers[-2nu phi_x/phi] = -2nu d_x(heat[phi]/phi)', burg + 2*nu*diff(heat/phi, x))
ph = 1 + exp(-k*x + nu*k**2*t)        # soluzione del calore -> fronte di Burgers
check('front from phi = 1 + e^{-kx + nu k^2 t}', (diff(u, t) + u*diff(u, x) - nu*diff(u, x, 2)).subs(phi, ph).doit(), (t, x, nu, k))
summary()
