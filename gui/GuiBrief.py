from arrera_tk import aLabelImage

from gui.guibase import *
import threading as th
import datetime
import webbrowser

# Design de la page

"""
# Morning Brief et Afternoon Brief
+-----------------------------------------------------------------------------+
| HH:MM - DATE                                    NAME_ASSISTANT : TYPE BRIEF |
+-------------------------+---------------------------------------------------+
| BLOC 1                  | BLOC 2                                            |
|                         |                                                   |
|                         |                                                   |
|                         |                                                   |
|                         |                                                   |
| ----------------------- |                                                   |
| BLOC 3                  |                                                   |
|                         |                                                   |
|                         |                                                   |
|                         |                                                   |
|                         |                                                   |
|                         |                                                   |
+-------------------------+---------------------------------------------------+

## Morning Brief 

- BLOC 1: Meteo prevu dans le journer
- BLOC 2: Tache du jour 
- BLOC 3: Actu 

## Afternoon Brief

- BLOC 1: Meteo actuel et prevu dans l'apres midi
- BLOC 2: Tache 
- BLOC 3: Actu  

# Evening brief

+-----------------------------------------------------------------------------+
| HH:MM - DATE                                    NAME_ASSISTANT : TYPE BRIEF |
+------------------------------------+----------------------------------------+
| Bloc 1                             | bloc 2                                 |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
|                                    |                                        |
+------------------------------------+----------------------------------------+

- BLOC 1 : Meteo
- BLOC 2 : Actu

"""

