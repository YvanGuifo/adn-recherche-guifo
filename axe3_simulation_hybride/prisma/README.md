# Axe 3 — Revue PRISMA : Simulation Hybride en Santé (2020–2026)

Source canonique : `revue_PRISMA_simulation_hybride_sante_2020_2026.docx` (document de référence, à conserver comme source de vérité ; ce dossier en extrait les éléments structurés et exploitables par script).

## État au 22 juin 2026

- **44 articles vérifiés** avec DOI, PMID ou URL institutionnelle confirmée
- **6 emplacements réservés (H1–H6)** — voir `slots_h1_h6.yaml`
- **Grille d'extraction** — voir `grille_extraction.csv`
- **Lacunes majeures identifiées** — voir `lacunes_L1_L6.md`

## ⚠️ Note de transparence (rappel du document source)

> Ce document repose sur 10 requêtes web systématiques. 44 articles ont été vérifiés avec DOI, PMID ou URL institutionnelle confirmée. 6 emplacements (H1-H6) sont explicitement marqués comme « À compléter » car leur inclusion nécessite un accès direct aux bases de données PubMed, Scopus ou Web of Science. **Aucune référence n'a été inventée ou extrapolée.**

Cette règle s'applique à tout ajout futur dans ce dépôt : **toute ligne ajoutée à `corpus_articles.csv` doit avoir un DOI ou PMID vérifié** via `scripts/verification/doi_verify.py` avant intégration.

## Fichiers de ce dossier

| Fichier | Contenu |
|---|---|
| `slots_h1_h6.yaml` | Les 6 requêtes réservées, base de données cible, statut `automatisable` |
| `grille_extraction.csv` | Gabarit vide de la grille d'extraction systématique |
| `corpus_articles.csv` | Gabarit vide du corpus (44 articles vérifiés vivent dans Zotero / le .docx source — ce fichier sert à exporter un sous-ensemble travaillable, jamais à fabriquer des entrées) |
| `lacunes_L1_L6.md` | Les 6 lacunes majeures identifiées dans la littérature, et les axes/papiers qu'elles motivent |
| `prisma_flow_diagram.py` | Génère le diagramme de flux PRISMA 2020 (Identification → Screening → Éligibilité → Inclusion) à partir de compteurs réels |

## Note sur la grille d'extraction

Le document source intitule cette section **« Grille d'Extraction — 21 Dimensions »**, mais 20 champs sont explicitement détaillés dans le tableau correspondant. `grille_extraction.csv` reproduit fidèlement ces 20 champs documentés — aucun 21ᵉ champ n'a été inventé pour combler l'écart. Si vous identifiez le champ manquant dans vos notes originales, ajoutez-le et mettez à jour ce README.

## Champs automatisables vs manuels (slots H1–H6)

| Slot | Base | Automatisable via script |
|---|---|---|
| H1 | PubMed | ✅ `pubmed_search.py` |
| H2 | Scopus | ❌ — pas d'API gratuite ; requête manuelle |
| H3 | Web of Science | ❌ — pas d'API gratuite ; requête manuelle |
| H4 | PubMed | ✅ `pubmed_search.py` |
| H5 | ACM DL / IEEE Xplore | ❌ — pas d'API publique simple ; requête manuelle |
| H6 | PubMed | ✅ `pubmed_search.py` |

Pour H2, H3, H5 : exécuter la requête manuellement sur la plateforme indiquée, puis consigner les résultats vérifiés (DOI/titre/année) directement dans `slots_h1_h6.yaml` sous `articles_trouves`.
