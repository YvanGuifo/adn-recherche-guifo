"""
Utilitaires partagés par les scripts de veille, vérification et reporting.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Charge un fichier YAML depuis un chemin relatif à la racine du dépôt ou absolu."""
    p = Path(path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {p}")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_settings() -> dict[str, Any]:
    return load_yaml("config/settings.yaml")


def data_dir() -> Path:
    settings = load_settings()
    d = REPO_ROOT / settings.get("chemins", {}).get("data_dir", "data/veille_results")
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_json(name: str, payload: dict[str, Any]) -> Path:
    """Sauvegarde un résultat de veille horodaté dans data/veille_results/."""
    out_dir = data_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=_json_default)
    return path


def load_json_if_exists(name: str) -> dict[str, Any] | None:
    path = data_dir() / f"{name}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _json_default(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    raise TypeError(f"Type non sérialisable : {type(o)}")


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def write_github_output(key: str, value: str) -> None:
    """Écrit une paire clé=valeur dans $GITHUB_OUTPUT si présent (no-op en local)."""
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if not gh_output:
        return
    # Valeurs multi-lignes : utiliser un délimiteur, cf. doc GitHub Actions.
    with open(gh_output, "a", encoding="utf-8") as f:
        if "\n" in value:
            delim = "EOF_ADN"
            f.write(f"{key}<<{delim}\n{value}\n{delim}\n")
        else:
            f.write(f"{key}={value}\n")
