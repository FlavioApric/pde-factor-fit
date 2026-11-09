# RECEPIMENTO dell'audit — S8-DICT (27/10/2026)

**Fonti dell'audit:**
- `work/CHECK-F8/AUDIT_S8-DICT.md`, di S-CHECK-F8-DICT;
- `work/CHECK-F8/KA_DICT_N1_{input,attack,adjudication}.md`, kill-argument indipendente su N1, esito SURVIVES-WITH-FIXES;
- `work/CHECK-F8/AUDIT_S8-ENC.md`, per la condizione di R6.

**Formato:** fix → modifica → file/sezione. Nel PROOF_PACKAGE ogni intervento porta l'etichetta "[fix DICT-k]".

## Fix CRITICAL (locali)
- **DICT-2** (definizione di "identificabile"; KA P1, P2, P10) → "identificabile" ridefinito come ker Φ_u = 0, cioè "una legge, se esiste, è unica", con il controesempio u = t alla definizione vecchia. (IV) ora dice "se una legge esiste, non è unica". In (a′) è aggiunta la condizione d ≥ 1 oppure m ≥ 2 per avere K ≥ 2. → PROOF_PACKAGE §2.6 (Quadro, (IV), (a′)); LEDGER_ROWS DICT-RANGO-cor.
- **DICT-3** (V reale e zeri di u; KA P3) → in (b′) con V reale il "⟺" vale solo per u senza zeri. In generale vale solo (⇒), con la condizione iu_t + u_xx = 0 su Z(u) e il problema di divisione (Q3). Aggiunti i controesempi u = x³ e u = e^{−it}(x + x²). → PROOF_PACKAGE §2.6, corollario (b′) V reale; LEDGER_ROWS DICT-RANGO-cor.
- **DICT-4** (U3(d)(ii) con μ({0}) > 0) → prova riscritta: l'atomo in 0 si tiene esattamente come nodo λ_0 = 0, e la stima si fa su μ′ = μ − μ({0})δ_0 (μ′((0, ε_0)) → 0 per continuità dall'alto). L'enunciato resta invariato. → PROOF_PACKAGE §1.4 (ii); `sympy/s8dict_checks3.py` R1; LEDGER_ROWS DICT-U3d.
- **DICT-6** (N1(iii) senza L ∈ Ann(u); KA P5) → aggiunta l'ipotesi "L ∈ Ann(u)" e il passo "(L) ⊂ Ann(u) perché Ann(u) è un ideale". Nella nota sul caso N = 1 sono distinte le due differenze di dimensione (deg L contro deg L − D). → PROOF_PACKAGE §2.3; LEDGER_ROWS DICT-N1iii.

## Fix MAJOR
- **DICT-1** (Teorema A(iii), palle B_k e ipotesi U_0; KA P6) → prova riscritta con M+1 aperti disgiunti non connessi O_m. Ciascun O_m è un'unione di N+1 palline attorno a una (N+1)-upla di punti data dal Lemma ND, con matrice di valutazione invertibile, stabile per piccoli spostamenti. L'ipotesi U_0 è tolta: A(iii) vale per atomi differenziali senza ipotesi aggiuntive. → PROOF_PACKAGE §3.3 (prova di (iii) e nota); §7; LEDGER_ROWS DICT-A-iii; CHECK_REQUEST (aggiornamento); KILL_ARGUMENT_N1 (aggiornamento).
- **DICT-5** (caso magnetico dentro RANGO; KA P4) → caso tolto da RANGO e rinviato a SYS-N3, con la condizione div(|u|²B) = 0 e la formula di δV. Aggiunto il controesempio alla frase vecchia, "campi a divergenza nulla". **Claim nuovo DA AUDITARE: DICT-MAG-NU** (non unicità con B = |u|^{−2}∇^⊥χ), verificato in `sympy/s8dict_checks3.py` R3. → PROOF_PACKAGE §2.6, punto "Sistemi"; §7; LEDGER_ROWS DICT-MAG, DICT-MAG-NU; CHECK_REQUEST, punto 12.

