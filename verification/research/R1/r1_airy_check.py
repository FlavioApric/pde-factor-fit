import mpmath as mp
mp.mp.dps=30
def mu_num(sig,tt):
    f=lambda k: mp.exp(-sig**2*k**2)*mp.cos(k**3*tt)
    K=mp.sqrt(80)/sig   # e^{-sig^2 k^2} < e^{-80} oltre K
    pts=[K*j/4000 for j in range(4001)]
    return 2*mp.quad(f,pts)/(mp.sqrt(mp.pi)/sig)
def mu_closed(sig,tt):
    bb=sig**2*(3*tt)**(-mp.mpf(2)/3)
    return 2*mp.sqrt(mp.pi)*sig*(3*tt)**(-mp.mpf(1)/3)*mp.exp(2*bb**3/3)*mp.airyai(bb**2)
for sig,tt in [(1,1),(1,10),(mp.mpf('0.5'),3)]:
    print("sigma=%s t=%s numeric=%s closed=%s"%(sig,tt,mp.nstr(mu_num(sig,tt),15),mp.nstr(mu_closed(sig,tt),15)))
