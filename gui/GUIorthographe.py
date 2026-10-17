import threading as th
from gui.guibase import GuiBase,gestionnaire
from tkinter.messagebox import showinfo
from arrera_tk import *
from tkinter import END

class GUIOrthographe(GuiBase) :
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Correcteur de texte")
        self.__corrector = self._gestionnaire.getGestFNC().getFNCOrthographe()

        self.__index_load = 0

        self.__th_correction = th.Thread()

        self.__correction_is_ok = False

        self.__original_text = ""
        self.__text_corrected = ""

    def _mainframe(self):
        # Parametrage de la fenetre
        self._screen.rowconfigure(0, weight=1)
        self._screen.columnconfigure(0, weight=1)
        # Frame
        self.__f_load = aFrame(self._screen)

        self.__frame_main =  aFrame(self._screen)
        f_center = aFrame(self.__frame_main)

        f_no_corrected = aFrame(f_center)
        f_corrected = aFrame(f_center)

        f_button = aFrame(self.__frame_main)

        # Parametrage des grid
        # Frame Correct
        self.__frame_main.grid_rowconfigure(1, weight=1)
        self.__frame_main.grid_columnconfigure(0, weight=1)

        f_center.grid_rowconfigure(0, weight=1)
        f_center.grid_rowconfigure(1, weight=1)
        f_center.grid_columnconfigure(0, weight=1)

        for i in range(3):
            f_button.grid_columnconfigure(i, weight=1)

        f_no_corrected.grid_rowconfigure(1, weight=1)
        f_no_corrected.grid_columnconfigure(0, weight=1)

        f_corrected.grid_rowconfigure(1, weight=1)
        f_corrected.grid_columnconfigure(0, weight=1)

        self.__f_load.grid_rowconfigure(0, weight=1)
        self.__f_load.grid_columnconfigure(0, weight=1)

        # Widget
        # Label
        l_title = aLabel(self.__frame_main, text="Outil de correction orthographique", police_size=35)
        l_no_corrected = aLabel(f_no_corrected,text="Texte non corrigé",police_size=25)
        l_corrected = aLabel(f_corrected,text="Texte corrigé",police_size=25)
        self.__l_correction = aLabel(self.__f_load, text="",police_size=30)

        # ScrolledText
        self.__text_in = aTextScrollable(f_no_corrected)
        self.__text_out = aTextScrollable(f_corrected)
        # Bouton
        btn_corrected = aButton(f_button,text="Corriger",size=15,command=self.__check_texte)
        btn_clear  = aButton(f_button,text="Effacer",size=15,command=self.__clear_all)
        btn_copi = aButton(f_button, text="Copier", size=15, command=self.__copy_text)

        # Placement

        # Frame
        self.__frame_main.grid(row=0, column=0, sticky="nsew")
        f_center.grid(row=1, column=0, sticky="nsew")
        f_no_corrected.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        f_corrected.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        f_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Widget
        l_title.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        l_no_corrected.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        l_corrected.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))

        self.__l_correction.grid(row=0, column=0, sticky="nsew")

        self.__text_in.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.__text_out.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        btn_clear.grid(row=0, column=0, sticky="ew", padx=10,pady=10)
        btn_corrected.grid(row=0, column=1, sticky="ew", padx=10,pady=10)
        btn_copi.grid(row=0, column=2, sticky="ew", padx=10,pady=10)

        self.__text_in.enableTextBox()

    def setTexte(self,texte:str):
        self.__text_in.enableTextBox()
        self.__text_in.getTextBox().delete(1.0, END)
        self.__text_in.getTextBox().insert(END, texte)

    def __check_texte(self):
        text = self.__text_in.getTextBox().get(1.0, END)

        self.__th_correction = th.Thread(target=self.__correction_text,args=(text,))
        self.__th_correction.start()

        self.__frame_main.grid_forget()
        self.__f_load.grid(row=0, column=0, sticky="nsew")

        self._screen.after(100,self.__updating_during_correction)


    def __correction_text(self,text):
        self.__original_text = text
        self.__text_corrected = self.__corrector.corrected_text(text)

    def __updating_during_correction(self):
        if self.__th_correction.is_alive():
            if self.__index_load == 0 :
                text = "Correction en cours"
                self.__index_load =+1
            elif self.__index_load == 0 :
                text = "Correction en cours."
                self.__index_load = +1
            elif self.__index_load == 0 :
                text = "Correction en cours.."
                self.__index_load = +1
            elif self.__index_load == 0 :
                text = "Correction en cours..."
                self.__index_load = +1
            else :
                text = "Correction en cours...."
                self.__index_load = 0

            self.__l_correction.configure(text=text)

            self._screen.after(300, self.__updating_during_correction)
        else :
            self.__f_load.grid_forget()
            self.__frame_main.grid(row=0, column=0, sticky="nsew")

            if self.__text_corrected:
                self.__text_corrected = self.__corrector.getCorrections()

                self.__text_out.enableTextBox()
                self.__text_out.getTextBox().delete(1.0, END)
                self.__text_out.getTextBox().insert(END, self.__text_corrected)
                self.__text_out.disableTextBox()
            else:
                showinfo("Orthographe", "Impossible de faire la correction")


    def __copy_text(self):
        if copie_text(self.__text_corrected):
            showinfo("Info","Texte corriger copier")
        else :
            showinfo("Info","Le texte n'a pas pu être corrigé")

    def __clear_all(self):
        self.__text_out.enableTextBox()
        self.__text_out.getTextBox().delete(1.0, END)
        self.__text_out.disableTextBox()

        self.__text_in.getTextBox().delete(1.0, END)