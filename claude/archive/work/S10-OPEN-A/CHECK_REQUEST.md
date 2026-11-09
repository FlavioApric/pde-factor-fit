# CHECK_REQUEST — S10-OPEN-A (27/10/2026)

Al coordinatore: richieste di audit (proof-checker e, dove indicato, kill-argument) per i claim nuovi di `PROOF_PACKAGE.md`. Ordine di priorità.

## 1. S10A-T3 (§3) — priorità alta
- **Passo 2′.** Verificare la geometria lipschitziana: $B(y_0+\varepsilon e_i,r_\varepsilon)\subset\Omega$ per $y_0\in\bar\Omega\cap\bar C_i'$, con $r_\varepsilon=\varepsilon/(2\sqrt{1+L^2})$. Verificare anche la gestione di $C_i''$ (punti $y_0$ vicini a $y$ ma fuori da $C_i'$).
- **Passi 3–7** "identici a OPF5B-T1": controllare che nessuno usi la convessità (la mappa delle dipendenze di OPF5B-T1 dice di no).
- **Passo D.** Verificare l'argomento di codimensione finita: indipendenza aperta in $\mathcal K/S$ e un solo $U$ per tutti i $v_k$ (Precisazione 2).
- **[COL]** CON-FONTE: verificare le sedi (Grisvard Lemma 1.5.1.9; Verchota JFA 59 (1984) Thm 1.12; Hofmann–Mitrea–Taylor JGA 17 (2007)) e la forma usata: $\bar\Omega\subset\Phi_\sigma(\Omega)\subset\{\mathrm{dist}<C\sigma\}$. Richiesta per CIT-AUDIT.
- Kill-argument: cercare un dominio lipschitziano semplicemente connesso e un $P$ con somma non densa.

## 2. S10A-T2 (§2) — priorità alta
- **Passi 0–1.** Riscalamento $t=\nu^\alpha s$, valutazioni in ν dei tempi, passaggio da "vale per $\nu\in\Lambda^{-1}$" a identità polinomiale.
- **Passo 3** con $\mathfrak a>1$: controllare che all'ordine $\nu^{\mathfrak a}$ non ci siano contributi misti tra gli ordini intermedi dei tempi X e i fattori Y.
- **Passo 4 formale.** Il determinante di Hankel è identicamente nullo in $\mathbb C[[s]]$, contro $\varepsilon_0^ns^{n^2}\det\mathrm{Hilb}_n$.
- Esempi: endomorfismo di $A_1$ ($x\mapsto\mu x$, $\partial\mapsto\mu^{-1}\partial$) e algebra libera.
- Kill-argument: cercare un'algebra con (H) e (Dil) in cui una parola finita a $\varepsilon_0$ fissato esista. Se esiste, S10A-T2 è falso.

## 3. S10A-T1, S10A-L1, S10A-C1 (§1) — priorità media
- Stabilità di 𝔅 per moltiplicazione per $e^{\gamma t}$ (stima di Leibniz in S10A-L1(i)).
- S10A-T1(b): passaggio $H^{m+1}\Rightarrow H^m$.
- Lettura di P1-Q6: confermare che un termine costante (monomio di grado 0) è un "termine" secondo NOTAZIONE r. 44. Se lo è, l'enunciato letterale è FALSO (reazione–diffusione). Altrimenti S10A-C1 è solo un complemento.

## 4. S10A-P1 (§3) — priorità media
- Stima interna del flusso, continuità in $L^2$ sulle armoniche.
- ${*df}=-if'dz$.
- Decomposizione di Laurent delle armoniche complesse sull'anello.
- $f\in H^m(A)$ da $f'\in H^{m-1}(A)$ (stima in polari).
- (ii) generale: Rudin RCA Thm 13.11 (CON-FONTE, per CIT-AUDIT).

## 5. S10A-L2, S10A-C2 (§4) — priorità bassa
- Mappa aperta, compattezza di $\Pi_r|_M$, applicazione di OPR2-L1 con $r=2$.

## 6. Bookkeeping (§0, §5)
Confermare le righe di chiusura citate: r. 70, 110, 111, 146, 151, 154, 156, 170, 182, 138. In particolare OPF5A-T5 (r. 182) per P1-Q5 sui dati compatibili: non ho riletto il suo audit. Confermare anche la lettura "C3-Q1 CHIUSO per modello" (§5).

## Controlli SymPy
`sympy/s10a_q6.out` 7/7, `sympy/s10a_q7.out` 18/18, `sympy/s10a_p2q1.out` 7/7. Eseguiti con `D:\ProblemaBase\.venv\Scripts\python.exe -I`. Nessuno script `_vendor` eseguito.
