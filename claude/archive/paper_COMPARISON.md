# Paper A vs Paper B

Both papers have the same theorems, proofs, algorithm, data, figures and appendices. They differ in order, framing,
introduction and closing.

| | Paper A (your structure) | Paper B (proposed structure) |
|---|---|---|
| Title | Grouping Structure of Linear PDEs and Its Use in Learning Them from Data | Groups Are Factors: Learning Linear PDEs by Clustering Modes on the Factors of the Symbol |
| Opening | the symbol as a polynomial, then the transport + diffusion example | the transport + diffusion example and the failure of library regression on it, then the thesis |
| Theory order | ring → annihilator → EP → identification → factor decomposition → Friedrichs → interaction | ring → annihilator → EP → **factor decomposition first** → Friedrichs → interaction → identification |
| Theory map | roadmap figure | roadmap figure + theorem dependency graph |
| Nonlinear | own section between theory and algorithm, as in your outline | "Beyond the linear ring", inside the discussion |
| Algorithm | one section, in your order: interpolation, loop, pencil, structured fit, components, interference, labels, σ_n | "within one sample": interpolation, pencil, class, structured fit, components |
| Statistics | "The statistical layer" | "Grouping across samples" (the second grouping) |
| Limits | own section "Inference problems: solvable and unsolvable"; proved / design rule / measured table in the conclusion | subsection of the discussion, with the same table |
| Length (fallback class) | 35 pages incl. appendices | 35 pages incl. appendices |

## Referee scores (independent reviewer pass, before revision round 1)

| Item | A | B |
|---|---|---|
| Flow | 5 | 7 |
| Notation | 5 | 5 |
| Concept introduction | 5 | 7 |
| Graphics / captions | 7 | 8 |
| Math level | 7 | 7 |
| Readability | 5 | 7 |
| Publishability | 5 | 6 |

Round 1 fixed every finding (see the commit "apply referee round 1"); scores after the fixes are in the section below.

## Recommendation

**Submit B.** It states one idea in its first paragraph, shows the reader why it matters (a concrete equation on which
library regression fails), proves the grouping principle before the identification machinery, and its section titles
("within one sample", "across samples") are the two groupings of the method. A keeps your outline and is the better
choice if you want the analytical part to read as a self-contained chapter before any algorithm appears.

## Scores after revision round 1 (second independent referee pass)

| Item | A | B |
|---|---|---|
| Flow | 7 | 8 |
| Notation | 7 | 7 |
| Concept introduction | 8 | 8.5 |
| Graphics / captions | 8 | 8.5 |
| Math level | 8 | 8 |
| Readability | 7 | 8 |
| Publishability | 7 | 7.5 |

Revision round 2 then fixed everything that referee listed: the finite-data proposition now has a uniform bound and a
complete proof; abstracts separate the held-out result (19 of 20 right or equivalent, 14 with a confident label, 0
confident wrong) from the development benchmark; the error floor is stated as the Cramér–Rao bound it is; the last
double-used letters are gone (terms are now calligraphic, samples are indexed by q, cluster masses are w̄_j); the
dependency figure shows true dependencies; both introductions open with a schematic of the two groups; B's
nonlinear section moved into the discussion.

## Scores after revision round 2 (third independent referee pass)

| Item | A | B |
|---|---|---|
| Flow | 8 | 9 |
| Notation | 8.5 | 8.5 |
| Concept introduction | 8.5 | 9 |
| Graphics / captions | 9 | 9 |
| Math level | 9 | 9 |
| Readability | 8 | 8.5 |
| Publishability | 8 | 8.5 |

The referee's last items were then applied: the penalty sentence (a biased estimator can go below the unbiased floor
only by shrinking towards a prior), the last notation overloads (n_par, φ_j, z_0), the Burgers rate wording, a bridge
at the start of A's nonlinear section, a reader's guide in both introductions, and the 14/5 split in B's abstract.

The referee's main remaining objection was the evidence (one noise draw per benchmark cell). A new experiment answers
it: the grid designs were rerun with three independent seeds (new field and new noise each), 60 inputs. **The method is
right on 60/60 with no false-confident answer; weak SINDy is false-confident on 13/60.** This is now Table
`tab:multiseed` in both papers and is cited in the abstracts. Not rerun: the 400-point scattered design (its
Gaussian-process interpolation needs PyTorch, which this environment could not install).

A's flow and readability stay a point below B's because its section order is your outline by design (nonlinear outlook
between theory and algorithm, limits as their own section).
