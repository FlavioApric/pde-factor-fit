# R3 SymPy check s01 -- C2.1d ODE a coefficienti costanti.  Run: python -I s01_ode_const.py
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
x, a, b, r = symbols('x a b r')
D = lambda f, n=1: diff(f, x, n)
def pD(f):   # p(D) = (D-a)^3 (D-b)
    g = f
    for _ in range(3): g = D(g) - a*g
    return D(g) - b*g
for k in range(3):
    check(f'(D-a)^3(D-b) x^{k} e^(ax) = 0', pD(x**k*exp(a*x)), (x, a, b))
check('(D-a)^3(D-b) e^(bx) = 0', pD(exp(b*x)), (x, a, b))
# ERF (symbol action, MIT 18.03 L14): p(D) e^{rx} = p(r) e^{rx}
check('ERF p(D)e^{rx} = p(r)e^{rx}', pD(exp(r*x)) - (r-a)**3*(r-b)*exp(r*x), (x, a, b, r))
w = symbols('w', positive=True)
check('(D^2+w^2) cos(wx) = 0', D(cos(w*x), 2) + w**2*cos(w*x), (x, w))
print('x^3 e^{ax}: p(D)(.)/e^{ax} (expected NONzero, multiplicity 3):', sp.factor(sp.simplify(pD(x**3*exp(a*x))/exp(a*x))))
W = sp.Matrix([[exp(a*x), x*exp(a*x)], [D(exp(a*x)), D(x*exp(a*x))]]).det()
check('Wronskian of (D-a)^2 basis = e^{2ax}', W - exp(2*a*x), (x, a))
summary()
