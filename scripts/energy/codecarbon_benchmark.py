#!/usr/bin/env python3
"""
Gabarit de benchmark énergétique (Axe 2 — IA frugale vs deep learning).

Pensé pour mesurer le coût énergétique de pipelines développés pendant la formation
AI Portfolio (ex: RAG frugal vs RAG complexe, petit modèle vs grand modèle), dans le
cadre du principe de "double capitalisation formation -> recherche".

Nécessite : pip install -r requirements-energy.txt (codecarbon)

Usage (à adapter — remplacer `ma_fonction_a_mesurer` par le pipeline réel) :
    python scripts/energy/codecarbon_benchmark.py --label "rag_frugal_v1"
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common import data_dir, today_str  # noqa: E402

try:
    from codecarbon import EmissionsTracker
except ImportError:
    EmissionsTracker = None


def ma_fonction_a_mesurer():
    """
    REMPLACER par l'appel réel à mesurer (ex: pipeline RAG, inférence LLM, batch d'évaluation).
    Le contenu actuel est un placeholder neutre pour que le script reste exécutable
    avant intégration du pipeline réel.
    """
    time.sleep(2)  # simule une charge de travail
    return {"status": "placeholder — remplacer par le pipeline réel"}


def run_benchmark(label: str) -> dict:
    if EmissionsTracker is None:
        print("⚠️  codecarbon n'est pas installé. Lancer : pip install -r requirements-energy.txt",
              file=sys.stderr)
        sys.exit(1)

    tracker = EmissionsTracker(project_name=f"adn-recherche-{label}", log_level="error")
    tracker.start()
    t0 = time.perf_counter()
    try:
        result = ma_fonction_a_mesurer()
    finally:
        emissions_kg = tracker.stop()
    duration_s = time.perf_counter() - t0

    report = {
        "label": label,
        "date": today_str(),
        "duration_seconds": round(duration_s, 3),
        "emissions_kgCO2eq": emissions_kg,
        "result_summary": str(result)[:200],
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Benchmark énergétique (Axe 2)")
    parser.add_argument("--label", required=True, help="Identifiant du run (ex: rag_frugal_v1)")
    args = parser.parse_args()

    report = run_benchmark(args.label)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    out_dir = data_dir() / "energy_benchmarks"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.label}_{report['date']}.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[Rapport sauvegardé dans {out_path}]")


if __name__ == "__main__":
    main()
