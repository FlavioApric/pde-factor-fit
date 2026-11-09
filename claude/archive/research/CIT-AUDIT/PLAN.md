# PLAN — CIT-AUDIT (chiusura Fase 1, prima del Gate 1)

## 1. Domande
- Q1 (esistenza): ogni voce dei 15 `research/*/sources.bib` esiste all'arXiv ID / DOI / sede dichiarati?
- Q2 (metadati): autori, anno, titolo, rivista, volume, pagine sono corretti?
- Q3 (contesto): per i riferimenti su cui poggiano risultati chiave, il teorema/proposizione citato nel REPORT.md dice davvero ciò che il REPORT afferma (numerazione inclusa)?
- Esito per voce: VERIFICATO / METADATI ERRATI (+correzione) / NON TROVATO / CONTESTO NON SUPPORTATO.

## 2. Skill caricate (Regola 2) e uso
- `_vendor/Auto-claude-code-research-in-sleep/skills/citation-audit/SKILL.md` (letto con Read): workflow a tre livelli esistenza/metadati/contesto, verdetti KEEP/FIX/REPLACE/REMOVE mappati sulle 4 categorie richieste. Revisore Codex ESCLUSO (decisione utente): le verifiche le faccio io.
- `_vendor/scientific-agent-skills/skills/citation-management/SKILL.md` (letto): Crossref/arXiv/DOI come fonti canoniche dei metadati, controllo duplicati.
- `_vendor/scientific-agent-skills/skills/paper-lookup/SKILL.md` (letto): endpoint documentati (Crossref `api.crossref.org/works/<doi>`, arXiv `export.arxiv.org/api/query?id_list=`), cautela sulle risposte 200 "vuote".
- Nessuno script `_vendor` eseguito. Uso solo script miei (python -I nel venv) che interrogano Crossref/arXiv.

## 3. Fonti / procedura
1. Parsing di tutti i `sources.bib` → tabella (agente, chiave, tipo, autori, titolo, anno, sede, DOI, eprint).
2. Livello 1–2 automatico: DOI → Crossref; eprint → arXiv API; confronto titolo/anno/autori/volume.
3. Voci senza identificatori: ricerca Crossref bibliografica (`query.bibliographic`) + WebSearch per libri (zbMATH/editori).
4. Livello 3 (contesto) sui riferimenti PRIORITARI (elenco nel compito: Scholl et al. 2210.08342, He–Zhao–Zhong FoCM 24, Rosenbloom–Widder, Hörmander 7.6.13/14, Oberst 1990, Malgrange 1956, Crawley-Boevey 2003, Rapisarda–Antoulas 2016, Pierce 1979, Wei–Norman 1963/64, Jahnke–Lubich 2000, Casas–Murua–Nadinić 2012, Donoho–Kutyniok 2013, Schiebinger–Robeva–Recht 2018, Stanhope–Rubin–Swigon 2014, Efendiev–Vabishchevich 2008.08111, Robeva 2016, Engel–Nagel, Pazy, Zettl, Higham, Miller 1977): grep dei REPORT.md per l'uso, poi lettura dell'abstract/testo (arXiv) o delle fonti accessibili.
5. Manuali classici: verifica a campione.

## 4. Comunicazione
- Letta inbox/CIT-AUDIT.md (vuota). Output: AVVISO in `inbox/<ID>.md` per ogni agente con errori (registro per Fase 3); `PLAN-READY CIT-AUDIT` e `DONE CIT-AUDIT` in inbox/central.md. Non modifico file di altri agenti.

## 5. Criterio di fatto
- Tutte le voci con DOI/eprint controllate automaticamente; tutte le prioritarie controllate a mano su 3 livelli; voci senza identificatori controllate (o a campione per i manuali classici, dichiarato).
- Consegnati `AUDIT.md`, `sources_verified.bib`, AVVISI, DONE.
