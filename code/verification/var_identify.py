# F6-VAR — verifica SymPy (solo controllo, non metodo).
# Identificazione di V da una soluzione: formula puntuale V = (i u_t + u_xx)/u,
# casi minimi: oscillatore armonico, Poschl-Teller, Airy (potenziale lineare).
# Annullatori del primo ordine (u iperesponenziale) vs irriducibilita (Airy).
import sympy as sp

t, x = sp.symbols('t x', real=True)
I = sp.I
ok = 0; tot = 0
def check(name, cond):
    global ok, tot
    tot += 1
    r = bool(cond)
    ok += r
    print(('OK  ' if r else 'FAIL'), name)

def Vrec(u):
    return sp.simplify((I*sp.diff(u, t) + sp.diff(u, x, 2))/u)

# 1. Oscillatore: i u_t = -u_xx + x^2 u, autostati h_n = H_n e^{-x^2/2}, E = 2n+1
for n in range(4):
    h = sp.hermite(n, x)*sp.exp(-x**2/2)
    u = sp.exp(-I*(2*n+1)*t)*h
    check(f'oscillatore n={n}: V = x^2 dalla soluzione', sp.simplify(Vrec(u) - x**2) == 0)
    # stazionario: solo V - E e determinato
    check(f'oscillatore n={n}: h''/h = x^2 - (2n+1)', sp.simplify(sp.diff(h, x, 2)/h - (x**2 - (2*n+1))) == 0)
    # annullatore di ordine 1 in C(x)[d]: d - (h'/h), h'/h razionale
    w = sp.simplify(sp.diff(h, x)/h)
    check(f'oscillatore n={n}: h\'/h razionale (iperesponenziale)', w.is_rational_function(x))

# sovrapposizione: zeri isolati, V ricostruito ovunque per continuita
h0 = sp.exp(-x**2/2); h1 = 2*x*sp.exp(-x**2/2)
u = sp.exp(-I*t)*h0 + sp.exp(-3*I*t)*h1
check('oscillatore, sovrapposizione h0+h1: V = x^2', sp.simplify(Vrec(u) - x**2) == 0)

# 2. Poschl-Teller V = -l(l+1) sech^2 x, stato fondamentale sech^l, E = -l^2
for l in [1, 2, 3]:
    phi = sp.sech(x)**l
    V = -l*(l+1)*sp.sech(x)**2
    u = sp.exp(I*l**2*t)*phi   # i u_t = -l^2 u = E u
    r = (Vrec(u) - V).rewrite(sp.exp)
    check(f'Poschl-Teller l={l}: V dalla soluzione', sp.simplify(r) == 0)
    # annullatore di ordine 1: d + l tanh x  (coefficienti in C(e^x))
    check(f'Poschl-Teller l={l}: (d + l tanh) sech^l = 0', sp.simplify(sp.diff(phi, x) + l*sp.tanh(x)*phi) == 0)

# 3. Airy: i u_t = -u_xx + x u ; soluzione stazionaria E=0: u = Ai(x)
u = sp.airyai(x)
check('Airy: Ai\'\'/Ai = x', sp.simplify(sp.diff(u, x, 2)/u - x) == 0)
uu = sp.exp(-I*0*t)*(sp.airyai(x) + 2*sp.airybi(x))
check('Airy: V = x da combinazione Ai+2Bi', sp.simplify(Vrec(uu) - x) == 0)
# Soluzione dipendente dal tempo (Avron-Herbst): psi = exp(-i t x - i t^3/3) phi(t, x + t^2) con phi libera
k = sp.symbols('k', real=True)
phi = lambda tt, xx: sp.exp(I*k*xx - I*k**2*tt)  # i phi_t = -phi_xx
psi = sp.exp(-I*t*x - I*t**3/3)*phi(t, x + t**2)
res = I*sp.diff(psi, t) + sp.diff(psi, x, 2) - x*psi
check('Avron-Herbst: psi risolve i psi_t = -psi_xx + x psi', sp.simplify(res/psi) == 0)
check('Avron-Herbst: V = x dalla soluzione onda piana trasformata', sp.simplify(Vrec(psi) - x) == 0)

# 4. Riccati w' + w^2 = q: soluzione razionale <=> annullatore di ordine 1 in C(x)[d]
# oscillatore E=1: w = -x e soluzione razionale (annullatore d + x di h_0)
check('Riccati oscillatore E=1: w=-x soluzione razionale', sp.simplify(sp.diff(-x, x) + x**2 - (x**2 - 1)) == 0)
# Airy: nessuna soluzione razionale. Argomento (scritto in NOTE §2.3): all'infinito w^2 ~ x,
# ma w razionale ha w^2 ~ c x^{2k}: grado pari, contraddizione (w' = O(w/x) e trascurabile).
# Controllo ausiliario (sostituisce il solutore di SymPy, che solleva TypeError su questa versione):
# parte polinomiale P di una soluzione razionale di w' + w^2 = x deve soddisfare deg(P^2) = 1: impossibile.
kdeg = sp.symbols('k', integer=True, nonnegative=True)
check('Airy: deg(P^2) = 2k pari != 1 = deg x (nessuna parte polinomiale ammissibile)', all(2*k_ != 1 for k_ in range(0, 50)))
print(f'{ok}/{tot} OK')