class guiBrief(GuiBase):
    def __init__(self,gestionnaire:gestionnaire,name:str):
        super().__init__(gestionnaire,f"{gestionnaire.getName()} : {name}")
        self.__readVar = ""
        self.__out_breef = None
        self.__thRead = th.Thread()
        self.__thLoad = th.Thread()

        self.__th_meteo = th.Thread()
        self.__th_actuality = th.Thread()
        self.__th_task = th.Thread()

        self.__fnc_brief = self._gestionnaire.getGestFNC().getFNCBrief()

        self.__name = name

    def _mainframe(self):
        # Configuration de la fenetre
        self._screen.grid_rowconfigure(0, weight=0)
        self._screen.grid_rowconfigure(1, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)
        # Frame
        top_frame = aFrame(self._screen)

        # Configuration des colonnes de top_frame
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        # Widget Topframe
        self.__label_date = aLabel(top_frame, text="HH:MM - JEUDI XX JUILLET XXXX",police_size=20)
        self.__label_title = aLabel(top_frame, text="",police_size=20)
        self.__btn_read = aButton(top_frame, text="Lire")
        
        self.__main_frame = aFrame(self._screen)
        self.__load_frame = aFrame(self._screen)
        load_label = aLabel(self.__load_frame, text="Chargement en cours...", police_size=25)
        load_label.place(relx=0.5, rely=0.5, anchor="center")

        # Placement
        top_frame.grid(row=0, column=0, sticky="ew")

        self.__label_date.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 15))
        self.__label_title.grid(row=0, column=1, pady=(10, 15))
        self.__btn_read.grid(row=0, column=2, sticky="e", padx=10, pady=(10, 15))

    def __get_date(self):
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        date_actuelle = datetime.datetime.now()

        nom_jour = jours[date_actuelle.weekday()]  # .weekday() renvoie 0 pour Lundi, 6 pour Dimanche
        num_jour = date_actuelle.strftime("%d")  # Jour sur 2 chiffres (ex: "24")
        nom_mois = mois[date_actuelle.month - 1].upper()  # Mois en majuscules (ex: "JUILLET")
        annee = date_actuelle.strftime("%Y")  # Année sur 4 chiffres (ex: "2026")

        date_formatee = f"{nom_jour} {num_jour} {nom_mois} {annee}"

        return date_formatee

    def __set_title(self,title:str):
        self.__label_title.configure(text=f"{self.__name}: {title}")
        self._screen.title(f"{self.__name}: {title}")

    def __clear(self):
        for w in self.__main_frame.winfo_children():
            w.destroy()

    def view_morning(self):
        self.active()
        date = self.__get_date()
        self.__set_title("Morning Brief")
        self.__label_date.configure(text=date)
        self.__clear()

        self.__main_frame.grid_rowconfigure(0, weight=1)
        self.__main_frame.grid_rowconfigure(1, weight=1)
        self.__main_frame.grid_columnconfigure(0, weight=1)
        self.__main_frame.grid_columnconfigure(1, weight=2)

        weather = aFrame(self.__main_frame)
        tache = aFrame(self.__main_frame)
        actu = aFrame(self.__main_frame)

        # Affichage Frame
        weather.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        actu.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        tache.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.__th_meteo,self.__th_task,self.__th_actuality = self.__fnc_brief.morning_brief()

        self.__load_frame.grid(row=1, column=0, sticky="nsew")

        self.__update_weather(weather, True)
        self.__update_actu(actu, True)
        self.__update_task(tache,True)
        self.__update_morning()



    def view_afternoon(self):
        self.active()
        date = self.__get_date()
        self.__set_title("Afternoon Brief")
        self.__label_date.configure(text=date)
        self.__clear()

        self.__main_frame.grid_rowconfigure(0, weight=1)
        self.__main_frame.grid_rowconfigure(1, weight=1)
        self.__main_frame.grid_columnconfigure(0, weight=2)
        self.__main_frame.grid_columnconfigure(1, weight=1)

        weather = aFrame(self.__main_frame)
        actu = aFrame(self.__main_frame)
        tache = aFrame(self.__main_frame)

        # Affichage Frame
        weather.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tache.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        actu.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.__th_meteo, self.__th_task, self.__th_actuality = self.__fnc_brief.afternoon_brief()

        self.__load_frame.grid(row=1, column=0, sticky="nsew")

        self.__update_weather(weather, True)
        self.__update_actu(actu, True)
        self.__update_task(tache, True)
        self.__update_morning()

    def view_evening(self):
        self.active()
        date = self.__get_date()
        self.__set_title("Evening Brief")
        self.__label_date.configure(text=date)
        self.__clear()

        self.__main_frame.grid_rowconfigure(0, weight=1)
        self.__main_frame.grid_columnconfigure(0, weight=1)
        self.__main_frame.grid_columnconfigure(1, weight=2)

        weather = aFrame(self.__main_frame)
        actu = aFrame(self.__main_frame)

        # Affichage Frame
        weather.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        actu.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.__th_meteo,self.__th_actuality = self.__fnc_brief.evening_brief()

        self.__load_frame.grid(row=1, column=0, sticky="nsew")

        self.__update_weather(weather, True)
        self.__update_actu(actu, True)
        self.__update_evening_check()

    def __update_morning(self):
        try:
            if self._screen is None or not self._screen.winfo_exists():
                return
        except Exception:
            return
        if not self.__th_meteo.is_alive() and not self.__th_task.is_alive() and not self.__th_actuality.is_alive():
            self.__load_frame.grid_forget()
            self.__main_frame.grid(row=1, column=0, sticky="nsew")
        else :
            self._screen.after(100, self.__update_morning)

    def __update_evening_check(self):
        try:
            if self._screen is None or not self._screen.winfo_exists():
                return
        except Exception:
            return
        if not self.__th_meteo.is_alive() and not self.__th_actuality.is_alive():
            self.__load_frame.grid_forget()
            self.__main_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self._screen.after(100, self.__update_evening_check)

    def __update_weather(self, w_f:aFrame, first:bool=False):
        if first:
            w_f.grid_rowconfigure(0, weight=1)
            w_f.grid_columnconfigure(0, weight=1)
            l = aLabel(w_f,text="Chargement\nde la\nmeteo \nen cours ...")
            l.grid(row=0,column=0,sticky="nsew")

        if self.__th_meteo.is_alive():
            try:
                if self._screen is not None and self._screen.winfo_exists():
                    self._screen.after(100, self.__update_weather, w_f, False)
            except Exception:
                pass
        else :
            for w in w_f.winfo_children():
                w.grid_forget()
                w.destroy()

            data = self.__fnc_brief.get_data_meteo()

            if data is not None:

                t = aLabel(w_f, text="Meteo", police_size=30)

                t.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

                weather_key = list(data.keys())

                for row in range(len(weather_key)+1):
                    w_f.grid_rowconfigure(row, weight=1)
                w_f.grid_columnconfigure(0, weight=1)

                i = 1
                for key in weather_key:
                    meteo_info = data[key]
                    if meteo_info["ok"]:
                        try:
                            l = aLabelImage(w_f, police_size=15,
                                        path_img_light=meteo_info["icon"], height_img=50, widht_img=50,
                                        text=f"{meteo_info['description']} avec {meteo_info['temp']} °C a {meteo_info['town']}")
                        except KeyError:
                            l = aLabel(w_f, police_size=25, text="Imposible d'afficher la meteo")
                    else:
                        l = aLabel(w_f, police_size=25, text="Imposible de recuperer la meteo")

                    l.grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
                    i += 1
            else :
                w_f.grid_rowconfigure(0, weight=1)
                w_f.grid_columnconfigure(0, weight=1)
                l = aLabel(w_f, text="Un probleme est survenu",police_size=20)
                l.grid(row=0, column=0, sticky="nsew")

    def __update_actu(self, a_f:aFrame, first:bool=False):
        if first:
            a_f.grid_rowconfigure(0, weight=1)
            a_f.grid_columnconfigure(0, weight=1)
            l = aLabel(a_f, text="Chargement\ndes actualites \nen cours ...")
            l.grid(row=0, column=0, sticky="nsew")

        if self.__th_actuality.is_alive():
            try:
                if self._screen is not None and self._screen.winfo_exists():
                    self._screen.after(100, self.__update_actu, a_f, False)
            except Exception:
                pass
        else :
            for w in a_f.winfo_children():
                w.grid_forget()
                w.destroy()

            data = self.__fnc_brief.get_data_actu()

            if data is not None:
                cat = list(data.keys())

                a_f.grid_rowconfigure(0, weight=0)
                a_f.grid_rowconfigure(1, weight=1)
                a_f.grid_columnconfigure(0, weight=1)

                label_titre = aLabel(a_f, text="Actualités", police_size=30)
                scroll_f = aScrollableFrame(a_f, fg_color="transparent")

                scroll_f.grid(row=1, column=0, sticky="nsew")
                label_titre.grid(row=0, column=0, sticky="ew")

                scroll_f.grid_columnconfigure(0, weight=1)
                scroll_f.grid_columnconfigure(1, weight=0)
                
                row_idx = 0
                for c in cat:
                    lbl_cat = aLabel(scroll_f, text=c,police_size=30)
                    lbl_cat.grid(row=row_idx, column=0, columnspan=2, sticky="w", pady=(10, 5))
                    row_idx += 1
                    
                    for article in data[c]:
                        titre = article.get("titre", "Sans titre")
                        lien = article.get("lien", "")
                        
                        lbl_titre = aLabel(scroll_f, text=titre, police_size=18,justify="left",
                                           wraplength=550)
                        lbl_titre.grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
                        
                        if lien:
                            btn_lien = aButton(scroll_f, text="Ouvrir", command=lambda l=lien: webbrowser.open(l))
                            btn_lien.grid(row=row_idx, column=1, sticky="e", padx=5, pady=2)
                        
                        row_idx += 1
                        
                        separator = aFrame(scroll_f, height=2, fg_color="gray")
                        separator.grid(row=row_idx, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
                        row_idx += 1

    def __update_task(self, t_f:aFrame, first:bool=False):
        if first:
            t_f.grid_rowconfigure(0, weight=1)
            t_f.grid_columnconfigure(0, weight=1)
            l = aLabel(t_f, text="Chargement\ndes\ntaches \nen cours ...")
            l.grid(row=0, column=0, sticky="nsew")

        if self.__th_task.is_alive():
            try:
                if self._screen is not None and self._screen.winfo_exists():
                    self._screen.after(100, self.__update_task, t_f, False)
            except Exception:
                pass
        else:
            for w in t_f.winfo_children():
                w.grid_forget()
                w.destroy()

            data = self.__fnc_brief.get_data_task()

            if data is not None:
                all_tasks = data["all"]
                today = data["today"]
                projet = data["projet"]

                t_f.grid_rowconfigure(0, weight=0)
                t_f.grid_rowconfigure(1, weight=1)
                t_f.grid_columnconfigure(0, weight=1)

                label_titre = aLabel(t_f, text="Tâches", police_size=30)
                label_titre.grid(row=0, column=0, sticky="ew")

                scroll_f = aScrollableFrame(t_f, fg_color="transparent")
                scroll_f.grid(row=1, column=0, sticky="nsew")
                scroll_f.grid_columnconfigure(0, weight=1)

                row_idx = 0

                if today:
                    lbl_today = aLabel(scroll_f, text="tache du jour", police_size=20
                                       ,justify="left",wraplength=550)
                    lbl_today.grid(row=row_idx, column=0, sticky="w", pady=(10, 5), padx=5)
                    row_idx += 1
                    for t in today:
                        lbl_t = aLabel(scroll_f, text=f"- {t}", police_size=15, justify="left", wraplength=400)
                        lbl_t.grid(row=row_idx, column=0, sticky="w", padx=15, pady=2)
                        row_idx += 1

                if all_tasks:
                    lbl_all = aLabel(scroll_f, text="tout les tache", police_size=20
                                     ,justify="left",wraplength=550)
                    lbl_all.grid(row=row_idx, column=0, sticky="w", pady=(10, 5), padx=5)
                    row_idx += 1
                    for t in all_tasks:
                        lbl_t = aLabel(scroll_f, text=f"- {t}", police_size=15, justify="left", wraplength=400)
                        lbl_t.grid(row=row_idx, column=0, sticky="w", padx=15, pady=2)
                        row_idx += 1

                if projet:
                    lbl_projet = aLabel(scroll_f, text="tache des projet", police_size=20)
                    lbl_projet.grid(row=row_idx, column=0, sticky="w", pady=(10, 5), padx=5)
                    row_idx += 1
                    for t in projet:
                        lbl_t = aLabel(scroll_f, text=f"- {t}", police_size=15, justify="left", wraplength=400)
                        lbl_t.grid(row=row_idx, column=0, sticky="w", padx=15, pady=2)
                        row_idx += 1
