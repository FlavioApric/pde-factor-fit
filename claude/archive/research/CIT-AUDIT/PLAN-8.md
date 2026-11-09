# PLAN-8 — CIT-AUDIT-8 (Fase 8, fonti citate nei PROOF_PACKAGE, LEDGER_ROWS e RECEPIMENTO di S8-*, e negli audit di CHECK-F8)

Data: 2026-10-27 · Agente: CIT-AUDIT-8 · Precedenti: AUDIT-6 (metodo, esiti, gradi), PLAN-5 (formato). Bibliografia di riferimento: `sources_verified.bib`.

## 0. Ambito
- `work/S8-{SYS,VAR,CONV,ENC,DICT}/{PROOF_PACKAGE,LEDGER_ROWS,RECEPIMENTO}.md` (RECEPIMENTO esiste solo per ENC e DICT; nessuna sessione ha un `sources.bib`).
- Fonti citate in `work/CHECK-F8/AUDIT_*.md` e nei file `KA_*` dello stesso cartella.
- Raccolta: grep sui nomi d'autore e sugli anni nei file sopra (346 righe), poi lettura dei passi.

## 1. Esiti e gradi (come AUDIT-6)
Esiti: **VERIFICATO** / **DATI CORRETTI** / **CONTENUTO DIVERSO** / **NON TROVATO** / **PARZIALE** (metadati sì, enunciato o numero no). Gradi di lettura: (primaria) / (abstract) / (secondaria) / (memoria, non conta come verifica). Mai inventare volumi, pagine o numeri.

## 2. Lista con priorità

### Priorità A (portanti, o segnalate dal mandato o dagli audit)
| # | voce | usata in | cosa verificare |
|---|---|---|---|
| A1 | Oberst 1993, MCSS 6, 264–288 | SYS-EX, SYS-N1, SYS-T0 (prior art, fix SYS-2) | metadati; abstract; se possibile testo: definizione di μ(S), enunciato principale, caso μ(S) ≤ 1 ↔ zoccoli ≤ 1; rischio di novità |
| A2 | Oberst 1990, Acta Appl. Math. 20, 1–175 | SYS-EX Passo 3 (iniettività di C^∞(ℝ^n)), SYS-T1 | metadati (già in AUDIT-6); pp. 24–36; numeri di Bass di C^∞ |
| A3 | Oberst 1995, AAECC (*Variations on the fundamental principle*) | SYS §1 (prior art possibile) | metadati, abstract |
| A4 | Schindelar–Levandovskyy–Zerz 2011 | SYS-R1, VAR-VMPUM | metadati, titolo, abstract; delta SYS-R1 e VAR delta (1)–(4) |
| A5 | KMS 1993, 18.16 e 19.x | DICT-U1, U2 | 19.1 e 19.10 già verificati (AUDIT-6); 18.16 dichiarato non usato: controllare che cosa è |
| A6 | Holmgren e unicità laterale (Hörmander I Thm 8.6.5; Saut–Scheurer 1987; Isakov 1993) | VAR-L1, VAR-L2, VAR-T1 | metadati; enunciato di Saut–Scheurer; contenuto di Isakov 1993 |
| A7 | Casas 2007, J. Phys. A 40 | VAR-T10(4), CONV contratto (B) | Thm 3.4, raggio π, normalità in dimensione infinita |
| A8 | Pöschl–Teller (1933) e Crum 1955 | VAR-P8(c)(d), ENC-A9(b4), ENC-K1′ | metadati; attribuzione |
| A9 | Duistermaat–Grünbaum 1986 (+ Wilson 1998) | ENC-K1 | enunciato con V → 0 (già CONTENUTO DIVERSO in AUDIT-6: controllare il recepimento); Wilson 1998 metadati |
| A10 | Marchenko 1986 cap. 1; Povzner 1948; Levitan 1987 | ENC-1 | numero del teorema sul nucleo simmetrico; metadati |
| A11 | Bluman–Shtelen 1996 §2 | ENC-P0′-DIC, ENC tabella | classe V = α(t)x² + β(t)x + γ(t); condizione T′ = 1/ρ² (Schwarziana) |
| A12 | Reed–Simon II (essenziale autoaggiuntezza su 𝒮; §X.12) | ENC-P0′ (esempi), (H-P0) | teoremi di essenziale autoaggiuntezza applicabili a −∂² + x² e −∂² + Fx su 𝒮; §X.12 = sistemi di evoluzione |
| A13 | Mehler (formula / nucleo) | ENC-A9(b3), VAR-T10 | fonte citabile (Mehler 1866; DLMF 18.18) |
| A14 | Avron–Herbst 1977 | ENC-P0′, NS-EQ-Ω, errata F6 | metadati; normalizzazione della formula |
| A15 | Einkemmer–Ostermann 2015; Dang–Einkemmer–Ostermann 2025 | CONV-Q6 | abstract; norma e ordini |
| A16 | Ax 1971 | DICT-AX (NS-EXPALG) | metadati; enunciato (teorema in campi differenziali) |
| A17 | Wei–Norman 1963/1964 | VAR (contesto Lie), AUDIT_S8-VAR | metadati di entrambe le voci |
| A18 | VMPUM (definizione) | VAR §2.4 | che VMPUM sia di SLZ 2011 (o di Zerz/Levandovskyy precedenti) |

