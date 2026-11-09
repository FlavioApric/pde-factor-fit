# KA OPF5D-T3+L6 — aggiudicazione (S-CHECK-17, 26/10/2026)
Input: KA_OPF5D_T3_input.md (solo enunciati, ipotesi, prove). Attacco: KA_OPF5D_T3_attack.md (subagente fresco, nessun contesto). Aggiudicatore: S-CHECK-17, che ha anche ricontrollato ogni passo a mano.

**Esito: SOPRAVVISSUTO.** L'attacco non trova obiezioni FATALI né MAJOR. Ho verificato le obiezioni residue una per una.

| punto dell'attacco | verdetto | motivazione / riparazione |
|---|---|---|
| T3 "R ≡ 0, cioè b ≡ 0" copre solo k > 0, mentre L6 usa b(−k) = 0 | **fondato, MINOR** (= F5D-1) | Per v reale e k reale vale ψ_±(−k) = conj ψ_±(k), quindi b(−k) = conj b(k). Una riga da aggiungere in T3 prima di invocare L6. |
| L4: stime di Cauchy uniformi in x ≥ x_0 non seguono dalla stima di L3(i), che cresce con |x| | **fondato, MINOR** (= F5D-3) | Basta usare L3(iii): |m_+ − 1| ≤ e^{∫|v|/|k|} − 1 è uniforme in x, su un disco attorno a iκ che non tocca 0. |
| T3: l'enunciato normalizza q_{d*} = Π(λ − 4κ_j²), la prova trova 4^{−N}Π | fondato, cosmetico (= F5D-2) | Riscalare d*. |
| L3(ii): convergenza della serie derivata solo abbozzata | fondato, presentazione (in F5D-4) | Il conteggio n·C^{n−1}/(n−1)! è standard; va scritto in una riga. |
| L6: la notazione κ := −k collide con κ_j | cosmetico (= F5D-5) | Rinominare. |

Ho controllato in modo indipendente tutti e cinque i punti di CHECK_REQUEST, nell'ordine (a)–(e), e reggono. Il punto che ho controllato con più cura è la continuità di Ψ in k = 0 nel caso w(0) = 0. w è C¹ sul semidisco chiuso e analitico all'interno, quindi il suo differenziale in 0 è C-lineare, perché le equazioni di Cauchy–Riemann passano al bordo per continuità. Ne segue |w(k)| ≥ |k| vicino a 0.

**Controllo indipendente V-ex** (sympy/s17_crum_novikov.py → .out):
- N = 2 (κ = 1, 2): 11/11 OK. Il controllo copre:
  - l'intreccio di Crum LA = AL_0;
  - Novikov K_{d*} = 0 con q_{d*} = Π(λ − 4κ_j²);
  - l'assenza di relazioni di grado < N;
  - P = A∂A^T monico d'ordine 2N+1 con [P, L] = 0;
  - il simbolo di A → Π(ik ∓ κ_j) a ±∞, cioè R = 0 e poli di T in iκ_j;
  - l'uguaglianza fra il v di Crum e l'N-solitone di Hirota con k_j = 2κ_j.
- N = 3 (κ = 1, 2, 3): 6 controlli OK (intreccio, a_1, a_2, Novikov, indipendenza). Poi il run è stato interrotto dal timeout di 9 minuti durante il calcolo di [P, L].

**Stato dopo l'aggiudicazione:** L3–L8 e T3 sono OK con fix MINOR (F5D-1…F5D-5) e il kill-argument è sopravvissuto. Stato proposto: **DIMOSTRATO**, previo recepimento dei fix MINOR.
