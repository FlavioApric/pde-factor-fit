# Piano esteso — Fasi 6–11: Problema 1, Problema 2, convergenza, dizionario universale → algoritmo esteso → formalizzazione → paper

## Context
Phases 1–5 built the analytic theory of the algorithm for **scalar** PDEs with **constant coefficients** (linear package, Gate 3) and its scalar nonlinear extension (Phase 4, G★′-NL). The original plan (`D:\piano di ricerca.md`, H1/H2, §Phase 5) postponed Problema 1 (varying V: Schrödinger, Dirac) and Problema 2 (matrix coefficients: Dirac 4×4) until after Phase 5.
With the user (26/10) we fixed the scope of the extension:
- **P-A Systems / matrix coefficients** (Dirac, Maxwell, elasticity, coupled systems), including **identification up to gauge**.
- **P-B Variable coefficients.** V(x) (Weyl algebra) and V(t,x) (non-autonomous: propagators). **Two separate goals:** (B1) *identify* V; (B2) *remove* V as "noise" with an **analytic encoder**: transformation operators of Gel'fand–Levitan–Marchenko type, Liouville and gauge transforms, Darboux intertwining, homogenization or averaging when V oscillates. No ML.
- **P-C Convergence to a differential equation**, all three meanings: (C1) consistency as the data grows (identification in the limit, rates, impossibility; C3-P1 already rules out finite certificates); (C2) locality (when the law is a differential operator, nonlocal, or does not exist); (C3) convergence of the iterative parts (splitting, Dyson, Magnus).
- **P-D Operators outside the catalogue.**
  - (D1) Universal dictionary: user request: "prove that a dictionary taking everything into account can be created, and build it".
  - (D2) A misfit certificate.
  - (D3) Best approximation with an error bound.
  - (D4) Rules for enlarging the dictionary.
- **Other cases, all in scope:** nonlocal/fractional/integro-differential/delay; noisy data; dimension > 1+1; boundary conditions; singular or unbounded potentials (Coulomb, x²); non-polynomial nonlinearities (sine-Gordon, e^u).
- **Excluded:** ML of any kind, including Idea I (autoencoder/GMM), which stays postponed to a later phase. Numerics are used only for SymPy verification.

**Expected outcome:** a new target statement G★″, a theorem package (LEDGER), the **expanded algorithm** (specification with a guarantee for every step), the Lean formalization of the algebraic core, and the **paper** extending the Phase 5 paper or report with an "Expanded algorithm" section.

**Precondition:** start only after the Phase 5 session finishes (REPORT_FINALE, closed LEDGER, PBLean built). The parked routes from all phases are reviewed once before starting, as the plan's Phase 5 requires.

## Honesty about D1 (dictionary "for everything")
The target is the **strongest true form**, plus a negative theorem marking the boundary. Kill-argument runs before the statement is fixed. Candidate statements:
- **U1, local linear.** By Peetre's theorem, every continuous local linear operator is differential of locally finite order. Hence a filtered countable dictionary 𝓓_∞ = ∪_n 𝓓_n = {a(t,x)∂^α, with a in a countable dense basis} is universal by approximation on compacts.
- **U2, local nonlinear.** By Peetre–Slovák, local regular operators factor through finite jets. Stone–Weierstrass on jets then gives universal approximation by polynomials in (t, x, J^k u).
- **U3, nonlocal linear.** By the Schwartz kernel theorem, translation-invariant operators are Fourier multipliers. Graded symbol dictionaries (|ξ|^s, rational, log, memory kernels) are dense in classes S^m.
- **U4, systems.** Matrix versions over Mat_k, via Malgrange–Oberst duality (systems of PDE ↔ finitely generated modules).
- **N1, negative.** No countable dictionary gives *exact* identification of every operator from one solution: C3-P1, Ann(u) = 0 for generic u, cardinality. So "everything" holds in the approximation sense plus a misfit certificate, not as exact identification.
- **Link to C1.** The filtration of 𝓓_∞ together with consistency in the limit gives the "identification in the limit" theorem. This links P-C and P-D.

## Phases (same machinery as Phases 1–5)
**Phase 6: Research and scouting.** Same structure as Phase 1 and the Phase 4 sprint, with the `route-scout` skill and horizon scouts. Research topics:
- R9: systems and matrix modules: Malgrange–Oberst, Quillen–Suslin, Clifford/Dirac, square roots of Klein–Gordon, compatibility conditions.
- R10: Weyl algebra, holonomic D-modules, Loewy factorization, inverse Sturm–Liouville, transformation operators.
- R11: non-autonomous problems: propagators, Dyson/Magnus convergence, Floquet.
- R12: universality: Peetre, Slovák, Stone–Weierstrass, Schwartz kernels, symbol classes, n-widths.
- R13: convergence: identification in the limit, conditional stability (inverse-problem regularization theory, analytic).
- R14: nonlocal and fractional operators.
- R15: noise, dimension > 1+1, boundary conditions.
- R16: gauge and symmetries, homogenization for V as noise.

