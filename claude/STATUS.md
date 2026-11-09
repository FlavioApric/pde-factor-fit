# STATUS of `analytical` (2026-11-07)

- Paper `paper/analytical`: 57 pages, builds clean. Part I (Phases 0-5) in Structure B order, Part II (Phases 6-10) added from the complete edition: systems/gauge, variable coefficients, convergence/noise, encoder, dictionary, Phase-10 corrections, extended algorithm, limits, open-problem list, directions.
- Complete editions in original format: `paper/analytical_complete` (117 pp paper, 263 pp proof catalogue; both rebuilt from source, 0 undefined references), `analytical_phases05`, `analytical_explained`, `analytical_original`.
- Everything else of the old repository (all session plans, reports, audits, scouting, ledgers, scripts) is in `claude/archive/` and `verification/`; `INVENTORY.md` on `main` proves nothing is missing.
- Proofs: 29 proof packages in `proofs/<session>.md`; claim ledger `proofs/LEDGER.md` (final version only; earlier backups dropped).
- Verification: 94 scripts; 76 passed within 90 s, 12 slow (not judged), 6 removed for missing data (`verification/RESULTS.md`). Quick subset in pytest: 8 passed.
- Lean: `proofs/lean` holds the sources (core PBLean and the F10 files); not rebuilt in this environment.

## Main results (all proved unless noted)
Identification criterion; no finite certificate; factor decomposition on simply connected regions with overlap delta(P); per-term split false; stability iff the sum of kernels is closed (Friedrichs angle for two factors);
interaction term for commuting terms, O(N) value and Theta(2^N) table, discontinuous in Sobolev norms; Burgers closed form before the shock, jumps forced after; dictionary identification modulo differential consequences.

## Open (see `claude/notes/PROBLEMI_APERTI.md`)
KdV with nonzero reflection coefficient (INT-Q1); time-uniform shock estimate with several births (OPA-Q1); density of the sum of kernels on nonconvex domains; delta_N(K) for general N; sum closure for N >= 3 differential factors (C12-Q2); nonlinear asymptotics with derivatives.

## Not done
Independent human referee; official SIAM class build; English translation of the notes.