### Priorità B (CON-FONTE dichiarate, non portanti per stati DIMOSTRATO)
Malgrange exp. 246 Thm 3.2(2) p. 83 (CONV-D2); Palamodov 1970 cap. VII e Hörmander per 𝒟′ (CONV-Q17); Stein 1970 cap. VI §3.1 Thm 5 (CONV-T4(b)); Pazy cap. 5 / Phillips 1953 (VAR-P11(e)); Kato (domini comuni); Folland 1989 cap. 4 (Stone–von Neumann); van der Put–Singer 1.27/1.34 (VAR-T6); Matsumura §18, Matlis 1958 (SYS-T1); Andrianov–Sokolov 2003, Sokolov 0903.2835 (ENC-K1′); Niederer 1973 (lente); Wu–Yang 1975, Aharonov–Bohm 1959 (G-T2); Boman 1967 (DICT-U2); Slovák 1987/1988; Trefethen–Weideman 2014 Thm 5.1; Christensen 1972; Hunt–Sauer–Yorke 1992; Caffarelli–Silvestre 2007; Weiss–Tabor–Carnevale 1983, Weiss 1984; Owhadi 2017; Thaller 1992 cap. 5; Hochbruck–Lubich 2003; Moan–Niesen 2008.

### Priorità C (già verificate in audit precedenti; solo ricontrollo dei dati come scritti in F8)
Peetre 1959/60; Eisenbud–Huneke–Vasconcelos 1992; Sun 1993; Nakamura–Sun–Uhlmann 1995; Radford 1996; Booth–Legg–Jarvis 2001; Morozov 1966; Engl–Hanke–Neubauer 1996; Mathé–Pereverzev 2003; Chen–Billings–Luo 1989; Bagby–Bos–Levenberg 2002; Pinkus 1985; Prenter 1970; Kelly 1996 (rinvio tolto in CONV-7); Nečas 1967, Grisvard 1985.

## 3. Strumenti
Crossref API (`/works?query.bibliographic=`, `/works/<DOI>`), OpenAlex (abstract), arXiv API, Numdam, WebSearch/WebFetch per indici editoriali e secondarie. PDF ad accesso aperto letti con pdftotext nello scratchpad. Nessuno script `_vendor`. Paywall, 403 e pagine vuote non valgono come conferma.

## 4. Consegne
1. Questo file.
2. `AUDIT-8.md`: tabella per voce (esito, metadati verificati con fonte, contenuto rispetto all'uso, correzione con file e claim); sezione «rischio di novità»; elenco finale di correzioni per sessione (S8-SYS … S8-DICT), da girare dopo il Gate 8.
3. Voci verificate in coda a `sources_verified.bib`, marcate `% F8`.
4. Riga `DONE CIT-AUDIT-8` con i conteggi in `inbox/central-F6.md` (append).

Scrivo solo in `research/CIT-AUDIT/` e `inbox/` (append).
