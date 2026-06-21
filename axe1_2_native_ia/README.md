# Axe 1+2 — Native-IA Software Engineering & IA Frugale

## État au 22 juin 2026

- **Paper #184** ("Native-IA Software Engineering: Empirical Synthesis and Governance Framework") réentré en review (Industry Showcase Track) depuis le 17 juin 2026.
- **NIER paper** (ICSE 2027, deadline **23 octobre 2026**) : nouveau papier combinant la synthèse empirique de l'Axe 1 et la validation Axe 2, enrichi des observations de la formation AI Portfolio.

## Contenu de ce dossier

| Chemin | Contenu |
|---|---|
| `nier_icse2027/main.tex` | Squelette IEEEtran du NIER paper |
| `nier_icse2027/sections/*.tex` | Sections individuelles avec notes de phase (quand rédiger quoi) |
| `nier_icse2027/references.bib` | Bibliographie reprenant les 21 références déjà vérifiées du papier #184 |
| `veille/queries.yaml` | Requêtes arXiv automatisables (`scripts/veille/arxiv_monitor.py`) |

## Compiler le NIER paper

```bash
cd axe1_2_native_ia/nier_icse2027
latexmk -pdf main.tex
# ou, sans latexmk :
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Avant d'ajouter une référence

Toujours vérifier l'identifiant avant de l'ajouter à `references.bib` :

```bash
python ../../scripts/verification/doi_verify.py 10.xxxx/xxxxx
```

Puis valider l'ensemble du fichier :

```bash
python ../../scripts/verification/check_bibtex_dois.py references.bib --verify-online
```
