"""PR-C2d / C2.13, C2.36, C2.51, C2.55, C2.56 — checks.
Run: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I s1_sturm_liouville_green.py
"""
import sympy as sp

x, y, r, k = sp.symbols('x y r k', real=True)
n, m = sp.symbols('n m', integer=True, positive=True)
res = []
def ok(name, cond):
    res.append((name, bool(cond))); print(('PASS ' if cond else 'FAIL ') + name)

# (a) Dirichlet SL on [0,pi]: -u''=lam u, e_n = sin(n x), lam_n=n^2; orthogonality (Gram diagonal)
e = lambda j: sp.sin(j*x)
ok('a1 -e_n\'\' = n^2 e_n', sp.simplify(-sp.diff(e(n), x, 2) - n**2*e(n)) == 0)
G = sp.Matrix(4, 4, lambda i, j: sp.integrate(e(i+1)*e(j+1), (x, 0, sp.pi)))
ok('a2 Gram of {sin nx}_{n<=4} = (pi/2) I', G == sp.pi/2*sp.eye(4))

# (b) Green function of -d^2/dx^2, Dirichlet on [0,pi]: G(x,y)= x(pi-y)/pi (x<y), y(pi-x)/pi (x>y)
Gl = x*(sp.pi-y)/sp.pi; Gr = y*(sp.pi-x)/sp.pi
ok('b1 -G_xx=0 off-diagonal', sp.diff(Gl, x, 2) == 0 and sp.diff(Gr, x, 2) == 0)
ok('b2 BC G(0,y)=G(pi,y)=0', Gl.subs(x, 0) == 0 and sp.simplify(Gr.subs(x, sp.pi)) == 0)
jump = sp.simplify((sp.diff(Gr, x) - sp.diff(Gl, x)).subs(x, y))
ok('b3 jump of G_x at x=y equals -1 (delta)', jump == -1)
# bilinear (Mercer) expansion: Fourier-sine coefficient of G(.,y) = (2/pi) sin(ny)/n^2
cn = sp.simplify(2/sp.pi*(sp.integrate(Gl*sp.sin(n*x), (x, 0, y)) + sp.integrate(Gr*sp.sin(n*x), (x, y, sp.pi))))
ok('b4 G(x,y)=sum (2/pi) sin(nx)sin(ny)/n^2  [coefficient check]', sp.simplify(cn - 2/sp.pi*sp.sin(n*y)/n**2) == 0)

# (c) Green function = reproducing kernel of H^1_0(0,pi) with <u,v>=int u'v'
v = x*(sp.pi-x)*(1+x**2)   # test element of H^1_0
Kx = lambda yy: None
# K(x0,.) as a function of the integration variable s; x0 fixed symbol
s, x0 = sp.symbols('s x0', positive=True)
K_left = s*(sp.pi-x0)/sp.pi      # s < x0
K_right = x0*(sp.pi-s)/sp.pi     # s > x0
vs = v.subs(x, s)
ip = sp.integrate(sp.diff(K_left, s)*sp.diff(vs, s), (s, 0, x0)) + sp.integrate(sp.diff(K_right, s)*sp.diff(vs, s), (s, x0, sp.pi))
ok('c1 <G(x0,.), v>_{H^1_0} = v(x0)  (RKHS reproducing property)', sp.simplify(ip - v.subs(x, x0)) == 0)

# (d) Robin BC u'(0)=h u(0), u(pi)=0 : eigenfunctions cos(kx)+ (h/k) sin(kx), eigen-eq tan(k pi) = -k/h
phi = sp.cos(k*x) + sp.Symbol('h')/k*sp.sin(k*x)
h = sp.Symbol('h')
ok('d1 Robin: phi\'(0)=h phi(0)', sp.simplify(sp.diff(phi, x).subs(x, 0) - h*phi.subs(x, 0)) == 0)
ok('d2 Robin eigen-equation phi(pi)=0 <=> k cos(k pi)+h sin(k pi)=0', sp.simplify(k*phi.subs(x, sp.pi) - (k*sp.cos(k*sp.pi)+h*sp.sin(k*sp.pi))) == 0)

# (e) periodic BC on T: e^{inx} orthogonal; Gram = 2 pi delta
ok('e1 periodic: int_0^{2pi} e^{i2x} e^{-i3x} = 0', sp.integrate(sp.exp(2*sp.I*x)*sp.exp(-3*sp.I*x), (x, 0, 2*sp.pi)) == 0)

# (f) coordinates (C2.56): radial Laplacian u''+u'/r ; J0(kr) solves Helmholtz Delta u + k^2 u=0
J0 = sp.besselj(0, k*r)
ok('f1 (d_rr + (1/r) d_r + k^2) J0(kr) = 0', sp.simplify(sp.diff(J0, r, 2) + sp.diff(J0, r)/r + k**2*J0) == 0)
# Liouville transform: u = r^{-1/2} w  turns Bessel(0) into w'' + (k^2 + 1/(4 r^2)) w = 0 (SL normal form)
w = sp.Function('w')
u = w(r)/sp.sqrt(r)
expr = sp.simplify(sp.sqrt(r)*(sp.diff(u, r, 2) + sp.diff(u, r)/r + k**2*u))
ok('f2 Liouville normal form of radial Bessel', sp.simplify(expr - (sp.diff(w(r), r, 2) + (k**2 + 1/(4*r**2))*w(r))) == 0)

# (g) variational (C2.51): Rayleigh quotient of trial x(pi-x) for -u'' Dirichlet >= lam_1 = 1
tr = x*(sp.pi-x)
R = sp.integrate(sp.diff(tr, x)**2, (x, 0, sp.pi))/sp.integrate(tr**2, (x, 0, sp.pi))
ok('g1 Rayleigh quotient 10/pi^2 >= lambda_1=1', sp.simplify(R - 10/sp.pi**2) == 0 and R.evalf() >= 1)

print('ALL PASS' if all(c for _, c in res) else 'SOME FAIL')
