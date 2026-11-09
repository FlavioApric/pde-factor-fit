# CHECK_REQUEST — S8-ENC → S-CHECK-F8 · 27/10/2026

**Testo da controllare:** `work/S8-ENC/PROOF_PACKAGE.md`. Le verifiche sono in `work/S8-ENC/sympy/` (quattro script, 80/80 OK) e si rilanciano con:

`D:\ProblemaBase\.venv\Scripts\python.exe -I work/S8-ENC/sympy/<script>.py`

Nessun claim è proposto come DIMOSTRATO prima di questo controllo. Il kill-argument interno è in §10 del pacchetto: PASS-WITH-FIXES su ENC-N1′ ed ENC-P0, con revisori esterni non disponibili.

## Claim da controllare, in ordine di priorità

| # | ID | § | stato proposto dopo il check | perché è prioritario |
|---|---|---|---|---|
| 1 | ENC-1 (1)–(5) | 2 | DIMOSTRATO, + CON-FONTE Marchenko per il confronto | cammino critico di R6 (S8-DICT) e di G★″ |
| 2 | ENC-U1 | 2 | DIMOSTRATO | normalizzazione dell'encoder |
| 3 | ENC-T2 (a)(b)(c) | 3 | DIMOSTRATO (lemma a q noto) | fix F6, usato da DICT-R6 |
| 4 | ENC-P0(b) | 4 | DIMOSTRATO | teorema negativo per G★″ §6 |
| 5 | ENC-N1′ (i)–(iv), ENC-N1 FALSO | 5 | DIMOSTRATO / FALSO | B2 nel PROBLEM |
| 6 | ENC-K0 | 1 | DIMOSTRATO | giustifica (E2′) |
| 7 | ENC-A9(a) | 7 | DIMOSTRATO | E_int A9 di Schrödinger |
| 8 | ENC-K1′ | 6 | DIMOSTRATO (con nota "probabilmente noto") | tabella encoder |
| 9 | ENC-P0(a), P0′, POLE-N | 4 | DIMOSTRATO sotto (H-P0) | — |
| 10 | ENC-A9(b2), (b4)-nucleo | 7 | DIMOSTRATO | — |
| 11 | NS-EQUIV-Ω | 8 | DIMOSTRATO | fix F7.4 |
| 12 | FAD-1, FW-1 (libero), ENC-C1 | 9, 2 | DIMOSTRATO | strumenti |

## Punti delicati (dove guardare)

**D1. ENC-1, regolarità attraverso x = 0.** K è C² solo sui due triangoli Δ_±, non su Δ. La prova passa per l'identità g″ = qg + T(f″) su ciascun lato e per il fatto che g ∈ C¹(J) con g′(0±) = f′(0). Da verificare:
- che T(f″) sia continua in 0, con l'integrale su [−x, x] che tende a 0;
- che "C¹ con derivata seconda laterale continua e uguale su entrambi i lati ⇒ C²" sia applicato correttamente (serve la derivata seconda esistente in un intorno bucato, con limite comune).

**D2. ENC-1, regolarità di Φ.** Le formule per Φ_ξξ derivano sotto il segno d'integrale una funzione che è solo C¹ in partenza. Serve un bootstrap: prima Φ ∈ C¹ dall'equazione integrale, poi Φ_ξ è dato da una formula con Φ_ξ dentro l'integrale, quindi è derivabile. Controllare che l'ordine dell'argomento non sia circolare.

**D3. ENC-1(3), S = T′T = I.** Si usa:
- che T′T abbia forma I + ∫_{−x}^{x}R con R continua (composizione di due operatori di Volterra simmetrici);
- l'unicità della trasformata di Laplace a supporto compatto, per x fissato e k ∈ ℂ.

Verificare la forma del nucleo composto, in particolare i domini |s| ≤ |y| ≤ |x| per x < 0.

**D4. ENC-U1.** Il passaggio "C(x, ·) = 0 sull'interno ⇒ A = B = 0" richiede funzioni test f ∈ C²(J) che separino f(x), f(−x) e l'integrale. Controllare il caso in cui x è vicino a 0, dove [−x, x] è piccolo.

