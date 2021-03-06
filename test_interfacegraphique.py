# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 14:43:25 2022

@author: sshan
"""

from tkinter import *
from tkinter import filedialog 


##Création de la fenêtre
fenetre=Tk()

##Donner un titre à ma fenetre
fenetre.title("Traitement des données du centre Oscar Lambret")

##Changer taille fenêtre
fenetre.geometry("640x480")

def browseFiles(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
       
    
    label_file_explorer.configure(text="File Opened: "+filename)

label_file_explorer = Label(fenetre,  
                            text = "File Explorer using Tkinter", 
                            width = 100, height = 4,  
                            fg = "blue") 
 

def aide():
  # Création de la fenêtre
  fenetreAide = Tk()
  fenetreAide.title("Aide")

  # Texte :
  champ_label = Label(fenetreAide, text="Bienvenue dans la fenêtre aide ! :D ")
  champ_label.grid(row=1, column=0)
  champ_label = Label(fenetreAide, text="Cependant le logiciel n'est pas encore finis")
  champ_label.grid(row=2, column=0)
  champ_label = Label(fenetreAide, text="")
  champ_label.grid(row=3, column=0)
  champ_label = Label(fenetreAide, text="En cours de développement")
  champ_label.grid(row=4, column=0)


##----------Titre du graphique---------##
#plt.title(titre.get(), fontsize=(ValeurTitre.get()), fontweight='bold')



#----Création barre menu

menubar = Menu(fenetre)

menu1= Menu(menubar, tearoff=0)
menubar.add_command(label="Charger", command=browseFiles)

menu2 = Menu(menubar, tearoff=0)
menubar.add_command(label= "Aide", command=aide)

menu3 = Menu(menubar, tearoff=0)
menubar.add_command(label="Quitter")

menu4 = Menu(menubar, tearoff=0)
menubar.add_command(label="Réinitialiser")

menu5 = Menu(menubar, tearoff=0)
menubar.add_command(label="Enregistrer")


fenetre.config(menu=menubar)


##Afficher la fenêtre
fenetre.mainloop()