#!/usr/bin/env python3
"""
Veille PubMed via NCBI E-utilities (esearch + esummary).

Usage :
    python scripts/veille/pubmed_search.py --config axe3_simulation_hybride/veille/queries.yaml --axis axe3

Pour chaque requête définie dans le fichier YAML (clé `pubmed_queries`), ce script :
  1. interroge esearch.fcgi pour obtenir la liste des PMIDs correspondants ;
  2. interroge esummary.fcgi pour récupérer titre, revue, date, DOI de chaque PMID ;
  3. compare au résultat précédent sauvegardé (même id de requête) pour détecter les
     nouveaux PMIDs depuis la dernière exécution ;
  4. sauvegarde le tout dans data/veille_results/pubmed_<axis>_<id>.json.

Respecte les bonnes pratiques NCBI : paramètres tool/email, délai entre requêtes
(cf. https://www.ncbi.nlm.nih.gov/books/NBK25497/).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import load_yaml, load_settings, save_json, load_json_if_exists, today_str  # noqa: E402

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def esearch(query: str, mindate: str, maxdate: str, retmax: int, settings: dict) -> dict[str, Any]:
    params = {
        "db": "pubmed",
        "term": query,
        "datetype": "pdat",
        "mindate": mindate,
        "maxdate": maxdate,
        "retmax": retmax,
        "retmode": "json",
        "tool": settings["ncbi"]["tool_name"],
        "email": settings["ncbi"]["email"],
    }
    if settings["ncbi"].get("api_key"):
        params["api_key"] = settings["ncbi"]["api_key"]
    r = requests.get(f"{EUTILS_BASE}/esearch.fcgi", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def esummary(pmids: list[str], settings: dict) -> dict[str, Any]:
    if not pmids:
        return {"result": {}}
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
        "tool": settings["ncbi"]["tool_name"],
        "email": settings["ncbi"]["email"],
    }
    if settings["ncbi"].get("api_key"):
        params["api_key"] = settings["ncbi"]["api_key"]
    r = requests.get(f"{EUTILS_BASE}/esummary.fcgi", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def extract_doi(article_ids: list[dict]) -> str | None:
    for aid in article_ids or []:
        if aid.get("idtype") == "doi":
            return aid.get("value")
    return None


def run_query(entry: dict, settings: dict, axis: str) -> dict[str, Any]:
    qid = entry["id"]
    rate = settings["ncbi"].get("rate_limit_seconds", 0.4)

    search_res = esearch(
        query=entry["query"],
        mindate=entry.get("mindate", "2000/01/01"),
        maxdate=entry.get("maxdate", "3000/01/01"),
        retmax=entry.get("retmax", 50),
        settings=settings,
    )
    time.sleep(rate)

    idlist = search_res.get("esearchresult", {}).get("idlist", [])
    count = search_res.get("esearchresult", {}).get("count", "0")

    summary_res = esummary(idlist, settings)
    time.sleep(rate)

    articles = []
    result = summary_res.get("result", {})
    for pmid in idlist:
        doc = result.get(pmid)
        if not doc:
            continue
        articles.append({
            "pmid": pmid,
            "title": doc.get("title"),
            "journal": doc.get("fulljournalname") or doc.get("source"),
            "pubdate": doc.get("pubdate"),
            "doi": extract_doi(doc.get("articleids", [])),
        })

    # Diff vs exécution précédente
    result_name = f"pubmed_{axis}_{qid}"
    previous = load_json_if_exists(result_name)
    previous_pmids = {a["pmid"] for a in previous.get("articles", [])} if previous else set()
    new_articles = [a for a in articles if a["pmid"] not in previous_pmids]

    payload = {
        "query_id": qid,
        "nom": entry.get("nom", qid),
        "query": entry["query"],
        "axis": axis,
        "executed_at": today_str(),
        "total_count_pubmed": count,
        "articles": articles,
        "new_articles": new_articles,
    }
    save_json(result_name, payload)
    return payload


def main():
    parser = argparse.ArgumentParser(description="Veille PubMed (NCBI E-utilities)")
    parser.add_argument("--config", required=True, help="Chemin du fichier YAML de requêtes")
    parser.add_argument("--axis", required=True, help="Identifiant de l'axe (ex: axe3)")
    args = parser.parse_args()

    settings = load_settings()
    if settings["ncbi"]["email"] in (None, "", "<À_COMPLETER>"):
        print("⚠️  config/settings.yaml : ncbi.email n'est pas renseigné. "
              "NCBI demande un email valide pour identifier les requêtes automatisées.",
              file=sys.stderr)

    config = load_yaml(args.config)
    queries = config.get("pubmed_queries", [])
    if not queries:
        print(f"Aucune clé 'pubmed_queries' trouvée dans {args.config}", file=sys.stderr)
        sys.exit(1)

    total_new = 0
    n_errors = 0
    for entry in queries:
        print(f"→ Requête {entry['id']} ({entry.get('nom', '')})")
        try:
            result = run_query(entry, settings, args.axis)
        except requests.RequestException as e:
            n_errors += 1
            print(f"  ❌ Échec réseau pour cette requête : {e}", file=sys.stderr)
            continue
        n_new = len(result["new_articles"])
        total_new += n_new
        print(f"  {result['total_count_pubmed']} résultats PubMed au total, "
              f"{len(result['articles'])} récupérés, {n_new} nouveaux depuis la dernière exécution.")

    print(f"\nTerminé. {total_new} nouvel(le)s article(s) au total sur cet axe."
          + (f" ({n_errors} requête(s) en échec réseau)" if n_errors else ""))
    if n_errors == len(queries) and queries:
        sys.exit(1)


if __name__ == "__main__":
    main()
