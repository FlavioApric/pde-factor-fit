# PLAN — PR-C2e (Asse 4 S1–S15 + deliverable trasversali PR-C2.1, PR-C2.4, PR-C2.5)

Data: 2026-10-22 · Agente: PR-C2e · Fonte: `D:\piano di ricerca.md` §1.3-C2-EXT, §1.3-C2-TAX, card schema, PR-C2, Phase 1 · Notazione: `NOTAZIONE.md` · Protocollo: `PROTOCOLLO.md` (Regole 1–4).

## 1. Domande (dal piano + aggiunte motivate)
- Q1 (Asse 4): per ciascun attributo S1–S15 (che raggruppa C2.17 e C2.17′–C2.76′): definizione breve, valori ammessi quando è usato come COLONNA delle schede (card schema, campo (6)), rilevanza per G★ (★/◆/▲/■/●/◇/○ e perché).
- Q2 (PR-C2.1): file di tassonomia con tutti i 120 item (C2.1–C2.60, C2.17′–C2.76′), ciascuno collocato UNA sola volta; conteggio verificato (Asse 1: 41, Asse 2: 8, Asse 3: 5, Asse 4: 66 → 120). Controllo che nessun item sia doppio/mancante (script di conteggio sul testo del piano, solo come controllo).
- Q3 (PR-C2.4): indice incrociato item ↔ classi di nuclei condivise (calore/gaussiana, d'Alembert/onde viaggianti, Airy, Schrödinger/Fresnel, Bessel, armoniche/Poisson, esponenziali-polinomi, Lévy α-stabili/Mittag-Leffler, Green/risolventi, solitoni sech², …).
- Q4 (PR-C2.5): matrice delle componenti = lista dei termini elementari (∂_t, ∂_t², ∂_x, ∂_x², ∂_x³, ∂_x⁴, x·, f(x)·, reazione c·u, nonlocale |ξ|^α, frazionario in t, u u_x, u², |u|²u, sin u, …) × famiglie (T1–T12 + Asse 2), con simbolo e classe di nucleo del singolo termine. È la lista richiesta da A6.
- Q5 (aggiunta): quali attributi S separano i casi in cui il quadro additivo/moltiplicativo/log-simbolo (§1.2-2, G1–G3) si applica (commutatività, coefficienti costanti, invarianza per traslazione) — cioè quali colonne decidono E_int.

## 2. Skill (Regola 2) — ordine e uso
1. `scientific-agent-skills\skills\paper-lookup\SKILL.md` (Read) — verifica dei riferimenti standard (Evans, Hörmander, Polyanin, DLMF, Olver, Kato, Pazy, …).
2. `academic-research-skills\deep-research\SKILL.md` (Read) — workflow di ricerca/sintesi applicato a mano (nessun subagente: blocco tassonomico, non serve fan-out). `anthropic-skills:deep-research` non invocata perché coordina subagenti; dichiarato.
3. `scientific-agent-skills\skills\scientific-critical-thinking\SKILL.md` (Read) — controllo critico della classificazione (collocazioni ambigue, doppi conteggi, attributi non ortogonali).
4. `scientific-agent-skills\skills\citation-management\SKILL.md` (Read) — `sources.bib`.
Nessuno script `_vendor` eseguito.

## 3. Fonti / stringhe
Evans *PDE*; Hörmander *ALPDO I–II*; Courant–Hilbert II; Polyanin *Handbook of Linear PDEs*; Polyanin–Zaitsev *Nonlinear PDEs*; DLMF; Olver *Lie groups*; Pazy *Semigroups*; Kato *Perturbation theory*; Whitham *Linear and nonlinear waves*; Treves; Taylor *PDE I–III*; Samko–Kilbas–Marichev; Podlubny; Ablowitz–Clarkson; Guenther–Lee; Myint-U–Debnath; MIT 18.03/18.303.
Stringhe: "classification of PDE principal symbol", "fundamental solution constant coefficient Malgrange Ehrenpreis", "pseudo-differential symbol |xi|^alpha fractional Laplacian kernel", "Mittag-Leffler time-fractional diffusion fundamental solution", "heat kernel Feynman-Kac semigroup".

## 4. Scambi (grafo)
- PR-C2b ↔ PR-C2e: DOMANDA su termini/attributi delle famiglie T2–T9; integro le loro schede (`research/PR-C2b/cards`).
- PR-C2a, PR-C2c, PR-C2d: DOMANDA sui termini delle loro famiglie.
- → R3: TABELLA con la matrice delle componenti.
- Inbox `inbox/PR-C2e.md` letta: inizio (vuota), metà, prima della consegna.

## 5. Criterio di "fatto"
- `TAXONOMY.md`: 120 item, ciascuno una volta, conteggio per asse verificato; S1–S15 con definizione/colonna/rilevanza.
- `cross_index.md`: ≥10 classi di nuclei con gli item che le condividono.
- `components_matrix.md`: ≥20 termini elementari × famiglie, con simbolo e nucleo del termine isolato.
- `REPORT.md`, `sources.bib`, `open_questions.md`; `DONE PR-C2e` in `inbox/central.md`.
