# F6-CONV: verifica (V-ex) di CONV-T4: sin(theta) <= 2*delta/rho, e ordine 1/rho ottimale (esempio 2x2);
# e del passo di Weyl usato in CONV-T5: |sigma_1(A+E) - sigma_1(A)| <= ||E||.
import numpy as np, sympy as sp
rng = np.random.default_rng(0)
worst = 0.0; weyl_ok = True
for trial in range(20000):
    M = rng.integers(2, 7); R = M + rng.integers(0, 6)
    U, _ = np.linalg.qr(rng.normal(size=(R, R))); V, _ = np.linalg.qr(rng.normal(size=(M, M)))
    sv = np.sort(rng.uniform(0.05, 3, size=M)); sv[0] = 0.0
    S = np.zeros((R, M)); S[:M, :M] = np.diag(sv)
    A = U @ S @ V.T; lam = V[:, 0]; rho = sv[1]
    E = rng.normal(size=(R, M)); E *= rng.uniform(1e-4, 0.5) / np.linalg.norm(E, 2); d = np.linalg.norm(E, 2)
    _, s2, Vt = np.linalg.svd(A + E); lt = Vt[-1]
    sin = np.sqrt(max(0.0, 1 - (lt @ lam) ** 2))
    worst = max(worst, sin / (2 * d / rho))
    if abs(s2[-1] - 0.0) > d + 1e-12: weyl_ok = False
print('rapporto massimo sin(theta)/(2 delta/rho) su 20000 prove:', round(worst, 4), '(<= 1 atteso)')
print('Weyl |sigma_1(A+E)-sigma_1(A)| <= ||E||:', weyl_ok)
r, dl = sp.symbols('rho delta', positive=True)
At = sp.Matrix([[0, 0], [dl, r]])
k = At.nullspace()[0]; k = k / sp.sqrt(k.dot(k))
print('esempio 2x2: A=diag(0,rho), E=[[0,0],[delta,0]], ||E||=delta; sin(theta) =', sp.simplify(sp.sqrt(1 - k[0] ** 2)),
      '~ delta/rho  (ordine ottimale, costante entro il fattore 2)')
