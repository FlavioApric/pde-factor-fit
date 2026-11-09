# PLAN-9 — CIT-AUDIT-9 (prima del Gate 9)

Data: 2026-10-27 · Agente: CIT-AUDIT-9 · Modello di formato: `AUDIT-8.md`.
Mandato: `GATE8.md` §5 («Prima del Gate 9») e `research/DEVIL/ATTACK-8.md` O6. Scrittura solo in `research/CIT-AUDIT/` e `inbox/` (append).

## 1. Obiettivo

Portare a lettura primaria, quando possibile, le fonti da cui dipendono le rivendicazioni di novità di Fase 8, ed emettere un verdetto di novità con la formulazione esatta del delta per SYS-EX, SYS-N1, SYS-T0 ed ENC-K1′.

## 2. Voci e domanda per ciascuna

| # | fonte | domanda | claim interessati |
|---|---|---|---|
| P1 | Oberst 1993, MCSS 6(3) 264–288 | Contiene «M ↪ 𝒜 ⟺ zoccoli ≤ 1» o un equivalente (μ(S) = max_m dim soc_m)? Su quale insieme di funzioni (ℝ^n, C^∞, 𝒟′, successioni)? Dice qualcosa su Ω ≠ ℝ^n? | SYS-EX, SYS-N1, SYS-T0 |
| P2 | Oberst 1990, Acta Appl. Math. 20, 1–175 | Cogeneratore iniettivo grande; struttura di C^∞(ℝ^n) e 𝒟′(ℝ^n) (Ass, molteplicità); aperti diversi da ℝ^n; dualità | SYS-EX Passo 3, SYS-EX-C, SYS-T1 |
| P3 | Pommaret 2010 (arXiv:0902.2314) Thm 5.2.5 | Enunciato esatto, ipotesi (n-puro? lunghezza finita?), fonti che cita | SYS-EX, SYS-N1 |
| P4 | Isakov 1993, JDE 105, 217–238 | Enunciato del risultato per n = 1 (classe di operatori, regolarità, superficie) | VAR-L0, VAR-L1, VAR-L2 |
| P5 | Saut–Scheurer 1987, JDE 66, 118–139 | Classe di operatori coperta; serve davvero per qualche claim? | VAR-L2 (solo priorità) |
| P6 | Andrianov–Sokolov 2003, NPB 660; Sokolov 2008 (J. Math. Sci. 151; arXiv:0903.2835) | Enunciato di fattorizzazione: ipotesi su q (liscio? complesso?), località, trattamento degli zeri, coefficiente di testa | ENC-K1′ |
| P7 | Wilson 1993, J. reine angew. Math. 442 | Enunciato di classificazione bispettrale; legame con Duistermaat–Grünbaum e V → 0 | ENC-K1 |
| P8 | Voci PARZIALE di AUDIT-8 su cui poggia una riga DIMOSTRATO o CON-FONTE citata in `ALGORITMO_ESTESO.md` | numero di teorema o capitolo | vedi §3 |

## 3. Mappa PARZIALE (AUDIT-8) → righe di `ALGORITMO_ESTESO.md`

| voce AUDIT-8 | sorregge | stato della riga in ALGORITMO_ESTESO | priorità |
|---|---|---|---|
| A2 Oberst 1990 | SYS-EX Passo 3 (iniettività di C^∞(ℝ^n)) | DIMOSTRATO (noto su ℝ^n) | alta, ma coperta da B1 Malgrange (VERIFICATO) |
| A8 Saut–Scheurer | VAR-L2 (solo priorità) | DIMOSTRATO | media (P5) |
| A15 Marchenko | ENC-1 (solo confronto) | DIMOSTRATO | bassa |
| B4 Pazy cap. 5 | VAR-P11(e), VAR-L2-cor, ENC (H-P0) | CON-FONTE | **alta** |
| B5 Folland | VAR-T10(3) (metaplettico, Stone–von Neumann) | DIMOSTRATO | media |
| B6 van der Put–Singer 1.27/1.34 | VAR-T6 | CON-FONTE | **alta** |
| B8 Matsumura §18 | SYS-L1 (solo osservazione μ_p = numero di Bass) | non usata | bassa |
| B12 Niederer | ENC-P0′-DIC (lente) | DIMOSTRATO (forma esistenziale) | media |
| B17 Trefethen–Weideman Thm 5.1 | DICT-U3d (iii) | DIMOSTRATO (prova propria) | media |
| B24 Thaller cap. 5 | FW-1 con V | CON-FONTE | **alta** |
| B26 Moan–Niesen Thm 3 | CONV-T7 contratto (B), VAR-T10(4) | DIMOSTRATO (contratto) | **alta** |
| B29 Engel–Nagel III.1 | CONV-T7 contratto (B), Dyson–Phillips | DIMOSTRATO (contratto) | **alta** |
| B30 Nečas/Grisvard | CONV l.227 (uso generico) | — | bassa |
| B31 Hörmander III 18.1.13 | AUDIT_S8-DICT | — | bassa |
| B32 Kato | ENC l.216 (domini comuni) | osservazione | bassa |
| A21, A22, B2 | non sorreggono righe DIMOSTRATO / CON-FONTE in ALGORITMO_ESTESO | — | fuori ambito |

## 4. Metodo

Come AUDIT-8 §0: esiti VERIFICATO / DATI CORRETTI / CONTENUTO DIVERSO / NON TROVATO / PARZIALE; gradi di lettura primaria / abstract / secondaria / memoria. Metadati da Crossref (`doi.org`, `api.crossref.org`), arXiv, OpenAlex, Numdam, e-periodica, PDF degli autori. Paywall e login non valgono come conferma. PDF solo nello scratchpad della sessione. Nessuno script `_vendor`.

## 5. Consegne

- `AUDIT-9.md`: tabella per voce, sezione «Verdetto di novità» (SYS-EX/N1/T0, ENC-K1′) con la frase del delta da dichiarare nel paper, correzioni per file e claim, provenienza.
- Coda di `sources_verified.bib`: voci verificate, marcate `% F9`.
- `inbox/central-F6.md`: riga `DONE CIT-AUDIT-9`.
