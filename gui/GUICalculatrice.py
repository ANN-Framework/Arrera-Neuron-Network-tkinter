from tkinter.messagebox import showerror
from gui.guibase import GuiBase,gestionnaire
import math
from arrera_tk import *

class GUICalculatrice(GuiBase) :
    def __init__(self,gestionnaire:gestionnaire):
        super().__init__(gestionnaire,"Calculatrice")
        self.__operateurChooseComplex = ""

    def _mainframe(self):
        self._screen.minsize(500,500)
        self._screen.grid_rowconfigure(0, weight=1)
        self._screen.grid_columnconfigure(0, weight=1)
        #cadre
        # Partie calculatrice
        self.__mainView = aFrame(self._screen)
        fclavier = aFrame(self.__mainView)
        # Partie historique
        self.__fhistorique = aFrame(self._screen)
        # Partie Complex
        self.__fComplex = aFrame(self._screen)
        fEntryNB1 = aFrame(self.__fComplex,fg_color=self.__fComplex.cget("fg_color"))
        fOperateurComplex = aFrame(self.__fComplex,fg_color=self.__fComplex.cget("fg_color"))
        fEntryNB2 = aFrame(self.__fComplex,fg_color=self.__fComplex.cget("fg_color"))
        # Partie pythagore
        self.__fPythagore = aFrame(self._screen)

        # Configuration des frame
        fclavier.grid_columnconfigure(0, weight=1, uniform="col")
        fclavier.grid_columnconfigure(1, weight=1, uniform="col")
        fclavier.grid_columnconfigure(2, weight=1, uniform="col")
        fclavier.grid_columnconfigure(3, weight=1, uniform="col")
        fclavier.grid_columnconfigure(4, weight=1, uniform="col")
        fclavier.grid_columnconfigure(5, weight=1, uniform="col")
        fclavier.grid_columnconfigure(6, weight=1, uniform="col")

        fclavier.grid_rowconfigure(0, weight=1)
        fclavier.grid_rowconfigure(1, weight=1)
        fclavier.grid_rowconfigure(2, weight=1)
        fclavier.grid_rowconfigure(3, weight=1)
        fclavier.grid_rowconfigure(4, weight=1)
        fclavier.grid_rowconfigure(5, weight=1)
        fclavier.grid_rowconfigure(6, weight=1)

        self.__mainView.grid_rowconfigure(0, weight=1)  # la zone texte prend de la place en vertical
        self.__mainView.grid_rowconfigure(1, weight=2)  # la zone clavier peut prendre plus
        self.__mainView.grid_columnconfigure(0, weight=1)

        self.__fhistorique.grid_columnconfigure(0, weight=1)
        self.__fhistorique.grid_rowconfigure(0, weight=1)
        self.__fhistorique.grid_rowconfigure(1, weight=3)

        self.__fComplex.grid_columnconfigure(0, weight=1)
        self.__fComplex.grid_rowconfigure(1, weight=1)
        self.__fComplex.grid_rowconfigure(6, weight=1)

        self.__fPythagore.grid_columnconfigure(0, weight=1)
        self.__fPythagore.grid_columnconfigure(1, weight=0)
        self.__fPythagore.grid_columnconfigure(2, weight=0, minsize=60)
        self.__fPythagore.grid_columnconfigure(3, weight=0)
        self.__fPythagore.grid_columnconfigure(4, weight=1)
        self.__fPythagore.grid_rowconfigure(0, weight=1)
        self.__fPythagore.grid_rowconfigure(3, weight=1)

        # widget
        self.__zoneCalcule = aText(self.__mainView,center=True)
        #touche clavier
        #chiffre
        btnNb0 = aButton(fclavier,text="0",command= lambda : self.__ecritureCarractere("0"))
        btnNb1 = aButton(fclavier,text="1",
                               command= lambda : self.__ecritureCarractere("1"))
        btnNb2 = aButton(fclavier,text="2",
                               command= lambda : self.__ecritureCarractere("2"))
        btnNb3 = aButton(fclavier,text="3",
                               command= lambda : self.__ecritureCarractere("3"))
        btnNb4 = aButton(fclavier,text="4",
                               command= lambda : self.__ecritureCarractere("4"))
        btnNb5 = aButton(fclavier,text="5",
                               command= lambda : self.__ecritureCarractere("5"))
        btnNb6 = aButton(fclavier,text="6",
                               command= lambda : self.__ecritureCarractere("6"))
        btnNb7 = aButton(fclavier,text="7",
                               command= lambda : self.__ecritureCarractere("7"))
        btnNb8 = aButton(fclavier,text="8",
                               command= lambda : self.__ecritureCarractere("8"))
        btnNb9 = aButton(fclavier,text="9",
                               command= lambda : self.__ecritureCarractere("9"))
        btnPI = aButton(fclavier,text="PI",
                              command= lambda : self.__ecritureCarractere("3.1415926535897932"))
        # operateur
        btnVirgule = aButton(fclavier,text=".",
                                   command= lambda : self.__ecritureCarractere("."))
        btnPuissanceDix = aButton(fclavier,text="10^",
                                        command= lambda : self.__ecritureCarractere("*10**"))
        btnEgal = aButton(fclavier,text="=",
                                command=self.__calcule)
        btnplus = aButton(fclavier,text="+",
                                command= lambda : self.__ecritureCarractere("+"))
        btnMoin = aButton(fclavier,text="-",
                                command= lambda : self.__ecritureCarractere("-"))
        btnFois = aButton(fclavier,text="*",
                                command= lambda : self.__ecritureCarractere("*"))
        btnDiviser = aButton(fclavier,text="/",
                                   command= lambda : self.__ecritureCarractere("/"))
        btnParenthese1 = aButton(fclavier,text="(",
                                       command= lambda : self.__ecritureCarractere("("))
        btnParenthese2 = aButton(fclavier,text=")",
                                       command= lambda : self.__ecritureCarractere(")"))
        btnRacine = aButton(fclavier,text="sqrt",
                                  command= lambda : self.__ecritureCarractere("math.sqrt("))
        btnExposant = aButton(fclavier,text="^",
                                    command= lambda : self.__ecritureCarractere("**"))
        btnExpodentiel = aButton(fclavier,text="e^",
                                       command= lambda : self.__ecritureCarractere("math.exp("))
        btnLN = aButton(fclavier,text="ln",
                              command= lambda : self.__ecritureCarractere("math.log(x,math.e)"))
        btnLOG = aButton(fclavier,text="log",
                               command= lambda : self.__ecritureCarractere("math.log(x,10)"))
        #cercle trigo
        btnSIN = aButton(fclavier,text="SIN",
                               command=lambda : self.__ecritureCarractere("math.sin("))
        btnCOS = aButton(fclavier,text="COS",
                               command=lambda : self.__ecritureCarractere("math.cos("))
        btnTAN = aButton(fclavier,text="TAN",
                               command=lambda :self.__ecritureCarractere("math.tan("))
        btnARCSIN = aButton(fclavier,text="SIN-1",
                                  command=lambda : self.__ecritureCarractere("math.asin("))
        btnARCCOS = aButton(fclavier,text="COS-1",
                                  command=lambda : self.__ecritureCarractere("math.acos("))
        btnARCTAN = aButton(fclavier,text="TAN-1",
                                  command=lambda : self.__ecritureCarractere("math.cos("))
        #autre
        btnClear = aButton(fclavier,text="C",command=self.__clearAll)
        btnSuppr = aButton(fclavier,text="CE",command=self.__suppr)
        #btn fonction special
        btnAngle = aButton(fclavier, text="Randian en degres",command=self.__convertiseurDegRad)
        btnPythagore = aButton(fclavier, text="Theoreme de pythagore",command=self.__viewPythagore)
        btnNbComplex = aButton(fclavier, text="Nombre Complex", command=self.__viewComplex)
        btnHist = aButton(fclavier, text="Historique",command=self.__viewHistorique)

        # Frame Historique
        labelHist = aLabel(self.__fhistorique, text="Historique",police_size=30)
        self.__affichageHistorique = aTextScrollable(self.__fhistorique)
        self.__affichageHistorique.disableTextBox()
        btnBackHist = aButton(self.__fhistorique, text="Retour",command=self.__viewCalcule)

        # Frame Complex
        lTitleNombreComplex = aLabel(self.__fComplex, text="Nombre Complex",police_size=30)

        lComplexNB1 = aLabel(fEntryNB1, text=" j ")
        self.__entryComplexNB1_1 = aEntry(fEntryNB1,width=100)
        self.__entryComplexNB1_2 = aEntry(fEntryNB1,width=100)

        lComplexNB2 = aLabel(fEntryNB2, text=" j ")
        self.__entryComplexNB2_1 = aEntry(fEntryNB2,width=100)
        self.__entryComplexNB2_2 = aEntry(fEntryNB2,width=100)

        # Bouton operateur Complex
        btnComplexPlus = aButton(fOperateurComplex, text="+",command=lambda : self.__calcule_complex("plus"))
        btnComplexMoin = aButton(fOperateurComplex, text="-",command=lambda : self.__calcule_complex("moin"))
        btnComplexFois = aButton(fOperateurComplex, text="*",command=lambda : self.__calcule_complex("fois"))
        btnComplexDiv = aButton(fOperateurComplex, text="/",command=lambda : self.__calcule_complex("div"))

        # Resultat Complex
        self.__lResultatComplex = aLabel(self.__fComplex,text="Résultat : en attente",police_size=25)

        btnBackComplex = aButton(self.__fComplex, text="Retour",command=self.__viewCalcule)

        # Partie Pythagore
        lTitlePythagore = aLabel(self.__fPythagore, text="Theoreme de Pythagore",police_size=30)
        self.__entryPythagoreNB1 = aEntryLengend(self.__fPythagore,text="a")
        self.__entryPythagoreNB2 = aEntryLengend(self.__fPythagore,text="b")
        btnPythagoreTheoreme = aButton(self.__fPythagore, text="Theoreme",command=lambda : self.__calcule_pythagore(True))
        btnPythagoreRecibroque = aButton(self.__fPythagore, text="Réciproque",command=lambda : self.__calcule_pythagore(False))
        btnBackPythagore = aButton(self.__fPythagore, text="Retour",command=self.__viewCalcule)

        # Affichage des widgets
        # Clavier
        btnClear.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        btnSuppr.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        btnParenthese1.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        btnParenthese2.grid(row=0, column=3, sticky="nsew", padx=2, pady=2)
        btnDiviser.grid(row=0, column=4, sticky="nsew", padx=2, pady=2)
        btnFois.grid(row=0, column=5, sticky="nsew", padx=2, pady=2)
        btnExposant.grid(row=0, column=6, sticky="nsew", padx=2, pady=2)
        btnRacine.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        btnPuissanceDix.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        btnPI.grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
        btnVirgule.grid(row=1, column=3, sticky="nsew", padx=2, pady=2)
        btnSIN.grid(row=1, column=4, sticky="nsew", padx=2, pady=2)
        btnCOS.grid(row=1, column=5, sticky="nsew", padx=2, pady=2)
        btnTAN.grid(row=1, column=6, sticky="nsew", padx=2, pady=2)
        btnNb7.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
        btnNb8.grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
        btnNb9.grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
        btnMoin.grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
        btnARCSIN.grid(row=2, column=4, sticky="nsew", padx=2, pady=2)
        btnARCCOS.grid(row=2, column=5, sticky="nsew", padx=2, pady=2)
        btnARCTAN.grid(row=2, column=6, sticky="nsew", padx=2, pady=2)
        btnNb4.grid(row=3, column=0, sticky="nsew", padx=2, pady=2)
        btnNb5.grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
        btnNb6.grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
        btnplus.grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
        btnExpodentiel.grid(row=3, column=4, sticky="nsew", padx=2, pady=2)
        btnLN.grid(row=3, column=5, sticky="nsew", padx=2, pady=2)
        btnLOG.grid(row=3, column=6, sticky="nsew", padx=2, pady=2)
        btnNb1.grid(row=4, column=0, sticky="nsew", padx=2, pady=2)
        btnNb2.grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
        btnNb3.grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
        btnEgal.grid(row=4, column=3, rowspan=2, sticky="nsew", padx=2, pady=2)
        btnHist.grid(row=4, column=4, rowspan=2, columnspan=3, sticky="nsew", padx=2, pady=2)
        btnNb0.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        btnAngle.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=2, pady=4)
        btnPythagore.grid(row=6, column=2, columnspan=3, sticky="nsew", padx=2, pady=4)
        btnNbComplex.grid(row=6, column=5, columnspan=2, sticky="nsew", padx=2, pady=4)
        # affichage historique
        labelHist.grid(row=0, column=0)
        self.__affichageHistorique.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=10)
        btnBackHist.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        # Affichage MainView
        self.__zoneCalcule.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        fclavier.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        # Frame Complex
        lTitleNombreComplex.grid(row=0, column=0, pady=(10, 0))

        self.__entryComplexNB1_1.grid(row=0, column=0, padx=(0, 5))
        self.__entryComplexNB1_2.grid(row=0, column=1, padx=(0, 5))
        lComplexNB1.grid(row=0, column=2)

        self.__entryComplexNB2_1.grid(row=0, column=0, padx=(0, 5))
        self.__entryComplexNB2_2.grid(row=0, column=1, padx=(0, 5))
        lComplexNB2.grid(row=0, column=2)

        btnComplexPlus.grid(row=0, column=0, padx=5, pady=5)
        btnComplexMoin.grid(row=0, column=1, padx=5, pady=5)
        btnComplexFois.grid(row=1, column=0, padx=5, pady=5)
        btnComplexDiv.grid(row=1, column=1, padx=5, pady=5)

        fEntryNB1.grid(row=2, column=0, pady=(0, 15))
        fEntryNB2.grid(row=3, column=0, pady=(0, 20))
        fOperateurComplex.grid(row=4, column=0, pady=(0, 15))
        self.__lResultatComplex.grid(row=5, column=0, pady=(0, 10))

        btnBackComplex.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 20))

        lTitlePythagore.grid(row=0, column=0, columnspan=5, sticky="n", pady=(10, 20))
        self.__entryPythagoreNB1.grid(row=1, column=1, sticky="", padx=(10, 0), pady=(0, 12))
        self.__entryPythagoreNB2.grid(row=1, column=3, sticky="", padx=(0, 10), pady=(0, 12))
        btnPythagoreTheoreme.grid(row=2, column=1, sticky="", padx=(10, 0), pady=(6, 0))
        btnPythagoreRecibroque.grid(row=2, column=3, sticky="", padx=(0, 10), pady=(6, 0))

        btnBackPythagore.grid(row=4, column=0, columnspan=5, sticky="ew", padx=0, pady=(15, 10))

        self.__viewCalcule()
        # Configuration de la zone de calcul
        self.__zoneCalcule.bind("<KeyPress-Return>",self.__enterPressed)
        self.__zoneCalcule.bind("<KeyPress>",self.__carractereInterdit)
    
    def __viewCalcule(self):
        self.__fhistorique.grid_forget()
        self.__fComplex.grid_forget()
        self.__fPythagore.grid_forget()
        self.__mainView.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._screen.update()

    def __viewHistorique(self):
        self.__mainView.grid_forget()
        self.__fComplex.grid_forget()
        self.__fPythagore.grid_forget()
        self.__fhistorique.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._screen.update()

    def __viewComplex(self):
        self.__mainView.grid_forget()
        self.__fhistorique.grid_forget()
        self.__fPythagore.grid_forget()
        self.__fComplex.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._screen.update()

    def __viewPythagore(self):
        self.__mainView.grid_forget()
        self.__fhistorique.grid_forget()
        self.__fComplex.grid_forget()
        self.__fPythagore.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._screen.update()

    def __addHistorique(self,texte:str):
        """Ajoute un texte à l'historique de la calculatrice."""
        if not texte:
            return
        self.__affichageHistorique.enableTextBox()
        self.__affichageHistorique.getTextBox().insert(END, texte + "\n")
        self.__affichageHistorique.getTextBox().see(END)
        self.__affichageHistorique.disableTextBox()

    
    def __carractereInterdit(self,event):
        carractereSpeciaux = "'_,?;§!ùµ*£$¤¨@ç|~&²¹#`\°"
        carractereSpeciaux2 = '"'
        if event.char.isalpha():
            return "break"
        elif event.char in carractereSpeciaux:
            return "break"
        elif event.char in carractereSpeciaux2:
            return "break"
        
    def __enterPressed(self,event):
        self.__calcule()
        return "break"
        
    def __ecritureCarractere(self,crc:str):
        self.__zoneCalcule.insert("end",crc)
        self._screen.update()
        
    def __clearAll(self):
        self.__zoneCalcule.delete("1.0",END)
        self._screen.update()
        
    def __suppr(self):
        # Récupérer le contenu actuel du widget Text
        contenu = self.__zoneCalcule.get("1.0", "end-1c")

        if contenu:
            # Supprimer le dernier caractère
            contenu = contenu[:-1]

            # Mettre à jour le widget Text avec le nouveau contenu
            self.__zoneCalcule.delete("1.0", "end")
            self.__zoneCalcule.insert("1.0", contenu)
        self._screen.update()
            
    def __calcule(self):
        contenu = self.__zoneCalcule.get("1.0", END)
        contenu = contenu.replace(" ", "")
        try:
            resultat = eval(contenu)
            self.__affichageHistorique.update()
            self.__zoneCalcule.delete("1.0", END)
            self.__ecritureCarractere(str(resultat))
            self.__addHistorique(contenu + " = " + str(resultat))
        except Exception as e:
            self.__zoneCalcule.delete("1.0", END)
            self.__ecritureCarractere("Erreur 'clear pour uttiliser la calculatrice'")
        self._screen.update()

    def __convertiseurDegRad(self):
        contenu = self.__zoneCalcule.get("1.0", END)
        if contenu == "":
            self.__zoneCalcule.delete("1.0", END)
            self.__ecritureCarractere("Erreur 'clear pour uttiliser la calculatrice'")
        else:
            self.__zoneCalcule.delete("1.0", END)
            try :
                self.__ecritureCarractere(str(math.degrees(int(contenu))))
            except ValueError:
                self.__zoneCalcule.delete("1.0", END)
                self.__ecritureCarractere("Impossible de faire la conversion")

        self._screen.update()

    def __calcule_complex(self,calcule:str):
        """
        :param calcule: plus,moin,fois,div
        :return:
        """
        try :
            nb1_1 = int(self.__entryComplexNB1_1.get())
            nb1_2 = int(self.__entryComplexNB1_2.get())
            nb2_1 = int(self.__entryComplexNB2_1.get())
            nb2_2 = int(self.__entryComplexNB2_2.get())

            self.__entryComplexNB1_1.delete(0, END)
            self.__entryComplexNB1_2.delete(0, END)
            self.__entryComplexNB2_1.delete(0, END)
            self.__entryComplexNB2_2.delete(0, END)
        except ValueError:
            self.__lResultatComplex.configure(text="Erreur 'Nombre invalide'")
            showerror("Erreur", "Veuillez entrer des nombres valides.")
            return

        if calcule == "plus":
            self._gestionnaire.getGestFNC().getFNCCalculatrice().setComplexNb(nb1_1, nb1_2, nb2_1, nb2_2)
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().aditionNbComplex()
        elif calcule == "moin":
            self._gestionnaire.getGestFNC().getFNCCalculatrice().setComplexNb(nb1_1, nb1_2, nb2_1, nb2_2)
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().soustrationNbComplex()
        elif calcule == "fois":
            self._gestionnaire.getGestFNC().getFNCCalculatrice().setComplexNb(nb1_1, nb1_2, nb2_1, nb2_2)
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().multiplicationNbComplex()
        elif calcule == "div":
            self._gestionnaire.getGestFNC().getFNCCalculatrice().setComplexNb(nb1_1, nb1_2, nb2_1, nb2_2)
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().divisionNbComplex()
        else :
            self.__lResultatComplex.configure(text="Erreur 'Operateur inconnu'")
            showerror("Erreur","Operateur inconnu")
            return

        self.__lResultatComplex.configure(text=str(resultat))

    def __calcule_pythagore(self,theoreme:bool):
        """Calcule Pythagore
        :arg theoreme: True pour le théorème de Pythagore, False pour la réciproque
        """
        try:
            a = int(self.__entryPythagoreNB1.getEntry().get())
            b = int(self.__entryPythagoreNB2.getEntry().get())
            self._gestionnaire.getGestFNC().getFNCCalculatrice().setNbPythagore(a, b)
            self.__entryPythagoreNB1.getEntry().delete(0, END)
            self.__entryPythagoreNB2.getEntry().delete(0, END)
            self.__zoneCalcule.delete("1.0", END)
            self.__viewCalcule()
            self._screen.update()
        except ValueError:
            showerror("Erreur", "Veuillez entrer des nombres valides.")
            return

        if theoreme:
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().theoremePythagore()
            calcule = self._gestionnaire.getGestFNC().getFNCCalculatrice().getCalculePythagore()
        else :
            if b > a :
                showerror("Erreur","Impossible de faire la reciproque de Pythagore")
                return
            resultat = self._gestionnaire.getGestFNC().getFNCCalculatrice().reciproquePythagore()
            calcule = self._gestionnaire.getGestFNC().getFNCCalculatrice().getCalculePythagore()

        self.__ecritureCarractere(f"{calcule} = {resultat}")

        self._screen.update()

    def activeCalcule(self):
        self.active()
        self.__viewCalcule()

    def activePythagore(self):
        self.active()
        self.__viewPythagore()

    def activeComplex(self):
        self.active()
        self.__viewComplex()