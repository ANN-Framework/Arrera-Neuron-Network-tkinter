from tkinter.messagebox import showerror
from gui.guibase import GuiBase,gestionnaire
from datetime import datetime
from arrera_tk import *


class GUIAgenda(GuiBase):
    def __init__(self, gest: gestionnaire):
        super().__init__(gest, "Agenda")
        self.__fncAgenda = gest.getGestFNC().getFNCCalendar()
        self.__assetPath = self._gestionnaire.getConfigFile().asset+"calendar/"
        self.__dateSelected = None

    def _mainframe(self):
        # Config de la fenetre
        self._screen.rowconfigure(0, weight=1)
        self._screen.columnconfigure(0, weight=1)
        # Creation des frames Maitre
        self.__frameMain = aFrame(self._screen)
        self.__frameAddEvent = aFrame(self._screen)
        self.__frameSuppr = aFrame(self._screen)
        # Frame fille
        frameLogoTitle = aFrame(self.__frameMain,fg_color="transparent")
        frameBTNEvent = aFrame(self.__frameMain,fg_color="transparent")
        frameEventDay = aFrame(self.__frameMain)

        self.__frameAdd = aFrame(self.__frameAddEvent)
        frameBTNFAdd = aFrame(self.__frameAdd)
        self.__frameHeure = aFrame(self.__frameAddEvent)

        frameBTNSuppr = aFrame(self.__frameSuppr)
        # Configuration des frames
        # Frame Main
        self.__frameMain.columnconfigure(0, weight=0)
        self.__frameMain.columnconfigure(1, weight=1)
        self.__frameMain.rowconfigure(0, weight=1)
        self.__frameMain.rowconfigure(1, weight=1)
        self.__frameMain.rowconfigure(2, weight=1)

        frameLogoTitle.grid_columnconfigure(0, weight=0)
        frameLogoTitle.grid_columnconfigure(1, weight=1)
        frameLogoTitle.grid_columnconfigure(2, weight=0)
        frameLogoTitle.grid_rowconfigure(0, weight=1)
        frameLogoTitle.grid_rowconfigure(1, weight=0)
        frameLogoTitle.grid_rowconfigure(2, weight=1)

        frameBTNEvent.grid_columnconfigure(0, weight=1)
        frameBTNEvent.grid_columnconfigure(1, weight=0)
        frameBTNEvent.grid_columnconfigure(2, weight=1)
        frameBTNEvent.grid_rowconfigure(0, weight=0)
        frameBTNEvent.grid_rowconfigure(1, weight=1, minsize=24)
        frameBTNEvent.grid_rowconfigure(2, weight=0)

        frameEventDay.grid_columnconfigure(0, weight=1)
        frameEventDay.grid_rowconfigure(0, weight=0)
        frameEventDay.grid_rowconfigure(1, weight=0)
        frameEventDay.grid_rowconfigure(2, weight=1)

        self.__frameAddEvent.rowconfigure(0, weight=1)
        self.__frameAddEvent.columnconfigure(0, weight=1)

        self.__frameAdd.grid_columnconfigure(0, weight=1)
        self.__frameAdd.grid_rowconfigure(0, weight=0)
        self.__frameAdd.grid_rowconfigure(1, weight=0)
        self.__frameAdd.grid_rowconfigure(2, weight=0)
        self.__frameAdd.grid_rowconfigure(3, weight=0)
        self.__frameAdd.grid_rowconfigure(4, weight=0)
        self.__frameAdd.grid_rowconfigure(5, weight=0)
        self.__frameAdd.grid_rowconfigure(6, weight=1)
        self.__frameAdd.grid_rowconfigure(7, weight=0)

        frameBTNFAdd.grid_columnconfigure(0, weight=0)
        frameBTNFAdd.grid_columnconfigure(1, weight=1)
        frameBTNFAdd.grid_columnconfigure(2, weight=0)
        frameBTNFAdd.grid_rowconfigure(0, weight=0)

        self.__frameHeure.grid_columnconfigure(0, weight=1, uniform="col")
        self.__frameHeure.grid_columnconfigure(1, weight=1, uniform="col")
        self.__frameHeure.grid_columnconfigure(2, weight=1, uniform="col")
        self.__frameHeure.grid_rowconfigure(0, weight=0)
        self.__frameHeure.grid_rowconfigure(1, weight=1)
        self.__frameHeure.grid_rowconfigure(2, weight=0)

        self.__frameSuppr.grid_columnconfigure(0, weight=1, uniform="col")
        self.__frameSuppr.grid_columnconfigure(1, weight=1, uniform="col")
        self.__frameSuppr.grid_columnconfigure(2, weight=1, uniform="col")
        self.__frameSuppr.grid_rowconfigure(0, weight=0)
        self.__frameSuppr.grid_rowconfigure(1, weight=1)
        self.__frameSuppr.grid_rowconfigure(2, weight=0)

        frameBTNSuppr.grid_columnconfigure(0, weight=1, uniform="btns")
        frameBTNSuppr.grid_columnconfigure(1, weight=1, uniform="btns")
        frameBTNSuppr.grid_columnconfigure(2, weight=1, uniform="btns")
        frameBTNSuppr.grid_rowconfigure(0, weight=0)

        # Frame Add Event
        # Asset
        assetLogo = aImage(path_light=self.__assetPath+"calendar.png",
                                       path_dark=self.__assetPath+"calendar.png",
                                       width=64, height=64)

        # Widget
        # Frame Main
        # Logo et titre
        lLogoApp = aLabel(frameLogoTitle,image=assetLogo)
        lTitleApp = aLabel(frameLogoTitle,
                           text=self._gestionnaire.getName()+" : Agenda",
                           police_size=20)

        # Boutons
        btnCreateEvent = aButton(frameBTNEvent,text="Créer\nun événement",size=15,
                                                  command=self.__viewAddEvent)
        btnSupprimerEvent = aButton(frameBTNEvent, text="Supprimer\nun événement",size=15,
                                                     command=self.__viewSuppr)

        # Calendrier
        self.__miniCalendar = aDateSelector(self.__frameMain,
                                            month_format="letter",
                                            command=self.__dateSelectedOnCalendar)

        # Jour
        self.__labelDate = aLabel(frameEventDay,text="DATE",police_size=20)
        self.__labelEvent = aLabel(frameEventDay,text="EVENT",police_size=20)

        # Frame Add Event
        self.__labelTitleAddEvent = aLabel(self.__frameAdd,text="Ajouter un événement",police_size=30)
        self.__calendarAddEvent = aDateSelector(self.__frameAdd)
        self.__labelDateSelected = aLabel(self.__frameAdd,police_size=20)
        self.__entryNameEvent = aEntryLengend(self.__frameAdd,text="Titre",police_size=20,gridUsed=True)
        self.__entryDescriptionEvent = aEntryLengend(self.__frameAdd,police_size=20,text="Description",gridUsed=True)
        self.__entryLieuEvent = aEntryLengend(self.__frameAdd,police_size=20,text="Lieu",gridUsed=True)
        self.__checkHour = aCheckBox(self.__frameAdd,text="Définir une heure",boolean_value=False)

        btnAddEvent = aButton(frameBTNFAdd,text="Ajouter",size=20,command=self.__addNewEvent)
        btnCancelEvent = aButton(frameBTNFAdd,text="Annuler",size=20,command=self.__backToMain)

        # Partie hour
        labelHour = aLabel(self.__frameHeure,text="Selectionner l'heure",police_size=20)

        self.__hour_picker = aHourPickers(self.__frameHeure)

        self.__btnValiderHour = aButton(self.__frameHeure,text="Valider",size=15)
        btnCancelHour = aButton(self.__frameHeure,text="Annuler",size=15,command=self.__backToMain)
        # Partie suppr
        labelSuppr = aLabel(self.__frameSuppr,text="Supprimer un événement",police_size=20)
        self.__selectMenuSuppr = None
        btnSupprEvent = aButton(frameBTNSuppr,text="Supprimer",size=20,command=self.__supprEvent)
        btnCancelSuppr = aButton(frameBTNSuppr,text="Annuler",size=20,command=self.__backToMain)
        # Placement des frames
        frameEventDay.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=0, pady=0)
        frameLogoTitle.grid(row=0, column=0, sticky="nw", padx=0, pady=0)
        frameBTNEvent.grid(row=1, column=0, sticky="w", padx=(40, 0), pady=0)

        # Placement des widgets
        # Logo et titre
        lLogoApp.grid(row=1, column=0, sticky="w")
        lTitleApp.grid(row=1, column=2, sticky="e")
        # Boutons
        btnCreateEvent.grid(row=0, column=1, sticky="n")
        btnSupprimerEvent.grid(row=2, column=1, sticky="s")
        # Mini calendrier
        self.__miniCalendar.grid(row=2, column=0, sticky="sw", padx=0, pady=0)
        # Jour
        self.__labelDate.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 5))
        self.__labelEvent.grid(row=1, column=0, sticky="w",  padx=10, pady=(0, 10))

        # Ajout Event
        self.__labelTitleAddEvent.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        self.__entryNameEvent.grid(row=2, column=0, sticky="ew", padx=12, pady=6)
        self.__entryDescriptionEvent.grid(row=3, column=0, sticky="ew", padx=12, pady=6)
        self.__entryLieuEvent.grid(row=4, column=0, sticky="ew", padx=12, pady=6)
        self.__checkHour.grid(row=5, column=0, sticky="ew", padx=12, pady=6)
        btnCancelEvent.grid(row=0, column=0, sticky="w", padx=(10, 6), pady=8)
        btnAddEvent.grid(row=0, column=2, sticky="e", padx=(6, 10), pady=8)
        frameBTNFAdd.grid(row=7, column=0, sticky="sew", padx=12, pady=12)

        labelHour.grid(row=0, column=0, columnspan=3, sticky="n", pady=(10, 5))               # haut-centre
        self.__hour_picker.grid(row=1, column=1, sticky="")                               # centre-centre
        btnCancelHour.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))    # bas-gauche
        self.__btnValiderHour.grid(row=2, column=2, sticky="e", padx=10, pady=(5, 10))  # bas-droite

        labelSuppr.grid(row=0, column=0, columnspan=3, sticky="n", pady=(10, 5))
        frameBTNSuppr.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(5, 10))
        btnCancelSuppr.grid(row=0, column=0, sticky="w", padx=10)
        btnSupprEvent.grid(row=0, column=2, sticky="e", padx=10)

        # Affichage principal
        self.__frameMain.grid(row=0, column=0, sticky="nsew")

        # Ajout de l'affichage des event du jour
        self.__viewEventDay(datetime.today().strftime("%Y-%m-%d"))
        
        # Check du mini calendar 
        # (Event is now handled by the command argument in aDateSelector)
        self._screen.update()

    def __backToMain(self):
        self.__frameAddEvent.grid_forget()
        self.__frameSuppr.grid_forget()
        self.__frameMain.grid(row=0, column=0, sticky="nsew")
        self._screen.update()

    def __viewEventDay(self, date):
        """date (YYYY-MM-DD)"""
        self.__labelDate.configure(text=date)
        try :
            listEvent = self.__fncAgenda.checkEventWithDate(date)
            if not listEvent:
                self.__labelEvent.configure(text="Aucun événement")
                return True
            else :
                texte = ""
                for event in listEvent:
                    texte += "- " + event + "\n"
                self.__labelEvent.configure(text=texte)
            self.__dateSelected = date
            self._screen.update()
            return True
        except Exception as e:
            return False
    
    def __dateSelectedOnCalendar(self, event_or_date):
        if isinstance(event_or_date, str):
            date_str = event_or_date
        else:
            date_str = self.__miniCalendar.get_date()
        self.__viewEventDay(date_str)

    def __viewAddEvent(self):

        self.__calendarAddEvent.grid_forget()
        self.__labelDateSelected.grid_forget()

        self.__calendarAddEvent.grid(row=1, column=0, sticky="n",  padx=12, pady=6)

        self.__frameMain.grid_forget()
        self.__frameHeure.grid_forget()
        self.__frameAddEvent.grid(row=0, column=0, sticky="nsew")
        self.__frameAdd.grid(row=0, column=0, sticky="nsew")
        self._screen.update()

    def __addNewEvent(self):
        name = self.__entryNameEvent.getEntry().get()
        if name == "" :
            showerror("Erreur",
                      "Le nom de l'événement ne peut pas être vide")
            return False
        description = self.__entryDescriptionEvent.getEntry().get()
        lieu = self.__entryLieuEvent.getEntry().get()

        # Clear des champs
        self.__entryNameEvent.getEntry().delete(0, 'end')
        self.__entryDescriptionEvent.getEntry().delete(0, 'end')
        self.__entryLieuEvent.getEntry().delete(0, 'end')

        if self.__dateSelected is not None:
            date = datetime.strptime(self.__dateSelected, "%Y-%m-%d").date()
        else :
            date = datetime.strptime(self.__calendarAddEvent.get_date(), "%Y-%m-%d").date()

        if self.__checkHour.getBooleanVar().get():
            self.__frameAdd.grid_forget()
            self.__frameHeure.grid(row=0, column=0, sticky="nsew")
            self.__btnValiderHour.configure(command = lambda :
            self.__fncAgenda.addEventToCalendar(name=name, date=date,
                                                descrption=description, lieu=lieu,
                                                heure=str(self.__hour_picker.getValueHour()+":"+
                                                          self.__hour_picker.getValueMinute()))
            and self.__backToMain())
            return True

        if self.__fncAgenda.addEventToCalendar(name=name, date=date, descrption=description, lieu=lieu):
            self.__backToMain()
            self.__viewEventDay(date)
            return True

        else :
            showerror("Erreur",
                      "Une erreur est survenue lors de l'ajout de l'événement")
            return False

    def __viewSuppr(self):
        del  self.__selectMenuSuppr
        listEvent = self.__fncAgenda.getAllEvents()
        if not listEvent :
            showerror("Erreur","Aucun événement à supprimer")
            return False

        self.__selectMenuSuppr = aOptionMenu(self.__frameSuppr,value=listEvent)

        self.__selectMenuSuppr.grid(row=1, column=1, sticky="", pady=10)

        self.__frameAddEvent.grid_forget()
        self.__frameSuppr.grid(row=0, column=0, sticky="nsew")
        self.__frameMain.grid_forget()
        self._screen.update()
        return True

    def __supprEvent(self):
        name = self.__selectMenuSuppr.getValue()
        if name == "" :
            showerror("Erreur",
                      "Aucun événement sélectionné")
            return False

        if self.__fncAgenda.delEvent(name):
            self.__backToMain()
            return True
        else :
            showerror("Erreur",
                      "Une erreur est survenue lors de la suppression de l'événement")
            return False

    def activeAdd(self):
        self.active()
        self.__viewAddEvent()

    def activeDel(self):
        self.active()
        self.__viewSuppr()