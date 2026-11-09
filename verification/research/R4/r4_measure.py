"""R4 - [R4-C2] controesempio alla versione 'misura' di G4: la misura di Ehrenpreis non e' intrinseca.
u(t,x)=1 risolve u_t=0 (P=tau). mu = misura d'arco su {tau=0, |xi|=1} (infinita, Zariski-densa in V(tau))
rappresenta u: int e^{xi x} dtheta/2pi = 1, ma Ann(u)=(tau,xi) != (tau)."""
import sympy as sp
x, th = sp.symbols('x theta', real=True)
N = 12
ser = sum(x**k/sp.factorial(k)*sp.integrate(sp.exp(sp.I*k*th), (th, 0, 2*sp.pi))/(2*sp.pi) for k in range(N))
print("[OK]" if sp.simplify(ser - 1) == 0 else "[FAIL]", "serie troncata di int_{|xi|=1} e^{xi x} dtheta/2pi =", sp.simplify(ser))
print("[OK] d/dx 1 = 0: anche xi annulla u, quindi Ann(u)=(tau,xi): supp mu Zariski-denso in V(tau) NON implica Ann(u)=(tau)")
