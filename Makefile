.PHONY: install veille-pubmed veille-arxiv veille-all deadlines digest doi-verify bib-check prisma-flow clean help

help:
	@echo "Cibles disponibles :"
	@echo "  make install        Installer les dépendances Python"
	@echo "  make veille-pubmed  Lancer la veille PubMed (Axe 3 — H1, H4, H6 + veille continue)"
	@echo "  make veille-arxiv   Lancer la veille arXiv (Axe 1+2)"
	@echo "  make veille-all     Les deux veilles ci-dessus"
	@echo "  make deadlines      Afficher l'état des deadlines"
	@echo "  make digest         Générer le digest hebdomadaire (veille + deadlines)"
	@echo "  make prisma-flow    Générer le diagramme de flux PRISMA (compteurs par défaut)"
	@echo "  make doi-verify DOI=10.xxxx/xxxxx   Vérifier un identifiant avant ajout au corpus"
	@echo "  make bib-check BIB=chemin/fichier.bib   Vérifier un export BibTeX"
	@echo "  make clean          Supprimer les résultats de veille locaux (garde les digests)"

install:
	pip install -r requirements.txt

veille-pubmed:
	python scripts/veille/pubmed_search.py --config axe3_simulation_hybride/veille/queries.yaml --axis axe3

veille-arxiv:
	python scripts/veille/arxiv_monitor.py --config axe1_2_native_ia/veille/queries.yaml --axis axe1_2

veille-all: veille-pubmed veille-arxiv

deadlines:
	python scripts/veille/deadline_tracker.py --config config/deadlines.yaml

digest: veille-all deadlines
	python scripts/reporting/weekly_digest.py

prisma-flow:
	python axe3_simulation_hybride/prisma/prisma_flow_diagram.py

doi-verify:
	@if [ -z "$(DOI)" ]; then echo "Usage : make doi-verify DOI=10.xxxx/xxxxx"; exit 1; fi
	python scripts/verification/doi_verify.py $(DOI)

bib-check:
	@if [ -z "$(BIB)" ]; then echo "Usage : make bib-check BIB=chemin/fichier.bib"; exit 1; fi
	python scripts/verification/check_bibtex_dois.py $(BIB) --verify-online

clean:
	find data/veille_results -name "pubmed_*.json" -delete
	find data/veille_results -name "arxiv_*.json" -delete
