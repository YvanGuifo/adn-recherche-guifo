#!/usr/bin/env python3
"""
Vérifie qu'un DOI ou PMID existe réellement, avant tout ajout au corpus.

C'est l'outil central du principe de non-fabrication : aucune référence ne doit
entrer dans corpus_articles.csv, grille_extraction.csv ou un .bib sans être passée
par ce script (ou son équivalent CI, voir check_bibtex_dois.py).

Usage :
    python scripts/verification/doi_verify.py 10.1136/bmj.n71
    python scripts/verification/doi_verify.py 33782057          # détecté comme PMID (tout numérique)
    python scripts/verification/doi_verify.py 10.1136/bmj.n71 33782057   # plusieurs identifiants

Code de sortie : 0 si tous les identifiants sont vérifiés, 1 sinon.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import load_settings  # noqa: E402

CROSSREF_API = "https://api.crossref.org/works"
NCBI_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def verify_doi(doi: str, settings: dict) -> dict:
    headers = {"User-Agent": settings["crossref"].get("user_agent", "adn-recherche-guifo/1.0")}
    try:
        r = requests.get(f"{CROSSREF_API}/{doi}", headers=headers, timeout=20)
    except requests.RequestException as e:
        return {"identifiant": doi, "type": "doi", "trouve": False, "erreur": str(e)}

    if r.status_code != 200:
        return {"identifiant": doi, "type": "doi", "trouve": False, "erreur": f"HTTP {r.status_code}"}

    msg = r.json().get("message", {})
    titre = " ".join(msg.get("title", [])) or None
    revue = " ".join(msg.get("container-title", [])) or None
    date_parts = (msg.get("published") or msg.get("published-print") or msg.get("published-online") or {}).get("date-parts", [[None]])
    annee = date_parts[0][0] if date_parts else None

    return {
        "identifiant": doi, "type": "doi", "trouve": True,
        "titre": titre, "revue": revue, "annee": annee,
    }


def verify_pmid(pmid: str, settings: dict) -> dict:
    params = {
        "db": "pubmed", "id": pmid, "retmode": "json",
        "tool": settings["ncbi"]["tool_name"], "email": settings["ncbi"]["email"],
    }
    try:
        r = requests.get(NCBI_ESUMMARY, params=params, timeout=20)
    except requests.RequestException as e:
        return {"identifiant": pmid, "type": "pmid", "trouve": False, "erreur": str(e)}

    if r.status_code != 200:
        return {"identifiant": pmid, "type": "pmid", "trouve": False, "erreur": f"HTTP {r.status_code}"}

    result = r.json().get("result", {})
    doc = result.get(pmid)
    if not doc or doc.get("error"):
        return {"identifiant": pmid, "type": "pmid", "trouve": False, "erreur": "PMID introuvable"}

    return {
        "identifiant": pmid, "type": "pmid", "trouve": True,
        "titre": doc.get("title"), "revue": doc.get("fulljournalname") or doc.get("source"),
        "annee": (doc.get("pubdate") or "").split(" ")[0] or None,
    }


def main():
    parser = argparse.ArgumentParser(description="Vérifie l'existence réelle de DOI/PMID avant ajout au corpus")
    parser.add_argument("identifiants", nargs="+", help="Un ou plusieurs DOI et/ou PMID")
    args = parser.parse_args()

    settings = load_settings()
    all_ok = True

    for ident in args.identifiants:
        ident = ident.strip()
        is_pmid = ident.isdigit()
        result = verify_pmid(ident, settings) if is_pmid else verify_doi(ident, settings)

        if result["trouve"]:
            print(f"✅ {result['type'].upper()} {result['identifiant']} — VÉRIFIÉ")
            print(f"   Titre : {result.get('titre')}")
            print(f"   Revue/Conférence : {result.get('revue')}")
            print(f"   Année : {result.get('annee')}")
        else:
            all_ok = False
            print(f"❌ {result['type'].upper()} {result['identifiant']} — NON VÉRIFIÉ "
                  f"({result.get('erreur', 'introuvable')})")
            print("   ⚠️  Ne pas ajouter cette référence au corpus tant qu'elle n'est pas vérifiée.")
        print()

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
