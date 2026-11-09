# Aggiudicazione kill-argument — OPF5B-T2 / P3 / C4 · S-CHECK-18 · 26/10/2026
Input: KA_OPF5B_T2C4_input.md. Attacco: KA_OPF5B_T2C4_attack.md (subagente indipendente, esito SURVIVES WITH MINOR FIXES; controlli SymPy propri nel suo scratchpad).
| punto | esito attacco | decisione |
|---|---|---|
| T2 (b)⇒(a′): frazioni sinistre, A′p_m^{−1} = c^{−1}A″ ⟺ cA′ = A″p_m (Ore sinistra) | sopravvive | confermato |
| T2 rango/piattezza, (d′), (e) | sopravvive | confermato |
| Ore di 𝔄∖0 in A_2 | lacuna di citazione | accolta → F5B-9 (CON-FONTE, numero non verificato; C4 non lo usa) |
| P3 (i),(iii),(v),(vi) | sopravvive | confermato a mano (vi: cancellazione in dominio, N minimo) |
| P3(iv) "la prova di T4 usa solo dominio noetheriano" | lacuna di attribuzione | accolta → F5B-8: citare T2 sopra 𝔄_π (P̂ monico ⇒ saturato) invece della frase |
| P3 vs T2 (π-torsione contro saturazione completa) | nessun conflitto | confermato: senza π-torsione M ↪ 𝒟_π/𝒟_πP̂ ≅ 𝔄_π^m, quindi senza A_1-torsione |
| C4(a) azione destra su 𝒟/x𝒟 e argomento del grado | sopravvive | confermato; ricontrollato con implementazione indipendente (s18, test 3) |
| C4(b) h_j, grado in s, passaggio Ω′ → Ω | sopravvive | confermato; s18 test 7 (ordine, grado ≤ 4) |
| C4(c),(d) | sopravvive | confermato (s18 test 4–6) |
## Esito
**T2, P3, C4 SOPRAVVIVONO** con fix MINOR (F5B-7, F5B-8, F5B-9). C4 è valido anche per Ω che incontra {x = 0}.
