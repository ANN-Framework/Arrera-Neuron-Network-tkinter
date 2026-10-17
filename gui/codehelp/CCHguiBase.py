from gui.guibase import GuiBase, gestionnaire,abstractmethod

class CCHguiBase(GuiBase):
    def __init__(self,gestionnaire:gestionnaire,name:str):
        super().__init__(gestionnaire,"")
        self._titleGUI = gestionnaire.getName() + " CodeHelp : " + name