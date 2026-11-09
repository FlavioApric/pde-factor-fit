# R3 SymPy check s06 -- C2.6d coefficienti dipendenti da x: Euler-Cauchy/Mellin, Hermite, OU, Mehler, Legendre, Bessel/Frobenius.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
x, t, y = symbols('x t y', positive=True); s, mm, r = symbols('s m r')
nu = symbols('nu', positive=True)
check('Euler operator: x dx x^s = s x^s', x*diff(x**s, x) - s*x**s, (x,))
ECd = lambda f: x**2*diff(f, x, 2) + (1-2*mm)*x*diff(f, x) + mm**2*f
check('Euler-Cauchy double root: x^m', ECd(x**mm), (x,))
check('Euler-Cauchy double root: x^m log x', ECd(x**mm*log(x)), (x,))
xr = symbols('xr', real=True)
for n in (0, 1, 4, 7):
    Hn = hermite(n, xr)
    check(f'Hermite ODE H_{n}', diff(Hn, xr, 2) - 2*xr*diff(Hn, xr) + 2*n*Hn)
    hn = Hn*exp(-xr**2/2)
    check(f'Hermite function h_{n}: (-d2+x2)h = (2n+1)h', -diff(hn, xr, 2) + xr**2*hn - (2*n+1)*hn)
for n in (0, 2, 3):
    He = sp.expand(2**(-sp.Rational(n, 2))*hermite(n, xr/sqrt(2)))
    u = exp(-n*t)*He*exp(-xr**2/2)
    check(f'OU Fokker-Planck u_t = u_xx + (xu)_x, mode n={n}', diff(u, t) - diff(u, xr, 2) - diff(xr*u, xr))
Mk = (2*pi*sinh(2*t))**(-sp.Rational(1, 2))*exp(-((xr**2 + y**2)*cosh(2*t) - 2*xr*y)/(2*sinh(2*t)))
check('Mehler kernel: (dt - dxx + x^2) M = 0', diff(Mk, t) - diff(Mk, xr, 2) + xr**2*Mk, (t, xr, y))
z = symbols('z')
Leg = lambda f, n: (1-z**2)*diff(f, z, 2) - 2*z*diff(f, z) + n*(n+1)*f
for n in (0, 1, 3, 6):
    check(f'Legendre P_{n}', Leg(legendre(n, z), n))
check('Legendre Q_0 = atanh z', Leg(atanh(z), 0), (z,), domain=(0.1, 0.9))
check('Legendre Q_1 = z atanh z - 1', Leg(z*atanh(z) - 1, 1), (z,), domain=(0.1, 0.9))
Bes = lambda f, v: x**2*diff(f, x, 2) + x*diff(f, x) + (x**2 - v**2)*f
for v in (0, 1, sp.Rational(1, 3), nu):
    check(f'Bessel J_{v}', Bes(besselj(v, x), v), (x, nu))
    check(f'Bessel Y_{v}', Bes(bessely(v, x), v), (x, nu))
check('Bessel nu=1/2: sin(x)/sqrt(x)', Bes(sin(x)/sqrt(x), sp.Rational(1, 2)), (x,))
ind = sp.expand(sp.simplify(Bes(x**r, nu)/x**r)).subs(x, 0)
check('Bessel indicial equation r^2 - nu^2', ind - (r**2 - nu**2))
summary()
