import os
from dataclasses import dataclass

@dataclass
class confTkinter:
    """
    Configuration de l'interface Tkinter pour un assistant Arrera.
    Permet à chaque assistant d'avoir ses propres visuels, icônes et thèmes.
    """
    asset: str = "asset/"  # Emplacement du dossier d'assets de l'assistant
    icon: str = ""         # Icône de l'assistant (par défaut: icon.png dans asset)
    theme: str = ""        # Fichier JSON de thème (par défaut: theme/theme_default.json dans asset)

    def __post_init__(self):
        # 1. Résolution du chemin absolu du dossier d'assets
        if not os.path.isabs(self.asset):
            self.asset = os.path.abspath(self.asset)

        if not self.asset.endswith(os.sep) and not self.asset.endswith("/"):
            self.asset += "/"

        if not os.path.exists(self.asset):
            raise FileNotFoundError(
                f"[confTkinter] Dossier d'assets introuvable : '{self.asset}'. "
                f"Veuillez spécifier l'emplacement du dossier d'assets de votre assistant."
            )

        # 2. Résolution de l'icône de l'assistant
        if not self.icon:
            default_icon = os.path.join(self.asset, "icon.png")
            self.icon = default_icon if os.path.exists(default_icon) else ""
        elif not os.path.isabs(self.icon):
            self.icon = os.path.abspath(self.icon)

        # 3. Résolution du thème
        if not self.theme:
            default_theme = os.path.join(self.asset, "theme", "theme_default.json")
            self.theme = default_theme if os.path.exists(default_theme) else ""
        elif not os.path.isabs(self.theme):
            self.theme = os.path.abspath(self.theme)