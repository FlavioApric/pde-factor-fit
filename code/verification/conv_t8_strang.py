# S-CHECK-F8-CONV: controllo indipendente di CONV-T8 (splitting Lie/Strang con Dirichlet + trasporto, primo ordine in eps)
# (1) forma chiusa (a) contro somma diretta dei prodotti modali (matrici troncate, potenze esplicite)
# (2) pendenze log-log in L2 di G^Lie e G^Str per u0 = e1
# (3) minorante esplicito di (c) e maggiorante con la costante corretta in (d)
# (4) [V-ex] pendenza in L^inf vicino a x = 0
import mpmath as mp
import sympy as sp
mp.mp.dps = 30
OK = []
def check(name, cond):
    OK.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

L = c = D = T = mp.mpf(1)
kap = D*mp.pi**2/L**2
lam = lambda n: -kap*n*n
def V(m, n):
    return mp.mpf(0) if (m+n) % 2 == 0 else -4*c*m*n/(L*(m*m-n*n))

# (0) identita' simboliche: b/(a-b) = 1/(e^x-1), (a+b)/(a-b) = coth(x/2)
x = sp.symbols('x', positive=True)
a, b = sp.exp(x), sp.Integer(1)
check("b/(a-b)=1/(e^x-1)", sp.simplify(b/(a-b) - 1/(sp.exp(x)-1)) == 0)
check("(a+b)/(a-b)=coth(x/2)", sp.simplify(((a+b)/(a-b) - sp.coth(x/2)).rewrite(sp.exp)) == 0)
# V_mn dall'integrale
m_, n_ = 2, 1
xx = sp.symbols('xx')
Vsym = sp.integrate(sp.sqrt(2)*sp.sin(m_*sp.pi*xx)*(-1)*sp.diff(sp.sqrt(2)*sp.sin(n_*sp.pi*xx), xx), (xx, 0, 1))
check("V_21 = -4c*2*1/(L*3)", sp.simplify(Vsym - sp.Rational(-8, 3)) == 0)

phiL = lambda y: 1/y - 1/(mp.e**y - 1)
phiS = lambda y: 1/y - mp.coth(y/2)/2

# (1) somma diretta per u0 = e1, modo m, contro forma chiusa
def direct(m, h, nu, strang):
    am, a1 = mp.e**(lam(m)*h), mp.e**(lam(1)*h)
    S1 = V(m, 1)*(mp.e**(lam(1)*T) - mp.e**(lam(m)*T))/(lam(1)-lam(m))
    s = mp.mpf(0)
    for k in range(nu):
        if strang:
            s += am**(nu-k-1)*(h/2)*(V(m, 1)*a1 + am*V(m, 1))*a1**k
        else:
            s += am**(nu-k)*h*V(m, 1)*a1**k
    return S1 - s
def closed(m, h, strang):
    xm = (lam(1)-lam(m))*h
    f = phiS(xm) if strang else phiL(xm)
    return V(m, 1)*(mp.e**(lam(1)*T) - mp.e**(lam(m)*T))*h*f
err = 0
for nu in (4, 16):
    h = T/nu
    for m in (2, 4, 6, 10):
        for st in (False, True):
            err = max(err, abs(direct(m, h, nu, st) - closed(m, h, st)))
check("forma chiusa (a) = somma diretta (err %.1e)" % float(err), err < mp.mpf(10)**-20)

# (2) norme L2 per u0 = e1 (somma sui modi pari, troncata a M grande con coda trascurabile)
def normG(h, strang, Mmax=None):
    Mmax = Mmax or int(60/mp.sqrt(h)) + 200
    s = mp.mpf(0)
    for m in range(2, Mmax, 2):
        s += closed(m, h, strang)**2
    return mp.sqrt(s)
hs = [mp.mpf(4)**-k for k in range(3, 8)]
GS = [normG(h, True) for h in hs]; GL = [normG(h, False) for h in hs]
slS = [mp.log(GS[i]/GS[i+1])/mp.log(4) for i in range(len(hs)-1)]
slL = [mp.log(GL[i]/GL[i+1])/mp.log(4) for i in range(len(hs)-1)]
print("pendenze Strang:", [mp.nstr(v, 6) for v in slS])
print("pendenze Lie   :", [mp.nstr(v, 6) for v in slL])
check("Strang pendenza -> 5/4 (|ultima-1.25|<3e-3)", abs(slS[-1]-mp.mpf(1.25)) < 3e-3)
check("Lie pendenza -> 1 (|ultima-1|<3e-2)", abs(slL[-1]-1) < 3e-2)
# rapporto G^Str / h^{5/4} stabile
rat = [GS[i]/hs[i]**mp.mpf(1.25) for i in range(len(hs))]
print("G^Str/h^(5/4):", [mp.nstr(v, 6) for v in rat])

