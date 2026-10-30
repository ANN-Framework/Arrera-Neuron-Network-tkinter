# AGENTS.md — Arrera Neuron Network Tkinter Frontend (`ann-tkinter`)

Ce dépôt contient **`ann-tkinter`**, l'interface graphique Tkinter / CustomTkinter (`arrera_tk`) de l'assistant Opale, propulsée par le moteur Headless **`ann-core`** (`ArreraNeuronNetwork`).

---

## 1. Architecture et séparation des responsabilités

- **Rôle de `ann-tkinter`** : Gérer uniquement l'affichage graphique, les fenêtres secondaires (`ann_tkinter/gui`), les boîtes de dialogue (`tkinter.filedialog`, `tkinter.messagebox`) et les ressources visuelles (`ann_tkinter/asset`).
- **Rôle de `ann-core` (dépendance externe)** : Fournir toute la logique métier (`fnc/`), les gestionnaires (`gestionnaire/`), la voix (`librairy/arrera_voice.py`) et le cerveau neuronal (`brain/`, `neuron/`).
- **Règle d'or** : Ne jamais dupliquer la logique métier du Core dans `ann-tkinter`. Les vues de `ann_tkinter/gui` appellent les méthodes exposées par `self._gestionnaire.getGestFNC()` ou `self._gestionnaire.getUserConf()`.

---

## 2. Connexion entre `ann-tkinter` et `ann-core`

La liaison avec le moteur `ann-core` repose sur l'injection de dépendances :

1. **[`ann_tkinter/gui`](ann_tkinter/gui/TkinterGuiManager.py)** :
   - Implémente l'interface abstraite `IGestGui` provenant de `ann-core` (`gestionnaire.IGestGui`).
   - Retourne `has_gui() -> True`.
   - Instancie et pilote toutes les vues Tkinter (`GUIAgenda`, `GUIArreraDownload`, `GUIArreraWork`, `GUICalculatrice`, `GUIHelp`, `GUIHorloge`, `GUILecture`, `GUIMail`, `GUITache`, `GUITraducteur`, `GUIorthographe`, `GuiBrief`, `GuiNews`, et les vues `ann_tkinter/gui`).
   - Appelle `self.__gestionnaire.getGestIA().generate_final_response(...)` lorsqu'une ouverture/fermeture de fenêtre nécessite une réponse formulée par l'IA.
2. **[`src/GUIOpale.py`](src/GUIOpale.py)** :
   - Initialise `ABrain(config=self.__config)` depuis `ann-core`.
   - Injecte le gestionnaire graphique dès le démarrage :
     ```python
     gest = self.__assistantBrain.getGestionnaire()
     gest.set_gui_manager(TkinterGuiManager(gest))
     ```
   - Cet appel active automatiquement les outils `INTERFACE` et `CODEHELP` dans le prompt système de `ann-core`.

---

## 3. Structure des dossiers

- **`main.py`** : Point d'entrée de l'application graphique (`GUIOpale`).
- **`src/GUIOpale.py`** : Fenêtre principale de l'assistant Opale (chat, mode vocal, paramètres utilisateur, intégration socket).
- **`ann_tkinter/gui`** :
  - `guibase.py` : Classe de base pour toutes les fenêtres secondaires Tkinter (`Toplevel` / `arrera_tk`).
  - `TkinterGuiManager.py` : Pont entre `ann-core` et les fenêtres de `ann_tkinter/gui`.
  - `GUI*.py` & `ann_tkinter/gui` : Vues spécialisées pour chaque outil de l'assistant.
  - *Note sur les dialogues de fichiers* : C'est la couche `ann_tkinter/gui` (ex. `ann_tkinter/gui`, `src/GUIOpale.py`) qui ouvre `filedialog.askopenfilename` / `askdirectory` et transmet le chemin sélectionné aux méthodes de `ann-core` (`openWordDirectly`, `openTableurDirectly`, `setWorkFolder`, `setDownloadFolderDur`, etc.).
- **`asset/`** : Contient toutes les icônes (`.png`), sons (`.mp3`) et fichiers de thèmes nécessaires à l'interface, configurable par assistant via `confTkinter(asset=..., icon=...)`.
- **`test-gui.py`** : Harnais de test permettant de lancer et vérifier individuellement chaque fenêtre de `ann_tkinter/gui` via `TkinterGuiManager`.

---

## 4. Installation et commandes utiles

- **Installer `ann-core` en mode éditable dans l'environnement virtuel de `ann-tkinter`** :
  ```bash
  .venv/bin/pip install -e ../ArreraNeuronNetwork
  ```
- **Lancer l'application complète** :
  ```bash
  .venv/bin/python main.py
  ```
- **Lancer l'outil de test des interfaces graphiques** :
  ```bash
  .venv/bin/python test-gui.py
  ```
