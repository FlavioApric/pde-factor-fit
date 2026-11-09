import sys, itertools, random
sys.stdout.reconfigure(encoding='utf-8')
import sympy as sp
t,x,y=sp.symbols('t x y',real=True)
random.seed(1)
def app(Q,f,vars_):
    # Q: dict {(a,b,c): coeff} for d_t^a d_x^b d_y^c
    return sp.expand(sum(co*sp.diff(f,*( [t]*a+[x]*b+[y]*c )) if (a+b+c)>0 else co*f for (a,b,c),co in Q.items()))
ok=True
for n_ in (2,3):
  vs=[t,x] if n_==2 else [t,x,y]
  for M in (0,1,2,3):
    N=M+2
    E=sp.exp(x**2+(y**2 if n_==3 else 0))
    mons=[m for m in itertools.product(range(M+1),repeat=n_) if sum(m)<=M]
    q=sum(random.randint(-3,3)*sp.prod([v**e for v,e in zip(vs,m)]) for m in mons)
    eps=sp.Rational(1,sp.factorial(N-1))
    v=q+eps*t**(N-1)*E
    # tau^N kills v
    assert sp.simplify(sp.diff(v,t,N))==0
    # jet: v - q has order N-1
    ser=sp.series((v-q).subs({x:x, }),t,0,N-1).removeO()
    assert sp.simplify(ser)==0
    # random Q with reduced form (deg_t<N) nonzero -> Q(d)v != 0 ; also check the c_j formula
    for trial in range(15):
      Q={}
      for a in range(N):
        for b in range(3):
          for c in (range(2) if n_==3 else [0]):
            if random.random()<0.3: Q[(a,b,c)]=random.randint(-2,2)+sp.I*random.randint(-2,2)
      Q={k:c for k,c in Q.items() if c!=0}
      if not Q: continue
      r=sp.simplify(app(Q,v,vs))
      if r==0: ok=False; print('COUNTEREXAMPLE',n_,M,Q)
      # c_j check: Q_j(dx) d_t^j (t^{N-1} E) = c_j t^{N-1-j} r_j E
    for j in range(N):
      lhs=sp.diff(t**(N-1),t,j); cj=sp.factorial(N-1)/sp.factorial(N-1-j)
      assert sp.simplify(lhs-cj*t**(N-1-j))==0
print('lemma checks ok' if ok else 'FAILED')
# entireness bound: sum over N_k of |t|^{N_k-1}/(N_k-1)! <= e^{|t|}
print('done')
