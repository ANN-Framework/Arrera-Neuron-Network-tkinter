from tkinter.messagebox import showerror, askyesno, showinfo
from fnc.fonctionTache import fncArreraTache
from gui.guibase import*
import tkinter as tk
import customtkinter as ctk
from datetime import datetime,date
from functools import partial

class GUIBaseTache(GuiBase):
    def __init__(self, gestionnaire: gestionnaire,fncTask:fncArreraTache):
        super().__init__(gestionnaire,"Tache")
        self._fnctask = fncTask
        self.__directoryAsset = self._gestionnaire.getConfigFile().asset+"tache/"
        self._title = ""

    def _mainframe(self):
        self._screen.title(self._title)
        # Frame
        frameTitle = aFrame(self._screen)
        self.__frameTask = aFrame(self._screen)
        self.__frameAdd = aFrame(self._screen)
        self.__frameAddTask = aFrame(self.__frameAdd)
        frameBTNAdd = aFrame(self.__frameAddTask,fg_color="transparent")
        self.__frameSuppression = aFrame(self._screen)
        self.__frameSuppr = aFrame(self.__frameSuppression,fg_color="transparent")


        # Config

        self.__frameAdd.rowconfigure(0, weight=1)
        self.__frameAdd.columnconfigure(0, weight=1)

        self.__frameAddTask.columnconfigure(0, weight=1)
        self.__frameAddTask.rowconfigure(4, weight=1)

        frameBTNAdd.columnconfigure(0, weight=1)
        frameBTNAdd.columnconfigure(1, weight=1)

        self.__frameSuppression.grid_columnconfigure(0, weight=1)
        self.__frameSuppression.grid_rowconfigure(1, weight=1)

        # img
        imgLogo = aImage(path_light=self.__directoryAsset+"task.png",
                                          path_dark=self.__directoryAsset+"task.png",
                                          width=64, height=64)
        imgSuppr = aImage(path_light=self.__directoryAsset+"task-suppr.png",
                                          path_dark=self.__directoryAsset+"task-suppr.png",
                                            width=32, height=32)
        imgPlus = aImage(path_light=self.__directoryAsset+"task-plus.png",
                                           path_dark=self.__directoryAsset+"task-plus.png",
                                           width=32, height=32)

        self.__imgNoFinish = aImage(path_light=self.__directoryAsset+"task-nofinish.png",
                                                     path_dark=self.__directoryAsset+"task-nofinish.png",
                                                     width=32, height=32)

        self.__imgFinish = aImage(path_light=self.__directoryAsset+"task-finish.png",
                                                     path_dark=self.__directoryAsset+"task-finish.png",
                                                     width=32, height=32)
        # Widgets
        labelLogo = aLabel(frameTitle,text="",image=imgLogo)
        labelTitle = aLabel(frameTitle,text=self._title,police_size=20,wraplength=100)
        btnAddTask = aButton(frameTitle,text="",image=imgPlus,command=self.__viewAddTask)
        btnDelTask = aButton(frameTitle,text="",image=imgSuppr,command=self.__viewSuppr)
        self.__btnFinishTask = aButton(frameTitle,text="",image=self.__imgFinish)

        # Add task frame
        # Add
        labelTitleAddTask = aLabel(self.__frameAddTask, text="Ajouter une tâche",police_size=35)

        self.__entryNameTask = aEntryLengend(self.__frameAddTask,text="Nom de la tache",police_size=20,gridUsed=True)

        f_calendar = aFrame(self.__frameAddTask,fg_color="transparent")
        self.__add_date_task = aCheckBox(f_calendar,text="Mettre une date",boolean_value=False)
        self.__calendarDate = aDateSelector(f_calendar)

        self.__entryDescriptionTask = aEntryLengend(self.__frameAddTask,text="Description",police_size=20,gridUsed=True)

        btnCancelAddTask = aButton(frameBTNAdd,text="Annuler",command=self.__backToMain,size=25)
        btnConfirmAddTask = aButton(frameBTNAdd, text="Confirmer", command=self.__addNewTask,size =25)

        # Supp
        labelTitleSuppr = aLabel(self.__frameSuppression, text="Supprimer une tâche",police_size=35)
        btnBackSuppr = aButton(self.__frameSuppression, text="Retourner a l'acceuil",
                                                command=self.__backToMain,size=25)

        # Placement
        # Widget
        labelLogo.pack(side="left", padx=(10, 5))
        labelTitle.pack(side="left", padx=(5, 10))
        self.__btnFinishTask.pack(side="right", padx=(5, 10))
        btnDelTask.pack(side="right", padx=(5, 10))
        btnAddTask.pack(side="right", padx=(10, 5))

        labelTitleAddTask.grid(row=0, column=0, sticky="n", pady=(10, 8))
        self.__entryNameTask.grid(row=1, column=0, sticky="ew", padx=10, pady=(2, 8))
        f_calendar.grid(row=2, column=0, sticky="", padx=10, pady=(0, 8))
        self.__calendarDate.pack(side="right", padx=10, pady=(0, 8))
        self.__add_date_task.pack(side="left", padx=10, pady=(0, 8))
        self.__entryDescriptionTask.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 8))

        frameBTNAdd.grid(row=5, column=0, sticky="ew", padx=10, pady=(8, 10))

        btnCancelAddTask.grid(row=0, column=0, sticky="w", padx=(0, 5))
        btnConfirmAddTask.grid(row=0, column=1, sticky="e", padx=(5, 0))

        labelTitleSuppr.grid(row=0, column=0, sticky="ew")
        self.__frameSuppr.grid(row=1, column=0, sticky="nsew")
        btnBackSuppr.grid(row=2, column=0, sticky="ew")

        # Frame
        frameTitle.pack(side="top", fill="x", pady=(0, 2))
        self.__frameTask.pack(side="top", fill="both", expand=True, pady=(2, 2))
        self.__viewTaskNoFinish()

    def __disableAllFrame(self):
        self.__frameTask.pack_forget()
        self.__frameAdd.pack_forget()
        self.__frameSuppression.pack_forget()
        self._screen.update()

    def __viewTaskNoFinish(self):
        self.__disableAllFrame()
        self.__frameTask.pack(side="top", fill="both", expand=True, pady=(2, 2))
        # ta liste de tâches
        tasks = self._fnctask.getNoFinishTask()

        self.__btnFinishTask.configure(text="",image=self.__imgFinish,
                                       command=self.__viewTaskFinish)

        # 1) nettoyer le frame si déjà utilisé
        for w in self.__frameTask.winfo_children():
            w.destroy()

        # 2) faire en sorte que le frame parent grandisse correctement
        self.__frameTask.grid_rowconfigure(0, weight=1)
        self.__frameTask.grid_columnconfigure(0, weight=1)

        # 3) un unique conteneur scrollable, toujours
        if len(tasks) != 0:
            container = aScrollableFrame(self.__frameTask)
            container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # 4) les colonnes du conteneur prennent la largeur
            container.grid_columnconfigure(0, weight=1)

            # 5) créer les checkboxes
            self._task_vars = []  # pour relire l'état plus tard
            for i, label in enumerate(tasks):
                var = tk.BooleanVar(value=False)
                cb = ctk.CTkCheckBox(container,text=label,variable=var,command= partial (self.__finishTask,var, label))
                cb.grid(row=i, column=0, sticky="w", padx=8, pady=(0, 4))
                self._task_vars.append(var)
        else:
            labelNoTask = aLabel(self.__frameTask,text="Aucune tâche pour le moment",police_size=40)
            labelNoTask.pack(pady=20)

        self._screen.update()

    def __finishTask(self, var:tk.BooleanVar, name:str):
        if var.get():
            self._fnctask.finishTask(name)
            self.__viewTaskNoFinish()

    def __viewTaskFinish(self):
        self.__disableAllFrame()
        self.__frameTask.pack(side="top", fill="both", expand=True, pady=(2, 2))
        # ta liste de tâches
        tasks = self._fnctask.getFinishTask()

        self.__btnFinishTask.configure(text="",image=self.__imgNoFinish,
                                       command=self.__viewTaskNoFinish)

        # 1) nettoyer le frame si déjà utilisé
        for w in self.__frameTask.winfo_children():
            w.destroy()

        # 2) faire en sorte que le frame parent grandisse correctement
        self.__frameTask.grid_rowconfigure(0, weight=1)
        self.__frameTask.grid_columnconfigure(0, weight=1)

        # 3) un unique conteneur scrollable, toujours
        if len(tasks) != 0:
            container = aScrollableFrame(self.__frameTask)
            container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # 4) les colonnes du conteneur prennent la largeur
            container.grid_columnconfigure(0, weight=1)

            # 5) créer les checkboxes
            self._task_vars = []  # pour relire l'état plus tard
            for i, label in enumerate(tasks):
                var = tk.BooleanVar(value=True)
                cb = ctk.CTkCheckBox(container,text=label, variable=var, command=partial(self.__unfinishTask, var, label))
                cb.grid(row=i, column=0, sticky="w", padx=8, pady=(0, 4))
                self._task_vars.append(var)
        else:
            labelNoTask = aLabel(self.__frameTask,text="Aucune tâche fini pour le moment",police_size=40)
            labelNoTask.pack(pady=20)

        self._screen.update()

    def __unfinishTask(self, var:tk.BooleanVar, name:str):
        if not var.get():
            self._fnctask.unfinishTask(name)
            self.__viewTaskFinish()

    def __viewAddTask(self):
        self.__disableAllFrame()
        self.__entryNameTask.getEntry().delete(0, tk.END)
        self.__frameAdd.pack(side="top", fill="both", expand=True, pady=(2, 2))
        self.__frameAddTask.grid(row=0, column=0, sticky="nsew")
        self._screen.update()

    def __addNewTask(self):
        # Var
        dateAdd = False
        descriptionAdd = False

        name = self.__entryNameTask.getEntry().get()
        if name == "":
            showerror("Erreur",
                      "Le nom de la tâche ne peut pas être vide")
            return



        if self.__add_date_task.getBooleanVar().get():
            date_str = self.__calendarDate.get_date()
            date_calendar = datetime.strptime(date_str, "%Y-%m-%d")
            dateAdd = True

        description = self.__entryDescriptionTask.getEntry().get()
        if description != "":
            descriptionAdd = True
            self.__entryDescriptionTask.getEntry().delete(0, tk.END)

        if dateAdd and not descriptionAdd:
            if not self._fnctask.addTask(name,date=date_calendar):
                showerror("Erreur","La tache n'a pas pu être ajouter")
        elif dateAdd and descriptionAdd:
            if not self._fnctask.addTask(name,date=date_calendar,description=description):
                showerror("Erreur","La tache n'a pas pu être ajouter")
        elif not dateAdd and descriptionAdd:
            if not self._fnctask.addTask(name,description=description):
                showerror("Erreur","La tache n'a pas pu être ajouter")
        else :
            if not self._fnctask.addTask(name):
                showerror("Erreur","La tache n'a pas pu être ajouter")

        self.__viewTaskNoFinish()

    def __backToMain(self):
        self.__frameAdd.grid_forget()
        self.__frameSuppression.pack_forget()
        self.__frameTask.pack(side="top", fill="both", expand=True, pady=(2, 2))
        self._screen.update()
        self.__viewTaskNoFinish()

    def __viewSuppr(self):
        self.__disableAllFrame()
        self.__frameSuppression.pack(side="top", fill="both", expand=True, pady=(2, 2))

        # ta liste de tâches
        tasks = self._fnctask.getAllTask()

        # 1) nettoyer le frame si déjà utilisé
        for w in self.__frameSuppr.winfo_children():
            w.destroy()

        # 2) faire en sorte que le frame parent grandisse correctement
        self.__frameSuppr.grid_rowconfigure(0, weight=1)
        self.__frameSuppr.grid_columnconfigure(0, weight=1)

        # 3) un unique conteneur scrollable, toujours
        if len(tasks) != 0:
            container = aScrollableFrame(self.__frameSuppression)
            container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            # 4) les colonnes du conteneur prennent la largeur
            container.grid_columnconfigure(0, weight=1)

            # 5) créer les checkboxes
            self._task_vars = []  # pour relire l'état plus tard
            for i, label in enumerate(tasks):
                var = tk.BooleanVar(value=False)
                cb = ctk.CTkCheckBox(container,text=label, variable=var, command=partial(self.__delTask,var, label))
                cb.grid(row=i, column=0, sticky="w", padx=8, pady=(0, 4))
                self._task_vars.append(var)
        else:
            labelNoTask = aLabel(self.__frameSuppr,text="Aucune tâche enregistré",police_size=25)
            labelNoTask.pack(pady=20)

        self._screen.update()

    def __delTask(self,var, name:str):
        if var.get():
            if (askyesno("Confirmation",
                         "Voulez vous vraiment supprimer cette tâche ?")):
                self._fnctask.delTask(name)
                showinfo("Tache","Suppression de la tâche effectué")
            self.__backToMain()
            self.__viewTaskNoFinish()

    def activeDel(self):
        self.active()
        self.__viewSuppr()

    def activeFinish(self):
        self.active()
        self.__viewTaskFinish()

    def activeAdd(self):
        self.active()
        self.__viewAddTask()