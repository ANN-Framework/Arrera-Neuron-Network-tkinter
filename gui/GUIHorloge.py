from arrera_tk import *
from gui.guibase import GuiBase,gestionnaire

class GUIHorloge(GuiBase):
    def __init__(self, gest: gestionnaire):
        super().__init__(gest, "Horloge")
        self.__fncHorloge = self._gestionnaire.getGestFNC().getFNCHorloge()
        self.__assetDirectory = self._gestionnaire.getConfigFile().asset+"horloge/"
        self.__clockEnable = False
        self.__minuteurEnable = False

    def _mainframe(self):
        # Conf de la fenetre
        self._screen.grid_rowconfigure(0, weight=0)
        self._screen.grid_rowconfigure(1, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)
        # Frame principal
        self.__frameNav = aFrame(self._screen)
        self.__frameHorloge = aFrame(self._screen)
        self.__frameChrono = aFrame(self._screen)
        self.__frameMinuteur = aFrame(self._screen)

        # Frame secondaire
        self.__frameSetMinuteur = aFrame(self.__frameMinuteur)
        self.__frameViewMinuteur = aFrame(self.__frameMinuteur)

        # Conf frame
        self.__frameNav.grid_columnconfigure(0, weight=1)  # espace à gauche
        self.__frameNav.grid_columnconfigure(1, uniform="btns")
        self.__frameNav.grid_columnconfigure(2, uniform="btns")
        self.__frameNav.grid_columnconfigure(3, uniform="btns")
        self.__frameNav.grid_columnconfigure(4, weight=1)
        self.__frameNav.grid_rowconfigure(0, weight=0)

        self.__frameHorloge.grid_rowconfigure(0, weight=1)
        self.__frameHorloge.grid_columnconfigure(0, weight=1)

        self.__frameMinuteur.grid_rowconfigure(0, weight=1)
        self.__frameMinuteur.grid_columnconfigure(0, weight=1)

        self.__frameSetMinuteur.grid_rowconfigure(0, weight=1)
        self.__frameSetMinuteur.grid_rowconfigure(1, weight=1)
        self.__frameSetMinuteur.grid_rowconfigure(2, weight=1)
        self.__frameSetMinuteur.grid_columnconfigure(0, weight=1, uniform="cols")
        self.__frameSetMinuteur.grid_columnconfigure(1, weight=1, uniform="cols")
        self.__frameSetMinuteur.grid_columnconfigure(2, weight=1, uniform="cols")

        self.__frameViewMinuteur.grid_columnconfigure(0, weight=1)

        self.__frameViewMinuteur.grid_rowconfigure(0, weight=1)
        self.__frameViewMinuteur.grid_rowconfigure(1, weight=0)
        self.__frameViewMinuteur.grid_rowconfigure(2, weight=0)
        self.__frameViewMinuteur.grid_rowconfigure(3, weight=1)

        self.__frameChrono.grid_columnconfigure(0, weight=1, uniform="cols")
        self.__frameChrono.grid_columnconfigure(1, weight=1, uniform="cols")
        self.__frameChrono.grid_columnconfigure(2, weight=1, uniform="cols")
        self.__frameChrono.grid_rowconfigure(0, weight=1)
        self.__frameChrono.grid_rowconfigure(1, weight=0)
        self.__frameChrono.grid_rowconfigure(2, weight=0)
        self.__frameChrono.grid_rowconfigure(3, weight=1)

        # img
        tailleIMG = 30
        imgHorloge = aImage(path_dark=self.__assetDirectory+"horloge.png",
                                             path_light=self.__assetDirectory+"horloge.png",
                                             width=tailleIMG,height=tailleIMG)
        imgChrono = aImage(path_dark=self.__assetDirectory+"chronometre.png",
                                             path_light=self.__assetDirectory+"chronometre.png",
                                             width=tailleIMG,height=tailleIMG)
        imgMinuteur = aImage(path_dark=self.__assetDirectory+"minuteur.png",
                                             path_light=self.__assetDirectory+"minuteur.png",
                                             width=tailleIMG,height=tailleIMG)

        # Widget
        # Nav
        btnHorloge = aButton(self.__frameNav,text="",image=imgHorloge,
                                              command=self.__viewHorloge)
        btnMinuteur = aButton(self.__frameNav,text="",image=imgMinuteur,
                                               command=self.__viewMinuteur)
        btnChrono = aButton(self.__frameNav,text="",image=imgChrono,
                                             command=self.__viewChrono)
        # Horloge
        self.__labelViewClock = aLabel(self.__frameHorloge,text="00:00:00",font=("Roboto", 45, "bold"))

        # Minuteur
        # Set Minuteur
        self.__picket_minuteur = aHourPickers(self.__frameSetMinuteur,minute_pickers=True)
        btnReset = aButton(self.__frameSetMinuteur,text="Reset",command=self.__resetMinuteur)
        btnStartMinuteur1 = aButton(self.__frameSetMinuteur,text="Start",command=self.__startMinuteur)
        btnStartMinuteur2 = aButton(self.__frameSetMinuteur,text="1 Min",command=self.__setOneMin)
        btnStartMinuteur3 = aButton(self.__frameSetMinuteur, text="3 Min",command=self.__setThreeMin)

        # View Minuteur
        self.__labelViewTimeMinuteur = aLabel(self.__frameViewMinuteur,text="00:00:00",font=("Roboto", 45, "bold"))
        btnStopMinuteur = aButton(self.__frameViewMinuteur,text="Stop",command=self.__fncHorloge.stopMinuteur)

        # Chrono
        self.__labelViewChrono = aLabel(self.__frameChrono,text="00:00:00",font=("Roboto", 45, "bold"))

        btnResetChrono = aButton(self.__frameChrono,text="Reset",command=self.__resetChrono)

        self.__btnStartStopChrono = aButton(self.__frameChrono,text="Start",command=self.__enableOrDisableChrono)

        # Placement des widget
        btnHorloge.grid( row=0, column=1, padx=(8, 8), pady=10)
        btnMinuteur.grid(row=0, column=2, padx=(8, 8), pady=10)
        btnChrono.grid( row=0, column=3, padx=(8, 8), pady=10)

        self.__labelViewClock.grid(row=0, column=0, padx=10, pady=10)

        self.__picket_minuteur.grid(row=1, column=1, padx=12, pady=12)
        btnStartMinuteur2.grid(row=1, column=0, padx=8, pady=8)
        btnStartMinuteur3.grid(row=1, column=2, padx=8, pady=8)
        btnReset.grid(row=2, column=1, padx=8, pady=(6, 2))
        btnStartMinuteur1.grid(row=3, column=1, padx=8, pady=(2, 12))

        self.__labelViewChrono.grid(row=1, column=1, padx=12, pady=12)
        btnResetChrono.grid(row=2, column=0, padx=10, pady=(6, 12))
        self.__btnStartStopChrono.grid(row=2, column=2, padx=10, pady=(6, 12))

        self.__labelViewTimeMinuteur.grid(row=1, column=0, padx=12, pady=12)
        btnStopMinuteur.grid(row=2, column=0, padx=12, pady=(8, 16))

        self.__frameNav.grid(row=0, column=0, sticky="ew")
        self.__frameHorloge.grid(row=1, column=0, sticky="nsew")

        self.__clockEnable = True
        self.__activeClock()

    def __disableAllFrame(self):
        self.__frameHorloge.grid_forget()
        self.__frameChrono.grid_forget()
        self.__frameMinuteur.grid_forget()

    def __viewHorloge(self):
        self.__disableAllFrame()
        self.__clockEnable = True
        self.__activeClock()
        self.__frameHorloge.grid(row=1, column=0, sticky="nsew")

    def __viewMinuteur(self):
        self.__disableAllFrame()
        self.__clockEnable = False
        self.__frameMinuteur.grid(row=1, column=0, sticky="nsew")
        if self.__minuteurEnable:
            self.__frameSetMinuteur.grid_forget()
            self.__frameViewMinuteur.grid(row=0, column=0, sticky="nsew")
        else :
            self.__frameViewMinuteur.grid_forget()
            self.__frameSetMinuteur.grid(row=0, column=0, sticky="nsew")

    def activeMinuteur(self):
        self.active()
        self.__viewMinuteur()

    def __viewChrono(self):
        self.__disableAllFrame()
        self.__clockEnable = False
        self.__frameChrono.grid(row=1, column=0, sticky="nsew")

    def activeChrono(self):
        self.active()
        self.__viewChrono()

    # Horloge
    def __activeClock(self):
        if self.__clockEnable:
            current_time = self.__fncHorloge.getHorloge()
            self.__labelViewClock.configure(text=current_time)
            self._screen.after(1000, self.__activeClock)

    # Minuteur
    def __setThreeMin(self):
        self.__picket_minuteur.setValueHour("03")
        self.__picket_minuteur.setValueMinute("00")

    def __setOneMin(self):
        self.__picket_minuteur.setValueHour("01")
        self.__picket_minuteur.setValueMinute("00")

    def __resetMinuteur(self):
        self.__picket_minuteur.setValueHour("00")
        self.__picket_minuteur.setValueMinute("00")
        self.__labelViewTimeMinuteur.configure(text="00:00:00")

    def __startMinuteur(self):
        min = self.__picket_minuteur.getValueHour()
        sec = self.__picket_minuteur.getValueMinute()
        if min == "" and sec == "":
            return False
        try :
            min = int(min)
            sec = int(sec)

            time = min * 60 + sec
            if time <= 0:
                return False
            else :
                self.__fncHorloge.startMinuteur(time)
                self.__minuteurEnable = True
                self.__frameViewMinuteur.grid(row=0, column=0, sticky="nsew")
                self.__frameSetMinuteur.grid_forget()
                self._screen.after(1, self.__updateMinuteur)
                return True
        except ValueError:
            return False

    def __updateMinuteur(self):
        self.__minuteurEnable = self.__fncHorloge.getStatMinuteur()
        if self.__minuteurEnable:
            time = self.__fncHorloge.getTimeMinuteur()
            if time is None:
                self.__minuteurEnable = False
                self.__labelViewTimeMinuteur.configure(text="00:00:00")
                self.__frameViewMinuteur.grid_forget()
                self.__frameSetMinuteur.grid(row=0, column=0, sticky="nsew")
                return False
            else :
                self.__labelViewTimeMinuteur.configure(text=time)
                self._screen.after(1, self.__updateMinuteur)
                return True
        else:
            self.__minuteurEnable = False
            self.__frameViewMinuteur.grid_forget()
            self.__frameSetMinuteur.grid(row=0, column=0, sticky="nsew")
            return False

    # Chrono

    def __enableOrDisableChrono(self):
        if not self.__fncHorloge.getStatChrono():
            self.__btnStartStopChrono.configure(text="Stop")
            self.__fncHorloge.startChrono()
            self._screen.after(100, self.__updateChrono)
        else :
            self.__btnStartStopChrono.configure(text="Start")
            self.__fncHorloge.stopChrono()

    def __updateChrono(self):
        if self.__fncHorloge.getStatChrono():
            time = self.__fncHorloge.getTimeChrono()

            total_cs = int(round(time * 100))           # 1 s = 100 centièmes
            minutes, rem_cs = divmod(total_cs, 60 * 100)  # 6000 = 60s * 100cs
            seconds, centiseconds = divmod(rem_cs, 100)

            time = f"{minutes:02d}:{seconds:02d}:{centiseconds:02d}"

            self.__labelViewChrono.configure(text=str(time))
            self._screen.after(100, self.__updateChrono)

    def __resetChrono(self):
        self.__fncHorloge.resetChrono()
        self.__fncHorloge.stopChrono()
        self.__btnStartStopChrono.configure(text="Start")
        self.__labelViewChrono.configure(text="00:00:00")

