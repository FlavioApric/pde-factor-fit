# S4-ID — verifica (non metodo) della riduzione psi (forma normale ALG-L1) e di [F] ∩ V.
# psi: theta y = d_t^a d_x^b y  |->  D_N^a D^b y_0  in A = Q[y_0..y_M].
# ker(psi|_V) = [F] ∩ V (ALG-L1(ii)). Si calcola dim ker psi|_V per:
#   V_{d,k} = monomi di grado <= d nei theta y con |theta| <= k (costante inclusa);
#   H_{D,k} = span{ theta(y^j) : |theta| <= k, 1 <= j <= D }  (dizionario di Hammerstein).
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
from itertools import combinations_with_replacement

def make_eq(name, nu=sp.Rational(1), kk=6):
    M = 40
    y = sp.symbols('y0:%d' % M)
    if name == 'burgers':      # y_t = -y0 y1 + nu y2
        N = -y[0]*y[1] + nu*y[2]; n = 2
    elif name == 'kdv':        # y_t = -6 y0 y1 - y3
        N = -6*y[0]*y[1] - y[3]; n = 3
    elif name == 'fisher':     # y_t = y2 + y0 - y0^2
        N = y[2] + y[0] - y[0]**2; n = 2
    elif name == 'kdvb':       # y_t = -y0 y1 + nu y2 - y3
        N = -y[0]*y[1] + nu*y[2] - y[3]; n = 3
    return y, sp.expand(N), n

def Dx(p, y):
    return sp.expand(sum(sp.diff(p, y[j])*y[j+1] for j in range(len(y)-1) if p.has(y[j])))

def DN(p, y, DkN):
    return sp.expand(sum(sp.diff(p, y[j])*DkN(j) for j in range(len(y)) if p.has(y[j])))

class Psi:
    def __init__(self, name, nu=sp.Rational(1)):
        self.y, self.N, self.n = make_eq(name, nu)
        self.name = name
        self._DkN = {0: self.N}
        self._cache = {}
    def DkN(self, j):
        if j not in self._DkN:
            self._DkN[j] = Dx(self.DkN(j-1), self.y)
        return self._DkN[j]
    def theta(self, a, b):
        key = (a, b)
        if key not in self._cache:
            if a == 0:
                val = self.y[b]
            else:
                val = DN(self.theta(a-1, b), self.y, self.DkN)
            self._cache[key] = val
        return self._cache[key]

def kernel_dim(images):
    gens = sorted(set().union(*[e.free_symbols for e in images]), key=lambda s: s.name) or [sp.Symbol('z')]
    dicts = [sp.Poly(e, *gens, domain=QQ).as_dict() if e != 0 else {} for e in images]
    keys = sorted(set().union(*[set(d.keys()) for d in dicts]))
    rows = [[QQ.convert(d.get(key, 0)) for d in dicts] for key in keys]
    if not rows:
        return len(images)
    Mx = DomainMatrix(rows, (len(keys), len(images)), QQ)
    return len(images) - Mx.rank()

def V_dk(psi, d, k):
    thetas = [(a, b) for a in range(k+1) for b in range(k+1-a)]
    imgs = []
    for e in range(0, d+1):
        for cmb in combinations_with_replacement(thetas, e):
            p = sp.Integer(1)
            for (a, b) in cmb:
                p = p*psi.theta(a, b)
            imgs.append(sp.expand(p))
    return imgs

def H_Dk(psi, D, k):
    # theta(y^j) -> D_N^a D^b (y0^j)
    imgs = []
    for j in range(1, D+1):
        base = psi.y[0]**j
        cache = {}
        for a in range(k+1):
            for b in range(k+1-a):
                p = base
                for _ in range(b):
                    p = Dx(p, psi.y)
                for _ in range(a):
                    p = DN(p, psi.y, psi.DkN)
                imgs.append(sp.expand(p))
    return imgs

if __name__ == '__main__':
    out = []
    def rep(s):
        print(s, flush=True)
    which = sys.argv[1] if len(sys.argv) > 1 else 'V'
    if which == 'V':
        for name, cases in [('burgers', [(2, 2), (2, 3), (3, 2), (3, 3)]),
                            ('fisher', [(2, 2), (2, 3), (3, 2)]),
                            ('kdv', [(2, 3), (2, 4), (3, 3)]),
                            ('kdvb', [(2, 3), (3, 3)])]:
            psi = Psi(name)
            for d, k in cases:
                t0 = time.time()
                imgs = V_dk(psi, d, k)
                kd = kernel_dim(imgs)
                rep(f"{name}: dim([F] cap V_(d={d},k={k})) = {kd}  (dim V = {len(imgs)}) [{time.time()-t0:.1f}s]")
        psi = Psi('burgers', nu=sp.Rational(1, 3))
        imgs = V_dk(psi, 2, 2)
        rep(f"burgers nu=1/3: dim([F] cap V_(2,2)) = {kernel_dim(imgs)}")
    if which == 'H':
        psi = Psi('burgers')
        for D, k in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (3, 4)]:
            imgs = H_Dk(psi, D, k)
            kd = kernel_dim(imgs)
            # R.F_B ∩ H_{D,k}: theta F_B with |theta| <= k-2  -> number of theta with |theta| <= k-2
            exp_rf = (k-1)*k//2
            rep(f"burgers Hammerstein D={D} ord<={k}: dim([F] cap H) = {kd}; dim(R.F_B cap H) = {exp_rf}")
