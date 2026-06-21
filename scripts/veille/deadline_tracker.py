#!/usr/bin/env python3
"""
Suivi des deadlines (config/deadlines.yaml) avec calcul d'urgence.

Usage :
    python scripts/veille/deadline_tracker.py --config config/deadlines.yaml
    python scripts/veille/deadline_tracker.py --config config/deadlines.yaml --alert-threshold 7 --github-output

Catégories d'urgence (jours restants) :
    > 60       -> ok
    30 - 60    -> a_surveiller
    7 - 30     -> urgent
    < 7        -> critique
    null/passé -> sans_date / depassee
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import load_yaml, write_github_output  # noqa: E402


def categorize(jours: int | None) -> str:
    if jours is None:
        return "sans_date"
    if jours < 0:
        return "depassee"
    if jours < 7:
        return "critique"
    if jours < 30:
        return "urgent"
    if jours < 60:
        return "a_surveiller"
    return "ok"


EMOJI = {
    "critique": "🔴",
    "urgent": "🟠",
    "a_surveiller": "🟡",
    "ok": "🟢",
    "sans_date": "⚪",
    "depassee": "⚫",
}


def build_table(deadlines: list[dict]) -> tuple[str, list[dict]]:
    """Retourne (markdown_table, liste_enrichie_avec_urgence)."""
    today = date.today()
    rows = []
    for dl in deadlines:
        date_str = dl.get("date")
        jours = None
        if date_str:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            jours = (d - today).days
        urgence = categorize(jours)
        rows.append({**dl, "jours_restants": jours, "urgence": urgence})

    # Tri : urgence décroissante (critique d'abord), puis par date
    ordre_urgence = {"critique": 0, "urgent": 1, "a_surveiller": 2, "ok": 3, "sans_date": 4, "depassee": 5}
    rows.sort(key=lambda r: (ordre_urgence[r["urgence"]], r["jours_restants"] if r["jours_restants"] is not None else 9999))

    lines = ["| Statut | Échéance | Date | Jours restants | Axe | Priorité |",
             "|---|---|---|---|---|---|"]
    for r in rows:
        emoji = EMOJI[r["urgence"]]
        jours_txt = f"{r['jours_restants']} j" if r["jours_restants"] is not None else "—"
        date_txt = r.get("date") or "non fixée"
        lines.append(f"| {emoji} | {r['nom']} | {date_txt} | {jours_txt} | {r.get('axe','—')} | {r.get('priorite','—')} |")

    return "\n".join(lines), rows


def main():
    parser = argparse.ArgumentParser(description="Suivi des deadlines")
    parser.add_argument("--config", default="config/deadlines.yaml")
    parser.add_argument("--alert-threshold", type=int, default=7,
                         help="Seuil en jours pour considérer une deadline comme critique")
    parser.add_argument("--github-output", action="store_true",
                         help="Écrit critical/message dans $GITHUB_OUTPUT (pour Actions)")
    args = parser.parse_args()

    config = load_yaml(args.config)
    deadlines = config.get("deadlines", [])
    table, rows = build_table(deadlines)

    print(table)

    critiques = [r for r in rows if r["urgence"] == "critique"]

    if args.github_output:
        is_critical = "true" if critiques else "false"
        message = "\n".join(
            f"- **{r['nom']}** : {r['jours_restants']} jour(s) restant(s) (échéance {r['date']})"
            for r in critiques
        ) or "Aucune deadline critique actuellement."
        write_github_output("critical", is_critical)
        write_github_output("message", message)

    return table


if __name__ == "__main__":
    main()
