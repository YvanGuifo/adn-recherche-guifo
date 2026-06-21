# ADN de Recherche et Stratégie Scientifique Intégrée

**A. Yvan GUIFO FODJO** — Docteur en Informatique (Sorbonne Université / LIP6), Enseignant-Chercheur (EFREI Paris / Université Paris-Panthéon-Assas)

*Version Markdown — dérivée de `ADN_Recherche_v2_GUIFO_2026.docx`. Le .docx reste la version de référence pour diffusion formelle ; ce fichier sert de version consultable et versionnée dans le dépôt.*

---

## 1. Identité scientifique

Ingénierie et modélisation du numérique responsable, combinant génie logiciel, modélisation mathématique et intelligence artificielle interprétable, appliquées aux enjeux de santé publique et de développement durable.

**Piliers structurants :**
- P1 — Pensée systémique et modélisation formelle
- P2 — Responsabilité environnementale du numérique
- P3 — IA frugale, interprétable et explicable
- P4 — Génie logiciel comme levier central de durabilité
- P5 — Impact sociétal mesurable (santé, politiques publiques)

---

## 2. Les trois axes de recherche

### Axe 1 — Ingénierie logicielle et numérique durable
Conception, modélisation et évaluation de systèmes logiciels durables sous contraintes environnementales et sociétales.

### Axe 2 — IA responsable, frugale et explicable
IA frugale, interprétable et responsable pour l'aide à la décision. Sert de couche de validation empirique pour l'Axe 1.

### Axe 3 — Modélisation et simulation de systèmes socio-techniques
Modélisation et simulation de systèmes complexes pour la santé et le développement durable. Matérialisé par la revue PRISMA 2020-2026 (voir `axe3_simulation_hybride/prisma/`).

---

## 3. Formation AI Portfolio — intégration stratégique

La formation « AI Solutions Engineer & FDE » (12 semaines, juin–septembre 2026) n'est pas une activité parallèle : c'est un accélérateur pour les Axes 1 et 2, via la **règle de double capitalisation** :

> Chaque livrable de la formation doit être documenté avec une perspective recherche (mesures d'énergie, traçabilité des artefacts, observations cognitives). Ce matériau empirique alimente directement le NIER paper.

| Sprint | Contenu | Synergie recherche |
|---|---|---|
| 1 (S1-S4) | Prompt engineering, LangChain, Docker, Azure OpenAI | Architecture pipelines GenAI → framework Native-IA |
| 2 (S5-S8) | RAG avancé, multi-agents (LangGraph), LangSmith, sécurité LLM, certification AI-103 | Orchestration agents, observabilité, validation sémantique |
| 3 (S9-S12) | Projet Enterprise AI Assistant (FDE end-to-end) | Cas d'étude validant le cadre de gouvernance NIER |

---

## 4. Planning phasé — 18 semaines vers ICSE NIER

| Phase | Semaines | Dates | Jalon |
|---|---|---|---|
| 1 — Fondations & Cadrage | S1-S4 | 22 juin – 19 juillet | Squelette NIER v0.1, 2 slots PRISMA |
| 2 — Montée en puissance | S5-S8 | 20 juillet – 16 août | NIER draft v1, AI-103, 4/6 slots |
| 3 — Convergence | S9-S12 | 17 août – 13 septembre | NIER draft v2 relu, formation terminée, 6/6 slots |
| 4 — Sprint final NIER | S13-S18 | 14 septembre – 23 octobre | **Soumission ICSE 2027 NIER** |

Planning détaillé jour par jour : `planning/ADN_Recherche_Planning_GUIFO_2026.html`.

---

## 5. Principes opérationnels

1. **Non-fabrication (règle absolue)** — aucune référence sans DOI/PMID vérifié, aucun résultat sans données réelles. Outillé par `scripts/verification/`.
2. **Stratégie cascade** — NIER d'abord ; décision JSS Special Issue après notification NIER.
3. **Vérifiabilité avant complétude** — 44 articles vérifiés valent mieux que 50 avec des références douteuses.
4. **Double capitalisation formation-recherche** — chaque projet de formation documenté avec perspective recherche.
5. **Dialogue stratégique avant matérialisation** — clarification → décision confirmée → production.

---

## 6. Roadmap publications

| Axe | Papier | Cible | Deadline | Statut |
|---|---|---|---|---|
| 1+2 | Native-IA SE: Empirical Synthesis and Governance Framework | Industry Showcase Track | — | En review (réentré 17/06/2026) |
| 1+2 | NIER Paper | ICSE 2027 NIER | 23/10/2026 | En rédaction — **primaire** |
| 1+2 | Extended paper | JSS Special Issue | 31/01/2027 | Conditionnel — secondaire |
| 3 | Revue PRISMA simulation hybride santé | J. Simulation / Nature Sustainability | Q4 2026 (indicatif) | Corpus 44/50 |
| 2 | IA frugale vs deep learning — benchmark énergétique | Pattern Recognition / KBS | Q1 2027 (indicatif) | Idée |

---

## 7. Outils & ressources

- **Bibliographie** : Zotero 7 + Better BibTeX
- **Rédaction** : LaTeX (IEEEtran, Overleaf), DOCX pour planification
- **Automatisation** : Python — NCBI E-utilities, arXiv API, CrossRef API, CodeCarbon
- **Suivi deadlines** : `config/deadlines.yaml`, vérifié contre se-deadlines.github.io / conf.researchr.org
- **Versioning** : Git + GitHub Actions (ce dépôt)

---

## 8. Lacunes scientifiques identifiées (Axe 3, alimentent aussi Axe 1/2)

Voir `axe3_simulation_hybride/prisma/lacunes_L1_L6.md` pour le détail complet (L1 fragmentation méthodologique, L2 absence d'intégration SDLC, L3 XAI marginale, L4 frugalité non mesurée, L5 faible reproductibilité, L6 LMIC sous-représentés).
