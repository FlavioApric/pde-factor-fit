# KA attack report: OPF5A-L5 / OPF5A-T5 (kill-argument review)

Input read: only `work/CHECK/KA_OPF5A_T5_input.md`. Scripts are in the scratchpad (s20ka_nt.py, s20ka_modal.py, s20ka_conv.py, s20ka_dec.py). No project file was modified except this one.

## A1. L5(a) conjugation
- Target: S(t) = e^{-c^2 t/4D} M_theta S^D M_theta^{-1}.
- Attack: recomputed M^{-1} A M w = D w'' + (2D theta - c) w' + (D theta^2 - c theta) w. With theta = c/2D this gives D w'' - (c^2/4D) w. M_theta preserves H^2 ∩ H^1_0.
- Outcome: SURVIVES.

## A2. L5(b) Gaussian shift
- Attack: (z ∓ ct)^2/4Dt = z^2/4Dt ∓ theta z + c^2 t/4D. This gives G(z ∓ ct) = e^{±theta z - c^2t/4D} G(z).
- Outcome: SURVIVES.

## A3. L5(c) term-by-term computation
- Direct terms, j=0: S gives G(x-y-ct) on (0,L). S^D S_2 gives the same kernel on (0,L-ct). The difference is the integral over (L-ct, L), which equals int_0^{ct} G(xi+ct-s) u~(s) ds because G is even. SURVIVES.
- Reflected terms, j=0: S gives -e^{-c^2t/4D} e^{theta x} ∫G(x+y)e^{-theta y}u0. S^D S_2 gives -e^{-c^2t/4D} e^{-theta x} ∫_0^{L-ct} G(x+y)e^{-theta y}u0. The difference is -2 e^{-c^2t/4D} sinh(theta x)(...) = B_0. Extending the second integral to (0,L) adds terms with x+y ≥ L-ct ≥ L/2. These are bounded by e^{-L^2/16Dt}, which is at most e^{-L^2/20Dt} up to constants. SURVIVES.
- Reflected terms, j=1: the kernel term is -G(x+y-2L) = -G(xi+s). The S^D S_2 kernel is K(x, y+ct), with reflected term -G(z'-ct). In the difference this enters with sign +, and G(z'-ct) = e^{theta(xi+s) - c^2t/4D} G(xi+s). Recombining the integrals gives B_L - ∫_0^{ct} G(xi+s-ct) u~(s) ds. Sign and the factor 2 sinh(theta xi) e^{theta s} are correct. (The text's phrase "In S^D S_2 the term is +..." means "its contribution to the difference is +", which is correct.) SURVIVES.
- Origin of R_L: T_1 minus the j=1 leftover, after r = ct - s, gives ∫_0^{ct}[G(xi+r) - G(xi-r)] u~(ct-r) dr = R_L. Sign is correct. SURVIVES.
- R_im: every remaining image has |argument| ≥ L - ct ≥ L/2. The weights are at most e^{theta L} (in S) or 1 (in S^D S_2). The Gaussian dominates, and the Schur bound holds. SURVIVES.
- Independent numerical check (s20ka_dec.py): u0 = sin(pi x/L)(1+x), L=1.3, D=0.3, c=1.7. A modal (DST, 2^15 nodes) E^mult was compared against B_0+B_L+R_L computed by direct quadrature. Relative residual: 9.3e-7 at t=1e-2 and 3.9e-6 at t=2.5e-3 (quadrature level). Without R_L the residual is 1.8e-2 and 4.7e-3, which confirms R_L is the missing piece. SURVIVES.

## A4. L5(d) bounds on R_L
- K_+ ≥ 0 is the half-line Dirichlet kernel and a contraction on L^2(0,∞), which gives the first bound. K_+(xi,r) = -∫_{-r}^{r} G'(xi+eta) d eta holds (sign checked). Minkowski gives ||K_+(.,r)|| ≤ 2r ||G'_{Dt}||_2 = C r (Dt)^{-3/4}. Minkowski again in r gives the second bound.
- Outcome: SURVIVES.

## A5. Step 1 (R_L ≤ C t^{k+5/4})
- |u~(s)| ≤ C s^k holds: all derivatives of order < k vanish at L by the minimality of k, and u0(L) = 0.
- ∫_0^{ct} r (ct)^k dr ~ t^{k+2}. Times t^{-3/4} this is t^{k+5/4}. Relative to the main term it is t^{k/2+1/2} ⊂ O(t).
- Outcome: SURVIVES.

## A6. Step 2: |rho| ≤ C(x^2 + y + t)
- sinh(theta x)/(theta x) = 1 + O(x^2) (it is even in x). e^{-theta y} = 1 + O(y) and e^{-c^2t/4D} = 1 + O(t) on the bounded set [0,L]^2 × [0,1]. Products of 1+O(.) factors stay in the stated form.
- The identity 2 sinh(theta x) = (c/D) x · sinh(theta x)/(theta x) holds because 2 theta = c/D.
- Outcome: SURVIVES.

## A7. Step 2 scaling of the remainder to t^{k/2+5/4}
- Term by term after x = sqrt(Dt) w, y = sqrt(Dt) v: x y^{k+1} and x y^k · y scale as t^{(k+2)/2}. x y^k x^2 and x y^k t scale as t^{(k+3)/2} ≤ t^{(k+2)/2} for t ≤ 1.
- phi(w) ≤ C(w + w^3) e^{-w^2/4} by (w+v)^2 ≥ w^2 + v^2 for w, v ≥ 0. The text's bound (1+w^{k+3}) is weaker but still valid.
- The L^2(dx) norm adds a factor (Dt)^{1/4}, giving t^{k/2+5/4}. The Taylor-tail piece over y > L is e^{-L^2/4Dt}-small.
- Outcome: SURVIVES.

## A8. Exponents of D and power of |c| in the leading term
- M_0 = -(c/D)(gamma_0/k!) · sqrt(Dt) w · (Dt)^{k/2} g_k(w) = -c (gamma_0/k!) D^{(k-1)/2} t^{(k+1)/2} w g_k(w).
- The L^2 norm multiplies this by (Dt)^{1/4}, giving D^{k/2-1/4} t^{k/2+3/4}. |c| appears to the first power.
- The numerics below test both D ≠ 1 and |c| ≠ 1.
- Outcome: SURVIVES.

## A9. Step 3 (B_L)
- Replacing theta → -theta in the B_0 form gives exactly B_L (-2 sinh(-theta xi) = 2 sinh(theta xi)). With u~^{(k)}(0) = (-1)^k u0^{(k)}(L), only |.| enters the norm.
- Outcome: SURVIVES.

## A10. Cross term <M_0, M_L>
- w g_k(w) ≤ C e^{-w^2/8}. Then |M_0 M_L| ≤ C t^{k+1} exp(-(x^2 + (L-x)^2)/8Dt) ≤ C e^{-L^2/16Dt}.
- Outcome: SURVIVES.

## A11. Only one endpoint active (u0^{(k)}(0) = 0 but u0^{(k)}(L) ≠ 0, and the converse)
- With gamma_0 = 0 we get M_0 = 0, and the Taylor bound becomes |u0(y)| ≤ C y^{k+1}. So B_0 = O(t^{k/2+5/4}), which is absorbed into the relative O(t^{1/2}).
- Numerics: cases "k2 only0" and "k2 onlyL" both converge to the predicted constant.
- Outcome: SURVIVES.

## A12. Is the relative error really O(t^{1/2}) and not O(t^{1/4})?
- Analytically, every correction is t^{k/2+5/4} (B-M), t^{k+5/4} (R_L) or exponentially small. Relative to the main term these are t^{1/2} or better. No t^{1/4} source exists.
- Numerically: when t is divided by 4, the relative error drops by a factor tending to 2. That is the signature of t^{1/2}, not t^{1/4} (which would give 1.41).
- Outcome: SURVIVES.

## A13. Hypotheses (u0 ∈ C^{k+1}, u0(0) = u0(L) = 0)
- These suffice. C^{k+1} is used only for the Taylor remainder C y^{k+1} (C^{k,1} would also suffice). k is finite by assumption, so the denominator is > 0.
- Small point: the flat-data claim (O(t^p) for every p) needs u0 flat to infinite order at both ends. That is what the text says.
- Constants depend on ||u0||_{C^{k+1}}, c, D and L. That is acceptable.
- Outcome: SURVIVES.

## A14. Reflection for c < 0
- The setup defines S_2 f = f(x - ct) 1_{x > ct}, which literally makes sense only for c > 0. For c < 0 one must read S_2 as transport with inflow at L.
- With that reading, x → L - x maps the problem to the c > 0 case. The formula (|c|, sum of squares of the endpoint derivatives) is invariant under the swap.
- Numerics with c = -0.8, D = 2, inflow at L: the constant is confirmed in all cases.
- Outcome: GAP (definitional only: the c < 0 version of S_2 is not written out). Severity MINOR.

## A15. Constants Ntilde_k (computed independently with scipy quad)
- Ntilde_1 = 0.2340046, Ntilde_2 = 0.3252441, Ntilde_3 = 0.6103437 (Ntilde_4 = 1.398871).
- These match the declared 0.234005, 0.325244 and 0.610344.
- Outcome: SURVIVES.

## A16. Modal check of the full asymptotic formula (s20ka_modal.py)
- Method: exact semigroups via e^{theta x}-conjugated sine series, DST with 2^18 nodes. Discretization converged to about 1e-9 relative (checked from 2^16 to 2^19 nodes).
- Parameters: L = 1.3, with (D, c) = (0.3, 1.7) and (2.0, -0.8). Times t = 1e-2, 2.5e-3, 6.25e-4, 1.5625e-4.
- Relative deviation at t = 1.5625e-4:

| Case | Relative deviation |
|---|---|
| k=1, both endpoints | 8.7e-3 / -2.7e-2 |
| k=2, both endpoints | 6.3e-3 / -6.6e-2 |
| k=2, endpoint 0 only | -6.4e-2 / -6.8e-2 |
| k=2, endpoint L only | 2.4e-3 / -8.9e-2 |
| k=3 | -9.1e-3 / -1.0e-1 |

- Ratios between successive times tend to 2, so all cases converge at rate t^{1/2}.
- Outcome: SURVIVES.

## Overall verdict: SURVIVES

All steps of L5 and T5 survive term-by-term recomputation. This covers the signs, the origin of R_L, the K_+ bound, the bound on rho, the scaling, the exponents, the cross term and the single-endpoint case. Independent numerics confirm the constants, the D and |c| dependence, the exact decomposition, and the O(t^{1/2}) relative error, including for c < 0.

The only defect is MINOR: the c < 0 form of S_2 (inflow at L) is implicit and not written out. The "Conseguenza" paragraph, which cites OPA-T2(iii) and OPA-P4, was not checked because those statements are not in the input.
