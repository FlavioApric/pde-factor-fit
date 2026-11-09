#!/usr/bin/env python3
"""Check that every relative link in README.md and the top-level markdown files of claude/ points to an existing file.
Usage: python code/tools/check_links.py   (from the repository root).  Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT."""
import re,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
bad=0
for md in [root/'README.md']+[f for f in sorted((root/'claude').glob('*.md')) if f.name!='REPO_MAP.md']:
    for m in re.finditer(r'\]\(([^)#\s]+)(?:#[^)]*)?\)',md.read_text(encoding='utf-8')):
        t=m.group(1)
        if re.match(r'(https?:|mailto:)',t): continue
        p=(md.parent/t).resolve()
        if not p.exists():
            bad+=1; print(f'{md.relative_to(root)}: broken link {t}')
    # paths written in backticks that look like repository files
    for m in re.finditer(r'(?<!\[)`((?:paper|code|tests|benchmarks|claude)/[\w./-]+\.(?:pdf|tex|py|md|csv|json|html))`(?!\]\()',md.read_text(encoding='utf-8')):
        t=m.group(1)
        if not (root/t).exists():
            bad+=1; print(f'{md.relative_to(root)}: missing file {t}')
print('links ok' if not bad else f'{bad} problems'); sys.exit(1 if bad else 0)
