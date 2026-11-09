# R3 SymPy check s03 -- C2.3d diffusione.
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
t, x, k = symbols('t x k', positive=True)
Dd = symbols('D', positive=True)
H = lambda u: diff(u, t) - Dd*diff(u, x, 2)
G = exp(-x**2/(4*Dd*t))/sqrt(4*pi*Dd*t)
check('heat kernel G', H(G), (t, x, Dd))
check('Fourier mode e^{-Dk^2 t} e^{ikx}', H(exp(-Dd*k**2*t + I*k*x)), (t, x, k, Dd))
for n in (1, 2, 3, 5):
    check(f'd_x^{n} G  (Hermite-Gauss family)', H(diff(G, x, n)), (t, x, Dd))
n = 4; z = x/sqrt(4*Dd*t)
check('Rodrigues: d_x^4 G = (4Dt)^{-2} H_4(z) G', diff(G, x, n) - (4*Dd*t)**(-sp.Rational(n, 2))*hermite(n, z)*G, (t, x, Dd))
def v(n):
    return sum(sp.factorial(n)/(sp.factorial(j)*sp.factorial(n-2*j))*x**(n-2*j)*(Dd*t)**j for j in range(n//2+1))
for n in (2, 3, 6):
    check(f'heat polynomial v_{n}', H(v(n)), (t, x, Dd))
He = lambda n, y: sp.expand(2**(-sp.Rational(n, 2))*hermite(n, y/sqrt(2)))
for n in (3, 4):
    check(f'v_{n}(x,-1/(2D)) = He_{n}(x)', sp.expand(v(n).subs(t, -1/(2*Dd))) - He(n, x), (x,))
# Appell transform (D=1): A[u](t,x) = G(t,x) u(-1/t, x/t)
G1 = G.subs(Dd, 1); v3 = v(3).subs(Dd, 1)
A = G1*v3.subs({t: -1/t, x: x/t}, simultaneous=True)
check('Appell transform of v_3 solves heat (D=1)', (diff(A, t) - diff(A, x, 2)), (t, x))
check('similarity erf(x/sqrt(4Dt))', H(sp.erf(x/sqrt(4*Dd*t))), (t, x, Dd))
summary()
