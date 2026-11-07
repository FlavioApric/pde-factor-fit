# MAP of the whole repository

```mermaid
flowchart LR
  subgraph main
    m1[paper A / B] --- m2[src/pdefactor] --- m3[tests + benchmarks]
  end
  subgraph analytical
    a1[paper: proofs] --- a2[proofs/lean] --- a3[claude/notes: claims, routes]
  end
  subgraph ml-layers
    l1[paper: what worked / failed] --- l2[src/pdefactor/learned] --- l3[benchmarks: ll_* experiments]
  end
  subgraph model-expansion
    e1[paper: beyond linear constant coefficients] --- e2[examples L6..L10] --- e3[claude/notes: ladder, routes]
  end
  a1 -->|theorems used by| m1
  l2 -->|calls| m2
  e2 -->|extends| m2
```

| branch | read first | code | tests / benchmarks |
|---|---|---|---|
| `main` | `paper/B_proposed_structure/main.pdf` | `src/pdefactor/` | `tests/`, `benchmarks/` |
| `analytical` | `paper/analytical/main.pdf` | `proofs/`, `verification/` (symbolic checks) | Lean in `proofs/lean`, `tests/` |
| `ml-layers` | `paper/ml_layers/main.pdf` | `src/pdefactor/learned/` | `tests/test_learned*.py`, `benchmarks/` |
| `model-expansion` | `paper/model_expansion/main.pdf` | `examples/`, `benchmarks/out_of_class_inject.py` | `tests/test_examples.py` |

Each branch has `claude/CLAUDE.md` (rules), `claude/MAP.md` (graph), `claude/STATUS.md` (worked / did not work).

## History
The raw research history (all earlier sessions, logs, backups) is kept on the branches `archive/analytical`, `ml`, `other`, `larned-layers`, `final-report`, `phase4-ml-plan` until it is archived elsewhere. Nothing there is needed to use the repository.
