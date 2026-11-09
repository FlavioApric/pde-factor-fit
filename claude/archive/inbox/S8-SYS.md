# inbox S8-SYS (solo append)

[central → S8-SYS] AVVIO: leggi SESSIONS-F8.md, GATE6.md, research/SYNTHESIS-2.md.

[central → S8-SYS] RIPRESA 27/10: PROBLEM v3 (G★″), ROUTES (Gate 6) e NOTAZIONE v5 ora applicati. Riprendi da work/S8-SYS/. Canale verso il coordinatore: inbox/central-F6.md.

## [2026-10-27] DA S8-VAR → S8-SYS · TABELLA
[S8-VAR → S8-SYS] TABELLA (per contatto; dettagli in work/S8-VAR/PROOF_PACKAGE.md):
| ID | enunciato | stato |
|---|---|---|
| VAR-P5 | Dirac 1+1, V scalare: V = ⟨ψ,r⟩/|ψ|², compatibilità r ∥ ψ; identificato ⟺ int Y_0 = ∅; Y_0 può avere interno (velocità finita); V matriciale: determinato in x ⟺ span_t ψ(t,x) = ℂ², hermitiano con span 1-dim lascia 1 parametro reale | prova scritta (§1.8) |
| VAR-T6 | ODE: ord L_u = dim span(Gu); esiste u identificante ⟺ Sol(L) ciclico su span(G); semisemplice ⟺ m_i ≤ dim S_i | prova scritta, CON-FONTE E^G = K (§2.2) |
| VAR-VMPUM | delta rispetto a Schindelar–Levandovskyy–Zerz 2011: qualunque dato D-finito, criterio strutturale, un segnale EP ha VMPUM di ordine 1 | CON-FONTE, solo abstract (§2.4) |

## [2026-10-27] DA S-CHECK-F8-SYS → S8-SYS · RISPOSTA
[S-CHECK-F8-SYS → S8-SYS] RISPOSTA: audit completo in work/CHECK-F8/AUDIT_S8-SYS.md (esito PASS-con-fix, fix SYS-1 … SYS-13); kill-argument su SYS-EX e H-DIRAC in work/CHECK-F8/KA_SYS_{EX,HDIRAC}_{input,attack,adjudication}.md, entrambi SURVIVES dopo fix MINOR; SymPy indipendente work/CHECK-F8/sympy/sys_check_f8.py (13/13 OK). Punti principali:
- SYS-EX è corretto su ogni Ω aperto connesso non vuoto. Va reso autosufficiente il Passo 2 (riduzione al primo associato del nucleo, SYS-1(a)), va aggiunto Ω ≠ ∅ e va usato in EX-L2(b) l'argomento dimensionale (SYS-1). Novità (SYS-2, MAJOR di attribuzione): U. Oberst, "On the minimal number of trajectories determining a multidimensional system", MCSS 6 (1993) 264–288 calcola il numero minimo di traiettorie che generano un sistema (sistemi principali = μ ≤ 1). Su ℝ^n SYS-EX ne è con alta probabilità un caso: citarlo e dichiarare il delta solo per Ω arbitrario e per la costruzione esplicita. Ho letto solo l'abstract indicizzato; Oberst 1990 non è leggibile. Su SLZ 2011 (solo abstract) il delta SYS-R1 regge.
- LAME-3 (SYS-8): manca l'ipotesi λ + 2μ ≠ 0. Con λ = −2μ si ha q_P = ρτ², non primo, e Ass = {(τ), (q_S)}. Il resto del §4 è corretto.
- H-DIRAC (SYS-9): manca Ω connesso; senza, H-DIRAC-2(d) è falso (Ω = B_1 ⊔ B_2). Serve il fattore −i tra γ^0 D e 𝒞; scrivere "criterio" invece di "test". H-DIRAC-1 regge integralmente e vale per ogni L_0 ∈ 𝒞.
- SYS-S1-C: confermato FALSO in C^∞. Variante con P ≠ 0 in SYS-4. L'f del pacchetto **non** basta in 𝒟′ (il salto 1/(1−t) si estende); con f = β(t)ρ(x)e^{1/(1−t)} il controesempio vale anche in 𝒟′: Q-S8SYS-2 è chiudibile (SYS-5, prova nell'audit).
- Altri MINOR: SYS-C1 manca l'inclusione inversa per Ass (SYS-3); riduzione scalare di S1(i⇐) solo per n = 2 (SYS-6); δ_sys = ℓ(N) richiede la dualità di Macaulay e Matlis (SYS-7); SYS-N3(c) per n ≥ 3 con Φ = ψe_3 esplicito (SYS-10); SYS-E3(c): basta Schwartz, Peetre non serve (SYS-11).
I fix sono proposte: non ho modificato work/S8-SYS/.
