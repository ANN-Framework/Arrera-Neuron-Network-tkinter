from tkinter.messagebox import showerror, showinfo
from arrera_tk import *
from tkinter import END
from gui.guibase import GuiBase,gestionnaire
from gui.GUITaskProject import GUITaskProject

class GUIWork(GuiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Work")
        # Attributs
        self.__emplacementAsset = self._gestionnaire.getConfigFile().asset + "work/"
        self.__fnc_work = gestionnaire.getGestFNC().getFNCWork()
        self.__guiTaskProject = None
        self.__wordOpen = False
        self.__tableurOpen = False
        self.__projectOpen = False

    def _mainframe(self):
        self._screen.grid_rowconfigure(0, weight=0)
        self._screen.grid_rowconfigure(1, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)

        # Image
        img_w_tableur= aImage(path_light=self.__emplacementAsset + "acceuil/tableur.png",
                              width=50, height=50)
        img_w_texte = aImage(path_light=self.__emplacementAsset + "acceuil/word.png",
                                width=50, height=50)
        img_w_project = aImage(path_light=self.__emplacementAsset + "acceuil/project.png",
                                   width=50, height=50)

        # Frame
        f_header = aFrame(self._screen,height=50)
        self.__f_welcome = aFrame(self._screen)
        f_welcome_btn = aFrame(self.__f_welcome)
        f_welcome_task_projet = aFrame(self.__f_welcome)

        self.__f_projet = aFrame(self._screen)
        f_projet_header = aFrame(self.__f_projet,height=50)
        self.__f_projet_body = aFrame(self.__f_projet)
        self.__f_projet_footer = aFrame(self.__f_projet,height=50)

        self.__f_word = aFrame(self._screen)
        f_word_header = aFrame(self.__f_word,height=50)
        self.__f_word_body = aFrame(self.__f_word)
        self.__f_word_footer = aFrame(self.__f_word,height=50)

        self.__f_tableur = aFrame(self._screen)
        f_tableur_header = aFrame(self.__f_tableur, height=50)
        self.__f_tableur_body = aFrame(self.__f_tableur)
        self.__f_tableur_footer = aFrame(self.__f_tableur, height=50)

        # Configuration des grid
        self.__f_welcome.grid_rowconfigure(0, weight=1)
        self.__f_welcome.grid_columnconfigure(0, weight=1)
        self.__f_welcome.grid_columnconfigure(1, weight=1)

        self.__f_projet.grid_rowconfigure(0, weight=0)
        self.__f_projet.grid_rowconfigure(1, weight=1)
        self.__f_projet.grid_rowconfigure(2, weight=0)
        self.__f_projet.grid_columnconfigure(0, weight=1)

        self.__f_word.grid_rowconfigure(0, weight=0)
        self.__f_word.grid_rowconfigure(1, weight=1)
        self.__f_word.grid_rowconfigure(2, weight=0)
        self.__f_word.grid_columnconfigure(0, weight=1)

        self.__f_tableur.grid_rowconfigure(0, weight=0)
        self.__f_tableur.grid_rowconfigure(1, weight=1)
        self.__f_tableur.grid_rowconfigure(2, weight=0)
        self.__f_tableur.grid_columnconfigure(0, weight=1)

        self.__f_projet_body.grid_rowconfigure(0, weight=1)
        self.__f_projet_body.grid_columnconfigure(0, weight=1)

        self.__f_tableur_body.grid_rowconfigure(0, weight=1)
        self.__f_tableur_body.grid_columnconfigure(0, weight=1)

        for i in range(3):
            f_welcome_btn.grid_rowconfigure(i, weight=1)
        f_welcome_btn.grid_columnconfigure(0, weight=1)

        f_welcome_task_projet.grid_rowconfigure(0, weight=0)
        f_welcome_task_projet.grid_rowconfigure(1, weight=1)
        f_welcome_task_projet.grid_columnconfigure(0, weight=1)

        f_projet_header.grid_rowconfigure(0, weight=1)
        f_projet_header.grid_columnconfigure(0, weight=1)

        self.__f_projet_footer.grid_rowconfigure(0, weight=1)
        self.__f_projet_footer.grid_columnconfigure(0, weight=1)

        f_word_header.grid_rowconfigure(0, weight=1)
        f_word_header.grid_columnconfigure(0, weight=1)

        self.__f_word_footer.grid_rowconfigure(0, weight=1)
        self.__f_word_footer.grid_columnconfigure(0, weight=1)

        self.__f_word_body.grid_rowconfigure(0, weight=1)
        self.__f_word_body.grid_columnconfigure(0, weight=1)

        self.__f_tableur_footer.grid_rowconfigure(0, weight=1)
        self.__f_tableur_footer.grid_columnconfigure(0, weight=1)

        f_projet_header.grid_propagate(False)
        self.__f_projet_footer.grid_propagate(False)

        f_word_header.grid_propagate(False)
        self.__f_word_footer.grid_propagate(False)

        f_tableur_header.grid_propagate(False)
        self.__f_tableur_footer.grid_propagate(False)
        # header
        l_title = aLabel(f_header,police_size=30,text=f"{self._gestionnaire.getConfigFile().name} : Work")
        # Welcome
        btn_w_tableur = aButton(f_welcome_btn, text="Tableur",
                                image=img_w_tableur, command=self.__view_tableur)
        btn_w_word = aButton(f_welcome_btn, text="Traitement\nde texte",
                             image=img_w_texte, command=self.__view_word)
        btn_w_projet = aButton(f_welcome_btn,text="Projet",
                               image=img_w_project,command=self.__view_projet)

        # Projet
        l_title_projet = aLabel(f_projet_header,text="Projet",police_size=25)
        btn_p_exit = aButton(self.__f_projet_footer,text="Retour",command=self.__view_acceuil)

        # Welcome Task Projet
        l_title_task = aLabel(f_welcome_task_projet,text="Tache des projets",police_size=25)
        self.__text_view_task = aTextScrollable(f_welcome_task_projet)

        # Word
        l_title_word = aLabel(f_word_header,text="Traitement de texte",police_size=25)

        btn_w_exit = aButton(self.__f_word_footer, text="Retour", command=self.__view_acceuil)

        # Tableur
        l_title_tableur = aLabel(f_tableur_header, text="Tableur", police_size=25)

        btn_t_exit = aButton(self.__f_tableur_footer, text="Retour", command=self.__view_acceuil)
        # Placement
        l_title.pack(pady=10)

        btn_w_tableur.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        btn_w_word.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        btn_w_projet.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        l_title_task.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.__text_view_task.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        f_header.grid(row=0, column=0, sticky="ew")
        f_header.grid_propagate(False)

        f_welcome_btn.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        f_welcome_task_projet.grid(row=0, column=1, sticky="nsew",padx=10,pady=10)

        f_projet_header.grid(row=0, column=0, sticky="ew",padx=10,pady=10)
        self.__f_projet_body.grid(row=1, column=0, sticky="nsew",padx=10,pady=10)
        self.__f_projet_footer.grid(row=2, column=0, sticky="ew",padx=10,pady=10)

        f_word_header.grid(row=0, column=0, sticky="ew",padx=10,pady=10)
        self.__f_word_body.grid(row=1, column=0, sticky="nsew",padx=10,pady=10)
        self.__f_word_footer.grid(row=2, column=0, sticky="ew",padx=10,pady=10)

        f_tableur_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.__f_tableur_body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.__f_tableur_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        l_title_projet.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        btn_p_exit.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)

        l_title_tableur.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        btn_t_exit.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        l_title_word.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)
        btn_w_exit.grid(row=0, column=0, sticky="nsew",padx=10,pady=10)

        self.__f_welcome.grid(row=1, column=0, sticky="nsew")

        self.__load_view_task_projet()

    def __update_etat(self):
        self.__wordOpen = self.__fnc_work.getEtatWord()
        self.__tableurOpen = self.__fnc_work.getEtatTableur()
        self.__projectOpen = self.__fnc_work.getEtatProject()
        if self.__projectOpen:
            self.__guiTaskProject = GUITaskProject(self._gestionnaire,
                                                   self.__fnc_work.getNameProjet(),
                                                   self._gestionnaire.getGestFNC().getFNCWork().getFNCTaskProjet())
        else:
            self.__guiTaskProject = None

    def __load_view_task_projet(self):
        name_project = None
        list_tache = []
        if self.__fnc_work.getEtatProject():
            name_project = self.__fnc_work.getNameProjet()
            self.__fnc_work.closeProjet()
        list_projet = self.__fnc_work.getListProjet()
        if list_projet is not None:
            for projet in list_projet:
                if self.__fnc_work.openProjet(projet):
                    # Récupération des tâches non terminées
                    if self.__fnc_work.setListTacheNoFinishProjet():
                        for i in self.__fnc_work.getListTacheNoFinishProjet():
                            list_tache.append(f"{projet} : {i}")
                    self.__fnc_work.closeProjet()

        self.__text_view_task.enableTextBox()
        self.__text_view_task.getTextBox().delete(1.0, END)

        if list_projet is None:
            self.__text_view_task.getTextBox().insert(END, "Aucun projet enregistré")
        elif len(list_tache) > 0:
            for task in list_tache:
                self.__text_view_task.getTextBox().insert(END, f"{task}\n\n")
        else:
            self.__text_view_task.getTextBox().insert(END, "Aucune tâche enregistrée dans les projets")

        self.__text_view_task.disableTextBox()

        if name_project is not None:
            self.__fnc_work.openProjet(name_project)

    def activeProjet(self):
        self.active()
        self._mainframe()
        self.__view_projet()

    def activeTableur(self):
        self.active()
        self._mainframe()
        self.__view_tableur()

    def activeWord(self):
        self.active()
        self._mainframe()
        self.__view_word()

    def activeAcceuil(self):
        self.active()
        self._mainframe()
        self.__view_acceuil()

    def __view_acceuil(self):
        self.__f_projet.grid_forget()
        self.__f_word.grid_forget()
        self.__f_tableur.grid_forget()
        self.__f_welcome.grid(row=1, column=0, sticky="nsew")

    def __view_word(self):
        self.__f_welcome.grid_forget()
        self.__f_projet.grid_forget()
        self.__f_tableur.grid_forget()
        self.__f_word.grid(row=1, column=0, sticky="nsew")
        if not self.__fnc_work.getEtatWord():
            self.__view_word_noopen()
        else :
            self.__view_word_open()

    def __view_tableur(self):
        self.__f_welcome.grid_forget()
        self.__f_projet.grid_forget()
        self.__f_word.grid_forget()
        self.__f_tableur.grid(row=1, column=0, sticky="nsew")
        if not self.__fnc_work.getEtatTableur():
            self.__view_tableur_noopen()
        else :
            self.__view_tableur_open()


    def __view_projet(self):
        self.__f_welcome.grid_forget()
        self.__f_word.grid_forget()
        self.__f_tableur.grid_forget()
        self.__f_projet.grid(row=1, column=0, sticky="nsew")

        self.__f_projet_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        for widget in self.__f_projet_body.winfo_children():
            widget.destroy()
 
        list_projet = self.__fnc_work.getListProjet()
        f_view_projet = aScrollableFrame(self.__f_projet_body,fg_color=self.__f_projet_body.cget("fg_color"))
        f_view_projet.grid_columnconfigure(0, weight=1)

        i = 0
        for i, p in enumerate(list_projet):
            b = aButton(f_view_projet, text=p, size=17, command=lambda p=p: self.__open_projet(p))
            b.grid(row=i, column=0, sticky="ew", padx=15, pady=15)

        btn_create = aButton(f_view_projet, text="Créer un projet",command=self.__windows_create_projet, size=17)
        if i != 0:
            i += 1

        btn_create.grid(row=i, column=0, sticky="ew", padx=15, pady=15)


        f_view_projet.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def __windows_create_projet(self):
        screen = aTopLevel(width=300, height=125, resizable=False, title="Création d'un projet")
        aLabel(screen, text="Création d'un projet", police_size=25).placeTopCenter()
        entry = aEntryLengend(screen,text="Nom du projet", width=150)
        entry.placeCenter()
        aButton(screen,text="Valider",size=15,command = lambda : self.__create_projet(screen,entry)).placeBottomRight()
        aButton(screen, text="Annuler",size=15).placeBottomLeft()

    def __create_projet(self,s:aTopLevel,e:aEntryLengend):
        projet = e.getEntry().get()
        e.getEntry().delete(0,END)
        if self.__fnc_work.createProjet(projet):
            showinfo("Info", "Projet créé avec succès")
            self.__update_etat()
            self.__view_projet_open()
            s.destroy()
        else :
            showerror("Erreur", "Impossible de créer le projet")


    def __windows_action_projet(self, title:str, texte:str):
        screen = aTopLevel(width=300, height=125,resizable=False,title=title)
        aLabel(screen, text=texte,police_size=25).placeTopCenter()
        entry = aEntry(screen,width=150)
        entry.placeCenter()
        return screen,entry

    def __win_add_type(self):
        screen,entry = self.__windows_action_projet("Type du projet","Entrez le type du projet")
        aButton(screen,text="Enregistrer le type",
                command=lambda: self.__fnc_work.addTypeProjet(entry.get())).placeBottomCenter()

    def __create_file_projet(self, screen: aTopLevel,menu:aOptionMenu):
        name_file = self.__entryNameFile.get()
        if not name_file:
            showerror("Erreur", "Imposible de créer un fichier sans nom.")
            return

        type_file = menu.getValue()

        self.__fnc_work.createFileProject(name_file, type_file)
        screen.destroy()

    def __win_create_file(self):
        """
        Ouvre une fenêtre pour créer un fichier de projet.
        """
        listType = ["excel","xlsx",
                    "word","docx",
                    "Open Document Texte","odt",
                    "markdown","md",
                    "Arrera Postite",".ab"]
        screen = aTopLevel(title="Création d'un fichier de projet",
                           width=300, height=200, resizable=False)


        aLabel(screen, text="Creation d'un\nfichier dans le projet",
               police_size=25).placeTopCenter()
        self.__entryNameFile = aEntry(screen,width=150)
        self.__entryNameFile.placeLeftCenter()
        menuType = aOptionMenu(screen, value=listType).placeRightCenter()
        aButton(screen, text="Valider", command=lambda: self.__create_file_projet(screen,menuType)
                ).placeBottomCenter()

    def __open_task_projet(self):
        self.__update_etat()
        if self.__guiTaskProject is not None :
            self.__guiTaskProject.active()
            return True
        else :
            return False

    def __view_projet_open(self):
        for widget in self.__f_projet_body.winfo_children():
            widget.destroy()

        f_projet = aFrame(self.__f_projet_body,fg_color=self.__f_projet_body.cget("fg_color"))
        frame_center = aFrame(f_projet,fg_color=self.__f_projet_body.cget("fg_color"))

        f_projet.grid_rowconfigure(0, weight=0)
        f_projet.grid_rowconfigure(1, weight=1)
        f_projet.grid_rowconfigure(2, weight=0)
        f_projet.grid_columnconfigure(0, weight=1)

        label_title = aLabel(f_projet, text="",anchor="w")
        btn_bottom = aButton(f_projet, text="Ferme le projet",size=25,
                             command=self.__close_projet)

        label_title.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        frame_center.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        f_projet.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_bottom.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.__f_projet_footer.grid_forget()

        name = self.__fnc_work.getNameProjet()

        label_title.configure(text=f"Projet : {name}", font=("Roboto", 25, "normal"),
                              justify="left")

        for i in range(2):
            frame_center.grid_columnconfigure(i, weight=1)

        for i in range(3):
            frame_center.grid_rowconfigure(i, weight=1)

        buttons = []
        list_image = [aImage(path_light=self.__emplacementAsset +"project/setType-project.png", width=80, height=80),
                      aImage(path_light=self.__emplacementAsset +"project/create-file-project.png", width=80, height=80),
                      aImage(path_light=self.__emplacementAsset +"project/view-task-project.png", width=80, height=80)]

        for i in range(3):
            btn = aButton(frame_center, text="", image=list_image[i])
            buttons.append(btn)

        buttons[0].configure(command=self.__win_add_type)
        buttons[1].configure(command=self.__win_create_file)
        buttons[2].configure(command=self.__open_task_projet)

        buttons[0].grid(row=0, column=0, padx=5, pady=5)
        buttons[1].grid(row=0, column=1, padx=5, pady=5)
        buttons[2].grid(row=1, column=0, padx=5, pady=5)

    def __open_projet(self,name:str):
        if self.__fnc_work.openProjet(name):
            self.__update_etat()
            self.__view_projet_open()


    def __close_projet(self):
        self.__fnc_work.closeProjet()
        self.__guiTaskProject = None
        self.__view_projet()

    def __view_word_noopen(self):
        self.__f_word_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        for widget in self.__f_word_body.winfo_children():
            widget.destroy()

        f = aFrame(self.__f_word_body,fg_color=self.__f_word_body.cget("fg_color"))

        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

        img_open = aImage(path_light=self.__emplacementAsset+"word/open-word.png",
                          width=80, height=80)

        btn_open = aButton(f,text="",image=img_open,command=self.__open_word)

        f.grid(row=0, column=0, sticky="nsew",padx=10, pady=10)

        btn_open.grid(row=0, column=0)

    def __open_word(self):
        if self.__fnc_work.openWord():
            self.__view_word_open()
            self.__update_etat()


    def __close_word(self):
        self.__fnc_work.closeWord()
        self.__view_word_noopen()

    def __view_word_open(self):
        self.__f_word_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        for widget in self.__f_word_body.winfo_children():
            widget.destroy()

        f = aFrame(self.__f_word_body,fg_color=self.__f_word_body.cget("fg_color"))

        f.grid_rowconfigure(0, weight=0)
        f.grid_rowconfigure(1, weight=1)

        f.grid_columnconfigure(0, weight=0)
        f.grid_columnconfigure(1, weight=1)
        f.grid_columnconfigure(2, weight=0)

        l = aLabel(f,text=f"Document : {self.__fnc_work.getNameFileWord()}",police_size=25)

        img_edit = aImage(path_light=self.__emplacementAsset+"word/write-word.png",
                          height=80,width=80)
        img_computer = aImage(path_light=self.__emplacementAsset+"word/open-word-coputer-soft.png",
                              height=80,width=80)
        img_close = aImage(path_light=self.__emplacementAsset+"word/close-word.png",
                           height=80,width=80)

        btn_edit = aButton(f,text="",command=self.__edit_word,
                           image=img_edit)
        btn_computer = aButton(f,text="",command=self.__fnc_work.openWordOs,
                               image=img_computer)
        btn_close = aButton(f,text="",command=self.__close_word,
                            image=img_close)

        f.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        l.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 5), sticky="w")

        btn_edit.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        btn_computer.grid(row=1, column=1)
        btn_close.grid(row=1, column=2, padx=10, pady=10, sticky="e")

    def __edit_word(self):
        if self.__fnc_work.getEtatWord():
            self.__f_word_footer.grid_forget()

            for widget in self.__f_word_body.winfo_children():
                widget.destroy()

            main = aFrame(self.__f_word_body,fg_color=self.__f_word_body.cget("fg_color"))
            b = aFrame(main,fg_color=self.__f_word_body.cget("fg_color"))

            main.grid_rowconfigure(0, weight=0)
            main.grid_rowconfigure(1, weight=1)
            main.grid_rowconfigure(2, weight=0)
            main.grid_columnconfigure(0, weight=1)

            b.grid_columnconfigure(0, weight=0)
            b.grid_columnconfigure(1, weight=1)
            b.grid_columnconfigure(2, weight=0)
            b.grid_rowconfigure(0, weight=0)

            l = aLabel(main,text=f"Edition : {self.__fnc_work.getNameFileWord()} ",police_size=20)

            self.__textbox_word = aTextScrollable(main)

            self.__textbox_word.enableTextBox()
            self.__textbox_word.getTextBox().delete("1.0", "end")
            self.__fnc_work.readWord()
            self.__textbox_word.getTextBox().insert("1.0",self.__fnc_work.getReadWord())

            self.__textbox_word.getTextBox().bind("<KeyRelease>", self.__safe_write_document)

            btn_read = aButton(b, text="Lire", size=15, command=self.__read_word)
            btn_exit = aButton(b,text="Retour",size=15,command=self.__view_word_open)

            main.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            b.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

            l.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
            self.__textbox_word.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
            btn_read.grid(row=0, column=0, sticky="w")
            btn_exit.grid(row=0, column=2, sticky="e")

    def __read_word(self):
        if self.__fnc_work.readWord():
            text = self.__fnc_work.getReadWord()
            if text :
                self._gestionnaire.getArrVoice().say(text)
            else :
                showinfo("Info", "Le document est vide.")
        else :
            showinfo("Erreur", "Une erreur est survenue lors de la lecture du document.")

    def __safe_write_document(self,event=None):
        data = self.__textbox_word.getTextBox().get("1.0", "end")

        self.__fnc_work.writeWordEcrase(data)

    def __view_tableur_noopen(self):
        self.__f_tableur_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        for widget in self.__f_tableur_body.winfo_children():
            widget.destroy()

        f = aFrame(self.__f_tableur_body, fg_color=self.__f_word_body.cget("fg_color"))

        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

        img_open = aImage(path_light=self.__emplacementAsset + "tableur/open-tableur.png",
                          width=80, height=80)

        btn_open = aButton(f, text="", image=img_open,command=self.__open_tableur)

        f.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_open.grid(row=0, column=0)

    def __open_tableur(self):
        if self.__fnc_work.openTableur():
            self.__view_tableur_open()
            self.__update_etat()

    def __close_tableur(self):
        self.__fnc_work.closeTableur()
        self.__view_tableur_noopen()

    def __view_tableur_open(self):
        if self.__fnc_work.getEtatTableur():
            self.__f_tableur_footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
            for widget in self.__f_tableur_body.winfo_children():
                widget.destroy()

            f = aFrame(self.__f_tableur_body, fg_color=self.__f_word_body.cget("fg_color"))

            f.grid_rowconfigure(0, weight=0)
            f.grid_rowconfigure(1, weight=1)

            f.grid_columnconfigure(0, weight=1)
            f.grid_columnconfigure(6, weight=1)

            for i in range(1, 6):
                f.grid_columnconfigure(i, weight=0)

            label = aLabel(f,text=f"Tableur : {self.__fnc_work.getNameFileTableur()}",police_size=25)

            img_view = aImage(path_light=self.__emplacementAsset + "tableur/view-tableur.png",height=80, width=80)
            img_computer = aImage(path_light=self.__emplacementAsset + "tableur/open-tableur-coputer-soft.png",height=80, width=80)
            img_edit = aImage(path_light=self.__emplacementAsset + "tableur/add-valeur.png",height=80, width=80)
            img_close = aImage(path_light=self.__emplacementAsset + "tableur/close-tableur.png",height=80, width=80)

            btn_view = aButton(f, text="",image=img_view,command=self.__read_tableur)
            btn_computer = aButton(f, text="",image=img_computer,command= self.__fnc_work.openTableurOs)
            btn_edit = aButton(f, text="",image=img_edit,command=self.__edit_tableur)
            btn_close = aButton(f, text="",image=img_close,command=self.__close_tableur)

            label.grid(row=0, column=0, columnspan=7, sticky="w", padx=10, pady=(10, 5))

            btn_view.grid(row=1, column=1, padx=5, pady=10)
            btn_computer.grid(row=1, column=2, padx=5, pady=10)
            btn_edit.grid(row=1, column=3, padx=5, pady=10)
            btn_close.grid(row=1, column=4, padx=5, pady=10)

            f.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def __read_tableur(self):
        if self.__fnc_work.readTableur():

            self.__f_tableur_footer.grid_forget()

            for widget in self.__f_tableur_body.winfo_children():
                widget.destroy()

            f = aFrame(self.__f_tableur_body, fg_color=self.__f_word_body.cget("fg_color"))

            f.grid_rowconfigure(0, weight=1)
            f.grid_rowconfigure(1, weight=0)
            f.grid_columnconfigure(0, weight=1)

            b = aButton(f,text="Quitter",size=20,command=self.__view_tableur_open)

            data = self.__fnc_work.getReadTableur()

            if data:
                fscroll = aScrollableFrame(f)
                for row in data:
                    lbl = aLabel(fscroll, text=row+"\n",police_size=15)
                    lbl.configure(anchor="w")
                    lbl.pack(side="top", anchor="w", fill="x", padx=5, pady=2)
                fscroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            else :
                lbl = aLabel(f, text="Le tableur est vide.",police_size=15)
                lbl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

            b.grid(row=1, column=0, padx=10, pady=5)

            f.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def __edit_tableur(self):
        if self.__fnc_work.getEtatTableur():

            list_action = ["Ajout de valeur",
                           "Ajout d'un maximun",
                           "Ajout d'un minimun",
                           "Ajout d'une moyenne",
                           "Ajout d'une somme",
                           "Ajout d'un comptage",
                           "Suppression d'une valeur"]

            self.__f_tableur_footer.grid_forget()

            for widget in self.__f_tableur_body.winfo_children():
                widget.destroy()

            f = aFrame(self.__f_tableur_body, fg_color=self.__f_word_body.cget("fg_color"))

            c = aFrame(f,fg_color=f.cget("fg_color"))
            b = aFrame(f,fg_color=f.cget("fg_color"))

            f.grid_rowconfigure(0, weight=0)
            f.grid_rowconfigure(1, weight=1)
            f.grid_rowconfigure(2, weight=0)
            f.grid_columnconfigure(0, weight=1)

            c.grid_columnconfigure(0, weight=1)

            b.grid_columnconfigure(0, weight=1)
            b.grid_columnconfigure(1, weight=1)

            l_title = aLabel(f,text=f"Edition : {self.__fnc_work.getNameFileTableur()}",police_size=15)

            menu = aOptionMenuLengend(c,text="Action",values=list_action,gridUsed=True)
            menu.getOptionMenu().configure(command=lambda action: self.__change_optionmenu(action,e_1,e_2))

            e_1 = aEntryLengend(c,text="Case",gridUsed=True)
            e_2 = aEntryLengend(c,text="Valeur",gridUsed=True)

            btn1 = aButton(b, text="Annuler",command=self.__view_tableur_open)
            btn2 = aButton(b, text="Valider",
                           command=lambda :self.__set_action(menu,e_1,e_2))

            l_title.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
            c.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
            b.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

            menu.grid(row=0, column=0, sticky="ew", pady=5)
            e_1.grid(row=1, column=0, sticky="ew", pady=5)
            e_2.grid(row=2, column=0, sticky="ew", pady=5)

            btn1.grid(row=0, column=0, padx=5, sticky="ew")
            btn2.grid(row=0, column=1, padx=5, sticky="ew")

            f.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def __change_optionmenu(self,action,ecase:aEntryLengend,eval:aEntryLengend):

        ecase.grid(row=1, column=0, sticky="ew", pady=5)
        eval.grid(row=2, column=0, sticky="ew", pady=5)

        if action == "Ajout de valeur":
            ecase.changeTextLabel("Case : ")
            eval.changeTextLabel("Valeur : ")
        elif action == "Ajout d'un maximun":
            ecase.changeTextLabel("Case de debut : ")
            eval.changeTextLabel("Case de fin : ")
        elif action == "Ajout d'un minimun":
            ecase.changeTextLabel("Case de debut : ")
            eval.changeTextLabel("Case de fin : ")
        elif action == "Ajout d'une moyenne":
            ecase.changeTextLabel("Case de debut : ")
            eval.changeTextLabel("Case de fin : ")
        elif action == "Ajout d'une somme":
            ecase.changeTextLabel("Case de debut : ")
            eval.changeTextLabel("Case de fin : ")
        elif action == "Ajout d'un comptage":
            ecase.changeTextLabel("Case de debut :" )
            eval.changeTextLabel("Case de fin : ")
        elif action == "Suppression d'une valeur":
            ecase.changeTextLabel("Case : ")
            eval.changeTextLabel("")
            eval.grid_forget()

    def __set_action(self,m:aOptionMenuLengend,ecase:aEntryLengend,eval:aEntryLengend):
        if self.__fnc_work.getEtatTableur():
            action = m.getValue()

            case = ecase.getEntry().get()
            val = eval.getEntry().get()

            ecase.getEntry().delete(0, "end")
            eval.getEntry().delete(0, "end")

            if action == "Ajout de valeur":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addValeurOnTableur(case, val):
                    showinfo("Tableur","Valeur ajouter")
            elif action == "Ajout d'un maximun":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addMaximumOnTableur(case, val):
                    showinfo("Tableur", "Maximun ajouter")
            elif action == "Ajout d'un minimun":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addMinimumOnTableur(case, val):
                    showinfo("Tableur", "Minimum ajouter")
            elif action == "Ajout d'une moyenne":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addMoyenneOnTableur(case, val):
                    showinfo("Tableur", "Minimum ajouter")
            elif action == "Ajout d'une somme":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addSommeOnTableur(case, val):
                    showinfo("Tableur", "Somme ajouter")
            elif action == "Ajout d'un comptage":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.addComptageOnTableur(case, val):
                    showinfo("Tableur", "Comptage ajouter")
            elif action == "Suppression d'une valeur":
                if case == "" or val == "":
                    showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                if self.__fnc_work.delValeur(case):
                    showinfo("Tableur", "Valeur supprimer")

            self.__view_tableur_open()

    # Methode qui sert juste a l'ouverture de l'interface de task des projet

    def open_task_projet(self):
        return self.__open_task_projet()

    def open_task_projet_add(self):
        self.__update_etat()
        if self.__guiTaskProject is not None:
            self.__guiTaskProject.activeAdd()
            return True
        else:
            return False

    def open_task_projet_del(self):
        self.__update_etat()
        if self.__guiTaskProject is not None:
            self.__guiTaskProject.activeDel()
            return True
        else:
            return False

    def active_manage_tableur(self):
        self.__update_etat()
        if self.__tableurOpen:
            self.__view_tableur()
            self.__edit_tableur()
            return True
        else :
            return False

    def active_read_tableur(self):
        self.__update_etat()
        if self.__tableurOpen:
            self.__view_tableur()
            self.__read_tableur()
            return True
        else:
            return False

    def active_read_word(self):
        self.__update_etat()
        if self.__wordOpen:
            self.__view_word()
            self.__read_word()
            return True
        else:
            return False

    def active_write_word(self):
        self.__update_etat()
        if self.__wordOpen:
            self.__view_word()
            self.__edit_word()
            return True
        else:
            return False