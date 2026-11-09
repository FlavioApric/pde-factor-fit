# REPORT — S5-FIX7 · fix F5C-1..F5C-12 in work/OP-F5C/PROOF_PACKAGE.md · 26/10/2026

**Mandato:** applicare SOLO i fix decisi da `work/CHECK/AUDIT_OP-F5C.md` (S-CHECK-19), con marcatura in linea `[fix <id>, S5-FIX7]`, testo vecchio barrato o riportato come "testo originale".
**Skill caricate (lettura SKILL.md):** skills-local/session-protocol. Nessuno script `_vendor` eseguito; nessun processo toccato; run `opf5c_delta0_4_5`, `opf5c_delta0_5`, `opf5c_delta_4_7` e loro .out non toccati.
**Fonti dei fix:** AUDIT_OP-F5C.md §1–§2; KA_OPF5C_T6_adjudication.md (per F5C-6/7/8/9). Nessuna matematica nuova.
**File modificati:** `work/OP-F5C/PROOF_PACKAGE.md` (37 marcatori S5-FIX7), questo file, `inbox/central.md` (append).

## Fix applicati
| Id | Dove | Cosa |
|---|---|---|
| F5C-1 | Convenzioni, §0, T2 enunciato/prova, §6 | Π_N(k) normalizzato monico in y_N ⇒ Π_N(k) = χ_k (non ±); omogeneità pesata W_N solo per il χ universale ∈ ℂ[k, y] |
| F5C-2 | dopo (Nov′) | Inserita la prova di 3 righe (linearizzazione in X = 0, G_c(−κ_i) = 0) che le costanti sono a_j = e_j(κ) |
| F5C-3 | P7(b) | Frase "resto di V² + λ^{2N+1}" corretta: per k ≠ 0, r_m = Σv_iv_j + f_m; termini lineari in v non cancellano v_2²v_{N−1} |
| F5C-4 | L8 | Citazione Kreuzer–Robbiano §4.3 barrata e sostituita dalla prova per sollevamento delle sizigie di Koszul (testo dell'audit); L8 ora autonomo |
| F5C-5 | P9 (metodo, tabella, nota), §0, §3.5 | Certificati k = 0 N = 2,3,4 dichiarati non salvati da OP-F5C, con puntatori alle riproduzioni S-CHECK-19 (`work/CHECK/sympy/s19_delta_b*.out`, `_g*.out`; N=2,K=3 senza .out dedicato); righe K = 2N e N=1,K=2: "= N+1" solo per k testato, ∀k solo ≤ (V-ex) |
| F5C-6 (MAJOR) | L9 | Ipotesi g ∈ C² (o C^{1,1}); osservazione con il controesempio C¹ dell'audit (A = 0, g(z) = −z/(2 log(1/z)), z = e^{−√x}); Chicone non necessario |
| F5C-7 (MAJOR) | T6(b), prova, Cor.(iii), §0, §4.6 | Riparazione (α): ipotesi sull'intero getto z = (u,…,u^{(K−1)}) = O(e^{−β|x|}); bootstrap su W^{ss}_loc aggiunto solo come osservazione "via alternativa non scritta" (l'audit ne dà solo lo schema) |
| F5C-8 | T6(c) | q_± definiti nelle code effettive (archi della stessa orbita monotona); chiusura di T_± via convergenza puntuale, T_+ ∩ T_− = ∅ |
| F5C-9 | T6 enunciato, Cor.(ii) | p complesso: ℓ, s, n_u riferiti a Re p o Im p con α ≠ 0; Cor.(ii) per relazioni reali |
| F5C-10 | L2, T2 dipendenze | Citati Blum-Smith 2.4.17, 2.4.18, 2.4.19 con la catena; Bruns–Herzog ed Eisenbud marcati "non usati" |
| F5C-11 | T5, §0 | T5 → CONDIZIONALE (Ritt/Kolchin, numero non verificato), con nota sulle ricerche dell'audit |
| F5C-12 | O6 (Conseguenza) | Ricordato che senza analiticità congiunta in (t,x) φ è solo C^∞; conclusione invariata |

**Tabella di stato:** §0 ha ora la colonna "stato proposto dall'audit S-CHECK-19"; aggiunta §0.1 (stato per claim, colonna copiata da AUDIT §0, con fix applicati).
**Bibliografia:** aggiunta §8 "Bibliografia verificata" (copia di AUDIT §2).

## Non applicato / da decidere
- F5C-5(i) "salvare gli .out": S5-FIX7 può scrivere solo nel PROOF_PACKAGE; non ho creato file .out. Il package rimanda alle riproduzioni S-CHECK-19 già su disco (N = 2, K = 3 k = 0: nessun .out dedicato trovato).
- F5C-7 (β) bootstrap: non scritto per esteso nell'audit ⇒ solo osservazione, non usato.
- Stato di T6(b)/Cor.(iii) dopo la riparazione (α): l'audit non lo fissa esplicitamente (dice PROVA SCRITTA con lacuna finché F5C-7 non è riparato); lo decide il coordinatore.

DONE S5-FIX7
