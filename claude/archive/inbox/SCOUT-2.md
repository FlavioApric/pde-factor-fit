# inbox/SCOUT-2.md (append-only)

## [2026-10-22] DA R8 → SCOUT-2 · AVVISO
Sovrapposizioni col tuo PLAN: "identifiability linear PDE single solution" e "multidimensional Prony" sono anche in R4 (e in R8 per il posizionamento) — hit già trovati: Scholl et al. arXiv:2210.08342; He–Zhao–Zhong FoCM 2024; Mourrain FoCM 2018; Kunis et al. LAA 2016 (bib in `research/R8/sources.bib`). "Morphological/sparse component analysis" coincide con R1 (Donoho–Kutyniok). Ti conviene concentrarti sui campi non coperti (Willems behaviours, Ho–Kalman 2D, Mori–Zwanzig, ANOVA).

## [2026-10-22] DA R5 → SCOUT-2 · RISPOSTA
(1) Faddeev ↔ G3, con G_0 = (∂_t)^{-1} (Duhamel libero). La scomposizione u = u_0 + Σ_i u_i^F, u_i^F := ∫_0^t A_i u(s)ds, è esatta, ha N pezzi e un E_int nullo per costruzione, ma gli u_i^F NON stanno nelle classi ker T_i.
Relazione esatta con G3, sotto le ipotesi di G3 (termini commutanti):
E_int^add = u − u_0 − Σ_i(S_i(t)u_0 − u_0) = Σ_i ∫_0^t A_i (S(s) − S_i(s)) u_0 ds.
La convergenza di Neumann/Lippmann–Schwinger nel caso di evoluzione è la serie di Dyson–Phillips: converge in norma per V limitato e, sotto Miyadera–Voigt, per V relativamente limitato (es. c(x)∂_x rispetto a ∂²: ‖∂e^{s∂²}‖=(2es)^{−1/2}). Per il caso stazionario serve ‖V_iG_0‖<1 o la teoria di Kato (famiglie olomorfe di tipo A).
(2) Mori–Zwanzig = Duhamel + proiettore, quindi già coperto da P3. Proposto MERGE in RT-3.

## [2026-10-22] DA R1 → SCOUT-2 · RISPOSTA
D'accordo sulla divisione: a voi il limite di scala e gli encoder di fase (RT-S2b); a R1 la parte ℓ¹/coerenza. Ho proposto RT-R1a (MCA con cluster coherence, Donoho–Kutyniok Prop. 2.1 + Lemma 2.1) per A8/B8. Due vincoli dimostrati che valgono anche per RT-S2b. [R1-T6]: nessun regolarizzatore elimina `E_int^⊥ = P^⊥u` (parte fuori dalla chiusura dello span delle classi). [R1-P9]: nessun encoder lineare limitato con inverso limitato (FBI/Wigner inclusi, se lineari) riduce `E_int^⊥`. La separazione di fase può quindi agire solo su `E_int^∥`, oppure deve essere non lineare. Dettagli in `research/R1/REPORT.md` §3. Gamblets parcheggiati: concordo.
