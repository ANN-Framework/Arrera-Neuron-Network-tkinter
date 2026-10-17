import webbrowser as w
from github import Github, BadCredentialsException
from gui.codehelp.CCHguiBase import CCHguiBase,gestionnaire
from arrera_tk import *
import threading as th

class CHGithub(CCHguiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Github")
        self.__tokenGithub = ""
        self.__list_depo = []
        self.__list_depo_obj = {}  # Stocke les objets repo complets
        self.__th_load = th.Thread()
        self.__github = None

    def _mainframe(self):
        # Recuperation du token
        self.__tokenGithub = self._gestionnaire.getUserConf().getTokenGithub()
        # Grid
        self._screen.grid_rowconfigure(0, weight=0)  # header (pas extensible)
        self._screen.grid_rowconfigure(1, weight=1)  # contenu (prend tout le reste)
        self._screen.grid_columnconfigure(0, weight=1)
        #Frame
        f_hearder = aFrame(self._screen, height=60)
        self.__f_main = aFrame(self._screen)
        self.__f_error = aFrame(self._screen)
        self.__f_load = aFrame(self._screen)

        self.__f_depot = aScrollableFrame(self.__f_main)
        self.__f_info = aFrame(self.__f_main)

        self.__f_main.grid_columnconfigure(0, weight=1)
        self.__f_main.grid_columnconfigure(1, weight=1)
        self.__f_main.grid_rowconfigure(0, weight=1)

        f_hearder.grid_columnconfigure(0, weight=1)
        f_hearder.grid_rowconfigure(0, weight=1)

        self.__f_error.grid_rowconfigure(0, weight=1)
        self.__f_error.grid_columnconfigure(0, weight=1)

        self.__f_load.grid_rowconfigure(0, weight=1)
        self.__f_load.grid_columnconfigure(0, weight=1)

        # Label
        label_title = aLabel(f_hearder, text="CodeHelp : GitHub",font=("Roboto",30,"bold"))
        self.__l_load = aLabel(self.__f_load,text="Chargement des dépôts",font=("Roboto",25,"bold"))

        self.__label_error = aLabel(self.__f_error,font=("Roboto",25,"bold"))

        #Affichage
        f_hearder.grid(row=0, column=0, sticky="nsew")
        f_hearder.grid_propagate(False)

        self.__label_error.grid(row=0, column=0)
        self.__l_load.grid(row=0, column=0)

        label_title.grid(row=0, column=0)

        self.__f_depot.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.__f_info.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        if ((self.__tokenGithub is None or self.__tokenGithub == "") or
                not self.__check_token(self.__tokenGithub) or
                not self._gestionnaire.getNetworkObjet().getEtatInternet()):
            self.__show_error()
        else:
            self.__show_main()

    def __get_data_github(self):
        self.__list_depo = []
        self.__list_depo_obj = {}
        if self.__tokenGithub and self.__check_token(self.__tokenGithub):
            try :
                access = Github(self.__tokenGithub)
                for repo in access.get_user().get_repos():
                    self.__list_depo.append(str(repo.name))
                    self.__list_depo_obj[str(repo.name)] = repo  # Stocke l'objet repo
                return True
            except Exception as e:
                return False
        else :
            return False

    def __check_token(self,token:str):
        try:
            self.__github = Github(token)
            self.__user = self.__github.get_user()
            return True
        except BadCredentialsException:
            return False
        except Exception as e:
            print("Erreur:", e)
            return False


    def __show_main(self):
        self.__th_load = th.Thread(target=self.__set_view_depots)
        self.__th_load.start()

    def __set_view_depots(self):
        self.__f_load.grid(row=1, column=0, sticky="nsew")
        self._screen.after(100,self.__update_during_load_depots)
        if self.__get_data_github():
            for i, repo in enumerate(self.__list_depo):
                btn = aButton(
                    self.__f_depot,
                    text=repo,
                    command=lambda r=repo: self.__on_click_repo(r)
                )
                btn.grid(row=i, column=0, sticky="ew", padx=5, pady=5)

            self.__f_load.grid_forget()
            self.__f_main.grid(row=1, column=0, sticky="nsew")
            self.__f_depot.grid_columnconfigure(0, weight=1)
        else :
            self.__f_load.grid_forget()
            self.__label_error.configure(text="Erreur lors de la récupération des dépôts")
            self.__f_error.grid(row=1, column=0, sticky="nsew")

    def __update_during_load_depots(self):
        if self.__th_load.is_alive():
            self._screen.update()
            self._screen.after(100, self.__update_during_load_depots)

    def __show_error(self):
        if not self._gestionnaire.getNetworkObjet().getEtatInternet():
            self.__label_error.configure(text="L'application a besoin d'une\nconnexion Internet pour fonctionner")
        else :
            self.__label_error.configure(text="Aucun token enregistré\nRendez-vous\ndans les paramètres pour\nl'enregistrer")
        self.__f_error.grid(row=1, column=0, sticky="nsew")

    def __on_click_repo(self, repo_name):
        for widget in self.__f_info.winfo_children():
            widget.destroy()

        # Configure grid pour __f_info
        self.__f_info.grid_rowconfigure(0, weight=0)  # header
        self.__f_info.grid_rowconfigure(1, weight=1)  # contenu
        self.__f_info.grid_rowconfigure(2, weight=0)  # bouton web
        self.__f_info.grid_columnconfigure(0, weight=1)

        top_frame = aFrame(self.__f_info, height=50,fg_color=self.__f_info.cget("fg_color"))
        top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        info_depots = self.__get_info_depots(repo_name)

        c = aScrollableFrame(self.__f_info)
        p = aScrollableFrame(self.__f_info)
        s = aScrollableFrame(self.__f_info)

        # Placer les frames scrollables avec grid (ligne 1)
        c.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        p.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        s.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        btn_commits = aButton(top_frame, text="Commits",
                                    command=lambda: self.__show_commits(c, s, p))
        btn_pr = aButton(top_frame, text="Pull Requests",
                               command=lambda:  self.__show_pr(c, s, p))
        btn_issues = aButton(top_frame, text="Issues",
                                   command=lambda: self.__show_issues(c, s, p))

        btn_web = aButton(self.__f_info, text="Dépôt GitHub",
                          command=lambda : w.open(info_depots["link"]))

        # Utiliser grid au lieu de pack pour les boutons
        btn_commits.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        btn_pr.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        btn_issues.grid(row=0, column=2, sticky="ew", padx=2, pady=2)

        if info_depots["commit"]:
            list_commit = info_depots["commit"]
            for i, commit in enumerate(list_commit):
                l = aLabel(c,text=commit,font=("Roboto",15,"bold"),wraplength=350,justify="left")
                l.pack(fill="x", padx=5, pady=2)

        if info_depots["pr"]:
            list_pr = info_depots["pr"]
            for i, pr in enumerate(list_pr):
                l = aLabel(p,text=pr,font=("Roboto",15,"bold"),wraplength=250)
                l.pack(fill="x", padx=5, pady=2)

        if info_depots["issue"]:
            list_issue = info_depots["issue"]
            for i, issue in enumerate(list_issue):
                l = aLabel(s,text=issue,font=("Roboto",15,"bold"),wraplength=250)
                l.pack(fill="x", padx=5, pady=2)

        self.__show_commits(c, s, p)
        btn_web.grid(row=2, column=0, sticky="ew", padx=5, pady=5)


    def __get_info_depots(self,repos_name):
        # Récupère l'objet repo stocké plutôt que de faire une nouvelle requête
        depots = self.__list_depo_obj.get(repos_name)

        if depots is None:
            # Fallback en cas de repo non trouvé
            return {"commit":[],"pr":[],"issue":[],"link":""}

        list_commit = []

        for i, commit in enumerate(depots.get_commits()):
            if i >= 20:
                break
            text = f"{commit.commit.author.name} - {commit.commit.message[:50]}"
            list_commit.append(text)

        list_pr = []
        for pr in depots.get_pulls(state="all"):
            text = f"{pr.title} ({pr.state})"
            list_pr.append(text)

        list_issue = []
        for issue in depots.get_issues(state="all"):
            if issue.pull_request is None:
                text = f"{issue.title} ({issue.state})"
                list_issue.append(text)

        return {"commit":list_commit,"pr":list_pr,"issue":list_issue,"link":depots.html_url}

    def __show_commits(self, commit:aScrollableFrame, issue:aScrollableFrame, pr:aScrollableFrame):
        issue.grid_forget()
        pr.grid_forget()
        commit.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def __show_pr(self, commit:aScrollableFrame, issue:aScrollableFrame, pr:aScrollableFrame):
        issue.grid_forget()
        pr.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        commit.grid_forget()

    def __show_issues(self, commit:aScrollableFrame, issue:aScrollableFrame, pr:aScrollableFrame):
        issue.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        pr.grid_forget()
        commit.grid_forget()
