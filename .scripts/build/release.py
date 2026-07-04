# ///////////////////////////////////////////////////////////////
# RELEASE - Publie une GitHub Release (installeur + zip) via gh CLI
# ///////////////////////////////////////////////////////////////

"""Publie une GitHub Release pour flash-excel avec le `gh` CLI local.

Lit la version depuis [project] de pyproject.toml, résout les artefacts
produits par `build.py` (installeur Inno Setup + zip du dist), affiche le
titre tel qu'il sera créé, demande confirmation, puis crée la release
attachée au tag `vX.Y.Z`.

Prérequis :
    - `gh` installé et authentifié (`gh auth login`)
    - artefacts déjà buildés : `uv run build.py`

Usage :
    uv run .scripts/build/release.py            # confirmation interactive
    uv run .scripts/build/release.py --yes       # sans confirmation
    uv run .scripts/build/release.py --title "…"  # titre personnalisé
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = PROJECT_ROOT / "pyproject.toml"

# alpha / beta / rc / dev / a0 / b1 … → pré-release (aligné sur 02-tag-sync.yml)
_PRERELEASE_RE = re.compile(r"(alpha|beta|rc|dev|a\d+|b\d+)")

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////


def _force_utf8_stdout() -> None:
    """Évite les UnicodeEncodeError d'affichage sur console Windows cp1252."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def _read_version() -> str:
    """Retourne [project].version de pyproject.toml."""
    data = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    return data["project"]["version"]


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    """Exécute une commande et capture stdout/stderr (texte)."""
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def _fail(message: str) -> None:
    """Affiche une erreur et quitte en code 1."""
    print(f"❌ {message}", file=sys.stderr)
    sys.exit(1)


def _resolve_assets(version: str) -> tuple[Path, Path, Path]:
    """Valide les artefacts et retourne (installeur, zip source, zip versionné).

    Le zip du dist n'est pas versionné (`flash-excel.zip`) : l'asset final est
    une copie versionnée, effectuée seulement après confirmation.
    """
    installer = PROJECT_ROOT / "dist" / "installer" / f"flash-excel-{version}-setup.exe"
    zip_src = PROJECT_ROOT / "dist" / "flash-excel.zip"

    if not installer.is_file():
        _fail(
            f"Installeur introuvable : {installer}\n   → lance d'abord `uv run build.py`."
        )
    if not zip_src.is_file():
        _fail(f"Zip introuvable : {zip_src}\n   → lance d'abord `uv run build.py`.")

    return installer, zip_src, zip_src.with_name(f"flash-excel-{version}.zip")


# ///////////////////////////////////////////////////////////////
# MAIN
# ///////////////////////////////////////////////////////////////


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publie une GitHub Release flash-excel."
    )
    parser.add_argument(
        "--title", help="Titre de la release (défaut : « Flash-Excel vX.Y.Z »)."
    )
    parser.add_argument(
        "--yes", action="store_true", help="Ne pas demander de confirmation."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    _force_utf8_stdout()

    if shutil.which("gh") is None:
        _fail("`gh` introuvable. Installe GitHub CLI puis `gh auth login`.")
    if _run(["gh", "auth", "status"]).returncode != 0:
        _fail("`gh` non authentifié. Lance `gh auth login`.")

    version = _read_version()
    tag = f"v{version}"
    title = args.title or f"Flash-Excel v{version}"
    is_prerelease = bool(_PRERELEASE_RE.search(version))

    # Ne pas écraser silencieusement une release existante.
    if _run(["gh", "release", "view", tag]).returncode == 0:
        _fail(f"La release {tag} existe déjà. Supprime-la ou change de version.")

    installer, zip_src, zip_versioned = _resolve_assets(version)
    tag_exists = (
        _run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"]).returncode == 0
    )

    # Récapitulatif + titre as-is avant action.
    print("─" * 60)
    print("📦 GitHub Release à publier")
    print(f"   Tag        : {tag}" + ("" if tag_exists else "  (sera créé par gh)"))
    print(f"   Titre      : {title}")
    print(f"   Pré-release: {'oui' if is_prerelease else 'non'}")
    print("   Artefacts  :")
    for name in (installer.name, zip_versioned.name):
        print(f"     - {name}")
    print("─" * 60)

    answer = (
        "y" if args.yes else input("Publier cette release ? [y/N] ").strip().lower()
    )
    if answer not in {"y", "yes", "o", "oui"}:
        print("Annulé.")
        return 1

    # Copie versionnée du zip seulement une fois la publication confirmée.
    shutil.copy2(zip_src, zip_versioned)

    cmd = ["gh", "release", "create", tag, "--title", title, "--generate-notes"]
    if is_prerelease:
        cmd.append("--prerelease")
    cmd += [str(installer), str(zip_versioned)]

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        _fail(f"Échec de `gh release create` (code {result.returncode}).")

    print(f"✅ Release {tag} publiée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
