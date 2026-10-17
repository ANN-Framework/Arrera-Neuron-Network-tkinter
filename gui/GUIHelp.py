from gui.guibase import GuiBase,gestionnaire
from arrera_tk import *

class GUIHelp(GuiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Aide")
        self._textRead = ""

    def _mainframe(self):
        self._screen.minsize(500, 620)
        self._screen.maxsize(500, 620)

        self._screen.grid_columnconfigure(0, weight=1)
        self._screen.grid_rowconfigure(0, weight=0, minsize=25)
        self._screen.grid_rowconfigure(1, weight=1)
        self._screen.grid_rowconfigure(2, weight=0, minsize=25)

        # Frame
        topFrame = aFrame(self._screen)
        labelFrame = aFrame(self._screen)
        btnFrame = aFrame(self._screen)

        # Conf frame
        labelFrame.grid_rowconfigure(0, weight=1)
        labelFrame.grid_columnconfigure(0, weight=1)

        # IMG
        imgLogo = aImage(path_dark=self._gestionnaire.getConfigFile().icon,
                                          path_light=self._gestionnaire.getConfigFile().icon,
                                          width=50,height=50)
        # Widgets
        logoLabel = aLabel(topFrame,image=imgLogo)
        self._titleLabel = aLabel(topFrame, text="", font=("Roboto", 30, "bold"))

        btnRead = aButton(btnFrame,text="Lire")
        btnQuit = aButton(btnFrame,text="Quitter",command=self._screen.destroy)
        self._textBox = aTextScrollable(labelFrame)
        # Affichage
        logoLabel.pack(side="left", anchor="center", padx=(6, 10), pady=6)
        self._titleLabel.pack(side="left", anchor="center", pady=6)

        btnRead.pack(side="left", anchor="center", padx=(6, 10), pady=6)
        btnQuit.pack(side="right", anchor="center", pady=6)

        self._textBox.grid(row=0, column=0, sticky="nsew")

        topFrame.grid(row=0, column=0, sticky="nsew")
        labelFrame.grid(row=1, column=0, sticky="nsew")
        btnFrame.grid(row=2, column=0, sticky="nsew")

    def activeHelp(self, texte:str):
        self.active()
        self._textBox.enableTextBox()
        self._textBox.getTextBox().delete(1.0, "end")
        self._textBox.getTextBox().insert("end", texte)
        self._textBox.disableTextBox()
        self._titleLabel.configure(text="Aide")
        self._textRead = texte