## Fix MINOR
- **DICT-7** (G-R(a)) → il test d'arresto di R1 diventa r_n = dist(D_0u, W_n), calcolato con la Gram del sistema affine aumentato su una base massimale di W_n. È tolto "λ_min(G′_n) > 0 per minimalità". → PROOF_PACKAGE §3.5, Teorema G-R; LEDGER_ROWS DICT-GR.
- **DICT-8** (I-LIM, notazione d e modello per ramo) → d indica il grado minimo, come in CONV-T1(5), e la dimensione è d′. È dichiarato il modello per ramo: esatto in BSS, approssimato come enunciato analitico con ε_opt. → PROOF_PACKAGE §4, "Ramo esatto"; LEDGER_ROWS DICT-ILIM.
- **DICT-9** (NS-T1 e ALG-T1) → la "Conseguenza" è ristretta alle forme evolutive (per esempio u_tt = u_xx + sin u). Per u_xt = sin u il riferimento ad ALG-T1 è tolto. → PROOF_PACKAGE §5.2.
- **DICT-10** (NS-L1, logaritmo globale) → per la direzione w ↦ u è dichiarato Ω semplicemente connesso, oppure u modulo (2πi/λ)ℤ. → PROOF_PACKAGE §5.1.
- **DICT-11** (etichetta di Ax) → "CON-FONTE (verificata, enunciato standard; numero del teorema da verificare)", come in CIT-AUDIT-6 riga 18. → PROOF_PACKAGE §5 (triage), §5.2, §7; LEDGER_ROWS DICT-AX.
- **DICT-12** (U2-a, dipendenza di F) → nota: F dipende da (f, K), e U2 non richiede l'indipendenza. → PROOF_PACKAGE §1.2, Lemma U2-a.
- **DICT-13** (Teorema A(i), topologia D′; KA P7) → l'apertura in D′ è ristretta ad atomi i cui trasposti conservano C_c^∞ (operatori differenziali). → PROOF_PACKAGE §3.3, enunciato e prova di (i).
- **DICT-14** (N1(i), continuità della parametrizzazione; KA P8) → aggiunto il paragrafo "Applicazione alle classi elencate": la continuità va verificata, e con parametri razionali l'esito vale comunque. → PROOF_PACKAGE §2.1.
- **DICT-15** (N1(iv)(c), Σ⁰₂ ∖ Π⁰₂; KA P9) → la frase diventa "verificabile nel limite, non decidibile nel limite, con qualunque successione di regole", allineata a CONV-7; la classe è ridotta a commento. → PROOF_PACKAGE §2.4 (c).
- **DICT-16** ("raro" → "magro"; KA P11) → le u differenzialmente algebriche formano un insieme magro e shy, denso e non raro. → PROOF_PACKAGE §2.5, "Legame con F4-ALG".
- **DICT-17** (R6-T(c), dominio) → (c) è enunciato per u ∈ C^∞(Ω) con D_iu ∈ Y. → PROOF_PACKAGE §3.6 (c).
- **DICT-18** (R6, motivazione dell'esclusione di MF3) → la ragione è sostituita con "liscezza di Wᵗψ in x_0 per q generale non verificata". L'esclusione resta. → PROOF_PACKAGE §3.6, "Cosa non fa".

## Punti del coordinatore
- **N1(vi) FALSO** → registrato come FALSO con enunciato originale e controesempi: u = t + x nella classe u_t = a(t,x)u_x, dove a ≡ 1 è unica; u = t − x² nella classe normalizzata. → PROOF_PACKAGE §2.6bis (nuova) e triage §2; §7; LEDGER_ROWS DICT-N1vi; `sympy/s8dict_checks3.py` R2.
- **Fix del KA su N1** → P1–P11 recepiti tramite DICT-1, 2, 3, 5, 6, 13, 14, 15, 16. → PROOF_PACKAGE §2.8 (paragrafo sul KA indipendente); KILL_ARGUMENT_N1.md (aggiornamento).
- **R6: condizione soddisfatta** → ENC-1, ENC-C1 ed ENC-T2 sono DIMOSTRATO in AUDIT_S8-ENC, che conclude "il cammino critico ENC-1 → ENC-C1 → ENC-T2 → R6 regge". Il Lemma R6-T è mantenuto, con stato proposto DIMOSTRATO e citazione di AUDIT_S8-ENC. Resta una riserva: se S8-ENC modifica ENC-T2 nel suo recepimento, il lemma si riallinea alla segnalazione in inbox/S8-DICT.md. → PROOF_PACKAGE §3.6, "Stato"; §7; LEDGER_ROWS DICT-R6.

## Altri file
- **PROOF_PACKAGE**:
  - intestazione: paragrafo "Audit" con fonti, convenzione delle etichette e stati;
  - §7: tabella riscritta con gli stati proposti dall'audit e i fix per riga.
- **sympy**: nuovo `s8dict_checks3.py` → `.out` **9/9 OK** (R1 DICT-4, R2 N1(vi), R3 DICT-MAG-NU). I check precedenti non cambiano.

## Claim nuovi o cambiati
- **Nuovi:**
  - DICT-MAG-NU (**DA AUDITARE**);
  - §2.6bis, registrazione di N1(vi) come FALSO (non è un claim nuovo).
- **Cambiati nell'enunciato:**
  - DICT-RANGO (definizione di identificabile; (IV); (a′); (b′) V reale);
  - DICT-N1iii (L ∈ Ann(u));
  - DICT-A(iii) (senza U_0);
  - DICT-A(i) (topologia D′ ristretta);
  - DICT-GR (test d'arresto);
  - DICT-NS (conseguenza ristretta a forme evolutive; log globale);
  - DICT-N1iv(c) (formulazione);
  - DICT-R6(c) (dominio).
- **Cambiati solo nella prova:** DICT-U3d(ii).
- **Tolti:** il caso magnetico da RANGO (rinviato a SYS-N3).

---

# Post-Gate 8 (27/10/2026)

**Fonti:**
- `work/CHECK-F8/AUDIT_S8-DICT_rev2.md`, rilievi MAG-1…MAG-5;
- `research/DEVIL/ATTACK-8.md`, rilievi O5, O13, O15, O19;
- `research/CIT-AUDIT/AUDIT-8.md` §5, blocco S8-DICT;
- GATE8.md: RT-DICT è ATTIVA.

Il formato resta fix → modifica → file/sezione. Gli stati cambiano solo verso il basso. Prima della modifica PROOF_PACKAGE è stato salvato nello scratchpad della sessione.

## AUDIT_S8-DICT_rev2
- **MAG-1** (ipotesi, non solo redazione) → A, V ∈ C^∞(J × Ω; ℝ) dipendono da (t, x); U ⊂ J × Ω; χ ∈ C_c^∞(U); ∇, ∇^⊥ agiscono solo nelle variabili spaziali. Il caso statico (A, V indipendenti da t) è coperto solo per u stazionaria e χ = χ(x); per u non stazionaria la non unicità statica non è dimostrata. → PROOF_PACKAGE §2.6, punto "Sistemi" ("Classe", "Caso statico"); LEDGER_ROWS DICT-MAG, DICT-MAG-NU.
- **MAG-2** → l'ipotesi "u ≠ 0 su Ū" è sostituita da supp χ ⊂ {u ≠ 0} (U ⊂ {u ≠ 0}), e si aggiunge u ≢ 0. Se u ≡ 0 ogni coppia è una legge e la non unicità è banale. → PP §2.6 (corollario DICT-MAG-NU, "Ipotesi"); LEDGER_ROWS DICT-MAG-NU.
- **MAG-3** → il "se e solo se" dell'identità delle differenze è enunciato solo per supp B ⊂ {u ≠ 0}. Se supp B incontra Z(u) servono altre due condizioni: un'estensione liscia di δV attraverso Z(u), e B·∇u = 0 su Z(u). Questo caso non è trattato. → PP §2.6 ("Identità delle differenze"); LEDGER_ROWS DICT-MAG.
- **MAG-4** → la tesi diventa "seconda legge reale con campo magnetico diverso" (dB ≢ 0, quindi non un cambio di gauge). La prova è SYS-N3(a)(b), localizzata con k = −|u|²B = −∇^⊥χ, più SYS-N3(c) (principio del massimo, sulle fette per n ≥ 3). → PP §2.6 (corollario, "Tesi" e "Prova").
- **MAG-5** → in R6-T(f) la citazione di ENC-T2(c) è sostituita da DICT-N1(ii) e dal Teorema A. La prova di (f) è riscritta: la triangolarità viene da W = I + Volterra, che conserva i dati di Cauchy; la non certificabilità viene da N1(ii) con A(iii) per atomi differenziali. Anche (H-dato) non cita più ENC-T2(c). Nel paragrafo "Stato" è aggiunta la conferma di rev2. → PP §3.6 ((H-dato), (f), prova di (f), "Stato"); LEDGER_ROWS DICT-R6.

## ATTACK-8
- **O19** → coincide con MAG-5, recepito come sopra.
- **O15** → DICT-MAG-NU non è più un claim autonomo: è il **corollario di SYS-N3(c)** nel caso di u con zeri fuori da supp χ. Il punto dichiara che la riga canonica è SYS-N3, con la condizione div_x(ρ²B) = 0 (non div B = 0). → PP §2.6; §7; LEDGER_ROWS DICT-MAG-NU ("nessuno stato autonomo").
- **O13** → nel Teorema G-R l'etichetta "(ID)" diventa "(H-ID)", in due punti: l'ipotesi e (b). Una nota dice che è l'ipotesi d'unicità di NOTAZIONE, nella forma esatta a livello n ≥ n_0. → PP §3.5; §7; LEDGER_ROWS DICT-GR.
- **O5** → nuovo paragrafo "Significato e ipotesi" prima del Teorema RANGO:
  - "identificabile" significa ID-ker;
  - l'unicità della legge vale solo sotto (H-ex), cioè se una legge esiste;
  - controesempio u = t + sin x nella classe u_t = a u_xx + b u, con a, b costanti.
  → PP §2.6; §7 (righe RANGO "come ID-ker"); LEDGER_ROWS DICT-RANGO, DICT-RANGO-cor.

## CIT-AUDIT-8 §5
1. **Boman** → Math. Scand. 20 (1967) 249–268, DOI 10.7146/math.scand.a-10835. È tolto "numero di pagina da verificare"; l'enunciato resta CON-FONTE. → PP §1.2 (Fonti); §7 DICT-U2; LEDGER_ROWS DICT-U2.
2. **Ax** → *On Schanuel's conjectures*, Ann. of Math. (2) 93(2) (1971) 252–268, DOI 10.2307/1970774. **Declassamento:** "CON-FONTE verificata" diventa "CON-FONTE da leggere", perché il teorema differenziale non è stato letto. → PP §5 (triage), §5.2; §7 DICT-AX; LEDGER_ROWS DICT-AX.
3. **Christensen** → Israel J. Math. 13(3–4) (1972) 255–260. → PP §2.5; §7 DICT-N1v; LEDGER_ROWS DICT-N1v.
4. **Trefethen–Weideman** → il Thm 5.1 è dichiarato "CON-FONTE non letta"; numero e costante sono da controllare sulla fonte. → PP §1.4 (iii); §7 DICT-U3d; LEDGER_ROWS DICT-U3d.
5. **U2-a** (facoltativo, fatto) → aggiunta la frase "versione locale di KMS 18.16 sull'intorno 𝒱 di 19.10". → PP §1.2 (commento); LEDGER_ROWS DICT-U2.

## Altri file
- PROOF_PACKAGE: paragrafo "Post-Gate 8" nell'intestazione.
- LEDGER_ROWS: stessa nota nell'intestazione.
- CHECK_REQUEST: sezione "Aggiornamento post-Gate 8", con il punto 12 chiuso da rev2.
- Nessuno script nuovo. Le verifiche di MAG-NU restano `sympy/s8dict_checks3.py` R3 e `work/CHECK-F8/sympy/dict2_mag.py` (16/16).

## Stati
- **Scesi:**
  - DICT-AX, da "CON-FONTE verificata" a "CON-FONTE da leggere";
  - DICT-RANGO e DICT-RANGO-cor, da "DIMOSTRATO" a "DIMOSTRATO come ID-ker, unicità solo sotto (H-ex)";
  - DICT-MAG-NU, da "DA AUDITARE" a "corollario di SYS-N3(c), senza stato autonomo".
- **Non alzati:** rev2 propone DIMOSTRATO per DICT-MAG-NU dopo MAG-1 e MAG-2. Qui lo stato non è alzato: decide il coordinatore.
- **Invariati:** DICT-R6 (DIMOSTRATO, solo la citazione cambia) e DICT-GR (DIMOSTRATO, solo l'etichetta cambia).

## Claim nuovi o cambiati
- **Nuovi:** nessuno.
- **Riformulati:**
  - DICT-MAG / MAG-NU: ipotesi MAG-1 e MAG-2, "se e solo se" ristretto, corollario;
  - R6-T(f): stessa tesi, nuova prova da N1(ii) e Teorema A, da controllare in modo leggero;
  - RANGO: significato dichiarato.

---

# Controllo di R6-T(f) (27/10/2026)

**Fonte:** `work/CHECK-F8/AUDIT_S8-DICT_R6f.md`, esito PASS-con-fix: due fix MINOR, script `dict3_r6f.py` 8/8.

- **R6f-1** (luogo e giustificazione della triangolarità):
  - Modifica: l'enunciato (f1) dice "nei punti (t, x_0)" e nota che in x_1 ≠ x_0 la triangolarità non vale, perché W non è locale.
  - Nella prova il "quindi" dalla conservazione dei dati di Cauchy è sostituito dall'argomento O(|x − x_0|^{m+1}): se j^{m−1}f(x_0) = 0, allora j^m(Vf)(x_0) = 0. Poi linearità e commutazione con ∂_t.
  - → PROOF_PACKAGE §3.6, enunciato e prova di (f1).
- **R6f-2** ("a nessun livello" contro "al livello n"): applicate entrambe le opzioni.
  - (f2): enunciato e prova al livello n, con il Teorema A(iii) e N1(ii)(b).
  - (f2′): enunciato "a nessun livello", con il passo di Baire: Z è l'intersezione dei nuclei dei dati, F_n il fit omogeneo, chiuso per A(ii) e con interno vuoto in u + Z per A(iii); l'unione numerabile è magra.
  - → PROOF_PACKAGE §3.6 ((f2), (f2′) e prove).
- **Stato:**
  - R6(f): DIMOSTRATO **proposto** da AUDIT_S8-DICT_R6f dopo R6f-1 e R6f-2. La registrazione spetta al coordinatore.
  - R6(a)–(e): invariati.
  - → PROOF_PACKAGE §3.6 "Stato", §7; LEDGER_ROWS DICT-R6.
- **Claim nuovi:** nessuno. (f2′) è il passo indicato dall'audit, scritto per esteso.
