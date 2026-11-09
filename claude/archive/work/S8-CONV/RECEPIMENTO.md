# RECEPIMENTO — S8-CONV

## Audit F8 (27/10/2026)
Il recepimento dell'audit S-CHECK-F8-CONV (13 fix, nessuno rifiutato) è registrato in `PROOF_PACKAGE.md` §R, con una tabella fix per fix. Questo file non lo ripete.

## Post-Gate 8 (27/10/2026)
Fonti:
- `GATE8.md`: RT-CONV è ATTIVA. Mori–Zwanzig e R2a sono ELIMINATE come strade; i lemmi CONV-MZ1–MZ3 e CONV-R1 restano.
- `work/CHECK-F8/AUDIT_S8-CONV_T2prime.md`: mini-audit di CONV-T2′, verdetto PASS-con-fix; KA SURVIVES-WITH-FIXES.
- `research/DEVIL/ATTACK-8.md`, O4.
- `research/CIT-AUDIT/AUDIT-8.md` §5, voce S8-CONV.

| fix | origine | dove è applicato (PROOF_PACKAGE) | esito |
|---|---|---|---|
| T2P-1: q ∈ ℝ[t, x], ε ∈ ℝ ∖ {0} | mini-audit T2′ | §1.3′, lemma della famiglia test | applicato |
| T2P-2: stima di interezza (indice di grado e, e^{Σ\|x_i\|²} su ℂ^n, ordini disgiunti) | mini-audit T2′ | §1.3′, passo 3′, "Interezza" | applicato, compresa la parte facoltativa |
| T2P-3: modello dell'identificatore (ψ_K arbitrarie a valori ideali, successo = uscita definitivamente uguale ad Ann(u)); H_k strettamente crescente | mini-audit T2′ | §1.3′, enunciato ("In particolare") e passo 2′.3 | applicato, compresa la parte facoltativa |
| T2P-4 (facoltativo): Q(∂)g₀ al posto di "Qg₀" | mini-audit T2′ | §1.3, passo 1(ii) | applicato |
| T2P-5: §Z, il FALSO di MZ3 cita entrambe le letture | mini-audit T2′ (verifica del recepimento) | §Z | applicato |
| O4: la voce "Magnus (B)" del contratto CONV-T7 diventa condizionata | ATTACK-8 | §9: voce (B), riga Schrödinger con V ∈ C([0, T]; L^∞), e una nota sulla proposizione | applicato. Magnus è (B) solo in dimensione finita, oppure sotto Casas 2007 Thm 3.4 (Y normale) nella rappresentazione d'interazione A_I(t) = e^{iH_0t}V(t)e^{−iH_0t}; altrimenti vale Dyson. La proposizione di composizione non cambia, perché non usa Magnus. Ora il contratto è coerente con VAR-T10(4). |
| CIT §5.1: Casas Thm 3.4, raggio π ottimale (Es. 2), normalità in dimensione infinita; tolto "costante π non letta" | CIT-AUDIT-8 | §9, voce (B) | applicato |
| CIT §5.2: Stein cap. VI §3, Thm 5 (p. 181); tolto "da verificare" | CIT-AUDIT-8 | §2.2(b); riga CONV-T4 di LEDGER_ROWS | applicato |
| CIT §5.3: titolo e riferimento completi di Einkemmer–Ostermann 2015 (SIAM J. Sci. Comput. 37(3) A1577–A1592, DOI 10.1137/140994204); titolo di Dang–Einkemmer–Ostermann 2025; CONV-Q6′ resta aperto | CIT-AUDIT-8 | §6, punti 2 e 3; open_questions CONV-Q6′ | applicato |
| CIT §5.4: nessuna fonte per l'iniettività di 𝒟′(Ω); esclusione mantenuta | CIT-AUDIT-8 | §4.3; open_questions CONV-Q17 | applicato (CONV-D2 resta ristretto a C^∞) |

**Fix rifiutati.** Nessuno.

**Note storiche lasciate invariate.** §0.2 (correzioni da CIT-AUDIT-6) e la tabella di §R descrivono lo stato al momento di quei recepimenti; per esempio, §R riporta ancora Stein "da verificare". Il testo corrente delle prove è quello aggiornato. Anche la richiesta "Casas 2007: costante π" in `CHECK_REQUEST.md` è storica: ha trovato risposta in CIT-AUDIT-8.

**Stati in LEDGER_ROWS.** Solo modifiche verso il basso, o modifiche di testo senza cambio di stato:
- CONV-T2′ resta PROVA SCRITTA. Il mini-audit propone DIMOSTRATO, ma la promozione spetta al coordinatore. Sono compilate le colonne SymPy, proof-checker e kill-argument.
- Il contratto CONV-T7 è annotato con il Magnus condizionato.
- CONV-T4 ha la citazione di Stein verificata.

Nessuno stato è stato alzato.
