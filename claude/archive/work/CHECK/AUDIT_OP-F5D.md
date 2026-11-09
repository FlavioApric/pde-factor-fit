# AUDIT OP-F5D — S-CHECK-17 (26/10/2026)
Bersaglio: work/OP-F5D/PROOF_PACKAGE.md, con le priorità di CHECK_REQUEST.md.
Skill caricate: skills-local/session-protocol e skills-local/claim-lifecycle (passi 3–4: proof-checker con revisore = subagente Claude indipendente; kill-argument sul cammino critico). Nessuno script `_vendor` è stato eseguito.
Script propri: work/CHECK/sympy/s17_crum_novikov.py → s17_crum_novikov.out (vedi §3). Kill-argument: KA_OPF5D_{T3,T4,T6}_{input,attack,adjudication}.md.
Contesto consultato: OP-NL/PROOF_PACKAGE.md (OP-L16, OP-P17, OP-P18), OP-NL/sympy/lax_checks.out, S4-TERM/PROOF_PACKAGE.md (S4T-L2, S4T-T3). Il PROOF_PACKAGE e il LEDGER non sono stati modificati.
Politica applicata (coordinatore, 26/10): un fatto residuo con fonte pubblicata, verificata su enunciato e numero di teorema, diventa CON-FONTE (verificata), e il claim che ne dipende può essere DIMOSTRATO modulo quella fonte.

## 1. Verdetti per claim
| claim | verdetto | findings | KA | stato LEDGER proposto |
|---|---|---|---|---|
| OPF5D-T1 (Lax ∀n) | **OK** | — | no (non richiesto) | DIMOSTRATO |
| OPF5D-T2 (ZC ∀n) | **OK** | — | no | DIMOSTRATO |
| OPF5D-R1 (segno n = 0 in OP-P18) | **OK** (confermato) | — | no | correzione recepita: OP-P18 con Ω̃_d |
| OPF5D-L3 | OK con fix MINOR | F5D-4 | sì (in T3) | DIMOSTRATO |
| OPF5D-L4 | OK con fix MINOR | F5D-3 | sì | DIMOSTRATO |
| OPF5D-L5 | OK con fix MINOR | F5D-4 | sì | DIMOSTRATO |
| OPF5D-L6 | OK con fix MINOR | F5D-1, F5D-5 | **sopravvissuto** | DIMOSTRATO |
| OPF5D-L7, L8 | **OK** | — | sì | DIMOSTRATO |
| OPF5D-T3 | OK con fix MINOR | F5D-1, F5D-2 | **sopravvissuto** | DIMOSTRATO (V-ex N = 2 completo, N = 3 parziale: s17) |
| OPF5D-L9 | OK con fix MINOR | F5D-13 | no | DIMOSTRATO (nella classe (Cl)) |
| OPF5D-C1 | **OK** | — | (segue da T3 + L9) | DIMOSTRATO su ℝ in (Cl); su Ω limitato mod (UC), invariato |
| OPF5D-C2 | OK (logica) | F5D-12 | no | CONDIZIONALE [F4⁻] (CON-FONTE secondaria, testo di Kay–Moses non letto); V-ex N = 2 **eseguito** (s17) |
| OPF5D-L10 | OK con fix MINOR | F5D-6, F5D-8 | **sopravvissuto** | DIMOSTRATO |
| OPF5D-L11, L12 | **OK** | — | sì | DIMOSTRATO |
| OPF5D-T4 | OK con fix MINOR | F5D-6, F5D-7 | **sopravvissuto** | DIMOSTRATO a tempo fissato; INT-T2 dinamico mod L9-ZS (da scrivere) e (UC) |
| OPF5D-R2 | **OK** (T4 implica la falsità) | F5D-14 | no | FALSO (forma senza molteplicità), mod [DP] = CON-FONTE secondaria verificata |
| OPF5D-L13 | **OK** (classica) | — | no | DIMOSTRATO |
| OPF5D-P14 | OK con fix MINOR (logica) | F5D-10, F5D-11, F5D-15 | no | **CONDIZIONALE** [GT-u] (non trovata nel testo), [Hm] (CON-FONTE secondaria verificata) |
| OPF5D-P15 | OK (logica) | F5D-11, F5D-15 | no | **CONDIZIONALE** [GT-u], [Hm] |
| OPF5D-T6 | OK con fix MINOR | F5D-9 | **sopravvissuto** | DIMOSTRATO |
| OPF5D-T7 | **OK** | F5D-16 (nota) | no | DIMOSTRATO mod [K-U] = Kružkov 1970, §3 Thm 1, CON-FONTE **verificata sul testo primario** |

