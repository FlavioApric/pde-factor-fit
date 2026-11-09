# R3 SymPy check s07 -- Laplaciano polare / cilindrico / sferico assisimmetrico.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
r, th, t, z, k = symbols('r theta t z k', positive=True)
Lap2 = lambda f: diff(f, r, 2) + diff(f, r)/r + diff(f, th, 2)/r**2
for n in (0, 1, 3):
    e = besselj(n, k*r)*exp(I*n*th)
    check(f'Helmholtz polar J_{n}(kr) e^(in th)', Lap2(e) + k**2*e, (r, th, k))
    check(f'harmonic r^{n} e^(in th)', Lap2(r**n*exp(I*n*th)), (r, th))
    if n > 0: check(f'harmonic r^-{n} e^(in th)', Lap2(r**(-n)*exp(I*n*th)), (r, th))
check('harmonic log r', Lap2(log(r)), (r,))
u = exp(-k**2*t)*besselj(0, k*r)
check('radial heat e^{-k^2 t} J0(kr)', diff(u, t) - Lap2(u), (t, r, k))
G2 = exp(-r**2/(4*t))/(4*pi*t)
check('2D heat kernel (radial)', diff(G2, t) - Lap2(G2), (t, r))
Lap3c = lambda f: Lap2(f) + diff(f, z, 2)
check('cylindrical harmonic J_2(kr) e^{2i th} e^{kz}', Lap3c(besselj(2, k*r)*exp(2*I*th)*exp(k*z)), (r, th, z, k))
check('cylindrical harmonic I_1(kr) e^{i th} cos(kz)', Lap3c(sp.besseli(1, k*r)*exp(I*th)*cos(k*z)), (r, th, z, k))
Lsph = lambda f: diff(r**2*diff(f, r), r)/r**2 + diff(sin(th)*diff(f, th), th)/(r**2*sin(th))
for l in (1, 2, 4):
    check(f'spherical r^{l} P_{l}(cos th)', Lsph(r**l*legendre(l, cos(th))), (r, th))
    check(f'spherical r^-{l+1} P_{l}(cos th)', Lsph(r**(-l-1)*legendre(l, cos(th))), (r, th))
check('3D Newton potential 1/r', Lsph(1/r), (r,))
summary()
