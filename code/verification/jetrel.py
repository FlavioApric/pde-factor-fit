# S4-ID — utilita' comuni (solo verifica). Relazioni polinomiali a coefficienti costanti tra le
# derivate in x di una funzione razionale negli esponenziali formali E_i (D E_i = k_i E_i).
# Rango esatto su QQ con DomainMatrix (aritmetica razionale esatta, nessuna numerica).
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
from itertools import combinations_with_replacement, product


class JetModel:
    """u^{(j)} = P_j / Q^{j+c} con P_j, Q polinomi nelle E formali."""
    def __init__(self, ks, P0, Q, c):
        self.ks = [sp.nsimplify(k) for k in ks]
        self.N = len(ks)
        self.E = sp.symbols('E1:%d' % (self.N+1))
        self.gens = self.E
        self.Q = sp.Poly(Q(self.E), *self.gens, domain=QQ)
        self.c = c
        self.P = [sp.Poly(P0(self.E), *self.gens, domain=QQ)]
        self.DQ = self.D(self.Q)

    def D(self, p):
        out = sp.Poly(0, *self.gens, domain=QQ)
        for ki, Ei in zip(self.ks, self.E):
            out += sp.Poly(ki*Ei, *self.gens, domain=QQ) * p.diff(Ei)
        return out

    def jet(self, kmax):
        while len(self.P) <= kmax:
            j = len(self.P) - 1           # P_{j+1} = D(P_j) Q - (j+c) P_j D(Q)
            Pj = self.P[-1]
            self.P.append(self.D(Pj)*self.Q - (j + self.c)*Pj*self.DQ)
        return self.P[:kmax+1]

    def monomials(self, d, kmax):
        ms = []
        for e in range(0, d+1):
            for cmb in combinations_with_replacement(range(kmax+1), e):
                ms.append(cmb)
        return ms

    def relation_matrix(self, monos, kmax):
        P = self.jet(kmax)
        wt = lambda cmb: sum(j + self.c for j in cmb)
        top = max(wt(m) for m in monos)
        Qp = [sp.Poly(1, *self.gens, domain=QQ)]
        for _ in range(top):
            Qp.append(Qp[-1]*self.Q)
        cols = []
        for cmb in monos:
            num = sp.Poly(1, *self.gens, domain=QQ)
            for j in cmb:
                num = num*P[j]
            num = num*Qp[top - wt(cmb)]
            cols.append(num.as_dict())
        keys = sorted(set().union(*[set(cc.keys()) for cc in cols]))
        rows = [[QQ.convert(cols[j].get(key, 0)) for j in range(len(cols))] for key in keys]
        return DomainMatrix(rows, (len(keys), len(cols)), QQ)

    def rel_dim(self, d, kmax, monos=None):
        if monos is None:
            monos = self.monomials(d, kmax)
        M = self.relation_matrix(monos, kmax)
        return len(monos) - M.rank(), len(monos)

    def kernel(self, d, kmax, monos=None):
        if monos is None:
            monos = self.monomials(d, kmax)
        M = self.relation_matrix(monos, kmax)
        ns = M.nullspace().to_Matrix()
        y = sp.symbols('y0:%d' % (kmax+1))
        rels = []
        for r in range(ns.rows):
            expr = 0
            for j, cmb in enumerate(monos):
                term = ns[r, j]
                for jj in cmb:
                    term *= y[jj]
                expr += term
            rels.append(sp.factor(expr))
        return rels


def burgers_nshock(ks, nu=sp.Rational(1)):
    # u = -2 nu phi_x/phi, phi = 1 + sum E_i  => u^{(j)} = P_j/phi^{j+1}
    ks_s = [sp.nsimplify(k) for k in ks]
    return JetModel(ks, lambda E: -2*nu*sum(k*e for k, e in zip(ks_s, E)),
                    lambda E: 1 + sum(E), 1)


def kdv_nsoliton(ks):
    # u = 2 (log f)_xx, f = Hirota tau ; u^{(j)} = P_j / f^{j+2}
    ks_s = [sp.nsimplify(k) for k in ks]
    N = len(ks_s)
    def tau(E):
        f = 0
        for mu in product([0, 1], repeat=N):
            term = sp.Integer(1)
            for i in range(N):
                for j in range(i+1, N):
                    if mu[i] and mu[j]:
                        term *= ((ks_s[i]-ks_s[j])/(ks_s[i]+ks_s[j]))**2
            for i in range(N):
                if mu[i]:
                    term *= E[i]
            f += term
        return f
    m = JetModel(ks, lambda E: 0, tau, 2)
    f = m.Q
    f1 = m.D(f); f2 = m.D(f1)
    m.P = [2*(f*f2 - f1*f1)]
    return m
