from arrera_tk import *
from gui.guibase import GuiBase,gestionnaire
import threading as th
import webbrowser

class GuiNews(GuiBase):
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,f"Actualités")
        self.__fnc_news = self._gestionnaire.getGestFNC().getFNCActu()
        self.__th_load = th.Thread()
        self.__cath_launch = ""
        self.__dict_actus = {}

    def __recovery_actu(self):
        #print("launch")
        self.__fnc_news.setActu()
        self.__fnc_news.clear_articles()

    def __get_actu(self):
        self.__th_load = th.Thread(target=self.__recovery_actu)
        self.__th_load.start()
        self.__view_load()
        self.__update_actu()

    def _mainframe(self):
        # Configuration de la grille principale
        self._screen.grid_columnconfigure(0, weight=0)  # Frame gauche fixe
        self._screen.grid_columnconfigure(1, weight=1)  # Frame droite extensible
        self._screen.grid_rowconfigure(0, weight=1)  # Les frames prennent toute la hauteur

        self.__left = aFrame(self._screen)
        self.__right = aFrame(self._screen)
        
        self.__load = aFrame(self._screen)
        self.__load.grid_rowconfigure(0, weight=1)
        self.__load.grid_columnconfigure(0, weight=1)

        self.__right.grid_rowconfigure(0, weight=0)
        self.__right.grid_rowconfigure(1, weight=1)
        self.__right.grid_columnconfigure(0, weight=1)

        self.__left.grid_rowconfigure(0, weight=0)

        for ligne in range(1, 7):
            self.__left.grid_rowconfigure(ligne, weight=0)

        self.__left.grid_columnconfigure(0, weight=1)

        self.__l_cath = aLabel(self.__right,text="",police_size=25,anchor="w",justify="left")
        self.__fs_view_actu = aScrollableFrame(self.__right)
        
        l_load = aLabel(self.__load,text="Chargement des actualités...",police_size=35)
        l_load.grid(row=0, column=0)

        l_title = aLabel(self.__left,text="Catégories",police_size=30)

        btn_cath_all = aButton(self.__left,text="Tout",command=self.__view_all)
        btn_cath_main = aButton(self.__left,text="Généraliste",command=self.__view_main)
        btn_cath_tech = aButton(self.__left,text="Nouvelles technologies",command=self.__view_tech)
        btn_cath_cul = aButton(self.__left,text="Culture",command=self.__view_culture)
        btn_cath_sci = aButton(self.__left,text="Science",command=self.__view_science)
        btn_cath_sport = aButton(self.__left,text="Sport",command=self.__view_sport)

        btn_cath_all.grid(row=1,column=0,sticky="ew",padx=10,pady=25)
        btn_cath_main.grid(row=2, column=0, sticky="ew", padx=10, pady=15)
        btn_cath_tech.grid(row=3, column=0, sticky="ew", padx=10, pady=15)
        btn_cath_cul.grid(row=4, column=0, sticky="ew", padx=10, pady=15)
        btn_cath_sci.grid(row=5, column=0, sticky="ew", padx=10, pady=15)
        btn_cath_sport.grid(row=6, column=0, sticky="ew", padx=10, pady=15)

        self.__l_cath.grid(row=0,column=0,sticky="ew",padx=10,pady=(5, 2))
        self.__fs_view_actu.grid(row=1,column=0,sticky="nsew",padx=10,pady=(5, 10))
        self.__right.bind("<Configure>", self.__on_resize)

        l_title.grid(row=0,column=0,sticky="ew",padx=10,pady=(5, 10))

        self.__right.grid(row=0,column=1,sticky="nsew",padx=(5, 0),pady=0)
        self.__left.grid(row=0,column=0,sticky="nsew",padx=(0, 5),pady=0)

    def __on_resize(self, event):
        width = event.width
        if width <= 50:
            return

        new_wrap = max(200, width - 80)
        new_title_size = max(16, min(26, int(width / 35)))

        for card in self.__fs_view_actu.winfo_children():
            for widget in card.winfo_children():
                if getattr(widget, "_is_title", False):
                    try:
                        widget.configure(wraplength=new_wrap, police_size=new_title_size)
                    except Exception:
                        try:
                            widget.configure(wraplength=new_wrap)
                        except Exception:
                            pass

    def __create_article_widget(self, article: dict):
        titre = article.get("titre", "Sans titre")
        source = article.get("source", "Inconnue")
        lien = article.get("lien", "")

        card = aFrame(self.__fs_view_actu)
        card.pack(fill="x", padx=10, pady=10)

        lbl_titre = aLabel(card, text=titre, police_size=24, justify="left", wraplength=550)
        lbl_titre._is_title = True
        lbl_titre.pack(anchor="w", padx=10, pady=(10, 5))

        lbl_source = aLabel(card, text=f"De {source}", police_size=18, justify="left")
        lbl_source.pack(anchor="w", padx=10, pady=(0, 5))

        if lien:
            btn_open = aButton(card, text="Consulter l'article", command=lambda url=lien: webbrowser.open(url))
            btn_open.pack(anchor="w", padx=10, pady=(5, 10))

    def __format_scrollable_frame(self, type_cath: str):
        for widget in self.__fs_view_actu.winfo_children():
            widget.destroy()

        if not self.__dict_actus:
            return

        articles = []
        if type_cath == "all":
            for cat_list in self.__dict_actus.values():
                articles.extend(cat_list)
        elif type_cath == "main":
            articles = self.__dict_actus.get("Generaliste", [])
        elif type_cath == "tech":
            articles = self.__dict_actus.get("Tech", [])
        elif type_cath == "culture":
            articles = self.__dict_actus.get("Culture", [])
        elif type_cath == "sport":
            articles = self.__dict_actus.get("Sports", []) or self.__dict_actus.get("Sport", [])
        elif type_cath == "science":
            articles = self.__dict_actus.get("Science", [])

        for article in articles:
            self.__create_article_widget(article)

    def __view_load(self):
        self.__right.grid_forget()
        self.__left.grid_forget()
        self.__load.grid(row=0, column=0, columnspan=2, sticky="nsew")

    def __update_actu(self):
        if self.__th_load.is_alive():
            self._screen.after(1000, self.__update_actu)
            #print("update")
        else :
            self.__th_load = th.Thread()
            actus = self.__fnc_news.getActu()

            self.__dict_actus = {}
            for article in actus:
                cat = article.get("cathegorie", "Autre")
                article_clean = {k: v for k, v in article.items() if k != "cathegorie"}
                if cat not in self.__dict_actus:
                    self.__dict_actus[cat] = []
                self.__dict_actus[cat].append(article_clean)

            self.__load.grid_forget()
            self.__right.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=0)
            self.__left.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)

            if self.__cath_launch == "all":
                self.__view_all()
            elif self.__cath_launch == "main":
                self.__view_main()
            elif self.__cath_launch == "tech":
                self.__view_tech()
            elif self.__cath_launch == "culture":
                self.__view_culture()
            elif self.__cath_launch == "sport":
                self.__view_sport()
            elif self.__cath_launch == "science":
                self.__view_science()
            else :
                self.__view_all()

    def __view_main(self):
        self.__l_cath.configure(text="Généraliste")
        self.__format_scrollable_frame("main")

    def __view_all(self):
        self.__l_cath.configure(text="Toutes")
        self.__format_scrollable_frame("all")

    def __view_tech(self):
        self.__l_cath.configure(text="Nouvelles technologies")
        self.__format_scrollable_frame("tech")

    def __view_culture(self):
        self.__l_cath.configure(text="Culture")
        self.__format_scrollable_frame("culture")

    def __view_sport(self):
        self.__l_cath.configure(text="Sport")
        self.__format_scrollable_frame("sport")

    def __view_science(self):
        self.__l_cath.configure(text="Science")
        self.__format_scrollable_frame("science")

    def active_all(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "all"

    def active_main(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "main"

    def active_tech(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "tech"

    def active_culture(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "culture"

    def active_sport(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "sport"

    def active_science(self):
        self.active()
        self.__get_actu()
        self.__cath_launch = "science"