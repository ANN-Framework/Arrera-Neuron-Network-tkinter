from ann_tkinter.gui.GUIBaseTache import GUIBaseTache,gestionnaire


class GUITache(GUIBaseTache):
    def __init__(self, gestionnaire: gestionnaire):
        super().__init__(gestionnaire,
                         gestionnaire.getGestFNC().getFNCTask())
        self._title = f"{self._gestionnaire.getName()} : Tâches"