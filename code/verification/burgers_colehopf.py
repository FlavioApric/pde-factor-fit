"""PR-C2c / scheda C2.15 (Burgers, Cole-Hopf) -- verifiche SymPy.
Esecuzione: D:\\ProblemaBase\\.venv\\Scripts\\python.exe -I burgers_colehopf.py
Burgers viscoso: u_t + u u_x - nu u_xx = 0  (V*V_x degli appunti A6).
"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
nu = sp.symbols('nu', positive=True)
phi = sp.Function('phi')(x, t)

def burgers(u):
    return sp.diff(u, t) + u*sp.diff(u, x) - nu*sp.diff(u, x, 2)

# [B1] Identita' di Cole-Hopf: u = -2 nu phi_x/phi  =>  B[u] = -2 nu d_x( H[phi]/phi ),  H = d_t - nu d_xx
u = -2*nu*sp.diff(phi, x)/phi
H = sp.diff(phi, t) - nu*sp.diff(phi, x, 2)
idB1 = sp.simplify(burgers(u) - (-2*nu*sp.diff(H/phi, x)))
print('[B1] B[-2nu phi_x/phi] + 2nu d_x(H[phi]/phi) =', idB1)

# [B2] N-"modi" esponenziali: phi = sum_j a_j exp(k_j x + nu k_j^2 t) e' nel nucleo del calore (lineare!)
k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
a1, a2 = sp.symbols('a1 a2', positive=True)
def mode(k, a):
    return a*sp.exp(k*x + nu*k**2*t)
phi2 = 1 + mode(k1, a1) + mode(k2, a2)
print('[B2a] H[phi2] =', sp.simplify(sp.diff(phi2, t) - nu*sp.diff(phi2, x, 2)))
u2 = -2*nu*sp.diff(phi2, x)/phi2
print('[B2b] B[u2] =', sp.simplify(burgers(u2)))

# [B3] onda viaggiante (fronte d'urto viscoso): u = c - A tanh(A (x - c t)/(2 nu))
c, A = sp.symbols('c A', real=True)
utw = c - A*sp.tanh(A*(x - c*t)/(2*nu))
print('[B3] B[u_tw] =', sp.simplify(burgers(utw)))
# corrisponde a phi = exp(...)*(1 + exp(...)), cioe' 2 modi del calore
phitw = sp.exp(-(c - A)/(2*nu)*x + ((c - A)**2/(4*nu))*t) * (1 + sp.exp(-A*(x - c*t)/nu))
print('[B3b] u_tw == -2nu phi_x/phi per phi = somma di 2 esponenziali-calore:',
      sp.simplify((-2*nu*sp.diff(phitw, x)/phitw - utw).rewrite(sp.exp)))
print('       H[phitw] =', sp.simplify(sp.diff(phitw, t) - nu*sp.diff(phitw, x, 2)))

# [B4] E_int in coordinate u: u per phi=1+e1+e2 NON e' somma dei fronti singoli
u_1 = -2*nu*sp.diff(1 + mode(k1, a1), x)/(1 + mode(k1, a1))
u_2 = -2*nu*sp.diff(1 + mode(k2, a2), x)/(1 + mode(k2, a2))
Eint = sp.simplify(u2 - u_1 - u_2)
print('[B4] E_int = u(phi1+phi2-1) - u(phi1) - u(phi2) =', sp.factor(Eint))
# in coordinate phi: phi = phi_1 + phi_2 - 1  (E_int = 0 esatto, il "-1" e' il modo k=0 condiviso)

# [B5] Sovrapposizione non lineare: u = -2nu d_x log(phi_1 + phi_2) -- regola di composizione "log-sum-exp"
print('[B5] limite nu->0 (Hopf-Lax): -2nu log(sum_j exp(-S_j/(2nu))) -> min_j S_j  (verifica numerica)')
S1, S2 = sp.Rational(3, 10), sp.Rational(7, 10)
for nv in [sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]:
    val = -2*nv*sp.log(sp.exp(-S1/(2*nv)) + sp.exp(-S2/(2*nv)))
    print('     nu =', nv, ' -> ', sp.N(val, 12), ' (min =', sp.N(min(S1, S2)), ')')

# [B6] identificazione lineare nei coefficienti: dizionario {u_t, u u_x, u_xx}; lambda=(1,1,-nu) annulla
k1v, k2v, a1v, a2v, nuv = 1, -sp.Rational(1, 2), 1, 2, sp.Rational(3, 10)
uu = u2.subs({k1: k1v, k2: k2v, a1: a1v, a2: a2v, nu: nuv})
feat = [sp.diff(uu, t), uu*sp.diff(uu, x), sp.diff(uu, x, 2), sp.diff(uu, x)]
import random
random.seed(1)
pts = [(sp.Rational(random.randint(-20, 20), 10), sp.Rational(random.randint(0, 20), 10)) for _ in range(12)]
M = sp.Matrix([[sp.N(f.subs({x: px, t: pt}), 30) for f in feat] for (px, pt) in pts])
G = (M.T*M)
ev = sorted([abs(sp.N(e, 15)) for e in G.eigenvals(multiple=True)])
print('[B6] autovalori Gram jet 4x4 {u_t,uu_x,u_xx,u_x} (atteso: uno ~0):', [sp.N(e, 4) for e in ev])
ns = M.nullspace(simplify=False) if False else None
vec = sp.Matrix([1, 1, -nuv, 0])
print('     residuo max |M (1,1,-nu,0)| =', max(abs(sp.N(r, 15)) for r in (M*vec)))