Output: `research/SYNTHESIS-2.md`, with prior-art checks (novelty-check, CIT-AUDIT). Gate 6 is with the user: G★″ in PROBLEM.md (v3) and the ladder L6 (systems) → L7 (V(x)) → L8 (V(t,x)) → L9 (nonlocal) → L10 (universal dictionary).

**Phase 7: Skills and sessions** (Phase 2 re-entered). Reuse the skills in `skills-local/`: session-protocol, claim-lifecycle, route-scout, kernel-catalog-entry, formalize-claim, spec-sync. If needed, create new skills with `skill-creator`, for example a "universality-check" skill or a matrix-coefficient catalogue entry. Write the SESSIONS.md roster, the communication graph and exit criteria fixed in advance. Gate 7 is with the user.

**Phase 8: Proofs.** Planned sessions:
- S8-SYS: P-A and gauge.
- S8-VAR: B1, identify V.
- S8-ENC: B2, analytic encoder.
- S8-NA: V(t,x) and C3.
- S8-CONV: C1 and C2.
- S8-DICT: D1–D4, U1–U4, N1.
- S8-NLOC.
- S8-NOISE/DIM.
- S-CHECK, the independent auditor.
- DEVIL, kill-arguments at every gate.
- CIT-AUDIT.

Every claim goes through claim-lifecycle into the LEDGER: SymPy check plus proof-checker. Gate 8a sets the routes. Gate 8b decides whether to revise the Gate 3 / G★′-NL structure (feedback loop to the earlier phases).

**Phase 9: Expanded algorithm.** Write `ALGORITMO_ESTESO.md`, the step-by-step pipeline:
1. Data model.
2. Choose the level of 𝓓_∞.
3. Identification: scalar, system or variable-coefficient.
4. Misfit certificate, or best approximation with bound.
5. Analytic encoder for V.
6. Factor and term decomposition, and E_int.
7. Convergence guarantees.

Each step cites its LEDGER theorems and states its hypotheses, cost and known failure modes (the negative theorems). DEVIL attacks the specification.

**Phase 10: Integration and formalization** (same as Phase 5). An integration session checks notation and hypotheses across all results; incompatible routes go back to active. Then bottom-up formalization (`formalize-claim`) in `D:\ProblemaBase\PBLean`. Requirements:
- no `sorry`;
- `#print axioms` shows only the standard axioms;
- an independent reviewer compares each formal statement against the LEDGER.

Candidate targets for the algebraic core, where Mathlib suffices:
- kernel decomposition for modules over Mat_k(R);
- the Dirac / Klein–Gordon factorization;
- the gauge invariance of identification;
- the finite-level filtration of 𝓓_n;
- the coprime splitting for systems.

Mathlib limits (no Weyl algebra, no C₀-semigroups) are declared. Textbook examples checked against the theory:
- free Dirac;
- Schrödinger with harmonic and Pöschl–Teller potentials (Pöschl–Teller is reflectionless, the transformation-operator case);
- fractional heat equation;
- Maxwell in vacuum.

**Phase 11: Paper.** Extend the Phase 5 paper or report with:
- a new "Expanded algorithm" section;
- the theorem sections for P-A to P-D;
- the negative theorems;
- Lean outcomes and limits.

Use only the instructions of the academic-paper skill in `_vendor` (its scripts are not run). Before closing: proof-checker audit, citation audit, DEVIL review.

## Rules (unchanged from the previous plan)
- PLAN before working.
- Load the skills explicitly.
- Communicate through `inbox/` (append only).
- Only the coordinator edits BOARD, ROUTES, NOTAZIONE, PROBLEM and LEDGER.
- Honest statuses: DIMOSTRATO, CON-FONTE, V-ex, APERTO, FALSO.
- Do not run `_vendor` scripts.
- Python is run as `.venv\Scripts\python.exe -I`.
- Every step is saved to RIPRESA.md, so work can resume from another session.
- Gates are with the user (6, 7, 8a, 8b, a final one after 11). Coordinator defaults are revocable and recorded.

## Verification
- Every claim: SymPy check plus a proof-checker report in the LEDGER.
- Every gate: ROUTES updated, DEVIL report attached, at least one non-seed route scouted or killed.
- Phase 10: `lake build` passes with no sorry and only standard axioms. The textbook examples above agree with the theory.
- Phase 11: every theorem cited in the paper has a DIMOSTRATO or CON-FONTE row in the LEDGER, and the citations are audited.
