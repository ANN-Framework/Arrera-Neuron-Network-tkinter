import os
from datetime import datetime
from tkinter import StringVar, filedialog, messagebox
from arrera_tk import aFrame, aLabel, aButton, aEntry, aText
from gui.codehelp.CCHguiBase import CCHguiBase, gestionnaire

# Couleurs des boutons actifs
COLOR_BTN_PRIMARY_FG = ("#6750A4", "#7E57C2")
COLOR_BTN_PRIMARY_HOVER = ("#5B4396", "#9575CD")
COLOR_BTN_TEXT = "#FFFFFF"

# Couleurs des boutons désactivés
COLOR_BTN_DISABLED_FG = ("#E0E0E0", "#2D2A32")
COLOR_BTN_DISABLED_TEXT = ("#8E8E93", "#6E6B75")

# Couleurs des onglets
COLOR_TAB_ACTIVE_FG = ("#6750A4", "#7E57C2")
COLOR_TAB_ACTIVE_TEXT = "#FFFFFF"
COLOR_TAB_INACTIVE_FG = "transparent"
COLOR_TAB_INACTIVE_TEXT = ("#49454F", "#CAC4D0")
COLOR_TAB_INACTIVE_HOVER = ("#E8DEF8", "#383540")


class CHGitGestion(CCHguiBase):
    def __init__(self, gestionnaire: gestionnaire):
        super().__init__(gestionnaire, "Gestion Git")

        self.__fnc_codehelp = self._gestionnaire.getGestFNC().getFNCCodeHelp()
        self.__git = self.__fnc_codehelp.getGitObjet()
        self.__fnc_work = self._gestionnaire.getGestFNC().getFNCWork()

        self.__current_path = ""
        self.__path_var = None
        self.__commit_msg_var = None
        self.__branch_new_var = None
        self.__branch_switch_var = None

        self.__current_tab = "statut"

    def _mainframe(self):
        # Configuration de la fenêtre
        self._screen.minsize(1050, 720)
        self._screen.geometry("1080x750")

        # Variables Tkinter
        self.__path_var = StringVar(self._screen)
        self.__commit_msg_var = StringVar(self._screen)
        self.__branch_new_var = StringVar(self._screen)
        self.__branch_switch_var = StringVar(self._screen)

        # Grille principale directe sur la fenêtre (3 lignes, 2 colonnes)
        # Colonne 0 = 75% (cartes de gauche), Colonne 1 = 25% (cartes de droite)
        self._screen.grid_rowconfigure(0, weight=0)  # Top (Projet actif + statut Git)
        self._screen.grid_rowconfigure(1, weight=1)  # Centre (Onglets + Actions)
        self._screen.grid_rowconfigure(2, weight=0)  # Console / Messages
        self._screen.grid_columnconfigure(0, weight=3)
        self._screen.grid_columnconfigure(1, weight=1)

        # -------------------------------------------------------------
        # 1. BANDEAU SUPÉRIEUR (2 cartes directes sans wrapper)
        # -------------------------------------------------------------

        # 1.A Carte Projet Actif (ligne 0, col 0)
        f_proj = aFrame(self._screen)
        f_proj.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=(10, 5))
        f_proj.grid_columnconfigure(0, weight=1)
        f_proj.grid_columnconfigure(1, weight=0)

        l_proj_title = aLabel(f_proj, text="Projet actif", font=("Roboto", 13, "bold"))
        l_proj_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 2))

        self.__e_path = aEntry(f_proj, textvariable=self.__path_var, state="readonly")
        self.__e_path.grid(row=1, column=0, sticky="ew", padx=(12, 6), pady=(0, 10))

        btn_browse = aButton(
            f_proj,
            text="Choisir dossier...",
            command=self.__choose_folder,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=140,
            height=34
        )
        btn_browse.grid(row=1, column=1, padx=(6, 12), pady=(0, 10))

        # 1.B Carte Git Installé (ligne 0, col 1)
        f_git_status = aFrame(self._screen)
        f_git_status.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(10, 5))
        f_git_status.grid_rowconfigure(0, weight=1)
        f_git_status.grid_columnconfigure(0, weight=1)

        git_installed = self.__git.checkGitInstalled()
        status_text = "Git installé : Oui" if git_installed else "Git installé : Non"
        self.__l_git_installed = aLabel(f_git_status, text=status_text, font=("Roboto", 13, "bold"))
        self.__l_git_installed.grid(row=0, column=0, padx=12, pady=12)

        # -------------------------------------------------------------
        # 2. ZONE CENTRALE (2 cartes directes sans wrapper)
        # -------------------------------------------------------------

        # 2.A Carte Principale Gauche : Onglets & Contenu (ligne 1, col 0)
        f_main_left = aFrame(self._screen)
        f_main_left.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        f_main_left.grid_rowconfigure(1, weight=1)
        f_main_left.grid_columnconfigure(0, weight=1)

        # Barre des onglets (fond transparent pour se fondre dans la carte)
        f_tabs_bar = aFrame(f_main_left, fg_color="transparent")
        f_tabs_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))
        for c in range(4):
            f_tabs_bar.grid_columnconfigure(c, weight=1)

        self.__btn_tab_statut = aButton(
            f_tabs_bar,
            text="Statut",
            command=lambda: self.__switch_tab("statut"),
            height=36
        )
        self.__btn_tab_commit = aButton(
            f_tabs_bar,
            text="Commit",
            command=lambda: self.__switch_tab("commit"),
            height=36
        )
        self.__btn_tab_logs = aButton(
            f_tabs_bar,
            text="Logs",
            command=lambda: self.__switch_tab("logs"),
            height=36
        )
        self.__btn_tab_branches = aButton(
            f_tabs_bar,
            text="Branches",
            command=lambda: self.__switch_tab("branches"),
            height=36
        )

        self.__btn_tab_statut.grid(row=0, column=0, sticky="ew", padx=3)
        self.__btn_tab_commit.grid(row=0, column=1, sticky="ew", padx=3)
        self.__btn_tab_logs.grid(row=0, column=2, sticky="ew", padx=3)
        self.__btn_tab_branches.grid(row=0, column=3, sticky="ew", padx=3)

        # Conteneur des vues (fond transparent)
        self.__f_views_container = aFrame(f_main_left, fg_color="transparent")
        self.__f_views_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.__f_views_container.grid_rowconfigure(0, weight=1)
        self.__f_views_container.grid_columnconfigure(0, weight=1)

        # --- Vue 1 : Statut ---
        self.__v_statut = aFrame(self.__f_views_container, fg_color="transparent")
        self.__v_statut.grid_rowconfigure(1, weight=1)
        self.__v_statut.grid_columnconfigure(0, weight=1)

        h_statut = aFrame(self.__v_statut, fg_color="transparent")
        h_statut.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        h_statut.grid_columnconfigure(0, weight=1)
        aLabel(h_statut, text="Statut du dépôt (git status --short)", font=("Roboto", 13, "bold")).grid(row=0, column=0, sticky="w")
        aButton(
            h_statut,
            text="Rafraîchir",
            command=self.__action_refresh,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=110,
            height=32
        ).grid(row=0, column=1, sticky="e")

        self.__txt_statut = aText(self.__v_statut)
        self.__txt_statut.grid(row=1, column=0, sticky="nsew")

        # --- Vue 2 : Commit ---
        self.__v_commit = aFrame(self.__f_views_container, fg_color="transparent")
        self.__v_commit.grid_rowconfigure(1, weight=1)
        self.__v_commit.grid_columnconfigure(0, weight=1)

        aLabel(
            self.__v_commit,
            text="Rédiger un message de commit (git add . + git commit)",
            font=("Roboto", 13, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.__txt_commit = aText(self.__v_commit)
        self.__txt_commit.grid(row=1, column=0, sticky="nsew")

        btn_do_commit = aButton(
            self.__v_commit,
            text="Valider le commit (git commit)",
            command=self.__action_commit_direct,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            height=38
        )
        btn_do_commit.grid(row=2, column=0, sticky="e", pady=(8, 0))

        # --- Vue 3 : Logs ---
        self.__v_logs = aFrame(self.__f_views_container, fg_color="transparent")
        self.__v_logs.grid_rowconfigure(1, weight=1)
        self.__v_logs.grid_columnconfigure(0, weight=1)

        h_logs = aFrame(self.__v_logs, fg_color="transparent")
        h_logs.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        h_logs.grid_columnconfigure(0, weight=1)
        aLabel(h_logs, text="Historique des commits (git log -n20)", font=("Roboto", 13, "bold")).grid(row=0, column=0, sticky="w")
        aButton(
            h_logs,
            text="Rafraîchir",
            command=self.__refresh_logs,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=110,
            height=32
        ).grid(row=0, column=1, sticky="e")

        self.__txt_logs = aText(self.__v_logs)
        self.__txt_logs.grid(row=1, column=0, sticky="nsew")

        # --- Vue 4 : Branches ---
        self.__v_branches = aFrame(self.__f_views_container, fg_color="transparent")
        self.__v_branches.grid_rowconfigure(1, weight=1)
        self.__v_branches.grid_columnconfigure(0, weight=1)

        h_br = aFrame(self.__v_branches, fg_color="transparent")
        h_br.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        h_br.grid_columnconfigure(0, weight=1)
        aLabel(h_br, text="Branches locales (git branch)", font=("Roboto", 13, "bold")).grid(row=0, column=0, sticky="w")
        aButton(
            h_br,
            text="Rafraîchir",
            command=self.__refresh_branches,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=110,
            height=32
        ).grid(row=0, column=1, sticky="e")

        self.__txt_branches = aText(self.__v_branches)
        self.__txt_branches.grid(row=1, column=0, sticky="nsew")

        # Formulaire création / bascule de branche
        f_br_actions = aFrame(self.__v_branches, fg_color="transparent")
        f_br_actions.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        f_br_actions.grid_columnconfigure(1, weight=1)
        f_br_actions.grid_columnconfigure(4, weight=1)

        aLabel(f_br_actions, text="Nouvelle :").grid(row=0, column=0, padx=4)
        aEntry(f_br_actions, textvariable=self.__branch_new_var).grid(row=0, column=1, sticky="ew", padx=4)
        aButton(
            f_br_actions,
            text="Créer",
            command=self.__action_create_branch,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=80,
            height=32
        ).grid(row=0, column=2, padx=4)

        aLabel(f_br_actions, text="Basculer vers :").grid(row=0, column=3, padx=(12, 4))
        aEntry(f_br_actions, textvariable=self.__branch_switch_var).grid(row=0, column=4, sticky="ew", padx=4)
        aButton(
            f_br_actions,
            text="Basculer",
            command=self.__action_switch_branch,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            width=80,
            height=32
        ).grid(row=0, column=5, padx=4)

        # 2.B Carte Principale Droite : Actions (ligne 1, col 1)
        f_main_right = aFrame(self._screen)
        f_main_right.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        f_main_right.grid_columnconfigure(0, weight=1)
        f_main_right.grid_rowconfigure(6, weight=1)

        aLabel(f_main_right, text="▶ Actions", font=("Roboto", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=14, pady=(12, 8)
        )

        self.__btn_init = aButton(
            f_main_right,
            text="Initialiser dépôt (git init)",
            command=self.__action_init,
            height=38
        )
        self.__btn_add = aButton(
            f_main_right,
            text="Ajouter (git add .)",
            command=self.__action_add,
            height=38
        )
        self.__btn_commit_panel = aButton(
            f_main_right,
            text="Commit...",
            command=lambda: self.__switch_tab("commit"),
            height=38
        )
        self.__btn_create_branch = aButton(
            f_main_right,
            text="Créer une branche...",
            command=lambda: self.__switch_tab("branches"),
            height=38
        )
        self.__btn_switch_branch = aButton(
            f_main_right,
            text="Changer de branche...",
            command=lambda: self.__switch_tab("branches"),
            height=38
        )

        self.__btn_init.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        self.__btn_add.grid(row=2, column=0, sticky="ew", padx=12, pady=4)
        self.__btn_commit_panel.grid(row=3, column=0, sticky="ew", padx=12, pady=4)
        self.__btn_create_branch.grid(row=4, column=0, sticky="ew", padx=12, pady=4)
        self.__btn_switch_branch.grid(row=5, column=0, sticky="ew", padx=12, pady=4)

        # Alerte si dossier non git
        self.__f_not_git_alert = aFrame(f_main_right, fg_color=("#F3EDF7", "#1D1B20"), corner_radius=12)
        self.__f_not_git_alert.grid(row=6, column=0, sticky="sew", padx=12, pady=(16, 12))
        self.__f_not_git_alert.grid_columnconfigure(0, weight=1)

        l_alert_title = aLabel(self.__f_not_git_alert, text="ℹ Ce dossier n'est pas un dépôt Git.", font=("Roboto", 11, "bold"))
        l_alert_title.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 4))

        l_alert_desc = aLabel(
            self.__f_not_git_alert,
            text="Initialisez un dépôt pour commencer à utiliser Git dans ce projet.",
            wraplength=180,
            justify="left",
            font=("Roboto", 10)
        )
        l_alert_desc.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

        btn_alert_init = aButton(
            self.__f_not_git_alert,
            text="Initialiser (git init)",
            command=self.__action_init,
            fg_color=COLOR_BTN_PRIMARY_FG,
            text_color=COLOR_BTN_TEXT,
            hover_color=COLOR_BTN_PRIMARY_HOVER,
            height=36
        )
        btn_alert_init.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        # -------------------------------------------------------------
        # 3. BANDEAU INFÉRIEUR : Console / Messages (ligne 2, span 2)
        # -------------------------------------------------------------
        f_bottom = aFrame(self._screen)
        f_bottom.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        f_bottom.grid_rowconfigure(1, weight=1)
        f_bottom.grid_columnconfigure(0, weight=1)

        aLabel(f_bottom, text="Console / Messages", font=("Roboto", 12, "bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=(8, 4)
        )
        self.__txt_console = aText(f_bottom, height=5)
        self.__txt_console.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 10))

        # Initialisation par défaut du dossier
        self.__init_target_path()
        self.__switch_tab("statut")

    # -----------------------------------------------------------------
    # Gestion de l'état des boutons (couleur + texte garantis lisibles)
    # -----------------------------------------------------------------
    def __set_btn_enabled(self, btn: aButton, enabled: bool):
        if enabled:
            btn.configure(
                state="normal",
                fg_color=COLOR_BTN_PRIMARY_FG,
                text_color=COLOR_BTN_TEXT,
                hover_color=COLOR_BTN_PRIMARY_HOVER
            )
        else:
            btn.configure(
                state="disabled",
                fg_color=COLOR_BTN_DISABLED_FG,
                text_color_disabled=COLOR_BTN_DISABLED_TEXT
            )

    # -----------------------------------------------------------------
    # Gestion du dossier cible
    # -----------------------------------------------------------------
    def __init_target_path(self):
        folder = ""
        if self.__fnc_work and self.__fnc_work.getEtatProject():
            folder = self.__fnc_work.getFolderProject()

        if not folder or not os.path.isdir(folder):
            work_emp = self._gestionnaire.getWorkEmplacement()
            if work_emp and os.path.isdir(work_emp):
                folder = work_emp
            else:
                folder = os.path.expanduser("~")

        self.__set_current_path(folder)

    def __choose_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.__current_path or os.path.expanduser("~"))
        if chosen and os.path.isdir(chosen):
            self.__set_current_path(chosen)

    def __set_current_path(self, path: str):
        self.__current_path = os.path.realpath(path)
        self.__path_var.set(self.__current_path)
        self.__log(f"Dossier sélectionné : {self.__current_path}")
        self.__refresh_all()

    # -----------------------------------------------------------------
    # Onglets
    # -----------------------------------------------------------------
    def __update_tab_buttons(self, active_tab: str):
        tabs = [
            ("statut", self.__btn_tab_statut),
            ("commit", self.__btn_tab_commit),
            ("logs", self.__btn_tab_logs),
            ("branches", self.__btn_tab_branches),
        ]
        for tab_name, btn in tabs:
            if tab_name == active_tab:
                btn.configure(
                    fg_color=COLOR_TAB_ACTIVE_FG,
                    text_color=COLOR_TAB_ACTIVE_TEXT,
                    hover_color=COLOR_BTN_PRIMARY_HOVER
                )
            else:
                btn.configure(
                    fg_color=COLOR_TAB_INACTIVE_FG,
                    text_color=COLOR_TAB_INACTIVE_TEXT,
                    hover_color=COLOR_TAB_INACTIVE_HOVER
                )

    def __switch_tab(self, tab: str):
        self.__current_tab = tab
        self.__update_tab_buttons(tab)

        for v in (self.__v_statut, self.__v_commit, self.__v_logs, self.__v_branches):
            v.grid_remove()

        if tab == "statut":
            self.__v_statut.grid(row=0, column=0, sticky="nsew")
            self.__refresh_status()
        elif tab == "commit":
            self.__v_commit.grid(row=0, column=0, sticky="nsew")
        elif tab == "logs":
            self.__v_logs.grid(row=0, column=0, sticky="nsew")
            self.__refresh_logs()
        elif tab == "branches":
            self.__v_branches.grid(row=0, column=0, sticky="nsew")
            self.__refresh_branches()

    # -----------------------------------------------------------------
    # Actions & Synchronisation
    # -----------------------------------------------------------------
    def __refresh_all(self):
        is_git = self.__git.isGitRepo(self.__current_path)

        if not is_git:
            self.__set_btn_enabled(self.__btn_init, True)
            self.__set_btn_enabled(self.__btn_add, False)
            self.__set_btn_enabled(self.__btn_commit_panel, False)
            self.__set_btn_enabled(self.__btn_create_branch, False)
            self.__set_btn_enabled(self.__btn_switch_branch, False)
            self.__f_not_git_alert.grid()
            self.__set_text(self.__txt_statut, "Ce dossier n'est pas un dépôt Git.")
            self.__set_text(self.__txt_logs, "Aucun historique disponible.")
            self.__set_text(self.__txt_branches, "Aucune branche disponible.")
            self.__log("Ce dossier n'est pas un dépôt Git.")
        else:
            self.__set_btn_enabled(self.__btn_init, False)
            self.__set_btn_enabled(self.__btn_add, True)
            self.__set_btn_enabled(self.__btn_commit_panel, True)
            self.__set_btn_enabled(self.__btn_create_branch, True)
            self.__set_btn_enabled(self.__btn_switch_branch, True)
            self.__f_not_git_alert.grid_remove()

            if self.__current_tab == "statut":
                self.__refresh_status()
            elif self.__current_tab == "logs":
                self.__refresh_logs()
            elif self.__current_tab == "branches":
                self.__refresh_branches()

    def __action_refresh(self):
        self.__refresh_all()
        self.__log("Statut rafraîchi.")

    def __refresh_status(self):
        if self.__git.isGitRepo(self.__current_path):
            status = self.__fnc_codehelp.gitStatus(self.__current_path)
            self.__set_text(self.__txt_statut, status)
        else:
            self.__set_text(self.__txt_statut, "Ce dossier n'est pas un dépôt Git.")

    def __refresh_logs(self):
        if self.__git.isGitRepo(self.__current_path):
            logs = self.__git.getLastLogs(self.__current_path, limit=20)
            self.__set_text(self.__txt_logs, logs)
        else:
            self.__set_text(self.__txt_logs, "Ce dossier n'est pas un dépôt Git.")

    def __refresh_branches(self):
        if self.__git.isGitRepo(self.__current_path):
            branches = self.__git.getBranches(self.__current_path)
            self.__set_text(self.__txt_branches, branches)
        else:
            self.__set_text(self.__txt_branches, "Ce dossier n'est pas un dépôt Git.")

    def __action_init(self):
        succes, out = self.__fnc_codehelp.gitInit(self.__current_path)
        self.__log(f"git init : {out}")
        if succes:
            messagebox.showinfo("Git", f"Dépôt Git initialisé dans {self.__current_path}")
            self.__refresh_all()
        else:
            messagebox.showerror("Erreur Git", out)

    def __action_add(self):
        succes, out = self.__fnc_codehelp.gitAdd(self.__current_path)
        self.__log(f"git add . : {out}")
        if succes:
            messagebox.showinfo("Git", "Fichiers indexés (git add .)")
            self.__refresh_status()
        else:
            messagebox.showerror("Erreur Git", out)

    def __action_commit_direct(self):
        msg = self.__txt_commit.get("1.0", "end").strip()
        if not msg:
            messagebox.showwarning("Message requis", "Veuillez entrer un message de commit.")
            return

        succes, out = self.__fnc_codehelp.gitCommit(msg, self.__current_path)
        self.__log(f"git commit : {out}")
        if succes:
            messagebox.showinfo("Git", f"Commit validé avec succès !\n{out}")
            self.__txt_commit.delete("1.0", "end")
            self.__switch_tab("logs")
            self.__refresh_all()
        else:
            messagebox.showwarning("Git", f"Échec du commit :\n{out}")

    def __action_create_branch(self):
        name = self.__branch_new_var.get().strip()
        if not name:
            messagebox.showwarning("Nom requis", "Veuillez entrer le nom de la nouvelle branche.")
            return

        succes = self.__git.createBranch(self.__current_path, name)
        out = self.__git.getLastOutput()
        self.__log(f"git checkout -b {name} : {out}")
        if succes:
            messagebox.showinfo("Git", f"Branche '{name}' créée et activée.")
            self.__branch_new_var.set("")
            self.__refresh_branches()
        else:
            messagebox.showerror("Erreur Git", out)

    def __action_switch_branch(self):
        name = self.__branch_switch_var.get().strip()
        if not name:
            messagebox.showwarning("Nom requis", "Veuillez entrer le nom de la branche à rejoindre.")
            return

        succes = self.__git.switchBranch(self.__current_path, name)
        out = self.__git.getLastOutput()
        self.__log(f"git checkout {name} : {out}")
        if succes:
            messagebox.showinfo("Git", f"Basculé sur la branche '{name}'.")
            self.__branch_switch_var.set("")
            self.__refresh_branches()
            self.__refresh_status()
        else:
            messagebox.showerror("Erreur Git", out)

    # -----------------------------------------------------------------
    # Utilitaires Texte & Console
    # -----------------------------------------------------------------
    def __set_text(self, text_widget: aText, content: str):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")

    def __log(self, message: str):
        time_str = datetime.now().strftime("%H:%M:%S")
        self.__txt_console.configure(state="normal")
        self.__txt_console.insert("end", f"[{time_str}] {message}\n")
        self.__txt_console.see("end")
        self.__txt_console.configure(state="disabled")