**D5. ENC-T2(c), non certificabilità.** La tesi richiede che j^N(Th_0) = 0 se j^N h_0 = 0. Segue dalla triangolarità di T, che è affermata per T come per W. Il pacchetto la verifica in SymPy solo fino all'ordine 3: controllare l'induzione in generale. Inoltre M > deg_ξ φ(P_*) garantisce φ(P_*)(α, ∂_x)(x − x_0)^M ≠ 0: verificare che il coefficiente di testa non si annulli. Basta un monomio di grado massimo in ξ con coefficiente non nullo in τ = α.

**D6. ENC-P0(a), ipotesi (H-P0).** La continuità di U_V(t)u_0 nella norma del grafo è CON-FONTE (Pazy cap. 5, VAR-P11). Nel verso (⇐) si usa il grafo chiuso per H_0M|_D: verificare che M = W(0) ∈ 𝔈 basti, cioè che MD ⊂ D implichi H_0M chiuso su D con la norma del grafo.

**D7. ENC-P0(b), rango delle moltiplicazioni.** Il lemma "moltiplicazione per m ∈ L^∞ di rango finito ⇒ m = 0 q.o." è elementare. Controllare che l'enunciato usi solo dim ker W < ∞ e non l'iniettività.

**D8. ENC-N1′.** È un quadro astratto: controllare che "compatibile con ~" sia definito in modo che [W_V u] abbia senso. Nell'esempio (iv) il fattore e^{−iq(x_0)t} della soluzione libera va assorbito nella classe modulo costanti. Verificare che 𝒪 sia definito "modulo ~ e modulo costanti" in modo coerente con DM-φ di NOTAZIONE v5.

**D9. ENC-K1′, divisione e insieme discreto.** La divisione euclidea a destra per A_1 = ∂ − g è fatta su J ∖ Z, dove g ha poli. A ogni passo serve un autovettore ψ_k di L_{q_{k−1}} su ker W_{k−1}, che è ancora di dimensione n − k + 1 su ogni sottointervallo di J ∖ Z. Controllare:
- che "suriettivo su C^∞ di ogni sottointervallo" basti per concludere W_1L_{q_1} = (L_0 + c)W_1;
- che Z resti chiuso e discreto in J (unione finita).

**D10. ENC-A9(a), Duhamel.** Il lemma del prodotto è applicato a s ↦ U(t − s)𝒮(s)f con 𝒮(s)f ∈ H², continua in H². Serve U(t − s) fortemente continuo su L² e derivabile su H² = D(H_0 + V), che è vero perché V è limitato. La costante 2/3 del termine t³ viene da ∫_0^t 2s²‖V′‖²ds; il PLAN diceva 1. Controllare anche il passaggio al limite E^mult/t² → ½[H_0, V]f (convergenza dominata in L²).

**D11. ENC-A9(b2).** Convenzioni di Fourier (f̂(p) = ∫f e^{−ipx}, x ↔ i∂_p) e segno della fase F²t³/12. Lo script `eint_closed` lo verifica sul nucleo. La normalizzazione di Avron–Herbst differisce da F6-ENC NOTE §5 (½∂² contro ∂²): da segnalare in errata a F6.

**D12. ENC-A9(b4), nucleo erfc.** L'unicità richiede G temperata. Verificare la stima di |G| per |z| → ∞ con √(it) = e^{iπ/4}√t: gli argomenti di erfc hanno parte reale ∓z/(2√(2t)) + O(1), e serve la stima asintotica di erfc nel settore |arg w| < 3π/4.

**D13. NS-EQUIV-Ω (d).** L'identità U_osc(π) = −iP richiede la normalizzazione H = −½∂² + ½x² (autovalori n + ½). Il pacchetto usa questa nella lente: controllare che sia coerente con la lente di §4 e con VAR-T10, che usa H = −∂² + x², periodo π/2 e tempi diversi.

