# ℹ️ Arrera Neuron Network — Tkinter Frontend (`ann-tkinter`)

![Baniere Arrera Neuron Network](asset/baniere.png)

Package officiel d'interface graphique (Tkinter / CustomTkinter via `arrera_tk`) pour les assistants personnels propulsés par **Arrera Neuron Network (`ann-core`) Version 4.0** en **Python 3.14**.

`ann-tkinter` implémente le contrat d'interface abstraite `IGestGui` fourni par `ann-core` et offre un ensemble complet de fenêtres modernes, responsives et prêtes à l'emploi.

---

## 🌟 Fonctionnalités Graphiques

L'interface graphique `ann-tkinter` regroupe la fenêtre principale de l'assistant ainsi que l'ensemble des interfaces secondaires spécialisées :

### 💬 Fenêtre Principale (`GUIOpale`)
* **Chat interactif & vocal** : Zone de discussion en langage naturel avec l'IA locale (GGUF), boutons d'écoute vocale (`arrera_voice`), historique et notifications.
* **Paramètres utilisateur** : Interface de gestion des préférences utilisateur (`user.json`), choix du modèle d'IA, recommandation matérielle et configuration logicielle.
* **Intégration Réseau & Socket** : Indicateurs d'état et commandes d'interface (modes 1 à 6).

### 🖥️ Vues Secondaires Dédiées (`ann_tkinter/gui`)
* 📅 **Agenda** (`GUIAgenda`) : Consultation, ajout et suppression d'événements du calendrier.
* ☕ **Briefing Quotidien** (`GuiBrief`) : Résumés matin (*Morning*), après-midi (*Afternoon*) et soir (*Evening*) combinant météo, tâches et actualités avec disposition 50/50 et retour à la ligne dynamique automatique.
* 📰 **Actualités** (`GuiNews`) : Affichage des flux RSS catégorisés (Généraliste, Science, Tech, etc.) et ouverture directe des articles dans le navigateur.
* 💼 **Arrera Work** (`GUIArreraWork`) : Gestion de projets professionnels/personnels, édition de documents Word (`.docx`, `.odt`), tableurs Excel (`.xlsx`) et mode Agent de code généré par IA.
* 📥 **Arrera Download** (`GUIArreraDownload`) : Téléchargement de vidéos et musiques YouTube/Web via `yt-dlp`.
* 🧮 **Calculatrice** (`GUICalculatrice`) : Interface multifonction avec modes Standard, Complexe et théorème de Pythagore.
* ⏰ **Horloge & Chronomètre** (`GUIHorloge`) : Horloge mondiale, chronomètre et minuteur avec signal sonore.
* 📖 **Lecture Vocale** (`GUILecture`) : Interface dédiée pour dicter et faire lire vocalement un texte long.
* ✉️ **Assistant Emails** (`GUIMail`) : Rédaction, correction stylistique et génération de réponses d'e-mails assistées par l'IA.
* 📝 **Gestion des Tâches** (`GUITache`) : To-do list complète (tâches du jour, tâches globales et tâches associées aux projets).
* 🌐 **Traducteur** (`GUITraducteur`) : Traduction instantanée de textes multi-langues.
* ✍️ **Correcteur Orthographique** (`GUIorthographe`) : Analyse et correction orthographique/grammaticale en direct par le LLM.
* 🛠️ **CodeHelp & Git** (`GUIHelp`) : Recherche rapide de documentation développeur (Python, DevDocs, Microsoft Learn, GitHub), sélecteur de couleurs, organisateur de variables et intégration des commandes Git (`status`, `commit`, `push`, `branch`, `log`).

---

## 🎨 Personnalisation et Assets (`confTkinter`)

`ann-tkinter` permet de personnaliser entièrement l'apparence et les ressources de l'assistant grâce à la classe [`confTkinter`](ann_tkinter/confTkinter.py) :

```python
from ann_tkinter import confTkinter

# Personnalisation des ressources pour un assistant spécifique
conf_gui = confTkinter(
    asset="/chemin/vers/mon_assistant/asset/",
    icon="/chemin/vers/mon_assistant/asset/icon.png"
)
```

Chaque assistant peut disposer de son propre thème, de ses propres icônes météo (`asset/meteo/`) et de sa propre identité visuelle sans modifier le code source du package.

---

## 📦 Installation & Prérequis

### Prérequis Système
* **Python 3.14** exclusivement.
* Bibliothèques système audio et vidéo requises par `ann-core` (PortAudio, libsndfile, VLC, FFmpeg). Consultez les [Dépendances de ann-core](../ArreraNeuronNetwork/markdown/dependency.md).

### Installation du package

Dans votre environnement virtuel Python 3.14 :

```bash
# Installation en mode éditable depuis les sources
pip install -e .

# Ou installation conjointe avec ann-core en local :
pip install -e ../ArreraNeuronNetwork
pip install -e .
```

---

## 🚀 Démarrage Rapide

### 1. Lancer l'assistant avec son interface graphique

```bash
python main.py
```

### 2. Tester individuellement les fenêtres graphiques

Le fichier `test-gui.py` permet d'exécuter et de tester n'importe quelle vue graphique de façon isolée :

```bash
python test-gui.py
```

---

## 📖 Intégration dans un Nouvel Assistant

Pour apprendre à connecter `ann-tkinter` à votre propre assistant ou pour créer une nouvelle fenêtre graphique :
👉 **[Consulter le Guide d'Intégration Tkinter (`INTEGRATION.md`)](./INTEGRATION.md)**

---

## 🔗 Liens Utiles

* **Moteur Headless Core** : [ArreraNeuronNetwork (`ann-core`)](../ArreraNeuronNetwork/readme.md)
* **Architecture Globale** : [Architecture ANN 4.0](../ArreraNeuronNetwork/markdown/ARCHITECTURE.md)
* **Guide Développeur** : [AGENTS.md](./AGENTS.md)