Criterio: DIMOSTRATO solo se OK oppure OK con fix MINOR, e, per i claim del cammino critico (T3 + L3–L8, T4 + L10–L12, T6), con il kill-argument sopravvissuto. Per i claim fuori dal cammino critico basta il proof-checker (claim-lifecycle, passo 4). Nessun MAJOR, nessun FALSO.

## 2. Findings numerati
**F5D-1 (MINOR, T3 → L6).** In T3, alla riga «R è continuo su (0,∞) … Λ finito ⟹ R ≡ 0, cioè b ≡ 0», si ottiene b ≡ 0 solo per k > 0. L6, invece, richiede b ≡ 0 su ℝ∖0: nella prova usa ψ_−(−k) = a(−k)ψ_+(k) per k > 0. *Riparazione:* aggiungere «per v reale ψ_±(−k) = conj ψ_±(k) (k reale), quindi b(−k) = conj b(k) e b ≡ 0 su ℝ∖0».

**F5D-2 (cosmetico, T3).** L'enunciato dà q_{d*} = Π(λ − 4κ_j²), la prova dà 4^{−N}Π. *Riparazione:* scrivere «q_{d*} ∝ Π» oppure riscalare d*.

**F5D-3 (MINOR, L4, semplicità).** La frase «stime di Cauchy in k di m_+, uniformi in x ≥ x_0» non segue da L3(i), la cui maggiorazione cresce con |x|. *Riparazione:* usare L3(iii), |m_+ − 1| ≤ e^{∫|v|/|k|} − 1, uniforme in x, su un disco attorno a iκ lontano da 0. Lo stesso vale per ∂_xm_+.

**F5D-4 (MINOR, L3(ii), L5(i); presentazione).**
- (a) In L3(ii) va scritto il conteggio della serie di Volterra derivata: il termine n-esimo è ≤ n·C_x^{n−1}·(…)/(n−1)!.
- (b) In L5(i), il passaggio «|w′(0)||k| + o(|k|) = |w(k)| sul semidisco» usa il fatto che il differenziale di w in 0 è C-lineare. Questo vale perché w è C¹ fino al bordo e analitica all'interno, e le equazioni di Cauchy–Riemann passano al limite. Va detto in una frase.

**F5D-5 (cosmetico, L6).** In «con κ := −k» la variabile collide con κ_j. Rinominare (p.es. k̃ := −k).

