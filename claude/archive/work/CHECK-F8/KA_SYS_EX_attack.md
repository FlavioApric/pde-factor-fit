# Kill-argument su SYS-EX (revisore ostile, 27/10/2026)

Fonte esaminata: soltanto `work/CHECK-F8/KA_SYS_EX_input.md`. Controlli di calcolo: `work/CHECK-F8/sympy/sys_ka_ex_check.py`.

## 1. Attacco principale: la riduzione del Passo 2 ignora i primi incomparabili

Il Passo 2 afferma che, se ψ: E → C^∞(Ω) non è iniettiva, "esistono q ∈ Ass(M) e una relazione su Ω" in cui compaiono soltanto il primo q e i primi p ⊋ q. Il testo non lo dimostra: rimanda alla "prova di SYS-T1", che non compare nell'input. Un elemento generico del nucleo è Σ_p Σ_j r_{p,j}(∂) f_{p,j} = 0, con p che varia in tutto Ass(M). Scegliendo q minimale fra i primi che hanno qualche r_{q,j} ∉ q, nella relazione restano in generale anche primi **incomparabili** con q, cioè né contenuti in q né contenenti q. Il caso più semplice è M = R/m_0 ⊕ R/m_1 con n = 1, dove la relazione è a·1 + b·e^x = 0. Di questi termini la prova scritta non dice nulla.

Le conseguenze sono due.
- Nel ramo "q massimale" la frase "la relazione contiene solo il termine r(∂)e^{λ·x}" è falsa così com'è scritta: possono comparire termini r′(λ′)e^{λ′·x} con λ′ ≠ λ, e termini f_{p,j} con p non massimale e p ⊄ m_λ.
- Nel ramo "q non massimale", h_0 viene scelto in ∏_{p ⊋ q} p. Un tale h_0 non annulla la parte di ν supportata su V(p) per p incomparabile, quindi l'uguaglianza Σ_j ∫ g F_j dy = 0 non segue.

Tentando di riparare, ho verificato che il difetto **non è fatale**. Per la minimalità di q, ogni altro primo p con un termine non nullo soddisfa p ⊄ q. Basta allora scegliere h_0 ∈ ∏_{p ≠ q, termine non nullo} p con h_0 ∉ q; esiste perché q è primo. Con questa scelta ν′ comprende tutti i termini diversi da q, e il resto dell'argomento (EX-L1, Stone–Weierstrass, misura degli zeri, EX-L2(b)) funziona senza modifiche. Il caso massimale si sistema allo stesso modo: si moltiplica per g ∈ ∏ m_{λ′} con g(λ) ≠ 0. Si tratta quindi di una lacuna di presentazione che si chiude in due righe, non di un passo falso. Non ho trovato alcun controesempio all'enunciato.

## 2. Punti secondari

1. **Passo 2, scelta di q (riga "altrimenti esistono q ∈ Ass(M)…").** Il testo non dice che q va preso minimale fra i primi con r_{q,j} ∉ q, né che i termini con r_{p,j} ∈ p si annullano. Senza la minimalità, la condizione p ⊄ q usata nella riparazione non vale. Severità: **MAJOR**, perché è la stessa lacuna del punto 1 e si ripara nello stesso modo.
2. **Enunciato SYS-EX: Ω vuoto.** Se si ammette Ω = ∅ come connesso, 𝒜 = 0, e allora M = R soddisfa (ii) ma non (i). Serve l'ipotesi Ω ≠ ∅. Severità: **MINOR**.
3. **Passo 2, ultimo punto (misura degli zeri di h_0∘s).** Il testo dice "olomorfa non nulla su U", ma ciò che serve è che la restrizione reale-analitica a B̊ non sia identicamente nulla. Questo segue da EX-L2(b), applicato in forma contrapposta a una palla contenuta in B̊. L'argomento regge, ma andrebbe detto esplicitamente. Severità: **MINOR**.
4. **EX-L2, prova di (b).** Il passaggio dal "luogo liscio connesso" è più pesante del necessario: se r si annulla su un aperto euclideo non vuoto di V(q) irriducibile, allora r ∈ q direttamente, per ragioni di dimensione. Il fatto citato è comunque corretto. Va però precisato che s(U) sta nel luogo liscio perché Δ contiene l'immagine dei punti singolari, come il testo dichiara. Severità: **MINOR**.
5. **EX-L2, esistenza di Δ e del rivestimento.** La finitezza di π implica che π è propria; insieme all'étalità generica (caratteristica 0) e al fatto che U è una palla, quindi semplicemente connessa, si ottengono fogli olomorfi. È corretto, ma poggia su fatti citati con numerazione da verificare. Severità: **MINOR**, solo bibliografica.
6. **SYS-L1.** La finitezza della famiglia (una somma diretta di sottomoduli non nulli in un modulo noetheriano è finita) e la sua essenzialità (ogni sottomodulo non nullo contiene una copia di R/p con p ∈ Ass) non sono scritte nell'input, ma sono standard e corrette. Severità: **MINOR**.
7. **Passo 3 e Osservazione 1.** L'uso dell'iniettività di C^∞(ℝ^n), invece di quella di C^∞(Ω), seguito da SYS-L0 applicato a ρ_Ω∘Ψ, è corretto: ρ_Ω è R-lineare e ker(ρ_Ω∘Ψ) ∩ E = ker(ρ_Ω∘ψ). L'attacco tramite Ω non convesso o non limitato quindi **non regge**. Anche il caso 𝒟′ regge, perché C^∞(Ω) ⊂ 𝒟′(Ω) è un'inclusione di R-moduli e SYS-N1 vale per le distribuzioni su Ω connesso.
8. **Attacchi verificati che non reggono.**
   - Più copie dello stesso primo: le palle disgiunte e Stone–Weierstrass sull'unione dei compatti separano i diversi F_j.
   - Primi annidati: ho verificato M = R ⊕ R/(ζ) con n = 1, f = (e^x − 1)/x. Il punto 0 sta nella palla B, ma h_0 = ζ elimina δ_0. SymPy conferma che a(∂)f + b = 0 implica a = b = 0, con grado di a fino a 2.
   - q = 0 e d = n: s = id, nessun problema.
   - Primi massimali dentro V(q): sono uccisi da h_0 ∈ m_λ.
   - Esempio del calore: il residuo dell'integrando è 0 (SymPy).
   - EX-L1: la trasformata si estende a una funzione intera, e il principio d'identità da un aperto reale vale.

   Severità: nessuna.
9. **Osservazione 2 (SYS-EX-C).** Il passaggio da (R/p)^N ↪ I iniettivo a μ_p(I) ≥ N richiede che E(R/p)^N sia un addendo diretto di I. È vero, ma non è scritto. Severità: **MINOR**, ed è fuori dal bersaglio.

## 3. Verdetto

**WOUNDED (lieve).** L'enunciato SYS-EX mi sembra vero: non ho trovato controesempi e la strategia (famiglia essenziale, funzioni intere rigide, iniettività di C^∞(ℝ^n), restrizione, SYS-L0) è solida. La prova contenuta nell'input ha però una lacuna reale nel Passo 2: la riduzione a una relazione che coinvolge solo q e i primi p ⊋ q non è dimostrata e, alla lettera, ignora i primi incomparabili. Si ripara in due righe, prendendo q minimale e h_0 nel prodotto di tutti gli altri primi presenti, con h_0 ∉ q. Corretti questo punto e l'ipotesi Ω ≠ ∅, il verdetto diventa SURVIVES.
