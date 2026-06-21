#!/usr/bin/env python3
"""
Veille arXiv via l'API officielle (export.arxiv.org/api/query, flux Atom).

Usage :
    python scripts/veille/arxiv_monitor.py --config axe1_2_native_ia/veille/queries.yaml --axis axe1_2

Respecte les Terms of Use arXiv : délai recommandé entre requêtes (par défaut 3s,
cf. config/settings.yaml -> arxiv.rate_limit_seconds), User-Agent identifiable.
Référence : https://info.arxiv.org/help/api/user-manual.html
"""
from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any

import feedparser
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import load_yaml, load_settings, save_json, load_json_if_exists, today_str  # noqa: E402

ARXIV_API = "https://export.arxiv.org/api/query"


def query_arxiv(entry: dict, settings: dict) -> list[dict[str, Any]]:
    params = {
        "search_query": entry["search_query"],
        "start": 0,
        "max_results": entry.get("max_results", 20),
        "sortBy": entry.get("sort_by", "submittedDate"),
        "sortOrder": entry.get("sort_order", "descending"),
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": settings["arxiv"].get("user_agent", "adn-recherche-guifo/1.0")}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    feed = feedparser.parse(r.text)

    results = []
    for e in feed.entries:
        arxiv_id = e.get("id", "").split("/abs/")[-1]
        results.append({
            "arxiv_id": arxiv_id,
            "title": " ".join(e.get("title", "").split()),
            "authors": [a.get("name") for a in e.get("authors", [])],
            "published": e.get("published"),
            "summary": " ".join(e.get("summary", "").split())[:500],
            "link": e.get("link"),
        })
    return results


def run_query(entry: dict, settings: dict, axis: str) -> dict[str, Any]:
    qid = entry["id"]
    articles = query_arxiv(entry, settings)

    result_name = f"arxiv_{axis}_{qid}"
    previous = load_json_if_exists(result_name)
    previous_ids = {a["arxiv_id"] for a in previous.get("articles", [])} if previous else set()
    new_articles = [a for a in articles if a["arxiv_id"] not in previous_ids]

    payload = {
        "query_id": qid,
        "nom": entry.get("nom", qid),
        "search_query": entry["search_query"],
        "axis": axis,
        "executed_at": today_str(),
        "articles": articles,
        "new_articles": new_articles,
    }
    save_json(result_name, payload)
    return payload


def main():
    parser = argparse.ArgumentParser(description="Veille arXiv")
    parser.add_argument("--config", required=True, help="Chemin du fichier YAML de requêtes")
    parser.add_argument("--axis", required=True, help="Identifiant de l'axe (ex: axe1_2)")
    args = parser.parse_args()

    settings = load_settings()
    config = load_yaml(args.config)
    queries = config.get("arxiv_queries", [])
    if not queries:
        print(f"Aucune clé 'arxiv_queries' trouvée dans {args.config}", file=sys.stderr)
        sys.exit(1)

    rate = settings["arxiv"].get("rate_limit_seconds", 3.0)
    total_new = 0
    n_errors = 0
    for i, entry in enumerate(queries):
        print(f"→ Requête {entry['id']} ({entry.get('nom', '')})")
        try:
            result = run_query(entry, settings, axis=args.axis)
        except requests.RequestException as e:
            n_errors += 1
            print(f"  ❌ Échec réseau pour cette requête : {e}", file=sys.stderr)
        else:
            n_new = len(result["new_articles"])
            total_new += n_new
            print(f"  {len(result['articles'])} résultats récupérés, {n_new} nouveaux depuis la dernière exécution.")
        if i < len(queries) - 1:
            time.sleep(rate)

    print(f"\nTerminé. {total_new} nouvel(le)s preprint(s) au total sur cet axe."
          + (f" ({n_errors} requête(s) en échec réseau)" if n_errors else ""))
    if n_errors == len(queries) and queries:
        sys.exit(1)


if __name__ == "__main__":
    main()