**F5D-6 (MINOR, L10, T4, definizione di Λ_m).** «b, ρ continui su ℝ» è falso per ρ quando a ha zeri reali (singolarità spettrali, ammesse da |a|² + |b|² = 1). Controesempio (dall'attacco, verificato): q = ½ sech x reale; per ζ = 0 la matrice di trasferimento è la rotazione di angolo ∫q = π/2, quindi a(0) = 0 e |b(0)| = 1. *Riparazione:*
- in L10 dire «b continuo su ℝ; ρ continuo dove a ≠ 0»;
- definire Λ_m con {ξ : b(ξ) ≠ 0};
- nel caso (⇒) di T4 usare b(ξ)Ω̃_d(ξ) = 0 con b continuo;
- aggiungere «ρ ≡ 0 ⟺ b ≡ 0: uno zero reale di a forza |b| = 1».

La logica della prova resta invariata.

**F5D-7 (MINOR, T4, ultima frase dell'enunciato).** Il passaggio a INT-T2 dinamico (con (UC) e «L9 per ZS, stessa prova») non è scritto. *Riparazione:* enunciare T4 come risultato a tempo fissato (completo) e INT-T2 dinamico come «mod L9-ZS e (UC)». L9-ZS è un'evoluzione standard di a e b (AKNS 1974), da scrivere come L9 in una classe (Cl-NLS).

**F5D-8 (MINOR, L10, «dimensione 1»).** Due soluzioni L²(+∞) indipendenti avrebbero Wronskiano (determinante) costante ≠ 0, che però tende a 0: assurdo. Una riga da aggiungere.

**F5D-9 (MINOR, T6, corollario (6)).**
- Il Θ(√ν) usa S4T-T3(iii). Ho verificato che non usa [F3], ma richiede u_0 ∈ C^∞ non costante e t > t*.
- (v) tramite (vi) richiede u_0 ∈ C².
- E^{mult}_{AB} è definito con S_B, quindi l'uso di v richiede S_B = Lax–Oleinik, cioè T7 mod [K-U].

*Riparazione:* enunciare il corollario con queste ipotesi. Refuso: ‖u_0′‖ senza pedice ∞. La stima principale di T6 vale per u_0 ∈ C¹ (o Lipschitz) e non è toccata.

**F5D-10 (MINOR, P14).** «R è C^∞ su (0,∞) per dati di Schwartz (L3 con tutti i momenti)»: L3 dà solo C¹. Servono le stime analoghe con ∂_k^jD_k(s) ≤ C s^{j+1} e il momento ∫(1+|y|)^{j+1}|v|. Si tratta di un'estensione immediata di L3 (oppure: GT §6 cita che (4.32) implica R ∈ C^l). Va scritta o citata. Ho verificato inoltre la coerenza con la notazione di GT: ν(k_0) = −(1/π)log|T(k_0)| = −(1/2π)log(1 − |R(k_0)|²) (GT (1.5), (5.29)).

**F5D-11 ([GT-u], P14/P15) — NON TROVATA come enunciato.** Ho letto GT sul PDF (arXiv:0807.5041v2): Thm 4.4, Cor 4.5, Thm 5.4, Thm A.6 e §6.
- Gli enunciati citati dal package coincidono parola per parola: ipotesi (4.32) e (5.26), regioni x/t ≥ C e x/t ≤ −C, errori O(t^{−l}) e O(t^{−α}) per ogni 1/2 < α < 1, formule (4.39), (4.40), (5.28)–(5.30).
- Nessun enunciato afferma l'uniformità dell'errore in x. Il Thm A.6 dà l'uniformità **in k** («uniformly in k as long as it stays a positive distance from Σ ∪ {±iκ}»); x entra solo tramite i parametri (k_0, γ^t, contorno).
- L'uniformità in x sui compatti delle regioni è la lettura standard e plausibile, ma resta un'inferenza: [GT-u] rimane un fatto mancante. P14 e P15 restano CONDIZIONALI.
- *Via alternativa segnalata dalla fonte:* GT, Remark 5.5, dice che (5.28) si ottiene derivando (5.27), e che questo passaggio «could be shown as in Deift and Zhou [11]» (Deift–Zhou, Comm. Math. Phys. 165 (1994) 175–191). È una possibile fonte per l'asintotica con derivate (non letta).

**F5D-12 ([F4⁻], C2).**
- Metadati di Kay–Moses confermati da fonti secondarie: J. Appl. Phys. 27 (1956) 1503–1508. Il testo non è stato letto, e l'identificazione «N-solitone di Hirota con k_j = 2κ_j ⟺ potenziale senza riflessione con autovalori −k_j²/4» non è un enunciato di Kay–Moses: richiede in più l'identità Wronskiano/Hirota (Freeman–Nimmo 1983, non letto).
- V-ex eseguito da S-CHECK-17 (s17): N = 2 completo (11/11), N = 3 parziale (6 controlli OK).

Stato: C2 resta CONDIZIONALE[F4⁻] con V-ex N = 2. Non è sul cammino critico: T3 non ne dipende.

**F5D-13 (MINOR, L9).** La regolarità C¹ in t delle soluzioni di Jost, con ∂_tm_± → 0 per x → ±∞ («equazione di Volterra derivata in t … controllata da (Cl)»), è solo abbozzata. *Riparazione:* scrivere la stima. Il termine sorgente ∫D_k(y−x)u_t m dy è maggiorato da (1/|k|)∫_x^∞|u_t|, e ∫(1+|x|)²|∂_tu| è uniforme sui compatti di tempo per (Cl). Basta per k ≠ 0, ed è l'unico caso usato. Non è un difetto logico.

**F5D-14 (R2, controllo della deduzione).** Con [DP] (a = ((ζ−ζ_1)/(ζ−ζ̄_1))², ρ ≡ 0), T4 dà ambiguità di dimensione max(0, M+1−4), cioè 0 in 𝓗_2 e 𝓗_3. La formula senza molteplicità con |Λ| = 2 predice invece M−1 = 1 e 2. La contraddizione è corretta: R2 segue da T4 + [DP]. [DP] è verificata da fonte secondaria pubblicata: Bilman–Buckingham, J. Nonlinear Sci. 2019, §1. Vi si legge che i «multiple-pole solitons» sono soluzioni senza riflessione con una coppia di poli d'ordine m ≥ 2, note «since the original work of Zakharov and Shabat», e generate per m = 2 da una trasformazione di Darboux (soluzione liscia, a decadimento esponenziale). Il testo primario (Zakharov–Shabat 1972; Olmedilla 1987) non è stato letto. Stato: FALSO mod [DP] = CON-FONTE secondaria verificata.

**F5D-15 ([Hm], P14/P15).**
- KVZ letto sul PDF arXiv:1708.05362v1 (pubblicato: GAFA 28 (2018) 1062–1090). A p. 2 si legge che le leggi di conservazione possono essere usate («cf. [26, §3]») per mostrare che, per s ≥ 0 intero, la norma H^s ammette un limite globale nel tempo dipendente solo dalla norma iniziale. Il rif. [26] è **P. D. Lax, «Periodic solutions of the KdV equation», Comm. Pure Appl. Math. 28 (1975) 141–188, §3** (primaria, non letta). Altra primaria plausibile: Bona–Smith 1975 (rif. [3] di KVZ), non letta.
- È un'affermazione dell'introduzione, non un teorema numerato. La valuto CON-FONTE secondaria verificata (enunciato e rinvio esatti).
- Per P14/P15 il fatto bloccante resta [GT-u].

**F5D-16 (T7, [K-U] — VERIFICATA sul testo primario).** Ho letto Kružkov 1970 (Math. USSR-Sb. 10 (1970) 217–243, PDF da mathnet.ru).
- **Definizione 1 (§2, p. 220)**: soluzione generalizzata limitata e misurabile; disuguaglianza (2.1) per ogni costante k e ogni f ≥ 0 liscia a supporto compatto contenuto nell'interno della banda; dato iniziale come limite essenziale in L¹ su ogni palla (2.2).
- **Teorema 1 (§3, p. 223)**: stabilità L¹ sui coni caratteristici, ∫_{S_t}|u − v| ≤ e^{γt}∫_{S_0}|u_0 − v_0|, sotto φ_i, ψ C¹ con φ_{ix_j}, φ_{it} lipschitziane in u.
- Per Burgers (φ = u²/2, ψ = 0) le ipotesi valgono e γ = 0: Teorema 1 ⇒ unicità.
- Le disuguaglianze provate in T7 sono esattamente (2.1) con ψ = 0, e ‖v(t) − u_0‖_∞ → 0 implica (2.2).

T7 è quindi DIMOSTRATO mod [K-U] = Kružkov 1970 Thm 1 (CON-FONTE verificata). Nota: la riga di T7 «testo non letto» va aggiornata.

## 3. Verifiche indipendenti
- **R1** contro work/OP-NL/sympy/lax_checks.out. V_0|_{q=0} = diag(i, 0), quindi la parte a traccia nulla è +(i/2)σ_3. Per n = 1, 2, 3 si ha diag(−2iz, 0), diag(−4iz², 0), diag(−8iz³, 0), cioè parte a traccia nulla −i2^{n−1}ζ^nσ_3. La costante «c indipendente da n» di OP-P18 è quindi falsa a n = 0, e la nota «−i2^{n−1}ζ^n(σ_3 + I) verificata per n = 0..3» di OP-P18 è errata per n = 0. Calcolo diretto: per q_t = iq = T_0 la V costante diagonale deve avere α − β = i, il che fissa la parte a traccia nulla a +(i/2)σ_3. **R1 confermato.**
- **T1, T2**: ricontrollo a mano completo (Q ⇒ 2F′ = −ζJF; [P_g, L] = −2g′L − Jg; telescopio; a′_{n+1} = 2Ja_n = 𝓡K_n; monicità via simmetria di L^n; induzione A′_m = qC_m − rB_m con la cancellazione dei termini in i; parte ζ^0 di −iζ[σ_3, R_n]; T̃_0 = −iq). Nessun errore. Gli output lax_all 34/34 e zc_all 32/32 sono coerenti.
- **s17_crum_novikov.py** (funzioni razionali in e = eˣ, nessun exp simbolico; eseguito con `.venv\Scripts\python.exe -I` e timeout di 9 minuti):
  - N = 2 (κ = 1, 2): **11/11 OK**. Copre:
    - Crum LA = AL_0;
    - a_1 e a_2 come antiderivate;
    - Novikov K_{d*} = 0 con q_{d*} = (λ−4)(λ−16);
    - K_0, K_1 indipendenti;
    - P = A∂A^T monico d'ordine 5 con [P, L] = 0;
    - simbolo di A → Π(ik ∓ κ_j) a ±∞ (R = 0, poli di T in iκ_j);
    - v di Crum = 2∂²log f di Hirota con k_j = 2κ_j (fasi c_1 = c_2 = 3).
  - N = 3 (κ = 1, 2, 3): **6 controlli OK**: A monico, LA = AL_0, a_1, a_2, Novikov con q = (λ−4)(λ−16)(λ−36), K_0..K_2 indipendenti. Poi timeout durante [P, L]; i controlli rimanenti per N = 3 non sono eseguiti.
  - È un V-ex, non una prova. È il controllo che solitons.py non era riuscito a fare.
- **T6**: il controllo numerico dell'attacco (Cole–Hopf su ℝ con quadratura fine) è coerente con burgers_l1 (9 controlli Burgers + 2 ZS = 11/11).

## 4. Bibliografia verificata
| chiave | riferimento completo | cosa è stato verificato | esito |
|---|---|---|---|
| [GT] | K. Grunert, G. Teschl, «Long-time asymptotics for the Korteweg–de Vries equation via nonlinear steepest descent», Math. Phys. Anal. Geom. 12 (2009) 287–324; arXiv:0807.5041v2 (PDF letto, pp. 1–3, 13–17, 21–30) | Thm 4.4 (ipotesi (4.32) con l ≥ 1, regione x/t ≥ C, (4.33)–(4.37), O(t^{−l})); Cor 4.5 ((4.39), (4.40)); Thm 5.4 (ipotesi (5.26) con (1+\|x\|)^6, regione x/t ≤ −C, (5.28) con O(t^{−α}) per ogni 1/2 < α < 1, (5.29), (5.30)); Thm A.6 (uniformità in k); Remark 5.5 | **verificata** (enunciati e numeri coincidono con l'uso in P14/P15). [GT-u]: **non trovata** |
| [Hm] | R. Killip, M. Vişan, X. Zhang, «Low regularity conservation laws for integrable PDE», Geom. Funct. Anal. 28 (2018) 1062–1090, DOI 10.1007/s00039-018-0444-0; arXiv:1708.05362v1 (PDF letto, pp. 1–2, 25–26) | §1, p. 2: limite globale in H^s (s ≥ 0 intero) dipendente solo dal dato, «cf. [26, §3]»; [26] = P. D. Lax, «Periodic solutions of the KdV equation», Comm. Pure Appl. Math. 28 (1975) 141–188 | **verificata come fonte secondaria** (enunciato nell'introduzione, non un teorema numerato); primaria Lax 1975 §3 identificata, non letta |
| [K-U] | S. N. Kružkov, «First order quasilinear equations in several independent variables», Math. USSR-Sb. 10 (1970) 217–243, DOI 10.1070/SM1970v010n02ABEH002156; orig. Mat. Sb. 81(123) (1970) 228–255 (PDF inglese letto, pp. 217–224) | Definizione 1 (§2, (2.1), (2.2)); Teorema 1 (§3, (3.1)): stabilità L¹ ⇒ unicità | **verificata** (fonte primaria) |
| [DP] | D. Bilman, R. Buckingham, «Large-order asymptotics for multiple-pole solitons of the focusing nonlinear Schrödinger equation», J. Nonlinear Sci. (2019), DOI 10.1007/s00332-019-09542-7; arXiv:1807.09058 (PDF letto, pp. 1–3) | §1: esistenza di soluzioni senza riflessione con una coppia di poli d'ordine m («since the original work of Zakharov and Shabat»), costruite per Darboux. Primarie citate: V. E. Zakharov, A. B. Shabat, JETP 34 (1972) 62–69; E. Olmedilla, Physica D 25 (1987) 330–346, DOI 10.1016/0167-2789(87)90107-2 (metadati da repository UCM) | **verificata come fonte secondaria**; primarie non lette. Dalla fonte non risulta citabile esplicitamente l'appartenenza a 𝒮, che è standard (decadimento esponenziale) |
| [F4⁻] | I. Kay, H. E. Moses, «Reflectionless transmission through dielectrics and scattering potentials», J. Appl. Phys. 27 (1956) 1503–1508 | solo metadati (fonti secondarie) | **non verificata** nell'enunciato usato; resta V-ex N = 2 (s17) |
| (via alternativa) | P. Deift, X. Zhou, «Long time asymptotics for integrable systems. Higher order theory», Comm. Math. Phys. 165 (1994) 175–191 | citato in GT Rem. 5.5 per derivare le asintotiche in x | da leggere (possibile chiusura di P14 con derivate) |

## 5. Domande CIT-AUDIT (CHECK_REQUEST)
- **[GT-u]**: non trovata. GT non dichiarano l'uniformità in x. Il Thm A.6 dà l'uniformità in k a distanza positiva dal contorno; §6 dà stime in t sui salti per k_0 fissato.
- **[Hm]**: fonte primaria identificata: Lax, CPAM 28 (1975) §3 (rif. [26] di KVZ); in alternativa Bona–Smith, Phil. Trans. R. Soc. A 278 (1975) 555–601 (rif. [3]). Nessuna delle due è stata letta. Verificata la sola secondaria (KVZ, GAFA 2018).
- **[K-U]**: verificata: Teorema 1, §3, p. 223 (stabilità L¹ ⇒ unicità), con la Definizione 1, §2, p. 220.
- **[DP]**: verificata come fonte secondaria (Bilman–Buckingham 2019); primarie ZS 1972 e Olmedilla 1987 non lette.
- **[F4⁻]**: non trovata nella forma usata; metadati Kay–Moses OK; V-ex N = 2 eseguito.

## 6. Fix richiesti (tutti MINOR o cosmetici)
F5D-1 (simmetria b(−k) = conj b(k)), F5D-2, F5D-3, F5D-4, F5D-5, F5D-6 (ρ → b; ρ ≡ 0 ⟺ b ≡ 0), F5D-7 (INT-T2 dinamico mod L9-ZS), F5D-8, F5D-9 (ipotesi del corollario di T6), F5D-10, F5D-13. In più: aggiornare la colonna SymPy di C2/L6/T3 («V-ex N = 2 eseguito da S-CHECK-17, s17») e la riga di T7 («testo di Kružkov letto: Thm 1 §3»).
