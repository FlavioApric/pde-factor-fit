# S10-OPEN-A, P2-Q1 su domini non convessi: Laplaciano sull'anello (solo verifica).
import sympy as sp
import mpmath as mp

ok = 0; tot = 0
def chk(name, cond):
    global ok, tot
    tot += 1; ok += bool(cond)
    print(("OK  " if cond else "FAIL"), name)

r, th = sp.symbols('r theta', positive=True)
rho = sp.Rational(3, 2)
z = r*sp.exp(sp.I*th)
def flux(h):   # Phi(h) = int_{|z| = rho} d_r h * rho dtheta
    return sp.simplify(sp.integrate((sp.diff(h, r)*r).subs(r, rho), (th, 0, 2*sp.pi)))
# (1) log|z| armonica, flusso 2 pi
L = sp.log(r)
chk("log r armonica", sp.simplify(sp.diff(L, r, 2) + sp.diff(L, r)/r) == 0)
chk("Phi(log r) = 2 pi", sp.simplify(flux(L) - 2*sp.pi) == 0)
# (2) flusso nullo su z^n e conj(z)^n, n = -5..5 (olomorfe e antiolomorfe monodrome sull'anello)
allzero = True
for n in range(-5, 6):
    allzero &= flux(sp.expand(z**n)) == 0
    allzero &= flux(sp.expand((r*sp.exp(-sp.I*th))**n)) == 0
chk("Phi = 0 su z^n e conj(z)^n, |n| <= 5", allzero)
# (3) identita *df = -i f' dz: Phi(f) = -i oint f'(z) dz
w = sp.symbols('w')
good = True
for n in (-3, -1, 2, 4):
    lhs = flux(sp.expand(z**n))
    zz = rho*sp.exp(sp.I*th)
    rhs = -sp.I*sp.integrate((n*zz**(n-1))*sp.I*zz, (th, 0, 2*sp.pi))
    good &= sp.simplify(lhs - rhs) == 0
chk("Phi(f) = -i oint f' dz per f = z^n", good)
# (4) ostruzione: d_z log|z| = 1/(2z) ha residuo 1/2 != 0
chk("Res_{z=0} 1/(2z) = 1/2", sp.residue(1/(2*w), w, 0) == sp.Rational(1, 2))
# (5) Phi(log r)/||log r||_{L2(1<r<2)}: numero finito > 0 (il funzionale separa log r dalla chiusura)
mp.mp.dps = 20
nrm = mp.sqrt(mp.quad(lambda rr: mp.log(rr)**2*rr, [1, 2])*2*mp.pi)
print("   ||log r||_L2 =", mp.nstr(nrm, 8), "  Phi/||.|| =", mp.nstr(2*mp.pi/nrm, 8))
chk("||log r||_L2 > 0 finito", 0 < nrm < 10)
# (6) stima interna (valore medio sul gradiente): |grad h(z)| <= (2/(pi d^3))^{1/2} ... controllo: per h = r^n cos(n th)
#     |Phi(h)| = 0 e sup_{r=rho}|d_r h| <= C ||h||_L2 con C indipendente da n (campione n = 1..8)
cs = []
for n in range(1, 9):
    for sgn in (1, -1):
        hn = lambda rr, tt, n=n, sgn=sgn: rr**(sgn*n)*mp.cos(n*tt)
        L2 = mp.sqrt(mp.quad(lambda rr, tt: hn(rr, tt)**2*rr, [1, 2], [0, 2*mp.pi]))
        gr = abs(sgn*n*rho**(sgn*n-1))
        cs.append(gr/L2)
print("   sup|d_r h|/||h||_L2 su r=3/2, n=1..8:", mp.nstr(max(cs), 6))
chk("stima interna uniforme sul campione (rapporto limitato)", max(cs) < 20)
print(f"{ok}/{tot} OK")
