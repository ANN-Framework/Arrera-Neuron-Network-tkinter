from pathlib import Path

# Racine du dossier package ann_tkinter
PACKAGE_ROOT = Path(__file__).resolve().parent

def get_asset_dir() -> str:
    """Retourne le chemin absolu du dossier asset/ avec un slash final."""
    return str(PACKAGE_ROOT / "asset") + "/"

def get_asset_file(relative_file: str) -> str:
    """Retourne le chemin absolu d'un fichier asset spécifique."""
    return str(PACKAGE_ROOT / "asset" / relative_file)