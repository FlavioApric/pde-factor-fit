# R3 SymPy check s05 -- C2.5d reazione.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
t, x = symbols('t x', positive=True); r, Dd, m = symbols('r D m', positive=True)
h = Function('h')
check('(dt - r) e^{rt} h(x) = 0', diff(exp(r*t)*h(x), t) - r*exp(r*t)*h(x))
G = exp(-x**2/(4*Dd*t))/sqrt(4*pi*Dd*t); u = exp(r*t)*G
check('(dt - D dxx - r) e^{rt} G = 0 (commuting product)', diff(u, t) - Dd*diff(u, x, 2) - r*u, (t, x, Dd, r))
check('(dxx - m^2) e^{-mx} = 0', diff(exp(-m*x), x, 2) - m**2*exp(-m*x))
gm = exp(-m*x)/(2*m)
check('Green of (-dxx+m^2): jump of derivative of e^{-m|x|}/2m is -1', 2*diff(gm, x).subs(x, 0) + 1)
summary()
