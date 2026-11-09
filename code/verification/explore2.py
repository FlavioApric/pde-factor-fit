# S4-ID esplorativo veloce (DomainMatrix). Solo controllo.
import sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from jetrel import burgers_nshock, kdv_nsoliton

def run(label, model, d, k):
    t0 = time.time()
    n, tot = model.rel_dim(d, k)
    print(f"{label} d={d} ord<={k}: dim J cap A = {n} (monomi {tot}) [{time.time()-t0:.1f}s]", flush=True)

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'b2':
        m = burgers_nshock((1, 3))
        for k in [2, 3, 4, 5, 6]:
            run('Burgers N=2 k=(1,3)', m, 2, k)
        for k in [2, 3, 4]:
            run('Burgers N=2 k=(1,3)', m, 3, k)
    if which == 'b3':
        m = burgers_nshock((1, 3, 7))
        for d, k in [(3, 2), (3, 3), (3, 4), (3, 5), (4, 3), (2, 5)]:
            run('Burgers N=3 k=(1,3,7)', m, d, k)
    if which == 'k1':
        m = kdv_nsoliton((1,))
        for d, k in [(2, 1), (3, 1), (2, 2), (2, 3), (3, 2)]:
            run('KdV N=1 k=(1)', m, d, k)
        print('kernel d=2 ord<=2:', m.kernel(2, 2))
    if which == 'k2':
        m = kdv_nsoliton((1, 2))
        for d, k in [(4, 2), (5, 2), (6, 2), (2, 3), (3, 3), (2, 4), (3, 4)]:
            run('KdV N=2 k=(1,2)', m, d, k)

    if which == 'k2b':
        m = kdv_nsoliton((1, 2))
        for d, k in [(7, 2), (8, 2), (4, 3), (5, 3)]:
            run('KdV N=2 k=(1,2)', m, d, k)

