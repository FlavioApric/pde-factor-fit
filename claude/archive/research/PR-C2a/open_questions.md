# open_questions — PR-C2a

1. **Componenti per coefficienti variabili** (C4.1, C3.3): se la componente naturale è il dato locale nei punti singolari (simbolo di Riemann), come si scrive $E_{int}$ quando due termini spostano la stessa singolarità?
   - Esempio: $D^2 - x$ (Airy) come "$D^2$ + $(-x)$", dove nessun pezzo ha una singolarità irregolare all'infinito ma la somma sì.
   - Candidato: la teoria di confluenza / poligono di Newton. Da girare a R5 e R2.
2. **Identificabilità con coeff. polinomiali da una sola $u$** (R4): il minimo annullatore in $\mathbb C(x)\langle D\rangle$ è unico.
   - Domanda aperta: quale bound su grado e ordine garantisce che il "guessing" su un dizionario finito di termini $x^jD^k$ trovi esattamente $L$ e non un suo multiplo sinistro?
   - Analogo di G4: $\mathrm{ord}L = \mathrm{ord}$ del minimo annullatore e grado minimo.
3. **Calcolo funzionale e non-identificabilità spettrale** (C2.5 §4): se $u$ ha supporto spettrale finito in una base Sturm–Liouville, allora ogni $f(T)$ con $f$ nulla su quel supporto la annulla.
   - Come si fissa la scelta "giusta" di $L$? Per minimo ordine differenziale? Va formalizzato in C3.2.
4. **Gram esponenziali di tipo Cauchy**: il condizionamento cresce esponenzialmente quando gli esponenti si avvicinano. Questo ha impatto su P2 (coerenza, RIP) per i dizionari $\{x^je^{\lambda x}\}$. Serve una stima esplicita (Beckermann, Gram di Cauchy?). Da passare a R1.
5. **Riccati come encoder** (D1, G7): la derivata logaritmica linearizza Riccati nel caso ODE.
   - Esiste una classe di nonlinearità polinomiali $y^k$ di ordine superiore con una linearizzazione esatta analoga (equazioni di Riccati matriciali, Schwarziano)? Da girare a PR-C2c.
6. **Sferoidali** (non ipergeometriche): servono in G★ (dimensione 1, potenziale $c^2x^2$ su $[-1,1]$) o solo come ◇? Proposta: ◇, salvo come esempio di classe "Heun".
7. **Riferimenti da confermare**: il numero di sezione esatto in Teschl (GSM 140) per il teorema dei nuclei a coeff. costanti e per Frobenius. Il contenuto è standard; manca solo la sezione precisa.
