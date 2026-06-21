#!/usr/bin/env python3
"""
Compile un digest hebdomadaire Markdown à partir des derniers résultats de veille
(PubMed, arXiv) et de l'état des deadlines. Sauvegardé dans
data/veille_results/digest_<date>.md — c'est ce fichier qui est posté comme issue
GitHub par le workflow .github/workflows/veille-hebdo.yml.

Usage :
    python scripts/reporting/weekly_digest.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import data_dir, load_yaml, save_json, today_str  # noqa: E402
from veille.deadline_tracker import build_table  # noqa: E402


def collect_new_items(prefix: str) -> list[dict]:
    """Parcourt data/veille_results/<prefix>_*.json et agrège les new_articles."""
    items = []
    for path in sorted(data_dir().glob(f"{prefix}_*.json")):
        import json
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        for art in payload.get("new_articles", []):
            items.append({**art, "_source_query": payload.get("nom"), "_query_id": payload.get("query_id")})
    return items


def section_deadlines() -> str:
    config = load_yaml("config/deadlines.yaml")
    table, _ = build_table(config.get("deadlines", []))
    return f"## 🚨 Deadlines\n\n{table}\n"


def section_new_pubmed() -> str:
    items = collect_new_items("pubmed")
    if not items:
        return "## 🆕 Nouvelles références PubMed (Axe 3)\n\nAucune nouvelle référence depuis la dernière exécution.\n"
    lines = ["## 🆕 Nouvelles références PubMed (Axe 3)\n"]
    for it in items:
        doi_txt = f" — DOI: {it['doi']}" if it.get("doi") else f" — PMID: {it['pmid']}"
        lines.append(f"- **[{it['_query_id']}]** {it.get('title')} ({it.get('journal')}, {it.get('pubdate')}){doi_txt}")
    return "\n".join(lines) + "\n"


def section_new_arxiv() -> str:
    items = collect_new_items("arxiv")
    if not items:
        return "## 🆕 Nouveaux preprints arXiv (Axe 1+2)\n\nAucun nouveau preprint depuis la dernière exécution.\n"
    lines = ["## 🆕 Nouveaux preprints arXiv (Axe 1+2)\n"]
    for it in items:
        lines.append(f"- **[{it['_query_id']}]** {it.get('title')} — {it.get('link')}")
    return "\n".join(lines) + "\n"


def section_corpus_status() -> str:
    try:
        slots = load_yaml("axe3_simulation_hybride/prisma/slots_h1_h6.yaml").get("slots", {})
        n_done = sum(1 for s in slots.values() if s.get("statut") == "complété")
        lines = ["## 📊 État du corpus PRISMA (Axe 3)\n",
                  f"- Slots H1–H6 complétés : **{n_done}/6**",
                  ""]
        for sid, s in slots.items():
            etat = "✅" if s.get("statut") == "complété" else "⏳"
            lines.append(f"  - {etat} **{sid}** ({s['base']}) — {s.get('domaine')}")
        return "\n".join(lines) + "\n"
    except FileNotFoundError:
        return ""


def main():
    date_str = today_str()
    parts = [
        f"# 📡 Digest de veille hebdomadaire — {date_str}\n",
        section_deadlines(),
        section_new_pubmed(),
        section_new_arxiv(),
        section_corpus_status(),
        "---\n_Généré automatiquement par `scripts/reporting/weekly_digest.py`._",
    ]
    digest = "\n".join(parts)

    out_path = data_dir() / f"digest_{date_str}.md"
    out_path.write_text(digest, encoding="utf-8")

    print(digest)
    print(f"\n[Digest sauvegardé dans {out_path}]")


if __name__ == "__main__":
    main()
