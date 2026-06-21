#!/usr/bin/env python3
"""
Vérifie un export BibTeX (Zotero + Better BibTeX) avant import dans le corpus.

Signale toute entrée sans champ doi/pmid/url institutionnelle — candidate à exclure
ou à compléter avant intégration, conformément au principe de non-fabrication.

Usage :
    python scripts/verification/check_bibtex_dois.py mon_export.bib
    python scripts/verification/check_bibtex_dois.py mon_export.bib --verify-online

Avec --verify-online, chaque DOI présent est en plus vérifié via CrossRef
(scripts/verification/doi_verify.py) pour détecter les DOI mal formés ou fantômes.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import load_settings  # noqa: E402
from doi_verify import verify_doi  # noqa: E402

ENTRY_RE = re.compile(r"@(\w+)\{([^,]+),", re.IGNORECASE)
FIELD_RE = re.compile(r"(\w+)\s*=\s*[{\"]([^}\"]*)[}\"]", re.IGNORECASE)


def parse_bib(text: str) -> list[dict]:
    """Parseur BibTeX minimal — suffisant pour vérifier la présence de champs clés.
    Pour un usage avancé, préférer `bibtexparser`, non requis ici pour rester léger."""
    entries = []
    # Découpe grossière par entrée @type{...}
    chunks = re.split(r"(?=@\w+\{)", text)
    for chunk in chunks:
        m = ENTRY_RE.search(chunk)
        if not m:
            continue
        entry_type, entry_key = m.group(1), m.group(2).strip()
        fields = {k.lower(): v.strip() for k, v in FIELD_RE.findall(chunk)}
        entries.append({"type": entry_type, "key": entry_key, "fields": fields})
    return entries


def main():
    parser = argparse.ArgumentParser(description="Vérifie les DOI/PMID d'un export BibTeX")
    parser.add_argument("bib_path", help="Chemin du fichier .bib à vérifier")
    parser.add_argument("--verify-online", action="store_true",
                         help="Vérifie en plus chaque DOI trouvé via CrossRef")
    args = parser.parse_args()

    path = Path(args.bib_path)
    if not path.exists():
        print(f"Fichier introuvable : {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    entries = parse_bib(text)

    if not entries:
        print("Aucune entrée BibTeX détectée — vérifier le format du fichier.")
        sys.exit(1)

    settings = load_settings() if args.verify_online else None
    n_missing = 0
    n_doi_invalid = 0

    print(f"{len(entries)} entrée(s) trouvée(s) dans {path.name}\n")

    for e in entries:
        doi = e["fields"].get("doi")
        pmid = e["fields"].get("pmid") or e["fields"].get("eprint")
        key = e["key"]

        if not doi and not pmid:
            n_missing += 1
            print(f"⚠️  [{key}] AUCUN identifiant vérifiable (ni doi, ni pmid) "
                  f"— titre: {e['fields'].get('title', '?')[:80]}")
            continue

        if doi and args.verify_online:
            result = verify_doi(doi, settings)
            if not result["trouve"]:
                n_doi_invalid += 1
                print(f"❌ [{key}] DOI présent mais non vérifié auprès de CrossRef : {doi}")
            else:
                print(f"✅ [{key}] DOI vérifié : {doi}")
        else:
            print(f"✓  [{key}] identifiant présent (doi={doi or '—'}, pmid={pmid or '—'})")

    print(f"\nRésumé : {len(entries)} entrées, {n_missing} sans identifiant"
          + (f", {n_doi_invalid} DOI invalides en ligne" if args.verify_online else ""))

    sys.exit(1 if (n_missing or n_doi_invalid) else 0)


if __name__ == "__main__":
    main()
