# tools: graphs of the repository and the old-vs-new inventory

```bash
# graph of this repository (all four branches must exist locally)
python tools/build_graph.py --name new --repo . --refs main analytical ml-layers model-expansion --out graphs
# compare with the stored graph of the earlier research repository (graphs/graph_old.json)
python tools/compare_graphs.py --old graphs/graph_old.json --new graphs/graph_new.json --out INVENTORY.md --csv inventory.csv
```

`build_graph.py` writes `graph_<name>.json` (every file and folder as a node; edges for containment, LaTeX `\input`/`\bibliography`/`\includegraphics`, Python imports, and file-path mentions in documents and scripts),
a directory-level Mermaid overview (`.mmd`) and an interactive HTML view (`.html`, loads vis-network from a CDN).
`compare_graphs.py` matches every file of the old graph to the new one (identical content after line-ending and path normalisation, moved, or modified) and classifies what is missing as *expected*
(build junk, logs, backups, caches, toolchain binaries, private notes, session reports) or a **real gap** (papers, code, tests, benchmarks, Lean, theory documents, small data); it exits with status 1 while a real gap exists.
The migration helper that placed the files is `import_old.py` and is not needed to use the repository.
