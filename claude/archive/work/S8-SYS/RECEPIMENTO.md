# RECEPIMENTO — S8-SYS
Il recepimento dell'audit F8 (S-CHECK-F8-SYS, fix SYS-1…SYS-13) è in `PROOF_PACKAGE.md` §10. Questo file raccoglie i recepimenti successivi.

## post-Gate 8
27/10/2026. Fonti: `GATE8.md`; `research/DEVIL/ATTACK-8.md` (O15, O21); `research/CIT-AUDIT/AUDIT-8.md` §3 e §5 (correzioni S8-SYS 1–5); messaggio del coordinatore. Tutte le correzioni sono accettate, nessuna è rifiutata. Gli stati in `LEDGER_ROWS.md` cambiano solo verso il basso.

| voce | contenuto | dove applicato |
|---|---|---|
| O21 (DEVIL-8) | SYS-S1-C, parte 𝒟′: ipotesi scritta β(1) ≠ 0 (con supp ρ ⊂ (1, 2)); la prova è confermata corretta e lo stato FALSO resta | PROOF_PACKAGE §3.3 (scelta di β e punto "Con un'altra f"); §9; LEDGER_ROWS SYS-S1-C |
| O15 (DEVIL-8) | SYS-N3: nel riassunto le variazioni B = A′ − A = −k/ρ² soddisfano div(ρ²B) = 0, non div B = 0; DICT-MAG-NU è un corollario di SYS-N3(c) (lo recepisce S8-DICT) | PROOF_PACKAGE §6, SYS-N3(b); §9; LEDGER_ROWS SYS-N3 |
| CIT-AUDIT-8 §5.1 e §3 | Oberst 1993 → MCSS 6(3) 264–288, DOI 10.1007/BF01211623, letto solo nell'abstract; aggiunti Pommaret 2010 (arXiv:0902.2314) Thm 5.2.5 e Macaulay §82. **SYS-EX, SYS-N1 e SYS-T0 su ℝ^n riclassificati NOTI** (rischio di novità altissimo). SYS-T0 è interamente noto (in n = 1 non c'è delta). **Delta dichiarato solo per Ω arbitrario**; costruzione esplicita e lettura come criterio non sono più rivendicate come novità | PROOF_PACKAGE §1 ("Riclassificazione post-Gate 8"), §2 Oss. 5, titolo di SYS-T0, §9; LEDGER_ROWS SYS-EX, SYS-N1, SYS-T0 |
| CIT-AUDIT-8 §5.2 | Oberst 1995 → AAECC 6(4–5) 211–243, DOI 10.1007/BF01235717 | PROOF_PACKAGE §1 |
| CIT-AUDIT-8 §5.3 | Oberst 1990: pp. 24–36 e §2–4 non letti, non citati come verificati | PROOF_PACKAGE §1 (confronto con Oberst 1990), SYS-EX Passo 3 |
| CIT-AUDIT-8 §5.4 | Wu–Yang → PRD 12(12) 3845–3857, DOI 10.1103/PhysRevD.12.3845, tolto "da verificare"; Aharonov–Bohm → 115(3) 485–491 | PROOF_PACKAGE §6, G-T2 "Fonti"; §9; LEDGER_ROWS G-T2 |
| CIT-AUDIT-8 §5.5 | Matlis → Pacific J. Math. 8(3) 511–528; EHV → Invent. Math. 110, 207–235; Matsumura §18: numero ancora da controllare (invariato) | PROOF_PACKAGE §1 (declassamento di SYS-T1), §2 Oss. 4 |

*Note.*
- Oberst 1993 resta "letto solo nell'abstract". Nessuno stato dipende dal suo testo, né da quello di Oberst 1990 o 1995. La riclassificazione NOTO per ℝ^n è prudenziale e segue CIT-AUDIT-8 §3.
- Resta in RT-SYS (GATE8): leggere l'enunciato principale di Oberst 1993 e Oberst 1990 §2–4, per controllare che il caso Ω arbitrario non vi sia già. Fino ad allora il delta "Ω arbitrario" è una dichiarazione, non una novità verificata.
- Non ho rieseguito SymPy: le modifiche sono di testo, ipotesi e citazioni. `sympy/s8sys_checks.py` (32/32 OK) è invariato.
