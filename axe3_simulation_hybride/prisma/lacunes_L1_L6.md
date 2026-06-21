# Lacunes majeures identifiées — Revue PRISMA Simulation Hybride en Santé

Source : `revue_PRISMA_simulation_hybride_sante_2020_2026.docx`, section 4.2.

## Les 6 lacunes

- **L1 — Fragmentation méthodologique** : durabilité, frugalité et explicabilité sont traitées de manière isolée dans tous les articles recensés.
- **L2 — Absence d'intégration SDLC** : aucun article ne couvre explicitement toutes les phases du cycle de vie logiciel.
- **L3 — XAI marginale** : l'explicabilité n'est intégrée que dans moins de 10 % des articles, et jamais comme contrainte de conception.
- **L4 — Frugalité computationnelle non mesurée** : le coût énergétique des modèles hybrides n'est reporté dans aucun article identifié.
- **L5 — Faible reproductibilité** : moins de 30 % des articles publient leur code source ou leurs données.
- **L6 — Pays à revenus faibles sous-représentés** : moins de 5 % des études portent sur des contextes LMIC (Cassidy et al., 2020).

## Distribution par paradigmes hybrides (synthèse thématique du corpus actuel)

| Combinaison | Nb articles | Outil dominant | Tendance | Lacune associée |
|---|---|---|---|---|
| DES + ABM | ~18 | AnyLogic | Urgences, EMS, COVID | XAI absente |
| SD + ABM | ~12 | AnyLogic | Épidémiologie, maisons de soins | Frugalité non mesurée |
| DES + SD + ABM | ~8 | AnyLogic | Multi-échelle COVID-19 | Coût computationnel non rapporté |
| Hybride + ML | ~6 | Python/Multiple | Tendance émergente 2024-2025 | Standards métriques absents |
| Digital Twin (hybride) | ~3 | Multiple | Oncologie, jumeau numérique | Intégration SDLC absente |

## Opportunités de publication alignées sur les axes

| Axe | Idée papier | Lacune adressée | Revue cible | Statut |
|---|---|---|---|---|
| Axe 1 | Cadre méthodologique unifié : SDLC + durabilité + IA frugale | L1, L2 | JSS / IEEE Software | En cours |
| Axe 2 | IA frugale vs deep learning : benchmark énergétique sur modèles santé | L3, L4 | Pattern Recognition / KBS | Idée |
| Axe 3 | Modélisation hybride SD+ABM maladies chroniques + durabilité | L5, L6 | Nature Sustainability / J. Simulation | Préliminaire |

Ces chiffres (~18, ~12, ~8...) sont des ordres de grandeur reportés dans le document source sur le corpus de 44 articles vérifiés ; ils seront à recalculer précisément une fois la grille d'extraction (`grille_extraction.csv`) remplie article par article.
