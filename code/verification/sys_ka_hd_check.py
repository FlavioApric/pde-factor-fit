import sympy as sp
t,x1,x2,x3,m=sp.symbols('t x1 x2 x3 m')
I2=sp.eye(2)
s1=sp.Matrix([[0,1],[1,0]]);s2=sp.Matrix([[0,-sp.I],[sp.I,0]]);s3=sp.Matrix([[1,0],[0,-1]])
p0,p1,p2,p3=[sp.I*v for v in (t,x1,x2,x3)]
sp_=p1*s1+p2*s2+p3*s3
X=p0*I2-sp_;Y=p0*I2+sp_
D=sp.BlockMatrix([[-m*I2,X],[Y,-m*I2]]).as_explicit()
KG=sp.expand(p0**2-p1**2-p2**2-p3**2)
print('YX',sp.simplify(Y*X-KG*I2)==sp.zeros(2))
# unimodular reduction: U*D*C = diag(-m I, (YX-m^2)/m)
U=sp.BlockMatrix([[I2,sp.zeros(2)],[Y/m,I2]]).as_explicit()
C=sp.BlockMatrix([[I2,X/m],[sp.zeros(2),I2]]).as_explicit()
print('Schur',sp.simplify(U*D*C - sp.diag(-m*I2,(Y*X-m**2*I2)/m)))
print('detU,detC',U.det(),C.det())
print('factor KG-m^2 (m=1):',sp.factor_list(KG-1))
print('1+1 factor:',sp.factor_list(sp.expand(p0**2-p1**2-1)))
print('det D',sp.factor(D.det()))
# H-DIRAC-1: random alpha0,B0, check no V!=I degree<=? gives tau-free deg<=1 difference (brute force deg V<=1)
import random
random.seed(1)
a=[sp.Matrix(4,4,lambda i,j:random.randint(-2,2)) for _ in range(3)]
B0=sp.Matrix(4,4,lambda i,j:random.randint(-2,2))
L0=t*sp.eye(4)+x1*a[0]+x2*a[1]+x3*a[2]+B0
vars_=[t,x1,x2,x3]
W=sp.zeros(4,4);unk=[]
for i in range(4):
  for j in range(4):
    c=sp.symbols(f'w{i}{j}_0:5');unk+=c
    W[i,j]=c[0]+sum(c[k+1]*vars_[k] for k in range(4))
E=sp.expand(W*L0)
eqs=[]
for e in E:
  P=sp.Poly(e,*vars_)
  for mon,co in P.terms():
    if mon[0]>0 or sum(mon)>1: eqs.append(co)
sol=sp.solve(eqs,unk,dict=True)
print('W solutions nonzero?',[any(v!=0 for v in s.values()) for s in sol], 'free:',set(unk)-set(sol[0].keys()) if sol else None)
