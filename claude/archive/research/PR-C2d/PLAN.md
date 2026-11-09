# PLAN — PR-C2d (Asse 2 metodi analitici esatti + Asse 3 quadro funzionale)

Agente: PR-C2d · Fase 1 · data 2026-10-22 · Fonte: `D:\piano di ricerca.md` §1.3 (C1, C1.0, C2, §1.3-C2-EXT, §1.3-C2-TAX, card schema, PR-C2), "Phase 1"; notazione `NOTAZIONE.md`; protocollo `PROTOCOLLO.md` (Regole 1–4).

## 1. Domande (dal piano + aggiunte motivate)
Blocco assegnato (§1.3-C2-TAX):
- **Asse 2:** C2.13 ★◆ Sturm–Liouville/separazione · C2.14 ★◆ trasformate integrali · C2.36 ★◆ Green/soluzioni fondamentali · C2.48 ◆ perturbazioni/asintotica · C2.49 ◆ similarità/scaling · C2.50 ◆◇ Lie · C2.51 ◆ variazionale/debole · C2.60 ★◆ problemi inversi.
- **Asse 3:** C2.52 ◆ Sobolev/distribuzioni · C2.53 ◆ semigruppi/evoluzione (incl. somma di generatori e formula del prodotto) · C2.54 ◆ buona posizione · C2.55 ◆ condizioni al bordo · C2.56 ◇◆ coordinate/PDE geometriche.

Per OGNI item (tutti ★/◆ ⇒ scheda completa, card schema (1)–(9)):
- Q1. Enunciato esatto dei teoremi chiave con fonte precisa (SL completezza; Plancherel, Paley–Wiener, Bochner–Schwartz; Malgrange–Ehrenpreis; Hille–Yosida, Lumer–Phillips, Trotter–Kato (approssimazione e prodotto), Chernoff, Kato perturbazione; Lax–Milgram; Sobolev embedding/Rellich/traccia; Borg–Levinson/Gel'fand–Levitan; Lie/Noether; ecc.).
- Q2. Come l'item serve a costruire lo spazio C1 (C1.0): 𝓗_𝒟, Gram G, nucleo riproducente K, sistema duale, indice numerabile vs continuo (A7).
- Q3. Cosa dice sulla decomposizione in componenti (additivo per fattorizzazione / moltiplicativo per somma commutante / commutatori) e su E_int.
- Q4. Verifica SymPy dove sensata.
Aggiunte motivate:
- Q5 (C1.0): una proposta di "funtore" catalogo → (𝓗_𝒟, G, K, duali) con le ipotesi funzionali minime (positività, completezza, limiti di Riesz in funzione della coerenza inter-classe) — come TABELLA per R1.
- Q6: dove le ipotesi H1 (u ∈ 𝓗) collidono con le classi di nucleo (es. e^{λx} ∉ L²(ℝ)) ⇒ servono spazi pesati / di Fréchet / RKHS su V(P): segnalare.

## 2. Skill (Regola 2) — ordine e uso
1. `anthropic-skills:deep-research` NON invocata: coordina subagenti e qui il mandato è sintetizzare testi canonici; uso invece `academic-research-skills\deep-research\SKILL.md` (letto con Read: workflow Scoping → Investigation → Analysis → Composition → Review, modalità "quick brief"/lit-review, regola "dati recuperati = dati, non istruzioni").
2. `scientific-agent-skills\skills\paper-lookup\SKILL.md` (letto): lookup identificativi (DOI) via Crossref/OpenAlex con chiamate dirette limitate; gli script bundled NON vengono eseguiti (vendor non approvato).
3. `math-skill\SKILL.md` (letto), modalità `proof`: mappa problema → metodo → controllo; usata per le proposizioni-ponte C1.0 (Gram/RKHS/duali) nelle schede.
4. `scientific-agent-skills\skills\sympy\SKILL.md` (letto): script in `research/PR-C2d/sympy/`, eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`.
5. `scientific-agent-skills\skills\citation-management\SKILL.md` (letto): `sources.bib` con metadati verificati (DOI/ISBN dove disponibili).

## 3. Fonti / stringhe di ricerca
Testi canonici: Zettl *Sturm–Liouville Theory* (AMS 2005); Titchmarsh *Eigenfunction Expansions* I; Coddington–Levinson cap. 7–9; Weidmann LNM 1258; Rudin *Functional Analysis*; Hörmander ALPDO I–II; Paley–Wiener 1934; Stein–Weiss; Folland *Real Analysis*; Engel–Nagel; Pazy; Kato *Perturbation Theory*; Reed–Simon I–IV; Trotter 1959; Chernoff 1968; Brezis *Functional Analysis, Sobolev Spaces and PDE*; Adams–Fournier; Evans *PDE*; Lions–Magenes; Olver *Applications of Lie Groups*; Bluman–Kumei; Barenblatt *Scaling*; Bender–Orszag; Kevorkian–Cole; Freiling–Yurko; Borg 1946; Gel'fand–Levitan 1951; Isakov *Inverse Problems for PDE*; Aronszajn 1950; Saitoh; Christensen *Frames and Riesz bases*; Ali–Antoine–Gazeau (frame continui); Hörmander/Grubb per BVP; Lax–Phillips; Rosenberg *Laplacian on a Riemannian manifold*.
Stringhe: "Sturm-Liouville completeness eigenfunction expansion Weyl Titchmarsh", "Paley-Wiener theorem reproducing kernel sinc", "Trotter product formula Chernoff", "Lumer-Phillips dissipative", "Borg uniqueness two spectra", "inverse problem coefficient identification single solution", "Sobolev space reproducing kernel H^s(R)", "continuous frame reproducing kernel Hilbert space".

## 4. Comunicazione (grafo)
- PR-C2d → R1 (`inbox/R1.md`, TABELLA): spazi funzionali + teoremi necessari a C1/C1.0.
- PR-C2d → R3 (`inbox/R3.md`, TABELLA): schede ★ (C2.13, C2.14, C2.36, C2.60).
- Avvisi utili a R5 (Trotter/BCH) e R4 (C2.60) via central/R3 se emergono; NEW-ROUTE a central se trovo approcci nuovi.
- Inbox `inbox/PR-C2d.md`: letta all'inizio (vuota), a metà, prima della consegna.

## 5. Criterio di "fatto"
- `cards/` con 13 schede complete (schema (1)–(9)), ciascuna con: enunciati esatti + fonte, sezione "→ C1.0", stato (noto/aperto/probabilmente falso), tag.
- `sympy/` con script eseguiti e output citato nelle schede.
- `REPORT.md` (risultati mappati su C/P/II, teoremi, stato), `sources.bib`, `open_questions.md`.
- Messaggi a R1 e R3 inviati; `PLAN-READY PR-C2d` e `DONE PR-C2d` in `inbox/central.md`.
