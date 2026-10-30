from abc import abstractmethod
from gestionnaire.gestion import gestionnaire
from arrera_tk import aTopLevel
from ann_tkinter.confTkinter import confTkinter

class GuiBase:
    _global_conf_tk: confTkinter = None

    def __init__(self, gest: gestionnaire, name: str, conf_tk: confTkinter = None):
        self._gestionnaire = gest
        # Utilise conf_tk direct, sinon la conf globale définie par le manager, sinon fallback par défaut
        self._conf_tk = conf_tk or GuiBase._global_conf_tk or confTkinter()
        self._titleGUI = self._gestionnaire.getName() + " : " + name
        self.__icon = self._conf_tk.icon
        self._screen = None

    @classmethod
    def set_global_conf(cls, conf: confTkinter):
        cls._global_conf_tk = conf

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