**D14. FAD-1(iii).** L'ordine O(‖V‖³) è nella norma di C(J) a λ e ℓ fissati. Controllare che la costante sia uniforme sul numero N di centri, oppure dichiarare che dipende da N.

## Citazioni da controllare (per CIT-AUDIT-8)
- Marchenko, *Sturm–Liouville Operators and Applications* (1986), cap. 1: numero del teorema sul nucleo simmetrico e costanti.
- Povzner, Mat. Sb. 23(65) (1948) 3–52.
- Duistermaat–Grünbaum, CMP 103 (1986) 177–240: enunciato esatto, solo V → 0.
- Andrianov–Sokolov, Nucl. Phys. B 660 (2003) 25 (hep-th/0301062), e Sokolov arXiv:0903.2835: priorità di ENC-K1′.
- Bluman–Shtelen 1996 §2 (già verificata in CIT-AUDIT-6 voce 16).
- Pazy cap. 5 / Reed–Simon II §X.12: propagatore (H-P0).
- Owhadi, SIAM Rev. 59 (2017) 99–149: localizzazione dei gamblets.
- Thaller, *The Dirac Equation* (1992) cap. 5: trasformazione di Eriksen.
- Mehler: forma del nucleo (b3), già in VAR-T10.

## Fusioni e doppi conteggi da applicare nel LEDGER
- ENC-L1 è fuso in VAR-P8(a) (R5-P7).
- ENC-A9(b3) coincide con VAR-T10.
- La formula operatoriale di ENC-A9(b4) coincide con VAR-P8(c): il contributo di S8-ENC è solo il nucleo erfc.
- ENC-N2(a) coincide con VAR-P4.

---

## Rev. 2 (27/10/2026): richiesta di audit dei claim nati nel recepimento

L'audit della prima versione è chiuso (`work/CHECK-F8/AUDIT_S8-ENC.md`), con i fix ENC-1…ENC-15 recepiti (`work/S8-ENC/RECEPIMENTO.md`). I claim seguenti sono **nuovi o riformulati** e vanno auditati:

| # | ID | § del PP | punto da controllare |
|---|---|---|---|
| R1 | ENC-P0(b)^cl | 4 | testo del revisore: verificare che "intreccia su C^∞_c(J)" basti anche se W non manda C^∞_c in C^∞_c |
| R2 | ENC-P0(b)^loc | 4 | come R1, con le funzioni test supportate in U |
| R3 | ENC-P0′ su nucleo denso | 4 | la prova non usa (H-P0): regola del prodotto con v C¹ in ℋ a valori in D(H_0); estensione per densità |
| R4 | esempi di P0′ su 𝒮(ℝ) (lente, Avron–Herbst, V = β(t)x + γ(t)) | 4 | invarianza di 𝒮 sotto U_osc(t) e U_AH(t); essenziale autoaggiuntezza su 𝒮 (CON-FONTE); formula della lente nella variabile y |
| R5 | ENC-P0′-DIC | 4 | il sistema T′ = 1/ρ², ρ′ = 4aρ, a′ + 4a² = −α dentro l'ansatz puntuale + gauge, e la normalizzazione di a |
| R6 | POLE-N^cl | 4 | il passaggio "intreccia i∂_t ⇒ ∂_tW = 0" e la scelta di un intervallo privo di poli a due tempi |
| R7 | ENC-T2(c′) | 3 | termine di ordine minimo p_d(α)(−1)^dM!/(M − 2d)!; il caso d = 0 (P_* = p_0(τ)) |
| R8 | ENC-N1′ rev. 2 | 5 | buona posizione del quadro con classi [𝒮_V], N_V e ≈; il punto (v) con la famiglia stretta |
| R9 | ENC-K1′ rev. | 6 | Z chiuso e numerabile; scelta globale di ψ_2 su J_1 |
| R10 | FAD-1(iii) | 9 | costante (Cℓ𝐕)³e^{Cℓ𝐕}/3 |

Nuova verifica: `sympy/enc_recep.py` → `enc_recep.out`, 10/10 OK.
