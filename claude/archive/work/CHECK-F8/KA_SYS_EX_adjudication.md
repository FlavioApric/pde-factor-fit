# KA SYS-EX — aggiudicazione (S-CHECK-F8-SYS, 27/10/2026)

Attacco: `KA_SYS_EX_attack.md`, scritto da un subagente indipendente che ha letto solo `KA_SYS_EX_input.md`. Esito dichiarato dall'attaccante: **WOUNDED (lieve)**, nessun controesempio all'enunciato.
Verifica dell'aggiudicatore: ho rifatto a mano tutti i passi della prova (SYS-L0, SYS-L1, SYS-N1, EX-L1, EX-L2, Passi 1–3) prima di leggere l'attacco; dettagli in `AUDIT_S8-SYS.md` §2.

## Punti dell'attacco

**P1 — Riduzione del Passo 2 ai soli primi p ⊇ q (attacco principale, proposto MAJOR).**
*Accusa.* La prova del Passo 2 rimanda a SYS-T1 e, alla lettera, ignora i primi incomparabili con q (esempio M = R/m_0 ⊕ R/m_1, relazione a + b e^x = 0).
*Verdetto: answered_by_current_text (fuori dall'estratto), con fix di presentazione.* L'estratto che ho preparato non conteneva la prova di SYS-T1 (PROOF_PACKAGE §1, riga 24), che fa esattamente la riduzione richiesta: si sceglie un elemento non nullo z ∈ ker φ ∩ E con annullatore **primo** q (esiste perché Ass(ker φ ∩ E) ≠ ∅). Scrivendo z = Σ c_{p,j} x_{p,j} con c_{p,j} ∈ R/p, si ha Ann(z) = ∩_{c_{p,j} ≠ 0} p, perché ogni R/p è un dominio. Da ∩ p = q segue che ogni p presente contiene q, e che q stesso è presente (q contiene il prodotto dei p, quindi uno di essi). Nell'esempio dell'attaccante z = a x_0 + b x_1 ha annullatore m_0 ∩ m_1, che non è primo; moltiplicando per g ∈ m_1 ∖ m_0 si ottiene l'elemento g(0) a x_0 ≠ 0 del nucleo, con annullatore m_0 e un solo addendo. Quindi i primi incomparabili non compaiono mai. La riparazione alternativa dell'attaccante (q minimale tra i primi con r_{q,j} ∉ q e h_0 nel prodotto di tutti gli altri primi presenti) è anch'essa corretta.
*Severità effettiva:* **MINOR** (la prova esiste nel pacchetto, ma il Passo 2 deve essere autosufficiente): fix **SYS-1(a)**.

**P2 — Ω vuoto (MINOR).** Corretto e banale: con Ω = ∅ si ha 𝒜 = 0. Va scritto "Ω aperto connesso non vuoto". Fix **SYS-1(b)**.

**P3 — h_0 ∘ s non identicamente nulla sulla palla reale (MINOR).** Corretto: il testo dice "non nulla su U", mentre serve "non identicamente nulla su B_{q,j}", che segue da EX-L2(b) in forma contrapposta. Lo zero set di una funzione reale-analitica non identicamente nulla su una palla connessa ha misura nulla. Fix **SYS-1(c)**.

**P4 — EX-L2(b), densità di Zariski (MINOR).** Accolto. La via più breve è dimensionale: se r ∉ q, V(q) ∩ V(r) ha dimensione d − 1 e non può contenere l'aperto s(U), che è una varietà complessa di dimensione d. Fix **SYS-1(d)**.

**P5 — Riferimenti per Δ e per il rivestimento (MINOR, bibliografico).** Accolto: la numerazione di Shafarevich resta da verificare (CIT-AUDIT-8).

**P6 — SYS-L1, finitezza ed essenzialità (MINOR).** Standard e corretto: una somma diretta di sottomoduli non nulli in un modulo noetheriano è finita; ogni sottomodulo non nullo contiene una copia di R/p con p associato. Nessun fix necessario, al più una riga.

**P7, P8 — attacchi non riusciti (Ω non convesso o illimitato, 𝒟′, più copie dello stesso primo, primi annidati, q = 0, d = n, primi massimali in V(q)).** Concordo con l'attaccante: nessun difetto. Ho verificato in particolare che il Passo 3 non usa l'iniettività di C^∞(Ω).

**P9 — SYS-EX-C: E(R/p)^N addendo diretto (MINOR).** Accolto: (R/p)^N ↪ I con I iniettivo implica E(R/p)^N ↪ I come addendo diretto, quindi μ_p(I) ≥ N. Fix **SYS-12**.

## Riepilogo
Punti: 9. answered_by_current_text: 1 (P1, con fix di presentazione); accolti come MINOR: 6; non riusciti: 2.

## Verdetto
**SURVIVES** dopo i fix MINOR SYS-1(a)–(d) e SYS-12. Nessun FATAL, nessun CRITICAL, nessun MAJOR matematico su SYS-EX. Resta un problema di **novità** (fix SYS-2, MAJOR di attribuzione): su Ω = ℝ^n l'enunciato è con alta probabilità contenuto in Oberst 1993 (MCSS 6, 264–288), che va citato.
