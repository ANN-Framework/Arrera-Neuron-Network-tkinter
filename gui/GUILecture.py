from gui.guibase import GuiBase,gestionnaire
from arrera_tk import *

class GUILecture(GuiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Lecture")
        self.__fncLecture = self._gestionnaire.getGestFNC().getFNCRead()

    def _mainframe(self):
        self._screen.grid_rowconfigure(0, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)
        # frame
        self.__frameSetText = aFrame(self._screen)
        self.__frameReadText = aFrame(self._screen)

        # Configuration
        self.__frameSetText.grid_columnconfigure(0, weight=1)
        self.__frameSetText.grid_rowconfigure(0, weight=0)
        self.__frameSetText.grid_rowconfigure(1, weight=1)
        self.__frameSetText.grid_rowconfigure(2, weight=0)

        self.__frameReadText.grid_rowconfigure(0, weight=1)
        self.__frameReadText.grid_columnconfigure(0, weight=1)

        # Widgets
        labelTitle = aLabel(self.__frameSetText, text="Lecture de texte",police_size=30)
        self.__textToRead = aTextScrollable(self.__frameSetText,police_size=20)
        buttonRead = aButton(self.__frameSetText, text="Lire le texte",size=20,command=self.__readText)

        labelViewRead = aLabel(self.__frameReadText, text="Lecture en cours...",police_size=25)

        self.__textToRead.enableTextBox()
        # Placement
        labelTitle.grid(row=0, column=0, padx=12, pady=(12, 8))
        self.__textToRead.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        buttonRead.grid(row=2, column=0, padx=12, pady=(8, 12))

        labelViewRead.grid(row=0, column=0, padx=12, pady=12)

        self.__frameSetText.grid(row=0, column=0, sticky="nsew")

    def __readText(self):
        texte = self.__textToRead.getTextBox().get("1.0", "end-1c")
        self.__textToRead.getTextBox().delete("1.0", "end")
        if texte != "":
            self.__fncLecture.read(texte)
            self.__frameSetText.grid_forget()
            self.__frameReadText.grid(row=0, column=0, sticky="nsew")
            self._screen.after(1000, self.__checkTheard)
        else:
            return

    def __checkTheard(self):
        if self.__fncLecture.getStatTheard():
            self._screen.after(1000, self.__checkTheard)
        else:
            self.__frameReadText.grid_forget()
            self.__frameSetText.grid(row=0, column=0, sticky="nsew")