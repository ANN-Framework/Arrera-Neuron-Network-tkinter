from fnc.fonctionArreraDownload import *
from tkinter.messagebox import showerror,showinfo
import threading as th
from gui.guibase import GuiBase,gestionnaire
from arrera_tk import *


class GUIArreraDownload(GuiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Arrera Download")
        # Mise en place de objet
        self.__objetArrera = CArreraDownload()

    def _mainframe(self):
        self._screen.geometry("450x450")
        self._screen.resizable(False,False)
        # Initilisation du theard
        self.__tDownload = th.Thread()
        # Var
        self.__listMode = ["Vidéo simple", "Juste son", "Juste vidéo"]
        # Frame
        # main
        self.__fMain = aFrame(self._screen, width=450, height=450)
        # Download
        self.__fDownload = aFrame(self._screen, width=450, height=450)
        # Widget
        # fmain
        labelTitle = aLabel(self.__fMain, text="Arrera Download",font=("Roboto",30,"bold"))

        self.__entryURL = aEntry(self.__fMain,width=400)
        btnDownload = aButton(self.__fMain, text="Telecharger", command=self.__downlaodView,size=20)
        self.__modeSelection = aOptionMenu(self.__fMain,value=self.__listMode)

        # fDownload
        self.__labelDownload = aLabel(self.__fDownload, text="",font=("Roboto",25,"bold"))
        # fmain
        labelTitle.placeTopCenter()
        self.__modeSelection.place(x=10, y=60)
        btnDownload.placeBottomCenterNoStick()
        self.__entryURL.placeCenter()
        # fDonwload
        self.__labelDownload.placeCenter()
        self.__fMain.placeCenter()

    def __backMain(self):
        self.__fMain.placeCenter()

    def __downlaodView(self):
        url = self.__entryURL.get()
        self.__entryURL.delete(0, END)
        folder = self._gestionnaire.getUserConf().getVideoDownloadFolder()
        if folder == "":
            showerror("Download", "Aucun dossier de telechargement enregistrer")
            return
        else:
            self.__objetArrera.setDownloadFolderDur(folder)

        # Recuperation du mode
        mode = self.__modeSelection.getValue()

        if mode == self.__listMode[0]:
            self.__objetArrera.setMode(1)
        elif mode == self.__listMode[1]:
            self.__objetArrera.setMode(2)
        elif mode == self.__listMode[2]:
            self.__objetArrera.setMode(3)
        if url == "":
            showerror("Download", "Aucun URL")
            return
        self.__objetArrera.setURL(url)
        self.__tDownload = th.Thread(target=self.__objetArrera.download)

        self.__fMain.place_forget()
        self.__fDownload.placeCenter()
        self.__labelDownload.configure(text="Telechargement en cours...")
        self.__tDownload.start()
        self._screen.after(500, self.__downloadCheck)

    def __downloadCheck(self):
        if self.__tDownload.is_alive():
            text1 = "Telechargement en cours..."
            text2 = "Telechargement en cours......"
            text3 = "Telechargement en cours........."

            textLabel = self.__labelDownload.cget("text")

            if textLabel == text1:
                self.__labelDownload.configure(text=text2)
            elif textLabel == text2:
                self.__labelDownload.configure(text=text3)
            else:
                self.__labelDownload.configure(text=text1)

            self._screen.after(500, self.__downloadCheck)
        else:
            showinfo("Download", "Telechargement terminer")
            self.__fDownload.place_forget()
            self.__tDownload = th.Thread()
            self.__fMain.placeCenter()
            self._screen.update()