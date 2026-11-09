# tools: graphs of the repository and the old-vs-new inventory

```bash
# graph of this repository (all four branches must exist locally)
python code/tools/build_graph.py --name new --repo . --refs main analytical ml-layers model-expansion --out claude/graph
# compare with the stored graph of the earlier research repository (claude/graph/graph_old.json)
python code/tools/compare_graphs.py --old claude/graph/graph_old.json --new claude/graph/graph_new.json --out claude/INVENTORY.md --csv claude/inventory.csv
```

`build_graph.py` writes `graph_<name>.json` (every file and folder as a node; edges for containment, LaTeX `\input`/`\bibliography`/`\includegraphics`, Python imports, and file-path mentions in documents and scripts),
a directory-level Mermaid overview (`.mmd`) and an interactive HTML view (`.html`, loads vis-network from a CDN).
`compare_graphs.py` matches every file of the old graph to the new one (identical content after line-ending and path normalisation, moved, or modified) and classifies what is missing as *expected*
(build junk, logs, backups, caches, toolchain binaries, private notes, session reports) or a **real gap** (papers, code, tests, benchmarks, Lean, theory documents, small data); it exits with status 1 while a real gap exists.
The migration helper (kept for provenance, it describes the old layout) that placed the files is `migrate_files.py` and is not needed to use the repository.

Other tools in `code/tools/`: `flatten_tex.py` (turns a multi-file LaTeX project into one `.tex` file, embedding the bibliography), `check_coverage.py` (checks that everything of an old LaTeX edition, by proof tag, theorem title, label and heading, is present in a new document), `paper_checks.py` (hygiene and notation checks of the manuscripts).
