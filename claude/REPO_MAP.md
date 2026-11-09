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

## Graphs
The file/dependency graph of this repository and of the earlier research repository are in `graphs/` (`graph_new.json`, `graph_old.json`, `.mmd` overviews, `.html` interactive views); `INVENTORY.md` compares them. Rebuild with `tools/build_graph.py`.

## History
The raw research history of the earlier repository is kept privately. Everything of value from it (papers, code, tests, benchmarks, plans, reports, audits) is in the four branches; `INVENTORY.md` proves it.
