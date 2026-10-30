# 🛠️ Guide Développeur — Intégrer Arrera Neuron Network avec Interface Tkinter (`ann-core` + `ann-tkinter`)

Ce guide complet vous accompagne pour concevoir une application de bureau Python dotée à la fois du **cerveau intelligent local (`ann-core`)** et de l'**ensemble des interfaces graphiques Tkinter / CustomTkinter (`ann-tkinter`)**.

En suivant ce guide, vous apprendrez à :
1. Installer et configurer simultanément le moteur IA et la couche graphique.
2. Lancer un assistant desktop interactif (texte, voix, fenêtres spécialisées).
3. Personnaliser l'identité visuelle de votre assistant (icônes, thèmes, sons, dossier d'assets).
4. Piloter les fenêtres graphiques automatiquement via l'IA ou programmatiquement dans votre code.
5. Intégrer les outils de l'ANN dans une application Tkinter / CustomTkinter existante.
6. Exploiter la voix hors-ligne, la mémoire persistante et les modules métier du Core.

---

## 📋 Table des Matières

1. [Prérequis & Installation](#1-prérequis--installation)
2. [Architecture : Comment Core et Tkinter s'articulent](#2-architecture--comment-core-et-tkinter-sarticulent)
3. [Démarrage Rapide : Assistant Desktop Complet en 25 lignes](#3-démarrage-rapide--assistant-desktop-complet-en-25-lignes)
4. [Double Configuration : `confNeuron` & `confTkinter`](#4-double-configuration--confneuron--conftkinter)
5. [Interaction avec l'Assistant : Chat & Déclenchement Automatique des Vues](#5-interaction-avec-lassistant--chat--déclenchement-automatique-des-vues)
6. [Contrôle Programmatique des Outils Graphiques](#6-contrôle-programmatique-des-outils-graphiques)
7. [Intégration dans une Application Tkinter Existante](#7-intégration-dans-une-application-tkinter-existante)
8. [Accès aux Fonctions Métier du Core (Météo, Tâches, Agenda...)](#8-accès-aux-fonctions-métier-du-core-météo-tâches-agenda)
9. [Activer la Voix Hors-Ligne (TTS / STT)](#9-activer-la-voix-hors-ligne-tts--stt)
10. [Mémoire Persistante & Contexte de Session](#10-mémoire-persistante--contexte-de-session)
11. [Créer une Nouvelle Fenêtre Graphique (`GuiBase`)](#11-créer-une-nouvelle-fenêtre-graphique-guibase)
12. [Bonnes Pratiques : Multithreading & Réactivité de l'Interface](#12-bonnes-pratiques--multithreading--réactivité-de-linterface)

---

## 1. Prérequis & Installation

### Prérequis Système
* **Python 3.14** exclusivement.
* Bibliothèques système pour l'audio et les médias :
  * **Linux (Debian/Ubuntu)** : `sudo apt install python3.14-dev portaudio19-dev libsndfile1 vlc ffmpeg`
  * **macOS** : `brew install portaudio libsndfile vlc ffmpeg`
  * **Windows** : VLC 64-bit et FFmpeg ajoutés au `PATH`.

### Installation des Packages
Installez `ann-tkinter` (qui référence automatiquement `ann-core` et `arrera_tk`) :

```bash
# Depuis GitHub
pip install git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Core.git@version4.0
pip install git+https://github.com/ANN-Framework/Arrera-Neuron-Network-Tkinter.git

# Ou en local (mode éditable) dans votre virtualenv :
pip install -e /chemin/vers/ArreraNeuronNetwork
pip install -e /chemin/vers/ann-tkinter
```

---

## 2. Architecture : Comment Core et Tkinter s'articulent

L'architecture repose sur une séparation stricte :
* **`ann-core`** s'occupe de la logique, de l'inférence IA locale (GGUF), de la voix (`piper-tts`), de la mémoire et des calculs. Il ne contient **aucun import graphique**.
* **`ann-tkinter`** fournit l'implémentation graphique concrète grâce au gestionnaire `TkinterGuiManager`.
* Le pont est réalisé par l'injection de dépendances : `gest.set_gui_manager(TkinterGuiManager)`. Cet appel indique au cerveau IA que l'assistant possède un écran (`has_gui() -> True`), activant dynamiquement la capacité de l'IA à ouvrir des fenêtres graphiques lors de requêtes en langage naturel.

```
┌────────────────────────────────────────────────────────┐
│                        ann-core                        │
│    (Cerveau ABrain, LLM GGUF, Voix, Modules fnc/)     │
│                           ▲                            │
│                           │ Contrat IGestGui           │
│                           ▼                            │
│                   TkinterGuiManager                    │
│                           ▲                            │
│         ┌─────────────────┴─────────────────┐          │
│         ▼                                   ▼          │
│  Fenêtre Principale               Sous-fenêtres Toplevel│
│  (GUIOpale - Chat/Voix)          (Agenda, Brief, ...)  │
└────────────────────────────────────────────────────────┘
```

---

## 3. Démarrage Rapide : Assistant Desktop Complet en 25 lignes

Voici le script complet pour démarrer un assistant de bureau interactif avec sa fenêtre principale, son chat IA et l'ensemble de ses fenêtres secondaires :

```python
import os
from config.confNeuron import confNeuron
from brain.brain import ABrain
from ann_tkinter import confTkinter
from ann_tkinter.gui.TkinterGuiManager import TkinterGuiManager
from ann_tkinter.gui.guibase import GuiBase
from src.GUIOpale import GUIOpale

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    asset_dir = os.path.join(base_dir, "asset")

    # 1. Configuration logique (Core)
    conf_core = confNeuron(name="Opale", active_ia=True, active_voice=False)

    # 2. Configuration graphique (Tkinter)
    conf_tk = confTkinter(asset=asset_dir, icon=os.path.join(asset_dir, "icon.png"))
    GuiBase.set_global_conf(conf_tk)

    # 3. Démarrage du cerveau et injection du gestionnaire graphique
    brain = ABrain(config=conf_core)
    gest = brain.getGestionnaire()

    gui_manager = TkinterGuiManager(gest, conf_tk=conf_tk)
    gest.set_gui_manager(gui_manager)

    # 4. Lancement de la fenêtre principale
    app = GUIOpale(brain, conf_tk=conf_tk)
    app.active()
    app.start()

if __name__ == "__main__":
    main()
```

---

## 4. Double Configuration : `confNeuron` & `confTkinter`

Une application intégrant l'ANN utilise deux objets de configuration complémentaires :

### Configuration Logique (`confNeuron`)
```python
from config.confNeuron import confNeuron

conf_core = confNeuron(
    name="MonAssistant",        # Nom utilisé par l'IA dans ses réponses
    active_ia=True,             # Active le moteur LLM GGUF local
    active_voice=True,          # Active la voix (synthèse + micro)
    ia_os_directory="/models"   # Dossier partagé optionnel pour modèles GGUF
)
```

### Configuration Visuelle (`confTkinter`)
```python
from ann_tkinter import confTkinter

conf_tk = confTkinter(
    asset="/chemin/vers/mon_asset_folder/",
    icon="/chemin/vers/mon_asset_folder/icon.png"
)
```

#### Arborescence recommandée pour vos assets :
```text
mon_projet/
├── asset/
│   ├── icon.png                 # Icône de toutes les fenêtres (obligatoire)
│   ├── logo.png                 # Logo de l'assistant (utilisé dans les paramètres)
│   ├── baniere.png              # Bannière visuelle
│   ├── meteo/                   # Icônes météo (01d.png, meteo-error.png...)
│   ├── sound/                   # Sons d'interface personnalisés
│   └── tache/                   # Visuels pour les tâches
```

---

## 5. Interaction avec l'Assistant : Chat & Déclenchement Automatique des Vues

Lorsque `TkinterGuiManager` est injecté, l'assistant est capable de répondre soit par du texte, soit en **ouvrant directement la bonne fenêtre graphique** selon la demande en langage naturel :

* *"Donne-moi les actualités"* ➔ Ouvre automatiquement la fenêtre **Actualités** (`GuiNews`).
* *"Quel est mon programme du jour ?"* ou *"Ouvre le brief"* ➔ Ouvre la fenêtre **Briefing** (`GuiBrief`) avec la météo, les tâches et les actualités réparties à 50/50.
* *"Ajoute une tâche"* ou *"Montre mes devoirs"* ➔ Ouvre la fenêtre **Tâches** (`GUITache`).
* *"Ouvre l'agenda"* ➔ Ouvre la fenêtre **Calendrier** (`GUIAgenda`).
* *"Lance la calculatrice"* ➔ Ouvre la **Calculatrice** (`GUICalculatrice`).
* *"Combien font 45 fois 12 ?"* ➔ Répond directement en texte dans la zone de chat sans ouvrir de fenêtre inutilement.

Tout cela est géré automatiquement par le routeur IA (`IARouter`) du Core sans que vous n'ayez à écrire de règles manuelles.

---

## 6. Contrôle Programmatique des Outils Graphiques

Vous pouvez également déclencher directement l'ouverture des fenêtres depuis votre propre code via `gui_manager` :

```python
gui = gest.getGestGUI()

# Calendrier
gui.open_agenda()

# Résumés quotidiens
gui.open_brief(mode=1)  # 1: Morning, 2: Afternoon, 3: Evening

# Gestion de projets & bureautique Word/Excel
gui.open_work()

# Outils de temps
gui.open_horloge(mode=1)  # 1: Horloge mondiale, 2: Chronomètre, 3: Minuteur

# Calculatrices
gui.open_calculatrice(mode=1)  # 1: Standard, 2: Complexe, 3: Pythagore

# Autres outils
gui.open_task()          # To-Do list
gui.open_news()          # Flux RSS
gui.open_mail()          # Client email IA
gui.open_traducteur()    # Outil de traduction
gui.open_orthographe()   # Correcteur orthographique
gui.open_codehelp()      # Docs dev et Git
gui.open_download()      # Téléchargement vidéo/audio
```

---

## 7. Intégration dans une Application Tkinter Existante

Si vous possédez déjà une application Tkinter / CustomTkinter, vous pouvez lui greffer le moteur d'ANN et ses fenêtres :

```python
import threading
import customtkinter as ctk
from config.confNeuron import confNeuron
from brain.brain import ABrain
from ann_tkinter import confTkinter
from ann_tkinter.gui.TkinterGuiManager import TkinterGuiManager
from ann_tkinter.gui.guibase import GuiBase

class MonAppExistante(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mon Logiciel d'Entreprise")
        self.geometry("900x600")

        # 1. Initialisation ANN Core + Tkinter
        self.conf_core = confNeuron(name="AssistantPro", active_ia=True, active_voice=False)
        self.brain = ABrain(config=self.conf_core)
        self.brain.start()
        self.gest = self.brain.getGestionnaire()

        self.conf_tk = confTkinter(asset="/chemin/vers/asset", icon="/chemin/vers/icon.png")
        GuiBase.set_global_conf(self.conf_tk)

        self.gui_manager = TkinterGuiManager(self.gest, conf_tk=self.conf_tk)
        self.gest.set_gui_manager(self.gui_manager)

        # 2. Interface de votre logiciel
        self.zone_chat = ctk.CTkTextbox(self, width=600, height=350)
        self.zone_chat.pack(pady=10)

        self.champ_texte = ctk.CTkEntry(self, width=500, placeholder_text="Posez une question à l'assistant...")
        self.champ_texte.pack(pady=5)
        self.champ_texte.bind("<Return>", lambda e: self.envoyer_question())

        # Boutons d'outils ANN intégrés
        cadre_boutons = ctk.CTkFrame(self)
        cadre_boutons.pack(pady=10)

        ctk.CTkButton(cadre_boutons, text="Agenda", command=self.gui_manager.open_agenda).pack(side="left", padx=5)
        ctk.CTkButton(cadre_boutons, text="Briefing", command=lambda: self.gui_manager.open_brief(1)).pack(side="left", padx=5)
        ctk.CTkButton(cadre_boutons, text="Tâches", command=self.gui_manager.open_task).pack(side="left", padx=5)
        ctk.CTkButton(cadre_boutons, text="Calculatrice", command=lambda: self.gui_manager.open_calculatrice(1)).pack(side="left", padx=5)

    def envoyer_question(self):
        question = self.champ_texte.get().strip()
        if not question:
            return
        self.champ_texte.delete(0, "end")
        self.zone_chat.insert("end", f"\nVous : {question}\n")

        # Exécution dans un thread séparé pour ne pas figer Tkinter
        def worker():
            reponse = self.brain.requet(question)
            # Mise à jour graphique sécurisée sur le thread Tkinter
            self.after(0, lambda: self.zone_chat.insert("end", f"Assistant : {reponse}\n"))

        threading.Thread(target=worker, daemon=True).start()

    def destroy(self):
        self.brain.destroy()
        super().destroy()

if __name__ == "__main__":
    app = MonAppExistante()
    app.mainloop()
```

---

## 8. Accès aux Fonctions Métier du Core (Météo, Tâches, Agenda...)

En plus de l'interface graphique et de l'IA, vous pouvez manipuler directement les données brutes :

```python
fnc = gest.getGestFNC()

# Récupérer les prévisions météo structurées (dict)
meteo = fnc.getFNCMeteo().get_meteo_actuelle()

# Ajouter des tâches dans la base locale
fnc.getFNCTache().add_task("Finaliser le rapport mensuel")

# Récupérer les articles d'actualités par catégorie
actu_tech = fnc.getFNCActu().get_actu_tech()

# Traduire du texte
texte_en = fnc.getFNCTraduction().translate("Bonjour", dest="en")
```

---

## 9. Activer la Voix Hors-Ligne (TTS / STT)

Pour activer les fonctionnalités vocales complètes dans votre interface graphique :

1. Réglez `active_voice=True` dans `confNeuron`.
2. Le moteur initialise `piper-tts` pour la synthèse vocale hors-ligne et `speechRecognition` pour l'écoute au microphone.
3. Les signaux sonores (bip d'écoute, son d'alarme) sont générés directement en mémoire sans fichier sonore externe requis.

Dans votre interface graphique, vous pouvez déclencher l'écoute au micro ou faire parler l'assistant :

```python
voice = gest.getVoiceEngine()

# Faire prononcer une phrase
voice.say("Bonjour ! Vos tâches du jour sont prêtes.")

# Déclencher une écoute micro
texte_entendu = voice.listen()
```

---

## 10. Mémoire Persistante & Contexte de Session

L'assistant conserve les informations utilisateur d'une session à l'autre grâce à `gestMemoire` (stocké dans `user.json`) :

```python
# Mémoriser une préférence ou une information
gest.getGestMemoire().memoriser("L'utilisateur préfère les résumés sous forme de liste à puces.")

# Suivre le contexte de conversation en cours
gest.getGestSession().set_context("projet_actif", "Refonte Site Web")
```

---

## 11. Créer une Nouvelle Fenêtre Graphique (`GuiBase`)

Pour créer votre propre vue secondaire intégrée à l'écosystème :

```python
from ann_tkinter.gui.guibase import GuiBase, aFrame, aLabel, aButton
from gestionnaire.gestion import gestionnaire

class GuiMonModule(GuiBase):
    def __init__(self, gest: gestionnaire, name: str):
        super().__init__(gest, f"{gest.getName()} : {name}")

    def _mainframe(self):
        self._screen.grid_rowconfigure(0, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)

        container = aFrame(self._screen)
        container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        titre = aLabel(container, text="Mon Outil Métier Spécifique", police_size=24)
        titre.pack(pady=20)

    def view(self):
        self.active()  # Construit et affiche la fenêtre Toplevel avec l'icône configurée
```

---

## 12. Bonnes Pratiques : Multithreading & Réactivité de l'Interface

1. **Ne jamais bloquer la boucle principale Tkinter** :
   Les requêtes `brain.requet(...)`, le téléchargement vidéo `yt-dlp` ou l'inférence LLM doivent s'exécuter dans un `threading.Thread(target=...)`.
2. **Mettre à jour l'interface via `after()`** :
   Tkinter n'est pas *thread-safe*. Dès qu'un thread secondaire a terminé son calcul, utilisez `self._screen.after(0, update_ui_callback)` pour rafraîchir les widgets sur le thread principal.
3. **Retour à la ligne responsive (`wraplength`)** :
   Dans les listes d'articles ou de tâches défilantes (`aScrollableFrame`), liez l'événement `<Configure>` du canvas parent (`scroll_f._parent_canvas.bind("<Configure>", on_resize)`) pour adapter automatiquement la largeur du texte à la taille de la fenêtre.
4. **Fermeture Propre** :
   Assurez-vous de capturer la fermeture de la fenêtre (`WM_DELETE_WINDOW`) pour appeler `brain.destroy()` et ainsi libérer immédiatement la RAM et couper les démons d'arrière-plan.
