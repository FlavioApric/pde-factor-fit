import sympy as sp, random
from sympy import (symbols, Function, exp, sqrt, pi, I, diff, simplify, sin, cos, sinh, cosh,
                   log, atanh, besselj, bessely, airyai, airybi, legendre, hermite, integrate, oo, Rational, expand_func, gamma)
RES = []
def check(name, expr, vars_=(), domain=(0.3, 2.0)):
    """PASS if expr simplifies to 0; else fall back to high-precision numeric spot checks (PASS-num)."""
    def ef(z):
        try: return sp.expand_func(z)
        except Exception: return z
    e = sp.simplify(ef(expr))
    if e == 0:
        RES.append((name, 'PASS')); print('PASS     ', name); return
    e2 = sp.simplify(sp.expand(sp.powsimp(ef(expr), force=True)))
    if e2 == 0:
        RES.append((name, 'PASS')); print('PASS     ', name); return
    random.seed(1); ok = True
    for _ in range(6):
        sub = {v: sp.Rational(random.randint(int(domain[0]*100), int(domain[1]*100)), 100) for v in vars_}
        val = sp.N(expr.subs(sub), 30)
        if abs(complex(val)) > 1e-20: ok = False; print('   residual', sub, val)
    tag = 'PASS-num' if ok else 'FAIL'
    RES.append((name, tag)); print(f'{tag:9s}', name)
def summary():
    n = sum(1 for _, t in RES if t.startswith('PASS'))
    print(f'--- {n}/{len(RES)} checks passed ---')
