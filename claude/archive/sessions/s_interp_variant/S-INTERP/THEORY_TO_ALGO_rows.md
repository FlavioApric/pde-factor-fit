
## 5. S-INTERP rows (2026-10-28)

| # | result (status) | what it says | decision in PDEFactorML |
|---|---|---|---|
| T25 | R2-T6 (DIMOSTRATO-CON-FONTE: Ehrenpreis 1970, Palamodov 1970, Hörmander §7.6) | every u ∈ ker P on a convex Ω is ∫_V e^{⟨x,z⟩}dμ(z) over the variety; for reduced P, B = 1; on the torus a countable basis indexed by V(P) ∩ (ℂ × iℤ) | the EPGP prior (`interp/epgp.py`) uses features e^{λ(κ)t + iκx} with Q_j(λ, iκ) = 0. κ runs on a lattice finer than 2π/L (continuous measure, non-unique). Each factor gets its own GP, which makes the component posteriors separable. |
| T26 | DICT-ILIM-Hs (DIMOSTRATO, F10-C2/C-19) | ‖f‖_{C^s} ≤ C‖f‖_{L²}^θ ‖f‖_{C^{s,1}}^{1−θ}, θ = 2/(2s+2+N) | a small L² interpolation error does not imply a small error in the derivatives the core reads, because the exponent θ < 1 amplifies it. So coverage is checked on u, and the high-κ (derivative-heavy) bias is measured separately on the decay rates λ(κ). |
