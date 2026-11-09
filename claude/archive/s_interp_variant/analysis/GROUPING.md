# Grouping study (plan 0b.4)

Key fact: in a superposition every point (t,x) carries every component, so grouping data points cannot separate factors. Grouping happens where the factors are separate.

| Type | Where it acts | Evidence | Verdict |
|---|---|---|---|
| **A. Mode space** (dispersion points by variety) | inside every cell | E1b: k-varieties alternating regression with BIC recovers the factor set in 10/10 cases to 1e-3 noise and 8/10 at 1e-1; coefficient error 2–10× lower than "fit P then factor". GPCA (fit one P, factor) is what the v1 core does. It fails under noise because factoring a float polynomial is ill-posed (E1) | **adopt structfit (k-varieties + BIC)**. Keep GPCA/core v1 as the exact-data reference |
| **B. Domain** (laws in different regions) | cell layout | E2: γ_N collapses on small cells (∝ L², T²). E3: the non-periodic extractor is not yet reliable, so the two-regime test is inconclusive (whole domain: wrong structure, p = 1.0; left half: no modes) | **adopt quadtree / region growing with evidence**, gated by γ_N and by the extractor. Needs S-DOMAIN first |
| **C. Flow family** (terms inside one factor) | inside a factor | branch regression already gives the terms (core tests). Nothing extra seen | **ignore** as a separate stage; terms come from the factor fit |
| **D. Hypothesis** (posterior over structures) | output | structfit gives posterior weights directly (0.45–0.98 in E1b). A low top weight flags ambiguity, e.g. heat at 1e-2: 0.47 between equivalent dx choices | **adopt** as the uncertainty output, combined over GP samples |
| **E. Joint/learned** (EM over EPGP mixtures) | refinement | not tested in 0b | keep for Phase 3/4 |

Encoder: analytic features (structure, factor coefficients, energy fractions, γ_N) per cell. PCA/AE only on top of them (P2-P4).

Stop/regroup: split a cell when the children's evidence beats the parent's and both children keep γ_N above the floor. Do not split a group whose bayes_split P(split) is low.
