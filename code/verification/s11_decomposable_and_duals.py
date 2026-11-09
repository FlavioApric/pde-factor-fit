# R3 SymPy check s11 -- (A) sottospazio decomponibile S = ker L ∩ (ker L1 + ker L2') per avvezione-diffusione;
#                         (B) sistema duale di Rosenbloom-Widder (polinomi del calore v_n / funzioni associate w_n).
exec(open(r'D:\ProblemaBase\research\R3\sympy\_hdr.py', encoding='utf8').read())
t, x, c, Dd = symbols('t x c D', positive=True)
s = x - c*t
L1 = lambda u: diff(u, t) + c*diff(u, x)
L2p = lambda u: -Dd*diff(u, x, 2)
L = lambda u: L1(u) + L2p(u)
basis = [(sp.Integer(1), sp.Integer(0)), (s, sp.Integer(0)), (s**2, 2*Dd*t), (s**3, 6*Dd*t*s)]   # (a, b)
for i, (a, b) in enumerate(basis):
    check(f'S basis {i}: L1 a = 0', L1(a)); check(f"S basis {i}: L2' b = 0", L2p(b)); check(f'S basis {i}: L(a+b) = 0', L(a + b))
# lunghezza di R/(P1+P2', P1 P2') = dim S  (Groebner, ordine lex tau > xi)
tau, xi = symbols('tau xi')
P1, P2 = tau + c*xi, -Dd*xi**2
Gb = sp.groebner([P1 + P2, P1*P2], tau, xi, order='lex')
print('Groebner basis of (P1+P2, P1*P2):', Gb.exprs)
check('ideal (P1+P2, P1P2) contains xi^4 (=> length 4 = dim S)', Gb.reduce(xi**4)[1])
check('xi^3 NOT in ideal (remainder nonzero => length exactly 4)', 0 if Gb.reduce(xi**3)[1] != 0 else 1)
# (B) Rosenbloom-Widder: u_t = u_xx ; v_n heat polynomials ; w_n(x,t) = k(x,t) v_n(x/t, -1/t)
xx = symbols('xx', real=True)
k = lambda X, T: exp(-X**2/(4*T))/sqrt(4*pi*T)
def v(n, X, T):
    return sum(sp.factorial(n)/(sp.factorial(j)*sp.factorial(n-2*j))*X**(n-2*j)*T**j for j in range(n//2+1))
w = lambda n, X, T: k(X, T)*v(n, X/T, -1/T)
for n in (0, 1, 3):
    W = w(n, xx, t)
    check(f'associated function w_{n} solves heat', diff(W, t) - diff(W, xx, 2), (t, xx))
M = sp.Matrix(4, 4, lambda n, m: sp.simplify(integrate(sp.expand(v(n, xx, -t)*w(m, xx, t)), (xx, -oo, oo))))
print('Gram <v_n(.,-t), w_m(.,t)>, n,m=0..3:'); sp.pprint(M)
check('biorthogonality: off-diagonal entries vanish', sum(abs(M[i, j]) for i in range(4) for j in range(4) if i != j))
summary()
