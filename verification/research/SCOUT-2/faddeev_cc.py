# Controllo (non metodo, k3): componenti di Faddeev/Lippmann-Schwinger per coefficienti costanti.
# L = L0 + V1 + V2 con L0 = d_t, V1 = c d_x, V2 = -D d_xx  (trasporto + diffusione).
# Su u = sum_m c_m exp(tau_m t + xi_m x), P(tau_m,xi_m)=0, la componente u_i := -G0 V_i u
# agisce come moltiplicatore w_i(tau,xi) = -v_i/p0 sulla varieta' caratteristica; sum_i w_i = 1 su V(P).
import sympy as sp
t,x,c,D = sp.symbols('t x c D', positive=True)
xi1,xi2 = sp.symbols('xi1 xi2')
a1,a2 = sp.symbols('a1 a2')
def tau(xi): return D*xi**2 - c*xi          # P = tau + c xi - D xi^2 = 0
modes = [(a1,xi1),(a2,xi2)]
u = sum(a*sp.exp(tau(k)*t + k*x) for a,k in modes)
L = lambda f: sp.diff(f,t) + c*sp.diff(f,x) - D*sp.diff(f,x,2)
print("L u =", sp.simplify(L(u)))
# G0 = (d_t)^{-1} on exponentials with tau != 0: exp(tau t + xi x) -> exp(...)/tau
def G0V(f_coeffs, vsym):
    return sum(a*(-vsym(k))/tau(k)*sp.exp(tau(k)*t+k*x) for a,k in f_coeffs)
u1 = G0V(modes, lambda k: c*k)          # componente "trasporto"
u2 = G0V(modes, lambda k: -D*k**2)      # componente "diffusione"
print("u1+u2-u =", sp.simplify(u1+u2-u))
# equazioni accoppiate di Faddeev: (L0+V_i) u_i = -V_i u_j  (j != i)
V1 = lambda f: c*sp.diff(f,x); V2 = lambda f: -D*sp.diff(f,x,2); L0 = lambda f: sp.diff(f,t)
print("Faddeev eq 1:", sp.simplify(L0(u1)+V1(u1)+V1(u2)))
print("Faddeev eq 2:", sp.simplify(L0(u2)+V2(u2)+V2(u1)))
print("w1(xi) =", sp.simplify(-c*xi1/tau(xi1)), " w2(xi) =", sp.simplify(D*xi1**2/tau(xi1)))
