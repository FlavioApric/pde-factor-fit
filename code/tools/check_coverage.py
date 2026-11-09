#!/usr/bin/env python3
"""Check that everything of an old LaTeX edition is present in a new document.

    python check_coverage.py --old OLD1.tex OLD2.tex ... --new NEW1.tex NEW2.tex ...

Compares (1) proof tags \\led{...}, (2) titles of theorem-like environments, (3) labels (ignoring a leading 'f:'),
(4) section/subsection titles, (5) 'Dim. An/Bn' references. Exit status 1 if something of the old text is missing.
Part of pde-factor-fit (c) 2026 Flavio Pricoco, MIT.
"""
import argparse,re,sys
def read(fs): return "\n".join(open(f,encoding="utf-8",errors="replace").read() for f in fs)
def norm(s): return re.sub(r"[^a-z0-9]+"," ",re.sub(r"\\[a-zA-Z]+\*?","",s.lower())).strip()
def tags(t):
    out=set()
    for m in re.finditer(r"\\led\{([^}]*)\}",t):
        for x in re.split(r"[,;/]\s*",m.group(1)):
            x=x.strip()
            if x: out.add(x)
    return out
ENV=r"(?:theorem|proposition|lemma|definition|corollary|example|falsebox)"
def envs(t):
    out=set()
    for m in re.finditer(r"\\begin\{"+ENV+r"\}\s*(?:\[\{?|\{)((?:[^{}\]]|\{[^{}]*\})*)",t):
        title=re.sub(r"\\(led|proved|openq|condl|falsest|modulo|pw|cf|vex|edmark)\b(\{[^}]*\})?","",m.group(1))
        n=norm(title)
        if n: out.add(n)
    return out
def labels(t): return {re.sub(r"^f:","",l) for l in re.findall(r"\\label\{([^}]*)\}",t)}
def heads(t): return {norm(m.group(2)) for m in re.finditer(r"\\(chapter|section|subsection|subsubsection)\*?\{((?:[^{}]|\{[^{}]*\})*)\}",t) if norm(m.group(2))}
def dims(t): return set(re.findall(r"Dim\.~?([AB][0-9]+)",t))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--old",nargs="+",required=True); ap.add_argument("--new",nargs="+",required=True)
    ap.add_argument("--ignore-heads",action="store_true"); ap.add_argument("--show",type=int,default=15)
    a=ap.parse_args(); o,n=read(a.old),read(a.new); bad=0
    for name,f in (("proof tags",tags),("theorem titles",envs),("labels",labels),("headings",heads),("Dim. references",dims)):
        if name=="headings" and a.ignore_heads: continue
        so,sn=f(o),f(n); miss=sorted(so-sn); bad+=len(miss) if name!="headings" else 0
        print(f"{name}: old {len(so)}, missing in new {len(miss)}"+("" if not miss else "  e.g. "+"; ".join(miss[:a.show])))
    return 1 if bad else 0
if __name__=="__main__": sys.exit(main())
