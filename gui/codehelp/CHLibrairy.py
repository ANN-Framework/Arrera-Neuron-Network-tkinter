import base64
from tkinter import StringVar
from arrera_tk import *
from gui.codehelp.CCHguiBase import CCHguiBase,gestionnaire
import webbrowser as wb
import requests


class CHLibrairy(CCHguiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Librairie")
        self.__index_content = None
        self.__listLib = []
        self.__dictURLName = {}

    def __testConnection(self):
        if self._gestionnaire.getNetworkObjet().getEtatInternet():
            try:
                response = requests.get(
                    "https://raw.githubusercontent.com/Arrera-Librairy/index-codehelp/refs/heads/main/index.json")
                response.raise_for_status()
                contenuJson = response.json()

                self.__index_content = contenuJson
                return True

            except requests.exceptions.RequestException as e:
                return False
        else:
            return False

    def _mainframe(self):
        self._screen.grid_rowconfigure(0, weight=0)
        self._screen.grid_rowconfigure(1, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)
        # Frame
        self.__h_frame = aFrame(self._screen)
        self.__f_main = aFrame(self._screen)
        self.__f_error = aFrame(self._screen)

        self.__left_panel = aFrame(self.__f_main)
        self.__right_panel = aFrame(self.__f_main)

        self.__h_frame.grid_rowconfigure(0, weight=1)
        self.__h_frame.grid_columnconfigure(0, weight=1)

        self.__f_error.grid_rowconfigure(0, weight=1)
        self.__f_error.grid_rowconfigure(2, weight=1)
        self.__f_error.grid_columnconfigure(0, weight=1)

        self.__f_main.grid_rowconfigure(0, weight=1)
        self.__f_main.grid_columnconfigure(0, weight=1)
        self.__f_main.grid_columnconfigure(1, weight=3)

        self.__left_panel.grid_columnconfigure(0, weight=1)

        self.__right_panel.grid_rowconfigure(0, weight=1)
        self.__right_panel.grid_columnconfigure(0, weight=1)

        # Widget
        # welcome Frame
        label_title = aLabel(self.__h_frame, text="CodeHelp : librairie",police_size=30)

        # Error Frame
        label_error = aLabel(self.__f_error, text="Impossible de récupérer l'index",police_size=25)

        self.__readme_box = aText(self.__right_panel)
        self.__readme_box.configure(state="disabled")

        self.__readme_box.grid(row=0, column=0, sticky="nsew")

        # Affichage
        self.__h_frame.grid(row=0, column=0, sticky="nsew")

        label_title.grid(row=0, column=0, sticky="nsew")
        label_error.grid(row=1, column=0)

        self.__left_panel.grid(row=0, column=0, sticky="nsew")
        self.__right_panel.grid(row=0, column=1, sticky="nsew")

        # Teste de la connection
        if self.__testConnection():
            self.__show_main()
        else :
            self.__show_error()


    def __show_error(self):
        self.__f_main.grid_remove()
        self.__f_error.grid(row=1, column=0, sticky="nsew")

    def __show_main(self):
        self.__f_error.grid_remove()

        for i, key in enumerate(self.__index_content):
            lib = self.__index_content[key]

            frame = aFrame(self.__left_panel)
            frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)

            frame.grid_columnconfigure(0, weight=1)

            # Nom
            label = aLabel(frame, text=lib["name"])
            label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

            # Bouton README
            btn_readme = aButton(
                frame,
                text="README",
                command=lambda l=lib: self.__show_readme(l)
            )
            btn_readme.grid(row=0, column=1)

            # Bouton GitHub
            btn_git = aButton(
                frame,
                text="GitHub",
                command=lambda url=lib["url"]: wb.open(url)
            )
            btn_git.grid(row=0, column=2)

        self.__f_main.grid(row=1, column=0, sticky="nsew")

    def __get_readme(self, owner, repo):
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"

        r = requests.get(url)

        if r.status_code != 200:
            return "README introuvable"

        data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8")

        return content

    def __parse_github_url(self, url):
        parts = url.split("/")
        return parts[-2], parts[-1]

    def __show_readme(self, lib):
        owner, repo = self.__parse_github_url(lib["url"])
        content = self.__get_readme(owner, repo)

        self.__readme_box.configure(state="normal")
        self.__readme_box.delete("1.0", "end")
        self.__readme_box.insert("end", content)
        self.__readme_box.configure(state="disabled")