# OP-F5D: (Lax) per ogni n via serie F; identificazione con K_n = R^n K_0; lemma Z (n<=5)
import sympy as sp
x=sp.symbols('x'); v=sp.Function('v')(x); phi=sp.Function('phi')(x)
NMAX=6
ok=0; tot=0
def chk(name,cond):
    global ok,tot; tot+=1; ok+=bool(cond); print(('OK  ' if cond else 'FAIL'),name)
D=lambda e,k=1: sp.diff(e,x,k)
# f_m da Q(F)=zeta
f=[sp.Integer(1)]
def bracket(fs,m):
    # coefficiente di z^m in (1/2)FF''-(1/4)F'^2+vF^2, F=sum f_i z^i
    s=0
    for i in range(m+1):
        j=m-i
        if i<len(fs) and j<len(fs):
            s+=sp.Rational(1,2)*fs[i]*D(fs[j],2)-sp.Rational(1,4)*D(fs[i])*D(fs[j])+v*fs[i]*fs[j]
    return s
for m in range(1,NMAX+2):
    s=sum(f[i]*f[m-i] for i in range(1,m))+bracket(f,m-1)
    f.append(sp.expand(-s/2))
# equazione lineare: f'_{m+1} = -1/2 J f_m, J g = 1/2 g''' + 2 v g' + v' g
J=lambda g: sp.Rational(1,2)*D(g,3)+2*v*D(g)+D(v)*g
for m in range(0,NMAX+1):
    chk(f'ricorrenza lineare m={m}', sp.expand(D(f[m+1])+J(f[m])/2)==0)
# nessun termine costante
for m in range(1,NMAX+2):
    chk(f'f_{m} senza termine costante', sp.expand(f[m].subs({sp.Derivative(v,(x,k)):0 for k in range(1,20)}).subs(v,0))==0)
# K_n via R con antiderivata 2(-4)^n f_{n+1}
K=[-D(v)]
for n in range(0,NMAX):
    anti=2*(-4)**n*f[n+1]
    chk(f'd/dx anti_{n} = K_{n}', sp.expand(D(anti)-K[n])==0)
    K.append(sp.expand(D(K[n],2)+4*v*K[n]+2*D(v)*anti))
chk('K_1 = -(v3+6vv1)', sp.expand(K[1]+D(v,3)+6*v*D(v))==0)
chk('K_2 = -(v5+10vv3+20v1v2+30v^2v1)', sp.expand(K[2]+D(v,5)+10*v*D(v,3)+20*D(v)*D(v,2)+30*v**2*D(v))==0)
Lop=lambda g: -D(g,2)-v*g
def Lpow(g,k):
    for _ in range(k): g=Lop(g)
    return g
def B(n,g):
    return (-1)**n*sum(f[j]*D(Lpow(g,n-j))-sp.Rational(1,2)*D(f[j])*Lpow(g,n-j) for j in range(n+1))
for n in range(0,6):
    c=sp.expand(B(n,Lop(phi))-Lop(B(n,phi))-sp.Rational(1,4**n)*K[n]*phi)
    chk(f'[B_{n},L] = 4^-n K_n (operatori)', c==0)
    # monico d'ordine 2n+1
    lead=sp.expand(B(n,phi)).coeff(sp.Derivative(phi,(x,2*n+1)))
    chk(f'B_{n} monico', sp.simplify(lead-1)==0)
print(f'TOTALE {ok}/{tot}')
