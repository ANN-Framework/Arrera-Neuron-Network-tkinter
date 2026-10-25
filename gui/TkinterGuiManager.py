from typing import Callable
from gestionnaire.IGestGui import IGestGui


class TkinterGuiManager(IGestGui):
    """
    Gestionnaire GUI Tkinter concret pour Arrera.
    Gère le chargement et le déclenchement des interfaces graphiques Tkinter.
    """
    def __init__(self, gest):
        self.__name_gui = None
        self.__gest = gest
        self.__parms = None
        self.__textOut = None
        self.__prompt = ""
        self.__valOut = 0

        self.__gestIA = gest.getGestIA()

        conf = gest.getConfigFile()

        from gui.GUIHelp import GUIHelp
        self.__guiHelp = GUIHelp(self.__gest)

        self.__guiAgenda = None
        self.__guiHorloge = None
        self.__guiTache = None
        self.__guiTraducteur = None
        self.__guiBrief = None
        self.__guiWork = None
        self.__guiCalculatrice = None
        self.__guiOrthographe = None
        self.__guiLecture = None
        self.__guiArreraDownload = None
        self.__guiNews = None
        self.__guiMail = None

        self.__gui_actions: dict[str, Callable[[], bool]] = {"aide": self.__action_aide}

        if conf.etatTime == 1:
            from gui.GUIAgenda import GUIAgenda  # TIME
            from gui.GUIHorloge import GUIHorloge  # TIME
            from gui.GUITache import GUITache  # TIME

            self.__guiAgenda = GUIAgenda(self.__gest)
            self.__guiHorloge = GUIHorloge(self.__gest)
            self.__guiTache = GUITache(self.__gest)

            self.__gui_actions.update({
                "agenda": lambda: self.__generic_action(
                    self.__guiAgenda.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'agenda est maintenant ouvert.")
                ),
                "horloge": lambda: self.__generic_action(
                    self.__guiHorloge.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'horloge est maintenant ouverte.")
                ),
                "minuteur": lambda: self.__generic_action(
                    self.__guiHorloge.activeMinuteur,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface du minuteur est ouverte.")
                ),
                "chrono": lambda: self.__generic_action(
                    self.__guiHorloge.activeChrono,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface du chronomètre est ouverte.")
                ),
                "tache": lambda: self.__generic_action(
                    self.__guiTache.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que son gestionnaire de tâches est ouvert.")
                ),
            })

            self.__prompt += """
                - "gui": Args ["nom_gui", ""]. nom_gui: agenda, horloge, minuteur, chrono, tache.
                """

        if conf.etatApi == 1:
            from gui.GUITraducteur import GuiTraducteur  # API
            from gui.GuiBrief import guiBrief  # API
            from gui.GuiNews import GuiNews

            self.__guiTraducteur = GuiTraducteur(self.__gest)
            self.__guiBrief = guiBrief(self.__gest, self.__gest.getName())
            self.__guiNews = GuiNews(self.__gest)

            self.__gui_actions.update({
                "traducteur": lambda: self.__generic_action(
                    self.__guiTraducteur.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que le traducteur est ouvert.")
                ),
                "actu_all": lambda: self.__generic_action(
                    self.__guiNews.active_all,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités (toutes les catégories) est ouverte.")
                ),
                "actu_main": lambda: self.__generic_action(
                    self.__guiNews.active_main,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités généralistes est ouverte.")
                ),
                "actu_tech": lambda: self.__generic_action(
                    self.__guiNews.active_tech,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités sur les nouvelles technologies est ouverte.")
                ),
                "actu_culture": lambda: self.__generic_action(
                    self.__guiNews.active_culture,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités culturelles est ouverte.")
                ),
                "actu_sport": lambda: self.__generic_action(
                    self.__guiNews.active_sport,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités sportives est ouverte.")
                ),
                "actu_science": lambda: self.__generic_action(
                    self.__guiNews.active_science,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface des actualités scientifiques est ouverte.")
                ),
                "morning_brief": lambda: self.__generic_action(
                    self.__guiBrief.view_morning,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que son brief du matin est prêt et affiché.")
                ),
                "afternoon_brief": lambda: self.__generic_action(
                    self.__guiBrief.view_afternoon,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que son brief de l'après-midi est prêt et affiché.")
                ),
                "evening_brief": lambda: self.__generic_action(
                    self.__guiBrief.view_evening,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que son brief de la soirée est prêt et affiché.")
                ),
            })

            self.__prompt += """
                - "gui": Args ["nom_gui", ""]. nom_gui: traducteur, actu_all, actu_main, actu_tech, actu_culture, actu_sport, actu_science, morning_brief, afternoon_brief, evening_brief.
                """

        if conf.etatWork == 1:
            from gui.GUIArreraWork import GUIWork  # WORK

            self.__guiWork = GUIWork(self.__gest)

            self.__gui_actions.update({
                "work": lambda: self.__generic_try_action(
                    self.__guiWork.activeAcceuil,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface d'Arrera Work est ouverte."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir l'interface d'Arrera Work.")
                ),
                "tache_projet": lambda: self.__generic_bool_action(
                    self.__guiWork.open_task_projet,
                    lambda: self.__gestIA.generate_final_response("", f"Annonce à l'utilisateur que les tâches de son projet {self.__gest.getGestFNC().getFNCWork().getNameProjet()} sont ouvertes."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir les tâches de son projet.")
                ),
            })

            self.__prompt += """
                - "gui": Args ["nom_gui", ""]. nom_gui: work, tache_projet.
                """

        if conf.etatService == 1:
            from gui.GUICalculatrice import GUICalculatrice  # SERVICE
            from gui.GUIorthographe import GUIOrthographe  # SERVICE
            from gui.GUILecture import GUILecture  # SERVICE
            from gui.GUIMail import GUIMail  # SERVICE

            self.__guiCalculatrice = GUICalculatrice(self.__gest)
            self.__guiOrthographe = GUIOrthographe(self.__gest)
            self.__guiLecture = GUILecture(self.__gest)
            self.__guiMail = GUIMail(self.__gest)

            self.__gui_actions.update({
                "calculatrice_normal": lambda: self.__generic_try_action(
                    self.__guiCalculatrice.activeCalcule,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que la calculatrice est ouverte."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir la calculatrice.")
                ),
                "calculatrice_pythagore": lambda: self.__generic_try_action(
                    self.__guiCalculatrice.activePythagore,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que la calculatrice en mode pythagore est ouverte."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir la calculatrice en mode pythagore.")
                ),
                "calculatrice_complex": lambda: self.__generic_try_action(
                    self.__guiCalculatrice.activeComplex,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que la calculatrice en mode complexe est ouverte."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir la calculatrice en mode complexe.")
                ),
                "orthographe": self.__action_orthographe,
                "lecture": lambda: self.__generic_action(
                    self.__guiLecture.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface de lecture est ouverte.")
                ),
                "mail": lambda: self.__generic_action(
                    self.__guiMail.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'interface de mail est ouverte.")
                ),
            })

            self.__prompt += """
                - "gui": Args ["nom_gui", "texte"]. nom_gui: calculatrice_normal, calculatrice_pythagore, calculatrice_complex, orthographe(texte="texte"), lecture, mail.
                """

        if conf.etatOpen == 1:
            from gui.GUIArreraDownload import GUIArreraDownload  # OPEN

            self.__guiArreraDownload = GUIArreraDownload(self.__gest)

            self.__gui_actions.update({
                "arrera_download": lambda: self.__generic_try_action(
                    self.__guiArreraDownload.active,
                    lambda: self.__gestIA.generate_final_response("", "Annonce à l'utilisateur que l'application Arrera Download est ouverte."),
                    lambda: self.__gestIA.generate_final_response("", "Informe l'utilisateur qu'il est impossible d'ouvrir l'application Arrera Download.")
                )
            })

            self.__prompt += """
                - "gui": Args ["nom_gui", ""]. nom_gui: arrera_download.
                """

        if conf.etatCodehelp == 1:
            from gui.codehelp.CHGithub import CHGithub
            from gui.codehelp.CHLibrairy import CHLibrairy
            from gui.codehelp.CHGitGestion import CHGitGestion
            from gui.codehelp.CCHcolorSelector import CCHcolorSelector

            self.__guiColorSelector = CCHcolorSelector(self.__gest)
            self.__guiGithub = CHGithub(self.__gest)
            self.__guiLibrairy = CHLibrairy(self.__gest)
            self.__guiGitGestion = CHGitGestion(self.__gest)

            self.__gui_actions.update({
                "GUIColorSelector": lambda: self.__generic_action(
                    self.__guiColorSelector.active,
                    lambda: self.__gestIA.generate_final_response("",
                                                                  "Annonce à l'utilisateur que le sélecteur de couleurs est ouvert.")
                ),
                "GUIGithubGestion": lambda: self.__generic_action(
                    self.__guiGithub.active,
                    lambda: self.__gestIA.generate_final_response("",
                                                                  "Annonce à l'utilisateur que le gestionnaire GitHub est ouvert.")
                ),
                "GUILibrairy": lambda: self.__generic_action(
                    self.__guiLibrairy.active,
                    lambda: self.__gestIA.generate_final_response("",
                                                                  "Annonce à l'utilisateur que la librairie CodeHelp est ouverte.")
                ),
                "GUIGitGestion": lambda: self.__generic_action(
                    self.__guiGitGestion.active,
                    lambda: self.__gestIA.generate_final_response("",
                                                                  "Annonce à l'utilisateur que l'interface de gestion Git est ouverte.")
                ),
            })

    def is_gui_available(self) -> bool:
        return True

    def get_prompt(self) -> str:
        return self.__prompt

    def setGUIActive(self, gui: str, parms=None) -> bool:
        if gui in self.__gui_actions:
            self.__name_gui = gui
            self.__parms = parms
            return True
        else:
            return False

    def launch_gui(self) -> bool:
        if self.__name_gui in self.__gui_actions:
            return self.__gui_actions[self.__name_gui]()
        return False

    def __generic_try_action(self, action, success_msg_provider, fail_msg_provider):
        try:
            action()
            self.__textOut = success_msg_provider()
            self.__valOut = 5
            return True
        except Exception:
            self.__textOut = fail_msg_provider()
            self.__valOut = 1
            return False

    def __generic_action(self, action, success_msg_provider):
        self.__textOut = success_msg_provider()
        action()
        self.__valOut = 5
        return True

    def __generic_bool_action(self, action, success_msg_provider, fail_msg_provider):
        if action():
            self.__textOut = success_msg_provider()
            self.__valOut = 5
            return True
        else:
            self.__textOut = fail_msg_provider()
            self.__valOut = 1
            return False

    def __action_orthographe(self):
        if self.__parms != "" and self.__gest.getGestFNC().getFNCOrthographe().getToolLaunched():
            self.__guiOrthographe.active()
            self.__guiOrthographe.setTexte(self.__parms)
            self.__textOut = self.__gestIA.generate_final_response("",
                                                                   "Annonce à l'utilisateur que le correcteur orthographique est ouvert avec son texte.")
            self.__valOut = 5
            return True
        else:
            self.__textOut = self.__gestIA.generate_final_response("",
                                                                   "Informe l'utilisateur qu'il est impossible d'ouvrir le correcteur orthographique.")
            self.__valOut = 1
            return False

    def __action_aide(self):
        self.__guiHelp.activeHelp(self.__parms[0])
        self.__textOut = self.__parms[1]
        self.__valOut = 5
        return True

    def textOut(self) -> str:
        return self.__textOut

    def activeAgenda(self) -> bool:
        if self.__guiAgenda is not None:
            self.__guiAgenda.active()
            return True
        return False

    def activeTache(self) -> bool:
        if self.__guiTache is not None:
            self.__guiTache.active()
            return True
        return False

    def activeHelp(self, texte: str) -> bool:
        if self.__guiHelp is not None:
            self.__guiHelp.activeHelp(texte)
            return True
        return False

    def active_morning_brief(self) -> bool:
        if self.__guiBrief is not None:
            self.__guiBrief.view_morning()
            return True
        return False

    def active_afternoon_brief(self) -> bool:
        if self.__guiBrief is not None:
            self.__guiBrief.view_afternoon()
            return True
        return False

    def active_evening_brief(self) -> bool:
        if self.__guiBrief is not None:
            self.__guiBrief.view_evening()
            return True
        return False

    def active_actu_all(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_all()
            return True
        return False

    def active_actu_main(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_main()
            return True
        return False

    def active_actu_tech(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_tech()
            return True
        return False

    def active_actu_culture(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_culture()
            return True
        return False

    def active_actu_sport(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_sport()
            return True
        return False

    def active_actu_science(self) -> bool:
        if self.__guiNews is not None:
            self.__guiNews.active_science()
            return True
        return False

    def activeMail(self) -> bool:
        if self.__guiMail is not None:
            self.__guiMail.active()
            return True
        return False
