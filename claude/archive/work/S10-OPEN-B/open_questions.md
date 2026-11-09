# open_questions — S10-OPEN-B

1. **[GT-u] / (U)** (§7): limitatezza delle costanti di Grunert–Teschl Thm 5.4, (5.20)–(5.21), per k_0 in compatti. Pista: riscrittura di GT §5 con costanti esplicite, oppure lettura di Deift–Zhou (non letta).
2. **INT-Q1 / (R)** (§8): escludere relazioni autonome con origine singolare e forma iniziale in I_PW. Servono i termini sottodominanti dell'asintotica radiativa.
3. **OPF5C-Q1** (§9): limiti inferiori graduati a k = 0 per N generale (K = 2N, 2N−1, 2N−2). δ_4(5) e i casi N = 6 sono non calcolati o in corso.
4. **OPR2-Q3** (§10): realizzabilità degli atomi con zoccolo ripetuto quando M non si spezza su 𝔇. È possibile che 𝓛 abbia un insieme colpitore finito pur con infiniti atomi? Nessun esempio noto.
5. **OPR2-Q2′** (§11): lemma di localizzazione (L), "Fredholm modulo vertici".
6. **Domini non convessi** (§5): per quali Ω la densità di OPF5B-T1 vale? Il controesempio usa un buco. Domande aperte: Ω semplicemente connesso non convesso (stellato rispetto a una palla, OPF5B-C1(d)) e P generale.
7. **L-loc** (§4): nessun controllo numerico con due nascite. Utile un Cole–Hopf con u_0′ con due minimi locali (es. sin x + 0.3 sin 2x) per confermare la forma 2ν log(1/max(|t−t_b|, √ν)).
8. Esistenza globale in 𝒮 per KdV (ipotesi di S10B-T3): CON-FONTE secondaria (KVZ), fonte primaria (Lax 1975, Bona–Smith 1975) non letta.

---

## rev2 (27/10/2026) — aggiornamenti dopo l'audit

- **#1 [GT-u].** La riduzione a (U) è ritirata perché tautologica. Resta APERTO senza riduzione. Fatto mancante: l'errore O(t^{−α}) di GT Thm 5.4 è uniforme per x/t in compatti di x/t ≤ −C. Serve la lettura di Deift–Zhou e di GT §5 con le costanti esplicite. S4ID-P8 e OPR2-P7 dipendono anche da (WP).
- **#2 INT-Q1.** Il ramo T6 è tolto. Per S10B-E8, INT-Q1 equivale a (R): nessuna relazione con parte lineare nulla e forma iniziale in I_PW, mod S4ID-P8, [GT-u], (WP). Per decidere (R) servono i termini sottodominanti dell'asintotica radiativa. La relazione cubica di Airy (OP-O5) è il caso test.
- **#5 OPR2-Q2′.** Per S10B-P11 la questione è ridotta a (L-int) ∧ (L-v) per ogni vertice. Restano aperti tre punti:
  - (a) (L-int): compattezza di P_iχ_0²P_j lontano dai vertici;
  - (b) il trasferimento di OPF5B-P8 (modello del cono, 𝒦 = 0) a (L-v) sul poligono, con gli errori (n_j·∇χ_v)f_j e d_j;
  - (c) gli ordini ≥ 2 e m ≥ 1, non toccati.
- **#6 (precisata, C1-a).** Il controesempio dell'anello vale per ogni m se il complementare contiene, dentro un rettangolo con lati in Ω, un rettangolo coordinato chiuso con interno non vuoto. Per un foro puntiforme vale solo per m = 0, perché δ_p ∉ H^{−1}. Domanda residua: caratterizzare i fori (insiemi di capacità positiva? di misura nulla ma non polari?) per cui esiste u ∈ H^m con u_xy = 0 su Ω e Λ(u) ≠ 0.
- **#7 L-loc.** Per la parte interna alla finestra è chiusa dal V-ex dell'audit (`audit_lloc.py`, seconda nascita t_2 = 1.8370, (I − pred)/ν stabile). Resta aperta l'uniformità tra finestre diverse quando le nascite si accumulano verso t → ∞.
- **Nuova #8 δ_N.** δ_5(2·5) e δ_5(8) aspettano una seconda esecuzione indipendente. N = 6 non è stato eseguito (oltre 3,5 h senza uscita). Serve un algoritmo graduato più efficiente: base di Gröbner pesata incrementale o calcolo in caratteristica p con sollevamento. È escluso ogni apprendimento automatico.
