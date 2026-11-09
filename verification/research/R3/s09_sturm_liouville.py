# R3 SymPy check s09 -- Sturm-Liouville: ortogonalita' pesata, identita' di Lagrange.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
import mpmath as mp
x = symbols('x', real=True)
check('Dirichlet [0,pi]: <sin 2x, sin 5x> = 0', integrate(sin(2*x)*sin(5*x), (x, 0, pi)))
check('Dirichlet [0,pi]: ||sin 5x||^2 = pi/2', integrate(sin(5*x)**2, (x, 0, pi)) - pi/2)
check('Legendre <P2,P5> = 0', integrate(legendre(2, x)*legendre(5, x), (x, -1, 1)))
check('Legendre ||P4||^2 = 2/9', integrate(legendre(4, x)**2, (x, -1, 1)) - sp.Rational(2, 9))
check('Hermite <H2,H4>_{e^{-x^2}} = 0', integrate(hermite(2, x)*hermite(4, x)*exp(-x**2), (x, -oo, oo)))
check('Hermite ||H3||^2 = 2^3 3! sqrt(pi)', integrate(hermite(3, x)**2*exp(-x**2), (x, -oo, oo)) - 48*sqrt(pi))
mp.mp.dps = 30
a1, a2 = mp.besseljzero(0, 1), mp.besseljzero(0, 2)
val = mp.quad(lambda s: s*mp.besselj(0, a1*s)*mp.besselj(0, a2*s), [0, 1])
print('Fourier-Bessel <J0(j1 x), J0(j2 x)>_x on [0,1] (expected 0):', val)
RES.append(('Fourier-Bessel orthogonality (numeric control)', 'PASS-num' if abs(val) < 1e-25 else 'FAIL'))
p, q = Function('p')(x), Function('q')(x)
u, v = Function('u')(x), Function('v')(x)
Lsl = lambda y: -diff(p*diff(y, x), x) + q*y
check("Lagrange identity vLu - uLv = d/dx[p(u v' - v u')]", v*Lsl(u) - u*Lsl(v) - diff(p*(u*diff(v, x) - v*diff(u, x)), x))
summary()
