# open_questions — S8-ENC · 27/10/2026

**Q1. ENC-U1 in classi più ampie.** Nella classe con nucleo K ∈ L¹ (q ∈ L¹), o con nuclei non triangolari (I + operatore integrale generale che commuta con ∂_t), gli intertwiner sono ancora solo la retta {T_{k_0}}, moltiplicata per il commutante di L_0? Il caso q ∈ L¹ è CON-FONTE (Marchenko), non dimostrato qui.

**Q2. Limitatezza di W su H^{2k}(J) con costanti esplicite.** L'induzione con (Wf)″ = W(f″) − W(qf) è solo schizzata, e serve per R6 di S8-DICT con norme di Sobolev. Va dimostrata una stima ‖W‖_{H^{2k}→H^{2k}} ≤ C(k, a, ‖q‖_{C^{2k−2}}).

**Q3. ENC-S1.** Trasporto della scomposizione per fattori coprimi in S = ℂ[τ, σ] attraverso φ e C12-T1′. Va scritto esplicitamente, ed è da verificare se lcm(Q, Q̃) pari ammetta una scomposizione coprima che resti pari.

**Q4. Separazione (S) non vuota.** Esiste una classe naturale di potenziali con 𝒮_V ∩ 𝒮_{V′} ≠ {0} per V ≠ V′, con un encoder strutturato per ogni V e con (S) vera? Il candidato sono le classi V(t, x) con fasce di silenzio di VAR-T1(c), dove però per ENC-P0(b) manca l'encoder indipendente dal tempo.

**Q5. E_int A9 per Schrödinger su Ω limitato.** Con condizioni di Dirichlet su J limitato, E^mult(t) = U(t) − U_0^D(t)e^{−itV} ha ancora termine principale (t²/2)[H_0^D, V]? Il commutatore [H_0^D, V] non conserva il dominio di Dirichlet se V′ ≠ 0 al bordo. Da confrontare con P3-T3 e CONV-Q6.

**Q6. ENC-1 in dimensione d ≥ 2.** Non esiste un operatore di Volterra triangolare analogo con nucleo locale (il problema caratteristico non è di Goursat). Strada possibile: operatori di trasformazione per L_q radiali (Bessel), oppure Faddeev a energia fissata (FAD-1 in d ≥ 2, dove la serie non converge sempre).

**Q7. ENC-K1′ globale.** La catena di Darboux locale si estende a tutto J attraversando gli zeri dei semi? La risposta è nota per potenziali razionali (Duistermaat–Grünbaum, monodromia banale), aperta per q ∈ C^∞ generale. Va confrontata con la letteratura (Andrianov–Sokolov, "intertwining senza singolarità").

**Q8. FW con potenziale.** Stima quantitativa della serie di Foldy–Wouthuysen troncata all'ordine m^{−k} per V ∈ W^{k,∞} (errore O(m^{−k−1})?). La trasformazione esatta di Eriksen è CON-FONTE.

**Q9. Citazioni da verificare.**
- Marchenko 1986 cap. 1: numero del teorema e costanti.
- Duistermaat–Grünbaum 1986: enunciato esatto.
- Andrianov–Sokolov 2003: lettura dell'enunciato, per la priorità di ENC-K1′.
- Owhadi 2017.
- Thaller 1992 cap. 5.
- Boyer (simmetrie di Schrödinger con potenziale quadratico): pagina.

**Q10. Encoder non locali per V non quadratico.** Bluman–Shtelen classificano solo gli encoder puntuali. Esistono famiglie di encoder non locali ma espliciti (E3), con cambio del tempo come in ENC-P0′, per V(t, x) non quadratico? Questo riaprirebbe B2 per potenziali dipendenti dal tempo.

## Aggiunte rev. 2 (dopo S-CHECK-F8-ENC)

**Q7 (aggiornata).** In ENC-K1′ l'insieme Z è chiuso e numerabile. Non è stato dimostrato che sia discreto: gli zeri dei semi successivi potrebbero accumularsi sui poli doppi di q_{k−1}. Va studiato con l'analisi di Frobenius al punto singolare regolare (esponenti −1 e 2).

**Q11. "W commuta con ∂_t" con c(t) non costante.** Il sotto-caso con W non locale in t (per esempio convoluzioni in t) e c(t) non costante non è coperto da P0(b), P0(b)^cl, P0(b)^loc (AUD ENC-15(d)).

**Q12. Continuazione laterale e (E1) sulle soluzioni.** VAR-L1 di S8-VAR fornisce la continuazione unica laterale da I × ω a I × J per V(t, x) ∈ L^∞_loc? Se sì, l'encoder per restrizione di KA P0 P6 è iniettivo sulle soluzioni. Allora, con la lettura "(E1) sulle soluzioni", esiste un encoder indipendente dal tempo per un V non autonomo. Domanda inviata a S8-VAR.

**Q13. Regolarità del propagatore con V solo continuo in norma.** Kato per domini comuni chiede in genere t ↦ H(t) fortemente C¹ (AUD ENC-15(b)). Va verificato se VAR-P11(e) vale con V ∈ C(ℝ; B(ℋ)). Da CIT-AUDIT-8 e S8-VAR.

**Q14. (S) modulo gauge.** Esiste una classe naturale in cui l'identificabilità modulo il gauge del modello di dato è non vacua e non banale (lettura di gauge di ENC-N1′)?

## Aggiunte post-Gate 8

**Q15. ENC-T2(c′) nella classe degli annullatori principali.** Nella classe C^∞(Ω) senza vincoli nessun getto finito certifica Ann_q(u) = (P_*). Con un vincolo di grado l'enunciato è falso (AUD2 KA P7). Resta aperto il caso della classe dei dati con annullatore principale: la perturbazione u + e^{αt}(x − x_1)^M della prova esce dalla classe (per esempio con u = e^{x²}). Serve una perturbazione che resti nella classe principale, oppure un getto che certifichi.
