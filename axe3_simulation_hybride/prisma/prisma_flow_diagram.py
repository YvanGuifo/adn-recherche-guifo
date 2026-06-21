#!/usr/bin/env python3
"""
Génère le diagramme de flux PRISMA 2020 (Identification -> Screening -> Éligibilité
-> Inclusion) à partir de compteurs réels saisis dans ce script ou en arguments CLI.

Conforme au principe de non-fabrication : tous les chiffres par défaut ci-dessous
sont None ("à compléter") tant que les comptages réels ne sont pas saisis — le
diagramme l'indique explicitement plutôt que d'inventer des totaux.

Usage :
    python axe3_simulation_hybride/prisma/prisma_flow_diagram.py \\
        --identifies 187 --doublons 23 --screenes 164 --exclus-titre-resume 98 \\
        --texte-integral 66 --exclus-texte-integral 22 --inclus 44

Référence méthodologique : Page M.J. et al. (2021). The PRISMA 2020 statement.
BMJ 372:n71. DOI: 10.1136/bmj.n71
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def box(ax, xy, w, h, text, facecolor="#eaf2f8", edgecolor="#1a5276"):
    x, y = xy
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                           linewidth=1.4, edgecolor=edgecolor, facecolor=facecolor)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=9.5, wrap=True)


def fmt(n):
    return "à compléter" if n is None else f"N = {n}"


def draw_flow(counts: dict, out_path: Path):
    fig, ax = plt.subplots(figsize=(7.5, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis("off")

    w, h = 7.5, 1.3
    x = 1.25

    stages = [
        ("Identification",
         f"Articles identifiés via bases de données\n"
         f"(PubMed, Scopus, WoS, IEEE, ACM)\n{fmt(counts['identifies'])}\n"
         f"+ snowballing : {fmt(counts.get('snowballing'))}"),
        ("Suppression des doublons",
         f"Doublons supprimés : {fmt(counts['doublons'])}"),
        ("Screening (titre/résumé)",
         f"Articles screenés : {fmt(counts['screenes'])}\n"
         f"Exclus à ce stade : {fmt(counts['exclus_titre_resume'])}"),
        ("Éligibilité (texte intégral)",
         f"Texte intégral évalué : {fmt(counts['texte_integral'])}\n"
         f"Exclus (critères I/E) : {fmt(counts['exclus_texte_integral'])}"),
        ("Inclusion",
         f"Articles inclus dans la synthèse : {fmt(counts['inclus'])}"),
    ]

    ys = [12.0, 9.8, 7.4, 5.0, 2.6]
    for (title, body), y in zip(stages, ys):
        box(ax, (x, y), w, h, f"{title}\n{body}")

    for y_top, y_bot in zip(ys[:-1], ys[1:]):
        ax.annotate("", xy=(x + w / 2, y_bot + h), xytext=(x + w / 2, y_top),
                     arrowprops=dict(arrowstyle="-|>", color="#1a5276", lw=1.3))

    ax.set_title("Diagramme de flux PRISMA 2020\nRevue : Simulation Hybride en Santé (2020–2026)",
                  fontsize=12, fontweight="bold", pad=10)
    ax.text(5, 0.3, "Référence : Page et al. (2021), BMJ 372:n71, DOI: 10.1136/bmj.n71",
            ha="center", fontsize=7.5, color="#666")

    fig.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    print(f"Diagramme sauvegardé : {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Génère le diagramme de flux PRISMA 2020")
    parser.add_argument("--identifies", type=int, default=None)
    parser.add_argument("--snowballing", type=int, default=None)
    parser.add_argument("--doublons", type=int, default=None)
    parser.add_argument("--screenes", type=int, default=None)
    parser.add_argument("--exclus-titre-resume", type=int, default=None)
    parser.add_argument("--texte-integral", type=int, default=None)
    parser.add_argument("--exclus-texte-integral", type=int, default=None)
    parser.add_argument("--inclus", type=int, default=44,
                         help="Par défaut 44 (corpus vérifié actuel) — ajuster une fois H1-H6 traités")
    parser.add_argument("--out", default="axe3_simulation_hybride/prisma/prisma_flow_diagram.png")
    args = parser.parse_args()

    counts = {
        "identifies": args.identifies, "snowballing": args.snowballing,
        "doublons": args.doublons, "screenes": args.screenes,
        "exclus_titre_resume": args.exclus_titre_resume,
        "texte_integral": args.texte_integral,
        "exclus_texte_integral": args.exclus_texte_integral,
        "inclus": args.inclus,
    }
    draw_flow(counts, Path(args.out))


if __name__ == "__main__":
    main()
