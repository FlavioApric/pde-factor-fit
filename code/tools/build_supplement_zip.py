"""Build code_and_data.zip for the SIMODS supplementary materials.

    python build_zip.py <repo> <example_run_dir> <out_dir>

Copies the parts of the repository needed to run the algorithm and reproduce the paper's numbers and figures,
the worked-example run (report + images), a README and CONTENTS.txt, then zips the folder.
"""
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

repo, run, out = (Path(a) for a in sys.argv[1:4])
root = out / "code_and_data"
if root.exists():
    shutil.rmtree(root)
root.mkdir(parents=True)

import io
import tarfile

# tracked files exactly as stored in git at HEAD (byte for byte), never the working copy
PATHS = ["code/pdefactor", "code/experiments", "benchmarks", "tests", "claude/benchmark_tables",
         "pyproject.toml", "LICENSE", "CITATION.cff"]
tar_bytes = subprocess.run(["git", "-C", str(repo), "-c", "core.autocrlf=false", "-c", "core.eol=lf", "archive", "--format=tar", "HEAD", *PATHS],
                           capture_output=True, check=True).stdout
with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as tf:
    for m in tf.getmembers():
        if m.isfile() and not m.name.endswith((".pkl", ".pyc")) and "__pycache__" not in m.name:
            dest = root / m.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(tf.extractfile(m).read())

ex = root / "example_run"
ex.mkdir()
for f in sorted(run.iterdir()):
    if f.suffix in (".md", ".json", ".png", ".npz"):
        shutil.copy2(f, ex / f.name)

commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
readme = f"""# Code and data for "Groups Are Factors: Learning Linear PDEs by Clustering Modes on the Factors of the Symbol"

Author: Flavio Pricoco. Supplementary material for the SIMODS submission.

This is a snapshot of the repository https://github.com/FlavioApric/pde-factor-fit at commit `{commit}`
(branch `simods-submission`, the version that produced the paper). Later versions of the code are maintained in the
repository. Code licence: MIT (`LICENSE`).
`CONTENTS.txt` lists every file.

## What is here

| folder | contents |
|---|---|
| `code/pdefactor/` | the complete algorithm (Python package `pdefactor`, entry point `pdefactor.loop.run_loop`) |
| `example_run/` | the worked example of Section 4.1 (transport + diffusion, 64 x 128 grid, 5 % noise, benchmark protocol): `report.md` (everything the run decided, readable), `report.json` (the same, machine readable), five images explained in SM5.1 |
| `benchmarks/` | benchmark scripts and every stored per-input result; `out/large.jsonl` is the large benchmark of Section 4.2 (one row per random equation: true factors, both methods' answers, runtimes) |
| `claude/benchmark_tables/` | the benchmark tables (`large.md`: Table 2; `p8_final_v5.md`: Table 3). The folder keeps its repository name so that the scripts run unchanged |
| `code/experiments/` | experiment scripts and the scripts that draw the paper's figures from the stored results |
| `tests/` | the test suite (pytest) |

## Install (Python 3.12 or newer)

```
pip install -e ".[dev]"
python -m pdefactor.demo            # simulates an equation, runs the algorithm, prints the answer (under a minute)
pip install -e ".[dev,baselines]"   # only for the benchmarks: adds PySINDy and PyDMD for the baselines
```

## Reproduce

```
# worked example of Section 4.1 (report + images, as in example_run/; a few minutes)
python code/experiments/worked_example.py --case transport_plus_diffusion --noise 0.05 --out my_run

# large benchmark of Section 4.2 (300 random equations; resumable; hours on several cores)
python benchmarks/bench_large.py --seeds 0-59 --noises 0.01 --workers 6
python benchmarks/large_report.py   # writes claude/benchmark_tables/large.md

# development benchmark (Table 3): rebuild the table from the stored rows in benchmarks/out
python benchmarks/p8_report.py
# ... or rerun the inputs themselves (all cases, designs and noise levels of the benchmark harness)
python benchmarks/bench_e2e.py --workers 6
# independent repetitions of the grid designs (Table 3, column "independent")
PDEFACTOR_FIELD_SEED=1 python code/experiments/multiseed.py --out ms.jsonl --workers 4 --methods pipeline weak_sindy

# figures of the paper from the stored results, typeset for the SIAM page (writes paper/figures/simods/)
mkdir -p paper/figures
python code/experiments/make_figs_simods.py
```

## Using the algorithm on your own data

```python
import numpy as np
from pdefactor.loop import run_loop

t = np.linspace(0, 2, 64)                              # times, shape (nt,)
x = np.linspace(0, 2*np.pi, 128, endpoint=False)       # positions, periodic, shape (nx,)
u = ...                                                # data, shape (nt, nx)
res = run_loop([u], t, x, sigma=0.01)                  # sigma: noise standard deviation
print(res.label, res.equation())
print(res.summary())
```
"""
(root / "README.md").write_text(readme, encoding="utf8", newline="\n")

# CONTENTS.txt: every file, by folder (as `ls -R1F` would list it), with sizes
lines = ["Contents of code_and_data.zip (every file, by folder; sizes in bytes)", ""]
for d in sorted([root] + [p for p in root.rglob("*") if p.is_dir()]):
    files = sorted(p for p in d.iterdir() if p.is_file())
    if not files:
        continue
    lines.append(f"{d.relative_to(out).as_posix()}/:")
    lines += [f"    {f.name}  ({f.stat().st_size})" for f in files]
    lines.append("")
(root / "CONTENTS.txt").write_text("\n".join(lines) + "\n", encoding="utf8", newline="\n")

z = out / "code_and_data.zip"
if z.exists():
    z.unlink()
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for p in sorted(root.rglob("*")):
        if p.is_file():
            zf.write(p, p.relative_to(out).as_posix())
n = sum(1 for p in root.rglob("*") if p.is_file())
print(f"{n} files, zip {z.stat().st_size/1e6:.1f} MB")
