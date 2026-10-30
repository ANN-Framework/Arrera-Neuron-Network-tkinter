from abc import abstractmethod
from gestionnaire.gestion import*
from arrera_tk import *

class GuiBase:
    def __init__(self,gestionnaire:gestionnaire,name:str):
        # Init objet
        self._gestionnaire = gestionnaire
        self._titleGUI = self._gestionnaire.getName() + " : " + name
        self.__icon = self._gestionnaire.getIcon()
        # Init de la var de la fenetre
        self._screen = None

    @abstractmethod
    def _mainframe(self):
        pass

    def active(self):
        self._screen = aTopLevel(
            title=self._titleGUI,
            width=800,
            height=600,
            resizable=True,
            icon=self.__icon)
        self._mainframe()
