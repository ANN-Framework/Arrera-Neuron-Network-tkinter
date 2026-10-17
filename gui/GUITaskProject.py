from gui.GUIBaseTache import GUIBaseTache,gestionnaire,fncArreraTache

class GUITaskProject(GUIBaseTache):
    def __init__(self, gestionnaire:gestionnaire,nameProject:str,fncTask:fncArreraTache):
        super().__init__(gestionnaire,fncTask)
        self._title = f"{self._gestionnaire.getName()} : {nameProject} tâches"