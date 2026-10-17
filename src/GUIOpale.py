from tkinter.messagebox import showerror, askyesno
from librairy.dectectionOS import OS
from arrera_tk import *
from config.confNeuron import confNeuron
from brain.brain import ABrain
import signal
import os
from datetime import datetime
import threading as th

class GUIOpale:
    def __init__(self):
        self.__emplacementLangue = "language/vouvoiment/"
        self.__objOS = OS()
        self.__logContent = ""


    def active(self):
        self.__guiConf()


    def __guiConf(self):
        screen = aTk(title = "Opale",resizable=False,
                     icon="asset/icon.png",width=500,height=500)

        frameNeuron = aFrame(screen,width=500,height=225,border_width=1)
        frameLangue = aFrame(screen,width=500,height=225,border_width=1)
        frameValidate = aFrame(screen,width=500,height=225,border_width=1)
        # Widget FrameNeuron
        labelTitleNeuron = aLabel(screen,text="Gestion de neurone",police_size=25)
        self.__checkService = aCheckBox(frameNeuron,text="Neuron\nservice",boolean_value=True)
        self.__checkTime = aCheckBox(frameNeuron, text="Neuron\nTemps",boolean_value=True)
        self.__checkOpen = aCheckBox(frameNeuron, text="Neuron\nOpen",boolean_value=True)
        self.__checkRecherche = aCheckBox(frameNeuron, text="Neuron\nRecherche",boolean_value=True)
        self.__checkChatbot = aCheckBox(frameNeuron, text="Neuron\nChatbots",boolean_value=True)
        self.__checkAPI = aCheckBox(frameNeuron, text="Neuron\nAPI",boolean_value=True)
        self.__checkCodeHelp = aCheckBox(frameNeuron, text="Neuron\nCodeHelp",boolean_value=True)
        self.__checkWork = aCheckBox(frameNeuron, text="Neuron\nWork",boolean_value=True)
        self.__checkSocket = aCheckBox(frameNeuron, text="Utilisation des socket",boolean_value=True)
        self.__checkbrief = aCheckBox(frameNeuron, text="Brief", boolean_value=True)
        # Widget FrameLangue
        labelTitleLangue = aLabel(frameLangue,text="Gestion de la langue",police_size=25)
        self.__langSet = aLabel(frameLangue,text="",police_size=25)
        self.__btnVous = aButton(frameLangue,text="Vouvoiment",size=20,command=lambda: self.__setLangue(1))
        self.__btnTutoiement = aButton(frameLangue,text="Tutoiement",size=20,command=lambda: self.__setLangue(2))
        # Widget FrameValidate
        btnValidate = aButton(frameValidate, text="Valider", size=25,
                                                command=lambda : self.__activateAssistantGUI(screen))
        # Affichage
        # FrameNeuron
        labelTitleNeuron.placeTopCenter()
        self.__checkService.place(x=10,  y=30,anchor="nw")
        self.__checkTime.place(x=130, y=30,anchor="nw")
        self.__checkOpen.place(x=260, y=30,anchor="nw")
        self.__checkRecherche.place(x=380, y=30,anchor="nw")
        self.__checkChatbot.place(x=10,  y=85,anchor="nw")
        self.__checkAPI.place(x=130, y=85,anchor="nw")
        self.__checkCodeHelp.place(x=260, y=85,anchor="nw")
        self.__checkWork.place(x=380, y=85,anchor="nw")
        self.__checkSocket.place(x=10, y=160,anchor="nw")
        self.__checkbrief.place(x=260, y=160,anchor="nw")
        # FrameLangue
        labelTitleLangue.placeTopCenter()
        self.__btnVous.placeLeftCenter()
        self.__btnTutoiement.placeRightCenter()
        # FrameValidate
        btnValidate.placeCenter()
        # Frame
        frameNeuron.pack()
        frameLangue.pack()
        frameValidate.pack()
        # Thead Assistant
        self.__thAssistant = th.Thread()

        screen.mainloop()

    def __setLangue(self,mode:int):
        """
        1. Vouvoiement
        2. Tutoiement
        """
        match mode:
            case 1 :
                self.__emplacementLangue = "language/vouvoiment/"
                self.__langSet.configure(text="Vouvoiment")
            case 2 :
                self.__emplacementLangue = "language/tutoiment/"
                self.__langSet.configure(text="Tutoiement")
            case _ :
                self.__emplacementLangue = "language/vouvoiment/"
                self.__langSet.configure(text="Vouvoiment")
        self.__btnVous.place_forget()
        self.__btnTutoiement.place_forget()
        self.__langSet.placeCenter()

    def __setConfig(self):
        try :
            if (not self.__checkService.getBooleanVar().get() and
                    not self.__checkTime.getBooleanVar().get() and
                    not self.__checkOpen.getBooleanVar().get() and
                    not self.__checkRecherche.getBooleanVar().get() and
                    not self.__checkChatbot.getBooleanVar().get() and
                    not self.__checkAPI.getBooleanVar().get() and
                    not self.__checkCodeHelp.getBooleanVar().get() and
                    not self.__checkCodeHelp.getBooleanVar().get()):
                showerror("Assistant"," Vous devez activer au moins un neurone.")
                return False

            self.__config = confNeuron(name="Opale",
                                       lang="fr",
                                       asset="asset/",
                                       icon="asset/icon.png",
                                       bute="developper un algo de ChatBot qui sera inclut dans SIX et Ryley",
                                       createur="Pauchet Baptiste",
                                       listFonction=["ouvrir une application", "aider sur les recherches de internet", "donner la meteo",
                                                     "faire un résumer des actualités"],
                                       moteurderecherche="google",
                                       etatService=int(self.__checkService.get()),
                                       etatTime=int(self.__checkTime.get()),
                                       etatOpen=int(self.__checkOpen.get()),
                                       etatSearch=int(self.__checkRecherche.get()),
                                       etatChatbot=int(self.__checkChatbot.get()),
                                       etatApi=int(self.__checkAPI.get()),
                                       etatCodehelp=int(self.__checkCodeHelp.get()),
                                       etatWork=int(self.__checkWork.get()),
                                       etatSocket=int(self.__checkSocket.get()),
                                       brief_enable=int(self.__checkbrief.get()),
                                       lienDoc="www.google.com",
                                       fichierLangue=str(self.__emplacementLangue),
                                       fichierKeyword="keyword/",
                                        voiceAssistant=True)
            return True
        except Exception as e:
            print(f"Erreur lors de la création de la configuration : {e}")
            return False


    def __activateAssistantGUI(self,screen:aTk):
        """
        Fonction qui permet de lancer l'assistant GUI
        """
        if self.__setConfig():
            if self.__startAssistantBrain():
                for widget in screen.winfo_children():
                    widget.destroy()
                self.__GUIAssistant(screen)
                self.__bootAssistant()
            else:
                showerror("Erreur", "Impossible de démarrer l'assistant (Erreur de chargement de l'IA). Vérifiez vos logs.")
        else:
            print("Erreur lors de la création de la configuration de l'assistant.")


    def __GUIAssistant(self, screen:aTk = None):
        if screen is None:
            screen = aTk(theme_file="asset/theme/theme_default.json",
                         title="Opale", resizable=False,
                         icon="asset/icon.png", width=500, height=500)
        else:
            screen.title("Opale Assistant")
            screen.geometry("500x500")
            screen.resizable(False, False)

        screen.protocol("WM_DELETE_WINDOW", self.__close)

        # Frame
        frameAssistant = aFrame(screen, width=500, height=225)
        frameUser = aFrame(screen, width=350, height=50)

        # Widget
        labelTitle = aLabel(screen, text="Assistant Opale", police_size=25)

        self.__labelAssistantText = aLabel(frameAssistant, text="TEXTE", police_size=20)
        self.__labelAssistantNumber = aLabel(frameAssistant, text="NUMBER", police_size=20)

        entryUser = aEntry(frameUser, width=200)
        btnSend = aButton(frameUser, text="Envoyer",size=15,
                                            command= lambda : self.__sendAssistantMessage(entryUser,screen))
        btnOpen = aButton(screen, text="OPEN",width=10,command=self.__viewOpen)
        self.__labelGeneration = aLabel(screen,text="Generation...",police_size=15)

        # Affichage

        labelTitle.placeTopCenter()
        frameAssistant.placeCenter()
        frameUser.placeBottomRight()

        self.__labelAssistantText.placeTopCenter()
        self.__labelAssistantNumber.placeBottomCenter()

        entryUser.placeLeftCenter()
        btnSend.placeRightCenter()

        btnOpen.placeBottomLeft()

        self.__keyboard(screen,entryUser)

        screen.after(200, self.__updateAssistant,screen)

    def __viewOpen(self):
        w = aTopLevel(title="Ouvert par l'assistant",width=300, height=100)

        word = aLabel(w,text="WORD",police_size=15)
        project = aLabel(w,text="PROJECT",police_size=15)
        tableur = aLabel(w,text="TABLEUR",police_size=15)

        word.placeCenterLeft()
        project.placeCenterRight()
        tableur.placeCenter()

        if self.__assistantBrain.getWord():
            word.configure(fg_color="green")
        else:
            word.configure(fg_color="red")

        if self.__assistantBrain.getProject():
            project.configure(fg_color="green")
        else:
            project.configure(fg_color="red")

        if self.__assistantBrain.getTableur():
            tableur.configure(fg_color="green")
        else:
            tableur.configure(fg_color="red")


    def __startAssistantBrain(self):
        try :
            self.__assistantBrain = ABrain(config=self.__config)
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage de l'assistant Brain : {e}")
            return False

    def __bootAssistant(self):
        """
        Fonction qui permet de lancer l'assistant
        """

        try :
            self.__labelAssistantText.configure(text=self.__assistantBrain.boot(), wraplength=200
                                                ,justify="left")
        except Exception as e:
            self.__labelAssistantText.configure(text=f"Erreur lors du boot de l'assistant : {e}",wraplength=200
                                                ,justify="left")

    def __sendAssistantMessage(self,entry:aEntry,screen:aTk):
        message = entry.get()
        if message:
            entry.delete(0, 'end')  # Clear the entry after sending
            t = th.Thread(target=self.__assistantBrain.neuron, args=(message,))
            t.start()
            if not self.__thAssistant.is_alive():
                self.__thAssistant = t
                self.__updateRequetteAssistant(screen, message)
        else:
            self.__labelAssistantText.configure(text="Veuillez entrer un message.", wraplength=200
                                                ,justify="left")

    def __updateRequetteAssistant(self,screen:aTk,message:str):
        q_size = self.__assistantBrain.get_ia_queue_size()
        if self.__thAssistant.is_alive() or q_size > 0:
            if q_size > 1:
                self.__labelGeneration.configure(text=f"Generation ({q_size} en attente)...")
            else:
                self.__labelGeneration.configure(text="Generation...")
            self.__labelGeneration.placeBottomRight()
            screen.after(500,self.__updateRequetteAssistant,screen,message)
        else :
            self.__labelGeneration.place_forget()
            nb = self.__assistantBrain.getValeurSortie()
            texte = self.__assistantBrain.getListSortie()
            self.__labelAssistantText.configure(text=texte[0], wraplength=200
                                                ,justify="left")
            self.__labelAssistantNumber.configure(text=str(nb))
            self.__addLog(nb,texte[0],message)
            if nb == 15:
                self.__close()


    def __keyboard(self,win:aTk,entry:aEntry):
        def anychar(event):
            if self.__objOS.osWindows():
                if event.keycode == 13:
                    self.__sendAssistantMessage(entry,win)
            elif self.__objOS.osLinux():
                if event.keycode == 36:
                    self.__sendAssistantMessage(entry,win)
            elif self.__objOS.osMac():
                if event.keycode == 603979789:
                    self.__sendAssistantMessage(entry,win)
        win.bind("<Key>", anychar)

    def __close(self):
        out = askyesno("Fermeture","Enregistrer le log avant de quitter ?")
        self.__assistantBrain.shutdown()
        if out:
            if self.__saveLog():
                print("Log sauvegardé avec succès.")
            else:
                print("Erreur lors de la sauvegarde du log.")

        if self.__objOS.osWindows():
            os.kill(os.getpid(), signal.SIGINT)
        elif self.__objOS.osLinux() or self.__objOS.osMac() :
            os.kill(os.getpid(), signal.SIGKILL)

    def __addLog(self,nbOut:int,outTexte:str,inTexte:str):
        self.__logContent += inTexte + " -> " + str(nbOut) + " : " + outTexte + "\n"

    def __saveLog(self):
        date = datetime.now().strftime("%d-%m-%Y-%H-%M")
        if self.__objOS.osLinux() or self.__objOS.osMac():
            home = os.path.expanduser("~")
            file = home+"/log_assistant/log_" + date + ".txt"
        else :
            home = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")
            file = home+"/log_assistant/log_" + date + ".txt"

        if not os.path.isfile(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)

        try :
            with open(file,"w",encoding="utf-8") as f:
                f.write(self.__logContent)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du log : {e}")
            return False


    def __updateAssistant(self,screen:aTk=None):

        if self.__assistantBrain.updateAssistant():
            varOut = self.__assistantBrain.getValeurSortie()
            self.__labelAssistantText.configure(text=self.__assistantBrain.getListSortie()[0], wraplength=200)
            self.__labelAssistantNumber.configure(text=str(varOut))
            if varOut == 15:
                self.__close()

        screen.after(1000,self.__updateAssistant,screen)