# MAP of `analytical`

```mermaid
flowchart TD
  R[README.md] --> P[paper/analytical.tex + .pdf: the paper, 11 phases]
  R --> PR[paper/analytical_proofs.tex + .pdf: all proofs]
  R --> C[code/]
  R --> T[tests/test_verification.py]
  R --> CL[claude/]
  C --> V[verification/: 534 checks and outputs]
  C --> L[lean/: Lean 4 formalisation]
  CL --> PP[proofs/: 29 proof packages + LEDGER.md]
  CL --> AR[archive/: work, research, claims, inbox, origin, editions]
  CL --> NO[notes/: problem, routes, open problems, final report, notation, bibliography]
  CL --> PV[PROVENANCE.md, INVENTORY.md, verification_results.md]
  P -. cites Dim. An/Bn .-> PR
  PR -. each card checked by .-> V
  PP -. source of .-> PR
```

| paper content | proof package (`claude/proofs/`) | checks (`code/verification/`) |
|---|---|---|
| identification, annihilator, EP | `C3.md`, `II.md`, `P4.md` | `c12_catalog.py`, `c3_checks.*` |
| factor decomposition, overlap | `C1C2.md` | `c12_*.py` |
| stability, Friedrichs angle | `C1C2.md`, `P2.md` | `p2_*.py`, `opf5c_*.py` |
| interaction term, cost, instability | `P1.md`, `P3.md` | `p1_checks.py`, `p3_checks.py` |
| Burgers, shock, dictionary | `S4-TERM.md`, `S4-ID.md`, `S4-INTEG.md` | `s4*.py` |
| systems, variable coefficients, encoders, convergence, dictionary (Phases 6-10) | `S8-*.md`, `S10-*.md`, `OP-*.md` | `s8*.py`, `s10*.py`, `opf5*.py` |
