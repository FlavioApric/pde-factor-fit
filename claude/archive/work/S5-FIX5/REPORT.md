# REPORT — S5-FIX5 · 26/10/2026
(Salvato dal coordinatore: la scrittura del subagente era bloccata dall'ambiente; testo fedele alla sua risposta finale.)
Mandato: applicare SOLO i fix già decisi dagli audit, marcati inline `[fix <id>, S5-FIX5]`; nessuna matematica nuova; stati LEDGER non toccati.
Skill caricate: skills-local/session-protocol. Nessuno script _vendor eseguito. Sostituzioni fatte con script Python di sola sostituzione testuale (scratchpad), con controllo di unicità per ogni stringa.
Controllo preliminare: grep di "S5-FIX5" e "Bibliografia verificata" nei PROOF_PACKAGE → nessuna occorrenza (nessun fix doppio).

## 1. work/OP-F5B/PROOF_PACKAGE.md ← AUDIT_OP-F5B (S-CHECK-18)
- F5B-1 → F1 riscritta in forma globale pesata (∀ε: E/cosh(ε|x|) ∈ B_{∞,P̃}); deduzione φE ∈ B_{∞,P̃} via Thm 10.1.15; convenzione P(D) ↔ p(ζ). Testo vecchio barrato.
- F5B-2 → ipotesi di T1: P ≠ 0 (c ≠ 0).
- F5B-3 → F2 citata con precisione: Stein cap. VI §3.1 Thm 5 p. 181, estensione unica per ogni k; Grisvard Cor. 1.2.2.3 per "convesso ⇒ lipschitziano". Intestazione vecchia conservata.
- F5B-4 → Passo 4: |τ_i| ≤ ε·diam Ω̄, w_0 = 0, convergenza uniforme sugli n+1 indici.
- F5B-5 → C1(c): "sui domini convessi limitati".
- F5B-6 → C1(d): condizione sugli intorni W′; osservazione esplicitamente non auditata.
- F5B-7 → sintesi §0, riga 2(ii), e P3 dopo (v): riformulazione come (iv)+(v). Testo vecchio barrato.
- F5B-8 → prova di P3(iv): T2 con 𝔄 := 𝔄_π (Ore {π^N}; P̂ monico ⇒ saturato, T2(e)). Testo vecchio barrato.
- F5B-9 → quadro §2: Ore per A_2 resta CON-FONTE non verificata; C4 non la usa.
- F5B-10 → nota di portata dopo T6: test "Tu ∉ 𝒯" = OP-ALG-C1(iv); non copre test Tu = 0 né test non lineari.
- F5B-11 → P7(a): ipotesi M = 𝔇/𝔇P con P monico (senza 𝔄-torsione).
- Tabella §5: colonna stato = "stato proposto dall'audit S-CHECK-18", con "(era: …)". Aggiunta riga con gli aggiornamenti proposti (OPF-Q3, P2-Q1, EX-Q1 chiusi; EX-BES → DIMOSTRATO).
- Aggiunta "Bibliografia verificata" (5 voci dall'audit).

## 2. work/OP-F5D/PROOF_PACKAGE.md ← AUDIT_OP-F5D (S-CHECK-17)
- F5D-1 → T3: b(−k) = conj b(k), quindi b ≡ 0 su ℝ∖0.
- F5D-2 → T3, enunciato: q_{d*} ∝ Π (la prova dà 4^{−N}Π).
- F5D-3 → L4: stime di Cauchy via L3(iii), uniformi in x, su un disco attorno a iκ (anche per ∂_xm_+). Testo vecchio barrato.
- F5D-4 → (a) L3(ii): conteggio n·C_x^{n−1}/(n−1)!; (b) L5(i): differenziale ℂ-lineare di w in 0 (Cauchy–Riemann al bordo).
- F5D-5 → L6: κ := −k diventa k̃ := −k.
- F5D-6 → L10: b continuo; ρ continuo dove a ≠ 0; controesempio ½ sech x; ρ ≡ 0 ⟺ b ≡ 0. Λ_m definito con b(ξ) ≠ 0. T4 (⇒) usa b continuo.
- F5D-7 → T4: risultato a tempo fissato; INT-T2 dinamico mod L9-ZS (da scrivere) e (UC). Frase vecchia barrata.
- F5D-8 → L10: argomento del Wronskiano per la dimensione 1.
- F5D-9 → corollario di T6: ipotesi esplicite (u_0 ∈ C^∞ non costante, t > t*; C² per (v); S_B = Lax–Oleinik mod [K-U]). Refuso ‖u_0′‖_∞ corretto.
- F5D-10 → P14: R ∈ C^∞ richiede l'estensione di L3 ai momenti superiori, oppure GT §6; coerenza di ν con GT (1.5), (5.29).
- F5D-11 → P14/P15: [GT-u] non trovata; P14 e P15 restano CONDIZIONALI; via alternativa Deift–Zhou 1994.
- F5D-12 → C2: metadati di Kay–Moses; nota Freeman–Nimmo; V-ex N = 2 (11/11) e N = 3 parziale (s17).
- F5D-13 → L9: stima del termine sorgente (1/|k|)∫_x^∞|u_t|.
- F5D-14 → R2: [DP] CON-FONTE secondaria verificata (Bilman–Buckingham 2019); controllo della deduzione riportato.
- F5D-15 → fonti §5 e P15: [Hm] = KVZ GAFA 28 (2018); primaria Lax CPAM 1975 §3 non letta.
- F5D-16 → T7 e §8: Kružkov 1970 Thm 1 §3 letto sul testo primario.
- Note di stato: colonna SymPy di C2/L6/T3 = "V-ex N = 2 eseguito da S-CHECK-17 (s17)"; riga T7 = "Kružkov Thm 1 §3 letto".
- Tabella §7: "stato proposto dall'audit S-CHECK-17", con "(era: …)".
- Aggiunta "Bibliografia verificata" (tabella dell'audit §4, 6 righe).
- Lasciati come testo storico: sintesi §0.2 e riga 8.

## 3. work/OP-NL/PROOF_PACKAGE.md
- OPF5D-R1 → OP-P18: nell'ipotesi (ZC) nota di correzione (per n = 0 lax_checks.out dà +(i/2)σ_3, quindi "n = 0..3" è errato a n = 0; testo vecchio conservato); nell'enunciato Ω_d sostituito da Ω̃_d := −d_0 + Σ_{n≥1}d_n(2ζ)^n (vecchia definizione barrata; effetto solo sugli insiemi di zeri); nella prova, nota: Ω_d = Ω̃_d, come in OPF5D-T4.
- CB-2 (dal coordinatore) → riga ~183: "Gel'fand–Dikii, Funct. Anal. Appl. 10(4) (1976) 259–273, DOI 10.1007/BF01076025".
- CB-3 (dal coordinatore) → riga ~92: "DLMF 9.7.9–9.7.10" (9.7.11 riguarda Bi).
- Non toccati: tabella di stato OP-NL righe 34–35 (stati: coordinatore); riga 34 "Gelfand–Dickey" senza anno (fuori da CB-2); work/P1 (CB-1, coordinatore).

## Non applicato
- F5B-12: nota senza riparazione, fuori da F5B-1..11.
- Unica scrittura bloccata: questo REPORT.md.
