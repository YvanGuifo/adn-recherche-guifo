# ADN de Recherche — A. Yvan GUIFO FODJO

Dépôt opérationnel pour la recherche, la veille scientifique et la production académique, organisé autour de trois axes de recherche, d'une formation en cours et d'une activité d'enseignement.

**Identité scientifique** : Ingénierie et modélisation du numérique responsable — génie logiciel, IA frugale/explicable, simulation hybride appliquée à la santé.

---

## 🎯 État au 22 juin 2026

| Élément | Statut |
|---|---|
| Paper #184 (Native-IA SE) | Réentré en review depuis le 17/06/2026 |
| NIER paper — ICSE 2027 | En préparation — **deadline 23 octobre 2026** |
| JSS Special Issue | Cible secondaire, conditionnelle (après notification NIER) |
| Revue PRISMA (Axe 3) | 44 articles vérifiés, 6 slots H1–H6 à compléter |
| Formation AI Portfolio | 12 semaines, juin–septembre 2026 |

---

## 📂 Structure du dépôt

```
.
├── axe1_2_native_ia/         Axe 1+2 — Native-IA SE & IA frugale
│   ├── nier_icse2027/        Squelette LaTeX IEEEtran du NIER paper
│   └── veille/queries.yaml   Requêtes arXiv automatisées
├── axe3_simulation_hybride/  Axe 3 — Simulation hybride en santé
│   ├── prisma/                Slots H1-H6, grille d'extraction, lacunes L1-L6
│   └── veille/queries.yaml   Requêtes PubMed automatisées
├── scripts/
│   ├── veille/                pubmed_search.py, arxiv_monitor.py, deadline_tracker.py
│   ├── verification/          doi_verify.py, check_bibtex_dois.py  ← anti-fabrication
│   ├── energy/                 codecarbon_benchmark.py (Axe 2)
│   └── reporting/             weekly_digest.py
├── config/                    settings.yaml, deadlines.yaml
├── data/veille_results/       Résultats de veille horodatés (JSON + digests Markdown)
├── planning/                  Planning HTML interactif (18 semaines)
├── .github/workflows/         Automatisation (veille hebdo, alertes deadlines)
└── docs/                      Version Markdown de l'ADN de recherche
```

---

## 🚀 Démarrage rapide

```bash
git clone <url-de-votre-repo>
cd adn-recherche-guifo
make install
```

Avant la première utilisation, compléter dans `config/settings.yaml` :
- votre email (requis par NCBI E-utilities et recommandé par les bonnes pratiques arXiv/CrossRef).

```bash
# Lancer toute la veille (PubMed Axe 3 + arXiv Axe 1+2)
make veille-all

# Vérifier l'état des deadlines
make deadlines

# Générer le digest complet (veille + deadlines en un seul rapport Markdown)
make digest

# Vérifier un DOI/PMID avant de l'ajouter à un corpus — ÉTAPE OBLIGATOIRE
make doi-verify DOI=10.1136/bmj.n71

# Vérifier un export BibTeX (Zotero + Better BibTeX) avant import
make bib-check BIB=axe1_2_native_ia/nier_icse2027/references.bib
```

---

## 🤖 Automatisation (GitHub Actions)

Une fois ce dépôt poussé sur GitHub, deux workflows s'activent automatiquement :

| Workflow | Fréquence | Action |
|---|---|---|
| `veille-hebdo.yml` | Tous les lundis 7h UTC | Lance PubMed + arXiv, génère un digest, commit les résultats, **ouvre une issue GitHub** avec le rapport complet |
| `deadline-check.yml` | Tous les jours 6h UTC | Vérifie les deadlines ; **ouvre une issue "🚨 urgent"** si une échéance tombe sous 7 jours |

Ces deux workflows peuvent aussi être déclenchés manuellement depuis l'onglet **Actions** de GitHub (`workflow_dispatch`).

➡️ **Créer les labels `veille` et `urgent`** dans Issues → Labels avant la première exécution, pour que les commandes `gh issue create --label` ne soient pas bloquées (un message d'avertissement non bloquant s'affichera sinon).

---

## ⚠️ Principe de non-fabrication

Ce dépôt encode comme **contrainte technique, pas seulement comme bonne intention**, la règle suivie depuis le début de la revue PRISMA :

> Aucune référence n'est incluse sans DOI ou PMID vérifié. Aucun résultat sans données réelles.

Concrètement :

- `scripts/verification/doi_verify.py` interroge CrossRef (DOI) ou PubMed (PMID) en temps réel — code de sortie ≠ 0 si l'identifiant n'existe pas.
- `scripts/verification/check_bibtex_dois.py` audite un fichier `.bib` entier et signale toute entrée sans identifiant vérifiable.
- Les slots PRISMA H1–H6 (`axe3_simulation_hybride/prisma/slots_h1_h6.yaml`) restent à `statut: "à compléter"` tant qu'aucun article vérifié n'y est rattaché — jamais remplis par extrapolation.
- `prisma_flow_diagram.py` affiche explicitement *"à compléter"* pour tout compteur non encore saisi, plutôt que d'inventer un total.

---

## 📊 Les 3 axes + l'enseignement

| Axe | Focus | Cible éditoriale |
|---|---|---|
| **Axe 1** | Génie logiciel durable | JSS / IEEE Software (via NIER) |
| **Axe 2** | IA frugale, explicable | Pattern Recognition / KBS (idée) |
| **Axe 3** | Simulation hybride santé | Nature Sustainability / J. Simulation |
| **Formation** | AI Solutions Engineer & FDE | Double capitalisation → matériau empirique pour Axe 1+2 |
| **Enseignement** | Cours/syllabus 2026-2027 | 2h/jour, lundi-vendredi (voir `planning/`) |

Voir `docs/adn_recherche.md` pour la version complète et narrative de l'ADN de recherche, et `planning/ADN_Recherche_Planning_GUIFO_2026.html` pour le planning interactif jour par jour (18 semaines, à ouvrir dans un navigateur).

---

## 🛠️ Outils & ressources

- **Bibliographie** : Zotero 7 + Better BibTeX (export `.bib` → vérifié par `check_bibtex_dois.py` avant import)
- **Rédaction** : LaTeX (IEEEtran, Overleaf-compatible), DOCX pour la planification
- **Automatisation** : Python (NCBI E-utilities, arXiv API, CrossRef API, CodeCarbon)
- **Suivi deadlines** : `config/deadlines.yaml` (maintenu manuellement, vérifié contre se-deadlines.github.io / conf.researchr.org)
- **Versioning** : Git + GitHub Actions

---

## 📜 Licence

Code sous licence MIT (voir `LICENSE`). Les contenus académiques (manuscrits, revue PRISMA) restent la propriété de l'auteur jusqu'à publication — voir la clarification dans `LICENSE`.
