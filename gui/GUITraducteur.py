from tkinter import StringVar
from arrera_tk import *
from gui.guibase import GuiBase,gestionnaire

class GuiTraducteur(GuiBase):
    def __init__(self, gestionnaire: gestionnaire):
        super().__init__(gestionnaire, "Traducteur")
        self._fncTrad = self._gestionnaire.getGestFNC().getFNCTraduction()
        self.__listLang = self._fncTrad.getLang()
        self.__dictLang = self._fncTrad.getLangAndLangCode()

    def _mainframe(self):
        # Variables
        self.__varLangIn = StringVar(self._screen)
        self.__varLangOut = StringVar(self._screen)
        # Frame
        frameTop = aFrame(self._screen)
        frameTrad = aFrame(self._screen)
        # Config Fenetre
        self._screen.grid_columnconfigure(0, weight=1)
        self._screen.grid_rowconfigure(0, weight=0, minsize=60)  # hauteur fixe/mini pour le bandeau haut
        self._screen.grid_rowconfigure(1, weight=1)
        # config frame
        frameTrad.grid_columnconfigure(0, weight=1, uniform="halves")
        frameTrad.grid_columnconfigure(1, weight=1, uniform="halves")
        frameTrad.grid_columnconfigure(2, weight=1, uniform="halves")
        frameTrad.grid_columnconfigure(3, weight=1, uniform="halves")
        frameTrad.grid_rowconfigure(0, weight=0)
        frameTrad.grid_rowconfigure(1, weight=1)
        frameTrad.grid_rowconfigure(2, weight=0)
        # Widgets
        labelTitle = aLabel(frameTop,text=self._gestionnaire.getName()+" : Traducteur",
                            police_size=30)
        self.__textBoxIn = aText(frameTrad)
        self.__textBoxOut = aText(frameTrad)

        btnTrad = aButton(frameTrad,text="Traduire",command=self.__translate,size=20)
        self.__menuLangIn = aOptionMenuLengend(frameTrad,text="Langue d'entrée ",
                                               values=self.__listLang,gridUsed=True)
        self.__menuLangOut = aOptionMenuLengend(frameTrad,text="Langue de sortie ",
                                                values=self.__listLang,gridUsed=True)

        # Placement
        frameTop.grid(row=0, column=0, sticky="ew")
        frameTrad.grid(row=1, column=0, sticky="nsew")

        labelTitle.pack(side="left", anchor="nw", padx=10, pady=5)

        self.__menuLangIn.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(10, 5), pady=(10, 5))
        self.__menuLangOut.grid(row=0, column=2, columnspan=2, sticky="ew", padx=(10, 5), pady=(10, 5))

        self.__textBoxIn.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(10,5), pady=(0,10))
        self.__textBoxOut.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=(5,10), pady=(0,10))

        btnTrad.grid(row=2, column=0, columnspan=4, sticky="ew", padx=10, pady=(0,10))

        self.__clear()

    def __clear(self):
        self.__textBoxIn.delete("1.0","end")
        self.__textBoxOut.delete("1.0","end")
        self.__menuLangIn.set_text("Langue d'entrée")
        self.__menuLangOut.set_text("Langue de sortie")

    def __translate(self):
        langIn = self.__menuLangIn.getValue()
        langOut = self.__menuLangOut.getValue()
        texte = self.__textBoxIn.get("1.0","end").strip()
        self.__textBoxIn.delete("1.0","end")

        if langIn == "Langue d'entrée":
            return

        if langOut == "Langue de sortie":
            return

        if langIn == langOut:
            return

        if not texte:
            return

        codeIn = self.__dictLang.get(langIn)
        codeOut = self.__dictLang.get(langOut)

        if self._fncTrad.setTranlator(codeOut,codeIn):
            traduction = self._fncTrad.tranlate(texte)
            if traduction:
                self.__textBoxOut.delete("1.0","end")
                self.__textBoxOut.insert("1.0",traduction)