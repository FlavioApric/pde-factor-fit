# MAP of the whole repository

```mermaid
flowchart LR
  subgraph main
    m1[paper: structure A/B, explained] --- m2[code/pdefactor] --- m3[tests + benchmarks]
  end
  subgraph analytical
    a1[paper: 130 pp + all proofs 263 pp] --- a2[code/verification, lean] --- a3[claude/proofs: ledger, packages]
  end
  subgraph ml-layers
    l1[paper: every layer, what worked / failed] --- l2[code/pdefactor/learned] --- l3[benchmarks: ll_* experiments]
  end
  subgraph model-expansion
    e1[paper: ladder, routes, specification] --- e2[code: examples L6..L10] --- e3[claude/notes: full spec]
  end
  a1 -->|theorems used by| m1
  l2 -->|calls| m2
  e2 -->|extends| m2
```

| branch | read first | code | tests / benchmarks |
|---|---|---|---|
| `main` | `paper/structure_B.pdf` | `code/pdefactor/` | `tests/`, `benchmarks/` |
| `analytical` | `paper/analytical.pdf`, `paper/analytical_proofs.pdf` | `code/verification/`, `code/lean/` | `tests/test_verification.py` |
| `ml-layers` | `paper/ml_layers.pdf` | `code/pdefactor/learned/` | `tests/test_learned*.py`, `benchmarks/` |
| `model-expansion` | `paper/model_expansion.pdf` | `code/ex_*.py`, `code/out_of_class_inject.py` | `tests/test_examples.py` |

Every branch has the same skeleton: `paper/ code/ tests/ [benchmarks/] claude/`; `claude/` holds all markdown, `PROVENANCE.md` (where each file came from) and a map. The file/dependency graphs of the old and the new repository are in `claude/graph/` (rebuild with `code/tools/build_graph.py`); `claude/INVENTORY.md` compares them.

## History
The raw research history of the earlier repository is kept privately. Everything of value from it (papers, code, tests, benchmarks, plans, reports, audits) is in the four branches; `claude/INVENTORY.md` proves it.