# (3) minorante di (c): ||G^Str|| >= |c| e^{lam1 T} phi* kappa^{1/4} h^{5/4}/(sqrt5 L), h <= 1/(36 kappa)
phistar = abs(phiS(1))
check("phi* = (coth(1/2)-2)/2 = 0.08198", abs(phistar - (mp.coth(0.5)-2)/2) < 1e-25 and abs(phistar-0.08198) < 1e-5)
okmin = True
for nu in (400, 1000, 3000):
    h = T/nu
    if h > 1/(36*kap): continue
    lb = abs(c)*mp.e**(lam(1)*T)*phistar*kap**0.25*h**1.25/(mp.sqrt(5)*L)
    g = normG(h, True)
    print("h=%s  ||G^Str||=%s  minorante=%s" % (mp.nstr(h, 4), mp.nstr(g, 6), mp.nstr(lb, 6)))
    okmin &= g >= lb
check("minorante (c) rispettato", okmin)
# conteggio pari nella finestra >= 1/(4 sqrt(kappa h))
okc = True
for kh in [mp.mpf(1)/36, mp.mpf(1)/50, mp.mpf(1)/200, mp.mpf(1)/1000, mp.mpf(1)/10**5]:
    lo, hi = mp.sqrt(1/kh+1), mp.sqrt(4/kh+1)
    cnt = len([m for m in range(int(lo), int(hi)+2) if m % 2 == 0 and lo <= m <= hi])
    okc &= cnt >= 1/(4*mp.sqrt(kh))
check("#pari in W_h >= 1/(4 sqrt(kappa h)) per kappa h <= 1/36", okc)
# monotonia di |phi_S| e bound |phi_S| <= min(x/12, 1/2)
xs = [mp.mpf(k)/10 for k in range(1, 400)]
check("|phi_S| crescente", all(abs(phiS(xs[i])) < abs(phiS(xs[i+1])) for i in range(len(xs)-1)))
check("|phi_S(x)| <= min(x/12,1/2)", all(abs(phiS(t)) <= min(t/12, mp.mpf(1)/2) for t in xs))

# (d) costante: |V_m1| <= 8|c|/(3Lm) dichiarato; il bound corretto e' 16|c|/(3Lm)
m = 4
v = abs(V(m, 1)); claimed = 8*abs(c)/(3*L*m); correct = 16*abs(c)/(3*L*m)
print("m=4: |V_41|=%s, 8/(3Lm)=%s, 16/(3Lm)=%s" % (mp.nstr(v, 6), mp.nstr(claimed, 6), mp.nstr(correct, 6)))
check("(d): il bound 8|c|/(3Lm) e' FALSO per m=4 (fix CONV-5)", v > claimed)
check("(d): il bound 16|c|/(3Lm) vale per m pari >= 2", all(abs(V(mm, 1)) <= 16*abs(c)/(3*L*mm) for mm in range(2, 400, 2)))
# difetto locale di Strang: pendenza 5/4
def ES(h):
    s = mp.mpf(0)
    for m in range(2, int(60/mp.sqrt(h))+200, 2):
        xm = (lam(1)-lam(m))*h
        s += (V(m, 1)*(mp.e**(lam(1)*h)-mp.e**(lam(m)*h))*h*phiS(xm))**2
    return mp.sqrt(s)
E = [ES(h) for h in hs]
slE = [mp.log(E[i]/E[i+1])/mp.log(4) for i in range(len(hs)-1)]
print("pendenze difetto locale Strang:", [mp.nstr(v, 6) for v in slE])
check("difetto locale Strang -> 5/4", abs(slE[-1]-mp.mpf(1.25)) < 5e-3)

# (4) [V-ex] L^inf vicino a 0: max su griglia x in (0, 0.05]
def Ginf(h):
    Mx = int(60/mp.sqrt(h)) + 200
    coef = [(m, closed(m, h, True)) for m in range(2, Mx, 2)]
    best = mp.mpf(0)
    for j in range(1, 401):
        xg = mp.mpf(j)/8000
        val = sum(cm*mp.sqrt(2)*mp.sin(m*mp.pi*xg) for m, cm in coef)
        best = max(best, abs(val))
    return best
mp.mp.dps = 20
GI = [Ginf(h) for h in hs[:4]]
slI = [mp.log(GI[i]/GI[i+1])/mp.log(4) for i in range(len(GI)-1)]
print("[V-ex] pendenze L^inf (x<=0.05):", [mp.nstr(v, 5) for v in slI])
check("[V-ex] L^inf Strang pendenza ~1 (|ultima-1|<0.1)", abs(slI[-1]-1) < 0.1)

print("TUTTI PASS" if all(OK) else "ALCUNI FAIL", "(%d/%d)" % (sum(OK), len(OK)))
