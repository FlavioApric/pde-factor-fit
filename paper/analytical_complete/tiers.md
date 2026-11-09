# Tiers of Phase 0–5 results (proof catalogue)

Ranking source: `graphify-out/graph.json`, in-degree on `depends_on` edges (how many other claims rely on the result), plus the headline theorems of `PAPER/paper.tex`. The statuses come from `claims/LEDGER.md` v2.

Labels: P = proved (audited), PM = proved modulo a cited theorem, PW = proof written (not audited), CS = from cited source, C = conditional, VX = checked on examples, F = false (counterexample proved), O = open.

## Part I — load-bearing results (full proof, step by step)

| # | ID | Result | in-deg | Label |
|---|---|---|---|---|
| A1 | C3-L2 | Splitting off the gcd: I = g·J, V(J) finite | 4 | P |
| A2 | C3-L3 | EP ⇔ finite-dimensional derivative span | 12 | P |
| A3 | C3-T1 | Identification criterion | 31 | P |
| A4 | C3-T6 | Intrinsic operator G_u, ≤ Σe_i tests | 6 | P |
| A5 | P4-T2 | Spectral characterisation, R·u ∩ EP ≅ R/J_u | 3 | P |
| A6 | C3-T2/T3 | Finite-data thresholds (Bézout, jet 2d−1) | 5 | P |
| A7 | C3-P1 | No finite certificate | 5 | P |
| A8 | P4-T4 | Decidable with a bound B | 5 | P |
| A9 | P4-T5 | Black-box impossibility | 5 | P |
| A10 | R2-T3 | Terms do not give components | 4 | P |
| A11 | C12-L3 | Finite quotient R/(Q_i,Q_j) | 5 | P |
| A12 | C12-L1′, L2′ | Twisted Poincaré lemma | 4 | P |
| A13 | C12-T1′ | Factor decomposition, ambiguity δ(P) | 12 | P |
| A14 | C12-P10 | Holes break the decomposition | – | P |
| A15 | C12-C1 | Loss of a derivative (counterexample) | – | F |
| A16 | C12-T3 | Chord criterion (N = 2) | – | P |
| A17 | C12-P7 | H^m components ⇔ closed and dense, γ_N | 4 | P |
| A18 | OPF5B-T1 | Density on bounded convex sets | – | PM |
| A19 | P1-T2 | Closed form of E_int in class 𝔅 | 7 | P |
| A20 | P1-T3 | Cost O(N) versus Θ(2^N) | 3 | P |
| A21 | P1-P1(e) | E_int not continuous in H^m | – | F |
| A22 | P2-T2, P2-T4 | No sparse representation, no stable regularisation | 4 | P |
| A23 | P3-T1 | Dyson–Phillips converges for every t | 7 | P |
| A24 | P1-T5 | No finite product of flows (non-commuting) | 3 | P |
| A25 | S4T-T1 | Jet of the nonlinear interaction term | 5 | P |
| A26 | S4T-T2 | Closed form before the shock | 3 | P |
| A27 | OPA-T1 | ‖E_int‖_{L¹} = Θ(ν) after the shock | 5 | PM |
| A28 | OPF5A-T2 | Uniform rate ν|log ν| | 3 | PM |
| A29 | S4ID-T1 | Dictionary criterion (exact sequence) | 10 | P |
| A30 | S4ID-T2 | Burgers with N shocks identifies iff d ≤ N | 6 | P |
| A31 | OPF5C-T2 | KdV N-soliton degree (N+2)2^{N−1} | – | PM |

## Part II — remaining results (grouped by phase, then by ID)

- **Phase 0–1, algebra and identification.** R4-T5[𝕋], R4-T5[alg], II-C1, II-L1, II-T1, II-P2, II-P6, II-P8, II-P10 (PW), II-T2, II-T3, II-C2, II-T4, II-P5, II-T7, II-T9 (CS), C3-T4, C3-T5, C3-C1, C3-P3, C3-P5, C3-C2, C3-P1[gen] (CS), P4-T1, P4-C1..C3, P4-L1..L7, P4-T3, P4-T6 (PM), OP-ALG-T1 (PM), OP-ALG-T3, T4, P5, L5, C1, OPR2-L2/L3/T3/C2/P3′, R6-T3 (F).
- **Phase 2, decomposition and regularity.** C12-T1, C12-L1, L2, L5, C12-T2, C12-P4, C12-P6 (CS), C12-P2/P3, P2-T3, OPF-L1..P7, OPF-T4, OPF5B-L1, C1, P3, L5, T6, P7, P8, T2, C4, OPR2-T1, T2, C2a, S5-L2.
- **Phase 3, interaction term.** R5-T2(i–iv), P1-L1..L5, P1-P2, P3, P4, P1-T4, P1-P5, P1-P6, P1-P1(a–d), P1-C1, P2-T1, L1, P2, P3, P4, C1, C2, P3-L1, L2, P2, T3, T4, T5, T6, R5-P6, R5-T4, TROP-3′, TROP-4, TROP-5..8 (PW), OPA-L2, OPA-T2, OPA-T3, OPA-P3, OPA-P4, OPF5A-L5, T5, L4, T4.
- **Phase 4, nonlinear.** Lemma J, S4T-L0, L1, L2, S4T-P3, S4T-T3 (PM / C), S4T-P5, P6, C1, OPA-L3..L5, OPF5A-L1..L3, T1, T3, C1, OPF5D-T6, T7, OPR2-L5, T5, S4ID-P1, L2, L4, L5, C2, P5, P6, S4ID-T3, T4, P7, S4ID-K1 = OP-T7, OP-L8..L10, OP-C11, OP-T1, E3, C3′, OP-L2, P4, O5, P6, OP-L12, P13, P14, OP-K15, OP-L16, P17, P18, OPF5C-L1..L8, T1, P7, P9, T6, OPF5D-T1, T2, L3..L8, T3, L9, C1, L10..L12, T4, INT-T1(A), UC-ω, B1, INT-P5, P6, F4LIN-T2, L-S, F4L-P3, KIEFFER-C, ALG-L1, ALG-T1, P3, P4, P6, MODREL-T1, OPR2-P4, P6, O8, O9′.
- **Conditional, open, false and example-only results** are listed with their labels only (no proof): INT-T1(B,C), INT-T2 dynamic, OPF5D-C2, P14, P15, S4ID-P8, OPR2-P7, S4T-T3(iv) (now closed by OPF5D-T6), OPF5C-T5, A1–A11, EX-*, and every row marked APERTO.

**Policy for long analytic proofs in Part II.** Proofs that take more than about 4 pages in their package (OPF5D scattering, OPF5A Burgers rates, OPF5C Hirota) are given as a full step structure with every key estimate displayed, plus a pointer to the package section for the routine computations. Each such proof is marked "condensed".
