from arrera_tk import aFrame, aButton, aLabel, aEntry, aText, aEntryLengend, aTextScrollable
import threading as th
import pyperclip
from gui.guibase import GuiBase,gestionnaire

class GUIMail(GuiBase) :
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Generation et correction de mail")
        self.__fnc_mail = self._gestionnaire.getGestFNC().getFNCMail()
        self.__th_generate = th.Thread()
        self.__index_load = 0

    def _mainframe(self):
        self._screen.grid_rowconfigure(0, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)

        # Frame de chargement plein écran
        self.__load_frame = aFrame(self._screen)
        self.__load_frame.grid_rowconfigure(0, weight=1)
        self.__load_frame.grid_columnconfigure(0, weight=1)
        self.__l_load = aLabel(self.__load_frame, text="Traitement en cours...", police_size=35)
        self.__l_load.grid(row=0, column=0)

        # Frame principale
        self.__main_frame = aFrame(self._screen)
        self.__main_frame.grid_rowconfigure(0, weight=0)
        self.__main_frame.grid_rowconfigure(1, weight=1)
        self.__main_frame.grid_rowconfigure(2, weight=0)
        self.__main_frame.grid_columnconfigure(0, weight=1)

        top_frame = aFrame(self.__main_frame)
        center_frame = aFrame(self.__main_frame)
        bottom_frame = aFrame(self.__main_frame)

        # Frame secondaire
        self.__redaction_frame = aFrame(center_frame,
                                        fg_color=center_frame.cget("fg_color"))
        self.__corrector_frame = aFrame(center_frame,
                                        fg_color=center_frame.cget("fg_color"))
        self.__reponse_frame = aFrame(center_frame,
                                      fg_color=center_frame.cget("fg_color"))

        out_frame = aFrame(center_frame,fg_color=center_frame.cget("fg_color"))

        # Configuration des frames
        top_frame.grid_rowconfigure(0, weight=1)
        for i in range(3):
            top_frame.grid_columnconfigure(i, weight=1, uniform="top_btns")

        # Configuration de center_frame : 2 colonnes (gauche dynamique, droite out_frame)
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(0, weight=1, uniform="center_cols")
        center_frame.grid_columnconfigure(1, weight=1, uniform="center_cols")

        # Configuration de redaction_frame
        self.__redaction_frame.grid_columnconfigure(0, weight=1)
        self.__redaction_frame.grid_rowconfigure(0, weight=0)
        self.__redaction_frame.grid_rowconfigure(1, weight=0)
        self.__redaction_frame.grid_rowconfigure(2, weight=0)
        self.__redaction_frame.grid_rowconfigure(3, weight=1)
        self.__redaction_frame.grid_rowconfigure(4, weight=0)

        # Configuration de corrector_frame
        self.__corrector_frame.grid_columnconfigure(0, weight=1)
        self.__corrector_frame.grid_rowconfigure(0, weight=0)
        self.__corrector_frame.grid_rowconfigure(1, weight=0)
        self.__corrector_frame.grid_rowconfigure(2, weight=0)
        self.__corrector_frame.grid_rowconfigure(3, weight=1)
        self.__corrector_frame.grid_rowconfigure(4, weight=0)

        # Configuration de reponse_frame
        self.__reponse_frame.grid_columnconfigure(0, weight=1)
        self.__reponse_frame.grid_rowconfigure(0, weight=0)
        self.__reponse_frame.grid_rowconfigure(1, weight=0)
        self.__reponse_frame.grid_rowconfigure(2, weight=0)
        self.__reponse_frame.grid_rowconfigure(3, weight=1)
        self.__reponse_frame.grid_rowconfigure(4, weight=0)
        self.__reponse_frame.grid_rowconfigure(5, weight=1)
        self.__reponse_frame.grid_rowconfigure(6, weight=0)

        # Configuration de out_frame
        out_frame.grid_columnconfigure(0, weight=1)
        out_frame.grid_rowconfigure(0, weight=0)
        out_frame.grid_rowconfigure(1, weight=0)
        out_frame.grid_rowconfigure(2, weight=0)
        out_frame.grid_rowconfigure(3, weight=0)
        out_frame.grid_rowconfigure(4, weight=1)

        bottom_frame.grid_rowconfigure(0, weight=1)
        for i in range(3):
            bottom_frame.grid_columnconfigure(i, weight=1, uniform="bottom_btns")

        # Placement de la frame principale et ses sous-frames
        self.__main_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.grid(row=0,column=0,sticky="ew",padx=5,pady=(5, 2))
        center_frame.grid(row=1,column=0,sticky="nsew",padx=5,pady=2)
        bottom_frame.grid(row=2,column=0,sticky="ew",padx=5,pady=(2, 5))

        # Placement de out_frame à droite (colonne 1)
        out_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Affichage de la frame par défaut à gauche (colonne 0)
        self.__show_redaction()

        # Declaration des widget
        btn_redaction = aButton(top_frame, text="Rédaction", command=self.__show_redaction)
        btn_corrector = aButton(top_frame, text="Correction", command=self.__show_corrector)
        btn_reponse = aButton(top_frame, text="Réponse", command=self.__show_reponse)

        btn_clear = aButton(bottom_frame, text="Effacer tout", command=self.__clear_all)
        btn_copie_body = aButton(bottom_frame, text="Copier le corps", command=self.__copy_body)
        btn_copy_all = aButton(bottom_frame, text="Copier tout", command=self.__copy_all)

        # Out
        l_title_out = aLabel(out_frame, text="Sortie", police_size=30)

        l_t_objet = aLabel(out_frame, text="Objet :",police_size=15)
        self.__e_view_objet = aEntry(out_frame)

        l_t_corp = aLabel(out_frame, text="Corps du mail :",police_size=15)
        self.__t_view_copr = aTextScrollable(out_frame)

        # Redaction
        l_title_redaction = aLabel(self.__redaction_frame, text="Redaction d'un mail", police_size=30)
        self.__e_redaction_objet = aEntryLengend(self.__redaction_frame, text="Objet", police_size=15, gridUsed=True)
        l_t_consigne_redaction = aLabel(self.__redaction_frame, text="Informations clés :", police_size=15)
        self.__t_write_consigne = aTextScrollable(self.__redaction_frame)
        self.__t_write_consigne.enableTextBox()
        btn_generate_redaction = aButton(self.__redaction_frame, text="Générer",
                                         command=self.__create_mail)

        # Correction
        l_title_correction = aLabel(self.__corrector_frame, text="Correction", police_size=30)
        self.__e_correction_objet = aEntryLengend(self.__corrector_frame, text="Objet", police_size=15, gridUsed=True)
        l_t_correction_redaction = aLabel(self.__corrector_frame, text="Corp du mail :", police_size=15)
        self.__t_write_correction = aTextScrollable(self.__corrector_frame)
        self.__t_write_correction.enableTextBox()
        btn_generate_correction = aButton(self.__corrector_frame, text="Corriger",
                                          command=self.__correct_mail)

        # Reponse
        l_title_reponse = aLabel(self.__reponse_frame, text="Réponse à un mail", police_size=30)
        self.__e_reponse_objet = aEntryLengend(self.__reponse_frame, text="Objet reçu ", police_size=15, gridUsed=True)
        l_t_reponse_mail = aLabel(self.__reponse_frame, text="Mail reçu :", police_size=15)
        self.__t_write_reponse_mail = aTextScrollable(self.__reponse_frame)
        self.__t_write_reponse_mail.enableTextBox()
        l_t_reponse_consigne = aLabel(self.__reponse_frame, text="Informations clés :", police_size=15)
        self.__t_write_reponse_consigne = aTextScrollable(self.__reponse_frame)
        self.__t_write_reponse_consigne.enableTextBox()
        btn_generate_reponse = aButton(self.__reponse_frame, text="Répondre",
                                       command=self.__reponse_mail)

        # Placement des widget de top et bottom
        btn_redaction.grid(row=0, column=0, sticky="ew", padx=15, pady=5)
        btn_corrector.grid(row=0, column=1, sticky="ew", padx=15, pady=5)
        btn_reponse.grid(row=0, column=2, sticky="ew", padx=15, pady=5)

        btn_clear.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        btn_copie_body.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        btn_copy_all.grid(row=0, column=2, sticky="ew", padx=10, pady=5)

        # Placement des widgets dans redaction_frame
        l_title_redaction.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 10))
        self.__e_redaction_objet.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        l_t_consigne_redaction.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__t_write_consigne.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        btn_generate_redaction.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Placement des widgets dans corrector_frame
        l_title_correction.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 10))
        self.__e_correction_objet.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        l_t_correction_redaction.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__t_write_correction.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        btn_generate_correction.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Placement des widgets dans reponse_frame
        l_title_reponse.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 10))
        self.__e_reponse_objet.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        l_t_reponse_mail.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__t_write_reponse_mail.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 5))
        l_t_reponse_consigne.grid(row=4, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__t_write_reponse_consigne.grid(row=5, column=0, sticky="nsew", padx=10, pady=(0, 10))
        btn_generate_reponse.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Placement des widgets dans out_frame
        l_title_out.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 10))
        l_t_objet.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__e_view_objet.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        l_t_corp.grid(row=3, column=0, sticky="w", padx=10, pady=(5, 2))
        self.__t_view_copr.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def __view_load(self):
        self.__index_load = 0
        self.__l_load.configure(text="Traitement en cours")
        self.__main_frame.grid_forget()
        self.__load_frame.grid(row=0, column=0, sticky="nsew")

    def __create_mail(self):
        objet = self.__e_redaction_objet.getEntry().get()
        text = self.__t_write_consigne.getTextBox().get("1.0", "end")

        self.__t_write_consigne.getTextBox().delete("1.0", "end")
        self.__e_redaction_objet.getEntry().delete(0, "end")

        self.__th_generate = th.Thread(target=self.__fnc_mail.create_mail,
                                       args=(objet, text,))
        self.__th_generate.start()
        self.__view_load()
        self.__update_generate()

    def __correct_mail(self):
        objet = self.__e_correction_objet.getEntry().get()
        text = self.__t_write_correction.getTextBox().get("1.0", "end")

        self.__t_write_correction.getTextBox().delete("1.0", "end")
        self.__e_correction_objet.getEntry().delete(0, "end")

        self.__th_generate = th.Thread(target=self.__fnc_mail.correct_mail,
                                       args=(objet, text,))
        self.__th_generate.start()
        self.__view_load()
        self.__update_generate()

    def __reponse_mail(self):
        objet = self.__e_reponse_objet.getEntry().get()
        text = self.__t_write_reponse_mail.getTextBox().get("1.0", "end")
        consigne = self.__t_write_reponse_consigne.getTextBox().get("1.0", "end")

        self.__e_reponse_objet.getEntry().delete(0, "end")
        self.__t_write_reponse_mail.getTextBox().delete("1.0", "end")
        self.__t_write_reponse_consigne.getTextBox().delete("1.0", "end")

        self.__th_generate = th.Thread(target=self.__fnc_mail.reply_mail,
                                       args=(objet, text, consigne,))
        self.__th_generate.start()
        self.__view_load()
        self.__update_generate()

    def __copy_body(self):
        corps = self.__fnc_mail.get_corps()
        if corps:
            pyperclip.copy(corps)

    def __copy_all(self):
        self.__fnc_mail.copy_mail_complet()

    def __clear_all(self):
        self.__e_redaction_objet.getEntry().delete(0, "end")
        self.__t_write_consigne.getTextBox().delete("1.0", "end")
        self.__e_correction_objet.getEntry().delete(0, "end")
        self.__t_write_correction.getTextBox().delete("1.0", "end")
        self.__e_reponse_objet.getEntry().delete(0, "end")
        self.__t_write_reponse_mail.getTextBox().delete("1.0", "end")
        self.__t_write_reponse_consigne.getTextBox().delete("1.0", "end")
        self.__e_view_objet.delete(0, "end")
        self.__t_view_copr.enableTextBox()
        self.__t_view_copr.getTextBox().delete("1.0", "end")
        self.__t_view_copr.disableTextBox()

    def __hide_all_left_frames(self):
        self.__redaction_frame.grid_forget()
        self.__corrector_frame.grid_forget()
        self.__reponse_frame.grid_forget()

    def __show_redaction(self):
        self.__hide_all_left_frames()
        self.__redaction_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def __show_corrector(self):
        self.__hide_all_left_frames()
        self.__corrector_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def __show_reponse(self):
        self.__hide_all_left_frames()
        self.__reponse_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def __update_generate(self):
        if self.__th_generate.is_alive():
            if self.__index_load == 0:
                text = "Traitement en cours"
                self.__index_load = 1
            elif self.__index_load == 1:
                text = "Traitement en cours."
                self.__index_load = 2
            elif self.__index_load == 2:
                text = "Traitement en cours.."
                self.__index_load = 3
            elif self.__index_load == 3:
                text = "Traitement en cours..."
                self.__index_load = 0

            self.__l_load.configure(text=text)
            self._screen.after(300, self.__update_generate)
        else :
            self.__load_frame.grid_forget()
            self.__main_frame.grid(row=0, column=0, sticky="nsew")

            self.__th_generate = th.Thread()

            objet = self.__fnc_mail.get_objet()
            text = self.__fnc_mail.get_corps()

            self.__e_view_objet.delete(0, "end")
            self.__e_view_objet.insert(0, objet)

            self.__t_view_copr.enableTextBox()
            self.__t_view_copr.getTextBox().delete("1.0", "end")
            self.__t_view_copr.getTextBox().insert("1.0", text)
            self.__t_view_copr.disableTextBox()
