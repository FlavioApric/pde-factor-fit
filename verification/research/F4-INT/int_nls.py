# F4-INT — verifiche NLS focusing i q_t + q_xx + 2|q|^2 q = 0 (controllo, non metodo; vincolo k3)
# Classe H_M (coefficienti REALI): q_t = d0 T0 + d1 T1 + d2 T2 + d3 T3, con
#   T0 = i q (fase, Omega ~ 1), T1 = q_x (traslazione, ~ zeta), T2 = i(q_xx + 2|q|^2 q) (NLS, ~ zeta^2),
#   T3 = -(q_xxx + 6|q|^2 q_x) (mKdV complessa, ~ zeta^3).
# Predizione (INT-T2): ambiguita' = max(0, M+1 - |Lambda U conj(Lambda)|), Lambda = autovalori discreti (+ supporto reale di rho).
#   1-solitone: 2 punti {zeta, conj zeta}: ambiguita' 1 in H_2, 2 in H_3.
#   breather di Satsuma-Yajima (zeta = i/2, 3i/2): 4 punti: ambiguita' 0 in H_2 e in H_3.
# Metodo di controllo: valutazione a 40 cifre in punti casuali, rango numerico via valori singolari.
import sympy as sp, mpmath as mp, random
mp.mp.dps = 40; random.seed(3)
x, t = sp.symbols('x t', real=True); I = sp.I
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(("OK  " if cond else "FAIL"), name)

def terms(q):
    qc = sp.conjugate(q)
    qx = sp.diff(q, x); qxx = sp.diff(qx, x); qxxx = sp.diff(qxx, x); qt = sp.diff(q, t)
    ab2 = q*qc
    return dict(qt=qt, T0=I*q, T1=qx, T2=I*(qxx + 2*ab2*q), T3=-(qxxx + 6*ab2*qx),
                NLSres=I*qt + qxx + 2*ab2*q)

def sing_vals(q, names, npts=16):
    T = terms(q)
    fs = {k: sp.lambdify((x, t), T[k], 'mpmath') for k in names}
    rows = []
    for _ in range(npts):
        X = mp.mpf(random.uniform(-2, 2)); Tt = mp.mpf(random.uniform(-1, 1))
        vals = [mp.mpc(fs[k](X, Tt)) for k in names]
        rows.append([v.real for v in vals]); rows.append([v.imag for v in vals])
    M = mp.matrix(rows)
    S = mp.svd_r(M, compute_uv=False)
    return sorted([float(s) for s in S])

def residual(q, npts=8):
    f = sp.lambdify((x, t), terms(q)['NLSres'], 'mpmath')
    return max(abs(mp.mpc(f(mp.mpf(random.uniform(-2, 2)), mp.mpf(random.uniform(-1, 1))))) for _ in range(npts))

def ndim(sv, tol=1e-25):
    return sum(1 for s in sv if s < tol)

# 1-solitone fermo e in moto: q = 2 eta sech(2 eta (x + 4 xi t)) exp(-2 i xi x - 4 i (xi^2 - eta^2) t)
for (eta, xi) in [(sp.Rational(1, 2), 0), (sp.Rational(1, 2), sp.Rational(1, 3))]:
    q = 2*eta*sp.sech(2*eta*(x + 4*xi*t))*sp.exp(-2*I*xi*x - 4*I*(xi**2 - eta**2)*t)
    check(f"1-sol (eta,xi)=({eta},{xi}): residuo NLS < 1e-30", residual(q) < 1e-30)
    sv = sing_vals(q, ['qt', 'T0', 'T1', 'T2']); d = ndim(sv)
    check(f"1-sol ({eta},{xi}): dim relazioni reali span{{q_t,T0,T1,T2}} = 2 (ambiguita' H_2 = 1); trovato {d}; sv={['%.1e' % s for s in sv]}", d == 2)
    sv = sing_vals(q, ['qt', 'T0', 'T1', 'T2', 'T3']); d = ndim(sv)
    check(f"1-sol ({eta},{xi}): dim relazioni reali span{{q_t,T0..T3}} = 3 (ambiguita' H_3 = 2); trovato {d}", d == 3)

# breather di Satsuma-Yajima (q(x,0) = 2 sech x): autovalori zeta = i/2, 3i/2
q = 4*sp.exp(I*t)*(sp.cosh(3*x) + 3*sp.exp(8*I*t)*sp.cosh(x))/(sp.cosh(4*x) + 4*sp.cosh(2*x) + 3*sp.cos(8*t))
check("breather: residuo NLS < 1e-30", residual(q) < 1e-30)
sv = sing_vals(q, ['qt', 'T0', 'T1', 'T2']); d = ndim(sv)
check(f"breather: dim relazioni reali span{{q_t,T0,T1,T2}} = 1 (identifica in H_2); trovato {d}; sv min={sv[0]:.1e}, 2o={sv[1]:.1e}", d == 1)
sv = sing_vals(q, ['qt', 'T0', 'T1', 'T2', 'T3']); d = ndim(sv)
check(f"breather: dim relazioni reali span{{q_t,T0..T3}} = 1 (identifica in H_3); trovato {d}; 2o sv={sv[1]:.1e}", d == 1)
print(f"\nTOTALE: {sum(OK)}/{len(OK)} OK")
