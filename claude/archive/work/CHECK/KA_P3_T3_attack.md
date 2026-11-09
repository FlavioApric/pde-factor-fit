**Rejection memo, P3-T3**

The computations in (i)–(iv) hold up. What fails is the theorem's main claim. The *Lettura* (2) says the dividing line is "exact and readable on the datum", namely $Vu_0\in H^1_0$, and that the alternative to $t^{5/4}$ is $t^2$. This is false outside the finite sine sums of (iii), and (iii) proves nothing beyond them.

A finite sine sum $u_0=\sum_{n\le N}c_ne_n$ automatically has $u_0''=0$ at both ends. So (iii)(c), through (iv), never has to face the extra condition $A_0u_0\in H^1_0$ that (iv) actually requires. That condition is a second compatibility condition, independent of $u_0'(0)=u_0'(L)=0$.

Counterexample: $u_0=x^2(L-x)^2$, with $L=c=D=1$. It lies in $D(A_0)$ and $Vu_0\in H^1_0$, but $u_0''(0)=2\neq0$. I evaluated the exact modal series of P3-P1(b), $E_m=\sum_nc_nV_{mn}T_{nm}$, keeping 6000 modes. The closed-form sine coefficients were checked by quadrature. The successive log–log slopes of $\lVert E^{mult,(1)}\rVert$ are 1.59, 1.67, 1.70, 1.72 for $t$ from $10^{-2}$ to $10^{-4}$, heading towards $7/4$ and not towards 2. The mechanism is the one in (iv): $\lVert\partial S_0(r)A_0u_0\rVert\sim r^{-1/4}$ in a boundary layer of width $\sqrt r$.

So the boundary does not produce a two-way split ($t^{5/4}$ or $t^2$). It produces a ladder of exponents, $5/4,\,7/4,\dots$, one step for each compatibility condition that fails. This exposes the "Θ versus $O(t^2)$" statement in (iii) as an accident of the finite-mode class. The constants also degrade without control: $C_1$ grows like $N\sum n|c_n|$ and $t_*\le|S|/(48A\kappa N^2)$ shrinks to 0 as $N$ grows. So nothing passes to the limit of general data.

The theorem as stated is correct but trivial, and the claim drawn from it is false.
