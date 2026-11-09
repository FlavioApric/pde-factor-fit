# RECEPIMENTO — S8-VAR

Il recepimento dell'audit S-CHECK-F8-VAR (fix VAR-1…VAR-17) è documentato in `PROOF_PACKAGE.md` §9. La risposta a S8-ENC su VAR-L1 e VAR-P11(e) è in `PROOF_PACKAGE.md` §10. Questo file è nato con il recepimento post-Gate 8.

## post-Gate 8 (27/10/2026)

Fonti: `GATE8.md`; `research/DEVIL/ATTACK-8.md` (O3, O8, O17, O20); `research/CIT-AUDIT/AUDIT-8.md` §5, voce S8-VAR. Regola sugli stati: solo verso il basso. Nessuno stato è stato alzato.

### Obiezioni di ATTACK-8

| obiezione | cosa chiede | dove è applicata | effetto sullo stato |
|---|---|---|---|
| O3 (MAJOR) | ritirare la F5 di DEVIL-6; in H = −∂² + x² la rottura a cos t = 0 esiste; VAR-T10-F è FALSO solo nella forma indicata; normalizzazione unica H = −∂² + x² | PP Convenzioni (paragrafo «Normalizzazione unica dell'oscillatore»); PP §4.3, fine del paragrafo «Correzione rispetto a F6»; LEDGER riga VAR-T10-F (colonna ipotesi) | invariato: VAR-T10-F FALSO solo nella forma «si rompe al tempo della lente/Fourier»; la frase F6 su cos t = 0 resta VERA |
| O8 (MAJOR) | VAR-P3 è una stima di modulo, non un certificato di robustezza | PP §1.6, enunciato (paragrafo «Natura del risultato»); LEDGER riga VAR-P3; nuova domanda VAR-Q19 in `open_questions.md` (obiettivo per la Fase 9, non un claim) | qualificato: «DIMOSTRATO come stima di modulo; non è un certificato di robustezza in DM2» |
| O17 (MINOR) | nell'enunciato di VAR-T1 sul caso V(t,x) aggiungere «fuori dalle fasce di silenzio, in (SF)» | PP §1.5, enunciato (i), paragrafo «Lettura»; LEDGER riga VAR-T1(c) | invariato (DIMOSTRATO (i)–(iii)); VAR-T1(c)-Q10 resta APERTO |
| O20 (MINOR) | VAR-L2-cor non va citato da righe DIMOSTRATO finché non è auditato | controllato: nessuna riga DIMOSTRATO di `LEDGER_ROWS.md` lo cita; vincolo ricordato in PP §11 e nella nota in testa a LEDGER_ROWS | VAR-L2-cor resta DA AUDITARE; lo audita S-CHECK-F8-VAR dopo questo recepimento |

### Correzioni di CIT-AUDIT-8 §5 (S8-VAR)

| punto | correzione | dove è applicata |
|---|---|---|
| 1 | Hörmander, ALPDO I (2ª ed.), Thm 8.6.5 confermato; tolto «numero da verificare» | PP §1.3, Osservazione (Holmgren); uscito dalla lista dei numeri non verificati (PP §8 punto 8, `open_questions.md`) |
| 2 | Saut–Scheurer 1987 (JDE 66, 118–139) è parabolico; per il tipo Schrödinger citare Isakov 1993 (JDE 105, 217–238, n = 1, attraverso x = costante); stato PROBABILMENTE NOTO | PP §1.3, paragrafo «Letteratura»; PP §6 riga VAR-L1; LEDGER riga VAR-L2 |
| 3 | «Pöschl–Teller» → «Pöschl–Teller modificato (iperbolico)», con Z. Phys. 83 (1933) 143–151 | PP §3.3, nota di terminologia in testa; LEDGER righe VAR-P8(c), VAR-P8(d) |
| 4 | Crum → Q. J. Math. 6(1) (1955) 121–127, DOI 10.1093/qmath/6.1.121; Crum, Casas, SLZ e Hörmander 8.6.5 escono dalla lista dei numeri non verificati | PP §3.3 (fine di (c)); PP §8 punto 8; LEDGER riga VAR-P8(c); `open_questions.md` |
| 5 | Folland cap. 4 per Stone–von Neumann è dubbio (forse cap. 1): da controllare; Pazy cap. 5 e van der Put–Singer 1.27/1.34 restano non verificati | PP §4.3 (3)(iii); PP §8 punto 8; `open_questions.md` |
| 6 | DOI di SLZ 10.1016/j.jsc.2011.08.001 | già presente in PP §2.4 (fix VAR-12); nessuna modifica |
| 7 | Mehler (VAR-T10): citare DLMF 18.18.28 | PP §4.3 (3)(iii), formula di U(t) |

### Note

- Nessuno script SymPy è stato modificato o rilanciato: le correzioni sono di enunciato e di citazione.
- Copia del PROOF_PACKAGE prima di questo recepimento: nella scratchpad della sessione (non nel progetto); il diff è limitato ai luoghi elencati sopra e alla nuova §11.
- Il contesto del Gate 8 (RT-IDV ATTIVA, RT-ODE-GAL ristretta a C3-Q2 generale, RT-NA PARCHEGGIATA) non cambia nessun claim di questo pacchetto; i trigger di RT-NA restano VAR-Q8, VAR-Q11, VAR-Q18.
