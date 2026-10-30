from arrera_tk import aFrame,aTk,aButton
from gestionnaire.gestion import gestionnaire
from ann_tkinter import TkinterGuiManager,confTkinter
from config.confNeuron import confNeuron

# Configuration de l'assistant
conf = confNeuron(name="Opale",
                  lang="fr",
                  bute="developper un algo de ChatBot qui sera inclut dans SIX et Ryley",
                  createur="Pauchet Baptiste",
                  listFonction=["ouvrir une application", "aider sur les recherches de internet", "donner la meteo",
                          "faire un résumer des actualités"],
                  moteurderecherche="google",
                  etatService=1,
                  etatTime=1,
                  etatOpen=1,
                  etatSearch=1,
                  etatChatbot=1,
                  etatApi=1,
                  etatCodehelp=1,
                  etatWork=1,
                  etatSocket=0,
                  lienDoc="www.google.com",
                  fichierLangue="language/vouvoiment/",
                  fichierKeyword="keyword/",
                  voiceAssistant=True)

conf_gui = confTkinter(asset="asset/",icon="asset/icon.png")

# Initialisation du gestionnaire principal
gest = gestionnaire(conf)
# Enregistrement du gestionnaire graphique Tkinter
gest.set_gui_manager(TkinterGuiManager(gest,conf_gui))
# Récupération du gestionnaire de GUI
gest_gui = gest.getGestGUI()

fnc_codehelp = gest.getGestFNC().getFNCCodeHelp()

# Créer la fenêtre principale
window = aTk()
window.title("Test des interfaces graphiques")
window.geometry("800x600")

# Créer un cadre pour les boutons
button_frame = aFrame(window)
button_frame.pack(pady=20, padx=20, fill="both", expand=True)

language = gest.getLanguageObjet()

# Dictionnaire des interfaces à tester et de leurs fonctions de lancement
gui_to_test = {
    "Agenda": gest_gui.activeAgenda,
    "Tâches": gest_gui.activeTache,
    "Aide": lambda: gest_gui.activeHelp("Texte d'aide de test"),
    "Calculatrice": lambda: gest_gui.setGUIActive("calculatrice_normal") and gest_gui.launch_gui(),
    "Calculatrice Pythagore": lambda: gest_gui.setGUIActive("calculatrice_pythagore") and gest_gui.launch_gui(),
    "Calculatrice Complex": lambda: gest_gui.setGUIActive("calculatrice_complex") and gest_gui.launch_gui(),
    "Orthographe": lambda: gest_gui.setGUIActive("orthographe", "Ceci est un texte de test.") and gest_gui.launch_gui(),
    "Arrera Download": lambda: gest_gui.setGUIActive("arrera_download") and gest_gui.launch_gui(),
    "Horloge": lambda: gest_gui.setGUIActive("horloge") and gest_gui.launch_gui(),
    "Lecture": lambda: gest_gui.setGUIActive("lecture") and gest_gui.launch_gui(),
    "Mail": gest_gui.activeMail,
    "Arrera Work": lambda: gest_gui.setGUIActive("work") and gest_gui.launch_gui(),
    "Traducteur": lambda: gest_gui.setGUIActive("traducteur") and gest_gui.launch_gui(),
    "Color Select" : lambda : (fnc_codehelp.setGUICodeHelp("GUIColorSelector"),fnc_codehelp.launchGui()),
    "Github" : lambda : (fnc_codehelp.setGUICodeHelp("GUIGithubGestion"),fnc_codehelp.launchGui()),
    "Librairy" : lambda : (fnc_codehelp.setGUICodeHelp("GUILibrairy"),fnc_codehelp.launchGui()),
    "Git Gestion" : lambda : (fnc_codehelp.setGUICodeHelp("GUIGitGestion"),fnc_codehelp.launchGui()),
    "Morning Brief": gest_gui.active_morning_brief,
    "Afternoon Brief": gest_gui.active_afternoon_brief,
    "Evening Brief": gest_gui.active_evening_brief,
    "actu_all":gest_gui.active_actu_all,
    "actu_main":gest_gui.active_actu_main,
    "actu_tech":gest_gui.active_actu_tech,
    "actu_culture":gest_gui.active_actu_culture,
    "actu_sport":gest_gui.active_actu_sport,
    "actu_science":gest_gui.active_actu_science,
}


# Créer un bouton pour chaque interface
# Organiser les boutons sur une grille pour une meilleure lisibilité
cols = 3
rows = (len(gui_to_test) + cols - 1) // cols
i = 0
for name, action in gui_to_test.items():
    row = i // cols
    col = i % cols
    btn = aButton(button_frame, text=name, command=action, height=4, width=15)
    btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    i += 1

# Configurer la grille pour qu'elle s'étende avec la fenêtre
for i in range(rows):
    button_frame.grid_rowconfigure(i, weight=1)
for i in range(cols):
    button_frame.grid_columnconfigure(i, weight=1)


# Lancer la boucle principale de l'interface graphique
window.mainloop()
