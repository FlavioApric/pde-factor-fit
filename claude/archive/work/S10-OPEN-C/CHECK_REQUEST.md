# S10-OPEN-C — CHECK_REQUEST (27/10/2026)

Richiesta di audit per S-CHECK. Le prove sono in `PROOF_PACKAGE.md` (§1–§17). Sono tutte prove scritte DA AUDITARE: nessun claim è dichiarato DIMOSTRATO da questa sessione.

## 0. Verifiche eseguite
`D:\ProblemaBase\.venv\Scripts\python.exe -I work/S10-OPEN-C/sympy/s10openc_checks.py` → **34/34 OK**. Lo script fa solo controlli, nessuna prova dipende da esso.

| test | contenuto | § |
|---|---|---|
| T1 | residuo telescopico della serie di Tychonoff | 3 |
| T2 | sup ℓ^{−k}e^{−ℓ^{−4}} = (k/4e)^{k/4} | 3 |
| T3 | Euler ZXZ di Dirac numerico, residuo ≤ 10^{−17} | 7 |
| T4a, T4b | g_1, g_2 polinomiali fino a t^9; identità formale fino a t^6 | 7(a) |
| T5a, T5b | sizigie di Maxwell; minore τ²(τ² − \|ξ\|²)² | 9 |
| T6a–e | A_1 senza polo, A_2 con polo 1/(2ξ), stesso Jordan e stesso polinomio caratteristico | 8 |
| T7 | C(t) = sin(nt)/n | 2 |
| T8a–c | tr M = −26/5, det M = 1, segmento | 5 |
| T9a–g | Darboux: segno L_0χ = V_1χ, nucleo, residuo 4/u² di 1/u, encoder inverso con ψ − φ = 0 | 12 |
| T10 | (∂_t − ∂_x)f(x + t) = 0 | 6 |
| T11a–c | u″/u = 4/x^6 − 6/x^4 → ∞, piattezza | 15 |
| T12a–c | atomi di media | 16 |
| T13 | errore L¹ ≤ stima (J = 4, 8, 12, 16; stima quasi esatta, dominata dalla coda E_1(Λ)) | 14 |
| T14a–c | scala del bump ε^{1/3} | 17 |

## 1. Claim da auditare, con i punti delicati

| ID proposto | § | punti delicati per l'auditor |
|---|---|---|
| VAR-P11(e) | 1 | D1: la derivata di F nel Lemma C (convergenza dominata, uniforme in t). D2: il passo di Gronwall con il doppio integrale. D3: la catena L2-cor ← P11(e) usa davvero solo B ∈ C¹(𝓛(L²))? |
| VAR-Q18-CE | 2 | D4: la soluzione esplicita è mite? Va controllata la seconda componente con il segno del prodotto scalare. D5: ‖B(t) − B(t′)‖ ≤ 2‖f(t) − f(t′)‖. |
| VAR-Q10-EX | 3 | D6: stima Gevrey 3/2 di B dalla §7.1 di S8-VAR (costante θ = 1/10). D7: e^{−ℓ^{−4}/2} ≤ ℓ su (0, 1]. D8: convergenza delle serie derivate in t (fattore ((k + j)!)^{7/4}). D9: int Z = ∅ richiede I = (0, 1), non ℝ, perché fuori da [0, 1] g ≡ 0. |
| VAR-Q17(a) | 4 | D10: VAR-L2-cor sull'intervallo traslato (η, T − η): le ipotesi sono invarianti per traslazione temporale? D11: φ̌(H)ψ_0 ∈ D(H_0) richiede D(H) = D(H_0) (V_0 limitato). |
| VAR-P12(d)-CE | 5 | D12: «propagatori uguali a meno di fase ⇒ stessa azione di coniugazione» (Stone–von Neumann). D13: l'esempio esce dalla classe V ∈ L^∞; va giudicato se conta come risposta a (d). |
| VAR-C3Q2-R | 6 | D14: additività del rango su un dominio di Ore non commutativo. D15: f(x + t) non D-finita (Wiman–Valiron, CON-FONTE). D16: GKdim(A_2/A_2L) = 3. |
| SYS-DIRAC-POL | 7 | D17: Lemma E per parti. D18: raggruppamento dei termini e^{iP_j} uguali a meno di costanti. D19: i tempi devono essere reali. |
| II-T2(b′)-CRIT | 8 | D20: esistenza di basi saturate analitiche (forma di Smith sul DVR). D21: lettura corretta della congettura Q-S8SYS-4. |
| SYS-MAXWELL | 9 | D22: il nucleo libero (argomento gcd con supporti disgiunti). D23: SYS-EX applicato con soc = 0 (≤ 1). |
| ENC-T2(c′)-P | 10 | D24: unicità di Cauchy per p(L_q)f = 0 con f a supporto compatto (q ∈ C^∞, ordine 2deg p). D25: commutatività in S usata per (τ − α)Ru. |
| ENC-Q4-S | 11 | D26: il composto di due operatori di Volterra simmetrici è ancora di Volterra simmetrico. D27: w(t, ·) ≢ 0 per ogni t. D28: confronto con ENC-N1′(v). |
| ENC-Q10-D | 12 | D29: la formula di κ è verificata solo da SymPy (T9g) su un esempio: serve la derivazione a mano. D30: dominio senza zeri di u. |
| DICT-ILIM-Hs | 13 | D31: condizione di cono uniforme per Lipschitz (Adams–Fournier §4.11, numero da verificare). D32: equivalenza delle norme sui polinomi uniforme per rotazioni. |
| DICT-U3d-v | 14 | D33: costante dell'errore di Čebyšëv. D34: pesi di segno qualsiasi accettabili nell'immersione markoviana. |
| DICT-Q3-R | 15 | D35: il controesempio u = e^{−1/x²}1_{x>0} sta nella classe Schrödinger con V reale; Malgrange è CON-FONTE. |
| DICT-Q4-C | 16 | D36: Amitsur CON-FONTE (rango ≤ N per N + 1 operatori). D37: ker D è intersezione di funzionali continui quando D ha rango finito in D′. |
| DM-δ-MINIMAX | 17 | D38: il limite superiore richiede che P3(c) valga per coppie arbitrarie nella classe con ‖V_2‖ ≤ 2M/δ_0. D39: ε_0 e il margine di u_1. |

## 2. Kill-argument interno (passaggio avversariale, REVIEW_UNAVAILABLE per i revisori esterni)

- **§3.** L'obiezione più forte: «Z(u) contiene anche I ∖ (0, 1)». È stata respinta restringendo a I = (0, 1). L'esempio resta valido.
- **§5.** Obiezione: «la classe quadratica non è la classe di P12». Accolta: l'esito (b) è dichiarato solo per la classe quadratica, e il caso L^∞ resta (c).
- **§7(b).** Obiezione: «i tempi potrebbero dipendere da t e da ξ in modo non polinomiale». Fuori dall'enunciato, che riguarda i tempi polinomiali.
- **§11.** Obiezione: «(S) vera ma (C) falsa rende l'esempio inutile per l'encoder cieco». Vero, ed è proprio quello che Q4 chiedeva: un'istanza con (S) non vacua. La lettura è riportata.
- **§16.** Obiezione: «senza Amitsur resta solo il controesempio». Accolta: lo stato proposto è CON-FONTE per la direzione positiva.
